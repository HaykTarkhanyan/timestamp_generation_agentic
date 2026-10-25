"""Nest the Tserunyan 15-27 chapter masters (DECISIONS #39): indent the listed lines of
edited_predicted/timestamps_raw.txt by 4 spaces, then regenerate the derived files and prove that only the
indentation changed. Flat master kept as timestamps_raw_flat.txt. ~30 s. Run from the repo root.

16-27: remap_chapters.py --to-cuts studio_cuts.txt (the plan under review).
15 (already edited and pushed): remap onto studio_cuts_to_enter.txt, indent edited/timestamps.txt (the
snapped list) by the same line numbers, metric_assemble.py 15.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
VERIFY = REPO / ".claude/skills/youtube-timestamps/scripts/verify_timestamps.py"
IND = "    "

# 1-based line numbers of the children (sub-chapters); the line before each run is its parent
NEST = {
    15: [3, 4, 6, 7, 8, 10, 11, 12, 17, 18, 19, 20, 21, 22, 27, 28],
    16: [8, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27],
    17: [3, 4, 5, 6, 8, 9, 10, 11, 13, 14, 15, 16, 17, 21, 22, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34],
    18: [2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 23, 24, 27, 28],
    19: [4, 5, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 29, 30],
    20: [2, 3, 5, 6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 22, 23, 25, 26],
    21: [8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26],
    22: [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28],
    23: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 24, 25, 26, 27],
    24: [2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29],
    25: [2, 3, 4, 6, 7, 8, 9, 15, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28],
    26: [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28],
    27: [3, 4, 5, 6, 8, 9, 11, 12, 13, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30],
}


def run(cmd):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"failed ({r.returncode}): {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-2000:]}")
    return r.stdout + r.stderr


def check_rules(n, kids, count):
    if 1 in kids or max(kids) > count:
        raise ValueError(f"Das {n}: bad child line numbers")
    runs, cur = [], []
    for i in range(1, count + 1):
        if i in kids:
            cur.append(i)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    lone = [r for r in runs if len(r) < 2]
    if lone:
        raise ValueError(f"Das {n}: parent with a single child at line(s) {lone}")
    return len(runs)


def indent(lines, kids):
    return [(IND + l if i in kids else l) for i, l in enumerate(lines, 1)]


def same_but_indent(a, b, what):
    if [l.lstrip() for l in a] != [l.lstrip() for l in b]:
        bad = next(k for k, (x, y) in enumerate(zip(a, b)) if x.lstrip() != y.lstrip()) if len(a) == len(b) else "length"
        raise ValueError(f"{what}: content changed, not just indentation (first difference at {bad})")


def read(p):
    return p.read_text(encoding="utf-8").splitlines()


def verify(ts, meta, tr):
    r = subprocess.run([sys.executable, str(VERIFY), str(ts), "--metadata", str(meta), "--transcript", str(tr),
                        "--min-gap", "30"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    return "valid" if r.returncode == 0 else "INVALID:\n" + (r.stdout + r.stderr)[-1500:]


for n, kids in NEST.items():
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep = d / "edited_predicted"
    raw_p = ep / "timestamps_raw.txt"
    raw = read(raw_p)
    if any(l.startswith(" ") for l in raw):
        raise ValueError(f"Das {n}: master already indented")
    parents = check_rules(n, set(kids), len(raw))
    flat_p = ep / "timestamps_raw_flat.txt"
    if not flat_p.exists():
        shutil.copy2(raw_p, flat_p)
    old_ts, old_desc = read(ep / "timestamps.txt"), read(ep / "description.txt")
    raw_p.write_text("\n".join(indent(raw, set(kids))) + "\n", encoding="utf-8")
    cuts = "studio_cuts_to_enter.txt" if n == 15 else "studio_cuts.txt"
    run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
         "--from-cuts", "raw", "--to-cuts", cuts])
    new_ts, new_desc = read(ep / "timestamps.txt"), read(ep / "description.txt")
    same_but_indent(old_ts, new_ts, f"Das {n} edited_predicted/timestamps.txt")
    same_but_indent(old_desc, new_desc, f"Das {n} edited_predicted/description.txt")
    if [l.startswith(IND) for l in new_ts] != [i in kids for i in range(1, len(raw) + 1)]:
        raise ValueError(f"Das {n}: indentation did not come through remap_chapters.py")
    status = verify(ep / "timestamps.txt", ep / "metadata.json", ep / "transcript.txt")
    extra = ""
    if n == 15:
        ed = d / "edited"
        snapped, old_final = read(ed / "timestamps.txt"), read(ed / "description.txt")
        if len(snapped) != len(raw) or any(l.startswith(" ") for l in snapped):
            raise ValueError("Das 15: edited/timestamps.txt is not the flat 30-line list")
        shutil.copy2(ed / "timestamps.txt", ed / "timestamps_flat.txt")
        (ed / "timestamps.txt").write_text("\n".join(indent(snapped, set(kids))) + "\n", encoding="utf-8")
        run(["scripts/non_essential/metric_assemble.py", "15"])
        same_but_indent(old_final, read(ed / "description.txt"), "Das 15 edited/description.txt")
        extra = f" | edited: {verify(ed / 'timestamps.txt', ed / 'metadata.json', ed / 'transcript.txt')}"
    print(f"Das {n}: {len(raw)} chapters, {len(kids)} nested under {parents} parents, only indentation changed, "
          f"verifier {status}{extra}", flush=True)
