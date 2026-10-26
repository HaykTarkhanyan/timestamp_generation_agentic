"""Build the studio.html review pages for the Vahagn linear algebra pieces, one at a time: the silence pass at
--min-silence 4 from the local raw file, plus the 360p video preview (DECISIONS #35; the user's pick on 21.1).
Reruns reuse an existing preview, so after writing content_cuts.json this is also the way to rebuild a page.

    python scripts/non_essential/vahagn_plan_queue.py                 # all pieces with a transcript
    python scripts/non_essential/vahagn_plan_queue.py 23.2 24.1       # some
    python scripts/non_essential/vahagn_plan_queue.py --no-preview    # pages only (~40-100 s each)
Expected: ~4 min per piece with a new preview (21.1: 22 min of video, preview 189 s), ~1.5 h for 23 pieces.
Progress with an ETA goes to stdout and logs/vahagn_plan_queue.log.
"""
import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_plan_queue.log", encoding="utf-8")])
log = logging.getLogger(__name__)


def pieces() -> list[tuple[str, Path, Path]]:
    """(section, output dir, raw file) for every upload in uploads.json that has a fetched transcript."""
    uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
    out = []
    for u in uploads:
        dirs = sorted(REPO.glob(f"output/*_{u['id']}"))
        if len(dirs) != 1:
            raise RuntimeError(f"{u['section']} {u['id']}: expected one output dir, found {dirs}")
        raws = [*RAW.glob(f"Videos Part */VidSection {u['section']}.mp4"),
                *RAW.glob(f"already_on_youtube/VidSection {u['section']}.mp4")]   # 21.2 lives there
        if len(raws) != 1:
            raise RuntimeError(f"{u['section']}: expected one raw file, found {raws}")
        if not (dirs[0] / "transcript.txt").exists():
            raise RuntimeError(f"{u['section']}: no transcript in {dirs[0]}")
        out.append((u["section"], dirs[0], raws[0]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*")
    ap.add_argument("--no-preview", action="store_true")
    ap.add_argument("--min-silence", type=float, default=4.0)
    ap.add_argument("--highpass", action="store_true",
                    help="analyse a 150 Hz high-passed copy (audio/hp150_source.wav): for the recordings with mains "
                         "hum (noise floor about -65 dB instead of -85), where the hum makes quiet speech count as "
                         "silence (23.3.b: 91%% of frames 'silent' raw, 66%% filtered). The preview keeps the raw sound.")
    args = ap.parse_args()

    todo = [p for p in pieces() if not args.sections or p[0] in args.sections]
    if args.sections and len(todo) != len(args.sections):
        raise SystemExit(f"unknown sections: {set(args.sections) - {p[0] for p in todo}}")
    t0 = time.time()
    for i, (sec, out, raw) in enumerate(todo, 1):
        audio = raw
        if args.highpass:
            audio = out / "audio" / "hp150_source.wav"
            if not audio.exists():
                audio.parent.mkdir(exist_ok=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vn", "-af",
                                "highpass=f=150,highpass=f=150", "-ac", "1", "-ar", "48000", str(audio)], check=True)
            vid = json.loads((out / "metadata.json").read_text(encoding="utf-8"))["id"]
            wav, src = out / "audio" / f"{vid}_16k.wav", out / "audio" / f"{vid}_16k.source.txt"
            if src.exists() and "hp150_source" not in src.read_text(encoding="utf-8"):
                # find_edit_points refuses a different --audio while the old WAV exists; both files are derived
                log.info(f"{sec}: replacing the analysis WAV built from the raw sound with the high-passed one")
                wav.unlink()
                src.unlink()
            proxy_src = out / "video" / f"{vid}_360p.source.txt"
            if proxy_src.exists():
                lines = proxy_src.read_text(encoding="utf-8").splitlines()
                if Path(lines[0].strip()) == raw and (len(lines) == 1 or
                                                      Path(lines[1].removeprefix("audio: ").strip()) == raw):
                    # the preview was encoded from the raw file; the high-passed copy has the same timeline.
                    # Record the match the way find_edit_points' --video mode does (line 2 "audio: <source>"),
                    # after checking the two lengths agree.
                    dur = lambda p: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                          "-of", "csv=p=0", str(p)], capture_output=True, text=True,
                                                         check=True).stdout)
                    d_raw, d_hp = dur(raw), dur(audio)
                    if abs(d_raw - d_hp) > 0.1:
                        raise RuntimeError(f"{sec}: high-passed copy {d_hp:.2f} s vs raw {d_raw:.2f} s")
                    proxy_src.write_text(f"{lines[0]}\naudio: {audio}\n", encoding="utf-8")
                    log.info(f"{sec}: preview kept (raw {d_raw:.2f} s = high-passed {d_hp:.2f} s)")
        cmd = [sys.executable, "scripts/find_edit_points.py", "--output-dir", str(out), "--audio", str(audio),
               "--min-silence", str(args.min_silence)]
        if not args.no_preview:
            cmd.append("--video-preview")
            if audio != raw:
                cmd += ["--video", str(raw)]
        r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        tail = [ln for ln in r.stdout.splitlines() + r.stderr.splitlines() if "Pre-ticked" in ln or "ERROR" in ln]
        if r.returncode != 0:
            log.error(f"{sec}: find_edit_points failed:\n{r.stderr[-1500:]}")
            raise SystemExit(1)
        el = time.time() - t0
        log.info(f"{i}/{len(todo)} {sec}: {tail[-1].split('INFO ')[-1] if tail else 'done'}  "
                 f"({el / 60:.1f} min elapsed, ~{el / i * (len(todo) - i) / 60:.1f} min left)")
    log.info(f"all {len(todo)} done in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
