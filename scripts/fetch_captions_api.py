"""Fetch a video's auto-captions through the YouTube Data API, for videos yt-dlp can't read.

fetch_subtitles.py goes through yt-dlp, which only sees public and unlisted videos. A private
upload (the Ուղեղամպրոպ channel uploads private) fails there with "Private video". This script
asks the API as the channel owner instead, with yt_publish.py's token for that channel, and
writes the same output folder fetch_subtitles.py does:

    <video-id>.<lang>.vtt   the API's auto-caption track (same <c> word timing as yt-dlp's)
    transcript.txt          cleaned by fetch_subtitles.parse_vtt
    metadata.json           id, title, duration, uploader, url, plus fps from the uploaded
                            file, which find_edit_points.py would otherwise ask yt-dlp for
    logs/fetch_captions_api.log

Quota: videos.list 1 + captions.list 50 + captions.download 200 units. Runtime: ~10 s.

Usage:
    python scripts/fetch_captions_api.py --channel brainstorm <VIDEO_ID> [--lang hy] [--output-dir DIR]
"""
import argparse
import json
import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parent / ".claude" / "skills" / "youtube-timestamps" / "scripts"))
import yt_publish  # noqa: E402
from fetch_subtitles import LOG_FORMAT, parse_vtt, slugify  # noqa: E402

log = logging.getLogger("fetch_captions_api")


def iso_seconds(duration: str) -> int:
    """'PT1H11M55S' -> 4315."""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not m:
        raise ValueError(f"Unexpected ISO 8601 duration: {duration!r}")
    h, mi, s = (int(g or 0) for g in m.groups())
    return h * 3600 + mi * 60 + s


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video_id")
    ap.add_argument("--channel", required=True, choices=sorted(yt_publish.TOKEN_FILES),
                    help="whose token to use: the channel that owns the video")
    ap.add_argument("--lang", default="hy")
    ap.add_argument("--output-base", default="output")
    ap.add_argument("--output-dir", type=Path, help="exact output dir instead of '<date>_<slug>_<id>'")
    ap.add_argument("--fps", type=float,
                    help="frame rate of the uploaded file, when fileDetails has none (Vahagn 21.2, uploaded by "
                         "someone else in March 2026: no frameRateFps); take it from the local file")
    args = ap.parse_args()

    t0 = time.time()
    log.setLevel(logging.INFO)
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    log.addHandler(console)

    yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES[args.channel]
    yt = yt_publish.get_service()

    items = yt.videos().list(part="snippet,contentDetails,fileDetails", id=args.video_id).execute()["items"]
    if not items:
        raise ValueError(f"{args.video_id}: no such video visible to the {args.channel} token")
    video = items[0]
    streams = video.get("fileDetails", {}).get("videoStreams", [])
    if streams and "frameRateFps" in streams[0]:
        fps = streams[0]["frameRateFps"]
    elif args.fps:
        fps = args.fps
        log.info(f"No frame rate in fileDetails; using --fps {fps}")
    else:
        raise ValueError(f"{args.video_id}: no frame rate in fileDetails (only the owner's token gets it); "
                         "pass --fps from the local file")
    metadata = {
        "id": video["id"],
        "title": video["snippet"]["title"],
        "duration": iso_seconds(video["contentDetails"]["duration"]),
        "url": f"https://youtu.be/{video['id']}",
        "uploader": video["snippet"]["channelTitle"],
        "fps": fps,
    }
    log.info(f"Title: {metadata['title']}, {metadata['duration']} s, {metadata['fps']} fps")

    out_dir = args.output_dir or Path(args.output_base) / (
        f"{datetime.now():%Y-%m-%d}_{slugify(metadata['title'])}_{metadata['id']}")
    (out_dir / "logs").mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(out_dir / "logs" / "fetch_captions_api.log", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    log.addHandler(file_handler)
    log.info(f"Output dir: {out_dir}")
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    tracks = yt.captions().list(part="snippet", videoId=args.video_id).execute().get("items", [])
    asr = [t for t in tracks if t["snippet"]["trackKind"] == "asr" and t["snippet"]["language"] == args.lang]
    if not asr:
        found = [(t["snippet"]["language"], t["snippet"]["trackKind"]) for t in tracks]
        raise RuntimeError(f"No {args.lang!r} auto-caption track yet (tracks: {found}). "
                           "YouTube can take a while after upload; try again later.")
    data = yt.captions().download(id=asr[0]["id"], tfmt="vtt").execute()
    vtt_path = out_dir / f"{metadata['id']}.{args.lang}.vtt"
    vtt_path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))

    transcript = parse_vtt(vtt_path)
    (out_dir / "transcript.txt").write_text(transcript, encoding="utf-8")
    log.info(f"Transcript: {transcript.count(chr(10))} lines. Done in {time.time() - t0:.0f} s")
    print(json.dumps({"output_dir": str(out_dir), "duration_seconds": metadata["duration"],
                      "fps": metadata["fps"], "title": metadata["title"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log.error(f"Failed: {exc}", exc_info=True)
        sys.exit(1)
