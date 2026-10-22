"""Build text-free background plates for the three umath thumbnail templates (~10 s).

The series titles stay baked in (they never change). The lesson-number line and the topic area
are cleaned: flat white for ANT and linear algebra. For Metric, each pixel there is the mean of
the references that have no text (plus a 6 px margin for JPEG ringing) at it; what is text in all
five (the shared "Դաս 1") is filled by harmonic inpainting (Laplace, scipy), and the red axis line
is redrawn through the filled area from its own intact stretches.
Run: python scripts/non_essential/build_umath_plates.py
Writes thumbnails/umath/templates/<series>_plate.png from thumbnails/umath/reference/*.jpg.
"""
import logging
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

REPO = Path(__file__).resolve().parents[2]
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/build_umath_plates.log", encoding="utf-8")])
log = logging.getLogger(__name__)
REF = REPO / "thumbnails/umath/reference"
OUT = REPO / "thumbnails/umath/templates"
OUT.mkdir(parents=True, exist_ok=True)


def load(pattern: str) -> np.ndarray:
    files = sorted(REF.glob(pattern))
    if not files:
        raise FileNotFoundError(pattern)
    log.info(f"{pattern}: {[f.name for f in files]}")
    return np.stack([np.array(Image.open(f).convert("RGB")).astype(float) for f in files])


def inpaint(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Harmonic fill of masked pixels from their unmasked neighbours, per channel."""
    out = img.copy()
    ys, xs = np.nonzero(mask)
    idx = -np.ones(mask.shape, int)
    idx[ys, xs] = np.arange(len(ys))
    n = len(ys)
    A = lil_matrix((n, n))
    B = np.zeros((n, 3))
    for k, (y, x) in enumerate(zip(ys, xs)):
        A[k, k] = 4
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = min(max(y + dy, 0), mask.shape[0] - 1), min(max(x + dx, 0), mask.shape[1] - 1)
            if mask[yy, xx]:
                A[k, idx[yy, xx]] -= 1
            else:
                B[k] += img[yy, xx]
    A = A.tocsr()
    for c in range(3):
        out[ys, xs, c] = spsolve(A, B[:, c])
    return out


# --- ANT: white plate left of the number band, title kept
ant = np.median(load("ant_das*.jpg"), axis=0)
ant[355:690, 85:925] = 255.0
Image.fromarray(np.clip(ant, 0, 255).astype(np.uint8)).save(OUT / "ant_plate.png")

# --- Linear algebra: white over the lesson line and the topic, title (blue, on the band) kept
la = np.median(load("linalg_das*.jpg"), axis=0)
la[55:275, 280:1250] = 255.0
la[355:448, 95:470] = 255.0
Image.fromarray(np.clip(la, 0, 255).astype(np.uint8)).save(OUT / "linalg_plate.png")

# --- Metric: median of 5, then inpaint what is still bright in the lesson line + topic area
stack = load("metric_das*.jpg")
mt = np.median(stack, axis=0)
region = np.zeros(mt.shape[:2], bool)
region[385:465, 60:790] = True
region[490:670, 60:790] = True
# per reference: its own text (bright) plus a margin that covers the JPEG ringing around it;
# each pixel is the mean of the references that have no text there
lum_stack = stack @ np.array([0.299, 0.587, 0.114])
text = np.stack([ndimage.binary_dilation(l > 100, iterations=6) for l in lum_stack]) & region
clean = ~text
count = clean.sum(0)
mean = (stack * clean[..., None]).sum(0) / np.maximum(count, 1)[..., None]
mt[region & (count > 0)] = mean[region & (count > 0)]
log.info(f"metric: pixels with no text-free reference: {(region & (count == 0)).sum()}")
# covered in every reference (the shared "Դաս 1"): inpaint, with a small margin
mask = ndimage.binary_dilation(region & (count == 0), iterations=2) & region
log.info(f"metric: inpainting {mask.sum()} pixels")
mt = inpaint(mt, mask)

# the red axis line is straight: fit it on clean pixels, then redraw it through the filled area by
# copying pixels from an intact stretch of the same line (shifted along its direction)
r, g = mt[..., 0], mt[..., 1]
red = (r - g > 25) & (r > 75) & ~mask
red[:240] = False
red[:, 790:] = False
ys, xs = np.nonzero(red)
a, b = np.polyfit(xs, ys, 1)
d = np.array([1.0, a]) / np.hypot(1.0, a)  # unit direction (dx, dy)
log.info(f"metric: red line y = {a:.4f} x + {b:.1f} from {len(xs)} pixels")
fixed = 0
for y, x in zip(*np.nonzero(mask)):
    if abs(y - (a * x + b)) / np.hypot(1.0, a) > 4:
        continue
    for s in range(6, 260, 3):
        for sign in (1, -1):
            xx, yy = int(round(x + sign * s * d[0])), int(round(y + sign * s * d[1]))
            if 0 <= yy < mask.shape[0] and 0 <= xx < mask.shape[1] and not mask[yy, xx]:
                mt[y, x] = mt[yy, xx]
                fixed += 1
                break
        else:
            continue
        break
log.info(f"metric: red line pixels restored: {fixed}")
Image.fromarray(np.clip(mt, 0, 255).astype(np.uint8)).save(OUT / "metric_plate.png")
log.info(f"plates written to {OUT}")
