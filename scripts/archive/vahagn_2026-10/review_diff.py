"""What did the user change on studio.html? For one output dir: every reviewed cut against the sound (same 10 ms
frames and threshold as find_edit_points) and the transcript, the pauses left uncut, and which pause length matches
the user's choices best. Read-only."""
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import cut_list  # noqa: E402
import find_edit_points as fep  # noqa: E402

d = Path(sys.argv[1])
data, fr = cut_list.load(d)
user = sorted(cut_list.read_cuts(d / "studio_cuts_edited.txt", fr), key=lambda c: c[1])
plan = sorted(cut_list.read_cuts(d / "studio_cuts.txt", fr), key=lambda c: c[1])
_, _, db, floor, thr, sound = fep.levels(d)
silent = ~sound
edges = np.flatnonzero(np.diff(np.r_[0, silent.astype(np.int8), 0]))
runs = [(a / 100, b / 100) for a, b in zip(edges[::2], edges[1::2])]
lines = []
for ln in (d / "transcript.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(\d+):(\d\d)(?::(\d\d))?\s+(.*)", ln)
    if m:
        h, mi, se = (0, int(m[1]), int(m[2])) if m[3] is None else (int(m[1]), int(m[2]), int(m[3]))
        lines.append((h * 3600 + mi * 60 + se, m[4]))
U = [(n, s / fr.fps, e / fr.fps, note) for n, s, e, note in user]


def mmss(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def said(a: float, b: float) -> str:
    return " / ".join(t for ts, t in lines if a - 1.5 <= ts <= b + 0.5)[:150]


print(f"floor {floor:.1f} dB, threshold {thr:.1f} dB")
print("\n== every reviewed cut ==")
for n, s, e, note in U:
    i0, i1 = int(s * 100), int(e * 100)
    snd = sound[i0:i1].sum() / 100
    inside = [(max(a, s), min(b, e)) for a, b in runs if b > s and a < e]
    longest = max((b - a for a, b in inside), default=0)
    tag = "NEW" if note.startswith("NEW") else ("CHG" if note.startswith("CHANGED") else "   ")
    print(f"{n:2d} {tag} {mmss(s):>7}-{mmss(e):<7} {e - s:5.2f}s  sound {snd:4.2f}s  longest pause {longest:4.2f}s  "
          f"{note.replace('CHANGED, ', '') if tag == 'CHG' else ''}")
    if snd > 0.3 or tag != "   ":
        print(f"         said: {said(s, e)}")


def covered(a: float, b: float) -> bool:
    return any(min(b, e) - max(a, s) >= 0.5 * (b - a) for _, s, e, _ in U)


print("\n== pauses of 1.5 s+ left uncut ==")
for a, b in runs:
    if b - a >= 1.5 and not covered(a, b):
        print(f"  {mmss(a)}-{mmss(b)} {b - a:4.2f}s   {said(a, b)[:110]}")

print("\n== which minimum pause matches the user ==")
print(" min   pauses  cut by user  left   user cuts with no such pause inside")
for x in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
    big = [(a, b) for a, b in runs if b - a >= x]
    cut = sum(covered(a, b) for a, b in big)
    orphan = sum(1 for _, s, e, _ in U if not any(min(b, e) - max(a, s) >= 0.5 * (b - a) for a, b in big))
    print(f" {x:3.1f}s  {len(big):6d}  {cut:11d}  {len(big) - cut:4d}   {orphan}")
print(f"\nplan {len(plan)} cuts, {sum(e - s for _, s, e, _ in plan) / fr.fps:.1f} s; "
      f"user {len(U)} cuts, {sum(e - s for _, s, e, _ in U):.1f} s")
