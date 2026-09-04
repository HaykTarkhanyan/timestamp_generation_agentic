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
from matplotlib.patches import Rectangle, Circle
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
# Left-stripe colour for the unsupervised block of the course (ML32 on). House
# navy - the same blue as the ML tag, so stripe and tag read as one unit and the
# thumbnails stay inside the three-colour palette, while the section change is
# still obvious next to the orange supervised lessons.
UNSUP_BAR = "#0033A0"
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

# English titles ("title_latin" lessons) render in Comic Sans MS Bold — the
# closest system font to Adamathuz's chunky rounded look (chosen over Bubble
# Sans / Arial Rounded).
LATIN_FONTKW = {"fontfamily": "Comic Sans MS", "fontweight": "bold"}


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


# --- ML 10 (practical): "find the mistakes" buggy-code panel ---

def draw_ml10_checklist(fig, bbox):
    """ML 10 practical: the planted ML mistakes as a 2x2 red-✗ grid — each bug
    *category* (bold) with the offending detail as a gray subtitle. No correct
    line is shown; the viewer is left to find them. Legible at thumbnail size."""
    ax = fig.add_axes(bbox)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    _strip(ax)
    items = [
        ("Data leakage", "fit() անել split-ից առաջ"),
        ("Չֆիքսված seed", "random_state չկա"),
        ("Սխալ մետրիկա", "R² տարբեր dataset-երի վրա"),
        ("Առանց feature scaling",
         "Ridge/Lasso օգտագործել,\nգործակիցներ համեմատել"),
    ]
    # faint 2x2 quadrant dividers
    ax.axvline(0.50, color="#e8eaed", linewidth=1.6, zorder=1)
    ax.axhline(0.50, color="#e8eaed", linewidth=1.6, zorder=1)
    cols = [0.015, 0.535]          # ✗ x for left / right column
    rows = [0.74, 0.24]            # center y for top / bottom row
    for i, (head, sub) in enumerate(items):
        cx, cy = cols[i % 2], rows[i // 2]
        ax.text(cx, cy, "✗", ha="center", va="center", fontsize=36,
                color=LINE_COLOR, fontweight="bold", zorder=4)
        # heads mix Armenian + Latin terms, so use the default dual-script sans
        # (DejaVu) rather than Latin-less Adamathuz. Subtitle is top-anchored so
        # 1-line and 2-line tiles keep their first line aligned.
        ax.text(cx + 0.055, cy + 0.10, head, ha="left", va="center", fontsize=25,
                color=TITLE_COLOR, fontweight="bold", zorder=4)
        ax.text(cx + 0.055, cy - 0.02, sub, ha="left", va="top", fontsize=15,
                color="#6b7280", family="monospace", linespacing=1.5, zorder=4)


def draw_ml11_logreg(fig, bbox):
    """ML 11: logistic regression — the decision boundary (probability surface +
    orange 0.5 boundary, fig/logreg_boundary_2d.pdf) next to the sigmoid curve
    that produces it (synthetic, same orange 0.5 threshold). Tells the full
    'score → sigmoid → probability → boundary' story."""
    _draw_image_row(fig, bbox, ["ml11_boundary.png", "ml11_sigmoid.png"],
                    gap=0.05, max_h=0.48, lift=0.07)


def draw_ml12_metrics(fig, bbox):
    """ML 12: classification metrics — the 2-model ROC-vs-PR comparison (Model A
    vs B look alike on ROC but B collapses on PR, fig/cm_roc_vs_pr.pdf) next to
    the F1 harmonic-mean heatmap (cm_f1_heatmap left panel)."""
    _draw_image_row(fig, bbox, ["ml12_rocpr.png", "ml12_f1.png"],
                    captions=["ROC-AUC vs PR-AUC", "F1"], gap=0.04, max_h=0.46)


def draw_ml13_threshold(fig, bbox):
    """ML 13: threshold tuning — every metric as a function of the threshold
    (recall/precision/F1 crossing, F1-best far below 0.5, fig/cm_threshold_metrics.pdf)
    next to Youden's J on the ROC (farthest point above the diagonal,
    fig/cm_youden.pdf). The two 'how to pick the cutoff' methods side by side."""
    _draw_image_row(fig, bbox, ["ml13_threshold.png", "ml13_youden.png"],
                    captions=["Metrics vs threshold", "Youden's J"],
                    gap=0.04, max_h=0.46)


def draw_ml14_calibration(fig, bbox):
    """ML 14: calibration — the reliability diagram (predicted vs observed
    frequency, below-diagonal = over-confident, fig/cal_reliability.pdf) next to
    the before/after isotonic fix that pulls the curve back onto the diagonal
    (fig/cal_before_after.pdf). Diagnosis then cure."""
    _draw_image_row(fig, bbox, ["ml14_reliability.png", "ml14_after.png"],
                    captions=["Reliability diagram", "After isotonic"],
                    gap=0.04, max_h=0.46)


def draw_ml15_imbalance(fig, bbox):
    """ML 15: data imbalance — the resampling grid (Original vs ROS/RUS/SMOTE on
    the same 600/40 majority/minority scatter, fig/imb_resampling_2d.pdf) next to
    Tomek links (drop the borderline majority point of each opposite-class
    nearest-neighbour pair, fig/imb_tomek.pdf)."""
    _draw_image_row(fig, bbox, ["ml15_resampling.png", "ml15_tomek.png"],
                    captions=["Resampling", "Tomek links"],
                    gap=0.04, max_h=0.46)


def draw_ml16_practical(fig, bbox):
    """ML 16 (practical): bank-marketing classification — the REAL plots from the
    solution notebook (16_bank_marketing_solution.ipynb), not the lecture's
    synthetic figures. Its lift-per-decile + cumulative-capture chart split into
    two panels: the top-scored 10% converts ~4x the base rate, and calling just
    the top decile already catches ~40% of subscribers (the practical's business
    headline)."""
    # each panel keeps its own title from the notebook, so no extra captions
    _draw_image_row(fig, bbox, ["ml16_lift.png", "ml16_capture.png"],
                    gap=0.05, max_h=0.48, lift=0.07)


def _mini_tree(ax, cx, cy, color, half_w=0.085, h=0.44, node_s=300, lw=6):
    """A small 7-node binary tree (root, 2 internal, 4 leaves) centered at (cx, cy)
    in axes coords — chunky gray edges, filled colored nodes with white rims.
    The visual building block of the boosting 'tree + tree + ...' schematic."""
    top, bot = cy + h / 2, cy - h / 2
    root = (cx, top)
    a, b = (cx - 0.55 * half_w, cy), (cx + 0.55 * half_w, cy)
    la1, la2 = (cx - 0.85 * half_w, bot), (cx - 0.25 * half_w, bot)
    lb1, lb2 = (cx + 0.25 * half_w, bot), (cx + 0.85 * half_w, bot)
    for (x1, y1), (x2, y2) in [(root, a), (root, b), (a, la1), (a, la2),
                               (b, lb1), (b, lb2)]:
        ax.plot([x1, x2], [y1, y2], color="#aab2c0", linewidth=lw,
                solid_capstyle="round", zorder=2)
    pts = [root, a, b, la1, la2, lb1, lb2]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=node_s, color=color,
               edgecolor="white", linewidth=1.6, zorder=3)


