"""Find which stretches of a raw recording were removed in the published (edited) version.

Loudness envelopes at 100 Hz, each clipped at its own floor + 15 dB (so codec noise in silences
doesn't matter). Walk the published audio in 2 s windows (hop 0.5 s) that contain speech and find
each one's position in the raw, searching forward from the last position and taking the EARLIEST
lag that scores close to the best (cuts are removals, so the raw position only moves forward).
A jump in offset = a removed raw stretch. Each stretch is then described: share of silence (raw
under floor + 20 dB, find_edit_points.py's rule) and its longest silence.

    python find_removed.py raw.wav published.wav [--csv out.csv]
"""
import sys

import numpy as np
import soundfile as sf

HZ = 100


def envelope(path):
    x, sr = sf.read(path, dtype="float32")
    hop = sr // HZ
    n = len(x) // hop
    e = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(axis=1)) + 1e-6)
    fl = np.percentile(e[e > -119], 5)
    return e, fl


raw_e, raw_fl = envelope(sys.argv[1])
pub_e, pub_fl = envelope(sys.argv[2])
silent = raw_e < raw_fl + 20
raw = np.maximum(raw_e, raw_fl + 15)
pub = np.maximum(pub_e, pub_fl + 15)
print(f"raw {len(raw) / HZ:.1f} s, published {len(pub) / HZ:.1f} s, removed {(len(raw) - len(pub)) / HZ:.1f} s; "
      f"raw floor {raw_fl:.1f} dB, published floor {pub_fl:.1f} dB, {silent.mean():.0%} of raw frames silent")

W, HOP = 2 * HZ, HZ // 2
matches = []                 # (pub_frame, raw_frame, corr)
pos_off = 0                  # current offset raw - pub
for p in range(0, len(pub) - W, HOP):
    w = pub[p:p + W]
    if w.std() < 2.5:        # (almost) flat: silence, carries no position information
        continue
    wz = (w - w.mean()) / w.std()
    found = None
    for ahead in (20 * HZ, 120 * HZ):
        lo = max(0, p + pos_off - HZ // 2)
        hi = min(len(raw), p + pos_off + ahead + W)
        seg = raw[lo:hi]
        if len(seg) < W:
            break
        cs = np.cumsum(np.concatenate([[0], seg]))
        cs2 = np.cumsum(np.concatenate([[0], seg ** 2]))
        m = (cs[W:] - cs[:-W]) / W
        sd = np.sqrt(np.maximum((cs2[W:] - cs2[:-W]) / W - m ** 2, 1e-9))
        c = np.correlate(seg, wz, "valid") / W / sd
        best = c.max()
        if best >= 0.9:
            k = int(np.argmax(c >= best - 0.02))       # earliest near-best lag
            found = (lo + k, float(c[k]))
            break
    if found:
        raw_f, sc = found
        pos_off = raw_f - p
        matches.append((p, raw_f, sc))

print(f"{len(matches)} matched windows of {len(range(0, len(pub) - W, HOP))}")

# offsets must be non-decreasing; drop isolated outliers that go backwards
clean = []
for p, r, s in matches:
    if clean and r - p < clean[-1][1] - clean[-1][0] - 5:
        continue
    clean.append((p, r, s))


def fmt(f):
    s = f / HZ
    return f"{int(s // 60)}:{s % 60:04.1f}"


rows = []
for (p0, r0, _), (p1, r1, _) in zip(clean, clean[1:]):
    d = (r1 - p1) - (r0 - p0)
    if d < 15:               # under 0.15 s: jitter
        continue
    # the removed raw part lies between r0 and r1 (raw), length d; place it where the raw is most silent
    span = (r1 - r0)
    best = None
    for x in range(0, max(1, span - d + 1)):
        a, b = r0 + x, r0 + x + d
        sv = silent[a:b].mean()
        if best is None or sv > best[0] + 1e-9:
            best = (sv, a, b)
    sv, a, b = best
    run = longest = 0
    for v in silent[a:b]:
        run = run + 1 if v else 0
        longest = max(longest, run)
    rows.append((a, b, d, sv, longest))

total = sum(r[2] for r in rows)
print(f"{len(rows)} removed stretches, {total / HZ:.1f} s in all (expected {(len(raw) - len(pub)) / HZ:.1f} s)")
for a, b, d, sv, lg in rows:
    print(f"  raw {fmt(a):>8} - {fmt(b):>8}  {d / HZ:5.1f} s  silent {sv:4.0%}  longest silence {lg / HZ:4.1f} s")
if rows:
    d = np.array([r[2] for r in rows]) / HZ
    print(f"lengths: median {np.median(d):.1f} s, min {d.min():.1f}, max {d.max():.1f}; >=80% silent: "
          f"{sum(r[3] >= 0.8 for r in rows)}, mostly speech (<50% silent): {sum(r[3] < 0.5 for r in rows)}")

# which raw silences survived, by length
runs, i = [], 0
while i < len(silent):
    if silent[i]:
        j = i
        while j < len(silent) and silent[j]:
            j += 1
        runs.append((i, j))
        i = j
    else:
        i += 1
cut = np.zeros(len(raw), bool)
for a, b, *_ in rows:
    cut[a:b] = True
for lo_s in (0.7, 1.0, 1.5, 2.0, 3.0):
    longer = [(a, b) for a, b in runs if (b - a) / HZ >= lo_s]
    kept = [(a, b) for a, b in longer if cut[a:b].mean() < 0.5]
    print(f"raw silences >= {lo_s:.1f} s: {len(longer):3d}, left uncut: {len(kept):3d}")
