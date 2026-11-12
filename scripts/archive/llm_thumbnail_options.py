"""Thumbnail options for the new Large Language Models series, first lesson [01] Tokenization.

The user (2026-10-28) picked the strawberry hook from the deck (fig/tok_strawberry_question.pdf:
"How many r's in strawberry?" as GPT-4o tokens, " strawberry" = one token, 101830) and asked
for "a bit more fun", in a new template for the LLM series, to choose from. This renders the
hook drawn by hand (token boxes, a marker circle, the famous wrong answer "2"), in the three
styles kept on 2026-09-26 (thumbnail_style_options.py: bignumber, notebook, highlighter) plus
two new ones (chat, xray), and a contact sheet.

Usage:
  python scripts/non_essential/llm_thumbnail_options.py
Runtime: ~20 s (guess; the log reports the actual time).
Output: thumbnails/llm_options/<option>.png and overview.png
"""
import io
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_thumbnails_final as base  # noqa: E402
import thumbnail_style_options as so  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont  # noqa: E402

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(LOG_DIR / "llm_thumbnail_options.log", encoding="utf-8")])
log = logging.getLogger("llm_thumbnail_options")

OUT = base.OUT_DIR / "llm_options"
RED, BLUE, ORANGE, CHARCOAL = so.RED, so.BLUE, so.ORANGE, so.CHARCOAL
MONO = {"family": "DejaVu Sans Mono"}
TOKENS = [("How", 5299), ("␣many", 1991), ("␣r", 428), ("'s", 885), ("␣in", 306),
          ("␣strawberry", 101830), ("?", 30)]
FILLS = ["#F8D4DA", "#D0D9EF", "#FBE7B7"]
LESSON = {"tag": "LLM 01", "title": "Tokenization", "title_latin": True, "bar_color": RED,
          "out": "LLM01.png"}


# ---------- drawing helpers (data units = pixels of the illustration canvas) ----------

def emoji(char, px):
    """A colour emoji as an RGBA image (PIL + Segoe UI Emoji; matplotlib draws it black)."""
    font = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", px)
    im = Image.new("RGBA", (int(px * 1.6), int(px * 1.6)), (255, 255, 255, 0))
    ImageDraw.Draw(im).text((im.width // 2, im.height // 2), char, font=font,
                            embedded_color=True, anchor="mm")
    box = im.getbbox()
    if box is None:
        raise ValueError(f"emoji {char!r} rendered empty")
    return im.crop(box)


def put_image(ax, im, cx, cy, h):
    w = h * im.width / im.height
    ax.imshow(np.asarray(im), extent=(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2), zorder=5)


def text_w(ax, s, size, **kw):
    t = ax.text(0, 0, s, fontsize=size, **kw)
    bb = t.get_window_extent(ax.figure.canvas.get_renderer())
    t.remove()
    inv = ax.transData.inverted()
    (x0, _), (x1, _) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
    return x1 - x0


def token_row(ax, x, y, size, ids=True, ink=CHARCOAL, id_ink="#7a7a7a", gap=22, hot_ink=RED,
              hot_pad=0, id_drop=0.9):
    """Draw TOKENS as coloured boxes from (x, y = box bottom); returns each box's (x0, x1, y0, y1).
    Widths come from one monospace advance times the length: measuring each token's own text
    came out short for the ␣ glyph and the boxes overlapped. hot_pad adds space on both sides of
    the circled token, id_drop sets how far below the boxes the IDs sit (in font sizes)."""
    ax.figure.canvas.draw()
    h = size * 2.1
    adv = text_w(ax, "M" * 10, size, **MONO) / 10
    boxes = []
    for i, (tok, tid) in enumerate(TOKENS):
        w = adv * len(tok) + size * 1.0
        hot = tok == "␣strawberry"
        if hot:
            x += hot_pad
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={size * 0.35}",
                                    facecolor=FILLS[i % 3], edgecolor=RED if hot else "#9a9a9a",
                                    lw=4 if hot else 1.5, zorder=3))
        ax.text(x + w / 2, y + h / 2, tok, fontsize=size, ha="center", va="center", color=ink,
                zorder=4, **MONO)
        if ids:
            ax.text(x + w / 2, y - size * id_drop, str(tid), fontsize=size * 0.78, ha="center", va="top",
                    color=hot_ink if hot else id_ink, fontweight="bold" if hot else "normal", zorder=4, **MONO)
        boxes.append((x, x + w, y, y + h))
        x += w + gap + (hot_pad if hot else 0)
    return boxes


