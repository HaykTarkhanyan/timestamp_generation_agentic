"""Thumbnails for the Large Language Models series (DECISIONS #55).

The template: cream background, no side bar, the title top left in Comic Sans MS Bold, a green
"LLM NN" card top right, the lesson's hook drawn by hand below, and a meme or emoji for the
punchline. Red only marks what is wrong. Ported from scripts/archive/llm_thumbnail_options.py,
round 4 (r4_a), which made LLM01.png; this script redraws LLM01 pixel for pixel.

Each lesson is a config in LESSONS with a draw(ax) function on a 1280x720 canvas (data units =
pixels, y up). Candidate designs for a lesson that has no pick yet live in OPTIONS.

Usage:
  python scripts/make_llm_thumbnails.py                  # every lesson -> thumbnails/LLMNN.png
  python scripts/make_llm_thumbnails.py LLM01            # lessons whose output name contains LLM01
  python scripts/make_llm_thumbnails.py --options LLM02  # candidates -> thumbnails/llm_options/ + a contact sheet
Runtime: ~2 s per thumbnail.
"""
import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_thumbnails_final as base  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from matplotlib.textpath import TextPath  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(LOG_DIR / "make_llm_thumbnails.log", encoding="utf-8")])
log = logging.getLogger("make_llm_thumbnails")

OUT, OPT_OUT, ASSETS = base.OUT_DIR, base.OUT_DIR / "llm_options", base.OUT_DIR / "assets"
RED, GREEN, ORANGE, CHARCOAL = base.DL_BAR, "#1E8449", base.BAR, base.TITLE_COLOR
CREAM = (255, 247, 236)
LATIN = base.LATIN_FONTKW
HAND = {"fontname": base.TAG_FONT}            # handwriting (Segoe Script): Latin only
MONO = {"family": "DejaVu Sans Mono"}
FILLS = ["#F8D4DA", "#D0D9EF", "#FBE7B7"]


# ---------- helpers ----------

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


def token_row(ax, x, y, size, tokens, hot, gap=16, hot_pad=36, id_drop=1.25, ink=CHARCOAL,
              id_ink="#7a7a7a", font=MONO):
    """Draw (text, id) tokens as coloured boxes from (x, y = box bottom); returns each box's
    (x0, x1, y0, y1). Widths come from one monospace advance times the length (measuring each
    token's own text came out short for the ␣ glyph). The token at index `hot` gets a red edge,
    a bold red ID and hot_pad of room on both sides for the circle. id None = no ID line."""
    ax.figure.canvas.draw()
    h = size * 2.1
    adv = text_w(ax, "M" * 10, size, **MONO) / 10
    boxes = []
    for i, (tok, tid) in enumerate(tokens):
        w = adv * len(tok) + size * 1.0
        is_hot = i == hot
        if is_hot:
            x += hot_pad
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={size * 0.35}",
                                    facecolor=FILLS[i % 3], edgecolor=RED if is_hot else "#9a9a9a",
                                    lw=4 if is_hot else 1.5, zorder=3))
        ax.text(x + w / 2, y + h / 2, tok, fontsize=size, ha="center", va="center", color=ink,
                zorder=4, **font)
        if tid is not None:
            ax.text(x + w / 2, y - size * id_drop, str(tid), fontsize=size * 0.78, ha="center", va="top",
                    color=RED if is_hot else id_ink, fontweight="bold" if is_hot else "normal", zorder=4,
                    **MONO)
        boxes.append((x, x + w, y, y + h))
        x += w + gap + (hot_pad if is_hot else 0)
    return boxes


def marker_circle(ax, box, color=RED, lw=5, sx=0.62, sy=0.85):
    """A hand-drawn ellipse round a box: a slight overshoot and wobble, like a marker."""
    x0, x1, y0, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * sx, (y1 - y0) * sy
    t = np.linspace(0, 2.2 * np.pi, 240) + 0.4
    g = 1 + 0.07 * (t - t[0]) / (2.2 * np.pi)
    wob = 1 + 0.035 * np.sin(3 * t + 1.0)
    ax.plot(cx + rx * g * wob * np.cos(t), cy + ry * g * wob * np.sin(t), color=color, lw=lw,
            solid_capstyle="round", zorder=6)


