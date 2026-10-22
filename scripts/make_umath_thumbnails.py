"""Thumbnails for the Համալսարանական մաթեմատիկա courses, made locally instead of in Canva.

    python scripts/make_umath_thumbnails.py --series ant --lesson 16 --topic "Քարլիցի մոդուլ։ Ցիկլոտոմիկ ընդլայնում"
    python scripts/make_umath_thumbnails.py --series metric --lesson 15 --topic "..." -o out.png
    python scripts/make_umath_thumbnails.py --compare      # rebuild the YouTube references side by side
        # ~2 s per thumbnail; --compare ~5 s

Series: `ant` (Papikian, Հանրահաշիվ և թվերի տեսություն), `metric` (Tserunyan, Մետրիկական
տարածություններ և տոպոլոգիա), `linalg` (Mikaelian, Գծային հանրահաշիվ). Each draws the lesson line and
the topic on a text-free plate (thumbnails/umath/templates/<series>_plate.png, built from the
YouTube thumbnails; the series title and the artwork are baked into it). Fonts, sizes, letter
spacing and baselines were fitted to those thumbnails (grayscale NCC 0.82-0.97, see
_knowledge/umath_thumbnails.md). A topic splits after "։" if it has one, else wraps at the width
limit; `\\n` sets the break by hand. If it does not fit, the font shrinks (one line per "։"-part
down to 85%, then wrapping down to 70%); below that it raises.
Math, LaTeX-like, between dollars: "$\\mathbb{R}^2$ հարթությունում", "$F_q$", "$x^{n+1}$"; plain
ℝ² works too. Double-struck letters come from Sans Serif Collection, sub/superscripts are the
main font at 0.67x, shifted as measured on the linalg 1.1 thumbnail.
Default output: thumbnails/umath/<series>_<lesson>.png.
"""
import argparse
import logging
import re
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
Path(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/make_umath_thumbnails.log", encoding="utf-8")])
log = logging.getLogger(__name__)

FONTS = REPO / "fonts"
BEBAS = FONTS / "arm-hmks-bebas-neue/Arm Hmk's Bebas Neue.TTF"
# for characters the main font lacks: Cambria Math, index 1 of cambria.ttc
FALLBACK = (Path(r"C:\Windows\Fonts\cambria.ttc"), 1)
# double-struck letters: Windows' Sans Serif Collection has the upright sans ℝ of the linalg
# 1.1 thumbnail (Cambria Math's has serifs; matplotlib mathtext's \mathbb is italic in every
# fontset, checked 2026-10-21). Against the reference ℝ (49 px tall, main font 64 px) it scores
# NCC 0.788 plain at 68 px and 0.975 at 66 px with a 1 px stroke (the original is bolder).
BB_FONT = (Path(r"C:\Windows\Fonts\SansSerifCollection.ttf"), 0)
BB_LETTERS = {"R": "ℝ", "Z": "ℤ", "Q": "ℚ", "N": "ℕ", "C": "ℂ", "P": "ℙ", "H": "ℍ"}
# measured on the same reference: the superscript 2 is 30 px tall (Mardoto Medium 43 px, NCC
# 0.93) with its baseline 29 px above the main one
SCALE = {"n": 1.0, "bb": 66 / 64, "sup": 0.67, "sub": 0.67}
SHIFT = {"n": 0.0, "bb": 0.0, "sup": -29 / 64, "sub": 0.12}  # baseline offset, in em; up is negative
STROKE = {"bb": 1}
SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻", "0123456789n+-"))
SUBSCRIPTS = dict(zip("₀₁₂₃₄₅₆₇₈₉", "0123456789"))


def mardoto(weight: str) -> Path:
    return FONTS / f"mardoto/Mardoto-{weight}.ttf"


_CMAPS: dict[tuple, set] = {}


def has_glyph(path: Path, index: int, ch: str) -> bool:
    key = (str(path), index)
    if key not in _CMAPS:
        from fontTools.ttLib import TTCollection, TTFont
        f = TTCollection(str(path)).fonts[index] if str(path).lower().endswith(".ttc") else TTFont(str(path))
        _CMAPS[key] = set(f.getBestCmap())
    return ord(ch) in _CMAPS[key] or ch.isspace()


# x is the ink's left edge (or right edge when align="right"); y is the baseline of the first line.
TEMPLATES = {
    "ant": {
        "plate": "ant_plate.png",
        # digits and "-" sit ~4.9 px tighter than the letters in the references (7 pairs in Դաս
        # 11-12, 13, 14, 15), so they get their own letter spacing
        "lesson": dict(fmt="ԴԱՍ {n}", font=BEBAS, size=81, track=6.5, num_track=1.6, color=(202, 38, 44),
                       x=100, y=432),
        "topic": dict(font=mardoto("Italic"), size=65, track=0.0, color=(0, 0, 0), x=100, y=549,
                      line_gap=82, align="left", max_w=815, max_baseline=690),
    },
    "metric": {
        "plate": "metric_plate.png",
        "lesson": dict(fmt="Դաս {n}", font=mardoto("Regular"), size=55, track=1.0, color=(240, 209, 120),
                       x=76, y=444),
        # the reference topics run to x~905, slightly over the sphere's lower left edge
        "topic": dict(font=mardoto("Bold"), size=57, track=0.5, color=(255, 255, 255), x=76, y=549,
                      line_gap=70, align="left", max_w=840, max_baseline=690),
    },
    "linalg": {
        "plate": "linalg_plate.png",
        "lesson": dict(fmt="ԴԱՍ {n}", font=BEBAS, size=67, track=2.5, color=(236, 65, 66), x=120, y=421),
        # the original is a rounded face of about Mardoto Medium's weight (a 1 px stroke on top
        # looked clearly heavier at real size); its round stroke ends are the visible difference
        "topic": dict(font=mardoto("Medium"), size=64, track=1.9, color=(0, 0, 0), x=1205, y=134,
                      line_gap=94, align="right", max_w=1020, max_baseline=330),
    },
}

# the YouTube thumbnails the templates were fitted to (series, lesson, topic, reference file)
REFERENCES = [
    ("ant", "15", "Դրինֆելդի մոդուլներ", "ant_das15_hWpA9f5fmUg.jpg"),
    ("ant", "14", "Գծային օպերատորներ։ Ժորդանյան նորմալ տեսք", "ant_das14_cHCKLOSxctg.jpg"),
    ("metric", "14", "Բեռի կատեգորիաների թեորեմ", "metric_das14_9Xye4V_MTEU.jpg"),
    ("metric", "13", "Կանտոր-Բենդիքսոնի թեորեմ։ Չնչին բազմություններ", "metric_das13_XvUbT3sTHPg.jpg"),
    ("linalg", "1.1", "Վեկտորի գաղափարը\nℝ² հարթությունում", "linalg_das1.1_AFkkDo_bx_o.jpg"),
    ("linalg", "20.3", "Գծային արտապատկերումները և բազիսի փոփոխությունը", "linalg_das20.3_pCzP2OJnUns.jpg"),
]


def parse(text: str) -> list[tuple[str, str]]:
    """(character, style) pairs; style is n (normal), bb (double-struck), sup or sub.

    LaTeX-like math goes between dollars: $\\mathbb{R}^2$, $F_q$, $x^{n+1}$. Outside them, ℝ ℤ ℚ
    ... are double-struck and ² ³ ... / ₂ ₃ ... superscripts / subscripts as typed."""
    out, i, in_math = [], 0, False
    while i < len(text):
        ch = text[i]
        if ch == "$":
            in_math, i = not in_math, i + 1
            continue
        if in_math and text.startswith("\\mathbb{", i):
            j = text.index("}", i)
            out += [(BB_LETTERS.get(c, c), "bb") for c in text[i + 8: j]]
            i = j + 1
            continue
        if in_math and ch in "^_":
            style = "sup" if ch == "^" else "sub"
            if text[i + 1: i + 2] == "{":
                j = text.index("}", i)
                out += [(c, style) for c in text[i + 2: j]]
                i = j + 1
            else:
                out.append((text[i + 1], style))
                i += 2
            continue
        if ch in SUPERSCRIPTS:
            out.append((SUPERSCRIPTS[ch], "sup"))
        elif ch in SUBSCRIPTS:
            out.append((SUBSCRIPTS[ch], "sub"))
        elif ch in BB_LETTERS.values():
            out.append((ch, "bb"))
        else:
            out.append((ch, "n"))
        i += 1
    if in_math:
        raise ValueError(f"unclosed $ in {text!r}")
    return out


_FONTS: dict[tuple, ImageFont.FreeTypeFont] = {}


def font_for(ch: str, style: str, font: ImageFont.FreeTypeFont) -> ImageFont.FreeTypeFont:
    """The font a character is drawn in: the main one (scaled for sup/sub), the double-struck one,
    or the fallback for a character the chosen font does not have."""
    size = max(int(round(font.size * SCALE[style])), 1)
    path, index = (BB_FONT if style == "bb" else (Path(font.path), 0))
    if not has_glyph(path, index, ch):
        path, index = FALLBACK
        if not has_glyph(path, index, ch):
            raise ValueError(f"no font here has {ch!r} (U+{ord(ch):04X})")
    if style == "n" and path == Path(font.path):
        return font
    key = (str(path), index, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(str(path), size, index=index)
    return _FONTS[key]


NUMERIC = set("0123456789-.")


def char_track(ch: str, track: float, num_track: float | None) -> float:
    return num_track if num_track is not None and ch in NUMERIC else track


def layout(text: str, font: ImageFont.FreeTypeFont, track: float, num_track: float | None = None) -> list[tuple]:
    """(character, font, baseline shift px, advance px) per character. Pairs of normal characters
    in the main font keep their kerning; letter spacing is added after every character (num_track
    instead after digits, "-" and ".", where a template sets it)."""
    items = parse(text)
    out = []
    for i, (ch, style) in enumerate(items):
        f = font_for(ch, style, font)
        nxt = items[i + 1] if i + 1 < len(items) else None
        if f is font and nxt and nxt[1] == "n" and font_for(nxt[0], "n", font) is font:
            adv = font.getlength(ch + nxt[0]) - font.getlength(nxt[0])
        else:
            adv = f.getlength(ch)
        if style in ("sup", "sub") and nxt and nxt[0] == " ":
            # the reference leaves 34 px between the superscript 2 and the next word, 9 px more
            # than a plain space gives
            adv += 9 / 64 * font.size
        out.append((ch, f, SHIFT[style] * font.size, adv + char_track(ch, track, num_track), STROKE.get(style, 0)))
    return out


def text_width(text: str, font: ImageFont.FreeTypeFont, track: float) -> float:
    return sum(item[3] for item in layout(text, font, track)) - track


def place(draw, text: str, spec: dict, font, y: float) -> None:
    items = layout(text, font, spec["track"], spec.get("num_track"))
    first_ch, first_font = items[0][0], items[0][1]
    w = sum(item[3] for item in items) - char_track(items[-1][0], spec["track"], spec.get("num_track"))
    x = (spec["x"] - first_font.getbbox(first_ch, anchor="ls")[0] if spec.get("align", "left") == "left"
         else spec["x"] - w)
    for ch, f, dy, adv, stroke in items:
        draw.text((x, y + dy), ch, font=f, fill=spec["color"], anchor="ls",
                  stroke_width=stroke, stroke_fill=spec["color"])
        x += adv


def wrap(topic: str, font, spec: dict, wrap_parts: bool = True) -> list[str]:
    """Explicit line breaks are kept as they are; otherwise split after "։" and, if wrap_parts,
    wrap each part at the width limit (a topic without "։" is always wrapped)."""
    topic = topic.replace("\\n", "\n")  # a literal \n typed on the command line
    if "\n" in topic:
        return [l.strip() for l in topic.split("\n") if l.strip()]
    parts = [p.strip() + "։" for p in topic.split("։")[:-1]] + [topic.split("։")[-1].strip()]
    lines = []
    for part in (p for p in parts if p):
        if not wrap_parts and "։" in topic:
            lines.append(part)
            continue
        cur = ""
        for word in re.findall(r"(?:\$[^$]*\$|[^\s$])+", part):  # a $...$ group stays whole
            trial = f"{cur} {word}".strip()
            if cur and text_width(trial, font, spec["track"]) > spec["max_w"]:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
    return lines


def make(series: str, lesson: str, topic: str) -> Image.Image:
    t = TEMPLATES[series]
    img = Image.open(REPO / "thumbnails/umath/templates" / t["plate"]).convert("RGB")
    if img.size != (1280, 720):
        raise ValueError(f"plate {t['plate']} is {img.size}, expected 1280x720")
    draw = ImageDraw.Draw(img)

    ls = t["lesson"]
    place(draw, ls["fmt"].format(n=lesson), ls, ImageFont.truetype(str(ls["font"]), ls["size"]), ls["y"])

    ts = t["topic"]
    # first one line per "։"-part, shrinking to at most 85%; then wrapping inside the parts, down
    # to 70%. At each step the largest size at which every line fits the width and the last
    # baseline stays above the template's limit wins; line spacing scales with the size.
    tries = [(s, False) for s in range(ts["size"], int(ts["size"] * 0.85) - 1, -1)]
    tries += [(s, True) for s in range(ts["size"], int(ts["size"] * 0.7) - 1, -1)]
    for size, wrap_parts in tries:
        font = ImageFont.truetype(str(ts["font"]), size)
        lines = wrap(topic, font, ts, wrap_parts)
        gap = ts["line_gap"] * size / ts["size"]
        if (all(text_width(l, font, ts["track"]) <= ts["max_w"] for l in lines)
                and ts["y"] + (len(lines) - 1) * gap <= ts["max_baseline"]):
            break
    else:
        raise ValueError(f"topic does not fit even at 70% size: {topic!r}; shorten it or add a \\n")
    if size != ts["size"]:
        log.info(f"topic font shrunk {ts['size']} -> {size} px to fit {len(lines)} lines")
    for i, line in enumerate(lines):
        place(draw, line, ts, font, ts["y"] + i * gap)
    return img


def compare() -> Path:
    ref_dir = REPO / "thumbnails/umath/reference"
    rows = []
    for series, lesson, topic, ref in REFERENCES:
        made = make(series, lesson, topic)
        orig = Image.open(ref_dir / ref).convert("RGB")
        row = Image.new("RGB", (2560, 720))
        row.paste(orig, (0, 0))
        row.paste(made, (1280, 0))
        rows.append(row.resize((1280, 360)))
    sheet = Image.new("RGB", (1280, 360 * len(rows)), "white")
    for i, r in enumerate(rows):
        sheet.paste(r, (0, 360 * i))
    out = REPO / "thumbnails/umath/templates/compare.png"
    sheet.save(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--series", choices=sorted(TEMPLATES))
    ap.add_argument("--lesson", help='lesson number as shown, e.g. "16" or "10.2-ա"')
    ap.add_argument("--topic", help="topic text; a '։' splits it into two lines")
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--compare", action="store_true", help="rebuild the reference thumbnails side by side")
    args = ap.parse_args()
    t0 = time.time()
    if args.compare:
        log.info(f"wrote {compare()} in {time.time() - t0:.1f} s (left: YouTube, right: local)")
        return
    if not (args.series and args.lesson and args.topic):
        ap.error("--series, --lesson and --topic are required (or --compare)")
    out = args.output or REPO / f"thumbnails/umath/{args.series}_{args.lesson}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make(args.series, args.lesson, args.topic).save(out)
    log.info(f"wrote {out} in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