def marker_circle(ax, box, color=RED, lw=5, grow=1.0, sx=0.56, sy=0.95):
    x0, x1, y0, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * sx * grow, (y1 - y0) * sy * grow
    t = np.linspace(0, 2.2 * np.pi, 240) + 0.4
    g = 1 + 0.07 * (t - t[0]) / (2.2 * np.pi)
    wob = 1 + 0.035 * np.sin(3 * t + 1.0)
    ax.plot(cx + rx * g * wob * np.cos(t), cy + ry * g * wob * np.sin(t), color=color, lw=lw,
            solid_capstyle="round", zorder=6)


def bubble(ax, x, y, w, h, text, size, face, ink, tail="left", font=None, edge="none"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h * 0.35}",
                                facecolor=face, edgecolor=edge, lw=2, zorder=3))
    tx = x + h * 0.5 if tail == "left" else x + w - h * 0.5
    sgn = -1 if tail == "left" else 1
    ax.add_patch(Polygon([(tx - 18, y + 4), (tx + 18, y + 4), (tx + sgn * 34, y - 26)],
                         closed=True, facecolor=face, edgecolor="none", zorder=3))
    ax.text(x + w / 2, y + h / 2, text, fontsize=size, ha="center", va="center", color=ink,
            zorder=4, **(font or {"family": "DejaVu Sans"}))


def canvas(w=1600, h=520, face="white"):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=150)
    fig.patch.set_facecolor(face)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_facecolor(face)
    return fig, ax


def to_image(fig, face="white"):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    img = Image.open(buf).convert("RGB")
    box = ImageChops.difference(img, Image.new("RGB", img.size, face)).getbbox()
    if box is None:
        raise ValueError("illustration rendered empty")
    pad = 14
    return img.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                     min(img.width, box[2] + pad), min(img.height, box[3] + pad)))


# ---------- illustrations ----------

def illo_hook():
    """The token row, the strawberry token circled, a robot answering "There are 2 r's." """
    fig, ax = canvas(1700, 600)
    boxes = token_row(ax, 30, 300, 36)
    marker_circle(ax, boxes[5])
    sx = (boxes[5][0] + boxes[5][1]) / 2
    ax.text(sx + 40, 520, "one token!", fontsize=36, color=RED, ha="center",
            fontname=base.TAG_FONT, rotation=4, zorder=6)
    put_image(ax, emoji("\U0001F916", 300), 1560, 120, 190)          # robot
    bubble(ax, 760, 60, 640, 130, "There are 2 r's.", 40, "#EEF1F6", CHARCOAL, tail="right",
           edge="#c9cfdb")
    return to_image(fig)


def illo_xray():
    """What the model sees: the word with its 3 r's -> one box, 101830."""
    fig, ax = canvas(1600, 520)
    put_image(ax, emoji("\U0001F353", 300), 150, 270, 230)           # strawberry
    word = "strawberry"
    x = 300
    for ch in word:
        ax.text(x, 330, ch, fontsize=60, color=RED if ch == "r" else CHARCOAL, va="center",
                fontweight="bold", **MONO)
        x += text_w(ax, ch, 60, **MONO)
    ax.text((300 + x) / 2, 200, "you: 3 r's", fontsize=30, color=CHARCOAL, ha="center",
            fontname=base.TAG_FONT)
    ax.annotate("", xy=(1080, 300), xytext=(960, 300),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=6, mutation_scale=40))
    ax.add_patch(FancyBboxPatch((1110, 245), 440, 115, boxstyle="round,pad=0,rounding_size=30",
                                facecolor="#FBE7B7", edgecolor=RED, lw=5, zorder=3))
    ax.text(1330, 302, "101830", fontsize=52, ha="center", va="center", color=RED,
            fontweight="bold", zorder=4, **MONO)
    ax.text(1330, 200, "the model: one token", fontsize=30, color=CHARCOAL, ha="center",
            fontname=base.TAG_FONT)
    return to_image(fig)


