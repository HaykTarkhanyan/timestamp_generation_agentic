"""Mains buzz per piece, the measure the user's sample points to: the 150-600 Hz band in the QUIETEST moments (10th
percentile of 128 ms frames, i.e. the pauses) relative to the piece's speech level (90th percentile, full band), per
minute and overall. Raw sound, 16 kHz mono, in blocks. usage: buzz_band.py [sections...]"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
RAW = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
SR, N, HOP = 16000, 2048, 1024
f = np.fft.rfftfreq(N, 1 / SR)
BAND = (f >= 150) & (f <= 600)
uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
todo = [u for u in uploads if len(sys.argv) < 2 or u["section"] in sys.argv[1:]]
res, t0 = {}, time.time()
for n, u in enumerate(todo, 1):
    raw = next(iter([*RAW.glob(f"Videos Part */VidSection {u['section']}.mp4"),
                     *RAW.glob(f"already_on_youtube/VidSection {u['section']}.mp4")]))
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(raw), "-vn", "-ac", "1", "-ar", str(SR), "-f",
                                      "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
    nf = (len(x) - N) // HOP
    band, full = np.empty(nf, np.float32), np.empty(nf, np.float32)
    win = np.hanning(N).astype(np.float32)
    for b0 in range(0, nf, 4000):
        b1 = min(nf, b0 + 4000)
        s = np.abs(np.fft.rfft(x[np.arange(N)[None, :] + HOP * np.arange(b0, b1)[:, None]] * win, axis=1)) ** 2
        band[b0:b1] = 10 * np.log10(s[:, BAND].sum(axis=1) + 1e-12)
        full[b0:b1] = 10 * np.log10(s.sum(axis=1) + 1e-12)
    speech = np.percentile(full, 90)
    fpm = int(60 * SR / HOP)
    per_min = [round(float(np.percentile(band[i:i + fpm], 10) - speech), 1) for i in range(0, nf - fpm // 2, fpm)]
    overall = float(np.percentile(band, 10) - speech)
    res[u["section"]] = {"buzz_vs_speech_db": round(overall, 1), "per_min": per_min}
    pm = np.array(per_min)
    print(f"{n:2d}/{len(todo)} {u['section']:7} 150-600 Hz in the quiet moments, vs speech: {overall:6.1f} dB; per minute "
          f"min {pm.min():6.1f} / median {np.median(pm):6.1f} / max {pm.max():6.1f}  {time.time() - t0:.0f} s", flush=True)
(Path(__file__).parent / ("buzz_band.json" if len(sys.argv) < 2 else "buzz_band_test.json")).write_text(
    json.dumps(res, indent=1), encoding="utf-8")
