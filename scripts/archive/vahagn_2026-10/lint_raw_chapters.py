"""Lint every Vahagn edited_predicted/timestamps_raw.txt: starts at 00:00, increasing, gaps >= 30 s (raw),
a parent has >= 2 children, children never first, last chapter >= 20 s before the raw end, no ASCII < >."""
import json
import re
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
LINE = re.compile(r"^(    )?(\d+):(\d\d) (.+)$")
total = 0
for u in uploads:
    dirs = list(REPO.glob(f"output/*_{u['id']}"))
    if not dirs or not (dirs[0] / "edited_predicted/timestamps_raw.txt").exists():
        print(f"{u['section']:7} no draft")
        continue
    d = dirs[0]
    dur = json.loads((d / "metadata.json").read_text(encoding="utf-8"))["duration"]
    rows = []
    issues = []
    for ln in (d / "edited_predicted/timestamps_raw.txt").read_text(encoding="utf-8").splitlines():
        m = LINE.match(ln)
        if not m:
            issues.append(f"unparsed: {ln!r}")
            continue
        rows.append((bool(m[1]), int(m[2]) * 60 + int(m[3]), m[4]))
        if "<" in ln or ">" in ln:
            issues.append(f"ASCII < or >: {ln}")
    if rows and rows[0][1] != 0:
        issues.append("first chapter not 00:00")
    if rows and rows[0][0]:
        issues.append("first chapter indented")
    for a, b in zip(rows, rows[1:]):
        if b[1] <= a[1]:
            issues.append(f"not increasing at {b[2][:40]}")
        elif b[1] - a[1] < 30:
            issues.append(f"gap {b[1] - a[1]} s before {b[2][:50]}")
    # children per parent
    i = 0
    while i < len(rows):
        if not rows[i][0]:
            j = i + 1
            while j < len(rows) and rows[j][0]:
                j += 1
            if j - i - 1 == 1:
                issues.append(f"parent with one child: {rows[i][2][:50]}")
            i = j
        else:
            i += 1
    if rows and dur - rows[-1][1] < 20:
        issues.append(f"last chapter {dur - rows[-1][1]} s before the end")
    total += len(issues)
    print(f"{u['section']:7} {len(rows):2d} chapters {'OK' if not issues else ''}")
    for s in issues:
        print(f"        - {s}")
print(f"{total} issue(s)")