def draw_boosting_trees(fig, bbox):
    """Boosting as 'start with one tree, then keep adding trees to fix the rest' —
    a 3-step progression in the style of the classic GBDT schematic, rebuilt on
    white. Course notation (running model F, base learners f, no y-hat):
    F1 = f1(x)  ->  F2 = F1 + f2(x)  ->  F3 = F2 + f3(x). Trees appear in
    Armenian-flag order: red, then blue, then yellow/orange."""
    ax = fig.add_axes(bbox)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    _strip(ax)
    RED, BLUE, YEL = LINE_COLOR, POINT_COLOR, BAR
    eq_y, ty = 0.87, 0.36
    tkw = dict(half_w=0.055, h=0.42, node_s=175, lw=5.5)
    plus = dict(ha="center", va="center", fontsize=30, color=TITLE_COLOR, fontweight="bold")
    eqkw = dict(ha="center", va="center", fontsize=26, color=TITLE_COLOR)
    arrow = dict(arrowstyle="-|>", color="#9aa3b2", lw=3.5)

    # step 1 — first tree
    ax.text(0.10, eq_y, r"$F_1 = f_1(x)$", **eqkw)
    _mini_tree(ax, 0.10, ty, RED, **tkw)
    ax.annotate("", xy=(0.205, ty), xytext=(0.15, ty), arrowprops=arrow)

    # step 2 — add a second tree
    ax.text(0.35, eq_y, r"$F_2 = F_1 + f_2(x)$", **eqkw)
    _mini_tree(ax, 0.28, ty, RED, **tkw)
    ax.text(0.35, ty, "+", **plus)
    _mini_tree(ax, 0.42, ty, BLUE, **tkw)
    ax.annotate("", xy=(0.535, ty), xytext=(0.485, ty), arrowprops=arrow)

    # step 3 — add a third tree
    ax.text(0.74, eq_y, r"$F_3 = F_2 + f_3(x)$", **eqkw)
    _mini_tree(ax, 0.60, ty, RED, **tkw)
    ax.text(0.67, ty, "+", **plus)
    _mini_tree(ax, 0.74, ty, BLUE, **tkw)
    ax.text(0.81, ty, "+", **plus)
    _mini_tree(ax, 0.88, ty, YEL, **tkw)


def draw_random_forest(fig, bbox):
    """Random forest as parallel, independent trees whose outputs are AVERAGED —
    the visual counterpoint to boosting's sequential sum. Three trees (red, blue,
    yellow) side by side, arrows converging into the mean (1/M) sum_m f_m(x)."""
    ax = fig.add_axes(bbox)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    _strip(ax)
    tkw = dict(half_w=0.062, h=0.40, node_s=185, lw=5.5)
    tree_y, box_cy = 0.70, 0.15
    xs = [0.18, 0.50, 0.82]
    for cx, c in zip(xs, [LINE_COLOR, POINT_COLOR, BAR]):
        _mini_tree(ax, cx, tree_y, c, **tkw)
    for cx in xs:
        ax.annotate("", xy=(0.50, box_cy + 0.10), xytext=(cx, tree_y - 0.235),
                    arrowprops=dict(arrowstyle="-|>", color="#9aa3b2", lw=3.5,
                                    shrinkA=2, shrinkB=6))
    ax.text(0.50, box_cy, r"$\hat{f}(x)\;=\;\dfrac{1}{M}\,\sum_{m=1}^{M} f_m(x)$",
            ha="center", va="center", fontsize=34, color=TITLE_COLOR,
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#f6f7f9",
                      edgecolor="#c2c8d2", linewidth=1.8))


def draw_ml20_logos(fig, bbox):
    """ML 20 (advanced boosting): the three production gradient-boosting library
    logos in a full-width row — XGBoost, LightGBM, CatBoost (user-provided images,
    trimmed onto white in thumbnails/assets/). Heights are matched and the row
    spans the band so there's no dead space on the sides."""
    x0, y0, w, h = bbox
    names = ["ml20_xgboost.png", "ml20_lightgbm.png", "ml20_catboost.png"]
    imgs = [plt.imread(str(OUT_DIR / "assets" / n)) for n in names]
    aspects = [im.shape[1] / im.shape[0] for im in imgs]
    k = 7.2 / 12.8
    gap = 0.03
    total_gap = gap * (len(imgs) - 1)
    fh = min(h, (w - total_gap) / (sum(aspects) * k))     # fill the full width
    widths = [a * fh * k for a in aspects]
    cx = x0 + (w - (sum(widths) + total_gap)) / 2.0
    iy = y0 + (h - fh) / 2.0                               # center vertically
    for im, wd in zip(imgs, widths):
        ax = fig.add_axes([cx, iy, wd, fh])
        ax.imshow(im)
        ax.axis("off")
        cx += wd + gap


