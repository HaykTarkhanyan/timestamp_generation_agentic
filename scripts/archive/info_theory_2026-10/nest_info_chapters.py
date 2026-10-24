"""Nest Ashot's chapter lists Metric-Academy style (4 spaces before a sub-chapter's time, one level, a parent
has 2+ children) and write videos over an hour as H:MM:SS on every line (0:00:00 ...). Labels and times are
unchanged. Reads the live descriptions; writes local copies (Դաս 4-8 description.txt + timestamps.txt in their
output folders, Դաս 0-3 into scratchpad/ashot_desc_nested/). No API writes. ~3 s.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
S = Path(__file__).parent
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()

# lesson -> (video id, local output folder or None, indices of the sub-chapters)
SPEC = {
    0: ("U3BbIALq4aM", None, set()),
    1: ("4IO6iU7rRTA", None, {3, 4, 5, 6, 12, 13, 17, 18, 19, 20}),
    2: ("N3LL6k55sao", None, {3, 4, 5, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 28, 29}),
    3: ("bHyOK-SSawI", None, {2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 24, 25}),
    4: ("fHPN7fJEusA", "2026-10-20_Das-4-ToDo-Informaciayi-tesutyun_fHPN7fJEusA", {1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 22, 23, 24, 25}),
    5: ("0WSFqm9E-Pc", "2026-10-20_Das-5-ToDo-Informaciayi-tesutyun_0WSFqm9E-Pc", {3, 4, 5, 11, 12, 13, 14, 15, 17, 18, 20, 21, 22, 23}),
    6: ("LRQ6r_DaAVU", "2026-10-24_Das-6-Tvyalneri-seghmum-Koderi_LRQ6r_DaAVU", {5, 6, 16, 17, 20, 21}),
    7: ("S8vcM74HZVE", "2026-10-24_das7-final-1080p_S8vcM74HZVE", {2, 3, 5, 6, 7, 9, 10, 15, 16, 19, 20, 21, 22, 23, 24}),
    8: ("LOHGyVgaIuI", "2026-10-24_das8-final-1080p_LOHGyVgaIuI", {5, 6, 7, 8, 9, 11, 12, 14, 15, 20, 21, 22, 23, 24, 25, 26}),
}
CHAP = re.compile(r"^\s*(\d+(?::\d+){1,2})\s+(.*)$")

r = yt.videos().list(part="snippet,contentDetails", id=",".join(v[0] for v in SPEC.values())).execute()
live = {v["id"]: v for v in r["items"]}
out_dir = S / "ashot_desc_nested"
out_dir.mkdir(exist_ok=True)
for n, (vid, folder, kids) in SPEC.items():
    v = live[vid]
    desc = v["snippet"]["description"]
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
    over_hour = int(m[1] or 0) > 0
    head, rest = desc.split("⏳ Թեմաներ\n", 1)
    lines = rest.split("\n")
    k = 0
    while k < len(lines) and CHAP.match(lines[k]):
        k += 1
    chap, tail = lines[:k], lines[k:]
    if not chap or max(kids, default=-1) >= len(chap):
        raise ValueError(f"Դաս {n}: {len(chap)} chapters, indices {sorted(kids)}")
    if 0 in kids:
        raise ValueError(f"Դաս {n}: the first chapter cannot be a sub-chapter")
    new = []
    for i, ln in enumerate(chap):
        ts, label = CHAP.match(ln).groups()
        sec = sum(int(x) * 60 ** j for j, x in enumerate(reversed(ts.split(":"))))
        ts = f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}" if over_hour else f"{sec // 60:02d}:{sec % 60:02d}"
        new.append(("    " if i in kids else "") + f"{ts} {label.rstrip()}")
    # every parent (a non-indented line followed by indented ones) must have 2+ children
    runs, i = [], 0
    while i < len(chap):
        if i in kids:
            j = i
            while j < len(chap) and j in kids:
                j += 1
            runs.append((i - 1, j - i))
            i = j
        else:
            i += 1
    lone = [p for p, size in runs if size < 2]
    if lone:
        raise ValueError(f"Դաս {n}: parents with a single child at indices {lone}")
    text = head + "⏳ Թեմաներ\n" + "\n".join(new + tail)
    if "<" in text or ">" in text or len(text) > 5000:
        raise ValueError(f"Դաս {n}: angle bracket or too long ({len(text)})")
    if folder:
        p = REPO / "output" / folder / "description.txt"
        local = p.read_text(encoding="utf-8")
        top, body = local.split("──────────────────────────────", 1)
        if body.strip() != desc.strip():
            print(f"Դաս {n}: local description.txt differed from live (before nesting); live wins")
        p.write_text(top + "──────────────────────────────\n\n" + text.strip() + "\n", encoding="utf-8")
        (REPO / "output" / folder / "timestamps.txt").write_text("\n".join(new) + "\n", encoding="utf-8")
    else:
        p = out_dir / f"das{n}.txt"
        p.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Դաս {n}: {len(chap)} chapters, {len(runs)} parents, {len(kids)} sub-chapters, "
          f"{'H:MM:SS' if over_hour else 'MM:SS'} -> {p}")
