"""Read-only: has YouTube applied the Studio edits of Tserunyan 16-27? Compares contentDetails.duration with the
Save dialog's length. Uses the umath token in memory (no token write, no project log). ~2 s."""
import re
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\scripts\.secrets\token_umath.json")
EXPECT = {  # Դաս: (video id, Save dialog length)
    16: ("3K76N175zvM", "1:29:34"), 17: ("uqI8xFU3fkc", "1:35:17"), 18: ("UdfgVV4qofs", "1:15:03"),
    19: ("zTxIdWu_4pk", "1:27:14"), 20: ("4L-qOijveyU", "1:25:13"), 21: ("KNoSL5it7gA", "1:29:20"),
    22: ("B7V06PBa79g", "1:19:55"), 23: ("qtZsHmGWQD8", "1:23:03"), 24: ("OnsBx1KRAFk", "1:28:11"),
    25: ("3E1Tmzyoy_s", "1:31:14"), 26: ("8i6uYydDd4E", "1:41:47"), 27: ("FSV22FEP16A", "1:39:45"),
}

creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube.force-ssl"])
if not creds.valid:
    creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds)
items = yt.videos().list(part="contentDetails,status", id=",".join(v for v, _ in EXPECT.values())).execute()["items"]
got = {}
for it in items:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", it["contentDetails"]["duration"])
    h, mi, s = (int(x or 0) for x in m.groups())
    got[it["id"]] = (h * 3600 + mi * 60 + s, it["status"]["privacyStatus"])


def sec(t):
    h, m, s = map(int, t.split(":"))
    return h * 3600 + m * 60 + s


done = 0
for n, (vid, want) in EXPECT.items():
    if vid not in got:
        raise RuntimeError(f"Das {n} {vid}: not returned by the API")
    d, priv = got[vid]
    ok = abs(d - sec(want)) <= 1
    done += ok
    print(f"Das {n} {vid}: now {d // 3600}:{d % 3600 // 60:02d}:{d % 60:02d}, saved {want} -> "
          f"{'APPLIED' if ok else 'still processing (old length)'} [{priv}]")
print(f"{done} of {len(EXPECT)} applied")
