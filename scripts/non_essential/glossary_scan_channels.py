"""Run the glossary check (.claude/skills/youtube-timestamps/scripts/glossary_check.py) over everything published:
the title and description of every upload on the given channels, plus the umath channel's chapter comments
on other channels' videos (ids from _knowledge/sevak_linalg_honors/README.md). Read-only API calls.

    python scripts/non_essential/glossary_scan_channels.py [--channels umath metric] [--out output/glossary_scan]

Writes <out>/scan.json first (every finding with channel, video id, title, line), then prints a summary.
Runtime: ~100 s for both channels (664 videos and comments; measured 2026-10-22).
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
sys.path.insert(0, str(REPO / ".claude/skills/youtube-timestamps/scripts"))
import yt_publish  # noqa: E402
from glossary_check import check_text  # noqa: E402

(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "glossary_scan_channels.log", encoding="utf-8")])
log = logging.getLogger("glossary_scan_channels")


def uploads(yt):
    me = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    pl, ids, tok = me["contentDetails"]["relatedPlaylists"]["uploads"], [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            return me["id"], list(dict.fromkeys(ids))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--channels", nargs="+", default=["umath", "metric"])
    ap.add_argument("--out", type=Path, default=REPO / "output" / "glossary_scan")
    args = ap.parse_args()
    t0, findings, scanned = time.time(), [], 0
    for ch in args.channels:
        yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES[ch]
        yt = yt_publish.get_service()
        _, ids = uploads(yt)
        for k in range(0, len(ids), 50):
            for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute()["items"]:
                sn = v["snippet"]
                scanned += 1
                for i, kind, found, sugg, line in check_text(sn["title"] + "\n" + sn["description"]):
                    findings.append({"channel": ch, "where": "title" if i == 1 else "description", "id": v["id"],
                                     "privacy": v["status"]["privacyStatus"], "title": sn["title"],
                                     "kind": kind, "found": found, "suggestion": sugg, "line": line})
            log.info(f"{ch}: {min(k + 50, len(ids))}/{len(ids)} videos, {time.time() - t0:.0f}s elapsed")
        if ch == "umath":
            readme = (REPO / "_knowledge/sevak_linalg_honors/README.md").read_text(encoding="utf-8")
            cids = sorted(set(re.findall(r"Ug[\w-]{20,}", readme)))
            for c in yt.comments().list(part="snippet", id=",".join(cids), textFormat="plainText").execute()["items"]:
                scanned += 1
                for i, kind, found, sugg, line in check_text(c["snippet"]["textDisplay"]):
                    findings.append({"channel": ch, "where": "comment", "id": c["id"], "privacy": "public",
                                     "title": c["snippet"].get("videoId", ""), "kind": kind, "found": found,
                                     "suggestion": sugg, "line": line})
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "scan.json").write_text(json.dumps(findings, ensure_ascii=False, indent=1), encoding="utf-8")
    counts = {k: sum(f["kind"] == k for f in findings) for k in ("DENY", "NEAR", "ENG")}
    log.info(f"{scanned} items scanned in {time.time() - t0:.0f}s: {counts}; wrote {args.out / 'scan.json'}")
    return 1 if counts["DENY"] else 0


if __name__ == "__main__":
    sys.exit(main())
