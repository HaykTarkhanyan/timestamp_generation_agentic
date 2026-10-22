# Deferred

Topics cut from current work so they don't get lost. Newest at the top.

- **2026-10-22 - Sevak Mkrtchyan's YouTube channel, Honors Linear Algebra (user: "pls also store
  this for future").** https://www.youtube.com/@sevakmkrtchyan-u1h - 10 lectures so far (16 Sep -
  14 Oct 2026), ongoing, no descriptions or chapters. Details in `_knowledge/umath_todo.md`,
  under Sevak.

- **2026-10-22 - Papikian's Galois Theory course (ARCS-ai, fall 2025) for the umath channel (user:
  "we may want to get it later as well").** 23 lectures, 22 recordings, notes and homework on his
  Teaching page; not on the channel yet. Details and next steps in `_knowledge/umath_todo.md`
  (its own section), files in `_knowledge/papikian_site/galois_theory_2025/`.

- **2026-10-21 - End screens for the Arnak videos (user: "park this as a task for future").** Wanted:
  in each video's last 10 s, Subscribe + the playlist + the next video. Agreed: 1-11 -> the next
  lesson, 12 -> 13, 12 (2025) -> 13, 13 -> "Best for viewer"; Claude saves each (user's OK). Done:
  **lesson 1** (7j53RC1y6i8), by hand through Playwright, saved, elements 1:07:16:00-1:07:26:00
  (Subscribe, Video: Դաս 2, Playlist). Left: 2-13 and the 2025 recording. Ready, not yet run:
  `scripts/non_essential/endscreen_template.js` + `make_endscreen_jobs.py` (README there). Studio
  facts: the End screen "+" menu has "Apply template"; the template card's aria-label is
  "1 video, 1 playlist, 1 subscribe"; template elements default to the last 20 s, each with
  start/end boxes in the panel; the preview boxes need a mouse click at their centre (an edit
  overlay intercepts locator clicks); "Choose specific video" opens a dialog with "Search your
  videos". The Playwright window must be uncovered and big enough (at 853x384 CSS px Studio's
  narrow layout did not open the end screen editor).

- **2026-10-21 - A `bazmachap` series for `make_umath_thumbnails.py` (Arnak's thumbnails made
  locally, DECISIONS #20's approach).** Parked because Canva was faster for the one 2025
  thumbnail (user: "wont it be faster to do with canva?"). Found so far, fitted on
  `thumbnails/umath/bazmachap_12.png` (scratchpad `fit_bazmachap.py`, size from ink height,
  spacing from ink width, NCC +-2 px): topic = **Mardoto Bold 57 px, spacing +1.45, NCC 0.920**,
  colour (46, 44, 44), line 1 ink x 74-834, y 429-485, line 2 y 504-570. Lesson line "Դաս 12":
  colour (69, 81, 194), ink x 76-311, y 340-386; **no local font matches** (best Mardoto Regular
  59 px, NCC 0.43): it and the series title are a Canva font to identify first. Plate: per-pixel
  max of the 8 Canva exports (bazmachap_06..13) removes the dark topic text; the shared "Դաս"
  needs a white fill (pure white there).

- **2026-10-20 - DECIDED the same evening:** lesson 10 = the 20-min part with its 2 trims, the
  description explains the unrecorded first part; the 2025 recording is published in full as
  "Դաս 12 (2025) | Կորելյացիաների շրջան։ Sparse PCA", right after the 2026 lesson 12, with a
  description note. The lecturer is not emailed (user). Original entry below.
- **2026-10-20 - Բազմաչափ վիճակագրություն: lesson 10 and the 2025 recording (user: "lesson 10
  decisions can wait").** The "2025" file (kJMKNFHYlFU) is the 2025 course's Դաս 12, not the
  missing first part of 2026 lesson 10 (an R regression practical that was never recorded).
  To decide: publish 10 part 2 alone (plan ready); what to do with the 2025 video (skip, extra,
  or only its sparse-PCA part, which 2026 lacks); whether to ask the lecturer for a 2025
  recording of the regression practical. The playlist sort (`--by lesson`) waits on the 2025
  title. Details in `_knowledge/arnak_multivariate/status.md`.
- **2026-10-20 - Arnak 10-13 and the 2025 recording: plans waiting for review.** Cut lists,
  chapters, titles and descriptions in each `output/2026-10-20_*Bazmachap*` /
  `*kJMKNFHYlFU*` folder (`edit_review.md` first). Not applied, not pushed. Thumbnails (Canva
  page 88 template) not started; PDF links are TODOs.

- **2026-10-20 - Կոմպլեքս անալիզ Դաս 20, 21, 23 show 2026 dates on YouTube** (9 Feb, 24 Feb,
  13 Mar 2026). First read as mistakes, but they are most likely **re-recording dates**: Sevak
  wrote on 10 Feb 2026 that he had re-voiced lesson 20 and would send "the other two" within
  about a week (Gmail thread "WG: [EXT] Դասախոսությունների տեսագրում, կոմպլեքս անալիզ",
  forwarded by a teammate). The original lectures fell in Nov-Dec 2025
  (Դաս 22 is 9 Dec, Դաս 24 is 16 Dec, and 24 calls 23 "the last lesson", so 23 was probably
  Fri 12 Dec). Open question for the user: show the lecture date or the re-recording date.
  Nothing changed.

- **2026-10-20 - DONE the same day: Կոմպլեքս անալիզ Դաս 20-23 chapters redone** on fixed
  transcripts (7/10/11/11 -> 16/15/20/17 chapters) and pushed; titles and date lines unchanged.
  ML lessons lost 0.3-4.8% of words to the old parser, probably not worth redoing.
- **2026-10-20 - A permanent regression test for `parse_vtt`.** The repo has no test framework;
  the space-only-top-line fixture lives only in a session scratchpad. Needs the user's pick of
  framework (or a plain assert script under `non_essential/`).

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
