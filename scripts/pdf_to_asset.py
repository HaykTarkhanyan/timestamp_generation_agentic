"""Rasterize a single-page PDF figure into a trimmed PNG thumbnail asset.

Course lecture figures live as vector PDFs in the reference repo's per-chapter
`fig/` folders (e.g. ml/05_interpretability/fig/*.pdf). To embed one in a
thumbnail (via make_thumbnails_final.py's _draw_image_row), it must first be a
tightly-cropped PNG on a white background. This script does that:

  1. render page 1 at high DPI (PyMuPDF),
  2. optionally crop a fraction off any edge (to drop a figure title / legend),
  3. trim the surrounding white margin so the figure fills the frame.

Fails loudly: a missing input, an empty page, or an all-white result raises.

Usage:
  python scripts/pdf_to_asset.py <in.pdf> <out.png> [--dpi 300]
      [--crop-top F] [--crop-bottom F] [--crop-left F] [--crop-right F]
      [--pad PX] [--bg 0-255]

Example (drop the tree figure's title band, then trim):
  python scripts/pdf_to_asset.py \
      ../01_python_math_ml_course/ml/05_interpretability/fig/tree_bike.pdf \
      thumbnails/assets/ml22_tree.png --dpi 300 --crop-top 0.13
"""
import argparse
import logging
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "pdf_to_asset.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


def rasterize(pdf_path: Path, dpi: int):
    """Render page 1 of the PDF to a PIL RGB image at the given DPI."""
    import fitz  # PyMuPDF
    from PIL import Image

    doc = fitz.open(str(pdf_path))
    if doc.page_count < 1:
        raise ValueError(f"PDF has no pages: {pdf_path}")
    if doc.page_count > 1:
        log.warning(f"{pdf_path.name} has {doc.page_count} pages; using page 1 only")
    pix = doc[0].get_pixmap(dpi=dpi, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    log.info(f"Rendered {pdf_path.name} at {dpi} dpi -> {img.width}x{img.height}px")
    return img


def crop_fractions(img, top, bottom, left, right):
    """Crop the given fraction off each edge (e.g. top=0.13 drops the top 13%)."""
    if not all(0 <= f < 1 for f in (top, bottom, left, right)):
        raise ValueError("crop fractions must be in [0, 1)")
    if top + bottom >= 1 or left + right >= 1:
        raise ValueError("crop fractions leave nothing behind")
    w, h = img.size
    box = (int(left * w), int(top * h), int(w - right * w), int(h - bottom * h))
    return img.crop(box)


def trim_white(img, bg: int, pad: int):
    """Trim the uniform-background border, then re-pad by `pad` px on each side."""
    from PIL import Image, ImageChops

    bg_img = Image.new("RGB", img.size, (bg, bg, bg))
    bbox = ImageChops.difference(img, bg_img).getbbox()
    if bbox is None:
        raise ValueError("image is entirely background - nothing to trim (bad crop?)")
    left, top, right, bottom = bbox
    w, h = img.size
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w, right + pad)
    bottom = min(h, bottom + pad)
    return img.crop((left, top, right, bottom))


def main():
    ap = argparse.ArgumentParser(description="Rasterize a PDF figure to a trimmed PNG asset.")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--crop-top", type=float, default=0.0)
    ap.add_argument("--crop-bottom", type=float, default=0.0)
    ap.add_argument("--crop-left", type=float, default=0.0)
    ap.add_argument("--crop-right", type=float, default=0.0)
    ap.add_argument("--pad", type=int, default=8, help="white padding (px) re-added after trim")
    ap.add_argument("--bg", type=int, default=255, help="background gray level to trim (0-255)")
    args = ap.parse_args()

    if not args.pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {args.pdf}")

    img = rasterize(args.pdf, args.dpi)
    img = crop_fractions(img, args.crop_top, args.crop_bottom, args.crop_left, args.crop_right)
    img = trim_white(img, args.bg, args.pad)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(args.out))
    log.info(f"Wrote {args.out} ({img.width}x{img.height}px)")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log.error(f"Failed: {exc}", exc_info=True)
        sys.exit(1)
