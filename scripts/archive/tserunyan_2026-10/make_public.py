"""Q25 (the user, 2026-10-27: "yes make public"): Tserunyan Դաս 15-27 unlisted -> public. videos.update(part=status)
with each video's own writable status fields sent back, only privacyStatus changed (playbook section 5). Backup of
the live status first; read back after: all public, every other field as before. Dry run unless --apply.
~1 unit to read, 50 per video changed (~650), ~20 s."""
import json
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST = "PLz3NrXxHz_CA3NjE0D_amd_QcTMx5HJvZ"
WRITABLE = ("embeddable", "license", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")
BACKUP = REPO / "_knowledge/tserunyan_metric/status_before_public_2026-10-27.json"

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
ids = {}
for n in range(15, 28):
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ids[n] = d.name.split("_", 2)[2]


def read():
    items = yt.videos().list(part="snippet,status", id=",".join(ids.values())).execute()["items"]
    got = {it["id"]: it for it in items}
    missing = [n for n, v in ids.items() if v not in got]
    if missing:
        raise RuntimeError(f"not returned by the API: Դաս {missing}")
    return got


live = read()
for n, vid in ids.items():
    st = live[vid]["status"]
    if "publishAt" in st:
        raise RuntimeError(f"Դաս {n} {vid}: has a scheduled publishAt {st['publishAt']}; not expected, stopping")
    print(f"Դաս {n} {vid} {st['privacyStatus']:8} madeForKids={st.get('madeForKids')} "
          f"embeddable={st.get('embeddable')} license={st.get('license')} | {live[vid]['snippet']['title'][:60]}")
pl = yt.playlists().list(part="status,contentDetails", id=PLAYLIST).execute()["items"][0]
print(f"playlist {PLAYLIST}: {pl['status']['privacyStatus']}, {pl['contentDetails']['itemCount']} items")
todo = [n for n, v in ids.items() if live[v]["status"]["privacyStatus"] != "public"]
print(f"{len(todo)} to make public, ~{50 * len(todo)} quota units")
if "--apply" not in sys.argv:
    print("dry run: nothing changed (add --apply)")
    sys.exit(0)

if not BACKUP.exists():
    BACKUP.write_text(json.dumps({str(n): {"id": v, "status": live[v]["status"]} for n, v in ids.items()},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"backup -> {BACKUP.relative_to(REPO)}")
t0 = time.time()
for i, n in enumerate(todo, 1):
    vid, st = ids[n], live[ids[n]]["status"]
    body = {k: st[k] for k in WRITABLE if k in st}
    body.setdefault("selfDeclaredMadeForKids", st["madeForKids"])
    body["privacyStatus"] = "public"
    yt.videos().update(part="status", body={"id": vid, "status": body}).execute()
    print(f"{time.strftime('%H:%M:%S')} {i}/{len(todo)} Դաս {n} {vid} -> public ({time.time() - t0:.0f} s)", flush=True)

time.sleep(5)  # reads can lag a few seconds
back = read()
bad = []
for n, vid in ids.items():
    before, after = live[vid]["status"], back[vid]["status"]
    if after["privacyStatus"] != "public":
        bad.append(f"Դաս {n}: {after['privacyStatus']}")
    changed = {k for k in set(before) | set(after) if k != "privacyStatus" and before.get(k) != after.get(k)}
    if changed:
        bad.append(f"Դաս {n}: also changed {sorted(changed)}: {[(k, before.get(k), after.get(k)) for k in changed]}")
if bad:
    raise RuntimeError("readback:\n" + "\n".join(bad))
print(f"read back: {len(ids)}/{len(ids)} public, no other status field changed ({time.time() - t0:.0f} s)")
