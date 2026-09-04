# non_essential

Scripts that are maintained and reusable, but not needed to run the timestamp /
publishing pipeline. Nothing in `scripts/` imports these.

| script | what it does | when you would re-run it |
| --- | --- | --- |
| `quantize_shrek.py` | Trims the white margins off `ml/09_clustering/img/shrek.webp`, downscales it, and runs the lesson-35 k-means colour quantization at k=4 and k=32 (seed 509), writing the three ML35 thumbnail panels into `thumbnails/assets/`. | Re-run if the source image changes, or to regenerate the ML35 panels at different k values. Prints the original unique-colour count, which is the caption on the first panel — update `draw_ml35_quantization` if it changes. |
| `split_figure_panels.py` | Splits one multi-panel course figure PDF into a separate PNG per sub-plot, so `_draw_image_row` can size, space and caption each panel itself. Finds the boundaries by scanning for all-white gutter columns instead of taking crop fractions by eye; `--crop-top` drops the sub-plot title band first, `--keep` picks which panels to write. | Whenever a thumbnail wants some of the panels out of a figure that holds a row of them (used for ML36's eigen-garments, ML37's mammoth, and ML38's Novembre 2008 panel a, where `--crop-bottom` drops the sub-panels below and a raised `--min-width-frac` discards the tiny "a" label). If it finds the wrong number of panels, adjust `--gutter-tol` (how many stray ink pixels a column may hold and still count as a gutter), `--white`, or `--min-width-frac`. Reads figure PDFs and already-raster borrowed PNGs alike. |

Added 2026-08-31 (`quantize_shrek.py`), 2026-09-03 (`split_figure_panels.py`).