def illo_notebook():
    """For the notebook card: the row, a circle, and the answer scribbled in the margin."""
    fig, ax = canvas(1700, 480)
    boxes = token_row(ax, 30, 240, 36)
    marker_circle(ax, boxes[5])
    ax.text(70, 70, "Q: how many r's?", fontsize=44, color=BLUE, fontname=base.TAG_FONT)
    ax.text(880, 70, "model: 2", fontsize=44, color=RED, fontname=base.TAG_FONT)
    put_image(ax, emoji("\U0001F926", 300), 1420, 100, 150)          # facepalm
    return to_image(fig)


# ---------- the two new styles (full canvas) ----------

def style_chat(fig, lesson, img=None):
    """A chat screen: the user asks, the model fails, the tokens explain why."""
    fig.patch.set_facecolor("#F3F5F9")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1280)
    ax.set_ylim(0, 720)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 18, 720, facecolor=RED, edgecolor="none"))
    ax.text(56, 670, lesson["tag"], fontsize=34, color=base.TAG_COLOR, va="top", fontname=base.TAG_FONT)
    ax.text(56, 610, lesson["title"], fontsize=68, color=CHARCOAL, va="top", **so.LATIN)
    bubble(ax, 590, 405, 620, 92, "How many r's in strawberry?", 28, BLUE, "white", tail="right")
    bubble(ax, 70, 285, 600, 92, "There are 2 r's in strawberry.", 28, "white", CHARCOAL,
           tail="left", edge="#c9cfdb")
    put_image(ax, emoji("\U0001F353", 200), 715, 331, 76)
    fig.canvas.draw()
    boxes = token_row(ax, 70, 95, 24, gap=14)
    marker_circle(ax, boxes[5], lw=4)
    ax.text(70, 215, "what it saw:", fontsize=26, color=RED, ha="left", fontname=base.TAG_FONT)


def style_xray(fig, lesson, img):
    """Dark page, white title, a big orange number: the 'what the model sees' view."""
    fig.patch.set_facecolor("#0f1a2e")
    for i, c in enumerate([RED, BLUE, ORANGE]):
        fig.add_artist(Rectangle((i / 3, 0.982), 1 / 3, 0.018, transform=fig.transFigure,
                                 facecolor=c, edgecolor="none"))
    fig.text(0.035, 0.955, "01", va="top", fontsize=150, color=ORANGE, **so.LATIN)
    fig.text(0.24, 0.90, lesson["title"], va="top", fontsize=78, color="white", **so.LATIN)
    fig.text(0.245, 0.745, "Large Language Models", va="top", fontsize=26, color="#9fb3d9",
             fontname=base.TAG_FONT)
    card = Image.new("RGB", (img.width + 60, img.height + 60), "white")
    card.paste(img, (30, 30))
    so.place(fig, card, (0.05, 0.04, 0.90, 0.56))


# ---------- round 2 (2026-10-28): option 2's content on white, one-line header, big picture ----------
# The user: "i like 2 and face palm is genius, maybe iterate on that face palm a bit more but i dont
# really like the background, i dont like the LLM 01's font as well also this way each thumbnail will
# get small area for the image".

