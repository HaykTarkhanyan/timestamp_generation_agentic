# Համալսարանական մաթեմատիկա thumbnails: the Canva templates, rebuilt locally

Built 2026-10-21 so new lessons get thumbnails from `scripts/make_umath_thumbnails.py` instead of
Canva. Three series so far: `ant` (Papikian), `metric` (Tserunyan), `linalg` (Mikaelian).

## How to make one

```
python scripts/make_umath_thumbnails.py --series ant --lesson 16 --topic "Քարլիցի մոդուլ։ Ցիկլոտոմիկ ընդլայնում"
python scripts/make_umath_thumbnails.py --series linalg --lesson 21.1 --topic "Վեկտորի գաղափարը\nℝ² հարթությունում"
python scripts/make_umath_thumbnails.py --compare     # thumbnails/umath/templates/compare.png
```

- Output `thumbnails/umath/<series>_<lesson>.png`, 1280x720, ~1 s.
- The topic splits after `։` (the series' own habit: Դաս 13 and 14 of both courses), else wraps
  at the width limit; `\n` sets the break by hand. A line that does not fit shrinks the font
  (one line per `։`-part down to 85%, then wrapping down to 70%); below that the script raises.
- Keep the thumbnail topic short. A full title like Դաս 16's "Քարլիցի ցիկլոտոմիկ ընդլայնում։
  Քարլիցի էքսպոնենցիալը" fits only as three crowded lines at 55 px instead of 65.
- **Math, LaTeX-like:** `$\mathbb{R}^2$`, `$F_q$`, `$x^{n+1}$` between dollars (plain `ℝ²` gives
  the same pixels). Double-struck letters are Windows' Sans Serif Collection at 66/64 of the
  topic size plus a 1 px stroke (NCC 0.975 against the linalg 1.1 ℝ; Cambria Math's ℝ has serifs,
  and matplotlib mathtext's `\mathbb` is italic in all of dejavusans, stixsans, stix and cm).
  Superscripts are the topic font at 0.67x, baseline raised 29/64 em (the reference 2: 30 px
  tall, Mardoto Medium 43 px NCC 0.93), plus 9/64 em before a following space (34 px gap, as in
  the reference). Other characters Mardoto lacks come from Cambria Math.

## What the templates are

Each is a text-free plate (`thumbnails/umath/templates/<series>_plate.png`) with the series title
and the artwork baked in, plus two drawn elements: the lesson line and the topic.

| Series | Lesson line | Topic |
|---|---|---|
| ant | `ԴԱՍ N`, Arm Hmk's Bebas Neue 81 px, letter spacing +6.5, rgb(202, 38, 44), left 100, baseline 432 | Mardoto Italic 65 px, black, left 100, baselines 549 / 631, max width 815 |
| metric | `Դաս N`, Mardoto Regular 55 px, +1.0, rgb(240, 209, 120), left 76, baseline 444 | Mardoto Bold 57 px, +0.5, white, left 76, baselines 549 / 619, max width 840 |
| linalg | `ԴԱՍ N`, Bebas 67 px, +2.5, rgb(236, 65, 66), left 120, baseline 421 | Mardoto Medium 64 px, +1.9, black, **right-aligned** at 1205, baselines 134 / 228 |

## How they were measured

- References: the `maxresdefault.jpg` thumbnails, 1280x720 (YouTube's largest; the listing's
  "1920x1080" webp came down at 1280x720, and the JPEG is ~2.8x the size of the webp, so less
  compressed): `thumbnails/umath/reference/`. ANT 11-12, 13-15, Metric 10-14, linear algebra 1.1, 10.2-ա, 20.3.
- Fonts from fonter.am (`fonts/arm-hmks-bebas-neue/`, `fonts/mardoto/`, `fonts/montserrat-armenian/`).
  None of them was installed; Windows' own Armenian fonts are Arial, Segoe UI, Sylfaen and the like.
- Fit (scratchpad `font_fit.py`): for each line, font x size x letter spacing x a ±2 px shift,
  scored by grayscale normalized cross-correlation against the reference's ink. Best scores:

  | Line | Fit | NCC |
  |---|---|---|
  | ANT topic (2 lessons) | Mardoto Italic 65-66 px, spacing 0 | 0.95, 0.96 |
  | ANT `ԴԱՍ 15` | Bebas 81 px, +6.5 | 0.82 |
  | Metric `Դաս 14` | Mardoto Regular 55 px, +1.0 | 0.97 |
  | Metric topic | Mardoto Bold 57 px, +0.5 | 0.83 |
  | Metric title (baked) | Mardoto Bold 65 px | 0.96 |
  | linalg `ՀԱՆՐԱՀԱՇԻՎ` (baked) | Bebas 70 px | 0.95 |
  | linalg `ԴԱՍ 1.1` | Bebas 67 px, +2.5 | 0.77 |
  | linalg topic | Mardoto Bold 64 px +1.6 scored best (0.70-0.83), but by eye the original is lighter, between Medium and Bold, **with round stroke ends** | |

  Montserrat Armenian lost every line it was tried on, although its name suggested the Metric text.
- **Digits are tighter than letters in the Bebas labels (found 2026-10-22).** The fit above was
  scored on whole labels with one digit pair, so it hid this. Glyph by glyph (scratchpad
  `label_extent.py`, red-ink column runs), every digit and "-" in ours advanced 4-5 px more than
  in ANT `ԴԱՍ 11-12` / 13 / 14 / 15 (7 pairs, mean 4.9) while the letters and the space matched to
  1 px; "ԴԱՍ 11-12" ended at x 410 against 389. ANT now has `num_track=1.6` for digits, "-" and
  "." (6.5 - 4.9): all four labels end within 1 px. linalg shows the same at +2 px per digit pair
  (`ԴԱՍ 20.3`: 2→0, 0→., .→3); not corrected yet, worth doing before its multi-digit labels.
- **The linalg topic face is not exactly reproduced.** Its round stroke ends belong to a font we
  do not have (a rounded face in Canva, probably). Mardoto Medium matches the weight; Medium plus a
  1 px round stroke looked clearly heavier at real size, so it was dropped. Visible only side by side.
- Plates: `scripts/non_essential/build_umath_plates.py`. ANT and linalg: the variable areas are
  flat colour. Metric: the dark grid behind the text was rebuilt from the five references (a pixel
  is the mean of those without text there; a per-pixel minimum picked up JPEG ringing and left
  ghost outlines, a median left a haze), the shared `Դաս 1` inpainted, and the red axis line
  (y = -0.7193 x + 771.1) redrawn from its intact stretches. A few faint grid lines fade out where
  text sat in every reference; at normal size they cannot be seen.

## Adding a series

Download 3-5 of its thumbnails (`yt-dlp --skip-download --write-all-thumbnails`, keep the largest
JPEG) into `thumbnails/umath/reference/`, find the fonts on fonter.am, refit with the same NCC
approach, add a plate step to the builder and an entry to `TEMPLATES`, and check `--compare`.
