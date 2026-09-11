"""Render the ML39 photo map: each demo photo drawn at its own UMAP position.

The lesson-39 practical clusters 92 personal photos by CLIP embedding, and its
payoff is an interactive Plotly map - but that map draws coloured DOTS and only
reveals the photo on hover, so a screenshot of it is mostly white space. A
thumbnail wants the thing the hover implies: the actual photos sitting where the
embedding puts them, khachkars in one corner and khorovats in another.

Nothing is recomputed or synthesised. The coordinates and the thumbnails are
read straight out of the practical's own generated map (out/demo_photos_map_*.html),
so the layout here is pixel-for-pixel the projection shown on screen - the
figure only swaps each dot for the photo it already stood for. Reading the HTML
also avoids installing umap-learn (and its numba/llvmlite chain) into this repo
just to reproduce a projection that had already been computed.

Fails loudly: a missing map, a newPlot call it cannot parse, or a trace without
thumbnails raises.

Usage:
  python scripts/non_essential/photo_scatter_ml39.py [--map umap|pca]
      [--out PATH] [--zoom F] [--dpi N]
"""
import argparse
import base64
import io
import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
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
        logging.FileHandler(LOG_DIR / "photo_scatter_ml39.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

COURSE = Path(r"C:\Users\hayk_\OneDrive\Desktop\01_python_math_ml_course\ml"
              r"\10_dimensionality_reduction\out")


def read_traces(html: Path) -> list[dict]:
    """Pull the trace list out of the page's Plotly.newPlot(...) call.

    The plotly.js bundle mentions newPlot in its own error strings, so take the
    LAST occurrence - that is the call the page actually makes - and let the
    JSON decoder find the end of the array rather than bracket-matching by hand
    (the traces contain base64 strings full of stray brackets)."""
    s = html.read_text(encoding="utf-8", errors="replace")
    i = s.rfind("Plotly.newPlot")
    if i < 0:
        raise ValueError(f"{html} has no Plotly.newPlot call")
    start = s.find("[", i)
    if start < 0:
        raise ValueError(f"{html}: no data array after newPlot")
    traces, _ = json.JSONDecoder().raw_decode(s, start)
    log.info(f"Parsed {len(traces)} traces from {html.name}")
    return traces


def decode_axis(v) -> np.ndarray:
    """Plotly writes numeric arrays either as a plain list or, for compactness,
    as {"dtype": "f8", "bdata": "<base64>"} - a raw little-endian buffer. The
    dtype codes are numpy's own, so frombuffer takes them as-is."""
    if isinstance(v, dict):
        return np.frombuffer(base64.b64decode(v["bdata"]), dtype=np.dtype(v["dtype"]))
    return np.asarray(v, dtype=float)


def decode_thumb(data_uri: str) -> Image.Image:
    b64 = data_uri.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--map", choices=["umap", "pca"], default="umap")
    p.add_argument("--out", type=Path, default=Path("thumbnails/assets/ml39_photo_map.png"))
    p.add_argument("--zoom", type=float, default=0.62, help="thumbnail scale on the axes")
    p.add_argument("--dpi", type=int, default=200)
    # Photos are drawn at a fixed pixel zoom, so the axes shape stretches only
    # their POSITIONS - widening it fits the projection to a 16:9 thumbnail band
    # without distorting any image.
    p.add_argument("--figsize", type=float, nargs=2, default=(14.0, 7.0),
                   metavar=("W", "H"), help="axes shape; wider spreads the layout")
    a = p.parse_args()

    html = COURSE / f"demo_photos_map_{a.map}.html"
    if not html.exists():
        raise FileNotFoundError(html)

    xs, ys, thumbs = [], [], []
    for tr in read_traces(html):
        cd = tr.get("customdata")
        if not cd:
            raise ValueError(f"trace {tr.get('name')!r} has no customdata thumbnails")
        tx, ty = decode_axis(tr["x"]), decode_axis(tr["y"])
        if not len(tx) == len(ty) == len(cd):
            raise ValueError(f"trace {tr.get('name')!r}: x/y/customdata lengths "
                             f"{len(tx)}/{len(ty)}/{len(cd)} disagree")
        for (x, y, row) in zip(tx, ty, cd):
            xs.append(x)
            ys.append(y)
            thumbs.append(decode_thumb(row[0]))
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    log.info(f"{len(thumbs)} photos, thumbnail size {thumbs[0].size}")

    fig, ax = plt.subplots(figsize=tuple(a.figsize), dpi=a.dpi)
    for x, y, im in zip(xs, ys, thumbs):
        ax.add_artist(AnnotationBbox(OffsetImage(np.asarray(im), zoom=a.zoom),
                                     (x, y), frameon=False, pad=0.0))
    ax.set_xlim(xs.min() - 0.06 * np.ptp(xs), xs.max() + 0.06 * np.ptp(xs))
    ax.set_ylim(ys.min() - 0.06 * np.ptp(ys), ys.max() + 0.06 * np.ptp(ys))
    ax.axis("off")
    fig.patch.set_facecolor("white")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.out, bbox_inches="tight", pad_inches=0.02, facecolor="white")
    plt.close(fig)
    w, h = Image.open(a.out).size
    log.info(f"Wrote {a.out} ({w}x{h}px)")


if __name__ == "__main__":
    main()
