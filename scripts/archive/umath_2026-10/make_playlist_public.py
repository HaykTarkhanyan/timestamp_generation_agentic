"""The user, 2026-10-28 (Q41): make the unlisted playlist "Մաթեմատիկական անալիզ 4" (PLz3NrXxHz_CD1urZ5q3bgm_YNWuT2osgS)
public so end screens can link it. playlists.update(part=snippet,status) changing only privacyStatus; the playlist's snippet and
status are backed up first and read back after. Dry run unless --apply. ~2 units to read, 50 to update, ~5 s.

    python scripts/archive/umath_2026-10/make_playlist_public.py [--apply]
"""
import json
import logging
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST = "PLz3NrXxHz_CD1urZ5q3bgm_YNWuT2osgS"
BACKUP = REPO / "output/endscreens/playlist_ma4_before_public_2026-10-28.json"

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_playlist_public")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_playlist_public.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()


def read():
    items = yt.playlists().list(part="snippet,status,contentDetails", id=PLAYLIST).execute()["items"]
    if len(items) != 1:
        raise SystemExit(f"playlist {PLAYLIST} not returned")
    return items[0]


before = read()
log.info(f"{before['snippet']['title']}: {before['status']['privacyStatus']}, {before['contentDetails']['itemCount']} items, "
         f"channel {before['snippet']['channelId']}")
if before["snippet"]["channelId"] != yt_publish.CHANNEL_IDS["umath"]:
    raise SystemExit("not a umath playlist")
if before["status"]["privacyStatus"] == "public":
    log.info("already public, nothing to do")
    sys.exit(0)
if "--apply" not in sys.argv:
    log.info("dry run: nothing changed (add --apply)")
    sys.exit(0)
BACKUP.write_text(json.dumps(before, ensure_ascii=False, indent=1), encoding="utf-8")
# part=status alone is refused ("unexpectedPart"): send the snippet's own writable fields back unchanged
snippet = {k: before["snippet"][k] for k in ("title", "description", "defaultLanguage", "tags") if k in before["snippet"]}
yt.playlists().update(part="snippet,status", body={"id": PLAYLIST, "snippet": snippet,
                                                   "status": {"privacyStatus": "public"}}).execute()
time.sleep(8)  # 2026-10-28: a read 1 s after the update still said "unlisted"; 13 s later it was public
after = read()
if after["status"]["privacyStatus"] != "public":
    raise SystemExit(f"read back: {after['status']['privacyStatus']}")
changed = {k for k in ("title", "description") if before["snippet"].get(k) != after["snippet"].get(k)}
if changed:
    raise SystemExit(f"read back: snippet fields changed too: {changed}")
log.info(f"read back: public, title and description unchanged; backup {BACKUP.relative_to(REPO)}")
