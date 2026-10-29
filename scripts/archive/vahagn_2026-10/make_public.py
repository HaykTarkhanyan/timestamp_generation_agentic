"""The user, 2026-10-28: "pls also set vahagn course public". The unlisted videos of Գծային հանրահաշիվ (expected: the
25 sections 21.1-28.4) -> public, videos.update(part=status) with each video's own writable status fields sent back,
only privacyStatus changed (the Tserunyan pattern, scripts/archive/tserunyan_2026-10/make_public.py). Status backup
first; read back after: all public, every other status field as before. Dry run unless --apply.
~3 units to read, 50 per video changed (~1,250), ~40 s.

    python scripts/archive/vahagn_2026-10/make_public.py            # dry run
    python scripts/archive/vahagn_2026-10/make_public.py --apply
"""
import json
import logging
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST = "PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM"
WRITABLE = ("embeddable", "license", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")
BACKUP = REPO / "_knowledge/vahagn_linalg/status_before_public_2026-10-28.json"

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("vahagn_make_public")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "vahagn_make_public.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
pl_ids = [it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PLAYLIST)]


def read(ids):
    got = {}
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k + 50])).execute()["items"]:
            got[v["id"]] = v
    missing = [i for i in ids if i not in got]
    if missing:
        raise RuntimeError(f"not returned by the API: {missing}")
    return got


live = read(pl_ids)
todo = [i for i in pl_ids if live[i]["status"]["privacyStatus"] != "public"]
sections = [re.match(r"^Դաս (\d+)\.", live[i]["snippet"]["title"]) for i in todo]
if len(todo) != 25 or any(not m or not 21 <= int(m[1]) <= 28 for m in sections):
    raise SystemExit(f"expected the 25 unlisted sections 21.1-28.4, found {len(todo)}: "
                     f"{[live[i]['snippet']['title'][:20] for i in todo]}")
for i in todo:
    st = live[i]["status"]
    if "publishAt" in st or st["privacyStatus"] != "unlisted":
        raise SystemExit(f"{i}: status {st}; expected plain unlisted, stopping")
    log.info(f"{i} {st['privacyStatus']:8} madeForKids={st.get('madeForKids')} embeddable={st.get('embeddable')} "
             f"license={st.get('license')} | {live[i]['snippet']['title'][:60]}")
pl = yt.playlists().list(part="status,contentDetails", id=PLAYLIST).execute()["items"][0]
log.info(f"playlist {PLAYLIST}: {pl['status']['privacyStatus']}, {pl['contentDetails']['itemCount']} items; "
         f"{len(todo)} to make public, ~{50 * len(todo)} units")
if "--apply" not in sys.argv:
    log.info("dry run: nothing changed (add --apply)")
    sys.exit(0)

BACKUP.write_text(json.dumps({i: {"title": live[i]["snippet"]["title"], "status": live[i]["status"]} for i in todo},
                             ensure_ascii=False, indent=1), encoding="utf-8")
log.info(f"backup -> {BACKUP.relative_to(REPO)}")
t0 = time.time()
for n, i in enumerate(todo, 1):
    st = live[i]["status"]
    body = {k: st[k] for k in WRITABLE if k in st}
    body.setdefault("selfDeclaredMadeForKids", st["madeForKids"])
    body["privacyStatus"] = "public"
    yt.videos().update(part="status", body={"id": i, "status": body}).execute()
    log.info(f"{n}/{len(todo)} {i} -> public ({time.time() - t0:.0f} s)")

time.sleep(5)  # reads can lag a few seconds
back = read(todo)
bad = []
for i in todo:
    before, after = live[i]["status"], back[i]["status"]
    if after["privacyStatus"] != "public":
        bad.append(f"{i}: {after['privacyStatus']}")
    changed = {k for k in set(before) | set(after) if k != "privacyStatus" and before.get(k) != after.get(k)}
    if changed:
        bad.append(f"{i}: also changed {sorted(changed)}: {[(k, before.get(k), after.get(k)) for k in changed]}")
if bad:
    raise RuntimeError("readback:\n" + "\n".join(bad))
log.info(f"read back: {len(todo)}/{len(todo)} public, no other status field changed ({time.time() - t0:.0f} s)")
