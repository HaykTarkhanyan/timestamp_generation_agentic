"""Render alternative thumbnail STYLES side by side, for the user to pick from.

The locked design in make_thumbnails_final.py (side stripe, handwritten tag,
title, illustration band at the bottom) stays the production one. On 2026-09-26
the user asked for a few fresh stylings to look at for FUTURE lectures, with no
change to anything already published. This renders each candidate style on a
handful of finished lessons of different shapes and writes a contact sheet with
today's design as the first row.

Styles the user kept (see STYLES at the bottom):
  bignumber    - white, the lesson number huge and solid as the tag, tricolour top edge
  notebook     - graph paper with a red margin, figure as a tilted taped card
  highlighter  - white, title under a highlighter stroke, marker circle round the tag
Tried and dropped on 2026-09-26 (code in git history, commit 5e1c976): split,
banner, dark (round 1); sticky, stamp, jupyter (round 2).

The Latin title font is LATIN below, so thumbnail_font_options.py can swap it.

Every lesson's illustration is rendered ONCE off-screen by its own draw
function at the production canvas size, trimmed, and then placed as an image,
so any draw function works in any style without being rewritten.

Usage:
  python scripts/non_essential/thumbnail_style_options.py [ML16 ML44 ...]
Runtime: ~15 s for the default 4 lessons x 3 styles (measured value is logged).
Output: thumbnails/style_options/<style>_<MLNN>.png and overview.png
"""
import io
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import make_thumbnails_final as base  # noqa: E402  (fonts, LESSONS, draw functions)

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont  # noqa: E402

# base already configured the root logger (into its own log file), so this
# script gets a dedicated, non-propagating logger with its own file.
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log = logging.getLogger("thumbnail_style_options")
log.propagate = False
log.setLevel(logging.INFO)
for handler in (logging.StreamHandler(sys.stderr),
                logging.FileHandler(LOG_DIR / "thumbnail_style_options.log", encoding="utf-8")):
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(handler)

OUT = base.OUT_DIR / "style_options"
DEFAULT_LESSONS = ["ML16", "ML36", "ML44", "ML46"]
K = 720 / 1280                         # figure-fraction x per unit of y
RED, BLUE, ORANGE = base.DL_BAR, base.UNSUP_BAR, base.BAR
CHARCOAL = base.TITLE_COLOR
LATIN = dict(base.LATIN_FONTKW)        # Latin title font; reassigned by thumbnail_font_options.py


# ---------- lesson helpers ----------

def lesson_by_name(name):
    for lesson in base.LESSONS:
        if lesson["out"] == f"{name}.png":
            return lesson
    raise KeyError(f"No lesson in make_thumbnails_final.LESSONS renders {name}.png")


def block_color(lesson):
    return lesson.get("bar_color", base.BAR)


def text_on(color):
    """White text reads on red and navy; orange needs charcoal."""
    return CHARCOAL if color == ORANGE else "white"


def illustration(lesson):
    """The lesson's own illustration, drawn off-screen and trimmed to content."""
    fig = plt.figure(figsize=(12.8, 7.2), dpi=200)
    fig.patch.set_facecolor("white")
    lesson["draw"](fig, lesson.get("chart_bbox", base.CHART_BBOX))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor="white")
    plt.close(fig)
    img = Image.open(buf).convert("RGB")
    box = ImageChops.difference(img, Image.new("RGB", img.size, "white")).getbbox()
    if box is None:
        raise ValueError(f"{lesson['out']}: draw function produced an empty image")
    pad = 12
    box = (max(0, box[0] - pad), max(0, box[1] - pad),
           min(img.width, box[2] + pad), min(img.height, box[3] + pad))
    return img.crop(box)


def place(fig, img, region, zorder=2):
    """Fit an image inside region = (x0, y0, w, h) in figure fractions, centred,
    aspect kept. Returns the box it actually occupies."""
    x0, y0, w, h = region
    a = img.width / img.height
    fh = min(h, w / (a * K))
    fw = fh * a * K
    box = (x0 + (w - fw) / 2, y0 + (h - fh) / 2, fw, fh)
    ax = fig.add_axes(box, zorder=zorder)
    ax.imshow(np.asarray(img))
    ax.axis("off")
    return box


