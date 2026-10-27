"""Probe: where does Vahagn's audio get a static / hiss layer? For every piece, the background level in the PAUSES
(find_edit_points' sound mask), per 10 s window, in a high band (3-7.5 kHz) and the whole band, against the piece's
own usual pause level. Stretches 8 dB+ above it are listed. Read-only; ~5 s per piece."""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import logging  # noqa: E402
logging.disable(logging.INFO)
import find_edit_points as fep  # noqa: E402

SR, N, HOP, WIN = 16000, 1024, 160, 10.0          # 10 ms hop, the sound mask's resolution
f = np.fft.rfftfreq(N, 1 / SR)
HI, ALL = (f >= 3000) & (f <= 7500), (f >= 150) & (f <= 7500)
uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
summary = {}
for u in [u for u in uploads if len(sys.argv) < 3 or u["section"] in sys.argv[2:]]:
    d = next(iter(REPO.glob(f"output/*_{u['id']}")))
    x, sr = sf.read(d / "audio" / f"{u['id']}_16k.wav", dtype="float32")
    _, _, _, _, _, sound = fep.levels(d)
    n = (len(x) - N) // HOP
    hi, al = np.empty(n, np.float32), np.empty(n, np.float32)
    win = np.hanning(N).astype(np.float32)
    for b0 in range(0, n, 20000):                    # in blocks: the whole STFT at once took ~2 GB of RAM
        b1 = min(n, b0 + 20000)
        idx = np.arange(N)[None, :] + HOP * np.arange(b0, b1)[:, None]
        spec = np.abs(np.fft.rfft(x[idx] * win, axis=1)) ** 2
        hi[b0:b1] = 10 * np.log10(spec[:, HI].mean(axis=1) + 1e-12)
        al[b0:b1] = 10 * np.log10(spec[:, ALL].mean(axis=1) + 1e-12)
        del idx, spec
    pause = ~sound[:n] if len(sound) >= n else np.r_[~sound, np.zeros(n - len(sound), bool)]
    w = int(WIN * 100)
    rows = []
    for k in range(0, n - w // 2, w):
        p = pause[k:k + w]
        if p.sum() >= 50:                                       # at least 0.5 s of pause in the window
            rows.append((k / 100, float(np.median(hi[k:k + w][p])), float(np.median(al[k:k + w][p]))))
    if not rows:
        continue
    t, h, a = map(np.array, zip(*rows))
    base_h, base_a = np.percentile(h, 20), np.percentile(a, 20)
    bad = h > base_h + 8
    st = []
    for i in np.flatnonzero(bad):
        if st and t[i] - st[-1][1] <= WIN:
            st[-1][1] = t[i] + WIN
            st[-1][2] = max(st[-1][2], h[i] - base_h)
        else:
            st.append([t[i], t[i] + WIN, h[i] - base_h])
    share = bad.mean()
    summary[u["section"]] = {"base_hi": round(base_h, 1), "share_noisy": round(float(share), 3),
                             "stretches": [[round(a_, 0), round(b_, 0), round(c_, 1)] for a_, b_, c_ in st]}
    desc = ", ".join(f"{int(a_ // 60)}:{int(a_ % 60):02d}-{int(b_ // 60)}:{int(b_ % 60):02d} +{c_:.0f}dB" for a_, b_, c_ in st[:8])
    print(f"{u['section']:7} pause hi-band base {base_h:6.1f} dB, all-band {base_a:6.1f} dB; "
          f"noisy windows {share * 100:4.1f}%  {desc}{' ...' if len(st) > 8 else ''}", flush=True)
(Path(sys.argv[1])).write_text(json.dumps(summary, indent=1), encoding="utf-8")
