"""Noise floor (5th percentile of 10 ms frame levels, digital silence excluded) and speech level (60th pct)
of several files, each decoded the same way: first channel only, 48 kHz."""
import subprocess
import sys

import numpy as np

for src in sys.argv[1:]:
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-af", "pan=mono|c0=c0", "-ar", "48000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.float32)
    hop = 480
    n = len(x) // hop
    lv = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(axis=1)) + 1e-9)
    lv = lv[lv > -150]
    print(f"{src.split('/')[-1][:40]:40}  floor {np.percentile(lv, 5):6.1f} dB   speech {np.percentile(lv, 60):6.1f} dB")
