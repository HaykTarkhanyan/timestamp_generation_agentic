"""End-screen job files for the Arnak playlist (lesson 1 was done by hand): one .playwright-mcp/endscreen_NN_<id>.js
per video from endscreen_template.js (next to this file). Run: python scripts/non_essential/make_endscreen_jobs.py
(~1 s; refresh output/arnak_overview/overview.json first with playlist_overview.py if titles changed). Next video: the next lesson in the playlist, but 12 -> 13 and 2025 -> 13
(the 2025 recording is an extra); 13 -> Best for viewer. The order and titles come from overview.json."""
import json
import re
from pathlib import Path

REPO = Path("C:/Users/hayk_/OneDrive/Desktop/timestamp_generation_agentic")
here = Path(__file__).parent
vids = json.loads((REPO / "output/arnak_overview/overview.json").read_text(encoding="utf-8"))["videos"]
tpl = (here / "endscreen_template.js").read_text(encoding="utf-8")
PL = "Բազմաչափ վիճակագրություն"
by_label = {}
for v in vids:
    m = re.match(r"^Դաս (\d+)( \(2025\))? \| (.+?) \| ", v["title"])
    by_label[m[1] + ("y" if m[2] else "")] = {"id": v["id"], "n": m[1], "topic": m[3]}
nxt = {str(n): str(n + 1) for n in range(1, 12)} | {"12": "13", "12y": "13", "13": None}
for i, label in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "12y", "13"], start=2):
    me, to = by_label[label], nxt[label] and by_label[nxt[label]]
    job = {"id": me["id"], "lesson": label, "playlist": PL,
           "next": {"prefix": f"Դաս {to['n']} |", "query": to["topic"]} if to else None}
    out = REPO / ".playwright-mcp" / f"endscreen_{i:02d}_{label}_{me['id']}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    print(out.name, "->", job["next"]["prefix"] if job["next"] else "Best for viewer", "|", job["next"]["query"] if job["next"] else "")
