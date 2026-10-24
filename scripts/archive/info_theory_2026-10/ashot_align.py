"""Find where a camera recording sits inside a separate audio recording: 1-second loudness envelopes of both
(ffmpeg decode to 8 kHz mono, streamed in chunks so a 17 h file never sits in RAM), then the offset with the
best correlation of the zero-mean log envelopes. Also prints the loudness per minute around the camera's end,
to see where the speech in the long recording stops. ~1-3 min for the 17 h file, single core.

    python ashot_align.py <long_audio> <camera_video> [label]
Writes <scratchpad>/ashot_align_<label>.json.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

SR = 8000


def envelope(path: str) -> np.ndarray:
    """dB loudness per second."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         stdout=subprocess.PIPE)
    out, buf = [], b""
    while True:
        chunk = p.stdout.read(SR * 2 * 600)  # 10 min at a time
        if not chunk:
            break
        buf += chunk
        n = len(buf) // (SR * 2)
        if n:
            a = np.frombuffer(buf[: n * SR * 2], dtype=np.int16).astype(np.float32).reshape(n, SR)
            out.append(10 * np.log10(np.mean(a * a, axis=1) + 1.0))
            buf = buf[n * SR * 2:]
    if p.wait():
        raise RuntimeError(f"ffmpeg failed on {path}")
    return np.concatenate(out)


t0 = time.time()
long_path, cam_path = sys.argv[1], sys.argv[2]
label = sys.argv[3] if len(sys.argv) > 3 else "x"
L = envelope(long_path)
C = envelope(cam_path)
print(f"long {len(L) / 3600:.2f} h, camera {len(C) / 60:.1f} min, decoded in {time.time() - t0:.0f} s", flush=True)
c = C - C.mean()
best = (-1e18, 0)
for off in range(0, len(L) - len(C) + 1):
    seg = L[off: off + len(C)]
    s = float(np.dot(seg - seg.mean(), c))
    if s > best[0]:
        best = (s, off)
off = best[1]
seg = L[off: off + len(C)]
r = float(np.corrcoef(seg, C)[0, 1])
tail = [round(float(L[m * 60: m * 60 + 60].mean()), 1) for m in range((off + len(C)) // 60 - 3, min(len(L) // 60, (off + len(C)) // 60 + 20))]
res = {"long": long_path, "camera": cam_path, "offset_s": off, "corr": round(r, 3), "long_s": len(L), "camera_s": len(C),
       "camera_end_in_long_s": off + len(C), "minute_db_from_3min_before_camera_end": tail}
Path(__file__).with_name(f"ashot_align_{label}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
print(f"done in {time.time() - t0:.0f} s")
