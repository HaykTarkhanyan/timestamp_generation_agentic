"""Read-only: the live title, description and duration of Tserunyan Դաս 1-14 from the playlist (umath token in
memory, 2-3 API units). Writes scratchpad/nest_1_14/live.json and one chapters_<N>.txt per video. ~3 s."""
import json
import re
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\scripts\.secrets\token_umath.json")
PLAYLIST = "PLz3NrXxHz_CA3NjE0D_amd_QcTMx5HJvZ"
OUT = Path(__file__).parent / "nest_1_14"
OUT.mkdir(exist_ok=True)

creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube.force-ssl"])
if not creds.valid:
    creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds)
ids, page = [], None
while True:
    resp = yt.playlistItems().list(part="contentDetails", playlistId=PLAYLIST, maxResults=50, pageToken=page).execute()
    ids += [it["contentDetails"]["videoId"] for it in resp["items"]]
    page = resp.get("nextPageToken")
    if not page:
        break
vids = yt.videos().list(part="snippet,contentDetails,status", id=",".join(ids)).execute()["items"]
live = []
for v in vids:
    m = re.match(r"Դաս (\d+)(?:-(\d+))?", v["snippet"]["title"])
    if not m or int(m.group(1)) > 14:
        continue
    live.append({"lesson": m.group(0).replace("Դաս ", ""), "id": v["id"], "title": v["snippet"]["title"],
                 "duration": v["contentDetails"]["duration"], "privacy": v["status"]["privacyStatus"],
                 "description": v["snippet"]["description"]})
live.sort(key=lambda x: int(x["lesson"].split("-")[0]))
(OUT / "live.json").write_text(json.dumps(live, ensure_ascii=False, indent=1), encoding="utf-8")
for x in live:
    chap = [l for l in x["description"].splitlines() if re.match(r"^\s*\d{1,2}:\d\d(:\d\d)?\s", l)]
    (OUT / f"chapters_{x['lesson']}.txt").write_text("\n".join(chap) + "\n", encoding="utf-8")
    print(f"Դաս {x['lesson']} {x['id']} {x['duration']} {x['privacy']}: {len(chap)} chapter lines, "
          f"{sum(1 for l in chap if l[:1].isspace())} indented")
