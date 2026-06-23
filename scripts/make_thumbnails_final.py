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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

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

# Latin title font for English titles ("title_latin" lessons) — Bubble Sans,
# same fonter.am foundry / bold-rounded look as Adamathuz. Falls back to a bold
# sans if missing.
LATIN_FONT_PATH = Path("fonts/bubble-sans/Bubble Sans 1.01.otf")
if LATIN_FONT_PATH.exists():
    font_manager.fontManager.addfont(str(LATIN_FONT_PATH))
    LATIN_PROPS = font_manager.FontProperties(fname=str(LATIN_FONT_PATH))
    log.info(f"Loaded Latin title font: {LATIN_PROPS.get_name()}")
else:
    LATIN_PROPS = font_manager.FontProperties(family="DejaVu Sans", weight="bold")


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


# --- ML 04 Practical 01 sub-panels (gradient descent from scratch) ---

def _draw_gd_contour_panel(ax):
    """Gradient descent on the loss contours — redrawn from the course's
    `grad_desc_alpha` figure: elongated elliptical contours, an orange start
    point theta^(0), and red arrows zig-zagging down the narrow valley to the
    red-star minimum. The zig-zag is the visual signature of GD overshooting."""
    x = np.linspace(-3, 3, 240)
    y = np.linspace(-2.2, 2.2, 240)
    X, Y = np.meshgrid(x, y)
    Z = 0.18 * X**2 + 0.62 * Y**2          # elongated bowl (narrow in y)
    ax.contour(X, Y, Z, levels=[0.12, 0.32, 0.62, 1.0, 1.55, 2.2, 2.95],
               colors=POINT_COLOR, linewidths=1.4, alpha=0.55, zorder=1)
    pts = [(-2.55, 1.6), (-1.75, -0.7), (-1.05, 0.55), (-0.6, -0.22),
           (-0.32, 0.13), (-0.14, -0.05), (0.0, 0.0)]
    for i in range(len(pts) - 1):
        ax.annotate("", xy=pts[i + 1], xytext=pts[i],
                    arrowprops=dict(arrowstyle="-|>", color=LINE_COLOR,
                                    lw=2.4, shrinkA=2, shrinkB=2), zorder=3)
    ax.scatter([pts[0][0]], [pts[0][1]], s=150, color=BAR, edgecolor="white",
               linewidth=2, zorder=5)
    ax.text(pts[0][0] + 0.05, pts[0][1] + 0.42, r"$\theta^{(0)}$",
            ha="center", va="bottom", fontsize=15, color=TITLE_COLOR, zorder=6)
    ax.scatter([0], [0], s=240, color=LINE_COLOR, edgecolor="white",
               linewidth=1.5, marker="*", zorder=5)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect("auto")
    _strip(ax)


def _draw_gd_update_panel(ax):
    """The gradient-descent update rule as math text, centered in the panel."""
    ax.text(0.5, 0.5, r"$\theta \;\leftarrow\; \theta \,-\, \alpha\,\nabla R_{\mathrm{emp}}(\theta)$",
            ha="center", va="center", fontsize=29, color=TITLE_COLOR,
            transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


def _draw_lr_curves_panel(ax):
    """Loss-vs-iteration for three learning rates: too small (blue, slow),
    just right (red, smooth decay to the floor), too large (orange, diverging
    oscillation). Armenian-flag palette."""
    t = np.linspace(0, 1, 200)
    good = 0.04 + 0.92 * np.exp(-6 * t)
    slow = 0.10 + 0.85 * np.exp(-1.4 * t)
    diverge = 0.55 + 0.30 * np.sin(22 * t) * (0.25 + 0.75 * t) + 0.10 * t
    ax.plot(t, slow, color=POINT_COLOR, linewidth=4, solid_capstyle="round", zorder=2)
    ax.plot(t, diverge, color=BAR, linewidth=4, solid_capstyle="round", zorder=3)
    ax.plot(t, good, color=LINE_COLOR, linewidth=4.5, solid_capstyle="round", zorder=4)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, 1.0)
    _strip(ax)