def robot_facepalm(px=420):
    """The robot emoji with a raised hand over its face: a robot facepalm, composed in PIL."""
    robot = emoji("\U0001F916", px)
    hand = emoji("\U0001F91A", int(px * 0.62)).rotate(28, expand=True, resample=Image.BICUBIC)
    out = Image.new("RGBA", (robot.width + hand.width // 3, robot.height + hand.height // 6), (0, 0, 0, 0))
    out.alpha_composite(robot, (0, out.height - robot.height))
    out.alpha_composite(hand, (int(robot.width * 0.34), int(out.height - robot.height * 0.98)))
    return out


def header(ax, badge=True, title_size=78):
    """One line: a red 'LLM 01' badge (or a big red '01') and the title; returns the header's bottom y."""
    ax.add_patch(Rectangle((0, 0), 16, 720, facecolor=RED, edgecolor="none"))
    if badge:
        ax.text(48, 642, "LLM 01", fontsize=34, color="white", va="center", ha="left", zorder=5,
                bbox=dict(boxstyle="round,pad=0.38,rounding_size=0.6", facecolor=RED, edgecolor="none"),
                **so.LATIN)
        ax.figure.canvas.draw()
        x = 48 + text_w(ax, "LLM 01", 34, **so.LATIN) + 52
    else:
        ax.text(40, 642, "01", fontsize=110, color=RED, va="center", ha="left", **so.LATIN)
        ax.figure.canvas.draw()
        x = 40 + text_w(ax, "01", 110, **so.LATIN) + 30
    ax.text(x, 642, "Tokenization", fontsize=title_size, color=CHARCOAL, va="center", ha="left",
            **so.LATIN)
    return 560


def full_axes(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1280)
    ax.set_ylim(0, 720)
    ax.axis("off")
    return ax


TOK_SIZE, TOK_Y = 33, 425          # the row spans the frame (~1180 px) right under the header


def v_facepalm_big(fig, lesson, img=None, badge=True):
    """Option 2 on white: tokens, the two scribbles, and a big facepalm."""
    ax = full_axes(fig)
    header(ax, badge=badge)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16)
    marker_circle(ax, boxes[5])
    ax.text(60, 255, "Q: how many r's?", fontsize=46, color=BLUE, fontname=base.TAG_FONT)
    ax.text(60, 110, "model: 2", fontsize=60, color=RED, fontname=base.TAG_FONT)
    put_image(ax, emoji("\U0001F926", 400), 1050, 175, 330)


def v_robot_facepalm(fig, lesson, img=None):
    """The robot answers '2 r's' and facepalms at itself."""
    ax = full_axes(fig)
    header(ax)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16)
    marker_circle(ax, boxes[5])
    ax.text(60, 262, "Q: how many r's?", fontsize=46, color=BLUE, fontname=base.TAG_FONT)
    bubble(ax, 60, 70, 600, 120, "There are 2 r's.", 42, "#EEF1F6", CHARCOAL, tail="right",
           edge="#c9cfdb")
    put_image(ax, robot_facepalm(), 975, 175, 330)


def v_robot_scribble(fig, lesson, img=None):
    """Option 2's scribbles with the robot facepalming instead of the person."""
    ax = full_axes(fig)
    header(ax)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16)
    marker_circle(ax, boxes[5])
    ax.text(60, 255, "Q: how many r's?", fontsize=46, color=BLUE, fontname=base.TAG_FONT)
    ax.text(60, 110, "model: 2", fontsize=60, color=RED, fontname=base.TAG_FONT)
    put_image(ax, robot_facepalm(), 975, 175, 330)


def v_strawberry_vs_model(fig, lesson, img=None):
    """You count 3 r's, the model sees one token and says 2: facepalm."""
    ax = full_axes(fig)
    header(ax, badge=False)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16)
    marker_circle(ax, boxes[5])
    put_image(ax, emoji("\U0001F353", 300), 120, 180, 200)
    ax.text(250, 255, "you: 3 r's", fontsize=46, color=BLUE, fontname=base.TAG_FONT)
    ax.text(250, 110, "model: 2", fontsize=60, color=RED, fontname=base.TAG_FONT)
    put_image(ax, emoji("\U0001F926", 400), 1050, 175, 330)


def v_facepalm_card(fig, lesson, img):
    """The same on white, but the picture on the tilted taped card of option 2."""
    ax = full_axes(fig)
    header(ax)
    card = so._taped_card(img, angle=-2.0)
    so.place(fig, card, (0.03, 0.01, 0.95, 0.76))


# ---------- round 3: r2_a with the badge top right, no side bar, other colours, backgrounds ----------
# The user: "i like the first one, but maybe put the card for lesson number on top right and also no
# need to the vertical line and we dont have to use red, pls iterate on background a bit more as well".
# Red stays only where it means "wrong" (the circle round the token, "model: 2").

