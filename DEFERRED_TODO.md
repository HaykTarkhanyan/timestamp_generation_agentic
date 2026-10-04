# Deferred

Topics cut from current work so they don't get lost. Newest at the top.

- **2026-10-04 - "Restate verbal changes" rule for the global CLAUDE.md.** Offered after
  the ML49 "keep the snake demo" misread; for now the rule lives in the lecture-edit-points
  skill only. Waiting for the user's answer.
- **2026-10-04 - Mapping chapter times through the final cuts is a scratch script.** ML48 used
  a throwaway `map_chapters.py`; the method is written in the lecture-edit-points skill. Make it
  a real script if it is needed for a third video.
- **2026-10-03 - Materials resolver and the CNN chapter.** `resolve_materials_url.py` finds
  lectures by `<NN>_*.tex`; the CNN decks are `L16_*` to `L19_*`, so lessons 48+ resolve to the
  NN chapter. The user said it's fine as is: set `.../ml/12_cnn/12_cnn.html` by hand for CNN
  lessons. A fix would be a small table of chapter start lessons (12_cnn starts at 48).
- **2026-10-03 - ML48 has its corrections twice**, as a comment and in the description. The
  comment can only be deleted by the user in Studio.
- **2026-09-26 - Thumbnail style and font for future lectures.** Candidates kept: bignumber,
  notebook, highlighter (`scripts/non_essential/thumbnail_style_options.py`) and the font sheet
  (`thumbnail_font_options.py`). The user hasn't picked yet; lectures still use the original style.
- **2026-09-26 - Note in `scripts/YT_PUBLISH_SETUP.md` that the curl/wget deny rule also blocks
  harmless downloads** (the user runs those with `!`). Offered, not answered.