# ---------- title: tokens, wrapping, drawing ----------

def title_tokens(lesson):
    """The title as (word, fontkw) tokens, whatever form the config uses."""
    if lesson.get("title_segments"):
        segs = lesson["title_segments"]
    elif lesson.get("title_latin"):
        segs = [(lesson["title"], "latin")]
    else:
        segs = [(lesson["title"], "arm")]
    tokens = []
    for text, kind in segs:
        kw = (dict(LATIN) if kind == "latin"
              else {"fontproperties": base.ARM_PROPS, "fontweight": "bold"})
        tokens += [(word, kw) for word in text.replace("\n", " ").split()]
    return tokens


def _width(fig, text, size, kw):
    t = fig.text(0, 0, text, fontsize=size, **kw)
    w = t.get_window_extent(fig.canvas.get_renderer()).width
    t.remove()
    return w / fig.bbox.width


def _wrap(fig, tokens, size, max_w):
    lines, cur, cur_w = [], [], 0.0
    for word, kw in tokens:
        ww = _width(fig, word + " ", size, kw)
        if cur and cur_w + ww > max_w:
            lines.append(cur)
            cur, cur_w = [], 0.0
        cur.append((word, kw))
        cur_w += ww
    lines.append(cur)
    widest = max(sum(_width(fig, w + " ", size, kw) for w, kw in line) for line in lines)
    return lines, widest


def fit_title(fig, lesson, max_w, max_lines, max_size, min_size, one_line_min=50):
    """One line if it fits at one_line_min pt or more (a wrapped title eats the
    figure's height); otherwise the largest size (stepping down by 2 pt) whose
    wrap fits max_lines and max_w."""
    fig.canvas.draw()
    tokens = title_tokens(lesson)
    for size in range(max_size, one_line_min - 1, -2):
        lines, widest = _wrap(fig, tokens, size, max_w)
        if len(lines) == 1 and widest <= max_w:
            return size, lines
    for size in range(max_size, min_size - 1, -2):
        lines, widest = _wrap(fig, tokens, size, max_w)
        if len(lines) <= max_lines and widest <= max_w:
            return size, lines
    raise ValueError(f"{lesson['out']}: title does not fit {max_lines} line(s) of "
                     f"width {max_w:.2f} even at {min_size} pt")


def draw_title(fig, lines, size, x0, y_top, color, boxes=None, **extra):
    """Draw wrapped lines top-down; returns the y of the block's bottom. If a
    list is passed as `boxes`, each line's (x0, x1, y_top, y_bottom) is appended."""
    renderer = fig.canvas.get_renderer()
    step = size * 1.12 * (100 / 72) / 720      # one line, in figure fractions
    y = y_top
    for line in lines:
        x = x0
        for i, (word, kw) in enumerate(line):
            text = word + (" " if i < len(line) - 1 else "")
            t = fig.text(x, y, text, fontsize=size, va="top", color=color, **kw, **extra)
            x += t.get_window_extent(renderer).width / fig.bbox.width
        if boxes is not None:
            boxes.append((x0, x, y, y - step))
        y -= step
    return y


def pill(fig, x, y, face, ink=None, ha="left", rotation=0, size=28):
    fig.text(x, y, "Գործնական", ha=ha, va="center", fontsize=size,
             fontproperties=base.ARM_PROPS, color=ink or text_on(face), rotation=rotation,
             bbox=dict(boxstyle="round,pad=0.45", facecolor=face, edgecolor="none"),
             zorder=5)


# ---------- styles ----------

