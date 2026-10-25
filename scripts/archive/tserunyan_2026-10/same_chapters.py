"""python same_chapters.py <old> <new>: the two chapter lists have the same indents, labels and seconds
(only the time format may differ); prints the first two lines of each. Exits 1 otherwise. ~0 s."""
import re
import sys
from pathlib import Path

LINE = re.compile(r"^(\s*)((?:\d+:)?\d+:\d{2})(\s.*)$")


def parse(p):
    out = []
    for l in Path(p).read_text(encoding="utf-8").splitlines():
        if not l.strip() or not LINE.match(l):
            continue
        m = LINE.match(l)
        secs = sum(int(v) * 60 ** i for i, v in enumerate(reversed(m[2].split(":"))))
        out.append((m[1], secs, m[3]))
    return out


a, b = parse(sys.argv[1]), parse(sys.argv[2])
if a != b:
    bad = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    print(f"DIFFERENT at chapter {bad + 1}: {a[bad] if bad < len(a) else None} vs {b[bad] if bad < len(b) else None}")
    sys.exit(1)
print(f"same {len(a)} chapters (indent, seconds, labels)")
