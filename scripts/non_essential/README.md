# non_essential

Scripts that are maintained and reusable, but not needed to run the timestamp /
publishing pipeline. Nothing in `scripts/` imports these.

| script | what it does | when you would re-run it |
| --- | --- | --- |
| `quantize_shrek.py` | Trims the white margins off `ml/09_clustering/img/shrek.webp`, downscales it, and runs the lesson-35 k-means colour quantization at k=4 and k=32 (seed 509), writing the three ML35 thumbnail panels into `thumbnails/assets/`. | Re-run if the source image changes, or to regenerate the ML35 panels at different k values. Prints the original unique-colour count, which is the caption on the first panel — update `draw_ml35_quantization` if it changes. |

Added 2026-08-31.
