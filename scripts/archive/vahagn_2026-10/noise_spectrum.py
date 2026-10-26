"""Noise character of a recording: mean spectrum of the quietest frames vs speech frames, in bands,
plus the strongest narrow peaks in the noise (hum and its harmonics).

    python noise_spectrum.py <media file>
"""
import subprocess
import sys

import numpy as np

src = sys.argv[1]
SR = 32000
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(pcm, np.float32)
N = 4096
hop = N // 2
frames = np.lib.stride_tricks.sliding_window_view(x, N)[::hop] * np.hanning(N)
spec = np.abs(np.fft.rfft(frames, axis=1)) ** 2
lvl = 10 * np.log10(spec.sum(axis=1) + 1e-12)
q = lvl < np.percentile(lvl, 10)          # quietest 10%: room noise
s = lvl > np.percentile(lvl, 60)          # speech
f = np.fft.rfftfreq(N, 1 / SR)
noise, speech = spec[q].mean(axis=0), spec[s].mean(axis=0)
print(f"{len(x) / SR:.0f} s; frame level: quiet frames {np.median(lvl[q]):.1f} dB, speech {np.median(lvl[s]):.1f} dB "
      f"(speech-to-noise {np.median(lvl[s]) - np.median(lvl[q]):.1f} dB)")
print("band            noise dB   speech dB   SNR")
for lo, hi in [(20, 80), (80, 200), (200, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)]:
    m = (f >= lo) & (f < hi)
    nd, sd = 10 * np.log10(noise[m].sum() + 1e-15), 10 * np.log10(speech[m].sum() + 1e-15)
    print(f"{lo:5d}-{hi:<5d} Hz   {nd:7.1f}    {sd:7.1f}   {sd - nd:5.1f}")
# narrow peaks in the noise: bins more than 10 dB above their 50 Hz neighbourhood median
nd = 10 * np.log10(noise + 1e-15)
peaks = []
for i in range(5, len(f) - 5):
    if f[i] > 4000:
        break
    nb = np.median(nd[max(0, i - 7):i + 8])
    if nd[i] - nb > 10 and nd[i] == nd[max(0, i - 2):i + 3].max():
        peaks.append((f[i], nd[i] - nb))
print("narrow noise peaks (Hz, dB above neighbours):", [(round(a), round(b, 1)) for a, b in peaks[:15]] or "none")
