#!/usr/bin/env python
"""Find edit points (cuts) in an unedited lecture recording and build a review page.

Two sources of cuts:
  1. Silence runs in the audio, >= --min-silence seconds (default 3.0). Each cut
     leaves --pad seconds of pause on both sides, so speech is never clipped.
  2. Content cuts picked from the transcript (<output-dir>/content_cuts.json,
     written by the LLM stage: dead air, "any questions?" + silence, logistics).
     Each edge is snapped outward to the nearest speech edge, minus the pad. An
     edge that lands on speech raises - fix the JSON, don't paper over it.

Writes, artifact of record first:
  <output-dir>/edit_points.json          every cut, its audio stats, the parameters
  <output-dir>/studio_cuts.txt           the pre-ticked cuts in whole frames, numbered as
                                         in Studio, listed last first for entry
  <output-dir>/edit_review/index.html    review page: spectrogram, "after the cut" and
                                         "what gets removed" clips per cut, tick/untick,
                                         copy the final list
  <output-dir>/edit_review/studio.html   the same clips per merged cut, numbered and timed
                                         exactly like Studio's Cut 1..N list
The frame rate comes from yt-dlp once and is kept in edit_points.json.
Clips and spectrograms (edit_review/media/) are regenerable and gitignored.

The audio is <output-dir>/audio/<id>_16k.wav. If it is missing it is converted
(ffmpeg, mono 16 kHz) from --audio <file>, the local recording the user uploaded
(the Zoom download in ~/Downloads, GMT<date>-<time>_Recording_<res>.mp4); its length
must match the YouTube video's within 2 s. Without --audio the audio is downloaded
from YouTube (yt-dlp, audio only, ~80 MB for 1h45m).

Usage:
  python scripts/find_edit_points.py --output-dir output/<date>_<slug>_<id> --audio <recording.mp4>
  python scripts/find_edit_points.py --output-dir ... --report-only   # page from JSON
  python scripts/find_edit_points.py --output-dir ... --speech-map 0:16:00 0:16:50
      # where the pauses are, to place content-cut edges (~10-25 s, reads the audio)
  python scripts/find_edit_points.py --output-dir ... --check-studio .playwright-mcp/<markers>.json
      # after entering cuts: Studio vs plan vs studio.html, exits 1 on any mismatch (<1 s)
  python scripts/find_edit_points.py --output-dir ... --report-only --video-preview
      # studio.html plays a 360p copy of the recording (<output-dir>/video/, made once and
      # reused). HEAVY: 2-3x realtime under load (2026-10-12), up to ~1 h for a 2 h recording

Runtime (ML48: 1h46m, 120 cuts, this laptop): 1.5-3.5 min wall, and it varied a
lot from run to run - the render loop took 80-137 s although an idle-machine probe
rendered a short cut in ~0.15 s and the 7-min chat cut in ~5 s. --report-only
re-renders the media too, so it costs about the same. Add ~1 min for the
download and conversion on the first run.
"""
import argparse
import hashlib
import html
import json
import logging
import math
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
from matplotlib import colormaps
from PIL import Image
from scipy.signal import butter, sosfilt, spectrogram
from tqdm import tqdm

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LOG_DIR = Path("logs")
SR = 16000
HOP = SR // 100            # 10 ms frames
BLIP_FRAMES = 20           # sounds shorter than 0.2 s inside silence are clicks, not speech
FAINT_FLAG_DB = -50.0      # a filled blip louder than this gets flagged "listen"
CONTEXT_S = 4.0            # seconds of audio either side in the "after the cut" clip
REMOVED_CAP_S = 30.0       # longer removed parts are previewed as first 15 s + last 15 s
STUDIO_MARGIN_S = 20.0     # studio.html spectrogram: room either side to move edges or add a cut (the user asked for more than 10)
PLAY_CONTEXT_S = 3.0       # studio.html Play starts this long before the cut (and runs to the window's end)
STUDIO_PX_PER_S = 80       # studio.html spectrogram detail, so zooming in shows more than bigger pixels (12.5 ms/px)
STUDIO_SPEC_MAX_W = 16000  # ...capped for the long cuts (a 10-min window gets ~40 ms/px, about one frame)
SPEC_W, SPEC_H = 960, 130  # spectrogram image size, px
MAGMA = colormaps["magma"]

log = logging.getLogger("find_edit_points")


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "find_edit_points.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_t(text: str) -> float:
    parts = [float(p) for p in text.strip().split(":")]
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def fmt_t(sec: float, digits: int = 1) -> str:
    sign = "-" if sec < 0 else ""
    sec = round(abs(sec), digits)          # round first, so 59.96 s can't print as ":60.0"
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    width = 3 + digits if digits else 2
    return f"{sign}{int(h)}:{int(m):02d}:{s:0{width}.{digits}f}"


# ---------------------------------------------------------------- audio

def media_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def ensure_wav(out_dir: Path, meta: dict, source: Path | None = None) -> Path:
    """The 16 kHz mono WAV everything reads. Made from `source` (the local recording the
    user uploaded, e.g. the Zoom download) when given, else from the YouTube audio."""
    audio_dir = out_dir / "audio"
    wav = audio_dir / f"{meta['id']}_16k.wav"
    if wav.exists():
        made_from = audio_source(wav)
        if source is not None and made_from != str(source.resolve()):
            raise ValueError(f"{wav.name} was made from {made_from}, not from --audio {source}. "
                             f"Delete the WAV to rebuild it from that file.")
        return wav
    audio_dir.mkdir(exist_ok=True)
    if source is not None:
        if not source.is_file():
            raise FileNotFoundError(f"--audio file not found: {source}")
        dur = media_duration(source)
        if abs(dur - meta["duration"]) > 2.0:
            raise ValueError(f"{source.name} is {dur:.1f} s long but the YouTube video is {meta['duration']} s - "
                             f"not the recording that was uploaded?")
        log.info(f"Using the local recording {source} ({dur:.1f} s, YouTube says {meta['duration']} s)")
        src = [source]
    else:
        src = sorted(p for p in audio_dir.glob(f"{meta['id']}.*") if p.suffix in (".webm", ".m4a", ".opus", ".mp3"))
    if not src:
        log.info(f"Downloading audio for {meta['id']} (yt-dlp, audio only)")
        subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", str(audio_dir / "%(id)s.%(ext)s"), meta["url"]], check=True)
        src = sorted(p for p in audio_dir.glob(f"{meta['id']}.*") if p.suffix in (".webm", ".m4a", ".opus", ".mp3"))
        if not src:
            raise FileNotFoundError(f"yt-dlp finished but no audio file appeared in {audio_dir}")
    log.info(f"Converting {src[0].name} -> {wav.name} (mono 16 kHz)")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(src[0]),
                    "-vn", "-ac", "1", "-ar", str(SR), str(wav)], check=True)
    wav.with_suffix(".source.txt").write_text(str(src[0].resolve()), encoding="utf-8")
    return wav


def audio_source(wav: Path) -> str:
    """Which recording the WAV was converted from (written next to it at conversion)."""
    side = wav.with_suffix(".source.txt")
    return side.read_text(encoding="utf-8").strip() if side.exists() else "unknown (WAV made before 2026-10-04)"


# ---------------------------------------------------------------- video preview (studio.html)

VIDEO_PROXY_H = 360        # proxy height; the width follows the recording's aspect ratio
VIDEO_PROXY_FPS = 15       # screen shares change slowly; fewer frames to encode
VIDEO_PROXY_GOP = 30       # a keyframe every 2 s. Seeks took 11-138 ms on a test proxy against 0.35-11 s
                           # (median ~2 s) on the Zoom original, whose keyframes are ~26 s apart (2026-10-12)


def video_proxy_path(out_dir: Path, video_id: str) -> Path:
    return out_dir / "video" / f"{video_id}_{VIDEO_PROXY_H}p.mp4"


def existing_video_proxy(out_dir: Path, data: dict) -> Path | None:
    """The proxy from an earlier --video-preview run, if there is one. Raises if it was made
    from a different recording than the WAV (its timeline would not match the cuts)."""
    dest = video_proxy_path(out_dir, data["video_id"])
    if not dest.exists():
        return None
    made_from = dest.with_suffix(".source.txt").read_text(encoding="utf-8").strip()
    if made_from != data["audio_source"]:
        raise ValueError(f"{dest.name} was made from {made_from}, but the audio comes from "
                         f"{data['audio_source']}. Delete {dest} and rerun with --video-preview.")
    return dest


