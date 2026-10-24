"""Check that render_lecture.py keeps the separate recorder in sync with the camera, without rendering any
picture: runs the script's own filter graph for the two audio tracks only (the recorder as it will be
published, and the camera's own sound put on the same timeline), over a window and through any cuts in it,
then cross-correlates them quarter by quarter. A wrong offset shows as a steady lag; a cut that shifts one
track shows as a jump between quarters.

Run:  python scripts/non_essential/render_sync_check.py --video <camera.MOV> --audio <recorder.mp3>
          --align <align.json> --window A B [--cuts <cut list> --cuts-fps 30] [--speed 1.0]
Expected wall-clock: ~5-10 s for a 2 min window (audio only).

Use --speed 1 (the default): after atempo the two tracks no longer line up sample by sample, so lags
scatter +-40 ms at 1.25x although the timeline is right. Measured on Դաս 7 (2026-10-24): at 1x the camera
sits +3 to +8 ms after the recorder in every quarter, with and without three cuts in the window.
"""
import argparse
import json
import logging
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/render_sync_check.log", encoding="utf-8")])
log = logging.getLogger(__name__)

# After the logging setup, so these modules' own basicConfig calls are no-ops
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import render_lecture as rl  # noqa: E402
from align_audio import SR, best_lag  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--video", type=Path, required=True)
    ap.add_argument("--audio", type=Path, required=True)
    ap.add_argument("--align", type=Path, required=True)
    ap.add_argument("--window", type=float, nargs=2, metavar=("A", "B"), required=True)
    ap.add_argument("--cuts", type=Path)
    ap.add_argument("--cuts-fps", type=int)
    ap.add_argument("--speed", type=float, default=1.0)
    args = ap.parse_args()

    t0 = time.time()
    al = json.loads(args.align.read_text(encoding="utf-8"))
    off, drift = al["offset0_s"], al["drift_ppm"] / 1e6
    v = next(s for s in rl.probe(args.video)["streams"] if s["codec_type"] == "video")
    src_fps = rl.rate(v["r_frame_rate"])
    step = (1 + drift) / src_fps
    cuts = rl.read_cuts(args.cuts, args.cuts_fps) if args.cuts else []
    a0, b0 = args.window
    segs = [(off + round((a - off) / step) * step, off + round((b - off) / step) * step)
            for a, b in rl.keep_segments(a0, b0, cuts)]
    cam_ss = max(0, int(((segs[0][0] - off) / (1 + drift) - 1.0) * src_fps)) / src_fps
    aud_ss = max(0, int((segs[0][0] - 1.0) * 1000)) / 1000
    opts = SimpleNamespace(npl=200, speed=args.speed, fps=25, window=args.window, gain_db=0.0, dip=0.0)
    graph = rl.build_graph(opts, v["r_frame_rate"], True, segs, off, drift, {"camera": 0, "audio": 1},
                           {0: cam_ss, 1: aud_ss})
    graph = ";\n".join(line for line in graph.split(";\n") if "[mv" not in line and "[camv]" not in line)
    span = b0 - a0 + 30

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "sync.mka"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cam_ss:.6f}", "-t", f"{span}", "-i", str(args.video),
                        "-ss", f"{aud_ss:.6f}", "-t", f"{span}", "-i", str(args.audio), "-filter_complex", graph,
                        "-map", "[ma]", "-map", "[ca]", "-c:a", "pcm_s16le", str(out)], check=True)

        def track(i: int) -> np.ndarray:
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-map", f"0:a:{i}", "-ac", "1",
                                "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
            x = np.frombuffer(r.stdout, dtype=np.float32)
            return x - x.mean()

        rec, cam = track(0), track(1)

    log.info(f"{len(segs)} segments ({len(cuts)} cuts in the list), recorder {len(rec) / SR:.1f} s, "
             f"camera {len(cam) / SR:.1f} s, speed {args.speed}")
    m, n = int(0.5 * SR), len(rec) // 4
    for q in range(4):
        a, b = q * n, (q + 1) * n
        k, peak, z = best_lag(cam[a + m:b - m], rec[a:b])
        # cam(t) = rec(t - D) puts cam[a + m:] at rec index a + m - D
        log.info(f"quarter {q + 1}: camera {(m - k) / SR * 1000:+.1f} ms after the recorder (peak {peak:.2f}, z {z:.0f})")
    log.info(f"done in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
