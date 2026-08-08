---
name: lecture-thumbnails
description: Generate a YouTube thumbnail (1280x720) for an ML lecture in the channel's locked design - orange left bar, "ML NN" handwritten tag, Armenian/Latin title, and a per-lesson illustration band. Use this whenever the user wants a thumbnail (or "thumbnail", "cover image", "preview image", "MLNN.png") for a lecture/video, or to add/redesign a lesson's thumbnail. STEP 0 is ALWAYS to source REAL figures before drawing anything synthetic - for a LECTURE that means the reference course repo's fig/ folder; for a PRACTICAL (Գործնական) it means the practical's OWN solution notebook outputs (its plots are on the practical's dataset, NOT the lecture's fig/). Renders via scripts/make_thumbnails_final.py; embeds real figures via scripts/pdf_to_asset.py; publishes via scripts/yt_publish.py set-thumbnail.
---

# ML Lecture Thumbnail Generator

Produce a 1280x720 thumbnail for a lecture video in the channel's **locked design**, then (after the user confirms) push it live. The generator is `scripts/make_thumbnails_final.py`: each lesson is a config dict + a `draw(fig, bbox)` function that fills the bottom illustration band.

## THE RULE (why this skill exists)

**Before drawing ANYTHING synthetic, check the reference course repo's `fig/` folder for a REAL slide figure that already shows the lesson's idea.** The course ships polished vector figures (PDF) for almost every concept - a decision tree, a PDP, an ROC curve, a calibration plot. Embedding the authentic figure (as ML06-17, ML20 do) is almost always better than a hand-drawn stand-in: it matches what students saw, it's correct, and it's on-brand. Reach for a synthetic redraw (ML18/19/21-style primitives) ONLY when no real figure fits the point you want to make.

> Learned 2026-07-31: I jumped straight to synthetic black-box/PDP redraws for the interpretability lessons and had to redo them after the user pointed out `ml/05_interpretability/fig/` was full of real figures. Don't repeat that - grep the `fig/` dir FIRST.

### PRACTICALS: source figures from the practical's OWN notebook, NOT `fig/`

`fig/` holds the **lecture's** teaching figures (a different, canonical dataset - bike-sharing, bank-marketing). A **practical** (Գործնական) *re-runs* those methods on its **own** dataset and produces NEW plots - and those new plots are what the video actually shows. So for a practical, using `fig/` puts the WRONG data on the thumbnail. The practical's real plots live as embedded outputs in its **solution notebook** in the reference repo.

STEP 0 for a practical is therefore different - find the notebook and pull its plot outputs:

1. Find the notebook (named for the lesson, next to the lecture sources):
   ```bash
   find "C:/Users/hayk_/OneDrive/Desktop/01_python_math_ml_course/ml" -iname "*<NN>*.ipynb"
   # e.g. ml/05_interpretability/25_startup_success_solution.ipynb ; dataset often in a
   # sibling folder like .../05_interpretability/Startup_Success/data.csv
   ```
2. Extract the embedded `image/png` outputs, printing each producing cell's source so you can tell which plot is which (PFI vs SHAP beeswarm vs local waterfall vs tree...). Save a short extractor to the scratchpad and run it:
   ```python
   import base64, json, logging, sys
   from pathlib import Path
   sys.stdout.reconfigure(encoding="utf-8")
   logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                       handlers=[logging.StreamHandler()])
   nb = json.loads(Path(NB_PATH).read_text(encoding="utf-8")); OUT = Path(OUT_DIR); OUT.mkdir(exist_ok=True); i = 0
   for ci, c in enumerate(nb["cells"]):
       if c.get("cell_type") != "code": continue
       for o in c.get("outputs", []):
           png = o.get("data", {}).get("image/png")
           if not png: continue
           (OUT / f"img{i:02d}_cell{ci:03d}.png").write_bytes(base64.b64decode(png))
           logging.info("img%02d cell%d: %s", i, ci, " ".join("".join(c["source"]).split())[:160]); i += 1
   ```
3. VIEW the candidates (Read tool), pick the ones that read at thumbnail scale, then crop each plot's own title band + trim white (PIL: crop off the top fraction, `ImageChops.difference` vs white -> `getbbox` -> re-pad) into `thumbnails/assets/ml<NN>_<slug>.png`. This is the PNG-input analogue of `pdf_to_asset.py`. KEEP the left-side feature/axis labels - on a practical they are what prove it's the right dataset.

> Learned 2026-08-08: for the IML *practical* (lesson 25, startup success) I first built the thumbnail from the lecture's `fig/` figures (bike-sharing PFI, bank counterfactual) - wrong dataset. The user caught it: "the plots are not from the practical, they are from the lecture." Fix was to pull the real startup-data plots out of `25_startup_success_solution.ipynb` (19 embedded outputs - PFI, SHAP beeswarm, and the local SHAP waterfall for the exact failing company #13 the counterfactual targets). For a practical, ALWAYS source from its own notebook. (Also: a method whose output is a text table, like DiCE counterfactuals, has no plot to embed - substitute the nearest authentic plot, e.g. the local explanation of the same row.)

### Where the figures live

Reference repo (a sibling of this project, NOT inside it):
`C:\Users\hayk_\OneDrive\Desktop\01_python_math_ml_course`

- Lecture sources: `ml/<NN>_<section>/` (e.g. `ml/05_interpretability/`), holding numbered `<NN>_<name>.pdf` slide decks (these also confirm the lesson number).
- **Figures: `ml/<NN>_<section>/fig/*.pdf`** (and some `*.png`). This is the folder to scan.

