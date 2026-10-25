"""Caption words inside the user's non-silent new cuts (and the changed edges) of Դաս 16 and 15, plus the speech
level there: what did the user cut that the silence detector calls sound? ~20 s per lecture. Repo root."""
import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import find_edit_points as fep  # noqa: E402

fit = json.loads((Path(__file__).parent / "user_pause_fit.json").read_text(encoding="utf-8"))
EXTRA = {"16": [("1:41:51.8", 16.0), ("0:13:47.9", 2.0), ("0:01:18.9", 4.6)],
         "15": []}
for n in ["16", "15"]:
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    vid = d.name.split("_", 2)[2]
    words = fep.caption_words((d / f"{vid}.hy.vtt").read_text(encoding="utf-8"))
    _, x, db, floor, thr, sound = fep.levels(d)
    print(f"\n=== Das {n}: floor {floor:.1f} dB, threshold {thr:.1f} dB")
    for label, spans in (("NOT SILENT", fit[n]["new_not_silence_even_at_1s"]), ("EDGE", EXTRA[n])):
        for start, length in sorted(spans, key=lambda s: fep.parse_t(s[0])):
            s = fep.parse_t(start)
            e = s + length
            w = " ".join(t for ts, t in words if s - 0.3 <= ts < e)
            seg = db[int(s * 100):int(e * 100)]
            snd = sound[int(s * 100):int(e * 100)]
            print(f"{label:10s} {start} +{length:5.2f} s | sound {100 * snd.mean():3.0f}% of frames, "
                  f"median {np.median(seg) - floor:+.0f} dB over floor | words: {w[:110] or '(none)'}")