def draw_ml21_importances(fig, bbox):
    """ML 21 (trees practical): a tornado chart contrasting how a TREE model and a
    LINEAR model rank the SAME features - the lecture's key 'aha'. education is a
    top feature for the tree but ~useless to the linear model (the relationship is
    non-linear); age is the reverse. Left bars = tree (red), right = linear (blue),
    feature names down the middle, value labels on every bar."""
    ax = fig.add_axes(bbox)
    ax.set_xlim(-1, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    _strip(ax)

    feats = ["capital", "age", "edu-num", "relation"]
    tree  = [0.34, 0.20, 0.30, 0.16]   # tree ranks edu-num high
    lin   = [0.14, 0.42, 0.04, 0.36]   # linear calls edu-num ~useless

    gap = 0.20                          # half-width of the center label gutter
    max_len = 0.68                      # bar extent per side (leaves room for labels)
    scale = max_len / max(max(tree), max(lin))
    ys = np.linspace(0.70, 0.14, len(feats))
    bar_h = 0.11

    ax.text(-(gap + max_len / 2), 0.90, "TREE", ha="center", va="center",
            fontsize=26, color=LINE_COLOR, **LATIN_FONTKW)
    ax.text(gap + max_len / 2, 0.90, "LINEAR", ha="center", va="center",
            fontsize=26, color=POINT_COLOR, **LATIN_FONTKW)

    for y, f, t, l in zip(ys, feats, tree, lin):
        wl = t * scale
        ax.add_patch(Rectangle((-gap - wl, y - bar_h / 2), wl, bar_h,
                               facecolor=LINE_COLOR, edgecolor="none"))
        ax.text(-gap - wl - 0.02, y, f"{t:.2f}", ha="right", va="center",
                fontsize=15, color=LINE_COLOR, fontweight="bold")
        wr = l * scale
        ax.add_patch(Rectangle((gap, y - bar_h / 2), wr, bar_h,
                               facecolor=POINT_COLOR, edgecolor="none"))
        ax.text(gap + wr + 0.02, y, f"{l:.2f}", ha="left", va="center",
                fontsize=15, color=POINT_COLOR, fontweight="bold")
        ax.text(0, y, f, ha="center", va="center", fontsize=15,
                color=TITLE_COLOR, fontweight="bold")


def draw_ml17_tree(fig, bbox):
    """ML 17: decision trees — the colored Titanic tree as a solo hero
    (fig/titanic_tree.pdf): if-else splits on gender / age / pclass, leaves shaded
    orange=died / blue=survived. The single most recognizable 'this is a decision
    tree' image; pairing it with the (very wide) staircase would squish both."""
    _draw_image_row(fig, bbox, ["ml17_tree.png"], max_h=0.52, lift=0.05)


def draw_ml22_blackbox(fig, bbox):
    """ML 22 (interpretability 1): the lecture's black box vs glass box framing.
    Left: an opaque charcoal box with a white '?' — data in, answer out, but we
    can't see inside (GPT, big boosting ensembles). Right: a glass box holding the
    course's REAL shallow bike-rentals tree (fig/tree_bike.pdf, via pdf_to_asset)
    — an intrinsically interpretable model we can just read. Labels in the bold
    Latin font (the lecturer's own terms)."""
    x0, y0, w, h = bbox
    ax = fig.add_axes(bbox)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    _strip(ax)

    box_h, cy = 0.60, 0.54
    black_cx, black_w = 0.18, 0.24
    glass_cx, glass_w = 0.70, 0.40      # wider — it holds the real tree

    # Left: black box — opaque charcoal, big white "?"
    ax.add_patch(Rectangle((black_cx - black_w / 2, cy - box_h / 2), black_w, box_h,
                           facecolor="#23262e", edgecolor="#0e0e0e", linewidth=3,
                           zorder=2))
    ax.text(black_cx, cy, "?", ha="center", va="center", fontsize=96,
            color="white", zorder=3, **LATIN_FONTKW)

    # Right: glass box — white fill, blue rim; the REAL tree inset inside it
    ax.add_patch(Rectangle((glass_cx - glass_w / 2, cy - box_h / 2), glass_w, box_h,
                           facecolor="white", edgecolor=POINT_COLOR, linewidth=3,
                           zorder=2))
    tree = plt.imread(str(OUT_DIR / "assets" / "ml22_tree.png"))
    pad = 0.08                          # inner padding as a fraction of the box
    ins = fig.add_axes([
        x0 + (glass_cx - glass_w / 2 + pad * glass_w) * w,
        y0 + (cy - box_h / 2 + pad * box_h) * h,
        glass_w * (1 - 2 * pad) * w,
        box_h * (1 - 2 * pad) * h,
    ])
    ins.imshow(tree)
    ins.axis("off")

    # labels beneath each box
    lab_y = cy - box_h / 2 - 0.10
    ax.text(black_cx, lab_y, "black box", ha="center", va="top", fontsize=23,
            color=TITLE_COLOR, **LATIN_FONTKW)
    ax.text(glass_cx, lab_y, "glass box", ha="center", va="top", fontsize=23,
            color=TITLE_COLOR, **LATIN_FONTKW)


def draw_ml23_two(fig, bbox):
    """ML 23 (chosen): two real course figures side by side — permutation feature
    importance bars (fig/pfi_bar.pdf, 'how important is each feature') and the
    ICE+PDP fan (fig/ice_pdp_bike_temp.pdf, 'how does temp affect the prediction').
    The two halves of the model-agnostic toolkit."""
    _draw_image_row(fig, bbox, ["ml23_pfi.png", "ml23_pdp_ice.png"],
                    captions=["Feature importance", "PDP + ICE"],
                    gap=0.05, max_h=0.46)


def draw_ml23_pdp_real(fig, bbox):
    """ML 23 alt: just the course's REAL ICE+PDP figure on bike temperature
    (fig/ice_pdp_bike_temp.pdf) as a solo hero. draw_ml23_pdp below is the
    synthetic fallback."""
    _draw_image_row(fig, bbox, ["ml23_pdp_ice.png"], max_h=0.54, lift=0.06)


def draw_ml23_pdp(fig, bbox):
    """ML 23 (interpretability 2): the partial dependence plot — a bold red PDP
    (the average effect) riding over a fan of faint blue ICE curves (one per row).
    The rise-then-fall shape is the lecture's temperature effect: bike rentals
    climb as it warms, then drop once it's too hot. The signature model-agnostic
    'how does this feature affect the prediction' graph."""
    ax = fig.add_axes(bbox)
    ax.set_facecolor(BG)
    rng = np.random.default_rng(509)
    xs = np.linspace(0, 1, 200)

    def hump(shift, amp):
        return amp * np.exp(-((xs - (0.60 + shift)) ** 2) / (2 * 0.17 ** 2))

    # ICE curves: same rise-then-fall shape, each row a vertical offset + jitter
    for _ in range(16):
        off = rng.normal(0, 0.06)
        amp = 1.0 + rng.normal(0, 0.12)
        sh = rng.normal(0, 0.04)
        ax.plot(xs, 0.12 + off + hump(sh, amp), color=POINT_COLOR,
                linewidth=1.6, alpha=0.22, zorder=2)

    # PDP mean — bold red on top
    ax.plot(xs, 0.12 + hump(0, 1.0), color=LINE_COLOR, linewidth=7,
            solid_capstyle="round", zorder=4)

    ax.text(0.63, 1.24, "PDP", ha="center", va="center", fontsize=21,
            color=LINE_COLOR, **LATIN_FONTKW)
    ax.text(0.13, 0.70, "ICE", ha="center", va="center", fontsize=16,
            color=POINT_COLOR, alpha=0.75, **LATIN_FONTKW)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.4)
    _strip(ax)


