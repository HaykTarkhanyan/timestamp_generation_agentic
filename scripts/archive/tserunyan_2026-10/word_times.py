"""Exact caption word times in a window: python word_times.py <lesson> <from> <to>. ~1 s. Repo root."""
import sys
from pathlib import Path
REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import find_edit_points as fep
n, a, b = sys.argv[1], fep.parse_t(sys.argv[2]), fep.parse_t(sys.argv[3])
(d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
vid = d.name.split("_", 2)[2]
for t, w in fep.caption_words((d / f"{vid}.hy.vtt").read_text(encoding="utf-8")):
    if a <= t <= b:
        print(f"{fep.fmt_t(t, 2)} {w}")