def make_video_proxy(out_dir: Path, data: dict, encoder: str) -> Path:
    """A small H.264 copy of the recording that studio.html plays instead of the WAV:
    VIDEO_PROXY_H p, VIDEO_PROXY_FPS fps, a keyframe every 2 s, mono AAC. Encoded once and
    reused while it matches the WAV's source recording."""
    existing = existing_video_proxy(out_dir, data)
    if existing:
        log.info(f"Video preview: reusing {existing}")
        return existing
    src = Path(data["audio_source"])
    if not src.is_file():
        raise FileNotFoundError(f"--video-preview needs the local recording, and the audio came from "
                                f"{data['audio_source']!r}: rerun the analysis with --audio <recording>")
    size = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                           "-of", "csv=p=0", str(src)], check=True, capture_output=True, text=True).stdout.strip()
    if not size:
        raise ValueError(f"{src} has no video stream")
    w0, h0 = map(int, size.split(","))
    width = round(w0 * VIDEO_PROXY_H / h0 / 2) * 2
    dest = video_proxy_path(out_dir, data["video_id"])
    dest.parent.mkdir(exist_ok=True)
    part = dest.with_suffix(".part.mp4")           # only renamed to dest once it is complete and checked
    if encoder == "qsv":                           # Intel Quick Sync: decode, scale and encode on the iGPU
        video = ["-hwaccel", "qsv", "-hwaccel_output_format", "qsv", "-c:v", "h264_qsv", "-i", str(src),
                 "-vf", f"vpp_qsv=w={width}:h={VIDEO_PROXY_H}:framerate={VIDEO_PROXY_FPS}",
                 "-c:v", "h264_qsv", "-preset", "veryfast", "-global_quality", "30"]
    else:
        video = ["-i", str(src), "-vf", f"fps={VIDEO_PROXY_FPS},scale={width}:{VIDEO_PROXY_H}",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p"]
    cmd = (["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "error", "-y", "-progress", "pipe:1"] + video
           + ["-g", str(VIDEO_PROXY_GOP), "-map", "0:v:0", "-map", "0:a:0", "-map_chapters", "-1", "-dn",
              "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-movflags", "+faststart", str(part)])
    log.info(f"Video preview: encoding {src.name} -> {dest.name} ({width}x{VIDEO_PROXY_H}, {encoder}). "
             f"Measured 2-3x realtime under load (2026-10-12), so up to ~1 h for a 2 h recording")
    t0 = last = time.time()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in proc.stdout:                       # ffmpeg -progress: key=value lines
        if line.startswith("out_time_us=") and line.strip() != "out_time_us=N/A" and time.time() - last >= 30:
            last = time.time()
            done = int(line.split("=", 1)[1]) / 1e6
            eta = (last - t0) / max(done, 1.0) * (data["duration"] - done)
            log.info(f"Video preview: {done / 60:.0f}/{data['duration'] / 60:.0f} min, "
                     f"{last - t0:.0f}s elapsed, ~{eta:.0f}s left")
    err = proc.stderr.read()
    if proc.wait() != 0:
        hint = "\nWithout Quick Sync, rerun with --video-encoder x264 (CPU)." if encoder == "qsv" else ""
        raise RuntimeError(f"ffmpeg failed ({encoder}): {err.strip()[-800:]}{hint}")
    dur = media_duration(part)
    if abs(dur - data["duration"]) > 1.0:
        raise ValueError(f"{part.name} is {dur:.1f} s long but the audio is {data['duration']:.1f} s: "
                         f"the page would play out of sync")
    part.replace(dest)
    dest.with_suffix(".source.txt").write_text(str(src), encoding="utf-8")
    log.info(f"Video preview: wrote {dest} ({dest.stat().st_size / 2**20:.0f} MB) in {time.time() - t0:.0f} s")
    return dest


def frame_levels(x: np.ndarray) -> np.ndarray:
    """Speech-band (100-4000 Hz) power per 10 ms frame, in dB. Filtered in 60 s chunks
    (the filter state carries over, so the result is the same): filtering 110 min at once
    needed a 0.85 GB float64 copy, and ML50's run died allocating it (2026-10-14)."""
    sos = butter(4, [100, 4000], btype="band", fs=SR, output="sos")
    zi = np.zeros((sos.shape[0], 2))
    step = SR * 60                                    # a multiple of HOP, so frames never straddle chunks
    out = []
    for i in range(0, len(x), step):
        y, zi = sosfilt(sos, x[i:i + step], zi=zi)
        y = y.astype(np.float32)
        n = len(y) // HOP
        out.append(10 * np.log10((y[: n * HOP].reshape(n, HOP) ** 2).mean(axis=1) + 1e-12))
    return np.concatenate(out)


def runs(mask: np.ndarray):
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    return np.flatnonzero(d == 1), np.flatnonzero(d == -1)


def sound_mask(db: np.ndarray, thr: float) -> np.ndarray:
    """True where something is audible; blips shorter than 0.2 s count as silence."""
    sound = db > thr
    a, b = runs(sound)
    for s, e in zip(a, b):
        if e - s < BLIP_FRAMES:
            sound[s:e] = False
    return sound


def blip_flags(db: np.ndarray, thr: float, i0: int, i1: int) -> list[str]:
    """Short sounds (filled as silence) inside frames i0..i1 that are loud enough to check."""
    a, b = runs(db[i0:i1] > thr)
    out = []
    for s, e in zip(a, b):
        peak = db[i0 + s: i0 + e].max()
        if peak > FAINT_FLAG_DB:
            out.append(f"short sound at {fmt_t((i0 + s) / 100)} ({peak:.0f} dB) - listen")
    return out


# ---------------------------------------------------------------- cuts

def silence_cuts(db, sound, thr, min_len, pad):
    a, b = runs(~sound)
    cuts = []
    for s, e in zip(a, b):
        run_len = (e - s) / 100
        if run_len < min_len:
            continue
        start, end = s / 100 + pad, e / 100 - pad
        if s == 0:                       # silence at the very start: nothing to keep before it
            start = 0.0
        if e == len(sound):
            end = len(sound) / 100
        cuts.append({
            "source": "silence", "kind": "safe", "default": True,
            "start": round(start, 2), "end": round(end, 2),
            "run_len": round(run_len, 2),
            "reason": f"{run_len:.1f} s of silence",
            "flags": blip_flags(db, thr, s, e),
        })
    return cuts


def snap_content(cut: dict, sound: np.ndarray, duration: float, pad_default: float) -> dict:
    """Put each edge at the speech edge next to it, leaving the pad of pause. Usually
    that widens the cut; an edge asked for within the pad of speech moves inward."""
    pad = float(cut.get("pad", pad_default))
    n = len(sound)
    s_req = parse_t(cut["start"])
    e_req = duration if cut["end"] == "end" else parse_t(cut["end"])
    if e_req <= s_req:
        raise ValueError(f"Content cut ends before it starts: {cut}")
    i, j = int(round(s_req * 100)), min(int(round(e_req * 100)), n)
    bad = []
    if i < n and sound[i]:
        bad.append(f"start {cut['start']} is on speech")
    if cut["end"] != "end" and j < n and sound[j]:
        bad.append(f"end {cut['end']} is on speech")
    if bad:
        raise ValueError(f"Content cut edge on speech ({'; '.join(bad)}): {cut['reason']!r}. "
                         f"Move the edge into a pause and rerun.")
    before = np.flatnonzero(sound[:i])
    if len(before):
        last_end = (before[-1] + 1) / 100
        nxt = np.flatnonzero(sound[i:])
        gap = ((i + nxt[0]) / 100 if len(nxt) else duration) - last_end
        start = last_end + min(pad, gap / 2)
    else:
        start = 0.0
    if cut["end"] == "end":
        end = duration
    else:
        after = np.flatnonzero(sound[j:])
        if len(after):
            next_start = (j + after[0]) / 100
            prev = np.flatnonzero(sound[:j])
            gap = next_start - ((prev[-1] + 1) / 100 if len(prev) else 0.0)
            end = next_start - min(pad, gap / 2)
        else:
            end = duration
    return {
        "source": "content", "kind": cut["kind"], "default": bool(cut["default"]),
        "start": round(start, 2), "end": round(end, 2),
        "requested": [cut["start"], cut["end"]],
        "reason": cut["reason"], "flags": [],
    }


def union(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1] + 0.05:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def video_fps(data: dict, url: str) -> int:
    """Frame rate of the uploaded video. Studio's time boxes are H:MM:SS:FF, so cut
    times have to be whole frames. Asked from yt-dlp once, then kept in the JSON."""
    if "fps" not in data:
        out = subprocess.run(["yt-dlp", "--skip-download", "--print", "%(fps)s", url],
                             check=True, capture_output=True, text=True).stdout.strip()
        try:
            data["fps"] = float(out.splitlines()[-1])
        except (ValueError, IndexError):
            raise ValueError(f"yt-dlp gave no frame rate for {url}: {out!r}")
        log.info(f"Video frame rate: {data['fps']:g} fps")
    if data["fps"] != int(data["fps"]):
        raise NotImplementedError(f"{data['fps']} fps: Studio frame numbering for fractional rates is unverified")
    return int(data["fps"])


def studio_cuts(data: dict, fps: int) -> list[dict]:
    """The pre-ticked cuts as Studio lists them: merged, rounded inward to whole frames,
    numbered Cut 1..N by start time (Studio sorts its list that way)."""
    def tc(frame):
        s, ff = divmod(frame, fps)
        h, rem = divmod(s, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}:{ff:02d}"
    ticked = [c for c in data["cuts"] if c["default"]]
    out = []
    for n, (s, e) in enumerate(union([[c["start"], c["end"]] for c in ticked]), 1):
        fs, fe = math.ceil(s * fps - 1e-6), math.floor(e * fps + 1e-6)
        if e >= data["duration"] - 0.05:    # the end trim: Studio's last frame, not one short (ML49: :04 vs :03)
            fe = round(data["duration"] * fps)
        out.append({
            "id": f"studio{n:02d}", "n": n, "start": fs / fps, "end": fe / fps,
            "start_tc": tc(fs), "end_tc": tc(fe),
            "sources": [c["id"] for c in ticked if c["start"] < e and c["end"] > s],
        })
    return out


def studio_lines(scuts):
    """Cut list for YouTube Studio: Studio's numbering, listed last first for entry."""
    return [f"Cut {c['n']:>2}   {c['start_tc']}  ->  {c['end_tc']}   ({c['end'] - c['start']:.2f} s)"
            for c in reversed(scuts)]


# ---------------------------------------------------------------- media

def write_clips(x, cut, media: Path):
    s, e = int(cut["start"] * SR), int(cut["end"] * SR)
    c = int(CONTEXT_S * SR)
    fade = int(0.02 * SR)
    a, b = x[max(0, s - c): s].copy(), x[e: e + c].copy()
    if len(a) > fade and len(b) > fade:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        a[-fade:] *= ramp[::-1]
        b[:fade] *= ramp
    after = np.concatenate([a, b]) if len(a) + len(b) else np.zeros(SR // 2, np.float32)
    sf.write(media / f"{cut['id']}_after.wav", after, SR, subtype="PCM_16")
    removed = x[s:e]
    if len(removed) > REMOVED_CAP_S * SR:
        half = int(REMOVED_CAP_S / 2 * SR)
        removed = np.concatenate([removed[:half], np.zeros(int(0.4 * SR), np.float32), removed[-half:]])
    peak = float(np.abs(removed).max()) if len(removed) else 0.0
    gain = min(0.5 / peak, 30.0) if peak > 1e-5 else 1.0   # make faint sounds audible, max +30 dB
    sf.write(media / f"{cut['id']}_removed.wav", np.clip(removed * gain, -1, 1), SR, subtype="PCM_16")
    cut["removed_gain_db"] = round(20 * math.log10(gain), 1)


def draw_spectrogram(x, cut, duration, media: Path, margin: float = 3.0, shade: bool = True,
                     px_per_s: float | None = None):
    """0-5 kHz spectrogram of the cut plus `margin` s either side, cut shaded red unless
    shade=False (studio.html draws the shading itself, so the edges can move). SPEC_W wide,
    or `px_per_s` pixels per second up to STUDIO_SPEC_MAX_W (studio.html zooms into it).
    Drawn with numpy + PIL: matplotlib took ~2 s per image here, this takes ~0.05 s."""
    w0 = max(0.0, cut["start"] - margin)
    w1 = min(duration, cut["end"] + margin)
    width = SPEC_W if px_per_s is None else min(STUDIO_SPEC_MAX_W, max(SPEC_W, round((w1 - w0) * px_per_s)))
    seg = x[int(w0 * SR): int(w1 * SR)]
    nper = 512 if (w1 - w0) / width < 0.125 else 2048    # SPEC_W: windows under 120 s
    # about 2 columns per pixel is enough; a fixed 75% overlap gave a 10-min cut 10k columns
    # (a 157 MB array, which failed to allocate on 2026-10-11 with 0.2 GB of RAM free)
    hop = max(nper // 4, len(seg) // (2 * width))
    f, t, sxx = spectrogram(seg, fs=SR, nperseg=nper, noverlap=max(0, nper - hop))
    sdb = 10 * np.log10(sxx[f <= 5000] + 1e-12)
    vmax = np.percentile(sdb, 99.5)
    norm = np.clip((sdb - (vmax - 70)) / 70, 0, 1)[::-1]          # low frequencies at the bottom
    # resize first, then colour: colouring the full grid costs 32 bytes a cell (~160 MB at 16000 px)
    small = np.asarray(Image.fromarray(np.ascontiguousarray(norm, dtype=np.float32)).resize((width, SPEC_H), Image.BILINEAR))
    img = (MAGMA(small)[..., :3] * 255).astype(np.uint8)
    if shade:
        span = w1 - w0
        a = int(round((cut["start"] - w0) / span * width))
        b = int(round((cut["end"] - w0) / span * width))
        red = np.array([217, 0, 18], np.float32)
        img[:, a:b] = (img[:, a:b] * 0.6 + red * 0.4).astype(np.uint8)
        for col in (a, b - 1):
            img[:, max(0, min(width - 2, col)): max(0, min(width - 2, col)) + 2] = red.astype(np.uint8)
    Image.fromarray(img).save(media / f"{cut['id']}_spec.png", optimize=False)
    cut["spec_window"] = [round(w0, 2), round(w1, 2)]
    cut["spec_px"] = width


# ---------------------------------------------------------------- transcript

def load_transcript(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+:\d\d(?::\d\d)?)\s+(.*)$", line)
        if m:
            rows.append((parse_t(m.group(1)), m.group(1), m.group(2)))
    return rows


def snippet(rows, s, e):
    inside = [r for r in rows if s - 6 <= r[0] <= e + 4]
    if len(inside) > 10:
        inside = inside[:5] + [None] + inside[-4:]
    return inside


# ---------------------------------------------------------------- page

PAGE_CSS = """
:root { --bg:#fbfaf7; --fg:#1d1d1f; --muted:#6b6b70; --card:#ffffff; --line:#e3e1dc;
        --red:#D90012; --blue:#0033A0; --orange:#F2A800; --absorbed:#f0efe9; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#17171a; --fg:#ececef; --muted:#9a9aa2; --card:#202024; --line:#34343a; --absorbed:#26262b; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.45 system-ui, "Segoe UI", sans-serif; }
main { max-width: 1000px; margin: 0 auto; padding: 16px; }
h1 { font-size: 22px; margin: 8px 0 4px; }
.sub { color: var(--muted); margin: 0 0 12px; }
nav ol { margin: 6px 0 16px; padding-left: 22px; }
nav a { color: var(--blue); }
details { background: var(--card); border:1px solid var(--line); border-radius:10px; margin: 12px 0; padding: 4px 14px 12px; }
summary { cursor: pointer; font-weight: 650; font-size: 17px; padding: 8px 0; }
.stats { position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 2px solid var(--red);
         padding: 8px 0; display:flex; flex-wrap:wrap; gap: 6px 18px; align-items:center; }
.stats b { font-variant-numeric: tabular-nums; }
.card { border-top: 1px solid var(--line); padding: 12px 0; }
.card.off { opacity: .45; }
.card.absorbed { background: var(--absorbed); opacity:.55; }
.head { display:flex; flex-wrap:wrap; gap: 4px 12px; align-items: baseline; }
.head label { font-weight: 650; font-variant-numeric: tabular-nums; cursor:pointer; }
.badge { font-size: 12px; padding: 1px 7px; border-radius: 9px; color:#fff; }
.safe { background: var(--blue); } .judgment { background: var(--orange); color:#1d1d1f; }
.reason { flex-basis: 100%; }
.flag { color: var(--red); font-size: 13px; }
.note { color: var(--muted); font-size: 13px; }
img.spec { width: 100%; height: auto; border-radius: 6px; margin: 6px 0 2px; display:block; }
.players { display:flex; flex-wrap:wrap; gap: 4px 18px; font-size: 13px; color: var(--muted); }
.players audio { height: 32px; width: 290px; max-width: 100%; vertical-align: middle; }
.tx { font-size: 13px; color: var(--muted); margin-top: 6px; }
.tx .t { font-variant-numeric: tabular-nums; margin-right: 8px; }
.tx .in { color: var(--fg); }
textarea { width: 100%; min-height: 260px; font: 13px/1.4 Consolas, monospace; background: var(--card);
           color: var(--fg); border: 1px solid var(--line); border-radius: 6px; padding: 8px; }
button, select { font: inherit; padding: 4px 10px; border-radius: 6px; border: 1px solid var(--line);
                 background: var(--card); color: var(--fg); cursor: pointer; }
ul.how li { margin: 4px 0; }
"""

PAGE_JS = """
const DATA = JSON.parse(document.getElementById('data').textContent);
const KEY = 'edit-points-' + DATA.video_id + '-' + DATA.signature;   // a changed cut list starts from the defaults
const byId = Object.fromEntries(DATA.cuts.map(c => [c.id, c]));
let ticked = new Set(DATA.cuts.filter(c => c.default).map(c => c.id));
try { const saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) ticked = new Set(saved); } catch (e) {}
const minSel = document.getElementById('minsil');
function fmt(sec, d=1) { sec = Math.round(sec * 10**d) / 10**d; const h=Math.floor(sec/3600), m=Math.floor(sec%3600/60), s=sec%60;
  return h + ':' + String(m).padStart(2,'0') + ':' + s.toFixed(d).padStart(d ? 3+d : 2, '0'); }
function active(c) { return ticked.has(c.id) && (c.source !== 'silence' || c.run_len >= +minSel.value); }
function union(iv) { const out=[]; iv.sort((a,b)=>a[0]-b[0]);
  for (const [s,e] of iv) { if (out.length && s <= out[out.length-1][1]+0.05) out[out.length-1][1]=Math.max(out[out.length-1][1],e); else out.push([s,e]); }
  return out; }
function tc(f) { const F = DATA.fps, s = Math.floor(f / F);
  return Math.floor(s/3600) + ':' + String(Math.floor(s%3600/60)).padStart(2,'0') + ':' +
         String(s%60).padStart(2,'0') + ':' + String(f%F).padStart(2,'0'); }
function studio(iv) {   // Studio's Cut 1..N (by start), whole frames rounded inward, listed last first
  const F = DATA.fps;
  const rows = iv.map(([s,e], i) => [i+1, Math.ceil(s*F - 1e-6), Math.floor(e*F + 1e-6)]);
  return rows.reverse().map(([n,fs,fe]) => 'Cut ' + String(n).padStart(2) + '   ' + tc(fs) + '  ->  ' + tc(fe) +
                                         '   (' + ((fe-fs)/F).toFixed(2) + ' s)'); }
function refresh() {
  const on = DATA.cuts.filter(active);
  const content = on.filter(c => c.source === 'content');
  for (const c of DATA.cuts) {
    const el = document.getElementById('card-' + c.id); if (!el) continue;
    const hidden = c.source === 'silence' && c.run_len < +minSel.value;
    el.style.display = hidden ? 'none' : '';
    el.classList.toggle('off', !ticked.has(c.id));
    const host = c.source === 'silence' && content.find(k => k.start <= c.start && k.end >= c.end);
    el.classList.toggle('absorbed', !!host);
    const n = el.querySelector('.absorbed-note'); if (n) n.textContent = host ? 'inside ' + host.id + ', which is ticked' : '';
    el.querySelector('input').checked = ticked.has(c.id);
  }
  const iv = union(on.map(c => [c.start, c.end]));
  const removed = iv.reduce((a,[s,e]) => a + e - s, 0);
  document.getElementById('n-cuts').textContent = iv.length;
  document.getElementById('t-removed').textContent = fmt(removed, 0);
  document.getElementById('t-new').textContent = fmt(DATA.duration - removed, 0);
  document.getElementById('export').value = studio(iv).join('\\n');
  try { localStorage.setItem(KEY, JSON.stringify([...ticked])); } catch (e) {}
}
document.querySelectorAll('.card input').forEach(cb => cb.addEventListener('change', e => {
  const id = e.target.dataset.id; if (e.target.checked) ticked.add(id); else ticked.delete(id); refresh(); }));
minSel.addEventListener('change', refresh);
document.getElementById('reset').addEventListener('click', () => {
  ticked = new Set(DATA.cuts.filter(c => c.default).map(c => c.id)); refresh(); });
document.getElementById('copy').addEventListener('click', async () => {
  const ta = document.getElementById('export');
  try { await navigator.clipboard.writeText(ta.value); } catch (e) { ta.select(); document.execCommand('copy'); }
  document.getElementById('copy').textContent = 'Copied'; setTimeout(() => document.getElementById('copy').textContent = 'Copy list', 1500); });
refresh();
"""


def card_html(c, rows):
    esc = html.escape
    badge = f'<span class="badge {c["kind"]}">{"safe" if c["kind"] == "safe" else "your call"}</span>'
    flags = "".join(f'<div class="flag">{esc(f)}</div>' for f in c["flags"])
    tx = []
    for r in snippet(rows, c["start"], c["end"]):
        if r is None:
            tx.append('<div>...</div>')
            continue
        cls = "in" if c["start"] - 1 <= r[0] <= c["end"] else ""
        tx.append(f'<div class="{cls}"><span class="t">{esc(r[1])}</span>{esc(r[2])}</div>')
    gain = c.get("removed_gain_db", 0)
    gain_note = f" (boosted +{gain:.0f} dB)" if gain >= 1 else ""
    capped = " - first 15 s + last 15 s" if c["end"] - c["start"] > REMOVED_CAP_S else ""
    return f"""
<div class="card" id="card-{c['id']}">
  <div class="head">
    <label><input type="checkbox" data-id="{c['id']}"> {c['id']} &nbsp; {fmt_t(c['start'])} &rarr; {fmt_t(c['end'])}</label>
    <span>{c['end'] - c['start']:.1f} s</span> {badge} <span class="note absorbed-note"></span>
    <div class="reason">{esc(c['reason'])}</div>
  </div>
  {flags}
  <img class="spec" loading="lazy" src="media/{c['id']}_spec.png" alt="spectrogram {c['id']}">
  <div class="note">spectrogram 0-5 kHz, {fmt_t(c['spec_window'][0], 0)} to {fmt_t(c['spec_window'][1], 0)}, cut part in red</div>
  <div class="players">
    <span>after the cut <audio controls preload="none" src="media/{c['id']}_after.wav"></audio></span>
    <span>what gets removed{gain_note}{capped} <audio controls preload="none" src="media/{c['id']}_removed.wav"></audio></span>
  </div>
  <div class="tx">{''.join(tx)}</div>
</div>"""


def build_page(data, rows, page: Path):
    content = [c for c in data["cuts"] if c["source"] == "content"]
    sil_long = [c for c in data["cuts"] if c["source"] == "silence" and c["run_len"] >= 5]
    sil_short = [c for c in data["cuts"] if c["source"] == "silence" and c["run_len"] < 5]
    p = data["params"]
    opts = "".join(f'<option value="{v:g}"{" selected" if v == p["min_silence"] else ""}>{v:g} s</option>'
                   for v in sorted({p["min_silence"], 2.0, 3.0, 4.0, 5.0, 8.0}) if v >= p["min_silence"])
    sections = [
        ("how", "How to apply this in YouTube Studio", f"""
<ul class="how">
  <li>Listen to <b>after the cut</b> first: it is {CONTEXT_S:g} s before the cut joined to {CONTEXT_S:g} s after, so you hear exactly how the edit will sound. <b>What gets removed</b> is the cut part itself, boosted so faint sounds are audible.</li>
  <li>Untick anything you want to keep. Ticks are remembered in this browser. The minimum-silence menu at the top hides the shorter silence cuts.</li>
  <li>In Studio: Editor &rarr; Trim &amp; cut &rarr; New Cut for each line of the list in the last section. It uses Studio's own numbering (Cut 1..N by start time) and its <code>H:MM:SS:FF</code> frame times, the same as <code>studio.html</code>, listed last first. Studio keeps the original timeline while you edit, so the times stay valid.</li>
  <li>Times are rounded inward to whole frames, so a cut never eats into speech.</li>
  <li>Studio edits can't be undone after saving. Keep your original recording.</li>
  <li>Chapters come after the edit: every cut shifts the times after it.</li>
</ul>
<p class="note">Silence = speech-band level below {p['threshold_db']:.0f} dB (noise floor {p['floor_db']:.0f} dB + 20) for at least {p['min_silence']:g} s; clicks under 0.2 s count as silence. Each silence cut leaves {p['pad']:g} s of pause on both sides. Content cuts come from the transcript, with edges snapped to the speech edge.</p>"""),
        ("content", f"Content cuts ({len(content)})", "".join(card_html(c, rows) for c in content)),
        ("sil-long", f"Silence cuts, 5 s and longer ({len(sil_long)})", "".join(card_html(c, rows) for c in sil_long)),
        ("sil-short", f"Silence cuts, under 5 s ({len(sil_short)})", "".join(card_html(c, rows) for c in sil_short)),
        ("export", "Final cut list for Studio (last first)", """
<p><button id="copy">Copy list</button> <button id="reset">Reset to my picks</button></p>
<textarea id="export" readonly></textarea>"""),
    ]
    toc = "".join(f'<li><a href="#{sid}">{html.escape(title)}</a></li>' for sid, title, _ in sections)
    body = "".join(f'<details open id="{sid}"><summary>{html.escape(title)}</summary>{inner}</details>'
                   for sid, title, inner in sections)
    sig = hashlib.sha1(json.dumps([[c["id"], c["start"], c["end"]] for c in data["cuts"]]).encode()).hexdigest()[:12]
    blob = json.dumps({**data, "signature": sig}, ensure_ascii=False).replace("</", "<\\/")
    page.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edit points {html.escape(data['video_id'])}</title>
<style>{PAGE_CSS}</style></head>
<body><main>
<h1>Edit points: {html.escape(data['title'])}</h1>
<p class="sub">{fmt_t(data['duration'], 0)} raw recording, https://youtu.be/{html.escape(data['video_id'])}</p>
<div class="stats">
  <span>Studio cuts <b id="n-cuts"></b></span>
  <span>removed <b id="t-removed"></b></span>
  <span>new length <b id="t-new"></b></span>
  <span>min silence <select id="minsil">{opts}</select></span>
</div>
<nav><ol>{toc}</ol></nav>
{body}
</main>
<script id="data" type="application/json">{blob}</script>
<script>{PAGE_JS}</script>
</body></html>
""", encoding="utf-8")


# ---------------------------------------------------------------- main

STUDIO_CSS = """
.specscroll { overflow-x: auto; overflow-y: hidden; padding: 3px 0; margin-top: 3px; }
.specwrap { position: relative; width: 100%; cursor: ew-resize; touch-action: none; user-select: none; }
.specwrap img { display: block; width: 100%; height: 130px; border-radius: 6px; pointer-events: none; }
.zoom button { min-width: 28px; }
.zoom .zl { display: inline-block; min-width: 34px; text-align: center; font-variant-numeric: tabular-nums; }
.bar { position: absolute; top: -3px; bottom: -3px; width: 3px; margin-left: -1px; background: #fff;
       box-shadow: 0 0 0 1px #000; border-radius: 2px; pointer-events: none; z-index: 2; }
.shade { position: absolute; top: 0; bottom: 0; background: rgba(217, 0, 18, .38); pointer-events: none;
         border-left: 3px solid var(--red); border-right: 3px solid var(--red); box-sizing: border-box; }
.shade.added { background: rgba(242, 168, 0, .40); border-color: var(--orange); }
.shade.other { background: rgba(150, 150, 150, .40); border: none; }
.edit, .added-row { display: flex; flex-wrap: wrap; gap: 6px 12px; align-items: center; margin: 4px 0; font-size: 14px; }
.edit .times, .added-row .times { font-variant-numeric: tabular-nums; }
.edit button, .added-row button { font-size: 13px; }
.added-row .tag { color: var(--orange); font-weight: 650; }
.was, .warn, .msg { font-size: 13px; color: var(--muted); }
.warn, .msg { color: var(--red); }
details.cut.changed > summary { color: var(--red); }
#export { width: 100%; min-height: 220px; font: 13px/1.4 ui-monospace, Consolas, monospace; }
#player { position: sticky; top: 0; z-index: 6; background: var(--bg); padding: 8px 0 10px; display: flex;
          gap: 12px; align-items: flex-end; border-bottom: 1px solid var(--line); }
#player video { width: 480px; max-width: 62vw; aspect-ratio: 16 / 9; background: #000; border-radius: 6px; display: block; }
#player.hidden video { display: none; }
#player .pinfo { display: flex; flex-direction: column; gap: 6px; font-size: 14px; color: var(--muted); }
body.has-video details.cut { scroll-margin-top: 300px; }
.axis { display: flex; justify-content: space-between; gap: 12px; font-size: 12px; color: var(--muted);
        font-variant-numeric: tabular-nums; }
.axis .a0, .axis .a1 { white-space: nowrap; }
.ctl { display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: center; margin: 8px 0 4px; }
.ctl .now { font-variant-numeric: tabular-nums; font-weight: 650; min-width: 90px; }
.play { min-width: 74px; }
.flag button { font-size: 12px; padding: 0 6px; margin-left: 6px; }
.err { color: var(--red); }
nav ol { columns: 2; font-variant-numeric: tabular-nums; }
summary { font-variant-numeric: tabular-nums; }
.stamp { font-size: 14px; background: var(--card); border: 1px solid var(--line); border-left: 4px solid var(--red);
         border-radius: 6px; padding: 6px 10px; display: inline-block; }
"""

STUDIO_JS = """
const A = document.getElementById('media');                  // the 360p video preview, or the WAV
const FPS = +document.body.dataset.fps, CTX = +document.body.dataset.ctx;
const NEW_LEN = 1.0;                                          // a cut added at the bar starts 1 s long
const KEY = 'studio-edits-' + document.body.dataset.list;   // a new cut list starts with no edits
const OVERLAP = ' - Studio would join them, adjust one of the two';
const cards = [...document.querySelectorAll('details.cut')];
let cur = null, raf = null, focusEl = null, uid = 0;
function tc(t) { const f = Math.floor(t * FPS + 1e-6), s = Math.floor(f / FPS);
  return Math.floor(s / 3600) + ':' + String(Math.floor(s % 3600 / 60)).padStart(2, '0') + ':' +
         String(s % 60).padStart(2, '0') + ':' + String(f % FPS).padStart(2, '0'); }
const num = (el, k) => parseFloat(el.dataset[k]);
const snap = t => Math.round(t * FPS) / FPS;   // Studio works in whole frames
// Every cut on the page: each card's planned cut, plus the cuts added on this page (host = the card).
const plan = cards.map(el => ({ host: el, s: num(el, 's0'), e: num(el, 'e0'), s0: num(el, 's0'), e0: num(el, 'e0'), added: false }));
cards.forEach((el, i) => { el.plan = plan[i]; });
let added = [];
const all = () => plan.concat(added);
const own = el => [el.plan, ...added.filter(c => c.host === el)];
const changed = c => !c.added && (Math.abs(c.s - c.s0) > 1e-6 || Math.abs(c.e - c.e0) > 1e-6);
function storageError(what, err) {
  document.getElementById('storage').textContent = `Edits can't be ${what} in this browser (${err.message}) - copy the list below before closing the tab.`;
}
function save() {
  const edits = {};
  plan.forEach(c => { if (changed(c)) edits[c.host.id] = [c.s, c.e]; });
  try { localStorage.setItem(KEY, JSON.stringify({ edits, added: added.map(c => ({ host: c.host.id, s: c.s, e: c.e })) })); }
  catch (err) { storageError('saved', err); }
}
function load() {
  let o;
  try { o = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (err) { storageError('loaded', err); return; }
  const edits = 'edits' in o ? o.edits : o;    // the first version stored only {cardId: [s, e]}
  plan.forEach(c => { if (edits[c.host.id]) [c.s, c.e] = edits[c.host.id]; });
  (o.added || []).forEach(a => { const h = document.getElementById(a.host);
    if (h) added.push({ id: ++uid, host: h, s: a.s, e: a.e, added: true }); });
}
function show(el, t) {
  const w0 = num(el, 'w0'), w1 = num(el, 'w1');
  t = Math.min(w1, Math.max(w0, t));
  el.querySelector('.bar').style.left = (100 * (t - w0) / (w1 - w0)) + '%';
  el.querySelector('.now').textContent = tc(t);
  el.dataset.pos = t;
  return t;
}
const ZOOMS = [1, 2, 4, 8, 16, 32, 64];
const parts = el => ({ sc: el.querySelector('.specscroll'), wrap: el.querySelector('.specwrap'), w0: num(el, 'w0'), w1: num(el, 'w1') });
function axis(el) {        // the times at the visible edges of the spectrogram
  const { sc, wrap, w0, w1 } = parts(el), W = wrap.offsetWidth;
  el.querySelector('.a0').textContent = tc(W ? w0 + sc.scrollLeft / W * (w1 - w0) : w0);
  el.querySelector('.a1').textContent = tc(W ? Math.min(w1, w0 + (sc.scrollLeft + sc.clientWidth) / W * (w1 - w0)) : w1);
}
function zoomTo(el, z, t, x) {   // zoom level z, keeping time t at x px from the visible left edge
  const { sc, wrap, w0, w1 } = parts(el);
  el.dataset.zoom = z;
  wrap.style.width = (100 * z) + '%';
  sc.scrollLeft = (t - w0) / (w1 - w0) * wrap.offsetWidth - x;
  el.querySelector('.zl').textContent = z + '\\u00d7';
  axis(el);
}
function zoomStep(el, dir, t, x) {   // one level in (+1) or out (-1), up to 4 screen px per image px
  const zs = ZOOMS.filter(z => z === 1 || z * parts(el).sc.clientWidth <= 4 * num(el, 'pxw'));
  let i = zs.indexOf(num(el, 'zoom'));
  if (i < 0) i = zs.length - 1;                                 // the window got narrower since
  zoomTo(el, zs[Math.max(0, Math.min(zs.length - 1, i + dir))], t, x);
}
function follow(el, t) {   // zoomed in: page the view along so the bar stays visible
  const { sc, wrap, w0, w1 } = parts(el);
  if (num(el, 'zoom') === 1) return;
  const x = (t - w0) / (w1 - w0) * wrap.offsetWidth;
  if (x < sc.scrollLeft || x > sc.scrollLeft + sc.clientWidth - 2) sc.scrollLeft = x - sc.clientWidth * 0.1;
}
const span = c => `${tc(c.s)} \\u2192 ${tc(c.e)}   (${(c.e - c.s).toFixed(1)} s)`;
function renderCard(el) {
  const w0 = num(el, 'w0'), w1 = num(el, 'w1'), p = el.plan, mine = own(el);
  const box = el.querySelector('.shades');
  box.textContent = '';
  all().forEach(c => {
    if (c.e <= w0 || c.s >= w1) return;
    const d = document.createElement('div'), a = Math.max(c.s, w0), b = Math.min(c.e, w1);
    d.className = 'shade' + (c.host !== el ? ' other' : c.added ? ' added' : '');
    d.style.left = (100 * (a - w0) / (w1 - w0)) + '%';
    d.style.width = (100 * (b - a) / (w1 - w0)) + '%';
    box.appendChild(d);
  });
  el.querySelector('.times').textContent = `start ${tc(p.s)}  end ${tc(p.e)}  (${(p.e - p.s).toFixed(2)} s)`;
  el.querySelector('.was').textContent = changed(p) ? `was ${tc(p.s0)} - ${tc(p.e0)}` : '';
  el.querySelector('.warn').textContent = p.warn.length ? p.warn.join(', ') + OVERLAP : '';
  el.querySelector('.added-cuts').innerHTML = mine.slice(1).map(c =>
    `<div class="added-row"><span class="tag">New Cut ${c.n}</span><span class="times">start ${tc(c.s)}  end ${tc(c.e)}  (${(c.e - c.s).toFixed(2)} s)</span>` +
    `<button data-id="${c.id}" data-do="s">Start = bar</button><button data-id="${c.id}" data-do="e">End = bar</button>` +
    `<button data-id="${c.id}" data-do="x">Remove</button><span class="warn">${c.warn.length ? c.warn.join(', ') + OVERLAP : ''}</span></div>`).join('');
  const extra = mine.length > 1 ? `   + new ${mine.slice(1).map(c => 'Cut ' + c.n).join(', ')}` : '';
  const title = `Cut ${p.n}   ${span(p)}` + (changed(p) ? '   changed' : '') + extra;
  el.classList.toggle('changed', changed(p) || mine.length > 1);
  el.querySelector('summary').textContent = title;
  document.querySelector(`nav a[href="#${el.id}"]`).textContent = title;
}
function renderAll() {
  const sorted = all().sort((a, b) => a.s - b.s || a.e - b.e);   // Studio numbers its list by start time
  sorted.forEach((c, i) => { c.n = i + 1; c.warn = []; });
  for (let i = 1; i < sorted.length; i++) if (sorted[i].s < sorted[i - 1].e) {
    sorted[i].warn.push(`overlaps Cut ${sorted[i - 1].n}`); sorted[i - 1].warn.push(`overlaps Cut ${sorted[i].n}`); }
  cards.forEach(renderCard);
  const nChanged = plan.filter(changed).length, nNew = added.length;
  let removed = 0, end = -1;                                    // union, so overlaps count once
  sorted.forEach(c => { removed += Math.max(0, c.e - Math.max(c.s, end)); end = Math.max(end, c.e); });
  const dur = +document.body.dataset.duration;
  const hms = t => { t = Math.round(t); return Math.floor(t / 3600) + ':' + String(Math.floor(t % 3600 / 60)).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); };
  document.getElementById('nchanged').textContent = nChanged || nNew ? ` \\u00b7 on this page: ${nChanged} changed, ${nNew} new` : '';
  document.getElementById('removed').textContent = `${hms(removed)}: ${hms(dur)} \\u2192 ${hms(dur - removed)}`;
  document.getElementById('export').value =
    `# ${sorted.length} cuts (${nChanged} changed, ${nNew} new on studio.html), numbered as in Studio, listed last first for entry\\n` +
    sorted.slice().reverse().map(c =>
      `Cut ${String(c.n).padStart(2)}   ${tc(c.s)}  ->  ${tc(c.e)}   (${(c.e - c.s).toFixed(2)} s)` +
      (c.added ? '   NEW' : changed(c) ? `   CHANGED, was ${tc(c.s0)} -> ${tc(c.e0)}` : '')).join('\\n');
}
function setEdge(c, k, t, fromButton = false) {
  const el = c.host;
  t = snap(Math.min(num(el, 'w1'), Math.max(num(el, 'w0'), t)));
  const s = k === 's' ? t : c.s, e = k === 'e' ? t : c.e;
  if (e - s < 1 / FPS - 1e-6) {
    if (fromButton) el.querySelector('.msg').textContent = `Cut ${c.n}: the start has to stay before the end - move the bar first.`;
    return;
  }
  el.querySelector('.msg').textContent = '';
  c[k] = t;
  renderAll();
  if (fromButton) save();
}
function addCut(el) {
  const w1 = num(el, 'w1');
  let s = snap(num(el, 'pos')), e = snap(Math.min(w1, s + NEW_LEN));
  if (e - s < NEW_LEN / 2) s = snap(e - NEW_LEN);                 // bar at the window's end: grow to the left
  added.push({ id: ++uid, host: el, s, e, added: true });
  renderAll(); save();
}
function tick() {
  if (!cur) return;
  let t = A.currentTime;
  if (cur.querySelector('.skip').checked) {                      // jump over every cut, added ones too
    const c = all().find(c => t >= c.s && t < c.e);
    if (c) { A.currentTime = c.e; t = c.e; }
  }
  if (t >= num(cur, 'w1')) A.pause();                            // the end of the spectrogram
  show(cur, t);
  follow(cur, t);
  if (!A.paused) raf = requestAnimationFrame(tick);
}
function label(el, playing) { el.querySelector('.play').textContent = playing ? 'Pause' : 'Play'; }
function play(el) {
  if (cur && cur !== el) { A.pause(); label(cur, false); }
  cur = focusEl = el;
  const nowcut = document.getElementById('nowcut');
  if (nowcut) nowcut.textContent = `Playing Cut ${el.plan.n}`;
  let t = num(el, 'pos');
  if (t >= num(el, 'w1') - 0.05) t = show(el, Math.max(num(el, 'w0'), el.plan.s - CTX));
  follow(el, t);
  A.currentTime = t;
  A.play().then(() => { label(el, true); cancelAnimationFrame(raf); raf = requestAnimationFrame(tick); })
          .catch(err => { if (err.name !== 'AbortError') el.querySelector('.err').textContent = 'Could not play: ' + err.message; });  // AbortError = paused before playback began
}
A.addEventListener('pause', () => { if (cur) label(cur, false); cancelAnimationFrame(raf); });
A.addEventListener('error', () => document.querySelectorAll('.err').forEach(e => e.textContent = 'Media failed to load: ' + A.src));
const player = document.getElementById('player');
if (player) {                                                   // video preview: hide/show, remembered per browser
  const btn = document.getElementById('vtoggle');
  const setHidden = h => { player.classList.toggle('hidden', h); btn.textContent = h ? 'Show video' : 'Hide video'; };
  try { setHidden(localStorage.getItem('studio-video-hidden') === '1'); } catch (err) { storageError('loaded', err); }
  btn.addEventListener('click', () => {
    const h = !player.classList.contains('hidden');
    setHidden(h); btn.blur();
    try { localStorage.setItem('studio-video-hidden', h ? '1' : '0'); } catch (err) { storageError('saved', err); }
  });
}
load();
cards.forEach(el => {
  el.dataset.zoom = 1;
  show(el, Math.max(num(el, 'w0'), el.plan.s - CTX));
  el.querySelector('.play').addEventListener('click', () => (cur === el && !A.paused) ? A.pause() : play(el));
  const wrap = el.querySelector('.specwrap');
  const tAt = ev => { const r = wrap.getBoundingClientRect();
    return num(el, 'w0') + Math.min(1, Math.max(0, (ev.clientX - r.left) / r.width)) * (num(el, 'w1') - num(el, 'w0')); };
  const px = t => { const r = wrap.getBoundingClientRect(); return r.left + (t - num(el, 'w0')) / (num(el, 'w1') - num(el, 'w0')) * r.width; };
  const edgeAt = ev => {   // within 8 px of an edge of this card's cuts: drag that edge instead of the bar
    let best = null, bd = 8;
    own(el).forEach(c => ['s', 'e'].forEach(k => { const d = Math.abs(ev.clientX - px(c[k])); if (d <= bd) { bd = d; best = { c, k }; } }));
    return best; };
  const sc = el.querySelector('.specscroll');
  const barX = () => { const x = px(num(el, 'pos')) - sc.getBoundingClientRect().left;   // bar off screen: centre it
    return x >= 0 && x <= sc.clientWidth ? x : sc.clientWidth / 2; };
  ['zin', 'zout'].forEach((k, i) => el.querySelector('.' + k).addEventListener('click', ev => {
    focusEl = el; ev.currentTarget.blur();                      // so the space bar plays again, not zooms again
    zoomStep(el, i ? -1 : 1, num(el, 'pos'), barX()); }));
  let wheel = 0;
  sc.addEventListener('wheel', ev => {   // Ctrl+wheel zooms around the pointer (a trackpad pinch sends the same)
    if (!ev.ctrlKey) return;
    ev.preventDefault();
    wheel += ev.deltaMode === 1 ? ev.deltaY * 33 : ev.deltaY;   // deltaMode 1: lines, not pixels
    if (Math.abs(wheel) < 50) return;
    const dir = wheel < 0 ? 1 : -1;
    wheel = 0;
    focusEl = el;
    zoomStep(el, dir, tAt(ev), ev.clientX - sc.getBoundingClientRect().left); }, { passive: false });
  sc.addEventListener('scroll', () => axis(el));
  let drag = null;
  const move = ev => {
    if (drag === 'bar') { const t = show(el, tAt(ev)); if (cur === el && !A.paused) A.currentTime = t; }
    else setEdge(drag.c, drag.k, tAt(ev)); };
  wrap.addEventListener('pointerdown', ev => { focusEl = el; drag = edgeAt(ev) || 'bar'; wrap.setPointerCapture(ev.pointerId); move(ev); });
  wrap.addEventListener('pointermove', ev => { if (drag) move(ev); else wrap.style.cursor = edgeAt(ev) ? 'col-resize' : 'ew-resize'; });
  wrap.addEventListener('pointerup', () => { if (drag && drag !== 'bar') save(); drag = null; });
  el.querySelector('.set-s').addEventListener('click', () => { focusEl = el; setEdge(el.plan, 's', num(el, 'pos'), true); });
  el.querySelector('.set-e').addEventListener('click', () => { focusEl = el; setEdge(el.plan, 'e', num(el, 'pos'), true); });
  el.querySelector('.reset').addEventListener('click', () => { el.plan.s = el.plan.s0; el.plan.e = el.plan.e0; renderAll(); save(); });
  el.querySelector('.add').addEventListener('click', () => { focusEl = el; addCut(el); });
  el.querySelector('.added-cuts').addEventListener('click', ev => {   // buttons of the added cuts, rebuilt on every render
    const b = ev.target.closest('button');
    if (!b) return;
    focusEl = el;
    const c = added.find(x => x.id === +b.dataset.id);
    if (b.dataset.do === 'x') { added = added.filter(x => x !== c); renderAll(); save(); }
    else setEdge(c, b.dataset.do, num(el, 'pos'), true); });
  el.querySelectorAll('.jump').forEach(b => b.addEventListener('click', () => { show(el, parseFloat(b.dataset.t)); play(el); }));
});
renderAll();
cards.forEach(axis);
window.addEventListener('resize', () => cards.forEach(axis));
document.getElementById('copy').addEventListener('click', () =>
  navigator.clipboard.writeText(document.getElementById('export').value)
    .then(() => document.getElementById('copied').textContent = 'copied')
    .catch(err => document.getElementById('copied').textContent = 'Copy failed: ' + err.message + ' - select the text and copy it by hand'));
document.getElementById('reset-all').addEventListener('click', () => {
  if (!confirm('Put every cut back to the planned times and remove the cuts you added?')) return;
  plan.forEach(c => { c.s = c.s0; c.e = c.e0; }); added = []; renderAll(); save(); });
document.addEventListener('keydown', ev => {
  const tag = document.activeElement.tagName;
  if (['INPUT', 'TEXTAREA', 'SELECT'].includes(tag)) return;
  if (ev.code === 'Space' && cur && tag !== 'BUTTON') { ev.preventDefault(); A.paused ? play(cur) : A.pause(); }
  if ((ev.code === 'ArrowLeft' || ev.code === 'ArrowRight') && focusEl) {   // move the bar 0.2 s, Shift: 1 s
    ev.preventDefault();
    const t = show(focusEl, num(focusEl, 'pos') + (ev.code === 'ArrowLeft' ? -1 : 1) * (ev.shiftKey ? 1 : 0.2));
    follow(focusEl, t);
    if (cur === focusEl && !A.paused) A.currentTime = t; } });
"""


def list_id(scuts) -> str:
    """Short fingerprint of a Studio cut list, shown on studio.html and by --check-studio."""
    return hashlib.sha1(json.dumps([[c["start_tc"], c["end_tc"]] for c in scuts]).encode()).hexdigest()[:8]


def check_studio(out_dir: Path, markers_file: Path) -> None:
    """Compare the cuts in Studio (the timeline markers, saved from Playwright) with the
    plan in edit_points.json and with the cut count of studio.html on disk. Lists every
    difference and exits non-zero on any mismatch."""
    data = json.loads((out_dir / "edit_points.json").read_text(encoding="utf-8"))
    plan = [(c["start_tc"], c["end_tc"]) for c in data["studio_cuts"]]
    text = markers_file.read_text(encoding="utf-8")
    first = min(i for i in (text.find("["), text.find("{")) if i >= 0)
    obj = json.loads(text[first: max(text.rfind("]"), text.rfind("}")) + 1])
    labels = obj["markers"] if isinstance(obj, dict) else obj
    vals = [lab.split("marker ")[1] for lab in labels]
    if len(vals) < 2 or len(vals) % 2:
        raise ValueError(f"{markers_file}: expected start/end marker pairs, got {len(vals)} labels")
    pairs = list(zip(vals[0::2], vals[1::2]))
    whole = pairs[0]
    fps = int(data["fps"])

    def sec(tc):
        h, m, s_, f = map(int, tc.split(":"))
        return h * 3600 + m * 60 + s_ + f / fps
    studio = sorted(pairs[1:], key=lambda c: sec(c[0]))
    page_n = (out_dir / "edit_review" / "studio.html").read_text(encoding="utf-8").count('<details open class="cut"')
    log.info(f"Studio: {len(studio)} cuts | plan (edit_points.json): {len(plan)} | studio.html: {page_n} "
             f"| list {list_id(data['studio_cuts'])} | whole video {whole[0]} - {whole[1]}")
    only_plan = [c for c in plan if c not in studio]
    only_studio = [c for c in studio if c not in plan]
    for c in only_plan:
        log.error(f"in the plan, not in Studio: {c[0]} -> {c[1]} ({sec(c[1]) - sec(c[0]):.2f} s)")
    for c in only_studio:
        log.error(f"in Studio, not in the plan: {c[0]} -> {c[1]} ({sec(c[1]) - sec(c[0]):.2f} s)")
    if page_n != len(plan):
        log.error(f"studio.html shows {page_n} cuts but the plan has {len(plan)}: rebuild the page (--report-only)")
    if only_plan or only_studio or page_n != len(plan) or len(studio) != len(plan):
        raise SystemExit(1)
    log.info(f"OK: Studio holds exactly the {len(plan)} planned cuts, frame for frame")


def build_studio_page(data, scuts, rows, page: Path, wav: Path, video: Path | None = None):
    """One collapsible section per cut, numbered exactly like Studio's Cut 1..N list.
    One shared player streams the full lecture: the 360p video preview in a panel that
    stays at the top while scrolling when `video` is given (--video-preview), else the WAV.
    Each cut's spectrogram has a draggable bar, and "skip the cut" plays the window as it
    will sound after the edit.
    The cut's edges can be moved on the page (drag an edge, or Start/End = bar) and new cuts
    added inside a cut's window; the numbering follows Studio's order. The changes stay in
    the browser's localStorage and feed a copyable list at the bottom."""
    media_file = video or wav
    if not media_file.exists():
        raise FileNotFoundError(f"The Studio page plays {media_file}, which is missing")
    esc = html.escape
    by_id = {c["id"]: c for c in data["cuts"]}
    sections = []
    for sc in scuts:
        src = [by_id[i] for i in sc["sources"]]
        content = [c for c in src if c["source"] == "content"]
        sil = [c for c in src if c["source"] == "silence"]
        why = [f'<div class="reason"><span class="badge {c["kind"]}">{"safe" if c["kind"] == "safe" else "your call"}</span> '
               f'{esc(c["reason"])}</div>' for c in content]
        if sil and not content:
            why.append(f'<div class="reason">{esc(sil[0]["reason"]) if len(sil) == 1 else f"{len(sil)} silences"}</div>')
        flags = []
        for c in sil:
            for f in c["flags"]:
                m = re.search(r"at (\d+:\d\d:\d\d(?:\.\d)?)", f)
                jump = f'<button class="jump" data-t="{parse_t(m.group(1)) - 1.0:.2f}">play here</button>' if m else ""
                flags.append(f'<div class="flag">{esc(f)}{jump}</div>')
        tx = []
        for r in snippet(rows, sc["start"], sc["end"]):
            if r is None:
                tx.append('<div>...</div>')
                continue
            cls = "in" if sc["start"] - 1 <= r[0] <= sc["end"] else ""
            tx.append(f'<div class="{cls}"><span class="t">{esc(r[1])}</span>{esc(r[2])}</div>')
        w0, w1 = sc["spec_window"]
        title = f"Cut {sc['n']}   {sc['start_tc']} \u2192 {sc['end_tc']}   ({sc['end'] - sc['start']:.1f} s)"
        sections.append((f"cut-{sc['n']}", title, f"""
<details open class="cut" id="cut-{sc['n']}" data-w0="{w0}" data-w1="{w1}" data-s0="{sc['start']}" data-e0="{sc['end']}" data-pxw="{sc['spec_px']}">
<summary>{esc(title)}</summary>
{''.join(why)}{''.join(flags)}
<div class="ctl"><button class="play">Play</button><span class="now"></span>
  <label><input type="checkbox" class="skip"> skip the cuts (hear the result)</label>
  <span class="zoom">zoom <button class="zout">-</button><span class="zl">1&times;</span><button class="zin">+</button></span><span class="err"></span></div>
<div class="specscroll"><div class="specwrap"><img loading="lazy" src="media/{sc['id']}_spec.png" alt="spectrogram cut {sc['n']}"><div class="shades"></div><div class="bar"></div></div></div>
<div class="axis"><span class="a0">{fmt_t(w0)}</span><span>0-5 kHz. Red: this cut, orange: cuts you added, grey: neighbouring cuts. Drag an edge to move it, anywhere else to move the bar. Ctrl+wheel zooms, Shift+wheel scrolls</span><span class="a1">{fmt_t(w1)}</span></div>
<div class="edit"><span class="times"></span><button class="set-s">Start = bar</button><button class="set-e">End = bar</button>
  <button class="reset">Reset</button><button class="add">Add a cut at the bar</button><span class="was"></span><span class="warn"></span><span class="msg"></span></div>
<div class="added-cuts"></div>
<div class="tx">{''.join(tx)}</div>
</details>"""))
    removed = sum(c["end"] - c["start"] for c in scuts)
    sections.append(("export-list", "Cut list with your changes (last first)", f"""
<details open id="export-list"><summary>Cut list with your changes (last first)</summary>
<p class="note">The same format as <code>studio_cuts.txt</code>, renumbered in Studio's order. Changed cuts say what they
were, added ones say NEW. Changes stay in this browser for this cut list only; enter them in Studio yourself, or paste
this list to Claude.</p>
<p><button id="copy">Copy list</button> <span id="copied"></span> <button id="reset-all">Put all cuts back</button></p>
<textarea id="export" readonly></textarea>
</details>"""))
    toc = "".join(f'<li><a href="#{sid}">{esc(title)}</a></li>' for sid, title, _ in sections)
    rel_media = (Path("..") / media_file.relative_to(page.parent.parent)).as_posix()
    if video:
        player = (f'<div id="player"><video id="media" preload="metadata" playsinline src="{rel_media}"></video>'
                  '<div class="pinfo"><span id="nowcut">Press Play on a cut</span>'
                  '<button id="vtoggle">Hide video</button></div></div>')
    else:
        player = f'<audio id="media" preload="metadata" src="{rel_media}"></audio>'
    page.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Studio cuts {esc(data['video_id'])}</title>
<style>{PAGE_CSS}{STUDIO_CSS}</style></head>
<body{' class="has-video"' if video else ''} data-fps="{data['fps']:g}" data-ctx="{PLAY_CONTEXT_S:g}" data-duration="{data['duration']}" data-list="{list_id(scuts)}"><main>
<h1>Studio cuts: {esc(data['title'])}</h1>
<p class="stamp"><b>{len(scuts)} cuts</b> &middot; list {list_id(scuts)} &middot; built {time.strftime("%Y-%m-%d %H:%M")}<span id="nchanged"></span>
 - reload this tab if the list changed since you opened it</p>
<p class="warn" id="storage"></p>
<p class="sub">{len(scuts)} cuts, numbered and timed exactly as in YouTube Studio's Trim &amp; cut list
({data['fps']:g} fps, H:MM:SS:FF). Removes <span id="removed">{fmt_t(removed, 0)}: {fmt_t(data['duration'], 0)} &rarr; {fmt_t(data['duration'] - removed, 0)}</span>.
Play starts {PLAY_CONTEXT_S:g} s before the cut and runs to the end of the spectrogram; space bar pauses, &larr;/&rarr; move the bar
0.2 s (Shift: 1 s). <b>Zoom</b> with the +/- buttons or Ctrl+mouse wheel; the spectrogram then scrolls sideways
(scrollbar or Shift+wheel) and follows the bar while playing. <b>To move a cut's edge</b>, drag it, or put the bar there and press Start = bar / End = bar
(whole frames; the spectrogram has {STUDIO_MARGIN_S:g} s of room either side). <b>Add a cut at the bar</b> makes a new 1 s cut
there, to drag into shape; every Cut number on the page and in the list follows Studio's order. To drop a cut, delete that
Cut N in Studio before saving.</p>
{player}
<nav><ol>{toc}</ol></nav>
{''.join(inner for _, _, inner in sections)}
</main>
<script>{STUDIO_JS}</script>
</body></html>
""", encoding="utf-8")


def levels(out_dir: Path, source: Path | None = None):
    """Audio, 10 ms speech-band levels, the silence threshold (noise floor + 20 dB)
    and the sound mask - shared by the analysis and --speech-map."""
    meta = json.loads((out_dir / "metadata.json").read_text(encoding="utf-8"))
    wav = ensure_wav(out_dir, meta, source)
    log.info(f"Reading {wav.name} and measuring levels")
    x, sr = sf.read(wav, dtype="float32")
    if sr != SR:
        raise ValueError(f"{wav} is {sr} Hz, expected {SR}")
    db = frame_levels(x)
    # Exact digital silence (all-zero samples, -120 dB here) is not the room's noise floor. ML50's
    # 11-min break was 10% of the frames and dragged the 5th percentile to -120 dB, so only 1 pause
    # was found; without it the floor was -94 dB and the counts matched ML48's (2026-10-14).
    digital = db <= -119.9
    floor = float(np.percentile(db[~digital], 5))
    thr = floor + 20
    sound = sound_mask(db, thr)
    log.info(f"{len(x) / SR / 60:.1f} min audio, noise floor {floor:.1f} dB (excluding {100 * digital.mean():.0f}% "
             f"digital silence), silence threshold {thr:.1f} dB, {100 * (~sound).mean():.0f}% of frames silent")
    return meta, x, db, floor, thr, sound


def speech_map(out_dir: Path, start: str, end: str, source: Path | None = None) -> None:
    """Print where the speech and the pauses are, 0.1 s per character, so a content
    cut's edges can be put inside a pause. '#' sound, '.' a click or short sound
    (under 0.2 s, counts as silence), '_' silence. One line per 10 s."""
    _, _, db, _, thr, sound = levels(out_dir, source)
    i0, i1 = int(parse_t(start) * 100), min(int(parse_t(end) * 100), len(sound))
    if i1 <= i0:
        raise ValueError(f"--speech-map end {end} is not after start {start}")
    for row in range(i0 - i0 % 1000, i1, 1000):
        chars = []
        for k in range(row, min(row + 1000, i1), 10):
            if k < i0:
                chars.append(" ")
            elif sound[k:k + 10].any():
                chars.append("#")
            elif (db[k:k + 10] > thr).any():
                chars.append(".")
            else:
                chars.append("_")
        line = "".join(chars)
        print(f"{fmt_t(row / 100, 0)}  " + "|".join(line[j:j + 10] for j in range(0, len(line), 10)))


def analyse(out_dir: Path, min_silence: float, pad: float, source: Path | None = None) -> dict:
    meta, x, db, floor, thr, sound = levels(out_dir, source)
    duration = len(x) / SR

    cuts = silence_cuts(db, sound, thr, min_silence, pad)
    log.info(f"{len(cuts)} silences >= {min_silence:g} s ({sum(c['run_len'] for c in cuts) / 60:.1f} min raw)")
    cc_path = out_dir / "content_cuts.json"
    if cc_path.exists():
        spec = json.loads(cc_path.read_text(encoding="utf-8"))
        content = [snap_content(c, sound, duration, pad) for c in spec["cuts"]]
        log.info(f"{len(content)} content cuts from {cc_path.name}")
    else:
        log.warning(f"No {cc_path} - silence cuts only. Write it in the LLM stage for content cuts.")
        content = []
    for k, c in enumerate(content, 1):
        c["id"] = f"C{k:02d}"
    for k, c in enumerate(sorted(cuts, key=lambda c: c["start"]), 1):
        c["id"] = f"S{k:03d}"
    all_cuts = content + sorted(cuts, key=lambda c: c["start"])
    return {
        "video_id": meta["id"], "title": meta["title"], "duration": round(duration, 2),
        "params": {"min_silence": min_silence, "pad": pad, "floor_db": round(floor, 1),
                   "audio_source": audio_source(out_dir / "audio" / f"{meta['id']}_16k.wav"),
                   "threshold_db": round(thr, 1), "blip_s": BLIP_FRAMES / 100},
        "cuts": all_cuts,
    }


def main():
    ap = argparse.ArgumentParser(description="Find cut points in an unedited lecture and build a review page.")
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--min-silence", type=float, help="shortest silence to cut, seconds (default 3.0)")
    ap.add_argument("--pad", type=float, help="pause left on each side of a cut, seconds (default 0.35)")
    ap.add_argument("--report-only", action="store_true", help="rebuild the page and clips from edit_points.json")
    ap.add_argument("--audio", type=Path,
                    help="the local recording that was uploaded (e.g. the Zoom download); "
                         "converted instead of downloading the audio from YouTube")
    ap.add_argument("--check-studio", type=Path, metavar="MARKERS_JSON",
                    help="compare Studio's cuts (timeline marker labels saved from Playwright) "
                         "with the plan and studio.html, then exit")
    ap.add_argument("--speech-map", nargs=2, metavar=("START", "END"),
                    help="print speech/pause map between two times (H:MM:SS) and exit")
    ap.add_argument("--video-preview", action="store_true",
                    help="also make a 360p copy of the recording (once; heavy, up to ~1 h for a 2 h recording) "
                         "so studio.html plays video instead of the WAV. Later runs reuse it")
    ap.add_argument("--video-encoder", choices=["qsv", "x264"], default="qsv",
                    help="for --video-preview: Intel Quick Sync on the iGPU (default) or libx264 on the CPU")
    args = ap.parse_args()
    if args.speech_map:
        setup_logging()
        speech_map(args.output_dir, *args.speech_map, source=args.audio)
        return
    if args.check_studio:
        setup_logging()
        check_studio(args.output_dir, args.check_studio)
        return
    if args.report_only and (args.min_silence is not None or args.pad is not None):
        ap.error("--min-silence/--pad only apply to a fresh analysis; --report-only reuses edit_points.json as is")
    args.min_silence = 3.0 if args.min_silence is None else args.min_silence   # the user's pick, ML48
    args.pad = 0.35 if args.pad is None else args.pad
    setup_logging()
    t0 = time.time()
    out_dir = args.output_dir
    jpath = out_dir / "edit_points.json"

    if args.report_only:
        data = json.loads(jpath.read_text(encoding="utf-8"))
    else:
        data = analyse(out_dir, args.min_silence, args.pad, args.audio)
        jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    fps = video_fps(data, f"https://youtu.be/{data['video_id']}")
    scuts = studio_cuts(data, fps)
    removed = sum(c["end"] - c["start"] for c in scuts)
    (out_dir / "studio_cuts.txt").write_text(
        f"# {data['title']} - pre-ticked cuts, numbered as in Studio, listed last first for entry\n"
        f"# {len(scuts)} cuts at {fps} fps, removes {fmt_t(removed, 0)}, new length {fmt_t(data['duration'] - removed, 0)}\n"
        + "\n".join(studio_lines(scuts)) + "\n", encoding="utf-8")

    review = out_dir / "edit_review"
    media = review / "media"
    media.mkdir(parents=True, exist_ok=True)
    x, _ = sf.read(out_dir / "audio" / f"{data['video_id']}_16k.wav", dtype="float32")
    for c in tqdm(data["cuts"], desc="clips + spectrograms"):
        write_clips(x, c, media)
        draw_spectrogram(x, c, data["duration"], media)
    for c in scuts:                       # the Studio page plays the full WAV, so no clips
        draw_spectrogram(x, c, data["duration"], media, margin=STUDIO_MARGIN_S, shade=False, px_per_s=STUDIO_PX_PER_S)
    data["studio_cuts"] = scuts
    jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    rows = load_transcript(out_dir / "transcript.txt")
    build_page(data, rows, review / "index.html")
    video = make_video_proxy(out_dir, data, args.video_encoder) if args.video_preview else existing_video_proxy(out_dir, data)
    log.info(f"studio.html plays the video preview {video}" if video
             else "studio.html plays the WAV (--video-preview makes a video preview)")
    build_studio_page(data, scuts, rows, review / "studio.html", out_dir / "audio" / f"{data['video_id']}_16k.wav", video)
    log.info(f"Pre-ticked: {len(scuts)} Studio cuts removing {removed / 60:.1f} min "
             f"({fmt_t(data['duration'], 0)} -> {fmt_t(data['duration'] - removed, 0)})")
    log.info(f"Wrote {jpath}, {out_dir / 'studio_cuts.txt'}, {review / 'index.html'}, "
             f"{review / 'studio.html'} in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
