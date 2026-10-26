"""Standalone preview of the nested Դաս 1-14 chapter lists (TOC + one collapsible section per video), and a backup of
the live descriptions before the change. Writes _knowledge/tserunyan_metric/nest_1-14_preview.html and
descriptions_before_nest_2026-10-26.json. ~1 s."""
import html
import json
import re
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
KNOW = REPO / "_knowledge" / "tserunyan_metric"
SRC = Path(__file__).parent / "nest_1_14"
live = json.loads((SRC / "live.json").read_text(encoding="utf-8"))
(KNOW / "descriptions_before_nest_2026-10-26.json").write_text(
    json.dumps([{k: v[k] for k in ("lesson", "id", "title", "description")} for v in live], ensure_ascii=False, indent=1),
    encoding="utf-8")
E = html.escape
toc, secs = [], []
for v in live:
    n = v["lesson"]
    new = (SRC / f"desc_{n}.txt").read_text(encoding="utf-8")
    rows = []
    for l in new.splitlines():
        m = re.match(r"^(\s*)(\d+:\d\d:\d\d) (.*)$", l)
        if m:
            cls = "child" if m.group(1) else "parent"
            rows.append(f'<div class="{cls}"><span class="t">{m.group(2)}</span> {E(m.group(3))}</div>')
    nested = sum(1 for l in new.splitlines() if re.match(r"^\s+\d+:\d\d:\d\d ", l))
    toc.append(f'<li><a href="#d{n}">Դաս {n}</a> <span class="m">{nested} of {len(rows)} nested</span></li>')
    secs.append(f'<details open id="d{n}"><summary>Դաս {n} - {E(v["title"].split(" | ")[1])} '
                f'<span class="m">({nested} of {len(rows)} nested)</span></summary>'
                f'<p class="m"><a href="https://youtu.be/{v["id"]}">youtu.be/{v["id"]}</a></p>{"".join(rows)}</details>')
page = f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tserunyan 1-14 nesting</title><style>
:root{{--bg:#fff;--fg:#1a1a1a;--m:#666;--line:#ddd;--acc:#0033A0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16181c;--fg:#e8e8e8;--m:#9a9a9a;--line:#333;--acc:#8fb0ff}}}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:16px}}
details{{border-top:1px solid var(--line);padding:8px 0}} summary{{font-weight:600;cursor:pointer}}
.m{{color:var(--m);font-weight:400;font-size:13px}} .t{{font-family:ui-monospace,monospace;color:var(--acc)}}
.parent{{margin-top:4px}} .child{{margin-left:2.2em;border-left:2px solid var(--line);padding-left:.6em}}
a{{color:var(--acc)}} ul{{columns:2}}</style></head><body>
<h1>Tserunyan Դաս 1-14: nested chapters, H:MM:SS</h1>
<p class="m">DECISIONS #39 for the published videos. Only the indent and the time format change; labels, times and the
rest of each description stay as they are live (checked by the build script). Indented lines become sub-chapters on YouTube.</p>
<ul>{"".join(toc)}</ul>{"".join(secs)}</body></html>"""
(KNOW / "nest_1-14_preview.html").write_text(page, encoding="utf-8")
print(f"{KNOW / 'nest_1-14_preview.html'} {len(page) // 1024} KB")
