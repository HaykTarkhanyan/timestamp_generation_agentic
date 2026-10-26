"""Was the published version sped up? Match 60 s of published audio against the raw envelope resampled
at speeds 1.00..1.30; the right speed gives a clear correlation peak.

    python speed_test.py raw.wav published.wav [pub_start_s ...]
"""
import sys

import numpy as np
import soundfile as sf
from scipy.signal import correlate

HZ = 100


def envelope(path):
    x, sr = sf.read(path, dtype="float32")
    hop = sr // HZ
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(axis=1)) + 1e-6)


raw, pub = envelope(sys.argv[1]), envelope(sys.argv[2])
starts = [float(s) for s in sys.argv[3:]] or [120.0, 400.0, 700.0]
L = 60 * HZ
t_raw = np.arange(len(raw)) / HZ
for st in starts:
    w = pub[int(st * HZ): int(st * HZ) + L]
    if len(w) < L:
        continue
    wz = (w - w.mean()) / w.std()
    res = []
    for s in np.arange(1.00, 1.301, 0.01):
        # raw played s times faster: published time t <-> raw time s*t
        n = int(len(raw) / s)
        r = np.interp(np.arange(n) * s / HZ, t_raw, raw)
        cs = np.cumsum(np.concatenate([[0], r]))
        cs2 = np.cumsum(np.concatenate([[0], r ** 2]))
        m = (cs[L:] - cs[:-L]) / L
        sd = np.sqrt(np.maximum((cs2[L:] - cs2[:-L]) / L - m ** 2, 1e-9))
        c = correlate(r, wz, mode="valid", method="fft") / L / sd
        k = int(np.argmax(c))
        res.append((c[k], s, k * s / HZ))
    res.sort(reverse=True)
    best = res[0]
    print(f"published {st:6.1f}-{st + 60:6.1f} s: best speed {best[1]:.2f}x (corr {best[0]:.3f}, at raw {best[2]:.1f} s); "
          f"next {res[1][1]:.2f}x ({res[1][0]:.3f}), {res[2][1]:.2f}x ({res[2][0]:.3f}); 1.00x: "
          f"{[r for r in res if abs(r[1] - 1.0) < 1e-6][0][0]:.3f}")
