"""End-screen job files for Metric Academy's "Մաթեմատիկա մեքենայական ուսուցման (ML-ի) համար" playlist: one
.playwright-mcp/endscreen_m4ml_NN_<id>.js per video from endscreen_template.js (next to this file): the next video in
course order, this playlist and Subscribe, last 10 s.
Run: python scripts/non_essential/make_endscreen_jobs_math4ml.py   (~15 s, reads the playlist through the API, read-only)
Then the files, best bundled with make_endscreen_batch.py, Studio signed in as Metric Academy.

Course order (the user's call, 2026-10-27): lectures ("Դաս N |") and practicals ("| Գործնական K |") as they were
published, oldest first, except that the lectures keep their number order (Դաս 31 went up a few minutes before Դաս 30).
So Դաս 0 -> Գործնական 1 -> Դաս 1 -> Դաս 2 -> Գործնական 2 ... The last video gets "Best for viewer". The playlist itself
stays newest first (also the user's call), so its end-screen link opens at the newest lecture.
"""
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST_ID = "PLfLD2TpGxVUxc1HLKBVe7KOS4CjU29pgR"
PLAYLIST = "Մաթեմատիկա մեքենայական ուսուցման (ML-ի) համար"
LECTURE = re.compile(r"^Դաս (\d+) \|")
PRACTICAL = re.compile(r"\| Գործնական (\d+) \|")
# End screens made before 2026-10-27 with "Best for viewer" (output/endscreens/math4ml_verify.json, group C): the user
# asked to point them at the next video too (Q13). Edit jobs from endscreen_edit_template.js
EDIT_BEST_FOR_VIEWER = {"-WEnJsl3esQ", "ZKdCO6o3i4E", "7bl1k6TZ9_Q", "UjGD31i8Ji4", "H8M6p-uSxCM", "JsSnSHZtG_o",
                        "mGOCt9ZcWJg", "W9ZncUE8Fno", "4exAPAxCXCw", "hF2jwMKdmE0", "G1RDesi8a2w", "uSv-d8tIwFg",
                        "tWIwahIeI_8", "twHQTcN_48E", "8fkODa_yEEM", "D9JIZXNzios", "xnT7eaba_UM", "ulNS3QVenYo",
                        "lAKPMjqQ6vc", "Ye0ZsTDnPx4", "fxYxoHIz-P0", "DDdzHnQsyrA", "xQKwAcaM410", "PNVE4gy1jt0",
                        "Z1LNPERo87g", "PYHNsndAnXE"}
# Group B: Գործնական 6, 7, 8 pointed back at Դաս 9 (a copy-paste slip, Q14): edit jobs that replace that video
DASS_9 = "Դաս 9 | Ածանցյալի կիրառություններ, ֆունկցիայի էքստրեմումի կետեր | Մաթեմատիկա ML-ի համար"
EDIT_FROM = {"d5bAQnILhvs": DASS_9, "FRjc1KiAbaw": DASS_9, "XFF03oPjAyE": DASS_9}
# Group A: Դաս 0-6 and Գործնական 4 had Subscribe + 2 videos, no playlist; the user asked to rebuild them to the standard
# (Q15): jobs from endscreen_template.js with "rebuild", which deletes exactly those 3 elements and adds the standard ones
REBUILD = {"7rIw7ocwMP4", "-VPo9D_E6FQ", "kh10WTvYTR0", "AjPnQIe-BSo", "CWfStEWc6VQ", "iV7d5DGmA-0", "6EoJWTOSKkQ",
           "I4EMKTQbVno"}
REBUILD_KINDS = ["Subscribe", "Video", "Video"]

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_jobs_math4ml")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_jobs_math4ml.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

items = yt_publish._playlist_items(yt_publish.get_service(), PLAYLIST_ID)
pos = {it["contentDetails"]["videoId"]: i for i, it in enumerate(items)}
videos = sorted(({"id": it["contentDetails"]["videoId"], "title": it["snippet"]["title"],
                  "published": it["contentDetails"]["videoPublishedAt"]} for it in items), key=lambda v: v["published"])
for v in videos:
    lec, pr = LECTURE.match(v["title"]), PRACTICAL.search(v["title"])
    if bool(lec) == bool(pr):
        raise ValueError(f"Neither or both of lecture / practical: {v['title']!r}")
    v["lecture"], v["practical"] = (int(lec[1]) if lec else None), (int(pr[1]) if pr else None)
for kind, first in (("lecture", 0), ("practical", 1)):
    nums = sorted(v[kind] for v in videos if v[kind] is not None)
    if nums != list(range(first, first + len(nums))):
        raise ValueError(f"{kind} numbers are not {first}..{first + len(nums) - 1} without gaps or repeats: {nums}")
# lectures back into number order inside the lecture slots of the publish order
slots = [i for i, v in enumerate(videos) if v["lecture"] is not None]
for i, v in zip(slots, sorted((videos[i] for i in slots), key=lambda v: v["lecture"])):
    videos[i] = v
tpl = (Path(__file__).parent / "endscreen_template.js").read_text(encoding="utf-8")
edit_tpl = (Path(__file__).parent / "endscreen_edit_template.js").read_text(encoding="utf-8")
for k, v in enumerate(videos):
    nxt = videos[k + 1] if k + 1 < len(videos) else None
    job = {"id": v["id"], "lesson": f"{k:02d} {v['title'][:40]}", "playlist": PLAYLIST, "channel": yt_publish.CHANNEL_IDS["metric"],
           "next": {"prefix": nxt["title"], "query": nxt["title"]} if nxt else None}
    out = REPO / ".playwright-mcp" / f"endscreen_m4ml_{k:02d}_{v['id']}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    log.info(f"{out.name} (playlist pos {pos[v['id']]}): {v['title'][:35]} -> {nxt['title'][:35] if nxt else 'Best for viewer'}")
    if v["id"] in REBUILD:
        out = REPO / ".playwright-mcp" / f"endscreen_m4mlrebuild_{k:02d}_{v['id']}.js"
        out.write_text(tpl.replace("__JOB__", json.dumps(job | {"rebuild": REBUILD_KINDS}, ensure_ascii=False)), encoding="utf-8")
    if v["id"] in EDIT_BEST_FOR_VIEWER | set(EDIT_FROM):
        if not nxt:
            raise ValueError(f"{v['title']!r} is the last video, it has no next one to point at")
        out = REPO / ".playwright-mcp" / f"endscreen_m4mledit_{k:02d}_{v['id']}.js"
        edit_job = {kk: job[kk] for kk in ("id", "lesson", "channel", "next")}
        if v["id"] in EDIT_FROM:
            edit_job["from"] = EDIT_FROM[v["id"]]
        out.write_text(edit_tpl.replace("__JOB__", json.dumps(edit_job, ensure_ascii=False)), encoding="utf-8")
missing = (EDIT_BEST_FOR_VIEWER | set(EDIT_FROM) | REBUILD) - {v["id"] for v in videos}
if missing:
    raise ValueError(f"Not in the playlist any more, fix EDIT_BEST_FOR_VIEWER / EDIT_FROM / REBUILD: {sorted(missing)}")
log.info(f"{len(videos)} job files written, course order; {len(EDIT_BEST_FOR_VIEWER) + len(EDIT_FROM)} edit jobs, "
         f"{len(REBUILD)} rebuild jobs")