def draw_ml24_two(fig, bbox):
    """ML 24 / IML 3 (chosen): the two most iconic real course figures, big - the
    SHAP beeswarm (fig/shap_beeswarm.pdf) and the famous LIME wolf-vs-husky 'snow
    detector' strip (fig/lime_husky.png). Counterfactuals stays named in the title.
    draw_ml24_three below is the 3-panel alternate (adds cf_flip_bank)."""
    _draw_image_row(fig, bbox, ["ml24_shap.png", "ml24_lime.png"],
                    captions=["SHAP", "LIME"], gap=0.05, max_h=0.48)


def draw_ml24_three(fig, bbox):
    """ML 24 / IML 3 alternate: three REAL course figures in a row, one per method
    - SHAP beeswarm, the LIME wolf-vs-husky 'snow detector' strip, and a
    counterfactual bank-flip (fig/cf_flip_bank.pdf). Left-to-right matches the
    title 'SHAP - LIME - Counterfactuals'."""
    _draw_image_row(fig, bbox, ["ml24_shap.png", "ml24_lime.png", "ml24_cf.png"],
                    gap=0.035, max_h=0.42)


def draw_ml25_toolkit(fig, bbox):
    """ML 25 / IML practical (Գործնական): three REAL figures from the practical's OWN
    notebook (25_startup_success_solution.ipynb), run on the startup-success data -
    NOT the lecture's teaching figures. Permutation importance bars, the SHAP
    beeswarm, and the local SHAP waterfall for the failing test company #13 (the one
    the counterfactual targets). Reads left-to-right: importance -> global -> local."""
    _draw_image_row(fig, bbox, ["ml25_pfi.png", "ml25_shap.png", "ml25_local.png"],
                    captions=["PFI", "Global SHAP", "Local SHAP"],
                    gap=0.035, max_h=0.40)


def draw_ml26_fe(fig, bbox):
    """ML 26 / feature engineering (lecture): two REAL slide figures on the bike
    dataset - binning a continuous feature (raw-vs-binned temperature, red line vs
    blue step-bins vs orange decile curve, fig/fe_binning_temp.pdf, left panel) and
    the temp*workingday interaction helping Ridge (+6.9 MAE) but not the tree (-1.1)
    (fig/fe_interaction_lin_vs_tree.pdf). Scatter + bars, two core FE techniques."""
    _draw_image_row(fig, bbox, ["ml26_binning.png", "ml26_interactions.png"],
                    captions=["Binning", "Interactions"], gap=0.05, max_h=0.48)


def draw_ml27_fs(fig, bbox):
    """ML 27 / feature selection (lecture): two REAL slide figures - the RFE
    cross-validation curve dipping to the orange k=45 marker (fig/fs_rfecv_curve.pdf,
    left panel, 'how few features can I keep') and the Boruta shadow bars, blue=kept /
    red=rejected below the dashed 'bar to beat' (fig/fs_boruta_shadow.pdf, 'which to
    keep vs noise'). The two headline selection methods of the lesson."""
    _draw_image_row(fig, bbox, ["ml27_rfecv.png", "ml27_boruta.png"],
                    captions=["RFE-CV", "Boruta"], gap=0.05, max_h=0.46)


def draw_ml28_classics(fig, bbox):
    """ML 28 / classic methods (lecture): three REAL slide figures, one per method
    family the roundup covers - LDA's shared-covariance linear boundary with the
    class Gaussians (fig/cm_lda_qda.pdf, left panel), the SVM max-margin boundary
    with circled support vectors (fig/cm_svm_margin.pdf), and the Gaussian-process
    band that pinches at data and balloons away (fig/cm_gp_band.pdf). SVM centered
    (the lesson's star). LDA replaces KNN per the user's pick."""
    _draw_image_row(fig, bbox, ["ml28_lda.png", "ml28_svm.png", "ml28_gp.png"],
                    captions=["LDA", "SVM", "Gaussian process"],
                    gap=0.04, max_h=0.44)


