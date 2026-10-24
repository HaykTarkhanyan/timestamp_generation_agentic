"""Page titles of every info theory deck (first non-empty line of each page), and which pages are new
compared with the previous deck of the same part. Writes deck_titles.json next to this script. ~2 s.

    python -I deck_titles.py <slides dir>
"""
import json
import sys
from pathlib import Path

import fitz

d = Path(sys.argv[1])
order = ["Intro-L-1", "Intro-L-1-extended", "L-3", "L-4", "L-5", "L-6", "L-8", "L-10", "L-11",
         "ChannelCapacity-L-13-end"]
out = {}
for key in order:
    pdf = next(p for p in d.glob("*.pdf") if p.stem.replace("InformationTheory-ASDS-2026-", "").replace("-posted", "") == key)
    doc = fitz.open(pdf)
    titles = []
    for page in doc:
        lines = [ln.strip() for ln in page.get_text().splitlines() if ln.strip()]
        titles.append(lines[0][:90] if lines else "")
    out[key] = {"file": pdf.name, "pages": len(doc), "titles": titles}

prev = None
for key in order:
    t = out[key]["titles"]
    if prev is not None:
        seen = set(out[prev]["titles"])
        new = [i + 1 for i, x in enumerate(t) if x not in seen]
        out[key]["new_pages"] = new
    prev = key
Path(sys.argv[0]).with_name("deck_titles.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for key in order:
    o = out[key]
    print(f"== {key}: {o['pages']} p, new pages {o.get('new_pages', 'all')[:60] if isinstance(o.get('new_pages'), list) else 'all'}")
    for i, x in enumerate(o["titles"], 1):
        if "new_pages" not in o or i in o["new_pages"]:
            print(f"  {i:3d} {x}")
