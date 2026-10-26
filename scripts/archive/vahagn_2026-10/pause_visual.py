"""Hypothesis test: does the user keep the pauses where the picture changes (Vahagn writing on his PDF) and cut the
ones where it stands still? For every silent run of 1.5 s+ (find_edit_points' own frames): how much of the screen
changes during it, from the 360p preview at 5 fps, 160x90 grey. Then cut-by-user vs left, side by side."""
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import cut_list  # noqa: E402
import find_edit_points as fep  # noqa: E402

d = Path(sys.argv[1])
data, fr = cut_list.load(d)
U = [(s / fr.fps, e / fr.fps) for _, s, e, _ in cut_list.read_cuts(d / "studio_cuts_edited.txt", fr)]
_, _, _, _, _, sound = fep.levels(d)
edges = np.flatnonzero(np.diff(np.r_[0, (~sound).astype(np.int8), 0]))
runs = [(a / 100, b / 100) for a, b in zip(edges[::2], edges[1::2]) if (b - a) / 100 >= 1.5]

proxy = next((d / "video").glob("*_360p.mp4"))
W, H, FPS = 160, 90, 5
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(proxy), "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                      "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
changed = (np.abs(np.diff(frames, axis=0)) > 25).sum(axis=(1, 2))    # pixels changed between frames k and k+1
print(f"{len(frames)} frames ({len(frames) / FPS / 60:.1f} min); changed px per step: median {np.median(changed):.0f}, "
      f"95th pct {np.percentile(changed, 95):.0f}")


def covered(a: float, b: float) -> bool:
    return any(min(b, e) - max(a, s) >= 0.5 * (b - a) for s, e in U)


rows = []
for a, b in runs:
    k0, k1 = int(np.ceil(a * FPS)), int(b * FPS)
    seg = changed[k0:k1]
    if len(seg) == 0:
        continue
    active = (seg > 4).mean()          # share of steps where more than a cursor-sized change happens
    rows.append((a, b, covered(a, b), active, int(seg.sum())))

for name, flag in (("CUT by user", True), ("LEFT uncut", False)):
    sel = [r for r in rows if r[2] == flag]
    act = np.array([r[3] for r in sel])
    print(f"\n{name}: {len(sel)} pauses; share of the pause with the picture changing: median {np.median(act):.2f}, "
          f"mean {act.mean():.2f}; still (under 10%): {(act < 0.10).sum()}, active (40%+): {(act >= 0.40).sum()}")
print("\npauses of 2.5 s+ with their activity:")
for a, b, cut, act, tot in sorted(rows):
    if b - a >= 2.5:
        print(f"  {int(a // 60)}:{a % 60:04.1f} {b - a:4.2f}s  {'CUT ' if cut else 'left'}  picture changing {act:4.2f}  ({tot} px)")
