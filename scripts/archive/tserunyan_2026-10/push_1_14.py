"""Push the nested H:MM:SS descriptions of Tserunyan Դաս 1-14 (the user's Q75 "Push all 12"): yt_publish.py
set-description per video, then read back through the API (description == our file) and as a viewer (yt-dlp:
chapters YouTube parsed == our chapter lines). Stops at the first failure. Description only; title, thumbnail and
visibility untouched. ~8 s per video, ~1.5 min. Repo root."""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
SRC = Path(__file__).parent / "nest_1_14"
TOKEN = REPO / "scripts" / ".secrets" / "token_umath.json"
live = json.loads((SRC / "live.json").read_text(encoding="utf-8"))
t_all = time.time()
for v in live:
    t0 = time.time()
    n, vid = v["lesson"], v["id"]
    f = SRC / f"desc_{n}.txt"
    r = subprocess.run([sys.executable, "scripts/yt_publish.py", "--channel", "umath", "set-description", vid, str(f)],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"Դաս {n}: set-description failed\n{(r.stdout + r.stderr)[-1200:]}")
    creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube.force-ssl"])
    if not creds.valid:
        creds.refresh(Request())
    yt = build("youtube", "v3", credentials=creds)
    want = f.read_text(encoding="utf-8").strip("\n")
    # a read right after the write can still serve the old text (Դաս 1-2, 2026-10-26: differed at once, identical
    # a minute later), so retry for ~20 s before calling it a mismatch
    for attempt in range(8):
        got = yt.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]
        if got["description"].strip("\n") == want:
            break
        time.sleep(3)
    else:
        raise RuntimeError(f"Դաս {n}: readback still differs from {f} after ~24 s")
    ours = [l for l in want.splitlines() if re.match(r"^\s*\d+:\d\d:\d\d ", l)]
    y = subprocess.run(["yt-dlp", "-J", "--skip-download", f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, encoding="utf-8")
    if y.returncode:
        raise RuntimeError(f"Դաս {n}: yt-dlp failed\n{y.stderr[-600:]}")
    chaps = json.loads(y.stdout).get("chapters") or []
    print(f"{time.strftime('%H:%M:%S')} Դաս {n} {vid}: description read back OK, "
          f"{sum(1 for l in ours if l[0].isspace())} of {len(ours)} indented, YouTube parsed {len(chaps)} chapters "
          f"{'OK' if len(chaps) == len(ours) else 'MISMATCH (may lag a few minutes)'} | {time.time() - t0:.0f} s", flush=True)
print(f"all 12 pushed in {time.time() - t_all:.0f} s", flush=True)