def badge(ax, x1, cy, text, size, face, ink="white", padx=20, pady=24):
    """A rounded card ending at x1, with the text centred on its ink. A text bbox centres the line
    box (ascent + descent), so "LLM 01", which has no descenders, sat high in the card."""
    prop = FontProperties(family=LATIN["fontfamily"], weight=LATIN["fontweight"])
    ext = TextPath((0, 0), text, size=size * ax.figure.dpi / 72, prop=prop).get_extents()
    w, h = ext.width + 2 * padx, ext.height + 2 * pady
    ax.add_patch(FancyBboxPatch((x1 - w, cy - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={h * 0.28}",
                                facecolor=face, edgecolor="none", zorder=5))
    ax.text(x1 - w + padx - ext.x0, cy - ext.height / 2 - ext.y0, text, fontsize=size, color=ink,
            va="baseline", ha="left", zorder=6, **LATIN)
    return x1 - w, cy - h / 2


def taped_card(img, angle=-3.0):
    """A picture on a white card with a border, soft shadow and a strip of orange tape, tilted;
    RGBA with transparent surroundings (from thumbnail_style_options.py's notebook style)."""
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
    tape = Image.new("RGBA", (tw, th), (242, 168, 0, 150)).rotate(5, expand=True, resample=Image.BICUBIC)
    canvas.alpha_composite(tape, (m + cw // 2 - tape.width // 2, m - tape.height // 2))
    return canvas.rotate(angle, expand=True, resample=Image.BICUBIC)


def meme(name, crop=None):
    """A meme from thumbnails/assets/ on a taped card; crop = (left, top, right, bottom) in pixels."""
    im = Image.open(ASSETS / name).convert("RGB")
    return taped_card(im.crop(crop) if crop else im)


def frame(ax, lesson):
    """The template: cream page, title top left, green card top right."""
    ax.imshow(np.full((720, 1280, 3), CREAM, np.uint8), extent=(0, 1280, 0, 720), zorder=-10, aspect="auto")
    ax.text(48, 642, lesson["title"], fontsize=lesson.get("title_size", 80), color=CHARCOAL, va="center",
            ha="left", **LATIN)
    badge(ax, 1250, 642, lesson["tag"], 34, GREEN)


# ---------- lessons ----------

def draw_llm01(ax):
    """GPT-4o's tokens for "How many r's in strawberry?", " strawberry" circled; 🙋 asks, 🤖 says 2,
    Picard facepalms."""
    toks = [("How", 5299), ("␣many", 1991), ("␣r", 428), ("'s", 885), ("␣in", 306),
            ("␣strawberry", 101830), ("?", 30)]
    boxes = token_row(ax, 42, 425, 33, toks, hot=5)
    marker_circle(ax, boxes[5])
    put_image(ax, emoji("\U0001F64B", 300), 100, 280, 82)          # raising hand
    ax.text(160, 255, "how many r's?", fontsize=46, color=GREEN, **HAND)
    put_image(ax, emoji("\U0001F916", 300), 104, 140, 96)          # robot
    ax.text(175, 100, "2", fontsize=80, color=RED, **HAND)
    put_image(ax, meme("llm01_picard_facepalm.jpg", crop=(140, 0, 895, 503)), 1010, 178, 330)


def pill(ax, x1, cy, text, size=24, face=ORANGE, ink=CHARCOAL):
    """A small card under the lesson card, e.g. "Practical"."""
    return badge(ax, x1, cy, text, size, face, ink=ink, padx=16, pady=14)


def bubble(ax, x, y, w, h, face="white", edge="#c9cfdb"):
    """A speech bubble with its tail on the left, pointing at whoever speaks."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h * 0.3}",
                                facecolor=face, edgecolor=edge, lw=2.5, zorder=3))
    ax.add_patch(plt.Polygon([(x + 4, y + h * 0.30), (x + 4, y + h * 0.62), (x - 30, y + h * 0.25)],
                             closed=True, facecolor=face, edgecolor="none", zorder=4))
    ax.plot([x + 2, x - 30, x + 2], [y + h * 0.62, y + h * 0.25, y + h * 0.30], color=edge, lw=2.5, zorder=4)


def blocks(ax, x, y, n, per_line, w=14, h=24, gap=3, edge="#9a9a9a"):
    """n small token blocks in rows of per_line, from (x, y = top row's bottom) downwards."""
    for i in range(n):
        r, c = divmod(i, per_line)
        ax.add_patch(FancyBboxPatch((x + c * (w + gap), y - r * (h + 6)), w, h,
                                    boxstyle="round,pad=0,rounding_size=3", facecolor=FILLS[i % 3],
                                    edgecolor=edge, lw=0.8, zorder=3))
    return x + min(n, per_line) * (w + gap)


# The practical's numbers (course repo llms/01_tokenization/results/02_armenian_tokens.json): LLM-1's
# Armenian line, 57 letters = 102 bytes = 102 GPT-4 tokens; the class's own BPE (500 merges, ~30 s) 28;
# GPT-4o 19. GPT-4's Armenian premium per meaning (NTREX-128): x9.16. The glitch probe: GPT-4o-mini
# asked to repeat " որովհ" / " վերաբերյ" replied with nothing.

def llm02_glitch(meme_file):
    def draw(ax):
        pill(ax, 1250, 560, "Practical")
        put_image(ax, emoji("\U0001F64B", 300), 95, 455, 86)            # raising hand
        ax.text(158, 430, "repeat after me:", fontsize=46, color=GREEN, **HAND)
        ax.figure.canvas.draw()
        x = 158 + text_w(ax, "repeat after me:", 46, **HAND) + 50
        boxes = token_row(ax, x, 418, 40, [("␣որովհ", None)], hot=0, hot_pad=0)
        marker_circle(ax, boxes[0])
        put_image(ax, emoji("\U0001F916", 300), 100, 260, 100)          # robot
        bubble(ax, 190, 205, 330, 110)
        ax.text(355, 140, "(nothing. at all.)", fontsize=30, color=RED, ha="center", **HAND)
        put_image(ax, meme(meme_file), 975, 175, 330)
    return draw


def thought_bubble(ax, x, y, w, h, tail_to, face="#F1F3F7", edge="#c9cfdb"):
    """A thinking cloud: a rounded box and three shrinking dots trailing to (tail_to)."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h * 0.18}",
                                facecolor=face, edgecolor=edge, lw=2.5, zorder=3))
    (tx, ty), (bx, by) = tail_to, (x + 30, y + 10)
    for k, r in enumerate([14, 10, 7]):
        f = (k + 1) / 4
        ax.add_patch(plt.Circle((bx + (tx - bx) * f, by + (ty - by) * f), r, facecolor=face, edgecolor=edge,
                                lw=2, zorder=3))


def llm02_thinking(meme_file):
    """gpt-oss-20b asked to spell " վերաբերյ" thinks in circles about "բրյ" (the saved run the class
    saw, results/02_probe_ledger.json): 'The word is "բրյ"?? ... I'm confused.'"""
    def draw(ax):
        pill(ax, 1250, 560, "Practical")
        put_image(ax, emoji("\U0001F64B", 300), 95, 455, 86)            # raising hand
        ax.text(158, 430, "spell it:", fontsize=46, color=GREEN, **HAND)
        ax.figure.canvas.draw()
        x = 158 + text_w(ax, "spell it:", 46, **HAND) + 50
        boxes = token_row(ax, x, 418, 40, [("␣վերաբերյ", None)], hot=0, hot_pad=0)
        marker_circle(ax, boxes[0])
        put_image(ax, emoji("\U0001F916", 300), 85, 85, 100)           # robot
        lines = [("The word is \"բրյ\"??", CHARCOAL), ("Actually the word: \"բրյ\"??", CHARCOAL),
                 ("I'm confused.", RED)]
        # the bubble is sized to its longest line: at a fixed 560 px the "??" stuck out (the user, 2026-11-10)
        w = max(text_w(ax, s, 26, **MONO) for s, _ in lines) + 60
        thought_bubble(ax, 175, 115, w, 235, tail_to=(120, 125))
        for i, (line, ink) in enumerate(lines):
            ax.text(205, 310 - i * 72, line, fontsize=26, color=ink, va="center",
                    fontweight="bold" if ink == RED else "normal", **MONO)
        pic = meme(meme_file, crop=(180, 0, 1354, 784) if "pikachu" in meme_file else None)
        h = min(300, (1262 - (175 + w) - 30) * pic.height / pic.width)
        pw = h * pic.width / pic.height
        put_image(ax, pic, 175 + w + 30 + pw / 2, 190, h)
    return draw


def llm02_tax(ax):
    pill(ax, 1250, 560, "Practical")
    ax.text(48, 528, "one Armenian sentence, 57 letters:", fontsize=34, color=GREEN, **HAND)
    rows = [("GPT-4", 102, 450, RED), ("ours", 28, 345, CHARCOAL), ("GPT-4o", 19, 285, CHARCOAL)]
    for name, n, y, ink in rows:
        ax.text(48, y + 12, name, fontsize=30, color=CHARCOAL, va="center", **LATIN)
        x_end = blocks(ax, 225, y, n, per_line=58)
        last_y = y - ((n - 1) // 58) * 30
        x_num = x_end + 14 if n <= 58 else 225 + (n - 58) * 17 + 14
        ax.text(x_num, last_y + 12, f"{n}", fontsize=30, color=ink, va="center", fontweight="bold", **MONO)
    ax.text(48, 175, "Armenian on GPT-4:", fontsize=40, color=CHARCOAL, **HAND)
    ax.text(48, 70, "x9 the price", fontsize=64, color=RED, **HAND)
    put_image(ax, meme("meme_surprised_pikachu.jpg", crop=(180, 0, 1354, 784)), 1040, 140, 250)


# The decoding lecture's numbers (course repo llms/06_decoding/): GPT-2's real greedy continuation of
# "The cat sat on the" (fig/dec_greedy_loop.pdf) and the real top 5 after it (floor 7.6%, bed 6.5%,
# couch 5.4%, ground 5.2%, edge 4.8%; results/roadmap_gpt2.json via the outline).
PROMPT = "The cat sat on the"


def llm03_loop(ax):
    ax.text(48, 505, "GPT-2, always the most likely token:", fontsize=34, color=GREEN, **HAND)
    t = ax.text(48, 440, PROMPT, fontsize=30, color=base.UNSUP_BAR, fontweight="bold", va="baseline",
                family="DejaVu Sans")
    ax.figure.canvas.draw()
    x = 48 + text_w(ax, PROMPT + " ", 30, family="DejaVu Sans", fontweight="bold")
    ax.text(x, 440, "floor, and the cat was still asleep.", fontsize=30, color=CHARCOAL, family="DejaVu Sans")
    put_image(ax, emoji("\U0001F916", 300), 100, 250, 110)
    bubble(ax, 195, 130, 840, 240)
    for i, line in enumerate(["\"I'm sorry. I'm sorry. I'm sorry.", "I'm sorry. I'm sorry. I'm sorry. I'm"]):
        ax.text(225, 290 - i * 80, line, fontsize=33, color=RED, family="DejaVu Sans", va="center")
    put_image(ax, emoji("\U0001F501", 300), 1150, 250, 150)        # repeat button
    del t


def llm03_temperature(ax):
    ax.text(48, 505, f"\"{PROMPT} ...\"", fontsize=34, color=GREEN, **HAND)
    rows = [("\U0001F976", "T = 0", "I'm sorry. I'm sorry. I'm sorry.", RED),      # GPT-2's real loop
            ("\U0001F642", "T = 1", "couch, purring quietly.", CHARCOAL),          # toy
            ("\U0001F975", "T = 5", "quantum potato Ponchik 509", RED)]           # toy, the user's words
    body = {"family": "Segoe UI"}                    # narrower than DejaVu Sans: leaves room for the dog
    ax.figure.canvas.draw()
    x_end = 262 + max(text_w(ax, text, 26, **body) for *_, text, _ in rows)
    for i, (face, name, text, ink) in enumerate(rows):
        y = 410 - i * 130
        put_image(ax, emoji(face, 300), 75, y, 84)
        ax.text(127, y, name, fontsize=30, color=CHARCOAL, va="center", **LATIN)
        ax.text(262, y, text, fontsize=26, color=ink, va="center", **body)
    dog = meme("meme_this_is_fine.jpg", crop=(150, 0, 800, 450))
    h = min(330, (1265 - x_end - 25) * dog.height / dog.width)     # as big as fits right of the text
    w = h * dog.width / dog.height
    put_image(ax, dog, x_end + 25 + w / 2, max(175, h / 2 + 10), h)


def llm03_dice(ax):
    ax.text(48, 505, f"\"{PROMPT} ___\"", fontsize=40, color=GREEN, **HAND)
    top5 = [("floor", 7.6), ("bed", 6.5), ("couch", 5.4), ("ground", 5.2), ("edge", 4.8)]
    for i, (w, p) in enumerate(top5):
        y = 410 - i * 72
        ax.text(230, y, w, fontsize=30, color=CHARCOAL, ha="right", va="center", family="DejaVu Sans")
        ax.add_patch(FancyBboxPatch((250, y - 22), p * 75, 44, boxstyle="round,pad=0,rounding_size=8",
                                    facecolor=FILLS[i % 3], edgecolor=RED if i == 0 else "#9a9a9a",
                                    lw=3 if i == 0 else 1.2, zorder=3))
        ax.text(260 + p * 75, y, f"{p}%", fontsize=26, color=CHARCOAL, va="center", family="DejaVu Sans")
    ax.text(48, 35, "+ 50,252 other tokens: 70.5%", fontsize=30, color="#7a7a7a", family="DejaVu Sans")
    put_image(ax, emoji("\U0001F3B2", 300), 960, 300, 200)         # die
    ax.text(960, 120, "which one?", fontsize=46, color=GREEN, ha="center", **HAND)


# The API practical's outputs as the class saw them (recording of 2026-11-11; course repo
# llms/02_decoding/04_llm_api.ipynb): 5b Llama 3.1 8B at T = 2 "The chilled onionatois-modris Medicallicensed
# socialism Dent allowNull THERE ..."; 8a Haiku 5.5 at T = 2 "The cat stretched lazily in a patch of sunlight,
# then curled up for a long nap on the windowsill." (OpenRouter dropped the knob); 8b gpt-5-nano, low effort:
# "Lilit", 110 completion tokens, 64 of them reasoning; 5f Llama with no stop string wrote the tool's result
# itself: "Observation: According to Wikipedia, the population of Gyumri is approximately 107,000 people."

def llm04_ignored(ax):
    pill(ax, 1250, 560, "Practical")
    ax.text(48, 505, "temperature = 2:", fontsize=40, color=GREEN, **HAND)
    body = {"family": "Segoe UI"}
    rows = [("Llama", ["The chilled onionatois-modris", "Medicallicensed socialism Dent"], RED),
            ("Haiku", ["The cat stretched lazily in a", "patch of sunlight, then curled up"], CHARCOAL)]
    for i, (name, lines, ink) in enumerate(rows):
        y = 390 - i * 160
        ax.text(48, y, name, fontsize=32, color=CHARCOAL, va="center", **LATIN)
        for k, line in enumerate(lines):
            ax.text(215, y + 24 - k * 50, line, fontsize=27, color=ink, va="center", **body)
    ax.text(48, 70, "no error. knob silently dropped.", fontsize=40, color=RED, **HAND)
    put_image(ax, meme("meme_blinking_guy.jpg"), 1030, 300, 250)


def llm04_request(ax):
    """No meme (the user, 2026-11-12: "were overdoing the fun, lets not force it"): the practical's point,
    the decoding knobs as fields of one request (values from the notebook's cells), and the first call's real
    usage (prompt 20, completion 39, $0.0000264)."""
    pill(ax, 1250, 560, "Practical")
    ax.text(48, 505, "the decoding knobs, as request fields:", fontsize=34, color=GREEN, **HAND)
    lines = [('{', None), ('  "model": "openai/gpt-4o-mini",', None), ('  "messages": [...],', None),
             ('  "temperature": 0.7,', ORANGE), ('  "top_p": 0.9,', ORANGE), ('  "max_tokens": 60,', ORANGE),
             ('  "stop": ["Observation:"],', ORANGE), ('  "seed": 509,', ORANGE), ('  "logprobs": true', ORANGE),
             ('}', None)]
    size, step, top = 22, 40, 438
    ax.add_patch(FancyBboxPatch((40, top - step * (len(lines) - 1) - 28), 665, step * (len(lines) - 1) + 56,
                                boxstyle="round,pad=0,rounding_size=18", facecolor="white", edgecolor="#c9cfdb",
                                lw=2.5, zorder=2))
    ax.figure.canvas.draw()
    adv = text_w(ax, "M" * 10, size, **MONO) / 10
    for i, (line, mark) in enumerate(lines):
        y = top - i * step
        if mark:
            key = line.split(":")[0]
            ax.add_patch(FancyBboxPatch((62 + adv * 2 - 4, y - 17), adv * (len(key) - 2) + 8, 34,
                                        boxstyle="round,pad=0,rounding_size=6", facecolor="#FBE7B7",
                                        edgecolor="none", zorder=3))
        ax.text(62, y, line, fontsize=size, color=CHARCOAL, va="center", zorder=4, **MONO)
    ax.annotate("", xy=(782, 255), xytext=(718, 255),
                arrowprops={"arrowstyle": "-|>", "color": CHARCOAL, "lw": 3, "mutation_scale": 28})
    usage = ['"prompt_tokens": 20,', '"completion_tokens": 39,', '"cost": 0.0000264']
    ax.add_patch(FancyBboxPatch((795, 150), 460, 210, boxstyle="round,pad=0,rounding_size=18",
                                facecolor="white", edgecolor="#c9cfdb", lw=2.5, zorder=2))
    ax.text(815, 320, "usage", fontsize=24, color="#7a7a7a", va="center", family="Segoe UI", zorder=4)
    for i, line in enumerate(usage):
        ax.text(815, 270 - i * 45, line, fontsize=size - 1, color=CHARCOAL, va="center", zorder=4, **MONO)


def llm04_temperature_plain(ax):
    """The same Llama / Haiku contrast as llm04_ignored, without the meme and the caption."""
    pill(ax, 1250, 560, "Practical")
    ax.text(48, 505, "the same request, temperature = 2:", fontsize=36, color=GREEN, **HAND)
    body = {"family": "Segoe UI"}
    rows = [("Llama 3.1", ["The chilled onionatois-modris Medicallicensed", "socialism Dent allowNull THERE son ado couch"],
             RED),
            ("Haiku 5.5", ["The cat stretched lazily in a patch of sunlight,", "then curled up for a long nap on the windowsill."],
             CHARCOAL)]
    for i, (name, lines, ink) in enumerate(rows):
        y = 370 - i * 190
        ax.text(48, y, name, fontsize=32, color=CHARCOAL, va="center", **LATIN)
        for k, line in enumerate(lines):
            ax.text(285, y + 27 - k * 54, line, fontsize=29, color=ink, va="center", **body)


def llm04_reasoning(ax):
    pill(ax, 1250, 560, "Practical")
    ax.text(48, 505, "Ani > Gor > Lilit. Youngest?", fontsize=38, color=GREEN, **HAND)
    put_image(ax, emoji("\U0001F916", 300), 95, 395, 90)            # robot
    ax.text(165, 372, "\"Lilit\"", fontsize=54, color=CHARCOAL, **HAND)
    w, h, gap, per = 15, 26, 3, 37                                   # 110 billed tokens, 64 of them reasoning
    for i in range(110):
        r, c = divmod(i, per)
        hidden = i < 64
        ax.add_patch(FancyBboxPatch((48 + c * (w + gap), 270 - r * (h + 7)), w, h,
                                    boxstyle="round,pad=0,rounding_size=3",
                                    facecolor="#BDBDBD" if hidden else FILLS[i % 3],
                                    edgecolor="#8a8a8a", lw=0.8, zorder=3))
    ax.text(48 + per * (w + gap) + 14, 230, "110 tokens\nbilled", fontsize=26, color=CHARCOAL, va="center",
            family="Segoe UI")
    ax.text(48, 70, "64 of them: thinking you never see", fontsize=40, color=RED, **HAND)
    put_image(ax, meme("meme_surprised_pikachu.jpg", crop=(180, 0, 1354, 784)), 1060, 330, 220)


def llm04_gyumri(ax):
    pill(ax, 1250, 560, "Practical")
    put_image(ax, emoji("\U0001F64B", 300), 90, 500, 78)            # raising hand
    ax.text(145, 480, "How many people live in Gyumri?", fontsize=38, color=GREEN, **HAND)
    put_image(ax, emoji("\U0001F916", 300), 90, 330, 90)            # robot
    lines = [("Action: search[Gyumri]", CHARCOAL), ("Observation: According to", RED),
             ("Wikipedia, ~107,000 people", RED)]
    for i, (line, ink) in enumerate(lines):
        ax.text(160, 405 - i * 55 - (12 if i else 0), line, fontsize=25, color=ink, va="center", **MONO)
    ax.figure.canvas.draw()
    x1 = 160 + text_w(ax, lines[2][0], 25, **MONO)
    marker_circle(ax, (150, x1 + 10, 262, 358), sx=0.58, sy=0.72)
    ax.text(48, 70, "it wrote the tool's answer itself", fontsize=40, color=RED, **HAND)
    put_image(ax, meme("meme_blinking_guy.jpg"), 1065, 300, 240)


LESSONS = [
    {"tag": "LLM 01", "title": "Tokenization", "draw": draw_llm01, "out": "LLM01.png"},
    # The user, 2026-11-10: "for thumbnails i like pikachu but pls notice that the ?? are out of the dialog box".
    {"tag": "LLM 02", "title": "Armenian Tokens", "draw": llm02_thinking("meme_surprised_pikachu.jpg"),
     "out": "LLM02.png"},
    # The user, 2026-11-10: "for the decoding thumbnail the temperature is the best, pls change 1987 to
    # quantum, and make the this is fine dog a bit bigger"; then "change second quantum to number 509, and
    # banana to potato, and yerevan to Ponchik".
    {"tag": "LLM 03", "title": "Decoding", "draw": llm03_temperature, "out": "LLM03.png"},
    # The user, 2026-11-12, after "were overdoing the fun, lets not force it": "d is good, the one with request
    # and response" (llm04_d_request).
    {"tag": "LLM 04", "title": "LLM APIs", "draw": llm04_request, "out": "LLM04.png"},
]

OPTIONS = {
    # 2026-11-10: "put as example model thinking bre actually the word is ... im confused".
    "LLM02d": [("llm02_d_thinking_blink", {"tag": "LLM 02", "title": "Armenian Tokens",
                                           "draw": llm02_thinking("meme_blinking_guy.jpg")}),
               ("llm02_e_thinking_pikachu", {"tag": "LLM 02", "title": "Armenian Tokens",
                                             "draw": llm02_thinking("meme_surprised_pikachu.jpg")})],
    "LLM02": [("llm02_a_glitch_blink", {"tag": "LLM 02", "title": "Armenian Tokens",
                                        "draw": llm02_glitch("meme_blinking_guy.jpg")}),
              ("llm02_b_tax_pikachu", {"tag": "LLM 02", "title": "Armenian Tokens", "draw": llm02_tax}),
              ("llm02_c_glitch_pikachu", {"tag": "LLM 02", "title": "Armenian Tokens",
                                          "draw": llm02_glitch("meme_surprised_pikachu.jpg")})],
    "LLM04plain": [("llm04_d_request", {"tag": "LLM 04", "title": "LLM APIs", "draw": llm04_request}),
                   ("llm04_e_temperature_plain", {"tag": "LLM 04", "title": "LLM APIs",
                                                  "draw": llm04_temperature_plain})],
    "LLM04": [("llm04_a_ignored", {"tag": "LLM 04", "title": "LLM APIs", "draw": llm04_ignored}),
              ("llm04_b_reasoning", {"tag": "LLM 04", "title": "LLM APIs", "draw": llm04_reasoning}),
              ("llm04_c_gyumri", {"tag": "LLM 04", "title": "LLM APIs", "draw": llm04_gyumri})],
    "LLM03": [("llm03_a_loop", {"tag": "LLM 03", "title": "Decoding", "draw": llm03_loop}),
              ("llm03_b_temperature", {"tag": "LLM 03", "title": "Decoding", "draw": llm03_temperature}),
              ("llm03_c_dice", {"tag": "LLM 03", "title": "Decoding", "draw": llm03_dice})],
}


def render(lesson, path):
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1280)
    ax.set_ylim(0, 720)
    ax.axis("off")
    frame(ax, lesson)
    lesson["draw"](ax)
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)


def contact_sheet(paths, out):
    cw, ch, gut = 640, 360, 18
    font = ImageFont.truetype("arial.ttf", 24)
    rows = -(-len(paths) // 2)
    sheet = Image.new("RGB", (2 * cw + 3 * gut, rows * (ch + 40) + gut), "white")
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(paths):
        x, y = gut + (i % 2) * (cw + gut), gut + (i // 2) * (ch + 40)
        draw.text((x, y), p.stem, fill="black", font=font)
        sheet.paste(Image.open(p).convert("RGB").resize((cw, ch), Image.LANCZOS), (x, y + 30))
        draw.rectangle([x - 1, y + 29, x + cw, y + 30 + ch], outline="#bbbbbb")
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filter", nargs="?", default="", help="Render only outputs whose name contains this")
    ap.add_argument("--options", action="store_true", help="Render OPTIONS[filter] instead of LESSONS")
    args = ap.parse_args()
    t0 = time.time()
    if args.options:
        if args.filter not in OPTIONS:
            raise ValueError(f"No options for {args.filter!r}; have {sorted(OPTIONS)}")
        OPT_OUT.mkdir(parents=True, exist_ok=True)
        outs = []
        for i, (name, lesson) in enumerate(OPTIONS[args.filter], 1):
            outs.append(OPT_OUT / f"{name}.png")
            render(lesson, outs[-1])
            log.info(f"{i}/{len(OPTIONS[args.filter])} {outs[-1]}, {time.time() - t0:.0f}s elapsed")
        sheet = OPT_OUT / f"overview_{args.filter.lower()}.png"
        contact_sheet(outs, sheet)
        log.info(f"Wrote {sheet}; done in {time.time() - t0:.0f}s")
        return
    todo = [ls for ls in LESSONS if args.filter in ls["out"]]
    if not todo:
        raise ValueError(f"No lesson output contains {args.filter!r}")
    for ls in todo:
        render(ls, OUT / ls["out"])
        log.info(f"Wrote {OUT / ls['out']} ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