def style_bignumber(fig, lesson, img):
    """The lesson number, huge and solid in the block colour, IS the tag; the
    title sits beside it. (A first version put the number faint behind the
    title, where it ran through the letters.)"""
    color = block_color(lesson)
    for i, c in enumerate([RED, BLUE, ORANGE]):
        fig.add_artist(Rectangle((i / 3, 0.982), 1 / 3, 0.018, transform=fig.transFigure,
                                 facecolor=c, edgecolor="none"))
    number, num_size = lesson["tag"].split()[-1], 150
    fig.text(0.035, 0.955, number, va="top", fontsize=num_size, color=color,
             **LATIN)
    fig.canvas.draw()
    x0 = 0.035 + _width(fig, number, num_size, LATIN) + 0.02
    num_bottom = 0.955 - num_size * (100 / 72) / 720
    size, lines = fit_title(fig, lesson, max_w=0.965 - x0, max_lines=2, max_size=66,
                            min_size=36, one_line_min=44)
    bottom = draw_title(fig, lines, size, x0, 0.90 if len(lines) == 1 else 0.93, CHARCOAL)
    if lesson.get("practical"):
        pill(fig, x0, bottom - 0.035, color)
        bottom -= 0.08
    place(fig, img, (0.04, 0.03, 0.92, min(bottom, num_bottom) - 0.04))


