"""Caption words (with times) from shortly before each end cut to the end of the upload, for Tserunyan 17-26,
grouped into 4 s lines, plus the end cuts as planned. For placing the end cut after her 'next time' line (Q48).
~1 s. Repo root."""
import json
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import find_edit_points as fep  # noqa: E402

FROM = {17: "1:48:00", 18: "1:23:50", 19: "1:37:00", 20: "1:33:00", 21: "1:31:30", 22: "1:27:30",
        23: "1:24:50", 25: "1:32:40", 26: "1:42:50"}
for n, start in FROM.items():
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    vid = d.name.split("_", 2)[2]
    t0 = fep.parse_t(start)
    cuts = json.loads((d / "content_cuts.json").read_text(encoding="utf-8"))["cuts"]
    print(f"\n=== Das {n}")
    for c in cuts:
        if fep.parse_t(c["end"]) > t0:
            print(f"  CUT {c['start']}-{c['end']} {c['kind']} {c['default']}")
    words = [(t, w) for t, w in fep.caption_words((d / f"{vid}.hy.vtt").read_text(encoding="utf-8")) if t >= t0]
    line, ls = [], None
    for t, w in words:
        if ls is None or t - ls >= 4:
            if line:
                print(f"  {fep.fmt_t(ls)} {' '.join(line)}")
            line, ls = [], t
        line.append(w)
    if line:
        print(f"  {fep.fmt_t(ls)} {' '.join(line)}")
