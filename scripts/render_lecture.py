"""Render a raw lecture recording for upload in one ffmpeg pass: cut, speed up with the pitch kept, tone-map
iPhone HDR (HLG) to SDR, take the sound from a separate recorder if there is one, and put the intro and
outro around it.

Run:
  python scripts/render_lecture.py --video <camera.MOV> [--audio <recorder.mp3> --align <align.json>]
      [--cuts <cut list> --cuts-fps 30] [--start S] [--end S] [--speed 1.25]
      --intro <intro.mp4> --outro <outro.mp4> -o <out.mp4> [--encoder qsv|x264] [--npl 200]
  python scripts/render_lecture.py ... --window 1800 1860 -o sample.mp4
      (a short sample of master time 1800-1860 s, no intro/outro, to look at before a full render)
Expected wall-clock: ~0.5x realtime of the OUTPUT, all cores busy: ~1.7 h for 55 min of finished video
(30 s --window samples of Դաս 6-8, 2026-10-24: 0.42-0.53x alone, 0.3x with other ffmpeg jobs running).
A guess until a full lecture is measured. Pieces on Դաս 7: HEVC 10-bit decode ~70 fps on the CPU (the
d3d11va hardware decoder is no faster), decode + tone map 27 s per 20 s of camera.
Progress and an ETA are logged every 30 s.
Sync is checked by scripts/non_essential/render_sync_check.py (audio only, seconds), not by a sample:
after atempo the two tracks no longer correlate sample by sample (lags scatter +-40 ms), at 1x they do.

Timelines. Cut lists, --start/--end and --window are in MASTER time: the audio file's timeline when
--audio is given (the audio-only caption uploads of Դաս 6 and 7 are that file from 0:00, so their
transcripts are in master time), else the camera's. The camera sits on it at
master = offset0 + t_camera * (1 + drift), with offset0 and drift from scripts/align_audio.py's JSON.
Cut boundaries are snapped to the camera's frame grid, and the audio is cut on a 1 ms grid at the same
points, so picture and sound stay together however many cuts there are.

Sound after the camera stops (Դաս 6's last 17 min): --tail-slides lists which slide is on screen from which
master time on; the stretches after the camera's last frame show those slides full screen, cut and sped up
like the rest. It needs an explicit --end: the audio file can run far past the lecture (Դաս 6's: 17 h).

The intro and outro play at normal speed (as in Դաս 2-5's Premiere projects); only the lecture is sped
up. Output: 1920x1080, --fps (25, like the intro clips and Դաս 0, 2, 4, 5), BT.709 SDR, AAC 48 kHz stereo.
Written to <out>.part.mp4 and renamed when ffmpeg finishes and the duration checks pass.
"""
import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/render_lecture.log", encoding="utf-8")])
log = logging.getLogger(__name__)

W, H = 1920, 1080
AUDIO_SR = 48000
AUDIO_STEP_S = 0.001  # the audio is selected in 1 ms chunks (48 samples)
HDR_TRANSFERS = {"arib-std-b67", "smpte2084"}
CUT = re.compile(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)")
ENCODERS = {
    # 20 rather than 22 (the user, 2026-10-24): crisper slide text after YouTube's re-encode, ~1.5x the size
    "qsv": ["-c:v", "h264_qsv", "-preset", "slow", "-global_quality", "20"],
    "x264": ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-profile:v", "high"],
}
AUDIO_OUT = ["-c:a", "aac", "-b:a", "160k", "-ar", str(AUDIO_SR), "-ac", "2"]
COLOR_OUT = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
EST_VIDEO_MBPS = 4.0  # for the free-disk check only
DURATION_TOLERANCE_S = 0.5


def probe(path: Path) -> dict:
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration:stream=index,codec_type,width,height,r_frame_rate,color_transfer",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def ffmpeg_major(ffmpeg: str) -> int:
    out = subprocess.run([ffmpeg, "-hide_banner", "-version"], capture_output=True, text=True, check=True).stdout
    m = re.match(r"ffmpeg version n?(\d+)\.", out)
    if not m:
        raise ValueError(f"can't read the version of {ffmpeg}: {out[:80]!r}")
    return int(m[1])