def draw_ml29_classical_ts(fig, bbox):
    """ML 29 / classical time series (lecture): the two REAL figures that carry the
    classical workflow - the ACF/PACF pair you read model orders off
    (fig/acf_pacf.pdf, PACF cutting off after lag 2 => AR(2)) and the SARIMA
    'airline model' forecast with its 95% band against the held-out actual
    (fig/arima_forecast.pdf). The ACF asset is cropped to the ACF panel alone: with
    both stem panels the row is width-limited and both figures shrink. Alternative
    asset kept: ml29_rolling.png, the raw/rolling(3)/rolling(12) smoothing figure
    from fig/rolling_mean.pdf."""
    _draw_image_row(fig, bbox, ["ml29_acf.png", "ml29_sarima.png"],
                    captions=["ACF", "SARIMA forecast"],
                    gap=0.05, max_h=0.44, lift=0.04)


def draw_ml30_ml_ts(fig, bbox):
    """ML 30 / time series with ML (lecture): the lesson's headline figure as a wide
    hero - gradient boosting on a trending series, raw-level predictions stuck
    under the largest y seen in training (red, MAE 19.0) next to the same model
    trained on differences and added back (green, MAE 6.7). Figure
    fig/gbm_forecast.pdf. Alternative asset kept: ml30_window.png, the sliding
    window (X, y) table from fig/supervised_reframe.pdf."""
    _draw_image_row(fig, bbox, ["ml30_gbm.png"], max_h=0.52, lift=0.03)


def draw_ml31_ts_practical(fig, bbox):
    """ML 31 / time-series practical: plots from the practical's OWN notebook
    (ml/08_time_series/31_electricity_forecast_solution.ipynb) - the monthly
    Armenian electricity/gas/steam series in billion drams, and the held-out 2025
    year with the baseline plus the best of each model family (SARIMA,
    Holt-Winters mul, LightGBM). NOT the lecture's fig/ figures: a practical runs
    the methods on its own dataset, so fig/ would show the wrong data.

    Shown as a single wide hero: both notebook plots are ~3:1, so a two-panel row
    collapses to thin unreadable ribbons (heights are matched, so the row height is
    capped by the summed aspects). Alternative assets kept: ml31_series.png (the
    full monthly series) and ml31_years.png (yearly totals, the dropped pre-2014
    years in red)."""
    _draw_image_row(fig, bbox, ["ml31_forecast.png"],
                    captions=["2025 forecast vs actual"],
                    max_h=0.50, lift=0.03)


def draw_ml32_clustering(fig, bbox):
    """ML 32 / clustering (lecture): one panel per algorithm family. Left is the
    "k-means be like" meme the user picked (four people each holding back their own
    ball-pit cluster) - it reads as k-means partitioning space far faster than a
    scatter plot does. Then DBSCAN recovering the concentric rings with noise marked
    x (right panel of fig/clu_dbscan_circles.pdf), and the Ward dendrogram you cut to
    pick the cluster count (fig/clu_dendrogram.pdf, right 30% cropped so the meme
    gets more width - the row is width-limited by the summed aspects). Alternative
    asset kept: ml32_kmeans.png, the real k-means-on-rings panel."""
    _draw_image_row(fig, bbox, ["ml32_kmeans_meme.png", "ml32_dbscan.png", "ml32_dendro.png"],
                    captions=["K-means", "DBSCAN", "Dendrogram"],
                    gap=0.04, max_h=0.46)


def draw_ml33_color_spaces(fig, bbox):
    """ML 33 / colour spaces (lecture + project brief): the project's own before/after
    - the Saryan painting at its original 196,680 colours next to the k-means
    16-colour quantization (fig/clu_image_quantization.pdf, split into its two
    panels) - plus the hue channel from fig/hsv_space.pdf, which shows what the image
    looks like when you keep only "which colour" and throw away purity and
    brightness."""
    _draw_image_row(fig, bbox, ["ml33_original.png", "ml33_quantized.png", "ml33_hue.png"],
                    captions=["Original", "16 colors", "HSV: hue"],
                    gap=0.05, max_h=0.46)


def draw_ml34_land_cover(fig, bbox):
    """ML 34 / clustering practical: panels from the practical's OWN notebook
    (ml/09_clustering/34_land_cover_solution.ipynb) - the Sentinel-2 true-colour
    view of the Sevan shoreline, the k-means k=5 segmentation fitted on all six
    bands, and the ESA WorldCover 2021 map used as the ground truth. Same scene
    three ways, so the thumbnail reads as input -> our result -> reality. NOT the
    lecture's fig/ figures: a practical runs on its own dataset."""
    _draw_image_row(fig, bbox, ["ml34_truecolor.png", "ml34_kmeans.png", "ml34_truth.png"],
                    captions=["True colour", "K-means k=5", "Ground truth"],
                    gap=0.045, max_h=0.46)


def draw_ml35_quantization(fig, bbox):
    """ML 35 / colour-quantization practical: the lesson's own k-means quantization run
    on the user-supplied shrek.webp (ml/09_clustering/img/), whose white top/bottom
    margins are trimmed first. 28,029 colours down to 4 and to 32 - a paint-by-numbers
    style source posterizes cleanly, so the 4-colour panel is unmistakably broken while
    32 is hard to fault, which is the whole point of the lesson. Regenerated by
    scratchpad/quantize_shrek.py (seed 509). Alternative assets kept: ml35_original /
    ml35_k4 / ml35_k32, the same three panels on the Saryan painting."""
    _draw_image_row(fig, bbox,
                    ["ml35_shrek_original.png", "ml35_shrek_k4.png", "ml35_shrek_k32.png"],
                    captions=["28,029 colors", "4 colors", "32 colors"],
                    gap=0.03, max_h=0.60, lift=0.01)


