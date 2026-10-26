"""Sound-only fix of the Vahagn linear algebra pieces (DECISIONS #38): Ashot's chain (80 Hz low cut + light afftdn),
a fixed gain to the chosen loudness with a -1 dBFS peak limiter, the picture copied untouched. The timeline does not
change, so the studio.html cut lists still apply; the cuts are entered in YouTube Studio after the upload.

    python scripts/non_essential/vahagn_audio_fix.py --target-lufs -16          # all 25 pieces
    python scripts/non_essential/vahagn_audio_fix.py --target-lufs -16 21.1     # some
    python scripts/non_essential/vahagn_audio_fix.py --own-level                # cleanup only, no gain
Expected: about 15-20x realtime (28.3.b, 5:14: pass 1, chain + loudness into a temporary float WAV, 4 s; pass 2,
gain + AAC + picture copied, ~9 s; to be confirmed by the first full run), ~25-30 min for all 25 (8.06 h). One core. Progress with an ETA to stdout and
logs/vahagn_audio_fix.log; results in _knowledge/vahagn_linalg/audio_fix.json; files in <raw folder>/audio_fixed/.
"""
import argparse
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
OUT = RAW / "audio_fixed"
# ffmpeg 9 (as for the renders): the chocolatey ffmpeg 5.1 on PATH took 23.6 s for pass 2 of 28.3.b, this one 8.6 s
FFMPEG = r"C:\Users\hayk_\tools\ffmpeg-9\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
CHAIN = "highpass=f=80,afftdn=nr=12:nf=-50:tn=1"   # render_lecture.py --denoise
LIMIT = "alimiter=limit=0.891:level=0"            # render_lecture.py: peaks at -1 dBFS, no auto-gain of its own
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_audio_fix.log", encoding="utf-8")])
log = logging.getLogger(__name__)


def ffmpeg(args: list) -> str:
    r = subprocess.run([FFMPEG, "-nostats", "-hide_banner", *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{r.stderr[-1500:]}")
    return r.stderr


def ebur(stderr: str) -> tuple[float, float]:
    """Integrated loudness and sample peak from the ebur128 summary."""
    return (float(re.findall(r"I:\s+(-?[\d.]+) LUFS", stderr)[-1]),
            float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", stderr)[-1]))


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,duration",
                        "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return {s["codec_type"]: s for s in json.loads(r.stdout)["streams"]}


def pieces() -> list[tuple[str, Path]]:
    uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
    out = []
    for u in uploads:
        raws = [*RAW.glob(f"Videos Part */VidSection {u['section']}.mp4"),
                *RAW.glob(f"already_on_youtube/VidSection {u['section']}.mp4")]
        if len(raws) != 1:
            raise RuntimeError(f"{u['section']}: expected one raw file, found {raws}")
        out.append((u["section"], raws[0]))
    return out


def fix(sec: str, raw: Path, target: float | None) -> dict:
    dest = OUT / f"{raw.stem} fixed{raw.suffix}"   # YouTube's first title is the file name: tells them from the raw uploads
    tmp = OUT / f"_tmp_{sec}.wav"
    if target is None:
        ffmpeg(["-y", "-i", raw, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", CHAIN, "-ar", "48000",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dest])
        before, gain = None, 0.0
    else:
        # pass 1: the slow chain once, measuring its loudness on the way into a float WAV (no rounding before the gain)
        before, _ = ebur(ffmpeg(["-y", "-i", raw, "-vn", "-af", f"{CHAIN},ebur128=peak=sample", "-c:a", "pcm_f32le",
                                 tmp]))
        gain = target - before
        ffmpeg(["-y", "-i", raw, "-i", tmp, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                # 48 kHz: the native AAC encoder took 11.9 s at the recordings' 32 kHz vs 5.2 s at 48 kHz (28.3.b);
                # also what YouTube recommends and what the loudness samples were encoded at
                "-af", f"volume={gain:.2f}dB,{LIMIT}", "-ar", "48000", "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart", dest])
        tmp.unlink()   # this run's own temporary file, by its literal name
    after, peak = ebur(ffmpeg(["-i", dest, "-vn", "-af", "ebur128=peak=sample", "-f", "null", "-"]))
    a, b = probe(raw), probe(dest)
    if (b["video"]["codec_name"], b["video"]["width"], b["video"]["height"]) != \
            (a["video"]["codec_name"], a["video"]["width"], a["video"]["height"]):
        raise RuntimeError(f"{sec}: picture changed: {a['video']} -> {b['video']}")
    for kind in ("video", "audio"):
        if abs(float(a[kind]["duration"]) - float(b[kind]["duration"])) > 0.05:
            raise RuntimeError(f"{sec}: {kind} length {a[kind]['duration']} -> {b[kind]['duration']}")
    return {"section": sec, "raw": str(raw), "output": str(dest), "lufs_after_chain": before, "gain_db": round(gain, 2),
            "lufs_out": after, "peak_out_dbfs": peak, "duration_s": float(b["video"]["duration"]),
            "size_mb": round(dest.stat().st_size / 1e6, 1)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*")
    lvl = ap.add_mutually_exclusive_group(required=True)
    lvl.add_argument("--target-lufs", type=float)
    lvl.add_argument("--own-level", action="store_true")
    args = ap.parse_args()
    todo = [p for p in pieces() if not args.sections or p[0] in args.sections]
    if args.sections and len(todo) != len(args.sections):
        raise SystemExit(f"unknown sections: {set(args.sections) - {p[0] for p in todo}}")
    OUT.mkdir(exist_ok=True)
    res_path = REPO / "_knowledge/vahagn_linalg/audio_fix.json"
    results = json.loads(res_path.read_text(encoding="utf-8")) if res_path.exists() else {}
    total = sum(float(probe(r)["video"]["duration"]) for _, r in todo)
    t0, done_s = time.time(), 0.0
    for i, (sec, raw) in enumerate(todo, 1):
        r = fix(sec, raw, args.target_lufs)
        results[sec] = r
        res_path.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
        done_s += r["duration_s"]
        el = time.time() - t0
        log.info(f"{i}/{len(todo)} {sec}: {r['lufs_after_chain']} -> {r['lufs_out']:.1f} LUFS (gain {r['gain_db']:+.1f} dB, "
                 f"peak {r['peak_out_dbfs']:.1f} dBFS)  {el / 60:.1f} min elapsed, "
                 f"~{el / done_s * (total - done_s) / 60:.1f} min left")
    log.info(f"all {len(todo)} done in {(time.time() - t0) / 60:.1f} min; files in {OUT}")


if __name__ == "__main__":
    main()