Always start with:
```bash
ls "C:/Users/hayk_/OneDrive/Desktop/01_python_math_ml_course/ml/<NN>_<section>/fig/"
```
Then Read the candidate PDFs (the Read tool renders them as images) to judge which read well at thumbnail scale. Prefer clean single-plot figures; skip busy multi-panel ones for a single band, or pair two clean ones side by side.

## The locked design (do not change)

- Canvas 1280x720 (`figsize=(12.8, 7.2), dpi=100`), white background.
- Vertical **orange** bar at the far left edge (channel identity).
- **Tag** "ML NN" top-left, Segoe Script (handwritten), navy `#0033A0`.
- **Title** below the tag, charcoal `#0e0e0e`. Armenian -> Adamathuz Bold; English -> Comic Sans MS Bold (`title_latin`); mixed -> `title_segments`.
- Optional **"Գործնական"** orange pill top-right for practicals (`"practical": True`).
- **Illustration band** across the bottom, filled by the lesson's `draw(fig, bbox)`.
- Palette = Armenian flag on white: orange `#F2A800` (`BAR`), blue `#0033A0` (`POINT_COLOR`), red `#D90012` (`LINE_COLOR`), charcoal title. No Metric branding.

### Font gotcha

`Adamathuz Bold` is **UPPERCASE ARMENIAN only** - it has no Latin glyphs and no lowercase. So:
- English / acronym titles (PFI, PDP, "Model-agnostic") -> `"title_latin": True` (Comic Sans).
- Mixed like "Բացատրելի ML" -> `"title_segments": [("Բացատրելի ", "arm"), ("ML", "latin")]`.
- Lowercase/mixed-case Armenian inside a panel (e.g. axis-ish labels) -> `fontname="Sylfaen"` (see the ML03 one-hot panel).
A stray `Glyph NN (x) missing from font Adamathuz` warning during title fitting is usually harmless - verify by viewing the PNG.

## Workflow

1. **Identify the lesson** (number + the one key idea the thumbnail should land) and **whether it is a lecture or a practical** (Գործնական). The video's current title / the reference deck names it.
2. **STEP 0 - source REAL figures** (see THE RULE):
   - **Lecture** -> scan `ml/<NN>_<section>/fig/` and Read the promising PDFs.
   - **Practical** -> find the practical's solution notebook and extract its embedded plot outputs (its plots are on the practical's OWN dataset; `fig/` would be the wrong data). See "PRACTICALS" under THE RULE.
3. **Propose the visual to the user.** Thumbnails are brand-facing and the user has strong opinions - offer 2-3 concepts (real-figure vs synthetic, one-panel vs two) and let them pick. Use `AskUserQuestion` with short ASCII previews.
4. **Turn each chosen figure into a trimmed PNG asset** in `thumbnails/assets/ml<NN>_<slug>.png`:
   - **Lecture PDF** -> `pdf_to_asset.py`:
     ```bash
     python scripts/pdf_to_asset.py "<ref>/ml/<NN>_<sec>/fig/<name>.pdf" \
         thumbnails/assets/ml<NN>_<slug>.png --dpi 300 --crop-top 0.10
     ```
     `--crop-top` drops the figure's own title band (tune the fraction; also `--crop-bottom/-left/-right`). It renders (PyMuPDF), crops, and trims the white margin.
   - **Practical notebook PNG** -> the extracted `imgNN_*.png` is already raster; crop its title band + trim white with a short PIL step (see "PRACTICALS" under THE RULE).
   - Either way, **VIEW the asset** to confirm the crop.
5. **Add a draw function** in `make_thumbnails_final.py`:
   - Real figures: `_draw_image_row(fig, bbox, ["ml<NN>_a.png", "ml<NN>_b.png"], captions=[...], gap=0.05, max_h=0.46)` - one or two panels, heights matched, optional bold captions.
   - Synthetic: compose the shared primitives (`_mini_tree`, `Rectangle`, bars, `_strip`) on an `ax` with `xlim/ylim (0,1)`. To inset an image inside a drawn box, convert box axes-coords to figure-coords with the `bbox` and `fig.add_axes(...)` (see `draw_ml22_blackbox`).
6. **Add the lesson config** to `LESSONS`:
   ```python
   {"tag": "ML NN", "title": "...",            # or title_segments / title_latin
    "title_size": 48, "title_max": 84,          # single-line titles auto-grow to title_max
    "draw": draw_mlNN, "practical": False,
    "chart_bbox": (0.06, 0.05, 0.90, 0.46),     # x0,y0,w,h of the band (tune per illo)
    "out": "MLNN.png"},
   ```
7. **Render just that lesson** (CLI filters by output-name substring):
   ```bash
   python scripts/make_thumbnails_final.py MLNN
   ```
8. **VIEW the PNG** (Read tool) - always. Iterate on layout/sizes.
9. **Confirm the FINAL version with the user before pushing.** Do not publish a thumbnail the user hasn't signed off on - they care and will (rightly) reject a surprise push.
10. **Publish** only after the go-ahead:
    ```bash
    python scripts/yt_publish.py recent 6                       # grab the video id if needed
    python scripts/yt_publish.py set-thumbnail <VIDEO_ID> thumbnails/MLNN.png
    ```
    `set-thumbnail` is metadata-only; it can be redone freely, so a wrong one is cheap to fix - but still get the OK first.

## Notes

- Output PNGs land in `thumbnails/MLNN.png`; embedded assets in `thumbnails/assets/`.
- Keep the same `tag`/number the channel uses (the lesson index), even if the title carries a sub-series name (e.g. tag "ML 22" with title "Interpretable ML (IML) 1").
- The generator keeps prior/alternate draw functions around (commented in configs) - follow that so a design can be swapped back.
- Encoding: the scripts force UTF-8 on stdout/stderr (Windows cp1252 mangles Armenian). Logs go to `logs/`.
