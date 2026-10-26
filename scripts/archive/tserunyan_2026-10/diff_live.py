"""Read-only: show where a live description differs from a local file. Usage: python diff_live.py <video id> <file>."""
import difflib
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\scripts\.secrets\token_umath.json")
creds = Credentials.from_authorized_user_file(str(TOKEN), ["https://www.googleapis.com/auth/youtube.force-ssl"])
if not creds.valid:
    creds.refresh(Request())
got = build("youtube", "v3", credentials=creds).videos().list(part="snippet", id=sys.argv[1]).execute()["items"][0]["snippet"]["description"]
want = Path(sys.argv[2]).read_text(encoding="utf-8").strip("\n")
print(f"live {len(got)} chars, file {len(want)} chars")
for l in difflib.unified_diff(want.splitlines(), got.splitlines(), "file", "live", lineterm="", n=0):
    print(repr(l))