def draw_gradient_descent_panels(fig, bbox):
    """ML 04a: three panels — loss bowl with descent steps, update rule,
    learning-rate convergence curves."""
    x0, y0, w, h = bbox
    gap = 0.02
    panel_w = (w - 2 * gap) / 3

    ax1 = fig.add_axes([x0, y0, panel_w, h])
    ax1.set_facecolor(BG)
    _draw_gd_contour_panel(ax1)

    ax2 = fig.add_axes([x0 + panel_w + gap, y0, panel_w, h])
    ax2.set_facecolor(BG)
    _draw_gd_update_panel(ax2)

    ax3 = fig.add_axes([x0 + 2 * (panel_w + gap), y0, panel_w, h])
    ax3.set_facecolor(BG)
    _draw_lr_curves_panel(ax3)


# --- ML 04 Practical 02 sub-panels (real data -> sklearn pipeline) ---

# Real bin heights from the course's House_Rent_Dataset.csv (4746 rows):
# raw Rent is heavily right-skewed; log(1+Rent) is ~bell-shaped. The thumbnail
# shows the actual class-data transform, not a synthetic stand-in.
RENT_RAW_HIST = [806, 1662, 664, 440, 258, 146, 147, 101, 49, 76, 56, 22,
                 39, 15, 18, 27, 21, 0, 38, 10, 7, 19, 11, 114]
RENT_LOG_HIST = [2, 4, 10, 53, 265, 555, 826, 827, 544, 486, 380, 227,
                 226, 94, 103, 59, 52, 20, 7, 3, 2, 0, 0, 1]


def _draw_logtransform_panel(ax):
    """The rent target's log transform on REAL course data: left = raw,
    right-skewed (blue); arrow labelled 'log'; right = bell-shaped after
    log(1+Rent) (red). Tells the signature EDA move of Practical 02."""
    raw = np.array(RENT_RAW_HIST, float)
    raw = raw / raw.max()
    logh = np.array(RENT_LOG_HIST, float)
    logh = logh / logh.max()
    n = len(raw)
    gap = 7
    ax.bar(np.arange(n), raw, width=0.96, color=POINT_COLOR,
           edgecolor="white", linewidth=0.3, zorder=2)
    ax.bar(np.arange(n) + n + gap, logh, width=0.96, color=LINE_COLOR,
           edgecolor="white", linewidth=0.3, zorder=2)
    ax.annotate("", xy=(n + gap - 1.2, 0.52), xytext=(n + 0.2, 0.52),
                arrowprops=dict(arrowstyle="-|>", color=TITLE_COLOR, lw=2.6))
    ax.text(n + gap / 2 - 0.5, 0.66, "log", ha="center", va="bottom",
            fontsize=13, fontstyle="italic", color=TITLE_COLOR)
    ax.set_xlim(-1, 2 * n + gap)
    ax.set_ylim(0, 1.08)
    _strip(ax)


