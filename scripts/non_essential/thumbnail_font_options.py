"""Render candidate Latin TITLE fonts in the three kept thumbnail styles.

On 2026-09-26 the user kept bignumber, notebook and highlighter from
thumbnail_style_options.py and wants to pick a title font next. Titles will be
mostly English from here on, so this compares Latin fonts; the Armenian font
(Adamathuz Bold) stays for now and only shows where a title mixes the two.

Rows are fonts, columns are the three styles, each on a different lesson so
every column tests something:
  bignumber   - ML44, a typical English title ("Neural Nets: Optimization")
  notebook    - ML24, the longest title, with middle-dot separators
  highlighter - ML46, Latin next to Adamathuz ("Neural Net ԶՐՈՅԻՑ")

Fonts load from their .ttf files, never by family name, so a missing file fails
loudly instead of matplotlib quietly substituting DejaVu Sans. Any .ttf dropped
into fonts/candidates/ joins the sheet automatically (labelled by file name).

Usage:
  python scripts/non_essential/thumbnail_font_options.py
Runtime: ~40 s for 10 fonts (guess; the log reports the actual time).
Output: thumbnails/font_options/<font>_<style>_<MLNN>.png and fonts_overview.png
"""
import logging
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thumbnail_style_options as opts  # noqa: E402  (styles, lessons, base generator)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from matplotlib.ft2font import FT2Font  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log = logging.getLogger("thumbnail_font_options")
log.propagate = False
log.setLevel(logging.INFO)
for handler in (logging.StreamHandler(sys.stderr),
                logging.FileHandler(LOG_DIR / "thumbnail_font_options.log", encoding="utf-8")):
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(handler)

WIN = Path("C:/Windows/Fonts")
CANDIDATES_DIR = Path("fonts/candidates")
OUT = opts.base.OUT_DIR / "font_options"

# Installed on this machine (Windows + Office). One per family, the weight that
# suits a thumbnail title. Grouped: current, handwritten, rounded/friendly,
# heavy sans, slab.
FONTS = [
    ("Comic Sans Bold (current)", WIN / "comicbd.ttf"),
    ("Ink Free", WIN / "inkfree.ttf"),
    ("Segoe Print Bold", WIN / "segoeprb.ttf"),
    ("Arial Rounded Bold", WIN / "arlrdbd.ttf"),
    ("Berlin Sans Demi", WIN / "brlnsdb.ttf"),
    ("Cooper Black", WIN / "coopbl.ttf"),
    ("Segoe UI Black", WIN / "seguibl.ttf"),
    ("Century Gothic Bold", WIN / "gothicb.ttf"),
    ("Franklin Gothic Heavy", WIN / "frahv.ttf"),
    ("Rockwell Extra Bold", WIN / "rockeb.ttf"),
]
COLUMNS = [("bignumber", "ML44"), ("notebook", "ML24"), ("highlighter", "ML46")]


def all_fonts():
    fonts = list(FONTS)
    if CANDIDATES_DIR.exists():
        fonts += [(p.stem, p) for p in sorted(CANDIDATES_DIR.glob("*.ttf"))]
    for label, path in fonts:
        if not path.exists():
            raise FileNotFoundError(f"font file for '{label}' not found: {path}")
    return fonts


def slug(label):
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


# Characters course titles actually use. Checked against each font's character
# map, because matplotlib only warns (once) and then draws an empty box.
NEEDED = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
          ":·-&?!'()")


def missing_glyphs(font_path):
    font = FT2Font(str(font_path))
    return "".join(ch for ch in NEEDED if font.get_char_index(ord(ch)) == 0)


def sheet(fonts, path):
    cell_w, cell_h, gut, label_w, head_h = 480, 270, 16, 400, 44
    img = Image.new("RGB", (label_w + len(COLUMNS) * (cell_w + gut),
                            head_h + len(fonts) * (cell_h + gut)), "white")
    draw = ImageDraw.Draw(img)
    head_font = ImageFont.truetype(str(WIN / "arial.ttf"), 26)
    note_font = ImageFont.truetype(str(WIN / "arial.ttf"), 22)
    for c, (style, name) in enumerate(COLUMNS):
        draw.text((label_w + c * (cell_w + gut) + 6, 8), f"{style} · {name}", fill="black",
                  font=head_font)
    for r, (label, font_path) in enumerate(fonts):
        y = head_h + r * (cell_h + gut)
        draw.text((10, y + cell_h // 2 - 30), label, fill="black",
                  font=ImageFont.truetype(str(font_path), 28))       # each name in its own font
        gaps = missing_glyphs(font_path)
        if gaps:
            draw.text((10, y + cell_h // 2 + 12), f"missing: {' '.join(gaps)}", fill="#D90012",
                      font=note_font)
        for c, (style, name) in enumerate(COLUMNS):
            src = OUT / f"{slug(label)}_{style}_{name}.png"
            x = label_w + c * (cell_w + gut)
            img.paste(Image.open(src).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS), (x, y))
            draw.rectangle([x - 1, y - 1, x + cell_w, y + cell_h], outline="#bbbbbb")
    img.save(path)
    log.info(f"Wrote {path} ({img.width}x{img.height}px)")


def main():
    t0 = time.time()
    fonts = all_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    lessons = {name: opts.lesson_by_name(name) for _, name in COLUMNS}
    illos = {name: opts.illustration(lesson) for name, lesson in lessons.items()}
    for i, (label, path) in enumerate(fonts, 1):
        opts.LATIN = {"fontproperties": FontProperties(fname=str(path))}
        for style, name in COLUMNS:
            fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
            fig.patch.set_facecolor("white")
            opts.STYLES[style](fig, lessons[name], illos[name])
            fig.savefig(OUT / f"{slug(label)}_{style}_{name}.png", facecolor=fig.get_facecolor())
            plt.close(fig)
        elapsed = time.time() - t0
        log.info(f"{i}/{len(fonts)} {label}: {elapsed:.0f}s elapsed, "
                 f"~{elapsed / i * (len(fonts) - i):.0f}s left")
    sheet(fonts, OUT / "fonts_overview.png")
    log.info(f"Done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
