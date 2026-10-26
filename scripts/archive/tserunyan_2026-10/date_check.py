"""Each Tserunyan description's date line against the date in the recording's file name
(video/*.source.txt). Read-only, instant."""
import re
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
MONTHS = {"մարտ": 3, "ապրիլ": 4, "մայիս": 5, "հունիս": 6}
bad = 0
for n in range(15, 28):
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    src = next((d / "video").glob("*.source.txt")).read_text(encoding="utf-8").splitlines()[0]
    y, m, dd = map(int, re.search(r"(\d{4})-(\d\d)-(\d\d)\.mp4", src).groups())
    ed = d / "edited" if (d / "edited" / "description.txt").exists() else d / "edited_predicted"
    line = next(l for l in (ed / "description.txt").read_text(encoding="utf-8").splitlines()
                if l.startswith("🗓️"))
    day, month, year = re.search(r"(\d+) (\S+), (\d{4})", line).groups()
    ok = (int(day), MONTHS[month], int(year)) == (dd, m, y)
    bad += not ok
    print(f"Das {n}: file {y}-{m:02d}-{dd:02d} | {line} | {'OK' if ok else 'MISMATCH'}")
print(f"{13 - bad} of 13 match")
