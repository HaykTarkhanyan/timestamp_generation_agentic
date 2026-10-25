"""Pause merge test on the user's Tserunyan edits (Դաս 15, 16): join silence runs separated by sounds of at most
G s, keep merged runs of at least T s that are at least F silent and have no caption word other than fillers,
pad 0.35 s. Score against the user's cuts: how many of their NEW cuts are found, how many found pauses they left
in. In memory only. ~20 s per lecture. Repo root."""
import json
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import find_edit_points as fep  # noqa: E402

CUT = re.compile(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)\s+\(([\d.]+) s\)\s*(\w*)")
FILLERS = {"ըըը", "ըը", "ըհը", "էէ", "էէէ", "օքեյ", "օկ", "ok", "okay", "հա", "հը", "մմ", "ամմ", "դ", "դս", "a"}


def tc(s, fps):
    h, m, sec, f = map(int, s.split(":"))
    return (h * 60 + m) * 60 + sec + f / fps


def ov(a, b):
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


out = {}
for n in ["16", "15"]:
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep = json.loads((d / "edit_points.json").read_text(encoding="utf-8"))
    fps = float(ep.get("fps", 25))
    user = [(tc(m[1], fps), tc(m[2], fps), m[4] or "KEPT") for l in (d / "studio_cuts_edited.txt").read_text(
        encoding="utf-8").splitlines() if (m := CUT.match(l))]
    new = [u for u in user if u[2] == "NEW"]
    vid = d.name.split("_", 2)[2]
    words = [(t, norm(w)) for t, w in fep.caption_words((d / f"{vid}.hy.vtt").read_text(encoding="utf-8")) if norm(w)]
    _, x, db, floor, thr, sound = fep.levels(d)
    a, b = fep.runs(~sound)
    sil = list(zip(a / 100, b / 100))
    for G in (0.0, 0.5, 1.0, 1.5):
        merged = []
        for s, e in sil:
            if merged and s - merged[-1][1] <= G:
                merged[-1] = (merged[-1][0], e, merged[-1][2] + (e - s))
            else:
                merged.append((s, e, e - s))
        for T in (3.0, 3.5, 4.0):
            cand = []
            for s, e, silent in merged:
                if e - s < T or silent / (e - s) < 0.6:
                    continue
                inner = [w for t, w in words if s + 0.3 <= t < e - 0.3]
                if any(w not in FILLERS for w in inner):
                    continue
                cand.append((s + 0.35, e - 0.35))
            found = sum(1 for u in new if any(ov(u, c) >= 0.5 * (u[1] - u[0]) for c in cand))
            extra = [c for c in cand if not any(ov(c, u) > 0 for u in user)]
            key = f"G{G:g}_T{T:g}"
            out.setdefault(n, {})[key] = {"cands": len(cand), "found": found, "new": len(new), "extra": len(extra),
                                          "extra_s": round(sum(c[1] - c[0] for c in extra), 1)}
            print(f"Das {n} join gaps <= {G:g} s, min {T:g} s: {len(cand):3d} pauses | user's NEW found {found}/{len(new)} "
                  f"| left in by the user: {len(extra)} ({sum(c[1] - c[0] for c in extra):.0f} s)", flush=True)
(Path(__file__).parent / "user_pause_merge_fit.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
