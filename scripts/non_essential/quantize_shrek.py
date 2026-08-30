"""Trim the white margins off shrek.webp and quantize it with k-means, exactly the way
the lesson-35 practical does, to build the ML35 thumbnail panels."""
import logging
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs/quantize_shrek.log", encoding="utf-8")],
)

SEED = 509
MAX_WIDTH = 420
SRC = Path(r"C:\Users\hayk_\OneDrive\Desktop\01_python_math_ml_course\ml\09_clustering\img\shrek.webp")
DST = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\thumbnails\assets")

img = Image.open(SRC).convert("RGB")
a = np.asarray(img)
logging.info("loaded %s (%dx%d)", SRC.name, a.shape[1], a.shape[0])

# --- strip the near-white margins (the user's ask: top/bottom, but do all sides) ---
non_white = ~(a > 244).all(axis=2)
rows = np.where(non_white.any(axis=1))[0]
cols = np.where(non_white.any(axis=0))[0]
a = a[rows[0] + 2:rows[-1] - 1, cols[0] + 2:cols[-1] - 1]  # +2px inset: the trim can leave a faint margin row
logging.info("trimmed margins: top=%d bottom=%d left=%d right=%d -> %dx%d",
             rows[0], non_white.shape[0] - 1 - rows[-1],
             cols[0], non_white.shape[1] - 1 - cols[-1], a.shape[1], a.shape[0])

uniq_full = len(np.unique(a.reshape(-1, 3), axis=0))
logging.info("unique colours in the trimmed original: %d", uniq_full)

# --- downscale for speed, keeping aspect ratio (as the notebook does) ---
im = Image.fromarray(a)
w, h = im.size
im = im.resize((MAX_WIDTH, int(h * MAX_WIDTH / w)), Image.LANCZOS)
arr = np.asarray(im)
pixels = arr.reshape(-1, 3).astype(np.float64) / 255.0
logging.info("working size %dx%d (%d pixels)", arr.shape[1], arr.shape[0], pixels.shape[0])

Image.fromarray(arr).save(DST / "ml35_shrek_original.png")

for k in (4, 32):
    km = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(pixels)
    out = (km.cluster_centers_[km.labels_].reshape(arr.shape) * 255).astype(np.uint8)
    Image.fromarray(out).save(DST / f"ml35_shrek_k{k}.png")
    logging.info("k=%2d  inertia=%.1f  -> ml35_shrek_k%d.png", k, km.inertia_, k)

logging.info("original unique colours = %d", uniq_full)