def tc_seconds(tc: str, fps: int) -> float:
    h, m, s, f = map(int, tc.split(":"))
    if f >= fps:
        raise ValueError(f"{tc}: frame {f} at {fps} fps")
    return (h * 60 + m) * 60 + s + f / fps


def read_cuts(path: Path, fps: int) -> list[tuple[float, float]]:
    cuts = [(tc_seconds(m[1], fps), tc_seconds(m[2], fps))
            for line in path.read_text(encoding="utf-8").splitlines() if (m := CUT.match(line.strip()))]
    if not cuts:
        raise ValueError(f"no 'Cut N  H:MM:SS:FF  ->  H:MM:SS:FF' lines in {path}")
    return sorted(cuts)


def keep_segments(start: float, end: float, cuts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """[start, end) minus the cuts."""
    segs, pos = [], start
    for a, b in cuts:
        if b <= pos or a >= end:
            continue
        if a > pos:
            segs.append((pos, a))
        pos = max(pos, b)
    if pos < end:
        segs.append((pos, end))
    return segs


def rate(r: str) -> float:
    num, den = r.split("/")
    return int(num) / int(den)


def select_expr(segs: list[tuple[float, float]], shift: float) -> str:
    # Each frame / chunk is kept if its time t is in [a - shift, b - shift): shifting by half a step keeps
    # exactly the grid points from a up to (not including) b, whatever the float rounding.
    return "+".join(f"gte(t,{a - shift:.6f})*lt(t,{b - shift:.6f})" for a, b in segs)


def read_tail_slides(path: Path, slides_dir: Path) -> list[tuple[float, Path]]:
    """(master time, image) per line 'H:MM:SS.s  image.png'; '#' starts a comment. Each slide stays on until
    the next line's time, the last one to the end."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        t, name = line.split(None, 1)
        h, m, s = t.split(":")
        img = slides_dir / name.strip()
        if not img.is_file():
            raise FileNotFoundError(f"{path}: {img} not found")
        out.append(((int(h) * 60 + int(m)) * 60 + float(s), img))
    if not out or [t for t, _ in out] != sorted(t for t, _ in out):
        raise ValueError(f"{path}: no slides, or times not increasing")
    return out


def tail_frames(tail_segs, slides, speed: float, fps: int) -> list[tuple[Path, int]]:
    """(image, number of output frames) for the kept stretches after the camera: each stretch split where the
    slide changes, at `speed`, frame counts from cumulative times so the total can't drift from the sound."""
    parts = []
    for a, b in tail_segs:
        cuts = [a] + [t for t, _ in slides if a < t < b] + [b]
        for x, y in zip(cuts, cuts[1:]):
            img = [p for t, p in slides if t <= x + 1e-6][-1]
            if parts and parts[-1][0] == img:
                parts[-1][1] += y - x
            else:
                parts.append([img, y - x])
    out, cum, done = [], 0.0, 0
    for img, d in parts:
        cum += d / speed
        n = round(cum * fps) - done
        done += n
        if n > 0:
            out.append((img, n))
    return out


def build_graph(args, src_rate: str, hdr: bool, segs, offset0: float, drift: float, inputs: dict,
                seeks: dict, vsegs=None, tail_inputs=(), dips=()) -> str:
    """seeks: input index -> the -ss given to that input; its timestamps then start there, so it is added back.
    segs: the kept master-time stretches (the sound); vsegs: those the camera covers (default: all);
    tail_inputs: (input index, frames) per slide shown after the camera, in order; dips: output times (from
    the lecture's start) where the picture jumps, each dipped to black for args.dip s on either side."""
    vsegs = segs if vsegs is None else vsegs
    W, H = getattr(args, "size", (1920, 1080))
    k = 1 + drift
    v_step = k / rate(src_rate)
    vsel = select_expr(vsegs, v_step / 2)
    asel = select_expr([(round(a, 3), round(b, 3)) for a, b in segs], AUDIO_STEP_S / 2)
    tone = (f"zscale=t=linear:npl={args.npl},format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
            "zscale=t=bt709:m=bt709:r=tv," if hdr else "")
    small = f"scale={W}:{H}," if (W, H) != (1920, 1080) else ""   # --check: tone-map small frames, much cheaper
    fit = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    # --denoise: a low cut for rumble and a light spectral denoise for steady hiss (the user picked "light" on
    # A/B files, 2026-10-24: pause noise -4.9 dB on Դաս 7's recorder, -2.3 dB on Դաս 8's camera mic, where
    # most of what remains is room sound; the speech loudness did not change)
    den = "highpass=f=80,afftdn=nr=12:nf=-50:tn=1," if getattr(args, "denoise", False) else ""
    aform = f"aresample={AUDIO_SR},aformat=sample_fmts=fltp:channel_layouts=stereo"
    a_cut = f"asetnsamples=n={round(AUDIO_SR * AUDIO_STEP_S)}:p=0,aselect='{asel}',asetpts=N/SR/TB,atempo={args.speed}"
    # A camera microphone is ~10 dB quieter than the recorders (Դաս 8: -35.6 LUFS; Դաս 6/7 recorders -22.8 /
    # -25.3; published Դաս 4/5 -25.6 / -25.2) and YouTube never turns quiet videos up. Plain gain, then a
    # peak limiter for the knocks that already reach 0 dBFS (level=0: no auto-gain of its own).
    gain = f",volume={args.gain_db}dB,alimiter=limit=0.891:level=0" if args.gain_db else ""
    cam, aud = inputs.get("camera"), inputs["audio"]
    g = [f"[{aud}:a:0]{aform},{den}asetpts=PTS+{seeks[aud]:.6f}/TB,{a_cut}{gain}[ma]"]
    parts = []
    if vsegs:
        to_master = f"(PTS+{seeks[cam]:.6f}/TB)*{k:.9f}+{offset0:.6f}/TB"
        g.append(f"[{cam}:v:0]fps={src_rate},setpts={to_master},select='{vsel}',setpts=N*{k:.9f}/FRAME_RATE/TB,"
                 f"setpts=PTS/{args.speed},fps={args.fps},{small}{tone}{fit},format=yuv420p[camv]")
        parts.append("[camv]")
    for j, (i, n) in enumerate(tail_inputs):  # slides: RGB -> BT.709 limited range, like the tone-mapped camera
        g.append(f"[{i}:v:0]trim=end_frame={n},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=decrease:"
                 f"out_color_matrix=bt709:out_range=tv,format=yuv420p,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=white,"
                 f"setsar=1[slide{j}]")
        parts.append(f"[slide{j}]")
    g.append(f"{''.join(parts)}concat=n={len(parts)}:v=1:a=0[mv0]" if len(parts) > 1 else f"{parts[0]}null[mv0]")
    # A fixed camera on a walking lecturer: a cut makes him jump, so dip to black and back across it. The fade
    # filter alone keeps everything after a fade-out black; 'enable' limits each one to its own window.
    d = args.dip
    fades = [f"fade=t=out:st={j - d:.3f}:d={d}:enable='between(t,{j - d:.3f},{j:.3f})',"
             f"fade=t=in:st={j:.3f}:d={d}:enable='between(t,{j:.3f},{j + d:.3f})'" for j in dips if d > 0]
    g.append(f"[mv0]{','.join(fades) or 'null'}[mv]")
    if args.window:
        if vsegs and aud != cam:  # the camera's own sound on the same timeline, for render_sync_check.py
            g.append(f"[{cam}:a:0]{aform},asetpts={to_master},{a_cut}[ca]")
        return ";\n".join(g)
    for name in ("intro", "outro"):
        i = inputs[name]
        g.append(f"[{i}:v:0]{fit},fps={args.fps},format=yuv420p[{name}v]")
        g.append(f"[{i}:a:0]{aform}[{name}a]")
    g.append("[introv][introa][mv][ma][outrov][outroa]concat=n=3:v=1:a=1[v][a]")
    return ";\n".join(g)


def run_ffmpeg(cmd: list[str], expected_s: float) -> None:
    """Run ffmpeg with -progress on stdout; log progress and an ETA every 30 s; fail loudly."""
    t0 = time.time()
    last = t0
    with tempfile.TemporaryFile() as err:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=err, text=True)
        for line in proc.stdout:
            # "out_time_us=N/A" until the first output frame (a long seek can take > 30 s)
            if line.startswith("out_time_us=") and "N/A" not in line and time.time() - last >= 30:
                last = time.time()
                done = max(int(line.split("=")[1]), 0) / 1e6
                elapsed = last - t0
                eta = elapsed * (expected_s - done) / done if done > 0 else float("nan")
                log.info(f"{done / 60:.1f} of {expected_s / 60:.1f} min rendered, {elapsed / 60:.1f} min elapsed, "
                         f"~{eta / 60:.1f} min left ({done / elapsed:.2f}x realtime)")
        proc.wait()
        if proc.returncode != 0:
            err.seek(0)
            log.error(f"ffmpeg failed ({proc.returncode}):\n{err.read().decode('utf-8', 'replace')[-3000:]}")
            raise RuntimeError(f"ffmpeg failed with exit code {proc.returncode}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--audio", type=Path, help="separate audio (recorder); its timeline becomes master time")
    ap.add_argument("--align", type=Path, help="align_audio.py JSON (offset0_s, drift_ppm); needed with --audio")
    ap.add_argument("--cuts", type=Path, help="cut list, 'Cut N  H:MM:SS:FF  ->  H:MM:SS:FF' lines, master time")
    ap.add_argument("--cuts-fps", type=int, help="frame rate of the cut list's :FF fields")
    ap.add_argument("--start", type=float, help="master time to start at (default: the camera's first frame)")
    ap.add_argument("--end", type=float, help="master time to end at (default: the camera's last frame)")
    ap.add_argument("--speed", type=float, default=1.25)
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--npl", type=int, default=200,
                    help="HLG nominal peak for the tone map; 200 matches Դաս 2-5's brightness (mean luma ~150)")
    ap.add_argument("--gain-db", type=float, default=0.0,
                    help="gain on the lecture's sound, with a peak limiter (tried +10..+18 on Դաս 8's camera "
                         "sound; the user kept it at 0, DECISIONS #32)")
    ap.add_argument("--intro", type=Path)
    ap.add_argument("--outro", type=Path)
    ap.add_argument("--encoder", choices=sorted(ENCODERS), default="qsv")
    ap.add_argument("--ffmpeg", default="ffmpeg",
                    help="ffmpeg binary; the portable 9.0.2 (C:/Users/hayk_/tools/ffmpeg-9/...) runs the same zscale "
                         "tone map 11-23%% faster than the system 5.1 (alternating runs, 2026-10-24)")
    ap.add_argument("--tail-slides", type=Path,
                    help="slides for the sound after the camera stops: 'H:MM:SS.s  image' per line (master time); "
                         "needs an explicit --end")
    ap.add_argument("--slides-dir", type=Path, help="folder of the --tail-slides images")
    ap.add_argument("--denoise", action="store_true", help="80 Hz low cut + light afftdn on the lecture's sound")
    ap.add_argument("--check", action="store_true",
                    help="a quick full-length check copy: 256x144, camera keyframes only (~1 picture/s; decoding "
                         "the 1080p HEVC is the bottleneck), everything else (cuts, dips, slides, sound) as final")
    ap.add_argument("--dip", type=float, default=0.25,
                    help="at each cut in the camera footage and at the switch to slides: fade to black over this "
                         "many seconds and back (the user, 2026-10-24: so the lecturer doesn't teleport); 0 = hard cut")
    ap.add_argument("--window", type=float, nargs=2, metavar=("A", "B"), help="render only master time A-B")
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()

    t0 = time.time()
    args.size = (256, 144) if args.check else (W, H)
    if args.output.exists():
        raise FileExistsError(f"{args.output} already exists; pass another -o or move it first")
    if bool(args.audio) != bool(args.align):
        raise ValueError("--audio and --align go together")
    if args.cuts and not args.cuts_fps:
        raise ValueError("--cuts needs --cuts-fps")
    if not args.window and not (args.intro and args.outro):
        raise ValueError("a full render needs --intro and --outro (or use --window for a sample)")
    if args.tail_slides and not (args.slides_dir and args.audio):
        raise ValueError("--tail-slides needs --slides-dir, and --audio (sound that goes on after the camera)")
    if args.tail_slides and not args.window and args.end is None:
        # The audio's own end can be far off: Դաս 6's recorder ran 17 h, its cut list covers the first 82 min
        raise ValueError("with --tail-slides pass --end (the master time the cut list runs to)")

    info = probe(args.video)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    src_fps = rate(v["r_frame_rate"])
    hdr = v.get("color_transfer") in HDR_TRANSFERS
    cam_len = float(info["format"]["duration"])
    offset0 = drift = 0.0
    master_len = cam_len
    if args.audio:
        al = json.loads(args.align.read_text(encoding="utf-8"))
        if al["camera"] != args.video.name or al["audio"] != args.audio.name:
            raise ValueError(f"{args.align} is for {al['camera']} + {al['audio']}, not these files")
        offset0, drift = al["offset0_s"], al["drift_ppm"] / 1e6
        master_len = float(probe(args.audio)["format"]["duration"])
    cover = (max(offset0, 0.0), min(offset0 + (cam_len - 1 / src_fps) * (1 + drift), master_len))
    log.info(f"camera {args.video.name}: {v['width']}x{v['height']} @ {src_fps:.3f} fps, {cam_len / 60:.1f} min, "
             f"{'HDR ' + v['color_transfer'] + ' -> SDR' if hdr else 'SDR'}; covers master {cover[0]:.2f}-"
             f"{cover[1]:.2f} s (offset {offset0:.4f} s, drift {drift * 1e6:.1f} ppm)")

    slides = read_tail_slides(args.tail_slides, args.slides_dir) if args.tail_slides else []
    start = args.window[0] if args.window else (args.start if args.start is not None else cover[0])
    default_end = master_len if slides else cover[1]
    end = args.window[1] if args.window else (args.end if args.end is not None else default_end)
    cuts = read_cuts(args.cuts, args.cuts_fps) if args.cuts else []
    step = (1 + drift) / src_fps
    snap = lambda x: offset0 + round((x - offset0) / step) * step  # noqa: E731
    segs = [(snap(a), snap(b)) for a, b in keep_segments(start, end, cuts)]
    segs = [(a, b) for a, b in segs if b - a >= step]
    if not segs:
        raise ValueError(f"nothing left to render in master {start:.2f}-{end:.2f} s")
    # With slides, everything from the camera's last frame on is the tail: split the stretches there
    cam_end = snap(cover[1]) if slides else float("inf")
    vsegs = [(a, min(b, cam_end)) for a, b in segs if a < cam_end - step / 2]
    tail_segs = [(max(a, cam_end), b) for a, b in segs if b > cam_end + step / 2]
    outside = [(a, b) for a, b in vsegs if a < cover[0] - step or b > cover[1] + step]
    if outside:
        raise ValueError(f"segments outside the camera's picture (master {cover[0]:.2f}-{cover[1]:.2f} s): "
                         f"{outside[:3]}; audio-only stretches need --tail-slides")
    if tail_segs and tail_segs[0][0] < slides[0][0] - step:
        raise ValueError(f"the first slide starts at {slides[0][0]:.2f} s, after the camera's end {cam_end:.2f} s")
    tail = tail_frames(tail_segs, slides, args.speed, args.fps) if tail_segs else []
    if tail:
        log.info(f"after the camera ({cam_end:.2f} s): " + ", ".join(f"{p.name} {n / args.fps:.1f} s" for p, n in tail))
    # Where the picture jumps, on the output timeline: between camera stretches, and from the camera to slides
    dips, cum = [], 0.0
    for i, (a, b) in enumerate(vsegs):
        cum += b - a
        if i < len(vsegs) - 1 or tail:
            dips.append(cum / args.speed)
    if dips and args.dip > 0:
        log.info(f"{len(dips)} picture jumps get a {2 * args.dip:.2f} s dip to black")
    kept = sum(b - a for a, b in segs)
    clips = 0.0 if args.window else sum(float(probe(p)["format"]["duration"]) for p in (args.intro, args.outro))
    expected = clips + kept / args.speed
    log.info(f"{len(segs)} segments, {len(cuts)} cuts: keeps {kept / 60:.1f} min of master {start:.1f}-{end:.1f} s; "
             f"at {args.speed}x plus {clips:.1f} s of intro/outro = {expected / 60:.2f} min")

    est_gb = expected * (EST_VIDEO_MBPS + 0.2) / 8 / 1000
    free_gb = shutil.disk_usage(args.output.resolve().parent).free / 1e9
    if free_gb < est_gb * 1.2 + 0.5:
        raise RuntimeError(f"{free_gb:.1f} GB free on the output's drive, the render needs ~{est_gb:.1f} GB "
                           "plus a margin; free space first")

    # Read each input only from ~1 s before the first kept frame to ~1 s after the last one: decoding runs at
    # ~70 fps here, a sample at 36 min took > 5 min without the seek, and without -t ffmpeg goes on decoding
    # to the end of the file after select has passed its last frame. The camera's seek is a whole number
    # of frames, so the fps filter's grid stays on the camera's frame times, which the cuts were snapped to.
    src_fps = rate(v["r_frame_rate"])
    cam_ss = cam_t = None
    if vsegs:
        # --check decodes keyframes only (~0.9 s apart on the iPhone files): start 3 s early so one comes
        # before the first kept frame; a missing first frame would shift all the picture after it
        lead = 3.0 if args.check else 1.0
        cam_ss = max(0, int(((vsegs[0][0] - offset0) / (1 + drift) - lead) * src_fps)) / src_fps
        cam_t = (vsegs[-1][1] - offset0) / (1 + drift) + 1.0 - cam_ss
    aud_ss = max(0, int((segs[0][0] - 1.0) * 1000)) / 1000
    aud_t = segs[-1][1] + 1.0 - aud_ss
    inputs, seeks, cmd = {}, {}, [args.ffmpeg, "-v", "error", "-y", "-nostats", "-progress", "pipe:1"]
    for name, path, ss, t in [("camera", args.video if vsegs else None, cam_ss, cam_t),
                              ("audio", args.audio, aud_ss, aud_t),
                              ("intro", args.intro, 0.0, None), ("outro", args.outro, 0.0, None)]:
        if path and not (args.window and name in ("intro", "outro")):
            inputs[name] = len(inputs)
            seeks[inputs[name]] = ss
            skip = ["-skip_frame", "nokey"] if args.check and name == "camera" else []
            cmd += skip + ["-ss", f"{ss:.6f}"] + (["-t", f"{t:.6f}"] if t else []) + ["-i", str(path)]
    inputs.setdefault("audio", inputs.get("camera"))
    tail_inputs = []
    for img, n in tail:  # a still image repeated at the output rate; trim keeps exactly n frames
        tail_inputs.append((cmd.count("-i"), n))
        cmd += ["-loop", "1", "-framerate", str(args.fps), "-t", f"{n / args.fps + 1:.3f}", "-i", str(img)]
    graph = build_graph(args, v["r_frame_rate"], hdr, segs, offset0, drift, inputs, seeks, vsegs, tail_inputs, dips)
    part = args.output.with_name(args.output.stem + ".part.mp4")
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "graph.txt"
        script.write_text(graph, encoding="utf-8")
        cmd += (["-/filter_complex", str(script)] if ffmpeg_major(args.ffmpeg) >= 7
                else ["-filter_complex_script", str(script)])   # 7.0 replaced it; 9.0 removed the old option
        if args.window:
            cmd += ["-map", "[mv]", "-map", "[ma]"] + (["-map", "[ca]"] if "[ca]" in graph else [])
        else:
            cmd += ["-map", "[v]", "-map", "[a]"]
        cmd += [*ENCODERS[args.encoder], *COLOR_OUT, *AUDIO_OUT, "-movflags", "+faststart", str(part)]
        log.info(f"ffmpeg: {len(graph):,} chars of filter graph, encoder {args.encoder}")
        run_ffmpeg(cmd, expected)

    out = probe(part)
    got = float(out["format"]["duration"])
    if abs(got - expected) > DURATION_TOLERANCE_S:
        raise RuntimeError(f"{part}: duration {got:.2f} s, expected {expected:.2f} s; left as .part")
    part.rename(args.output)
    elapsed = time.time() - t0
    log.info(f"wrote {args.output} ({args.output.stat().st_size / 1e6:.0f} MB, {got / 60:.2f} min, "
             f"{args.output.stat().st_size * 8 / got / 1e6:.1f} Mbps) in {elapsed / 60:.1f} min "
             f"({got / elapsed:.2f}x realtime)")


if __name__ == "__main__":
    main()
