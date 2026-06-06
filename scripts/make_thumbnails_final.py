"""Final thumbnail generator for ML lectures — locked-in design.

Locked design:
- Layout:         wide chart spanning the bottom band; no dead space
- Background:    white #ffffff
- Side accent:    vertical orange bar at the left edge (channel identity)
- Lesson tag:     "ML NN" in Segoe Script (handwritten), navy #0033A0, 36pt
- Title:          Armenian, two- or three-line wrap, charcoal, Adamathuz Bold.
                  Title size is per-lesson — bigger for 2-line titles, slightly
                  smaller for 3-line so the title block doesn't crash into the
                  chart.
- Illustration:   per-lesson chart filling the bottom 42% of canvas. Draw
                  functions take `(fig, bbox)` so they can carve the chart band
                  into sub-panels (used by ML 03's three-icon layout).
- Palette:        Armenian flag (orange / blue / red) on white
- NO Metric branding

Required asset: fonts/adamathuz/Adamathuz Bold.ttf
Required system font: Segoe Script (Windows)

Output: output/thumbnails/final/ML0N_final.png
"""
import logging
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import Rectangle

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

plt.rcParams["mathtext.fontset"] = "stix"

OUT_DIR = Path("thumbnails")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / "make_thumbnails_final.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# Locked palette
BG = "#ffffff"
BAR = "#F2A800"
TAG_COLOR = "#0033A0"
TITLE_COLOR = "#0e0e0e"
POINT_COLOR = "#0033A0"
LINE_COLOR = "#D90012"
RESIDUAL_COLOR = "#5a6478"

# Typography
TITLE_LS = 1.0
TAG_SIZE = 36
TAG_FONT = "Segoe Script"

# Chart area (used as default bbox for draw functions)
CHART_BBOX = (0.06, 0.06, 0.90, 0.42)

# Armenian title font
ARM_FONT_PATH = Path("fonts/adamathuz/Adamathuz Bold.ttf")
if not ARM_FONT_PATH.exists():
    raise FileNotFoundError(
        f"Required font not found: {ARM_FONT_PATH.resolve()}. "
        f"Extract fonter.am_adamathuz.zip into fonts/adamathuz/ before running."
    )
font_manager.fontManager.addfont(str(ARM_FONT_PATH))
ARM_PROPS = font_manager.FontProperties(fname=str(ARM_FONT_PATH))
log.info(f"Loaded Armenian font: {ARM_PROPS.get_name()}")


