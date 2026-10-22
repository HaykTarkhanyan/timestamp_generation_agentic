"""Put the ASOF intro and outro around a lecture recording without re-encoding the lecture video.

Run:  python scripts/concat_intro_outro.py <lecture.mp4> [-o out.mp4]
      (default output: <lecture>_asof.mp4 next to the input)
Expected wall-clock: ~11 min for a 1.5 h Zoom recording (measured 657 s on ANT Lecture 16,
2026-10-20), one CPU core. Nearly all of it is the AAC encode of the lecture audio: ffmpeg's
native AAC encoder runs ~7.7 s per minute of audio here; the video copy takes 0.04 s per
minute. The lecture's video is copied as-is; its audio is re-encoded to 48 kHz stereo AAC so
the intro music keeps its quality; only the ~16 s of intro and outro are re-encoded, to the
lecture's frame size (padded with white if its shape differs), frame rate and color tags. The three parts are joined via MPEG-TS so
each part's H.264 parameter sets travel in-band (an MP4 holds only one set, the intro's).
"""
import argparse
import json
import logging
import subprocess
import sys
import tempfile
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/concat_intro_outro.log", encoding="utf-8")])
log = logging.getLogger(__name__)

REPO = Path(__file__).resolve().parent.parent
INTRO = REPO / "assets" / "asof" / "hoy_nazan_asof.mp4"
OUTRO = REPO / "assets" / "asof" / "OutroScene.mp4"
AUDIO = ["-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k"]
DURATION_TOLERANCE_S = 0.5


def run(cmd: list[str]) -> str:
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        log.error(f"{cmd[0]} failed ({res.returncode}): {' '.join(cmd)}\n{res.stderr[-3000:]}")
        raise RuntimeError(f"{cmd[0]} failed with exit code {res.returncode}")
    return res.stdout


def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                           "format=duration:stream=codec_type,codec_name,width,height,"
                           "avg_frame_rate,color_space,color_range",
                           "-of", "json", str(path)]))


def video_stream(info: dict, path: Path) -> dict:
    streams = [s for s in info["streams"] if s["codec_type"] == "video"]
    if len(streams) != 1:
        raise ValueError(f"{path}: expected one video stream, found {len(streams)}")
    return streams[0]


def encode_clip(clip: Path, out_ts: Path, v: dict) -> None:
    """Re-encode an intro/outro to the lecture's video format, as MPEG-TS."""
    color = []
    if v.get("color_space") not in (None, "unknown"):
        color += ["-colorspace", v["color_space"]]
    if v.get("color_range") not in (None, "unknown"):
        color += ["-color_range", v["color_range"]]
    # Fit inside the lecture frame and pad with white (the clips' background), so a 16:9 clip
    # on a 1920x1342 iPad recording keeps its shape instead of being stretched.
    w, h = v["width"], v["height"]
    fit = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
           f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=white")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(clip),
         "-vf", f"{fit},fps={v['avg_frame_rate']},setsar=1,format=yuv420p",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high", "-bf", "0",
         *color, *AUDIO, "-f", "mpegts", str(out_ts)])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("lecture", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()
    lecture: Path = args.lecture
    out: Path = args.output or lecture.with_name(f"{lecture.stem}_asof.mp4")
    if out.exists():
        raise FileExistsError(f"{out} already exists; pass another -o or move it first")

    t0 = time.time()
    info = probe(lecture)
    v = video_stream(info, lecture)
    if v["codec_name"] != "h264":
        raise ValueError(f"{lecture}: video is {v['codec_name']}, the copy path needs h264")
    log.info(f"Lecture {lecture.name}: {v['width']}x{v['height']} @ {v['avg_frame_rate']}, "
             f"{float(info['format']['duration']):.1f} s")
    expected = sum(float(probe(p)["format"]["duration"]) for p in (INTRO, lecture, OUTRO))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        encode_clip(INTRO, tmp / "intro.ts", v)
        encode_clip(OUTRO, tmp / "outro.ts", v)
        log.info(f"1/3 intro and outro re-encoded ({time.time() - t0:.0f} s elapsed)")

        run(["ffmpeg", "-v", "error", "-y", "-i", str(lecture), "-map", "0:v:0", "-map", "0:a:0",
             "-c:v", "copy", "-bsf:v", "h264_mp4toannexb", *AUDIO, "-f", "mpegts",
             str(tmp / "lecture.ts")])
        log.info(f"2/3 lecture video copied, audio re-encoded ({time.time() - t0:.0f} s elapsed)")

        (tmp / "list.txt").write_text("".join(f"file '{n}.ts'\n" for n in ("intro", "lecture", "outro")),
                                      encoding="utf-8")
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
             "-c", "copy", "-movflags", "+faststart", str(out)])
        log.info(f"3/3 joined ({time.time() - t0:.0f} s elapsed)")

    got = float(probe(out)["format"]["duration"])
    if abs(got - expected) > DURATION_TOLERANCE_S:
        raise RuntimeError(f"{out}: duration {got:.2f} s, expected {expected:.2f} s (intro + lecture + outro)")
    log.info(f"Wrote {out} ({out.stat().st_size:,} bytes, {got:.2f} s, expected {expected:.2f} s) "
             f"in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
