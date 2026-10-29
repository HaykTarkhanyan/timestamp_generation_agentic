"""Read-only snapshot of every video's title and description on our YouTube channels, before a channel-wide
description change (the user, 2026-10-26: "fetch and save all, i mean all all", ahead of nesting the chapters of
every video description). Per channel (metric, umath, brainstorm, one token each): every upload in any visibility
(public, unlisted, private), with snippet (title, description, tags, publishedAt, ...), contentDetails (duration)
and status.

Writes snapshots/channels_<date>/<channel>.json and summary.json (per channel: videos by visibility, how many
descriptions carry chapters, how many are nested already, their time format). snapshots/ is git-ignored: it holds
private and unlisted videos and this repo is public. Read-only, 1 API unit per 50 videos (~30 units for all three
channels). Runtime ~1 min. From the repo root:

    python scripts/non_essential/snapshot_channels.py [--channels metric umath brainstorm]
"""
import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "snapshot_channels.log", encoding="utf-8")])
log = logging.getLogger("snapshot_channels")
CHAPTER = re.compile(r"^(\s*)(\d{1,2}:\d\d(?::\d\d)?)\s+\S")


def chapter_stats(desc: str) -> dict:
    lines = [m for m in map(CHAPTER.match, desc.splitlines()) if m]
    if len(lines) < 3 or lines[0].group(2) not in ("0:00", "00:00", "0:00:00", "00:00:00"):
        return {"chapters": 0}
    times = [m.group(2) for m in lines]
    fmt = ("H:MM:SS" if all(re.fullmatch(r"\d:\d\d:\d\d", t) for t in times)
           else "MM:SS" if all(re.fullmatch(r"\d\d:\d\d", t) for t in times)
           else "mixed")
    return {"chapters": len(lines), "nested": sum(1 for m in lines if m.group(1)), "format": fmt}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channels", nargs="+", default=["metric", "umath", "brainstorm"])
    args = ap.parse_args()
    t0 = time.time()
    out = REPO / "snapshots" / f"channels_{time.strftime('%Y-%m-%d')}"
    out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for ch in args.channels:
        yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES[ch]
        yt = yt_publish.get_service()
        me = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
        if me["id"] != yt_publish.CHANNEL_IDS[ch]:
            raise RuntimeError(f"{ch}: token belongs to {me['id']}, expected {yt_publish.CHANNEL_IDS[ch]}")
        ids, tok = [], None
        while True:
            r = yt.playlistItems().list(part="contentDetails", playlistId=me["contentDetails"]["relatedPlaylists"]["uploads"],
                                        maxResults=50, pageToken=tok).execute()
            ids += [i["contentDetails"]["videoId"] for i in r["items"]]
            tok = r.get("nextPageToken")
            if not tok:
                break
        ids = list(dict.fromkeys(ids))
        videos = []
        for k in range(0, len(ids), 50):
            videos += yt.videos().list(part="snippet,contentDetails,status", id=",".join(ids[k:k + 50])).execute()["items"]
            log.info(f"{ch}: {len(videos)}/{len(ids)} videos, {time.time() - t0:.0f}s elapsed")
        missing = set(ids) - {v["id"] for v in videos}
        if missing:
            raise RuntimeError(f"{ch}: {len(missing)} uploads not returned by videos.list: {sorted(missing)[:5]}")
        (out / f"{ch}.json").write_text(json.dumps({"fetched": time.strftime("%Y-%m-%d %H:%M"), "channel_id": me["id"],
                                                    "channel_title": me["snippet"]["title"], "videos": videos},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
        stats = [chapter_stats(v["snippet"]["description"]) for v in videos]
        privacy = {}
        for v in videos:
            privacy[v["status"]["privacyStatus"]] = privacy.get(v["status"]["privacyStatus"], 0) + 1
        with_ch = [s for s in stats if s["chapters"]]
        summary[ch] = {
            "channel": me["snippet"]["title"], "videos": len(videos), "by_visibility": privacy,
            "with_chapters": len(with_ch), "nested_already": sum(1 for s in with_ch if s["nested"]),
            "chapter_lines": sum(s["chapters"] for s in with_ch),
            "time_format": {f: sum(1 for s in with_ch if s["format"] == f) for f in ("MM:SS", "H:MM:SS", "mixed")},
        }
        log.info(f"{ch}: {summary[ch]}")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info(f"wrote {out} in {time.time() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
