"""Dump the info theory playlist (title, privacy, description) as JSON. Read-only, ~3 quota units."""
import json
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
PL = "PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy"
items = yt_publish._playlist_items(yt, PL)
ids = [it["contentDetails"]["videoId"] for it in items]
extra = sys.argv[1:]
ids += [i for i in extra if i not in ids]
out = []
for i in range(0, len(ids), 50):
    r = yt.videos().list(part="snippet,status,contentDetails", id=",".join(ids[i:i + 50])).execute()
    for v in r["items"]:
        out.append({"id": v["id"], "title": v["snippet"]["title"], "privacy": v["status"]["privacyStatus"],
                    "duration": v["contentDetails"]["duration"], "description": v["snippet"]["description"]})
dest = Path(__file__).with_name("info_playlist_dump.json")
dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for v in out:
    print(v["id"], v["privacy"], v["duration"], v["title"])
print("->", dest)