def _strip(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


# ---------- illustrations ----------
# Each draw function takes (fig, bbox) — bbox is (x, y, w, h) in figure coords.
# This lets some lessons draw a single chart and others (ML 03) carve the
# chart band into multiple sub-panels.

def draw_regression_simple(fig, bbox):
    """ML 01: simplified to just scatter + best-fit line. No residuals, fewer
    points, more breathing room."""
    ax = fig.add_axes(bbox)
    ax.set_facecolor(BG)
    rng = np.random.default_rng(509)
    x = np.linspace(0, 10, 14)
    y = 0.7 * x + 1.2 + rng.normal(0, 1.1, x.size)
    slope, intercept = np.polyfit(x, y, 1)
    xs = np.linspace(0, 10, 100)
    ax.plot(xs, slope * xs + intercept, color=LINE_COLOR, linewidth=7,
            solid_capstyle="round", zorder=3)
    ax.scatter(x, y, s=220, color=POINT_COLOR, edgecolor="white",
               linewidth=2.5, alpha=0.95, zorder=4)
    _strip(ax)


# --- ML 02 sub-panels (design matrix / normal equation / polynomial fit) ---

def _draw_design_matrix_panel(ax):
    """Textbook design matrix: bracket-style table with column headers
    '1 | x_1 | x_2 | x_1*x_2' (the last column is an interaction term).
    Column of 1s highlighted in orange. Wider column spacing so brackets
    don't crowd the values."""
    headers = ["1", r"$x_1$", r"$x_2$", r"$x_1 x_2$"]
    data = [
        ["1", "0.5", "0.9", "0.45"],
        ["1", "0.7", "0.8", "0.56"],
        ["1", "1.2", "0.4", "0.48"],
        ["1", "0.9", "1.5", "1.35"],
    ]
    n_rows = len(data)

    # Wider column spacing — was 1.0, now 1.35
    col_spacing = 1.35
    last_x = (len(headers) - 1) * col_spacing

    # Headers row (top)
    for j, h in enumerate(headers):
        ax.text(j * col_spacing, n_rows + 0.5, h,
                ha="center", va="center",
                fontsize=18, fontweight="bold", color=TITLE_COLOR)

    # Bracket lines around the matrix body
    body_top = n_rows - 0.4
    body_bot = -0.4
    bracket_pad = 0.95     # extra horizontal breathing room outside the cells
    left = -bracket_pad
    right = last_x + bracket_pad
    tick = 0.25            # bracket foot length
    ax.plot([left + tick, left, left, left + tick],
            [body_top, body_top, body_bot, body_bot],
            color=TITLE_COLOR, linewidth=2.2)
    ax.plot([right - tick, right, right, right - tick],
            [body_top, body_top, body_bot, body_bot],
            color=TITLE_COLOR, linewidth=2.2)

    # Highlight the column of 1s with a soft orange background
    hl_w = col_spacing * 0.65
    hl = Rectangle((-hl_w / 2, body_bot), hl_w, body_top - body_bot,
                   facecolor=BAR, alpha=0.20, edgecolor="none", zorder=1)
    ax.add_patch(hl)

    # Cell values
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            y_pos = n_rows - 1 - i
            color = BAR if j == 0 else TITLE_COLOR
            weight = "bold" if j == 0 else "normal"
            ax.text(j * col_spacing, y_pos, v,
                    ha="center", va="center",
                    fontsize=18, color=color, fontweight=weight, zorder=2)

    ax.set_xlim(left - 0.3, right + 0.3)
    ax.set_ylim(-0.9, n_rows + 1.0)
    ax.set_aspect("equal")
    _strip(ax)


def _draw_normal_eq_panel(ax):
    """The closed-form OLS solution rendered as math text, centered in the panel."""
    ax.text(0.5, 0.5, r"$\theta \; = \; (X^{\!T}\!X)^{-1} X^{\!T} y$",
            ha="center", va="center", fontsize=36, color=TITLE_COLOR,
            transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


def _draw_polynomial_panel(ax):
    """Compact scatter + cubic with two extrema, suitable for the smaller panel."""
    rng = np.random.default_rng(509)
    x = np.linspace(-2.8, 2.8, 12)
    y = x**3 / 3.0 - 2.0 * x + rng.normal(0, 0.4, x.size)
    coefs = np.polyfit(x, y, 3)
    xs = np.linspace(-2.8, 2.8, 200)
    ax.plot(xs, np.polyval(coefs, xs), color=LINE_COLOR, linewidth=4.5,
            solid_capstyle="round", zorder=3)
    ax.scatter(x, y, s=110, color=POINT_COLOR, edgecolor="white",
               linewidth=1.8, alpha=0.95, zorder=4)
    _strip(ax)


def draw_ml02_panels(fig, bbox):
    """ML 02: three side-by-side panels — design matrix, normal equation, polynomial."""
    x0, y0, w, h = bbox
    gap = 0.02
    panel_w = (w - 2 * gap) / 3

    ax1 = fig.add_axes([x0, y0, panel_w, h])
    ax1.set_facecolor(BG)
    _draw_design_matrix_panel(ax1)

    ax2 = fig.add_axes([x0 + panel_w + gap, y0, panel_w, h])
    ax2.set_facecolor(BG)
    _draw_normal_eq_panel(ax2)

    ax3 = fig.add_axes([x0 + 2 * (panel_w + gap), y0, panel_w, h])
    ax3.set_facecolor(BG)
    _draw_polynomial_panel(ax3)


# --- ML 03 sub-panels (missing data / one-hot encoding / scaling) ---

def _draw_missing_panel(ax):
    """Simple table: 3 rows x 4 cols of numeric values, with a few cells replaced
    by big red '?' markers — instantly reads as 'data with missing values'."""
    values = [
        ["1.2", "4.5",  "?",  "7.8"],
        ["2.1",  "?",  "5.6", "8.9"],
        ["3.4", "6.7",  "?",   "?"],
    ]
    rows = len(values)
    cols = len(values[0])

    for i, row in enumerate(values):
        for j, v in enumerate(row):
            y_pos = rows - 1 - i
            if v == "?":
                # Missing cell: red filled with white "?"
                rect = Rectangle((j - 0.45, y_pos - 0.45), 0.9, 0.9,
                                 facecolor=LINE_COLOR, alpha=0.95,
                                 edgecolor="white", linewidth=1.8, zorder=2)
                ax.add_patch(rect)
                ax.text(j, y_pos, "?", ha="center", va="center",
                        fontsize=28, color="white", fontweight="bold", zorder=3)
            else:
                # Normal cell: light background with the value
                rect = Rectangle((j - 0.45, y_pos - 0.45), 0.9, 0.9,
                                 facecolor="#f4f4f4", edgecolor="#dddddd",
                                 linewidth=1.5, zorder=2)
                ax.add_patch(rect)
                ax.text(j, y_pos, v, ha="center", va="center",
                        fontsize=14, color=TITLE_COLOR, zorder=3)

    ax.set_xlim(-0.7, cols - 0.3)
    ax.set_ylim(-0.7, rows - 0.3)
    ax.set_aspect("equal")
    _strip(ax)


def _draw_ohe_panel(ax):
    """One-hot encoding table with Armenian cheese feature names
    (պանիր_Լոռի, պանիր_Չանախ, պանիր_Գաուդա). Headers rotated 45° so the
    long Armenian text fits without crowding.

    Uses Sylfaen for the Armenian header text because Adamathuz is
    uppercase-only and we want the lowercase 'պանիր_' prefix."""
    col_x = [0.20, 0.50, 0.80]
    headers = ["պանիր_Լոռի", "պանիր_Չանախ", "պանիր_Գաուդա"]
    rows = [
        [1, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ]
    n_rows = len(rows)

    # Header row — Armenian rotated 35°. Anchor pulled DOWN so the rotated
    # text sits right above the data table (was 0.83 → 0.62, much closer).
    header_y = 0.62
    for j, h in enumerate(headers):
        ax.text(col_x[j], header_y, h,
                ha="left", va="bottom",
                fontsize=12, fontweight="bold", color=TITLE_COLOR,
                fontname="Sylfaen", rotation=35,
                rotation_mode="anchor",
                transform=ax.transAxes)

    # Underline sits just below the header anchor — tight visual link
    ax.plot([0.06, 0.94], [0.58, 0.58], color="#cccccc", linewidth=1.2,
            transform=ax.transAxes, zorder=1)

    # Data rows — start just below the underline (no big gap)
    row_top = 0.50
    row_bottom = 0.05
    row_step = (row_top - row_bottom) / max(n_rows - 1, 1)
    cell_half = 0.060

    for i, row in enumerate(rows):
        y_center = row_top - i * row_step
        for j, v in enumerate(row):
            x_center = col_x[j]
            if v == 1:
                rect = Rectangle((x_center - cell_half, y_center - cell_half),
                                 cell_half * 2, cell_half * 2,
                                 facecolor=LINE_COLOR, alpha=0.95,
                                 edgecolor="white", linewidth=1.8,
                                 transform=ax.transAxes, zorder=2)
                ax.add_patch(rect)
                ax.text(x_center, y_center, "1",
                        ha="center", va="center",
                        fontsize=15, color="white", fontweight="bold",
                        transform=ax.transAxes, zorder=3)
            else:
                rect = Rectangle((x_center - cell_half, y_center - cell_half),
                                 cell_half * 2, cell_half * 2,
                                 facecolor="#f4f4f4", edgecolor="#dddddd",
                                 linewidth=1.5,
                                 transform=ax.transAxes, zorder=2)
                ax.add_patch(rect)
                ax.text(x_center, y_center, "0",
                        ha="center", va="center",
                        fontsize=13, color="#999",
                        transform=ax.transAxes, zorder=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


def _draw_scaling_panel(ax):
    """Z-score and min-max scaling formulas. Uses \\mathrm{} for the variable
    letters so 'z' and 'x' render upright (not stix-italic) — much more legible
    at thumbnail scale than the default math italic."""
    # Z-score (top)
    ax.text(0.5, 0.95, "Z-SCORE", ha="center", va="top",
            fontsize=11, fontweight="bold", color="#888",
            family="DejaVu Sans", transform=ax.transAxes)
    ax.text(0.5, 0.70,
            r"$\mathrm{z} \, = \, \dfrac{\mathrm{x} - \mu}{\sigma}$",
            ha="center", va="center", fontsize=32, color=TITLE_COLOR,
            transform=ax.transAxes)

    # Separator
    ax.plot([0.1, 0.9], [0.48, 0.48], color="#dddddd", linewidth=1.2,
            transform=ax.transAxes)

    # Min-max (bottom)
    ax.text(0.5, 0.40, "MIN-MAX", ha="center", va="top",
            fontsize=11, fontweight="bold", color="#888",
            family="DejaVu Sans", transform=ax.transAxes)
    ax.text(0.5, 0.18,
            r"$\mathrm{x}' \, = \, \dfrac{\mathrm{x} - \mathrm{x}_{\min}}{\mathrm{x}_{\max} - \mathrm{x}_{\min}}$",
            ha="center", va="center", fontsize=24, color=TITLE_COLOR,
            transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


def draw_data_prep_panels(fig, bbox):
    """ML 03: three side-by-side icon panels — missing data, one-hot encoding, scaling."""
    x0, y0, w, h = bbox
    gap = 0.02
    panel_w = (w - 2 * gap) / 3

    ax1 = fig.add_axes([x0, y0, panel_w, h])
    ax1.set_facecolor(BG)
    _draw_missing_panel(ax1)

    ax2 = fig.add_axes([x0 + panel_w + gap, y0, panel_w, h])
    ax2.set_facecolor(BG)
    _draw_ohe_panel(ax2)

    ax3 = fig.add_axes([x0 + 2 * (panel_w + gap), y0, panel_w, h])
    ax3.set_facecolor(BG)
    _draw_scaling_panel(ax3)


# ---------- lesson configs ----------

LESSONS = [
    {
        "tag":        "ML 01",
        "title":      "Մեքենայական ուսուցման\nներածություն։ Գծային ռեգրեսիա",
        "title_size": 54,
        "draw":       draw_regression_simple,
        "out":        "ML01.png",
    },
    {
        "tag":        "ML 02",
        "title":      "Դիզայն մատրից, նորմալ հավասարում\nՊոլինոմիալ ռեգրեսիա",
        "title_size": 46,
        "draw":       draw_ml02_panels,
        "out":        "ML02.png",
    },
    {
        "tag":        "ML 03",
        "title":      "Տվյալների նախապատրաստում.\nբացակայող արժեքներ, կատեգորիկ սյուներ",
        "title_size": 44,
        "draw":       draw_data_prep_panels,
        "out":        "ML03.png",
    },
]


def render_thumbnail(lesson: dict) -> None:
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor(BG)

    # Vertical orange bar at left edge
    bar = fig.add_axes([0.0, 0.0, 0.024, 1.0])
    bar.set_facecolor(BAR)
    _strip(bar)

    # Lesson tag — Segoe Script handwritten, navy
    fig.text(0.06, 0.95, lesson["tag"], color=TAG_COLOR,
             fontsize=TAG_SIZE, va="top", fontname=TAG_FONT)

    # Title — Adamathuz Bold Armenian, lesson-specific size
    fig.text(0.06, 0.85, lesson["title"], color=TITLE_COLOR,
             fontsize=lesson["title_size"], fontweight="bold",
             fontproperties=ARM_PROPS,
             va="top", linespacing=TITLE_LS)

    # Illustration — draw function decides whether to use 1 axes or many
    lesson["draw"](fig, CHART_BBOX)

    out = OUT_DIR / lesson["out"]
    fig.savefig(out, facecolor=BG)
    plt.close(fig)
    log.info(f"Wrote {out}")


def main():
    log.info(f"Output dir: {OUT_DIR.resolve()}")
    for lesson in LESSONS:
        render_thumbnail(lesson)
    log.info(f"Done — rendered {len(LESSONS)} thumbnail(s)")


if __name__ == "__main__":
    main()
