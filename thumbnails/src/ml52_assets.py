"""ML 52 thumbnail assets from the Gesture Snake practical itself: one of the instructor's real
"left" crops, the exported model's real probabilities on it, and a board drawn by the game's own
draw_board (ml/12_cnn/52_gesture_snake/play_snake.py, imported, not copied).

The crop is the SHARPEST (variance of the Laplacian) of the "left" crops the model classifies as
"left" with confidence >= MIN_CONF, so the bars are a real output of the big CNN with augmentation
(gesture_model_bigcnn.pt2) - a chosen example, not a typical one. The most confident crop was
motion-blurred and hard to read as a thumb (2026-10-16). The board state (snake shape, food,
score) is set by hand; only the drawing is the game's.

The published ML52.png came from gesture_model.pt2 as it was on 2026-10-16 22:40, the 2.5 MB big
CNN (2,574,783 bytes, the size of gesture_model_bigcnn.pt2). The notebook was re-run at 22:52 and
gesture_model.pt2 became the 45 MB fine-tuned ResNet, so the bigcnn file is named explicitly. The
folder was renamed gesture_snake -> 52_gesture_snake on 2026-10-17.

The system Python's OpenCV does not load against its numpy, so run it in a throwaway env with
the practical's own pins (52_gesture_snake/requirements.txt):

    uv run --no-project --python 3.11 --with opencv-python==4.11.0.86 --with numpy==1.26.4 \
        --with torch==2.9.0 --with pillow==11.3.0 python thumbnails/src/ml52_assets.py
    # ~80 s (torch import + 100 crops on CPU); the first run also downloads torch (~3 min)
"""
import json
import logging
import sys
import time
from collections import deque
from pathlib import Path

import cv2
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
GAME = Path(r"C:\Users\hayk_\OneDrive\Desktop\01_python_math_ml_course\ml\12_cnn\52_gesture_snake")
MODEL = "gesture_model_bigcnn.pt2"
OUT = ROOT / "thumbnails" / "assets"
Path(ROOT / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(ROOT / "logs" / "ml52_assets.log", encoding="utf-8")])
log = logging.getLogger(__name__)

sys.path.insert(0, str(GAME))
import gesture_common as gc  # noqa: E402
import play_snake as ps      # noqa: E402

CROP_PX = 512   # the 128 px crop, upscaled for the thumbnail panel
MIN_CONF = 0.8


def sharpness(bgr):
    return float(cv2.Laplacian(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())


def best_left_crop(model):
    files = sorted((GAME / "gesture_data" / "hayk" / "left").glob("*.jpg"))
    if not files:
        raise FileNotFoundError(f"no crops in {GAME / 'gesture_data' / 'hayk' / 'left'}")
    good = []
    for f in files:
        img = gc.imread_u(f)
        label, conf, probs = ps.predict(model, img)
        if label == "left" and conf >= MIN_CONF:
            good.append((sharpness(img), f, conf, probs))
    if not good:
        raise ValueError(f"the model calls none of the {len(files)} 'left' crops 'left' with "
                         f"confidence >= {MIN_CONF}")
    s, f, conf, probs = max(good, key=lambda g: g[0])
    log.info(f"{len(files)} left crops, {len(good)} correct with conf >= {MIN_CONF}; sharpest: "
             f"{f.name} (Laplacian variance {s:.0f}, median of those {sorted(g[0] for g in good)[len(good) // 2]:.0f}, "
             f"conf {conf:.3f})")
    return f, conf, probs


def board_png():
    game = ps.Snake()
    # tail ... head: a long snake winding up the board, its head on row 4 heading left for the food
    path = ([(14, c) for c in range(1, 15)] + [(r, 14) for r in range(13, 10, -1)]
            + [(11, c) for c in range(13, 3, -1)] + [(r, 4) for r in range(10, 6, -1)]
            + [(7, c) for c in range(5, 12)] + [(r, 11) for r in range(6, 3, -1)]
            + [(4, c) for c in range(10, 6, -1)])
    if len(set(path)) != len(path):
        raise ValueError("the hand-set snake crosses itself")
    game.body = deque(path)
    game.heading = game.moved = "left"
    game.food, game.score = (4, 2), len(path) - 3
    rgb = cv2.cvtColor(ps.draw_board(game), cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).save(OUT / "ml52_board.png")
    log.info(f"wrote {OUT / 'ml52_board.png'} ({rgb.shape[1]}x{rgb.shape[0]}), head {game.body[-1]}, "
             f"food {game.food}, cell {ps.CELL} px")
    return {"head": game.body[-1], "food": game.food, "cell": ps.CELL, "grid": ps.GRID}


def main():
    t0 = time.time()
    model = ps.load_model(GAME / MODEL)
    f, conf, probs = best_left_crop(model)
    rgb = cv2.cvtColor(gc.imread_u(f), cv2.COLOR_BGR2RGB)
    Image.fromarray(rgb).resize((CROP_PX, CROP_PX), Image.LANCZOS).save(OUT / "ml52_thumb_left.png")
    board = board_png()
    meta = {"crop": f.name, "classes": list(gc.CLASSES), "probs": [round(float(p), 4) for p in probs],
            "model": MODEL, "board": board}
    (OUT / "ml52_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    log.info(f"probs {dict(zip(gc.CLASSES, meta['probs']))}")
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
