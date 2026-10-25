"""Which silence threshold reproduces the user's own Tserunyan edits (studio_cuts_edited.txt of Դաս 15, 16)?
Re-detects silences in memory with find_edit_points' own functions (nothing is written), at several minimum
lengths, and matches them against the user's cuts. ~20 s per lecture (WAV load). Run from the repo root.
Saves the result as JSON next to this script."""
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import find_edit_points as fep  # noqa: E402

CUT = re.compile(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)\s+\(([\d.]+) s\)\s*(\w*)")
THRESHOLDS = [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]


def tc(s, fps):
    h, m, sec, f = map(int, s.split(":"))
    return (h * 60 + m) * 60 + sec + f / fps


def overlap(a, b):
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


result = {}
for n in sys.argv[1:]:
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep = json.loads((d / "edit_points.json").read_text(encoding="utf-8"))
    fps = float(ep.get("fps", 25))
    user = []
    for line in (d / "studio_cuts_edited.txt").read_text(encoding="utf-8").splitlines():
        m = CUT.match(line)
        if m:
            user.append({"s": tc(m[1], fps), "e": tc(m[2], fps), "len": float(m[3]), "tag": m[4] or "KEPT"})
    new = [u for u in user if u["tag"] == "NEW"]
    _, x, db, floor, thr, sound = fep.levels(d)
    pad = ep["params"]["pad"]
    rows = {}
    for T in THRESHOLDS:
        cand = fep.silence_cuts(db, sound, thr, T, pad)
        iv = [(c["start"], c["end"]) for c in cand]
        hit_new = [u for u in new if any(overlap((u["s"], u["e"]), c) >= 0.5 * (u["e"] - u["s"]) for c in iv)]
        unused = [c for c in iv if not any(overlap(c, (u["s"], u["e"])) > 0 for u in user)]
        # edge differences of the matched new cuts: user minus detector (negative start = user cut earlier)
        ds, de = [], []
        for u in hit_new:
            c = max(iv, key=lambda c: overlap((u["s"], u["e"]), c))
            ds.append(round(u["s"] - c[0], 2))
            de.append(round(u["e"] - c[1], 2))
        rows[T] = {"candidates": len(cand), "new_matched": len(hit_new), "new_total": len(new),
                   "unused_candidates": len(unused),
                   "unused_examples": [(fep.fmt_t(c[0]), round(c[1] - c[0], 2)) for c in unused[:12]],
                   "median_start_diff": sorted(ds)[len(ds) // 2] if ds else None,
                   "median_end_diff": sorted(de)[len(de) // 2] if de else None}
        print(f"Das {n} >= {T:g} s: {len(cand):3d} candidates | user's NEW matched {len(hit_new)}/{len(new)} | "
              f"candidates the user did not cut: {len(unused)} | median edge diff start {rows[T]['median_start_diff']} "
              f"end {rows[T]['median_end_diff']}", flush=True)
    unmatched = [u for u in new if not any(overlap((u["s"], u["e"]), (c["start"], c["end"])) >= 0.5 * (u["e"] - u["s"])
                                           for c in fep.silence_cuts(db, sound, thr, 1.0, pad))]
    rows["new_not_silence_even_at_1s"] = [(fep.fmt_t(u["s"]), u["len"]) for u in unmatched]
    rows["new_len_sorted"] = sorted(u["len"] for u in new)
    print(f"Das {n}: user NEW cuts not matching any silence >= 1 s: {rows['new_not_silence_even_at_1s']}")
    print(f"Das {n}: user NEW cut lengths: {rows['new_len_sorted']}")
    print(f"Das {n}: {time.time() - t0:.0f} s", flush=True)
    result[n] = rows
(Path(__file__).parent / "user_pause_fit.json").write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
