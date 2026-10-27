"""How much buzz is left in each dehum sample: inside the user's pure-noise stretch (17.6-21.0 s of the 30 s excerpt),
the 50-600 Hz band and the full band, relative to the sample's own speech level (90th pct of 128 ms frames)."""
import subprocess
from pathlib import Path

import numpy as np

OUT = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\output\vahagn_linalg_overview\audio")
SR, N, HOP = 16000, 2048, 512
f = np.fft.rfftfreq(N, 1 / SR)
for name in ("1_raw", "2_current", "3_notches", "4_profile", "5_both", "6_both_strong"):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(OUT / f"dehum_{name}.m4a"), "-ac", "1", "-ar",
                                      str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    nf = (len(x) - N) // HOP
    s = np.abs(np.fft.rfft(x[np.arange(N)[None, :] + HOP * np.arange(nf)[:, None]] * np.hanning(N), axis=1)) ** 2
    t = np.arange(nf) * HOP / SR
    full = 10 * np.log10(s.sum(axis=1) + 1e-12)
    speech = np.percentile(full, 90)
    m = (t >= 17.8) & (t <= 20.7)
    band = 10 * np.log10(s[m][:, (f >= 50) & (f <= 600)].sum(axis=1).mean() + 1e-12) - speech
    allb = 10 * np.log10(s[m].sum(axis=1).mean() + 1e-12) - speech
    print(f"{name:14} in the noise stretch: 50-600 Hz {band:6.1f} dB, whole band {allb:6.1f} dB (vs its speech)")