def bg_image(kind):
    """A 1280x720 background as an RGB array."""
    w, h = 1280, 720
    if kind == "cream":
        return np.full((h, w, 3), (255, 247, 236), np.uint8)
    if kind == "sky":                                   # pale blue at the top fading to white
        t = np.linspace(0, 1, h)[:, None, None]
        top, bottom = np.array([226, 235, 250]), np.array([255, 255, 255])
        return np.broadcast_to(top * (1 - t) + bottom * t, (h, w, 3)).astype(np.uint8)
    if kind == "blobs":                                 # soft blurred pastel shapes in the corners
        im = Image.new("RGB", (w, h), (252, 252, 255))
        d = ImageDraw.Draw(im)
        d.ellipse([900, -220, 1500, 330], fill=(255, 226, 179))
        d.ellipse([-260, 420, 420, 1000], fill=(214, 225, 250))
        d.ellipse([620, 520, 1060, 900], fill=(250, 214, 220))
        return np.asarray(im.filter(ImageFilter.GaussianBlur(90)))
    if kind == "ids":                                   # faint rows of token IDs: the model's view
        im = Image.new("RGB", (w, h), (255, 255, 255))
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype("consola.ttf", 22)
        rng = np.random.default_rng(509)
        for row, y in enumerate(range(8, h, 34)):
            x = -40 * (row % 3)
            while x < w:
                s = str(int(rng.integers(10, 199999)))
                d.text((x, y), s, font=f, fill=(241, 243, 247))
                x += d.textlength(s + "  ", font=f)
        return np.asarray(im)
    if kind == "dark":
        return np.full((h, w, 3), (15, 26, 46), np.uint8)
    if kind == "white":
        return np.full((h, w, 3), 255, np.uint8)
    raise ValueError(f"unknown background {kind!r}")


def v_round3(fig, bg, badge_face, badge_ink="white"):
    dark = bg == "dark"
    ax = full_axes(fig)
    ax.imshow(bg_image(bg), extent=(0, 1280, 0, 720), zorder=-10, aspect="auto")
    ink = "white" if dark else CHARCOAL
    ax.text(48, 642, "Tokenization", fontsize=80, color=ink, va="center", ha="left", **so.LATIN)
    ax.text(1236, 642, "LLM 01", fontsize=34, color=badge_ink, va="center", ha="right", zorder=5,
            bbox=dict(boxstyle="round,pad=0.38,rounding_size=0.6", facecolor=badge_face,
                      edgecolor="none"), **so.LATIN)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16, id_ink="#b8c3d9" if dark else "#7a7a7a", hot_ink="#ff8a96" if dark else RED)
    marker_circle(ax, boxes[5], color="#ff4d5e" if dark else RED)
    ax.text(60, 255, "Q: how many r's?", fontsize=46, color="#9fc0ff" if dark else BLUE,
            fontname=base.TAG_FONT)
    ax.text(60, 110, "model: 2", fontsize=60, color="#ff4d5e" if dark else RED, fontname=base.TAG_FONT)
    put_image(ax, emoji("\U0001F926", 400), 1050, 175, 330)


ROUND3 = [("r3_1_cream_blue", "cream", BLUE, "white"),
          ("r3_2_sky_orange", "sky", ORANGE, CHARCOAL),
          ("r3_3_blobs_blue", "blobs", BLUE, "white"),
          ("r3_4_ids_charcoal", "ids", CHARCOAL, "white"),
          ("r3_5_white_orange", "white", ORANGE, CHARCOAL),
          ("r3_6_dark_orange", "dark", ORANGE, CHARCOAL)]


# ---------- round 4: r3_1 (cream, blue badge) with emojis for "Q:" and "model:" ----------
# The user: "i like the first one. perhaps change Q and model to emojis though". The robot always
# answers; the asker is the open choice. The circle is flatter, the IDs sit lower and the circled
# token gets room on both sides: in round 3 the circle cut through "101830" and clipped "?".
# Then: "llm 01 is not centered within the card also maybe use green instead of blue".

GREEN = "#1E8449"


def badge(ax, x1, cy, text, size, face, ink="white", padx=20, pady=24):
    """A rounded card ending at x1, with the text centred on its ink. A text bbox centres the line
    box (ascent + descent), so "LLM 01", which has no descenders, sat high in the card."""
    prop = FontProperties(family=so.LATIN["fontfamily"], weight=so.LATIN["fontweight"])
    ext = TextPath((0, 0), text, size=size * ax.figure.dpi / 72, prop=prop).get_extents()
    w, h = ext.width + 2 * padx, ext.height + 2 * pady
    ax.add_patch(FancyBboxPatch((x1 - w, cy - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h * 0.28}",
                                facecolor=face, edgecolor="none", zorder=5))
    ax.text(x1 - w + padx - ext.x0, cy - ext.height / 2 - ext.y0, text, fontsize=size, color=ink,
            va="baseline", ha="left", zorder=6, **so.LATIN)


MEME = base.OUT_DIR / "assets" / "llm01_picard_facepalm.jpg"   # knowyourmeme.com, 895x503