def _draw_pipeline_panel(ax):
    """Vertical sklearn-Pipeline flow: Data -> Preprocessing -> Regression,
    three boxes with downward arrows. Armenian labels in Sylfaen (Adamathuz
    is uppercase-only and these are mixed-case words)."""
    labels = ["Տվյալներ", "Նախամշակում", "Գծ. ռեգրեսիա"]
    edges = [POINT_COLOR, BAR, LINE_COLOR]
    box_w, box_h = 0.80, 0.20
    cx = 0.5
    centers_y = [0.82, 0.50, 0.18]
    for cy, lab, ec in zip(centers_y, labels, edges):
        rect = Rectangle((cx - box_w / 2, cy - box_h / 2), box_w, box_h,
                         facecolor="#f7f7f7", edgecolor=ec, linewidth=2.6,
                         transform=ax.transAxes, zorder=2)
        ax.add_patch(rect)
        ax.text(cx, cy, lab, ha="center", va="center", fontsize=13,
                fontname="Sylfaen", color=TITLE_COLOR,
                transform=ax.transAxes, zorder=3)
    for cy_top, cy_bot in [(0.82, 0.50), (0.50, 0.18)]:
        ax.annotate("", xy=(cx, cy_bot + box_h / 2 + 0.005),
                    xytext=(cx, cy_top - box_h / 2 - 0.005),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="-|>", color=TITLE_COLOR, lw=2.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


def _draw_coef_panel(ax):
    """Diverging horizontal coefficient bars — some features push price up
    (blue), some down (red), around a zero axis. Mirrors the 'interpreting
    coefficients' finale."""
    vals = [0.95, 0.62, 0.40, 0.22, -0.30, -0.58]
    y = np.arange(len(vals))[::-1]
    colors = [POINT_COLOR if v >= 0 else LINE_COLOR for v in vals]
    ax.barh(y, vals, color=colors, edgecolor="white", linewidth=1.2,
            height=0.62, zorder=2)
    ax.axvline(0, color=TITLE_COLOR, linewidth=1.8, zorder=3)
    ax.set_xlim(-0.85, 1.15)
    ax.set_ylim(-0.6, len(vals) - 0.4)
    _strip(ax)


def draw_pipeline_panels(fig, bbox):
    """ML 04b: three panels — skewed target histogram, sklearn pipeline flow,
    coefficient bars."""
    x0, y0, w, h = bbox
    gap = 0.02
    panel_w = (w - 2 * gap) / 3

    ax1 = fig.add_axes([x0, y0, panel_w, h])
    ax1.set_facecolor(BG)
    _draw_logtransform_panel(ax1)

    ax2 = fig.add_axes([x0 + panel_w + gap, y0, panel_w, h])
    ax2.set_facecolor(BG)
    _draw_pipeline_panel(ax2)

    ax3 = fig.add_axes([x0 + 2 * (panel_w + gap), y0, panel_w, h])
    ax3.set_facecolor(BG)
    _draw_coef_panel(ax3)


# ---------- alternative illustration variants (for picking) ----------

# --- ML 04 variant B: data + line being fit from scratch (wide hero) ---

def draw_gd_scatter_fit(fig, bbox):
    """ML 04 alt: scatter with the regression line being learned — faint early
    gradient-descent fits fading up to the bold final red line, plus the update
    rule. Reads as 'fitting a line from scratch'."""
    ax = fig.add_axes(bbox)
    ax.set_facecolor(BG)
    rng = np.random.default_rng(509)
    x = np.linspace(0, 10, 16)
    y = 0.7 * x + 1.2 + rng.normal(0, 1.0, x.size)
    xs = np.linspace(0, 10, 100)
    final_slope, final_int = np.polyfit(x, y, 1)
    stages = [(0.05, 4.6), (0.28, 3.3), (0.5, 2.0), (final_slope, final_int)]
    alphas = [0.16, 0.30, 0.48, 1.0]
    widths = [3.0, 3.0, 3.5, 7.0]
    for (s, b), a, w in zip(stages, alphas, widths):
        ax.plot(xs, s * xs + b, color=LINE_COLOR, linewidth=w, alpha=a,
                solid_capstyle="round", zorder=3)
    ax.scatter(x, y, s=200, color=POINT_COLOR, edgecolor="white",
               linewidth=2.5, alpha=0.95, zorder=4)
    ax.text(0.975, 0.10, r"$\theta \leftarrow \theta - \alpha\,\nabla R_{\mathrm{emp}}(\theta)$",
            ha="right", va="bottom", fontsize=21, color=TITLE_COLOR,
            transform=ax.transAxes)
    _strip(ax)


# --- ML 04 variant C: contour | 3D error surface | LR curves ---

def _draw_err_surface_panel(fig, rect):
    """3D loss surface (paraboloid bowl) with a descent path — a redraw of the
    course's err_surf figure."""
    ax = fig.add_axes(rect, projection="3d")
    ax.set_facecolor(BG)
    u = np.linspace(-2, 2, 44)
    v = np.linspace(-2, 2, 44)
    U, V = np.meshgrid(u, v)
    Z = 0.5 * U**2 + V**2
    ax.plot_surface(U, V, Z, cmap="viridis", alpha=0.92, linewidth=0,
                    antialiased=True, rcount=44, ccount=44)
    px = [-1.85, -1.1, -0.62, -0.32, -0.13, 0.0]
    py = [1.7, -0.55, 0.32, -0.12, 0.05, 0.0]
    pz = [0.5 * a * a + b * b + 0.05 for a, b in zip(px, py)]
    ax.plot(px, py, pz, color=LINE_COLOR, linewidth=3, marker="o",
            markersize=4, markerfacecolor=LINE_COLOR, zorder=10)
    ax.set_axis_off()
    ax.view_init(elev=34, azim=-58)


def draw_gradient_descent_panels_surface(fig, bbox):
    """ML 04 alt: contour+path | 3D error surface | learning-rate curves."""
    x0, y0, w, h = bbox
    gap = 0.02
    pw = (w - 2 * gap) / 3
    ax1 = fig.add_axes([x0, y0, pw, h])
    ax1.set_facecolor(BG)
    _draw_gd_contour_panel(ax1)
    _draw_err_surface_panel(fig, [x0 + pw + gap, y0 - 0.03, pw, h + 0.06])
    ax3 = fig.add_axes([x0 + 2 * (pw + gap), y0, pw, h])
    ax3.set_facecolor(BG)
    _draw_lr_curves_panel(ax3)


# --- ML 05 correlation heatmap (real house-data values) ---

CORR_LABELS = ["BHK", "Size", "Bath", "Rent"]
CORR_MATRIX = [
    [1.00, 0.72, 0.79, 0.60],
    [0.72, 1.00, 0.74, 0.57],
    [0.79, 0.74, 1.00, 0.69],
    [0.60, 0.57, 0.69, 1.00],
]


def _draw_corr_heatmap_panel(ax):
    """Correlation heatmap on REAL house-data columns — the strong BHK/Size/
    Bathroom correlations the lecture flags. RdBu_r so high corr reads warm."""
    M = np.array(CORR_MATRIX)
    ax.imshow(M, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
    n = M.shape[0]
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                    fontsize=11, fontweight="bold",
                    color="white" if abs(M[i, j]) > 0.62 else TITLE_COLOR)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(CORR_LABELS, fontsize=9, color=TITLE_COLOR)
    ax.set_yticklabels(CORR_LABELS, fontsize=9, color=TITLE_COLOR)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)