def draw_ml36_pca(fig, bbox):
    """ML 36 / PCA (lecture): the eigen-garments from fig/dr_eigengarments.pdf -
    the mean Fashion-MNIST garment plus the first two principal components as
    red/blue loading maps. Panels are near-square (419x407), so the row is
    width-limited at max_h 0.50 and fills the band edge to edge. Split out of the
    7-panel figure by scripts/non_essential/split_figure_panels.py."""
    _draw_image_row(fig, bbox,
                    ["ml36_eigen_1.png", "ml36_eigen_2.png", "ml36_eigen_3.png"],
                    captions=["mean garment", "PC1 (29%)", "PC2 (18%)"],
                    gap=0.03, max_h=0.50, lift=0.02)


def draw_ml37_tsne_umap(fig, bbox):
    """ML 37 / t-SNE + UMAP (lecture): the Google PAIR woolly mammoth the lesson
    spends its UMAP section on - the 3-D skeleton and its 2-D UMAP projection,
    where trunk, legs and tusks each survive as their own structure. From
    fig/borrowed/pair/umap_elephant.png, split by split_figure_panels.py with
    --gutter-tol 2 (a couple of stray points bridge the column between the two
    plots, so a zero-tolerance scan reads them as one). Only two panels and both
    near-square, so the row is height-bound, not width-bound - it cannot fill
    the band at any sane height. Height is bought by sitting the row lower
    (y0 0.03, no lift) rather than by raising it into the title, which is why
    max_h can be 0.635 while the captions stay where 0.61 put them. Alternative
    assets kept: ml37_cmp_1/2/3, the Fashion-MNIST PCA vs t-SNE vs UMAP
    comparison."""
    _draw_image_row(fig, bbox,
                    ["ml37_mammoth_1.png", "ml37_mammoth_2.png"],
                    captions=["original 3D", "UMAP projection"],
                    gap=0.03, max_h=0.635, lift=0.0)


