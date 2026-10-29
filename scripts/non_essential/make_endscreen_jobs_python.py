"""End-screen job files for Metric Academy's "Python - Դասեր" playlist: one .playwright-mcp/endscreen_py_NN_<id>.js
per video from endscreen_template.js (next to this file): the next video, this playlist and Subscribe, last 10 s.
Run: python scripts/non_essential/make_endscreen_jobs_python.py   (~15 s, reads the playlist through the API, read-only)
Then each file with browser_run_code_unsafe(filename=...), one at a time, Studio signed in as Metric Academy.

Next video: the next one in the playlist, skipping two extras that sit inside the chain (the user's call, 2026-10-27):
the [2023] homework discussion and the [1.5] dotenv short. The [2023] one links on to the video after it; dotenv links
to Libraries [02] NumPy, since 1.5 sits between 1 and 2. The last video gets "Best for viewer". The video element finds
its target by the full title, because "[05]"-style prefixes repeat across the course, Libraries and the 2023 videos.
"""
import json
import logging
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST_ID = "PLfLD2TpGxVUwNhdJWh3lpAJLFBjV6ilqv"
PLAYLIST = "Python - Դասեր"
# from Libraries [01] on, the playlist element is the Libraries playlist, as on the end screens made before 2026-10-27
LIB_PLAYLIST, LIB_FROM = "Python Libraries / Փայթըն գրադարաններ", "ZOOWqchxETU"
SKIP = {"6Aktg75ZquA", "tqR3DhSkNlQ"}          # [2023] [05] homework discussion, [1.5] Python-dotenv
NEXT_OVERRIDE = {"tqR3DhSkNlQ": "7XsIyFTImwk"}  # dotenv -> [02] NumPy | Libraries
# Libraries end screens made before 2026-10-27 whose video element is "Best for viewer" (output/endscreens/
# python_daser_survey.json): the user asked to point them at the next video too. Edit jobs from endscreen_edit_template.js
EDIT_BEST_FOR_VIEWER = {"3JJDA0xXvSE", "r44t7RPPm7U", "tqR3DhSkNlQ", "2BtFmBMSnsA", "qcLhrouK7yE", "zMeKyFWTe10",
                        "_19jYMHAv-8", "JRyqUIrG6As", "mzEPZxtrLs0"}

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_jobs_python")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_jobs_python.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

items = [(it["contentDetails"]["videoId"], it["snippet"]["title"])
         for it in yt_publish._playlist_items(yt_publish.get_service(), PLAYLIST_ID)]
ids = [v for v, _ in items]
missing = ({LIB_FROM} | SKIP | EDIT_BEST_FOR_VIEWER | set(NEXT_OVERRIDE) | set(NEXT_OVERRIDE.values())) - set(ids)
if missing:
    raise ValueError(f"Not in the playlist any more, fix SKIP / NEXT_OVERRIDE / EDIT_BEST_FOR_VIEWER: {sorted(missing)}")
title = dict(items)
tpl = (Path(__file__).parent / "endscreen_template.js").read_text(encoding="utf-8")
edit_tpl = (Path(__file__).parent / "endscreen_edit_template.js").read_text(encoding="utf-8")
for pos, (vid, t) in enumerate(items):
    nxt = NEXT_OVERRIDE.get(vid) or next((v for v in ids[pos + 1:] if v not in SKIP), None)
    pl = LIB_PLAYLIST if pos >= ids.index(LIB_FROM) else PLAYLIST
    job = {"id": vid, "lesson": f"{pos:02d} {t[:40]}", "playlist": pl, "channel": yt_publish.CHANNEL_IDS["metric"],
           "next": {"prefix": title[nxt], "query": title[nxt]} if nxt else None}
    out = REPO / ".playwright-mcp" / f"endscreen_py_{pos:02d}_{vid}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    log.info(f"{out.name}: {t[:45]} -> {title[nxt][:45] if nxt else 'Best for viewer'}")
    if vid in EDIT_BEST_FOR_VIEWER:
        out = REPO / ".playwright-mcp" / f"endscreen_pyedit_{pos:02d}_{vid}.js"
        edit_job = {k: job[k] for k in ("id", "lesson", "channel", "next")}
        out.write_text(edit_tpl.replace("__JOB__", json.dumps(edit_job, ensure_ascii=False)), encoding="utf-8")
        log.info(f"  edit job {out.name}: Best for viewer -> {title[nxt][:45]}")
log.info(f"{len(items)} job files written, {len(EDIT_BEST_FOR_VIEWER)} edit jobs")
