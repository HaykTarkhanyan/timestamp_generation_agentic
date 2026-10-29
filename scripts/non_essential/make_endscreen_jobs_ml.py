"""End-screen job files for Metric Academy's "Մեքենայական ուսուցում" (ML course) playlist: one
.playwright-mcp/endscreen_ml_NN_<id>.js per video from endscreen_template.js (next to this file): the next lesson,
this playlist and Subscribe, last 10 s.
Run: python scripts/non_essential/make_endscreen_jobs_ml.py   (~15 s, reads the playlist through the API, read-only)
Then each file with browser_run_code_unsafe(filename=...), one at a time, Studio signed in as Metric Academy.

The playlist is newest first, so "next" goes by the "[NN]" lesson number, not by position: [N] -> [N+1]. Videos without
a number (the Claude Code workshop, the Q&A) and the newest lesson get "Best for viewer" (the user's call, 2026-10-27).
When a new lesson is uploaded, the previous newest one should be pointed at it.
"""
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST_ID = "PLfLD2TpGxVUw03fbI6FG6LWUp_m62pqkx"
PLAYLIST = "Մեքենայական ուսուցում"
LESSON = re.compile(r"^\[(\d+)\] ")

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_jobs_ml")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_jobs_ml.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

items = [(it["contentDetails"]["videoId"], it["snippet"]["title"])
         for it in yt_publish._playlist_items(yt_publish.get_service(), PLAYLIST_ID)]
by_lesson = {}
for vid, t in items:
    m = LESSON.match(t)
    if m:
        n = int(m[1])
        if n in by_lesson:
            raise ValueError(f"Lesson [{n:02d}] twice in the playlist: {by_lesson[n][1]!r} and {t!r}")
        by_lesson[n] = (vid, t)
gaps = sorted(set(range(1, max(by_lesson) + 1)) - set(by_lesson))
if gaps:
    raise ValueError(f"Lesson numbers missing from the playlist: {gaps}")
tpl = (Path(__file__).parent / "endscreen_template.js").read_text(encoding="utf-8")
for pos, (vid, t) in enumerate(items):
    m = LESSON.match(t)
    nxt = by_lesson.get(int(m[1]) + 1) if m else None
    job = {"id": vid, "lesson": f"{pos:02d} {t[:40]}", "playlist": PLAYLIST, "channel": yt_publish.CHANNEL_IDS["metric"],
           "next": {"prefix": nxt[1], "query": nxt[1]} if nxt else None}
    out = REPO / ".playwright-mcp" / f"endscreen_ml_{pos:02d}_{vid}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    log.info(f"{out.name}: {t[:40]} -> {nxt[1][:40] if nxt else 'Best for viewer'}")
log.info(f"{len(items)} job files written, lessons [01]-[{max(by_lesson):02d}]")
