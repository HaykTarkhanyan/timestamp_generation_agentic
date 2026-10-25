"""Tserunyan: read one pushed video back from the API (umath channel) and compare it with the local
<folder>/edited/titles.txt (line 1) and edited/description.txt (from line 5, the part that is pushed). Prints
title / description OK or DIFF, the number of chapter lines (nested ones included), duration, visibility and
the thumbnail URL. 1 API unit, ~2 s. From the repo root:

    python scripts/non_essential/metric_readback.py <video id>

Moved 2026-10-25 from the scratchpad of the session that finished Դաս 15 (was readback15.py).
"""
import logging
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "metric_readback.log", encoding="utf-8")])
log = logging.getLogger("metric_readback")

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
vid = sys.argv[1]
(d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-*-Metric*_{vid}") if p.is_dir()]
v = yt.videos().list(part="snippet,status,contentDetails", id=vid).execute()["items"][0]
s = v["snippet"]
want_title = (d / "edited/titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
lines = (d / "edited/description.txt").read_text(encoding="utf-8").splitlines()
want_desc = "\n".join(lines[4:]).strip()
chap = sum(1 for l in s["description"].splitlines() if l.lstrip()[:1].isdigit() and ":" in l.lstrip()[:9])
title_status = "OK" if s["title"] == want_title else f"DIFF {s['title']!r}"
log.info(f"{d.name[11:17]} title {title_status}")
log.info(f"{d.name[11:17]} description {'OK' if s['description'].strip() == want_desc else 'DIFF'}")
thumb = s["thumbnails"].get("maxres", s["thumbnails"].get("high"))["url"]
log.info(f"{d.name[11:17]} chapter lines {chap} | duration {v['contentDetails']['duration']} | "
         f"{v['status']['privacyStatus']} | thumbnail {sorted(s['thumbnails'])[-1]} {thumb[-40:]}")
