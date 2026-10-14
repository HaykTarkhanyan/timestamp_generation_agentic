# Thumbnails: fill the illustration band, don't leave empty space

**Symptom.** ML51's first thumbnail ("one photo, four tasks") got "51 leaves too much vertical
empty space", and the redo got "again ton of empt space, also same issue with ml 50". Both
designs were redone before the user said "nice job" (2026-10-14).

**Cause.** The band under the title is wide: `chart_bbox` (0.05, 0.02, 0.92, 0.66) on a
1280x720 canvas is 1178 x 475 px, about 2.5:1. Panels in a single row are limited by the width
long before the height: four 3:2 photos side by side form a 6:1 strip, which fills well under
half of a 2.5:1 band, whatever `max_h` says.

**What worked (published ML50 and ML51):**

- **ML51:** one big detection panel on the left, full band height; segmentation and
  classification stacked in a column on the right; each task's tag drawn *inside* its panel,
  so no caption row eats height. `_place_asset(fig, name, x, y, h, caption=None, tag=None)` in
  `make_thumbnails_final.py` places one asset by height.
- **ML50:** a vertical redraw of ResNet-18 (drawn on an axes, so it stretches to the band
  height) next to the Grad-CAM overlay.
- The band was raised to 0.66 of the canvas height for both (the skill's example is 0.46).

**Two side lessons from the same round:**

- **The big panel came out pixelated** when cropped from the course's `fig/task_zoo.pdf`: the
  PDF embeds the photo at low resolution. `thumbnails/src/ml51_task_assets.py` redraws the
  panels from the full-resolution photo, importing the figure's own boxes, scores and mask
  from `task_zoo.py`. A panel that fills half the band needs a source at least that big.
- **Showing two PNGs:** `Start-Process` on two files in a row showed the user only ML51
  ("u didnt open ml 50 for me to view"): the Photos app reuses one window. Open one stacked
  preview image instead.
