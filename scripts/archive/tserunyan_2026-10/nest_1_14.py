"""DECISIONS #39 for the published Tserunyan Դաս 1-14 (the user, 2026-10-26: "39 - yes i want consistent"): nest the
live chapter lists (4 spaces, one level, a parent has 2+ children, a theorem with a single proof stays flat) and
write every time as H:MM:SS. Reads nest_1_14/live.json (fetch_1_14.py), writes nest_1_14/desc_<N>.txt (the whole
new description) and nest_1_14/plan.json. Proves: labels and seconds unchanged, only indent and time format differ,
nothing outside the chapter block changed, the rules hold. No YouTube writes. ~1 s."""
import json
import re
from pathlib import Path

OUT = Path(__file__).parent / "nest_1_14"
# lesson -> [(parent line, first child, last child)], 1-based line numbers of the live chapter list
PLAN = {
    "1-2": [(4, 5, 8), (9, 10, 12), (13, 14, 15)],
    "3": [(2, 3, 4), (7, 8, 9), (12, 13, 14), (16, 17, 19), (22, 23, 24)],
    "4": [(1, 2, 3), (5, 6, 9), (10, 11, 12), (14, 15, 16), (17, 18, 22), (23, 24, 25)],
    "5": [(8, 9, 10), (15, 16, 19), (23, 24, 25), (26, 27, 30)],
    "6": [(3, 4, 6), (7, 8, 10), (11, 12, 16)],
    "8": [(6, 7, 10), (11, 12, 15), (17, 18, 19), (20, 21, 22), (24, 25, 26)],
    "9": [(3, 4, 8), (9, 10, 11), (12, 13, 15)],
    "10": [(2, 3, 6), (7, 8, 9), (10, 11, 13), (14, 15, 16), (18, 19, 22), (26, 27, 29)],
    "11": [(6, 7, 9), (10, 11, 13), (18, 19, 21), (22, 23, 24)],
    "12": [(1, 2, 3), (4, 5, 8), (9, 10, 18), (19, 20, 23)],
    "13": [(1, 2, 6), (12, 13, 16), (19, 20, 22), (25, 26, 28)],
    "14": [(6, 7, 10), (11, 12, 14), (15, 16, 21)],
}
CHAP = re.compile(r"^(\s*)(\d{1,2}(?::\d\d){1,2})\s+(.*?)\s*$")


def secs(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def hms(s):
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


live = json.loads((OUT / "live.json").read_text(encoding="utf-8"))
total_nested = total_parents = 0
for v in live:
    n = v["lesson"]
    lines = v["description"].split("\n")
    idx = [i for i, l in enumerate(lines) if CHAP.match(l)]
    if idx != list(range(idx[0], idx[-1] + 1)):
        raise ValueError(f"Դաս {n}: chapter lines are not one block: {idx}")
    chap = [CHAP.match(lines[i]).groups() for i in idx]
    if any(ind for ind, _, _ in chap):
        raise ValueError(f"Դաս {n}: already indented")
    child = set()
    for p, a, b in PLAN[n]:
        if not (p + 1 == a and b - a >= 1 and b <= len(chap)) or p in child or child & set(range(a, b + 1)):
            raise ValueError(f"Դաս {n}: bad group {(p, a, b)}")
        child |= set(range(a, b + 1))
    parents = {p for p, _, _ in PLAN[n]}
    if parents & child or 1 in child:
        raise ValueError(f"Դաս {n}: a parent is also a child, or the first chapter is indented")
    new = [f"{'    ' if k in child else ''}{hms(secs(t))} {lab}" for k, (_, t, lab) in enumerate(chap, 1)]
    out = lines[:idx[0]] + new + lines[idx[-1] + 1:]
    # proof: same seconds and labels, only indent/format differ, rest of the description untouched
    back = [CHAP.match(l).groups() for l in new]
    assert [(secs(t), lab) for _, t, lab in back] == [(secs(t), lab) for _, t, lab in chap]
    assert out[:idx[0]] == lines[:idx[0]] and out[idx[0] + len(new):] == lines[idx[-1] + 1:]
    assert secs(back[0][1]) == 0 and not back[0][0]
    text = "\n".join(out)
    if re.search(r"[<>]", text) or len(text) > 5000:
        raise ValueError(f"Դաս {n}: ASCII < > or over 5000 chars ({len(text)})")
    (OUT / f"desc_{n}.txt").write_text(text, encoding="utf-8")
    total_nested += len(child)
    total_parents += len(parents)
    print(f"Դաս {n} {v['id']}: {len(chap)} chapters, {len(child)} nested under {len(parents)} parents, "
          f"{len(text)} chars")
(OUT / "plan.json").write_text(json.dumps(PLAN, indent=1), encoding="utf-8")
print(f"all 12: {total_nested} of {sum(1 for v in live for l in v['description'].splitlines() if CHAP.match(l))} "
      f"chapters nested under {total_parents} parents")
