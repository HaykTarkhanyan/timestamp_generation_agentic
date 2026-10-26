"""Where is Vahagn's webcam on screen? Writes <piece>/camera_on.json, which find_edit_points.py reads: every cut
touching a camera stretch becomes an unticked suggestion, since a cut makes him jump (the user, 2026-10-26, after
removing 70 of 75 planned cuts on 6 May: "see when hes on screen during the lecture ... then make all the cuts
unticked").

    python scripts/non_essential/vahagn_camera_on.py 23.4 24.1 ...      # then rerun the analysis of those pieces

How: his webcam is a box in the top-right corner (full res x 1136-1361, y 0-125) with black bars on both sides;
without it that corner is Acrobat's light-grey toolbar. Once a second, from the 360p preview, the left bar strip's
mean luminance: dark (under 100) = camera on. Measured 2026-10-26 on all 25 pieces: 21.1-23.1.a never (bar ~219),
23.1.b-28.4 on throughout (bar 0-52) except 28.3.a 18:08-18:38 and the first second of 24.2.a (bar ~220, the
toolbar visible: checked on a frame). The picture inside the box is no use as a signal: when he moves or the light
changes it runs from 42 to 192. Seconds on are joined across gaps of up to 2 s and widened by 1 s each side.
Write it only for pieces not yet reviewed: a changed plan no longer matches a list reviewed against the old one.
Expected: ~10 s per piece.
"""
import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
X0, W, H = 532, 106, 58          # the box in the 640x360 preview (even sizes: the source is 4:2:0)
BAR = (slice(5, 55), slice(2, 11))
DARK = 100
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_camera_on.log", encoding="utf-8")])
log = logging.getLogger(__name__)


def camera_seconds(preview: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(preview), "-vf", f"fps=1,crop={W}:{H}:{X0}:0",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32).mean(axis=3)
    return y[:, BAR[0], BAR[1]].mean(axis=(1, 2)) < DARK


def intervals(on: np.ndarray, duration: float) -> list[list[float]]:
    e = np.flatnonzero(np.diff(np.r_[0, on.astype(np.int8), 0]))
    runs = [[float(a), float(b)] for a, b in zip(e[::2], e[1::2])]
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= 2:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    return [[max(0.0, a - 1), min(duration, b + 1)] for a, b in merged]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="+")
    args = ap.parse_args()
    uploads = {u["section"]: u["id"] for u in
               json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))}
    for s in args.sections:
        vid = uploads[s]
        d = next(iter(REPO.glob(f"output/*_{vid}")))
        if (d / "studio_cuts_to_enter.txt").exists():
            raise SystemExit(f"{s} is already reviewed: a camera file would change its plan under the reviewed list")
        duration = json.loads((d / "edit_points.json").read_text(encoding="utf-8"))["duration"]
        on = camera_seconds(d / "video" / f"{vid}_360p.mp4")
        iv = intervals(on, duration)
        off = [[round(b, 1), round(a2, 1)] for (_, b), (a2, _) in zip(iv, iv[1:])]
        (d / "camera_on.json").write_text(json.dumps({
            "intervals": iv, "share_on": round(float(on.mean()), 3), "seconds": int(len(on)),
            "method": f"left black bar of the webcam box darker than {DARK} in the 360p preview, once a second "
                      "(scripts/non_essential/vahagn_camera_on.py)"}, indent=1), encoding="utf-8")
        log.info(f"{s}: camera on {on.mean() * 100:.1f}% of {len(on)} s, {len(iv)} stretch(es)"
                 + (f"; off between {off}" if off else "") + f" -> {d.name}/camera_on.json")


if __name__ == "__main__":
    main()