def picard_card():
    """The Picard facepalm meme, cropped to him, on the tilted taped card of the notebook style.
    The user: "feel free to source images fom the web as well, perhaps change he face palm with the meme"."""
    im = Image.open(MEME).convert("RGB")
    return so._taped_card(im.crop((140, 0, im.width, im.height)), angle=-3.0)


def v_round4(fig, asker, meme=True):
    ax = full_axes(fig)
    ax.imshow(bg_image("cream"), extent=(0, 1280, 0, 720), zorder=-10, aspect="auto")
    ax.text(48, 642, "Tokenization", fontsize=80, color=CHARCOAL, va="center", ha="left", **so.LATIN)
    badge(ax, 1250, 642, "LLM 01", 34, GREEN)
    boxes = token_row(ax, 42, TOK_Y, TOK_SIZE, gap=16, hot_pad=36, id_drop=1.25)
    marker_circle(ax, boxes[5], sx=0.62, sy=0.85)
    put_image(ax, emoji(asker, 300), 100, 280, 82)
    ax.text(160, 255, "how many r's?", fontsize=46, color=GREEN, fontname=base.TAG_FONT)
    put_image(ax, emoji("\U0001F916", 300), 104, 140, 96)          # robot
    ax.text(175, 100, "2", fontsize=80, color=RED, fontname=base.TAG_FONT)
    if meme:
        put_image(ax, picard_card(), 1010, 178, 330)
    else:
        put_image(ax, emoji("\U0001F926", 400), 1050, 175, 330)    # facepalm


ROUND4 = [("r4_a_raised_hand_picard", "\U0001F64B", True),
          ("r4_b_person_picard", "\U0001F9D1", True),
          ("r4_c_nerd_picard", "\U0001F913", True),
          ("r4_a_raised_hand", "\U0001F64B", False)]


def render(name, fn, img):
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("white")
    fn(fig, LESSON, img)
    out = OUT / f"{name}.png"
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    return out


def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    rnd = sys.argv[1] if len(sys.argv) > 1 else "2"
    if rnd == "1":
        hook, xray, note = illo_hook(), illo_xray(), illo_notebook()
        options = [("1_bignumber_hook", so.style_bignumber, hook),
                   ("2_notebook_scribble", so.style_notebook, note),
                   ("3_highlighter_xray", so.style_highlighter, xray),
                   ("4_chat", style_chat, None),
                   ("5_xray_dark", style_xray, hook),
                   ("6_bignumber_xray", so.style_bignumber, xray)]
        sheet_name = "overview.png"
    elif rnd == "3":
        options = [(name, (lambda fig, lesson, img, b=bg, f=face, k=ink: v_round3(fig, b, f, k)), None)
                   for name, bg, face, ink in ROUND3]
        sheet_name = "overview_round3.png"
    elif rnd == "4":
        options = [(name, (lambda fig, lesson, img, a=asker, m=meme: v_round4(fig, a, m)), None)
                   for name, asker, meme in ROUND4]
        sheet_name = "overview_round4.png"
    else:
        options = [("r2_a_facepalm_big", v_facepalm_big, None),
                   ("r2_b_robot_facepalm", v_robot_facepalm, None),
                   ("r2_c_you_vs_model", v_strawberry_vs_model, None),
                   ("r2_e_robot_scribble", v_robot_scribble, None)]
        sheet_name = "overview_round2.png"
    outs = []
    for i, (name, fn, img) in enumerate(options, 1):
        outs.append(render(name, fn, img))
        log.info(f"{i}/{len(options)} {name}, {time.time() - t0:.0f}s elapsed")
    cw, ch, gut = 640, 360, 18
    font = ImageFont.truetype("arial.ttf", 24)
    rows = -(-len(outs) // 2)
    sheet = Image.new("RGB", (2 * cw + 3 * gut, rows * (ch + 40) + gut), "white")
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(outs):
        x, y = gut + (i % 2) * (cw + gut), gut + (i // 2) * (ch + 40)
        draw.text((x, y), p.stem, fill="black", font=font)
        cell = Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS)
        sheet.paste(cell, (x, y + 30))
        draw.rectangle([x - 1, y + 29, x + cw, y + 30 + ch], outline="#bbbbbb")
    sheet.save(OUT / sheet_name)
    log.info(f"Wrote {OUT / sheet_name}; done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
