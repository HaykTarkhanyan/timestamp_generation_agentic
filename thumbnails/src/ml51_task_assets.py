"""ML 51 thumbnail panels at full resolution: detection, segmentation and classification on the
course's pomegranate photo, with the exact overlays of ml/12_cnn/py_src/task_zoo.py (its boxes,
scores and segmentation mask are imported, not copied). fig/task_zoo.pdf embeds the photo at
low resolution, so the big detection panel came out pixelated when cropped from it (2026-10-14).

    python thumbnails/src/ml51_task_assets.py      # ~5 s, writes thumbnails/assets/ml51_task_{det,seg,cls}.png
"""
import logging
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
COURSE_SRC = Path(r"C:\Users\hayk_\OneDrive\Desktop\01_python_math_ml_course\ml\12_cnn\py_src")
OUT = ROOT / "thumbnails" / "assets"
Path(ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(ROOT / "logs" / "ml51_task_assets.log", encoding="utf-8")])
log = logging.getLogger(__name__)

sys.path.insert(0, str(COURSE_SRC))
import task_zoo as tz  # noqa: E402  (the figure's own overlay data)


def panel(img, name, width_px, draw):
    """Save the photo filling a width_px-wide PNG (aspect kept), with `draw(ax, s)` overlays;
    s scales font sizes and line widths with the panel width."""
    h, w = img.shape[:2]
    dpi = 100
    fig = plt.figure(figsize=(width_px / dpi, width_px * h / w / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, interpolation="lanczos")
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    draw(ax, width_px / 1200)
    fig.savefig(OUT / name, dpi=dpi)
    plt.close(fig)
    log.info(f"wrote {OUT / name}")


def chip(ax, x, y, text, fc, size, va="top", ha="left"):
    ax.text(x, y, text, fontsize=size, fontweight="bold", color="white", va=va, ha=ha,
            bbox=dict(boxstyle="square,pad=0.3", fc=fc, ec="none"))


def main():
    t0 = time.time()
    img = plt.imread(tz.PHOTO)
    h, w = img.shape[:2]
    if (w, h) != (1920, 1280):
        raise ValueError(f"task_zoo's overlays are placed for 1920x1280, got {w}x{h}")

    def det(ax, s):
        for (x0, y0, x1, y1), sc in zip(tz.FRUIT_BOXES, tz.DET_SCORES):
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, ec=tz.ARM_ORANGE, lw=7 * s))
            low = sc == 0.90                    # its label sat on top of 0.62's in the deck figure
            ax.text(x0 + 14, (y1 - 18) if low else (y0 + 18), f"{sc:.2f}", fontsize=34 * s, fontweight="bold",
                    color="black", va="bottom" if low else "top",
                    bbox=dict(boxstyle="square,pad=0.2", fc=tz.ARM_ORANGE, ec="none"))

    def seg(ax, s):
        chip(ax, 40, 50, "fruit", tz.ARM_ORANGE, 62 * s)
        chip(ax, 1880, 50, "background", "#1e2a6e", 62 * s, ha="right")   # top: the thumbnail tag sits bottom-left

    def cls(ax, s):
        chip(ax, 40, 50, '"pomegranates"', tz.ARM_BLUE, 66 * s)

    panel(img, "ml51_task_det.png", 1200, det)
    panel(tz.build_semantic_overlay(img), "ml51_task_seg.png", 900, seg)
    panel(img, "ml51_task_cls.png", 900, cls)
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
