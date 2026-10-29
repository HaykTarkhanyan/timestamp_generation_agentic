"""Q37 (the user, 2026-10-28: groups A, B, C): delete 44 Vahagn uploads that the course no longer uses - A the 18
replaced 22.1-28.4 uploads, B the 25 raw caption uploads ("VidSection ..."), C the March "Դաս 21.2 | Todo".
Ids from _knowledge/vahagn_linalg/deletion_candidates_2026-10-28.json; metadata backed up first to
deleted_backup_2026-10-28.json (same folder; checked 2026-10-28: no description on the channel links any of them).
Before each delete: the video exists, is not public, is not in the course playlist and still has the recorded title;
any mismatch stops the run before anything is deleted. Read back after: videos.list returns none of them.
Dry run unless --apply. 50 units per delete (2,200) + ~5 to read; ~1 min.

    python scripts/archive/vahagn_2026-10/delete_replaced_uploads.py            # dry run
    python scripts/archive/vahagn_2026-10/delete_replaced_uploads.py --apply
"""
import json
import logging
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

K = REPO / "_knowledge/vahagn_linalg"
PLAYLIST = "PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM"
GROUPS = ("replaced", "raw", "old_21.2")

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("delete_replaced_uploads")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "delete_replaced_uploads.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

apply = "--apply" in sys.argv
t0 = time.time()
cand = json.loads((K / "deletion_candidates_2026-10-28.json").read_text(encoding="utf-8"))
rows = [r for g in GROUPS for r in cand[g]]
backup = json.loads((K / "deleted_backup_2026-10-28.json").read_text(encoding="utf-8"))
if len(rows) != 44 or len({r["id"] for r in rows}) != 44 or any(r["id"] not in backup for r in rows):
    raise SystemExit(f"expected 44 distinct ids, all in the backup; got {len(rows)}")

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
in_playlist = {it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PLAYLIST)}


def live(ids):
    got = {}
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute()["items"]:
            got[v["id"]] = v
    return got


now = live([r["id"] for r in rows])
problems = []
for r in rows:
    v = now.get(r["id"])
    if v is None:
        problems.append(f"{r['id']} not found")
    elif v["status"]["privacyStatus"] == "public":
        problems.append(f"{r['id']} is public")
    elif r["id"] in in_playlist:
        problems.append(f"{r['id']} is in the course playlist")
    elif v["snippet"]["title"] != r["title"]:
        problems.append(f"{r['id']} title changed: {v['snippet']['title']!r}")
if problems:
    for p in problems:
        log.error(p)
    raise SystemExit(f"{len(problems)} checks failed, nothing deleted")
for r in rows:
    log.info(f"{'DELETE' if apply else 'would delete'} {r['id']} {r['privacy']:8} {r['section']:7} {r['title'][:60]} (replaced by {r['replaced_by']})")
if not apply:
    log.info(f"dry run: {len(rows)} checked, all pass; rerun with --apply")
    raise SystemExit(0)

for i, r in enumerate(rows, 1):
    yt.videos().delete(id=r["id"]).execute()
    log.info(f"{i}/{len(rows)} deleted {r['id']} ({time.time() - t0:.0f} s)")
left = live([r["id"] for r in rows])
if left:
    raise SystemExit(f"read back: {len(left)} still returned: {sorted(left)}")
log.info(f"read back: none of the {len(rows)} is returned any more; {time.time() - t0:.0f} s, {50 * len(rows)} units")
