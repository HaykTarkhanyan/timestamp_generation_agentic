"""Which planned content cuts (ticked or suggested) the user's studio_cuts_edited.txt left out, and which of
the user's cuts are not in the plan. Usage: python missed_suggestions.py <output dir>. Instant."""
import json
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])


def sec(t):
    parts = [float(x) for x in t.split(":")]
    if len(parts) == 4:   # H:MM:SS:FF at 25 fps
        h, m, s, f = parts
        return h * 3600 + m * 60 + s + f / 25
    h, m, s = parts
    return h * 3600 + m * 60 + s


user = [(sec(a), sec(b)) for a, b in re.findall(r"^Cut\s+\d+\s+(\S+)\s+->\s+(\S+)",
                                                (d / "studio_cuts_edited.txt").read_text(encoding="utf-8"), re.M)]
plan = json.loads((d / "content_cuts.json").read_text(encoding="utf-8"))["cuts"]


def overlap(a, b, c, e):
    return max(0.0, min(b, e) - max(a, c))


def hms(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:04.1f}"


for c in plan:
    s, e = sec(c["start"]), sec(c["end"])
    cov = sum(overlap(s, e, a, b) for a, b in user)
    state = "TAKEN" if cov >= 0.8 * (e - s) else ("PARTLY" if cov > 0 else "LEFT OUT")
    tick = "ticked" if c["default"] else "suggestion"
    print(f"{state:8} {tick:10} {hms(s)} -> {hms(e)} ({e - s:.1f} s, {cov:.1f} s cut)\n    {c['reason'][:400]}")
print("\nuser cuts not touching any planned content cut:")
for a, b in user:
    if not any(overlap(a, b, sec(c["start"]), sec(c["end"])) for c in plan):
        print(f"    {hms(a)} -> {hms(b)} ({b - a:.1f} s)")
