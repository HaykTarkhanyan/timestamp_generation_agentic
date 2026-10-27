"""Exact hum fundamental from the user's pure-noise sample (28.3.a 20:47.6-20:51.0): zero-padded spectrum, the peaks
under 1.2 kHz, a least-squares fit of f0 over the ones that sit near k*f0, and the peaks that do not fit."""
import subprocess

import numpy as np
from scipy.signal import find_peaks

SR = 32000
raw = r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg\Videos Part 9\VidSection 28.3.a.mp4"
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", "1247.6", "-t", "3.4", "-i", raw, "-vn", "-ac", "1",
                                  "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
nfft = 2 ** 20
s = np.abs(np.fft.rfft(x * np.hanning(len(x)), nfft)) ** 2
f = np.fft.rfftfreq(nfft, 1 / SR)
db = 10 * np.log10(s + 1e-20)
keep = f < 1200
pk, prop = find_peaks(db[keep], prominence=12, distance=int(10 / (SR / nfft)))
peaks = [(float(f[i]), float(db[i])) for i in pk]
peaks = sorted(peaks, key=lambda p: -p[1])[:25]
best = None
for f0 in np.arange(44, 52, 0.01):                       # the ladder that explains the most peak energy
    k = np.round(np.array([p[0] for p in peaks]) / f0)
    err = np.abs(np.array([p[0] for p in peaks]) - k * f0)
    fit = (err < 2.0) & (k >= 1)
    score = sum(10 ** (peaks[i][1] / 10) for i in np.flatnonzero(fit))
    if best is None or score > best[0]:
        best = (score, f0, fit, k)
_, f0, fit, k = best
fk = np.array([p[0] for p in peaks])[fit]
kk = k[fit]
f0_ls = float((fk * kk).sum() / (kk * kk).sum())
print(f"f0 = {f0_ls:.2f} Hz (least squares over {fit.sum()} harmonics: k = {sorted(int(v) for v in kk)})")
print("on the ladder: " + ", ".join(f"{p[0]:.1f} ({p[1]:.0f} dB)" for p, ok in zip(peaks, fit) if ok))
print("not on it:     " + ", ".join(f"{p[0]:.1f} ({p[1]:.0f} dB)" for p, ok in zip(peaks, fit) if not ok))