def _panel_title(ax, text):
    """Small descriptive Armenian title above a panel (Sylfaen — mixed-case)."""
    ax.set_title(text, fontsize=15, fontname="Sylfaen", color=TITLE_COLOR,
                 pad=8)


def draw_pipeline_panels_heatmap(fig, bbox):
    """ML 05 alt: log transform | correlation heatmap | coefficient bars,
    each panel labelled with a short descriptive title."""
    x0, y0, w, h = bbox
    gap = 0.02
    pw = (w - 2 * gap) / 3
    ax1 = fig.add_axes([x0, y0, pw, h])
    ax1.set_facecolor(BG)
    _draw_logtransform_panel(ax1)
    _panel_title(ax1, "Վարձի log-ը")
    ax2 = fig.add_axes([x0 + pw + gap, y0, pw, h])
    ax2.set_facecolor(BG)
    _draw_corr_heatmap_panel(ax2)
    _panel_title(ax2, "Կորելացիա")
    ax3 = fig.add_axes([x0 + 2 * (pw + gap), y0, pw, h])
    ax3.set_facecolor(BG)
    _draw_coef_panel(ax3)
    _panel_title(ax3, "Գործակիցներ")


# --- ML 05 variant C: wide horizontal pipeline (hero) ---

def draw_pipeline_hero(fig, bbox):
    """ML 05 alt: a wide 4-stage sklearn-pipeline flow spanning the band —
    raw data -> preprocessing -> model -> prediction, Armenian-flag borders."""
    ax = fig.add_axes(bbox)
    ax.set_facecolor(BG)
    labels = ["Տվյալներ", "Նախամշակում", "Մոդել", "Գուշակություն"]
    edges = [POINT_COLOR, BAR, LINE_COLOR, POINT_COLOR]
    n = len(labels)
    box_w = 0.195
    box_h = 0.42
    gap = (1.0 - n * box_w) / (n - 1)
    cy = 0.5
    centers = []
    for k, (lab, ec) in enumerate(zip(labels, edges)):
        x_left = k * (box_w + gap)
        cx = x_left + box_w / 2
        centers.append(cx)
        rect = Rectangle((x_left, cy - box_h / 2), box_w, box_h,
                         facecolor="#f7f7f7", edgecolor=ec, linewidth=3.0,
                         transform=ax.transAxes, zorder=2)
        ax.add_patch(rect)
        ax.text(cx, cy, lab, ha="center", va="center", fontsize=15,
                fontname="Sylfaen", color=TITLE_COLOR,
                transform=ax.transAxes, zorder=3)
    for k in range(n - 1):
        x_start = centers[k] + box_w / 2 + 0.01
        x_end = centers[k + 1] - box_w / 2 - 0.01
        ax.annotate("", xy=(x_end, cy), xytext=(x_start, cy),
                    xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="-|>", color=TITLE_COLOR, lw=2.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _strip(ax)


# --- ML 06: embed two real course-slide plots ---

def draw_ml06_slides(fig, bbox):
    """ML 06: two actual plots lifted from the course deck
    ml_new/02_main_concepts_continued/L01d_validation_and_cv.pdf — the degree-6
    polynomial overfit demo (slide 2 / figure l01d_open_2_poly.pdf) and the k=5
    fold cross-validation grid (slide 24), cropped to thumbnails/assets/. Panel
    widths are matched to each plot's aspect so both fill the band at the same
    height; images top-aligned with captions over them."""
    x0, y0, _w, _h = bbox
    iy = y0 + 0.06         # both plots are wide/short — nudge down to center them
    img_h = 0.36
    gap = 0.04
    poly_w = 0.37          # widths matched to each plot's aspect so both fill
    cv_w = 0.49            # the band at the same height
    cap_y = iy + img_h + 0.018
    poly = plt.imread(str(OUT_DIR / "assets" / "ml06_poly.png"))
    cv = plt.imread(str(OUT_DIR / "assets" / "ml06_cv.png"))
    cv_x0 = x0 + poly_w + gap
    fig.text(x0 + poly_w / 2, cap_y, "Overfitting", ha="center", va="bottom",
             fontsize=19, fontweight="bold", color=TITLE_COLOR,
             family="DejaVu Sans")
    fig.text(cv_x0 + cv_w / 2, cap_y, "Cross-validation", ha="center",
             va="bottom", fontsize=19, fontweight="bold", color=TITLE_COLOR,
             family="DejaVu Sans")
    ax1 = fig.add_axes([x0, iy, poly_w, img_h])
    ax1.imshow(poly)
    ax1.set_anchor("N")
    ax1.axis("off")
    ax2 = fig.add_axes([cv_x0, iy, cv_w, img_h])
    ax2.imshow(cv)
    ax2.set_anchor("N")
    ax2.axis("off")


# --- generic embed of course-slide figures (ML 07-09) ---

def _draw_image_row(fig, bbox, asset_names, captions=None, gap=0.04,
                    max_h=0.42, lift=0.06):
    """Place one or more course-slide PNGs (from thumbnails/assets/) in a
    centered row. Heights are matched, so each panel's width follows its image
    aspect and the row fills the band; optional bold captions sit above."""
    x0, y0, w, _h = bbox
    imgs = [plt.imread(str(OUT_DIR / "assets" / a)) for a in asset_names]
    aspects = [im.shape[1] / im.shape[0] for im in imgs]
    k = 7.2 / 12.8                       # y-fraction to x-fraction conversion
    total_gap = gap * (len(imgs) - 1)
    fh = min(max_h, (w - total_gap) / (sum(aspects) * k))
    widths = [a * fh * k for a in aspects]
    cx = x0 + (w - (sum(widths) + total_gap)) / 2.0     # center the row
    iy = y0 + lift
    cap_y = iy + fh + 0.018
    for i, (im, wd) in enumerate(zip(imgs, widths)):
        ax = fig.add_axes([cx, iy, wd, fh])
        ax.imshow(im)
        ax.axis("off")
        if captions and captions[i]:
            fig.text(cx + wd / 2, cap_y, captions[i], ha="center", va="bottom",
                     fontsize=19, fontweight="bold", color=TITLE_COLOR,
                     family="DejaVu Sans")
        cx += wd + gap


def draw_ml07_regularization(fig, bbox):
    """ML 07: L1/L2 constraint geometry (Ridge ball vs Lasso diamond) + the
    test-error-vs-lambda U-curve. Figures fig/l03_l1_l2_geometry.pdf and
    fig/l03_mse_vs_lambda.pdf."""
    _draw_image_row(fig, bbox, ["ml07_geometry.png", "ml07_ucurve.png"])


def draw_ml08_hp_tuning(fig, bbox):
    """ML 08: the Grid / Random / Optuna search-pattern figure as a wide hero,
    sized to fill the band width. Figure fig/l01e_hp_search_patterns.pdf."""
    _draw_image_row(fig, bbox, ["ml08_search.png"], max_h=0.55)


def draw_ml09_metrics(fig, bbox):
    """ML 09: leverage / Cook's-distance (an influential point pulling the fit)
    + R^2 (variance explained vs the mean baseline), cropped from slides 29 and
    11 of 07_regression_metrics_notes.pdf."""
    _draw_image_row(fig, bbox, ["ml09_leverage.png", "ml09_r2.png"],
                    captions=["Leverage / Cook's", "R²"])


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
    # ML 04 — chosen: line-fitting hero (draw_gd_scatter_fit).
    # Alternates available to swap in: draw_gradient_descent_panels (contour
    # panels), draw_gradient_descent_panels_surface (with 3D error surface).
    {
        "tag": "ML 04", "title": "Գծային ռեգրեսիան\nզրոյից",
        "title_size": 78, "draw": draw_gd_scatter_fit,
        "practical": True, "out": "ML04.png",
    },
    # ML 05 — chosen: log transform | correlation heatmap | coefficients, with
    # per-panel titles (draw_pipeline_panels_heatmap). Alternates: draw_pipeline_panels
    # (vertical pipeline), draw_pipeline_hero (wide 4-stage flow).
    {
        "tag": "ML 05", "title": "Գծային ռեգրեսիա.\nտան վարձ գուշակել",
        "title_size": 50, "draw": draw_pipeline_panels_heatmap,
        "practical": True, "out": "ML05.png",
    },
    # ML 06 — theory lecture (no practical badge); embeds two real course-slide
    # plots: the polynomial overfit demo and the cross-validation diagram.
    {
        "tag": "ML 06", "title": "Մոդելի գնահատում",
        "title_size": 58, "draw": draw_ml06_slides,
        "out": "ML06.png",
    },
    # ML 07-09 — theory lectures (no badge); embed real course-slide figures.
    {
        "tag": "ML 07", "title": "Ռեգուլյարիզացիա",
        "title_size": 54, "title_max": 86, "draw": draw_ml07_regularization,
        "out": "ML07.png",
    },
    {
        "tag": "ML 08", "title": "Hyperparameter Tuning",
        "title_size": 40, "title_max": 60, "title_latin": True,
        "draw": draw_ml08_hp_tuning, "out": "ML08.png",
    },
    {
        "tag": "ML 09", "title": "Ռեգրեսիայի մետրիկաներ",
        "title_size": 50, "draw": draw_ml09_metrics,
        "out": "ML09.png",
    },
]