def draw_ml38_genes(fig, bbox):
    """ML 38 / dimensionality-reduction practical: panel a of Novembre et al.
    2008 (fig/borrowed/novembre2008_fig1.jpg) - the PCA of European genomes that
    comes out shaped like the map of Europe, with the real map inset. The user
    asked for this figure and only its top part, so panels b and c are cropped
    off (--crop-bottom 0.42) and the "a" label dropped by raising
    --min-width-frac above its width.

    A lone 1.21-aspect panel cannot fill a 16:9 band: filling the width would
    need fh > 1. So it runs as a centered hero with no caption, pushed as tall
    as the title allows; the side margins are geometry, not slack."""
    _draw_image_row(fig, bbox, ["ml38_genes_1.png"], max_h=0.68, lift=0.0)


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
    # ML 10 — practical (Գործնական badge); "find the ML mistakes" bug checklist.
    # Mixed "ML սխալները" title (Latin ML + Armenian, each in its own font).
    {
        "tag": "ML 10",
        "title_segments": [("ML", "latin"), (" սխալներ", "arm")],
        "title_size": 72, "title_max": 108, "draw": draw_ml10_checklist,
        "chart_bbox": (0.05, 0.05, 0.92, 0.52),
        "practical": True, "out": "ML10.png",
    },
    # ML 11 — classification: logistic regression (boundary + sigmoid, 1-line title).
    {
        "tag": "ML 11",
        "title": "Կլասիֆիկացիա։ Լոգիստիկ ռեգրեսիա",
        "title_size": 48, "draw": draw_ml11_logreg,
        "out": "ML11.png",
    },
    # ML 12 — classification metrics: 2-model ROC vs PR comparison + F1 (next video).
    {
        "tag": "ML 12",
        "title": "Կլասիֆիկացիայի մետրիկաներ",
        "title_size": 50, "draw": draw_ml12_metrics,
        "out": "ML12.png",
    },
    # ML 13 — threshold tuning: metrics-vs-threshold + Youden's J. Latin title.
    {
        "tag": "ML 13", "title": "Threshold tuning",
        "title_size": 44, "title_max": 66, "title_latin": True,
        "draw": draw_ml13_threshold, "out": "ML13.png",
    },
    # ML 14 — calibration: reliability diagram + before/after isotonic fix.
    {
        "tag": "ML 14", "title": "Կալիբրացիա",
        "title_size": 54, "draw": draw_ml14_calibration,
        "out": "ML14.png",
    },
    # ML 15 — data imbalance: resampling grid (ROS/RUS/SMOTE) + Tomek links.
    {
        "tag": "ML 15", "title": "Տվյալների դիսբալանս",
        "title_size": 48, "draw": draw_ml15_imbalance,
        "out": "ML15.png",
    },
    # ML 16 — practical (Գործնական badge): bank-marketing classification.
    # Two-line Armenian title; lift-by-decile + cost-optimal threshold panels.
    {
        "tag": "ML 16", "title": "Կլասիֆիկացիա.\nմարքեթինգային տվյալներ",
        "title_size": 44, "draw": draw_ml16_practical,
        "practical": True, "out": "ML16.png",
    },
    # ML 17 — decision trees: the colored Titanic tree as a solo hero.
    {
        "tag": "ML 17", "title": "Որոշման ծառ",
        "title_size": 64, "title_max": 92, "draw": draw_ml17_tree, "out": "ML17.png",
    },
    # ML 18 — random forest: parallel independent trees averaged.
    {
        "tag": "ML 18", "title": "Random Forest",
        "title_size": 56, "title_max": 90, "title_latin": True,
        "draw": draw_random_forest,
        "chart_bbox": (0.05, 0.03, 0.92, 0.58), "out": "ML18.png",
    },
    # ML 19 — gradient boosting: "one tree, then keep adding" 3-step schematic.
    {
        "tag": "ML 19", "title": "Gradient Boosting",
        "title_size": 56, "title_max": 90, "title_latin": True,
        "draw": draw_boosting_trees,
        "chart_bbox": (0.05, 0.03, 0.92, 0.58), "out": "ML19.png",
    },
    # ML 20 — advanced boosting: the three library logos (XGBoost/LightGBM/CatBoost).
    {
        "tag": "ML 20", "title": "Advanced Boosting",
        "title_size": 56, "title_max": 90, "title_latin": True,
        "draw": draw_ml20_logos,
        "chart_bbox": (0.03, 0.10, 0.94, 0.42), "out": "ML20.png",
    },
    # ML 21 — trees practical (Գործնական badge): tornado chart of tree-vs-linear
    # feature importances (the lesson's "same data, different story" moment).
    {
        "tag": "ML 21", "title": "Ծառեր",
        "title_size": 72, "title_max": 82, "draw": draw_ml21_importances,
        "practical": True, "chart_bbox": (0.06, 0.05, 0.88, 0.50), "out": "ML21.png",
    },
    # ML 22 — interpretability (lecture): black box vs glass box framing, a small
    # readable tree inside the glass box. Mixed "Բացատրելի ML" title.
    {
        "tag": "ML 22",
        "title": "Interpretable ML (IML) 1", "title_latin": True,
        "title_size": 44, "title_max": 78, "draw": draw_ml22_blackbox,
        "chart_bbox": (0.05, 0.04, 0.92, 0.54), "out": "ML22.png",
    },
    # ML 23 — interpretability part 2 (model-agnostic): two REAL course figures
    # (permutation importance bars + ICE/PDP). Latin title, IML series scheme.
    # (draw_ml23_pdp_real = solo PDP; draw_ml23_pdp = synthetic fallback.)
    {
        "tag": "ML 23", "title": "IML 2: PFI · PDP · ICE",
        "title_size": 44, "title_max": 84, "title_latin": True,
        "draw": draw_ml23_two,
        "chart_bbox": (0.06, 0.05, 0.90, 0.46), "out": "ML23.png",
    },
    # ML 24 — interpretability part 3 (IML 3): two big REAL figures (SHAP beeswarm
    # + LIME husky); Counterfactuals named in the title. Latin title.
    # (draw_ml24_three is the 3-panel alternate.)
    {
        "tag": "ML 24", "title": "IML 3: SHAP · LIME · Counterfactuals",
        "title_size": 40, "title_max": 72, "title_latin": True,
        "draw": draw_ml24_two,
        "chart_bbox": (0.05, 0.08, 0.92, 0.48), "out": "ML24.png",
    },
    # ML 25 — interpretability practical (Գործնական badge): the whole IML toolkit
    # applied end-to-end on the startup-success dataset. 3-panel montage of REAL
    # course figures (PFI bars + SHAP beeswarm + counterfactual flip), reusing the
    # IML 2/3 assets. Latin title; the orange pill carries "practical".
    {
        "tag": "ML 25", "title": "IML: Startup success",
        "title_size": 44, "title_max": 78, "title_latin": True,
        "draw": draw_ml25_toolkit, "practical": True,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML25.png",
    },
    # ML 26 — feature engineering (lecture): two REAL bike-dataset slide figures,
    # binning + a ratio/units feature. Latin title.
    {
        "tag": "ML 26", "title": "Feature engineering",
        "title_size": 52, "title_max": 92, "title_latin": True,
        "draw": draw_ml26_fe,
        "chart_bbox": (0.05, 0.06, 0.92, 0.48), "out": "ML26.png",
    },
    # ML 27 — feature selection (lecture): two REAL figures, the RFE-CV curve (k=45)
    # + the Boruta shadow bars. Latin title.
    {
        "tag": "ML 27", "title": "Feature selection",
        "title_size": 56, "title_max": 96, "title_latin": True,
        "draw": draw_ml27_fs,
        "chart_bbox": (0.05, 0.06, 0.92, 0.46), "out": "ML27.png",
    },
    # ML 28 — classic methods (lecture): 3-panel montage of REAL figures, one per
    # method family (LDA + SVM margin + GP band), SVM centered. Latin title.
    {
        "tag": "ML 28", "title": "Classic methods",
        "title_size": 54, "title_max": 94, "title_latin": True,
        "draw": draw_ml28_classics,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML28.png",
    },
    # ML 29 — classical time series (lecture): the ACF/PACF order-reading pair plus
    # the SARIMA forecast against held-out actuals. Latin title.
    {
        "tag": "ML 29", "title": "Classical time series",
        "title_size": 50, "title_max": 88, "title_latin": True,
        "draw": draw_ml29_classical_ts,
        "chart_bbox": (0.05, 0.06, 0.92, 0.46), "out": "ML29.png",
    },
    # ML 30 — time series with ML (lecture): the tree extrapolation trap and its fix
    # as one wide hero, the single thing to remember from the lesson. Latin title.
    {
        "tag": "ML 30", "title": "Time series with ML",
        "title_size": 52, "title_max": 92, "title_latin": True,
        "draw": draw_ml30_ml_ts,
        "chart_bbox": (0.05, 0.04, 0.92, 0.48), "out": "ML30.png",
    },
    # ML 31 — time-series practical (Գործնական): the practical's OWN notebook plots
    # (Armenian energy series + the 2025 model bake-off), never the lecture's fig/.
    {
        "tag": "ML 31", "title": "Energy forecast",
        "title_size": 54, "title_max": 94, "title_latin": True,
        "draw": draw_ml31_ts_practical, "practical": True,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML31.png",
    },
    # ML 32 — clustering (lecture): one panel per family, k-means failing on the rings
    # next to DBSCAN solving them, then the dendrogram. Latin title.
    {
        "tag": "ML 32", "title": "Clustering",
        "title_size": 56, "title_max": 96, "title_latin": True,
        "draw": draw_ml32_clustering,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML32.png",
    },
    # ML 33 — colour spaces + project brief (lecture): the 196,680 -> 16 colour
    # quantization the project asks for, plus the HSV hue channel. Latin title.
    {
        "tag": "ML 33", "title": "Color spaces",
        "title_size": 54, "title_max": 94, "title_latin": True,
        "draw": draw_ml33_color_spaces,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML33.png",
    },
    # ML 34 — clustering practical (Գործնական): the practical's OWN notebook panels,
    # Sevan true colour vs k-means k=5 vs the ESA WorldCover ground truth.
    {
        "tag": "ML 34", "title": "Sevan land cover",
        "title_size": 50, "title_max": 88, "title_latin": True,
        "draw": draw_ml34_land_cover, "practical": True,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML34.png",
    },
    # ML 35 — colour-quantization practical (Գործնական): the practical's OWN notebook
    # panels, the painting at 124,841 colours vs k-means with 4 and with 32.
    {
        "tag": "ML 35", "title": "Color quantization",
        "title_size": 46, "title_max": 74, "title_latin": True,
        "draw": draw_ml35_quantization, "practical": True,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.04, 0.92, 0.46), "out": "ML35.png",
    },
    # ML 36 - PCA (lecture): the eigen-garments, i.e. the components themselves
    # rendered as images - the mean garment plus PC1/PC2 loading maps.
    {
        "tag": "ML 36", "title": "Principal components",
        "title_size": 50, "title_max": 88, "title_latin": True,
        "draw": draw_ml36_pca,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.05, 0.92, 0.46), "out": "ML36.png",
    },
    # ML 37 - t-SNE + UMAP (lecture): the woolly mammoth, 3-D next to its UMAP
    # projection - the example the lesson actually dwells on.
    {
        "tag": "ML 37", "title": "t-SNE and UMAP",
        "title_size": 46, "title_max": 74, "title_latin": True,
        "draw": draw_ml37_tsne_umap,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.03, 0.92, 0.46), "out": "ML37.png",
    },
    # ML 38 - dimensionality-reduction practical (Գործնական): the Novembre 2008
    # "genes mirror geography" PCA, top panel only.
    {
        "tag": "ML 38", "title": "PCA on genomes",
        "title_size": 46, "title_max": 74, "title_latin": True,
        "draw": draw_ml38_genes, "practical": True,
        "bar_color": UNSUP_BAR,
        "chart_bbox": (0.05, 0.03, 0.92, 0.46), "out": "ML38.png",
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


def _segments_fontkw(segments):
    """Turn a list of (text, kind) into (text, fontkw) pairs. kind 'latin' uses
    the bold Latin font (Comic Sans), 'arm' uses Adamathuz Bold."""
    out = []
    for text, kind in segments:
        if kind == "latin":
            out.append((text, dict(LATIN_FONTKW)))
        else:
            out.append((text, {"fontproperties": ARM_PROPS, "fontweight": "bold"}))
    return out


def _mixed_title_width(fig, seg_kw, size):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    total, probes = 0.0, []
    for text, fontkw in seg_kw:
        p = fig.text(0.06, 0.85, text, fontsize=size, va="top", **fontkw)
        total += p.get_window_extent(renderer).width
        probes.append(p)
    for p in probes:
        p.remove()
    return total


def _fit_mixed_size(fig, seg_kw, configured, max_size=74, x0=0.06, x_right=0.94):
    w = _mixed_title_width(fig, seg_kw, max_size)
    if w <= 0:
        return configured
    avail = (x_right - x0) * fig.bbox.width
    fit = min(max_size, max_size * avail / w)
    return max(configured, fit)


def _draw_mixed_title(fig, seg_kw, size, x0=0.06, y=0.85):
    """Place font-segments left-to-right on one line, each in its own font."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    x = x0
    for text, fontkw in seg_kw:
        t = fig.text(x, y, text, color=TITLE_COLOR, fontsize=size, va="top",
                     linespacing=TITLE_LS, **fontkw)
        x += t.get_window_extent(renderer).width / fig.bbox.width


def render_thumbnail(lesson: dict) -> None:
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_facecolor(BG)

    # Vertical bar at left edge — orange by default. A lesson can override it with
    # "bar_color" to mark a new block of the course (the unsupervised part from
    # ML32 on uses UNSUP_BAR), so the stripe reads as a section marker at a glance.
    bar_color = lesson.get("bar_color", BAR)
    bar = fig.add_axes([0.0, 0.0, 0.024, 1.0])
    bar.set_facecolor(bar_color)
    _strip(bar)

    # Lesson tag — Segoe Script handwritten, navy
    fig.text(0.06, 0.95, lesson["tag"], color=TAG_COLOR,
             fontsize=TAG_SIZE, va="top", fontname=TAG_FONT)

    # "Գործնական" (practical) badge — top-right orange pill, white Armenian
    # text in the title font. Marks the video as a hands-on/practical session.
    if lesson.get("practical"):
        fig.text(0.963, 0.925, "Գործնական", ha="right", va="center",
                 fontsize=31, fontproperties=ARM_PROPS, color="white",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor=bar_color,
                           edgecolor="none"))

    # Title — Adamathuz Bold Armenian by default; "title_latin" lessons use a
    # bold Latin font (Adamathuz has no Latin glyphs). Single-line titles
    # auto-grow to fill the width (up to title_max); multi-line keep their size.
    tsize = lesson["title_size"]
    if lesson.get("title_segments"):
        # Mixed Latin+Armenian title (e.g. "ML սխալները") — each segment in its
        # own font, placed left-to-right, auto-grown to fill the width.
        seg_kw = _segments_fontkw(lesson["title_segments"])
        tsize = _fit_mixed_size(fig, seg_kw, tsize,
                                max_size=lesson.get("title_max", 74))
        _draw_mixed_title(fig, seg_kw, tsize)
    else:
        title = lesson["title"]
        if lesson.get("title_latin"):
            fontkw = dict(LATIN_FONTKW)
        else:
            fontkw = {"fontproperties": ARM_PROPS, "fontweight": "bold"}
        if "\n" not in title:
            tsize = _fit_single_line_size(fig, title, tsize,
                                          max_size=lesson.get("title_max", 74),
                                          fontkw=fontkw)
        fig.text(0.06, 0.85, title, color=TITLE_COLOR, fontsize=tsize,
                 va="top", linespacing=TITLE_LS, **fontkw)

    # Illustration — draw function decides whether to use 1 axes or many.
    # A lesson may request a taller/wider band via "chart_bbox".
    lesson["draw"](fig, lesson.get("chart_bbox", CHART_BBOX))

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
