"""Split a multi-panel course figure into one PNG per panel.

Many lecture figures are a single PDF holding a row of sub-plots (e.g.
dr_eigengarments.pdf = mean garment + PC1..PC6). Thumbnails want each panel as
its own asset so make_thumbnails_final.py's _draw_image_row can size them,
space them, and caption them individually.

Guessing crop fractions by eye is fiddly and gets it wrong by a few pixels, so
this finds the panel boundaries instead: after optionally dropping a title band
off the top, it scans for columns that are entirely (near-)white - the gutters
between panels - and treats each run of non-white columns as one panel. Each
panel is then row-trimmed the same way and written out.

Some figures have no perfectly empty gutter: a stray marker or an axis
whisker leaves a handful of pixels in the column that is otherwise the
split (the Google PAIR mammoth has exactly 2-3). --gutter-tol allows that
many ink pixels in a column and still calls it a gutter.

Fails loudly: a missing input, a title crop that eats the whole image, or a scan
that finds no panels raises.

Usage:
  python scripts/non_essential/split_figure_panels.py <figure> <out-prefix> \
      [--dpi 300] [--crop-top F] [--crop-bottom F] [--keep 1,2,3] \
      [--white 250] [--gutter-tol 0] [--min-width-frac 0.02] [--pad 6]

Example (first three panels of the eigen-garments row, titles dropped):
  python scripts/non_essential/split_figure_panels.py \
      ../01_python_math_ml_course/ml/10_dimensionality_reduction/fig/dr_eigengarments.pdf \
      thumbnails/assets/ml36_eigen --dpi 300 --crop-top 0.16 --keep 1,2,3
"""
import argparse
import logging
import sys
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
from PIL import Image

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "split_figure_panels.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def render(src: Path, dpi: int) -> np.ndarray:
    """Load the figure as RGB. Vector figures are rasterized at --dpi; borrowed
    assets that are already raster (fig/borrowed/**) are read as-is, since there
    is no resolution to choose - upscaling them would only invent pixels."""
    if src.suffix.lower() in RASTER_SUFFIXES:
        arr = np.asarray(Image.open(src).convert("RGB"))
        log.info(f"Loaded raster {src.name} -> {arr.shape[1]}x{arr.shape[0]}px")
        return arr
    doc = fitz.open(str(src))
    if doc.page_count == 0:
        raise ValueError(f"{src} has no pages")
    pix = doc.load_page(0).get_pixmap(dpi=dpi, alpha=False)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
    log.info(f"Rendered {src.name} at {dpi} dpi -> {pix.width}x{pix.height}px")
    return arr.copy()


def runs_of_content(mask: np.ndarray, min_len: int) -> list[tuple[int, int]]:
    """Contiguous [start, end) spans where mask is True, ignoring short ones."""
    spans, start = [], None
    for i, on in enumerate(mask):
        if on and start is None:
            start = i
        elif not on and start is not None:
            if i - start >= min_len:
                spans.append((start, i))
            start = None
    if start is not None and len(mask) - start >= min_len:
        spans.append((start, len(mask)))
    return spans


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("figure", type=Path, help="figure PDF, or an already-raster PNG/JPG/WEBP")
    p.add_argument("out_prefix", help="e.g. thumbnails/assets/ml36_eigen -> _1.png, _2.png")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--crop-top", type=float, default=0.0)
    p.add_argument("--crop-bottom", type=float, default=0.0)
    p.add_argument("--keep", default="", help="1-based panel indices, e.g. 1,2,3")
    p.add_argument("--white", type=int, default=250, help="pixels >= this count as white")
    p.add_argument("--gutter-tol", type=int, default=0,
                   help="a column with at most this many ink pixels is still a gutter")
    p.add_argument("--min-width-frac", type=float, default=0.02)
    p.add_argument("--pad", type=int, default=6, help="white border added back per panel")
    a = p.parse_args()

    if not a.figure.exists():
        raise FileNotFoundError(a.figure)

    img = render(a.figure, a.dpi)
    h, w, _ = img.shape
    top, bot = int(h * a.crop_top), h - int(h * a.crop_bottom)
    if bot - top < 10:
        raise ValueError(f"crop-top/{a.crop_top} + crop-bottom/{a.crop_bottom} left nothing")
    img = img[top:bot]
    log.info(f"After title crop: {img.shape[1]}x{img.shape[0]}px")

    ink = img.min(axis=2) < a.white                    # any dark-ish channel = content
    col_has_ink = ink.sum(axis=0) > a.gutter_tol   # tol 0 -> any ink at all
    spans = runs_of_content(col_has_ink, max(1, int(w * a.min_width_frac)))
    if not spans:
        raise ValueError("no panels found - is the figure blank, or --white too low?")
    log.info(f"Found {len(spans)} panel(s): {spans}")

    keep = [int(k) for k in a.keep.split(",") if k.strip()] if a.keep else range(1, len(spans) + 1)
    for n in keep:
        if not 1 <= n <= len(spans):
            raise ValueError(f"--keep {n} out of range (found {len(spans)} panels)")
        x0, x1 = spans[n - 1]
        panel = img[:, x0:x1]
        rows = (panel.min(axis=2) < a.white).any(axis=1)  # row-trim this panel
        ys = np.flatnonzero(rows)
        panel = panel[ys[0]:ys[-1] + 1]
        if a.pad:
            panel = np.pad(panel, ((a.pad, a.pad), (a.pad, a.pad), (0, 0)),
                           mode="constant", constant_values=255)
        out = Path(f"{a.out_prefix}_{n}.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(panel).save(out)
        log.info(f"Wrote {out} ({panel.shape[1]}x{panel.shape[0]}px)")


if __name__ == "__main__":
    main()