def _fit_single_line_size(fig, text, configured, max_size=74, fontkw=None,
                          x0=0.06, x_right=0.94):
    """Single-line titles aren't text-heavy, so grow them to fill the available
    width (up to max_size) for more impact; never shrink below the configured
    size. Multi-line titles keep their tuned size (height-constrained)."""
    if fontkw is None:
        fontkw = {"fontproperties": ARM_PROPS, "fontweight": "bold"}
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    probe = fig.text(x0, 0.85, text, fontsize=max_size, va="top", **fontkw)
    w = probe.get_window_extent(renderer).width
    probe.remove()
    if w <= 0:
        return configured
    avail = (x_right - x0) * fig.bbox.width
    fit = min(max_size, max_size * avail / w)
    return max(configured, fit)


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

    # "Գործնական" (practical) badge — top-right orange pill, white Armenian
    # text in the title font. Marks the video as a hands-on/practical session.
    if lesson.get("practical"):
        fig.text(0.963, 0.925, "Գործնական", ha="right", va="center",
                 fontsize=31, fontproperties=ARM_PROPS, color="white",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor=BAR,
                           edgecolor="none"))

    # Title — Adamathuz Bold Armenian by default; "title_latin" lessons use a
    # bold Latin font (Adamathuz has no Latin glyphs). Single-line titles
    # auto-grow to fill the width (up to title_max); multi-line keep their size.
    title = lesson["title"]
    tsize = lesson["title_size"]
    if lesson.get("title_latin"):
        fontkw = {"fontproperties": LATIN_PROPS}
    else:
        fontkw = {"fontproperties": ARM_PROPS, "fontweight": "bold"}
    if "\n" not in title:
        tsize = _fit_single_line_size(fig, title, tsize,
                                      max_size=lesson.get("title_max", 74),
                                      fontkw=fontkw)
    fig.text(0.06, 0.85, title, color=TITLE_COLOR, fontsize=tsize,
             va="top", linespacing=TITLE_LS, **fontkw)

    # Illustration — draw function decides whether to use 1 axes or many
    lesson["draw"](fig, CHART_BBOX)

    out = OUT_DIR / lesson["out"]
    fig.savefig(out, facecolor=BG)
    plt.close(fig)
    log.info(f"Wrote {out}")


def main():
    log.info(f"Output dir: {OUT_DIR.resolve()}")
    # Optional CLI filter: render only lessons whose output filename contains
    # one of the given substrings (e.g. `python make_thumbnails_final.py ML04`).
    # No args -> render everything.
    selected = sys.argv[1:]
    lessons = [l for l in LESSONS
               if not selected or any(s in l["out"] for s in selected)]
    for lesson in lessons:
        render_thumbnail(lesson)
    log.info(f"Done — rendered {len(lessons)} thumbnail(s)")


if __name__ == "__main__":
    main()