def _taped_card(img, angle=-2.5):
    """Illustration on a white card with a border, soft shadow and a strip of
    orange tape, tilted - as an RGBA image with transparent surroundings."""
    pad = int(0.025 * img.width)
    cw, ch = img.width + 2 * pad, img.height + 2 * pad
    m = int(0.03 * cw)
    canvas = Image.new("RGBA", (cw + 2 * m, ch + 2 * m), (0, 0, 0, 0))
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle([m + 12, m + 16, m + cw + 12, m + ch + 16], fill=(0, 0, 0, 80))
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(14)))
    card = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    card.paste(img, (pad, pad))
    ImageDraw.Draw(card).rectangle([0, 0, cw - 1, ch - 1], outline=(205, 205, 205, 255), width=3)
    canvas.alpha_composite(card, (m, m))
    tw, th = int(cw * 0.16), int(ch * 0.10)
    tape = Image.new("RGBA", (tw, th), (242, 168, 0, 150)).rotate(5, expand=True,
                                                                  resample=Image.BICUBIC)
    canvas.alpha_composite(tape, (m + cw // 2 - tape.width // 2, m - tape.height // 2))
    return canvas.rotate(angle, expand=True, resample=Image.BICUBIC)


def style_notebook(fig, lesson, img):
    fig.patch.set_facecolor("#fbf9f2")
    for x in np.arange(0, 1, 32 / 1280):
        fig.add_artist(Line2D([x, x], [0, 1], transform=fig.transFigure, color="#d9e6f2",
                              lw=1, zorder=-2))
    for y in np.arange(0, 1, 32 / 720):
        fig.add_artist(Line2D([0, 1], [y, y], transform=fig.transFigure, color="#d9e6f2",
                              lw=1, zorder=-2))
    fig.add_artist(Line2D([0.075, 0.075], [0, 1], transform=fig.transFigure, color="#e06666",
                          lw=2.5, zorder=-1))
    fig.text(0.10, 0.94, lesson["tag"], color=base.TAG_COLOR, fontsize=36, va="top",
             fontname=base.TAG_FONT)
    if lesson.get("practical"):
        pill(fig, 0.955, 0.90, block_color(lesson), ha="right", rotation=6)
    size, lines = fit_title(fig, lesson, max_w=0.86, max_lines=2, max_size=74, min_size=40)
    bottom = draw_title(fig, lines, size, 0.10, 0.83, CHARCOAL)
    place(fig, _taped_card(img), (0.10, 0.02, 0.86, bottom - 0.04))


def _hand_circle(fig, cx, cy, rx, ry, color):
    """A marker loop that overshoots its start, like a quick circle by hand."""
    t = np.linspace(0, 2.2 * np.pi, 240) + 0.4
    grow = 1 + 0.07 * (t - t[0]) / (2.2 * np.pi)            # spirals out a little
    wob = 1 + 0.035 * np.sin(3 * t + 1.0)
    fig.add_artist(Line2D(cx + rx * grow * wob * np.cos(t), cy + ry * grow * wob * np.sin(t),
                          transform=fig.transFigure, color=color, lw=3.5, alpha=0.9,
                          solid_capstyle="round", zorder=4))


def style_highlighter(fig, lesson, img):
    """Clean white page marked up by hand: the title under a highlighter
    stroke in the block colour, and a marker circle around the tag."""
    color = block_color(lesson)
    t = fig.text(0.06, 0.94, lesson["tag"], color=base.TAG_COLOR, fontsize=36, va="top",
                 fontname=base.TAG_FONT)
    fig.canvas.draw()
    bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
    _hand_circle(fig, (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2, bb.width * 0.68,
                 bb.height * 0.95, color)
    if lesson.get("practical"):
        pill(fig, 0.965, 0.915, color, ha="right")
    size, lines = fit_title(fig, lesson, max_w=0.88, max_lines=2, max_size=74, min_size=40)
    boxes = []
    bottom = draw_title(fig, lines, size, 0.06, 0.82, CHARCOAL, boxes=boxes)
    glyph_h = size * (100 / 72) / 720
    for x0, x1, top, _ in boxes:
        y = top - 0.62 * glyph_h
        fig.add_artist(Line2D([x0 - 0.012, x1 + 0.012], [y - 0.006, y + 0.004],
                              transform=fig.transFigure, color=color,
                              alpha=0.45 if color == ORANGE else 0.30, lw=size * 0.62,
                              solid_capstyle="butt", zorder=-1))
    place(fig, img, (0.04, 0.03, 0.92, bottom - 0.05))


STYLES = {"bignumber": style_bignumber, "notebook": style_notebook,
          "highlighter": style_highlighter}


# ---------- contact sheet ----------

def overview(names, path):
    """Rows: today's design, then each style. Columns: lessons."""
    cell_w, cell_h, gut, label_w, head_h = 480, 270, 16, 190, 44
    rows = ["current"] + list(STYLES)
    sheet = Image.new("RGB", (label_w + len(names) * (cell_w + gut),
                              head_h + len(rows) * (cell_h + gut)), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("arial.ttf", 26)
    for c, name in enumerate(names):
        draw.text((label_w + c * (cell_w + gut) + 6, 8), name, fill="black", font=font)
    for r, row in enumerate(rows):
        y = head_h + r * (cell_h + gut)
        draw.text((10, y + cell_h // 2 - 14), row, fill="black", font=font)
        for c, name in enumerate(names):
            src = base.OUT_DIR / f"{name}.png" if row == "current" else OUT / f"{row}_{name}.png"
            if not src.exists():
                raise FileNotFoundError(f"missing render for the overview: {src}")
            cell = Image.open(src).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS)
            sheet.paste(cell, (label_w + c * (cell_w + gut), y))
            draw.rectangle([label_w + c * (cell_w + gut) - 1, y - 1,
                            label_w + c * (cell_w + gut) + cell_w, y + cell_h], outline="#bbbbbb")
    sheet.save(path)
    log.info(f"Wrote {path} ({sheet.width}x{sheet.height}px)")


def main():
    t0 = time.time()
    names = sys.argv[1:] or DEFAULT_LESSONS
    OUT.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(names, 1):
        lesson = lesson_by_name(name)
        img = illustration(lesson)
        for style, fn in STYLES.items():
            fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
            fig.patch.set_facecolor("white")
            fn(fig, lesson, img)
            out = OUT / f"{style}_{name}.png"
            fig.savefig(out, facecolor=fig.get_facecolor())
            plt.close(fig)
        elapsed = time.time() - t0
        log.info(f"{i}/{len(names)} {name}: {len(STYLES)} styles, {elapsed:.0f}s elapsed, "
                 f"~{elapsed / i * (len(names) - i):.0f}s left")
    overview(names, OUT / "overview.png")
    log.info(f"Done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
