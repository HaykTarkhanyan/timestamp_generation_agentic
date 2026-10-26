# Decisions

Numbered, newest at the top. Superseded entries stay, marked as such.

## 45. While the lecturer's webcam is on screen, cuts are only suggestions

- **Decision:** A piece with `camera_on.json` (`scripts/non_essential/vahagn_camera_on.py`) gets every cut that touches
  a camera stretch unticked (`find_edit_points.py`, reason "camera on: a cut makes him jump"); the user ticks the ones
  worth a jump on studio.html.
- **Date / status:** 2026-10-26, active (the user, returning the 6 May batch with 70 of 75 planned cuts removed: "he
  had his video on and editing too much would make him teleport. pls for next batches see when hes on screen during
  the lecture, not just very beginning then make all the cuts unticked").
- **Why:** his webcam box (top-right, black bars on both sides) is on from 6 May to the end: 23.1.b-28.4 at 95-100%
  of every second, against 0% for 21.1-23.1.a. The only camera-off stretch in the 15 unreviewed pieces is 28.3.a
  18:09-18:37 (toolbar visible on the frame), so its cuts there stay ticked. Detector: the left bar's luminance in
  the 360p preview, dark under 100 (0-52 with the camera, ~219 without); the picture inside the box runs 42-192 as
  he moves, so it is not used.
- **Alternatives rejected:** dropping the cuts altogether (the user still added 8 cuts on 6 May, so suggestions are
  useful); a stricter threshold on the camera pieces (the user's call is which jumps are acceptable, not a length).
- **What would change this:** the user ticking most suggestions on a camera piece (then pre-tick the long pauses).
  Already reviewed pieces keep their plans: a camera file there would change the plan under the reviewed list.
- **Number:** was #40 until 2026-10-26; renumbered because this session and the Tserunyan session both used
  #39 and #40 (the user's Q76).

## 44. Vahagn's remaining pieces are reviewed in batches, one studio.html per lecture day

- **Decision:** Join each lecture day's pieces (2-4, 35-81 min) into one studio.html with one cut-list download, and
  split the download back into per-piece lists (`scripts/non_essential/vahagn_batch_review.py build` / `split`).
- **Date / status:** 2026-10-25, active (the user: "since here the vids are short i dont want to do one by one and
  keep on downloading many txts").
- **Why:** one page and one file per sitting; a day's pieces are consecutive parts of one lecture, so the page plays
  like the whole lecture. The page code is unchanged: the batch is a virtual output folder (pieces' analysis WAVs
  side by side on whole-frame slots, previews' pictures joined by stream copy, their sound re-encoded once, each
  piece's own planned cuts shifted unchanged). Tested on b0504 and b0506: an untouched plan splits back to every
  planned cut (26/26, 76/76, including a tail cut and the next piece's opening cut that the page joins into one); an
  edited list with a moved start, a moved end, a removed cut, a new cut and a new cut across a boundary splits into
  exactly those changes and passes `cut_list.py check`; the preview is in sync with the analysis audio (0 ms at the
  start and end of every piece; joining the sound by stream copy had put it 32 ms late, AAC's start-up delay).
- **Alternatives rejected:** one page per piece (the user's complaint); one page with every piece in a frame (file://
  pages can't read each other, so no single download); a fresh analysis of the joined audio (clean and hum pieces have
  different noise floors, and each piece's plan must stay its own for `check`).
- **What would change this:** batches too long to review in one sitting (then split a day in two: `build` takes any
  list of sections).
- **Number:** was #39 until 2026-10-26; renumbered because this session and the Tserunyan session both used
  #39 and #39 (the user's Q76).

## 43. Tserunyan 22-27: content cuts only, no pause cuts at all

- **Decision:** Re-plan 22-27 with no pause cuts (`--min-silence 100000`, so no silence qualifies); the content cuts
  stay as #40 and Q52 left them. For this playlist only. Supersedes #42 for 22-27.
- **Date / status:** 2026-10-26, active (the user, with the Դաս 21 list, where they had removed all 17 pause cuts and
  kept the 6 content cuts: "new plan no more waiting to write cuts for the rest of the videos in this playlist only.
  im fed up with them now. just content related staff pls, update the next htmls").
- **Why:** reviewing pauses cost the user more than they were willing to spend; on Դաս 21 they dropped every pause cut
  of the 7 s plan.
- **Alternatives rejected:** keeping a higher pause threshold (the user said no pause cuts at all).
- **What would change this:** a later course; the rule is for this playlist only.

## 42. Tserunyan 19-27: pauses only from 7 s, so the review is mostly content cuts

- **Decision:** Re-plan 19-27 with `--min-silence 7` instead of 4; the content cuts stay as #40 left them (math/talk
  as suggestions, practical and prompts ticked, next-time lines kept, Q52 waits kept with the silences inside them
  unticked). The review page still shows both pauses and content cuts (the user's Q59 "Show me both"). Դաս 15-18 keep
  the lists the user already made. Supersedes #40's 4 s for 19-27.
- **Date / status:** 2026-10-26, active (the user, sending the Դաս 18 list: "this is too much work - new approach im
  okay with waiting for her to type, that can be only cut if its super long, i need to know anout any content cuts
  but automated are toooo much extra work"; Q58 "7s").
- **Why:** reviewing 80-139 pause cuts per lecture cost the user more than the pauses cost viewers. Counted on the 4 s
  plans of 19-27: pauses of 8 s+ are 12-25 per lecture (156, 31.7 min), 10 s+ 6-17 (80, 21.4 min), 15 s+ 2-4 (23,
  11.3 min); the content cuts are 4-10 ticked plus 0-5 suggestions per lecture.
- **Alternatives rejected:** 15 s (offered as the recommendation), 10 s, 20 s, no pause cuts at all; showing only the
  content cuts on the page (the user wants both).
- **What would change this:** the user again adding many short pauses on 19-27, or asking for fewer cuts still.

## 41. studio.html shows the timeline and, below it, every cut on its own again

- **Decision:** a timeline page shows the per-cut cards again, in one collapsible section "Each cut on its own" under
  the timeline (one contents entry for it, not one per cut). Both views edit the one cut list STUDIO_JS keeps, so an
  edit in either shows in the other and in the exported list. Keys follow the last click: after a click on a card,
  Space and the arrows act on that card; after a click on the timeline, on the timeline (all other timeline keys
  unchanged). Supersedes #21.
- **Date / status:** 2026-10-25, active (the user, sending the Դաս 17 list: "for the next ones also include the view
  we had before where each cut was seperatley as as list, but also keep the full timeline as well").
- **Why:** #21's own trigger ("the user wanting a cut's own close-up view back"). No model change was needed:
  `renderAll()` already re-rendered every card and then called `tlRefresh()`; only the timeline's capture-phase key
  handler, which claimed Space and the arrows everywhere while the cards were hidden, had to let a clicked card have
  them. Checked in Playwright on Դաս 18 (74 cards): Remove cut on a card -> REMOVED in the export and in the
  timeline's data, Restore undoes it; Start = bar -> CHANGED line, Reset undoes it; ArrowRight after a card click
  moved that card's bar 0.2 s and not the timeline's, after a timeline click the reverse.
- **Alternatives rejected:** a show/hide toggle (the user asked for both at once); one contents entry per cut
  (74-139 lines above the timeline).
- **What would change this:** the user preferring one view again, or the next rework of STUDIO_JS (#21's JSON idea).

## 40. Tserunyan 17-27 re-planned from the user's Դաս 16 edit: 4 s pauses, her math talk kept

- **Decision:** For 17-27: silences of 4 s or more pre-ticked (`--min-silence 4`, no hum join); her math or talk
  content cuts (thinking aloud, false starts, room discussions, tangents, word searches) become unticked suggestions;
  practical cuts (searching notes, books or slides, pasting, drawing-tool fiddling, iPad/Zoom/screen trouble,
  household interruptions, homework and scheduling admin, time checks) and the "any questions?" prompts with their
  silence stay ticked. End cuts start after her "next time we'll ..." line (17, 18; 22's whole wrap-up cut and 17's
  chatter before the line, which no pause separates from it, became suggestions). Դաս 27's farewell (both goodbye
  cuts) is kept. Plans kept as `*_v4_4s`; the 5 s plans stay as `*_v3_5s`. Supersedes #26 for 17-27.
- **Date / status:** 2026-10-25, active. The user's answers: Q44 "4 s ticked only", Q45 "make them suggestions ill
  tick if i want uself" (follow-up: "Only the math/talk ones"), Q46 "Cut the prompt with its silence", Q48 keep the
  next-time line, Q50 "Keep both".
- **Why:** #26's own trigger fired: on Դաս 16 the user again added many short cuts by hand (56 new, 121 in all, the
  plan had 70) and unticked all 5 of her math/talk content cuts while keeping the 2 practical ones (searching her
  slides, a drawing fumble); on Դաս 15 they had added 87 and unticked her teaching tangent. Share of each pause length
  the user cut (silences re-detected in memory, `scripts/archive/tserunyan_2026-10/user_pause_fit.py`): 5 s+ 100% / 94% (Դաս 16 / 15),
  4-5 s 80% / 81%, 3.5-4 s 39% / 68%, 3-3.5 s 32% / 35%, under 3 s 8-13% / 32%. At 4 s the plan holds 29 of the 56
  added on 16 with 8 pauses they left in. 13 (16) and 18 (15) added cuts are pauses split by short sounds (fillers,
  clicks, Zoom's digital silence); joining silences across short sounds matched worse at every setting
  (`user_pause_merge_fit.py`, same folder), so no join.
- **Alternatives rejected:** 4 s ticked + 3-4 s as unticked suggestions and 3.5 s ticked (offered, the user picked
  4 s only); keeping 5 s (53 hand-added cuts on 16); unticking every judgment cut (the user: only the math/talk ones).
- **What would change this:** the user again adding many 3-4 s pauses or unticking practical cuts on 17-27.
- **Refined the same evening, after the user's Դաս 17 review:** a thinking invitation keeps its wait (Q52 "Keep words
  and wait, as suggestions": Դաս 26 0:58:01 "Any ideas?" + 21 s, Դաս 27 1:01:51 "shall we think about it?" + 10 s).
  The content cut and the silence cuts inside it are unticked, since the pause rule would still cut the wait
  (scripts/archive/tserunyan_2026-10/metric_keep_waits.py; a later full find_edit_points run re-ticks those silences).
  Homework talk stays cut (Q54 "Leave them cut", although on 17 the user kept one such remark).

## 39. Tserunyan's chapters are nested (15-27 now, the published 1-14 at the end of the course)

- **Decision:** Indent sub-chapters by 4 spaces in Մետրիկական տարածություններ և տոպոլոգիա, one level, a parent has
  2+ children, short theorem-then-proof pairs stay flat (the rules of #34 and #36). Դաս 15-27 are nested now in
  their masters (`edited_predicted/timestamps_raw.txt`, flat copy `timestamps_raw_flat.txt`); Դաս 1-14 (published,
  flat) get the same once 15-27 are finished. Labels and times unchanged.
- **Date / status:** 2026-10-25, active (the user's Q37: "nested, we update the older 14 in the end as well").
- **Why:** the same reading aid as Ashot (#34) and Vahagn (#36); her lectures run as definition, claim, proof
  steps, questions, which nest naturally. 13 lists: 252 of 376 chapters nested under 61 parents (2-6 per
  lecture), every derived file identical to the flat one apart from the leading spaces, 13/13 verifier-valid.
- **Pipeline changes:** `snap_chapters_to_captions.py` dropped the indent (rewrote every line from the stripped
  label) and now keeps it; `metric_readback.py` counts indented chapter lines. `remap_chapters.py` and
  `metric_assemble.py` already kept it. Checked by re-snapping Դաս 15: output identical to the nested list.
- **Alternatives rejected:** flat lists like 1-14 and the already pushed Դաս 15 (the user chose nesting); nesting
  only 16-27 and leaving 15 flat (one video out of step; it is unlisted, so its re-push costs nothing).
- **What would change this:** YouTube no longer keeping the indent or parsing indented chapters (then flatten all).
- **Time format (the user's Q40 the same day, "H:MM:SS throughout"):** every time as H:MM:SS (`0:03:58`), as Ashot
  (#34) and the ML course, instead of `03:58` mixed with `01:01:28`; all 13 lectures run over an hour. New opt-in
  `--hms` in `remap_chapters.py` and `snap_chapters_to_captions.py` (their default is unchanged for the other
  courses). Դաս 15 redone: seconds, labels and indents identical. Also for 1-14 at the end.

## 38. Vahagn's 25 pieces: only the sound is fixed locally; the cuts go in through YouTube Studio

- **Decision:** Fix the sound of 21.1-28.4 locally (`scripts/non_essential/vahagn_audio_fix.py`: Ashot's chain, 80 Hz
  low cut + light afftdn, then a per-piece gain to -16 LUFS with peaks limited to -1 dBFS, 48 kHz AAC 128k), copy the
  picture untouched, upload the results as new videos, and enter the reviewed studio.html cut lists in YouTube Studio
  afterwards. Replaces #35's local render with the cuts.
- **Date / status:** 2026-10-25, active (the user: "if we only do audio work how long will it take? cuts can be done
  in studio youtube later", then Q88 "yes"; the level picked on `output/vahagn_linalg_overview/audio/loudness_samples.html`:
  "Cleanup, raised to -16 LUFS").
- **Why:** speed and no waiting. Sound only: 21.1 (22:07) in 30 s, 28.3.b (5:14) in 11.6 s with gain, ~18 min for all
  25 on one core, against ~2.5 h of full-CPU rendering with the cuts, each piece blocked until its review. The picture is
  stream-copied, so the timeline does not move (21.1: 1327.456 s in and out) and the cut lists apply unchanged. No loss
  against the series: YouTube serves the published pieces at 720p at most (20.1), as it will the copied 1366x768.
- **Level:** the raw files are about -24 LUFS, the published pieces play at -29.7 (20.3's YouTube copy), and YouTube
  never turns quiet videos up (our raw 21.1 upload stayed at -24.2). Figures are ebur128 on mono files; counted as
  dual-mono (two speakers) the -16 output is -13.5 LUFS (28.3.b), at YouTube's ~-14 reference, so YouTube may turn it
  down by up to 0.5 dB. At -14 the 21.1 peaks would need ~8 dB of limiting (whole-piece peak -3.0 dBFS, gain +10.2 dB).
- **Chapters on the uploads** (added 2026-10-25 21:00, at the push): the uploads are uncut, so their descriptions
  carry the raw-timeline chapters (`timestamps_raw.txt`); once a piece's cuts are saved in Studio its description
  gets the remapped ones (`vahagn_push_metadata.py --chapters edited --description-only`). Every description
  matches its video at every moment; the 23 unreviewed pieces need the second push anyway.
- **Speed details:** ffmpeg 9 (#31), not the chocolatey 5.1 on PATH (pass 2 of 28.3.b 23.6 s against 8.6 s); 48 kHz
  output (AAC at the recordings' 32 kHz took 11.9 s for 28.3.b, at 48 kHz 5.2 s).
- **Alternatives rejected:** #35's render with the cuts (above); the recording's own level, -20 or -14 LUFS (samples
  page); Studio cuts on the existing raw uploads (sound stays raw, the reason for #35).
- **What would change this:** Studio's editor proving impractical for 25 videos (then render with the cuts after all);
  the finished hum pieces still sounding bad (Q83: then a stronger chain for those 11 only).

## 37. Vahagn 22.1-28.4: cut plans from pauses of 4 s, content cuts only where his talk leaves the topic

- **Decision:** Plan every remaining piece at `--min-silence 4` with a 360p video preview
  (`scripts/non_essential/vahagn_plan_queue.py`), plus content cuts only for off-topic talk (as unticked `judgment`
  suggestions where it is his own aside); the user reviews each on studio.html.
- **Date / status:** 2026-10-25, active (the user on 21.1: "for 21 s studio pls use 4 seconds as threshold").
- **Why:** On 21.1 the 4 s plan (15 cuts, 1.3 min) came back with all 15 kept, 7 edges adjusted and 4 short pauses
  added (2.8-4.6 s, plus the first 1.3 s): 19 cuts, 1.5 min. The recordings are dense; students' answers are not on
  them (only his mic), so his question-and-wait spots are plain silences the pause rule already takes.
- **Alternatives rejected:** 2 s (67 cuts, 3.0 min on 21.1) and 3 s (26 cuts, 1.8 min), the user picked 4 s; matching
  the previous editor's ~15% (not measurable: the published audio was processed, see #35).
- **Recordings with mains hum** (11 of 25, noise floor ~-65 dB against ~-85 dB, a 47 or 70 Hz line plus harmonics)
  are analysed from a 150 Hz high-passed copy (`vahagn_plan_queue.py --highpass`): the hum lifts the "floor + 20 dB"
  threshold over quiet speech (23.3.b: 91% of frames "silent", a 45-cut plan removing 5.6 of 9.6 min; filtered: 21 cuts,
  1.9 min; 23.2: 64% -> 54% silent). The preview and the render keep the original sound.
- **What would change this:** the user adding many short cuts on review again (21.1 added 4), which would argue for 3 s.

## 36. Vahagn's new pieces get one level of nested chapters, unlike the flat published 1.1-20.3

- **Decision:** Chapters for 21.1-28.4 nest one level where a topic has 2+ sub-chapters (4 spaces before the time,
  as DECISIONS #34 for Ashot); a parent never has a single child, and short theorem-then-proof pairs stay flat.
- **Date / status:** 2026-10-25, active (the user: "for the timestamps pls use 1 level hierarchy whenever its useful").
- **Why:** the user's request; the pieces are 5-30 min of tightly linked definition / theorem / proof / example runs,
  where a parent label reads faster than a flat list.
- **Alternatives rejected:** flat lists matching 1.1-20.3 (consistent with the published pieces, but not what the
  user asked for); renesting the 72 published pieces (not asked).
- **What would change this:** the user wanting the playlist uniform (then either flatten these or nest the old ones).

## 35. Vahagn's 24 missing pieces are rendered locally (cuts + improved sound) and uploaded as new videos

- **Decision:** Cut and fix the sound of Գծային հանրահաշիվ 21.1-28.4 locally with ffmpeg
  (`scripts/render_lecture.py`: the reviewed cut list, `--speed 1`, no intro/outro, no dip to black) and upload
  the results as new videos. The 24 raw uploads of 2026-10-24 only supply captions (set unlisted for yt-dlp);
  no titles, descriptions or Studio cuts go on them, and they go once the new ones are up.
- **Date / status:** 2026-10-25, superseded by #38 the same day (sound fixed locally, cuts in Studio). Was: (the user: "we need to improve the audios for those vids as well so i
  guess no need to do much updates on those videos on youtube because we will be uploading new ones anyways").
- **Why:** Studio can cut but can't touch the sound. The published pieces were processed: 20.1 and 20.3 are
  6 dB quieter than their raw files (-30.9 / -29.7 LUFS against -24.9 / -23.7) with a lower noise floor
  (-94.7 dB against -79.8 dB), so they were denoised and re-levelled outside YouTube. A local render also
  makes the number of cuts free (no Studio entry), so short pauses can go.
- **Alternatives rejected:** Studio cuts on the existing uploads (raw sound stays); Ashot's 1.25x speed (the
  published Vahagn pieces are 1x: the best speed match of published vs raw was 1.00x in 5 of 6 windows).
- **What would change this:** the user's pick on the audio samples showing the raw sound is fine as it is (then
  Studio cuts on the existing uploads would do).

## 34. Ashot's chapters are nested like Metric Academy's; videos over an hour use H:MM:SS throughout

- **Decision:** Indent sub-chapters by 4 spaces (one level, a parent has 2+ children) in all 9 Ինֆորմացիայի
  տեսություն videos, and write every time as H:MM:SS (`0:00:00`) in videos over an hour; under an hour the
  series' `MM:SS` stays. Labels and times unchanged.
- **Date / status:** 2026-10-24, active (the user: "make timestamps hierarchical like in Metric Academy ... if
  there is more than one hour start it with 00: like in MA").
- **Why:** same reading aid as the ML course (the skill's nesting rule, tested on YouTube 2026-08-31); the old
  lists mixed `05:04` and `01:03:31` in one video. Pushed for Դաս 1-8 and read back: indents kept, chapters
  still parsed (Դաս 2: 33, Դաս 8: 27). Դաս 0 stays flat: no parent there would have two children.
- **Alternatives rejected:** `M:SS` (`0:00`) for the short videos as in the ML course (the series already used
  `00:00`, and the user asked only about the hour format); nesting deeper than one level (YouTube keeps the
  list flat, and the skill forbids it).
- **What would change this:** the user wanting the same for Tserunyan, Papikian or Arnak (not applied there yet).

## 33. Ashot's slides: one Drive folder with the 4 final decks; every description gives its page range

- **Decision:** Put only the last deck of each part in a public math-team Drive folder (intro, Lectures 2-5,
  Lectures 6-11, Channel Capacity) and give each lesson's 📚 block "սլայդներ N-M", the deck link and the
  folder link.
- **Date / status:** 2026-10-24, active (the user picked the 4 decks and the deck + folder layout; slide
  numbers were their request: "include slide numbers for that lesson as well, not just the file").
- **Why:** His decks only grow within a part, so a page keeps its number in the later decks (by page text:
  L-10 -> L-11 70/71 pages identical at the same number, L-4 -> L-5 46/53, the rest small edits). One file
  per part plus a page range covers every lesson, and the final decks carry his latest corrections.
  Page table: `_knowledge/info_theory/slides_map.md`.
- **Alternatives rejected:** all 10 decks as posted, each lesson linking its own day's deck (10 overlapping
  files); the file link without pages (the user wanted the pages).
- **What would change this:** the lecturer asking for the per-week files, or a later deck renumbering pages.

## 31. The 1080p lecture renders use a portable ffmpeg 9.0.2 beside the system 5.1

- **Decision:** `render_lecture.py --ffmpeg C:/Users/hayk_/tools/ffmpeg-9/ffmpeg-9.0.2-full_build/bin/ffmpeg.exe`
  (gyan.dev full build, SHA-256 checked) for the final renders; the system ffmpeg 5.1 (chocolatey) stays for
  everything else. The script picks `-/filter_complex` (7.0+) or `-filter_complex_script` (5.1) by version.
- **Date / status:** 2026-10-24, active (the user: "lets install new ffmpeg").
- **Why:** The same zscale tone map ran 11-23% faster on 9.0.2, alternating runs on 20 s of Դաս 7
  (5.1: 25.0, 24.8 s; 9.0.2: 22.3, 19.2 s), with the same look (frame luma 145 both) and the same A/V timing
  (identical stream lengths on a test window).
- **Alternatives rejected:**
  - *GPU tone mapping with libplacebo (Vulkan on the Iris Xe)* - with hwupload/hwdownload the colours came
    back wrong in every pixel format (green planes, swapped channels); letting libplacebo do its own
    transfers fixed the colours but took 27.3 s, slower than zscale.
  - *Quick Sync decode + `vpp_qsv tonemap=1`* - failed on these files (Invalid argument).
  - *Replacing the system ffmpeg* - 9.0 removed `-filter_complex_script`, which other scripts here may use;
    a portable copy can't break them, and the system one can be switched later on purpose.
- **What would change this:** a newer Intel driver fixing the Vulkan readback (libplacebo could then be
  re-measured), or the system ffmpeg being upgraded anyway.

## 30. Classroom lectures: dip to black at every picture jump; Դաս 6 ends on his slides

- **Decision:** `render_lecture.py` fades to black and back (0.25 s each way, `--dip`) at every cut in the camera
  footage and at the switch from the camera to slides; a slide change stays instant. Դաս 6's last 17 min
  (sound only) show slide 38, then slide 39 from 1:05:47.8 to the end, full screen, after a straight cut
  from the camera; the description says why.
- **Date / status:** 2026-10-24, active (the user: "can we add a small transition between them like the screen
  going dark and reappearing so that it's not an instant blink, same for in video cuts. This is only about
  cases where prof is doing offline lecture so they don't teleport"; Q43 "straight cut, we clarify in
  description"; Q45 "keep 39 on screen").
- **Why:** With one fixed camera a hard cut makes the lecturer jump across the room; a short dip reads as
  "time passed". The fade only darkens existing frames, so lengths and sync are unchanged (measured: luma
  139 -> 16 -> 139 across Դաս 8's 7:20 cut, 151 -> 27 -> 228 into the slide).
- **Alternatives rejected:** *Hard cuts* - the teleporting. *A cross-fade* - shows two lecturers at once and
  needs overlapping frames, which would change the timing. *An on-screen note at the slides* - the
  description says it instead. *The agenda slide during his closing remarks* - the user kept slide 39.
- **What would change this:** the dip feeling slow or distracting on a lecture with many cuts.

## 32. Դաս 8's camera sound: no gain, light denoise

- **Decision:** Render Դաս 8 with `--denoise` and no `--gain-db`; replaces the +13 dB of #29 (and the +16
  tried after it).
- **Date / status:** 2026-10-24, active (the user: "lets do no gain, light denoise", after noticing their
  player had been set low while comparing the gain samples).
- **Why:** By ear at a normal volume. Measured on 7:05-7:45: -28.9 LUFS with no gain (published Դաս 4/5:
  ~-25; +13: -20.7; +16: -18.7). The boost also raised the room noise in pauses by the same amount.
- **Alternatives rejected:** +13 / +16 / +18 dB (judged on a quiet player); ~+4 dB to match Դաս 4/5 (offered).
- **What would change this:** viewers or the lecturer finding Դաս 8 too quiet next to the other lectures.

## 29. Ashot Դաս 6-8: content cuts only, extra ideas as unticked suggestions, no silence rule

- **Decision:** The cut plans for Ինֆորմացիայի տեսություն 6-8 hold only content cuts (dead air while he
  looks for a slide, the minutes before the lecture), plus unticked suggestions for borderline pauses; no
  automatic silence cuts (`--min-silence 9999`). Դաս 8's camera sound gets +13 dB (`--gain-db 13`).
- **Date / status:** 2026-10-24, active; the Դաս 8 gain revisited 2026-10-24, see #32 (the user: "this is classroom recording so if we do too many cuts
  than the prof will keep on teleporting, so we need to do semantically plus suggest some extra ideas,
  but no automatic 3s+ rule"; on the +10 dB sample: "with gain its better, even add a bit more").
- **Why:** One fixed camera on a walking lecturer: every cut is a visible jump, unlike a Zoom screen share
  where a cut is invisible. He also talks almost without pauses (Դաս 4/5: longest silences 5.4 s and 7 s).
  Դաս 8's plan came out at 2 ticked cuts (22 s) and 1 suggestion.
- **Alternatives rejected:** *Silences from 5 s (Tserunyan, #26) or 3 s (ML)* - the teleporting.
  *+10 dB* - the user asked for a bit more; the recorders of Դաս 6 / 7 need none.
- **What would change this:** a lecture with long dead stretches (a broken projector, a break), or the user
  finding the result too slow.

## 28. Ashot Դաս 6-8 are rendered with ffmpeg (`scripts/render_lecture.py`), matched to Դաս 2-5

- **Decision:** One ffmpeg pass per lecture: cuts on the recorder's timeline, the camera aligned to the
  recorder by `align_audio.py` (offset + clock drift), 1.25x with the pitch kept (atempo), iPhone HLG
  tone-mapped to BT.709 SDR with zscale + `tonemap=hable` at `npl=200`, 1080p 25 fps, intro and outro at
  1x, H.264 via Intel Quick Sync (`h264_qsv`, global_quality 22). Sound: the recorder for Դաս 6 and 7,
  the camera for Դաս 8 (it has no recorder file).
- **Date / status:** 2026-10-24, active, made by Claude on measured evidence; the look and speed still
  wait for the user's OK on a sample.
- **Why:** Դաս 2-5 were cut in Premiere (`info\*.prproj`, read 2026-10-24): camera picture, recorder
  sound (camera muted), 1.25x on Դաս 3 and 4 only (`PlaybackSpeed` 1.25; none in Դաս 5's project), intro
  `intro-attemt-2.mp4` (6.5 s) and outro `outro-attempt-2.mp4` (5.8 s) at 1x, 25 fps sequences (Դաս 0, 2,
  4, 5 are 25 fps on YouTube, Դաս 3 30), Lumetri exposure -1.1 to -1.9 (Դաս 4: +1.0). The new raw files
  are HEVC 10-bit HLG / BT.2020; read as SDR they look washed out (mean luma 177-191, published Դաս 2, 4, 5:
  138-153). `hable` at npl 200 gives 143-158, the same look, slides readable.
  Alignment: Դաս 7 offset 230.047 s, drift -11.4 ppm, residuals 3 ms; Դաս 6 200.869 s, -5.9 ppm, +-33 ms
  (room acoustics). After a render, the recorder and the camera's own sound agree within +3 to +8 ms
  (Դաս 7) and +-23 ms (Դաս 6) at 1x, through cuts.
- **Alternatives rejected:**
  - *Premiere, as for Դաս 0-5* - manual, and a cut list from studio.html can't go in without retyping.
  - *No tone map* - the washed-out look above.
  - *mobius / reinhard / clip tone maps, npl 100* - brighter than Դաս 2-5 (luma 194-219) with a warm cast.
  - *A Hald CLUT baked from the same chain* - mean pixel error 20 levels (the mapping went wrong) and only
    ~30% faster, since decoding is the bulk.
  - *Hardware decoding (d3d11va)* - no faster than the CPU here (20 s of video: 9.8 s vs 8.7 s).
  - *libx264* - kept as `--encoder x264`; Quick Sync leaves the CPU to the decode and tone map.
- **What would change this:** the user finding the sample too bright, dark or soft; a full render far
  slower than ~1.3x the recording; a newer ffmpeg with GPU tone mapping (`vpp_qsv` tonemap, libplacebo).

## 27. A cut list the user gives with "pw" is entered and saved by Claude when the checks pass

- **Decision:** When the user hands over their own cut list and asks for Playwright entry, Claude enters
  it and presses Save in Studio without asking again, if `cut_list.py diff` is identical frame for frame,
  the Save dialog's new length matches the prediction, and the original recording is on disk.
- **Date / status:** 2026-10-23, active (the user, during Tserunyan Դաս 15: "if i give you cut list myself
  and say will pw then you can also save it as well if your checks pass, unless local file is unavailable").
- **Why:** The list is already the user's reviewed decision, and the checks catch entry errors; asking
  again before Save only adds a round trip. Save can't be undone in Studio, so the local original is the
  safety net.
- **Alternatives rejected:** *Stop before Save every time* (the skill's default until now, which left the
  user to press Save); *save on any entry* (a list Claude planned but the user didn't review stays unsaved).
- **What would change this:** a saved edit that turns out wrong despite a clean diff, or no local original.

## 26. Tserunyan 16-27 cut silences from 5 s (no hum join); Դաս 15 takes the user's own edit

- **Decision:** For Մետրիկական տարածություններ և տոպոլոգիա 16-27 the active plan is the content cuts +
  silences of 5 s or more (`--min-silence 5`), without `hum_join.py`, saved as `*_v3_5s`. Դաս 15 uses the
  user's edit from studio.html (`studio_cuts_edited.txt`: 92 cuts, 14.8 min, one content cut dropped).
- **Date / status:** 2026-10-23, active. Supersedes #22 for Tserunyan (Papikian stays on #23).
- **Why:** After editing Դաս 15 on studio.html: "she is soo better then papikyan ... lets do the semantic
  cuts as always and regarding silences only cut obvious silences over 5 second". She rarely hums, so the
  hum join that Papikian needed (#23) has nothing to join. Her Դաս 15 edit kept 26 cuts under 4 s, but
  the plan for the rest takes only the obvious ones.
- **Alternatives rejected:**
  - *Content cuts only (#22)* - the user cut 87 more silences by hand on Դաս 15.
  - *4 s + hum join (`*_v2_4s`)* and *6 s + hum join (Papikian, #23)* - the user asked for 5 s, no hums.
- **What would change this:** the user again adding many short cuts by hand on 16-27, as on Դաս 15.

## 25. Correction notes only on the Metric Academy channel; umath lectures get none

- **Decision:** The stage-6 `⚠️ Ուղղումներ՝` block (#4) goes only on the user's own videos
  (Metric Academy channel). Lectures on Համալսարանական մաթեմատիկա (umath), given by other lecturers,
  get no correction notes, however clear the slip.
- **Date / status:** 2026-10-23, active (the user: "lets not add corrections to those at all, those
  are for just my videos (metric academy)"). Narrows #4.
- **Why:** On umath the lecturer is someone else (Tserunyan, Papikian, Dalalyan...), and a note under
  their lecture corrects them in public on a channel that is not theirs. The live descriptions already
  follow this: the 2026-10-22 audit dump has the block on 6 of 228 Metric Academy videos and on 0 of
  386 umath videos.
- **Alternatives rejected:**
  - *Notes for real slips only* (Tserunyan 17 Borel vs Baire, 18 "Egorov" for Lusin; Papikian 16,
    21, 23): drafted and checked, then dropped by the user.
  - *All proposed notes, including naming* (Tserunyan 19 T_1, 24 "Heine-Borel", 27 "has joins").
- **What would change this:** a lecturer asking for a correction to be added, or the user deciding
  that a particular slip would mislead viewers enough to note it.
- The slips found are kept, unpublished, in `edited_predicted/lecturer_slips_not_published.txt` per
  lecture and in `_knowledge/tserunyan_metric/codex_review_15-27.json`; chapter labels still state the
  correct condition (e.g. Դաս 24 "«Հայնե-Բորել» այս դասում՝ լրիվ և լիովին սահմանափակ").

## 24. Papikian's lecture 19 is "Դաս 18-19", following the existing "Դաս 11-12"

- **Decision:** The missing lecture number goes into the next lecture's label: lecture 19's title
  and thumbnail say "Դաս 18-19"; 20-23 keep the course numbers. No note about the gap.
- **Date / status:** 2026-10-22, active (the user: "lets do like precedent").
- **Why:** The course page has no lecture 18 at all (no notes, no recording; the slot is Fri
  22 Nov 2024; Դաս 19 picks up where 17 ended), like lecture 11 (its week lists the midterm
  solutions). The public lecture 12 video is "Դաս 11-12" in both the title and the thumbnail
  (`khvL7pQif3c`), so the playlist shows no gap. `sort-playlist --by lesson` reads the leading
  number, so 18-19 sorts as 18.
- **Alternatives rejected:**
  - *"Դաս 19"* - course numbering, but a visible gap that reads as a missing video.
  - *"Դաս 18"* - no gap, but every later number would differ from the course page and notes.
- **What would change this:** a lecture 18 recording turning up.

## 23. Papikian's lectures 17 and 19-23 cut pauses from 6 s plus hums; Դաս 16 takes the user's own edit

- **Decision:** For Հանրահաշիվ և թվերի տեսություն 17 and 19-23 the active plan is content cuts +
  pauses of 6 s or more (`--min-silence 6`) + `hum_join.py --write`, saved as `*_v3_6s`. Դաս 16
  uses the user's hand edit (`studio_cuts_edited.txt`, 128 cuts, 16.0 min). Metric (#22) is unchanged.
- **Date / status:** 2026-10-22, active. Supersedes #22 for Papikian only.
- **Why:** The user edited Դաս 16 by hand after the content-only plan ("jesus, mihran is awful at
  this i had to add cuts"), asked for the others "with 6 second threshold, but he does hmmm and
  slowly write A LOT", and on the 4 s vs 6 s question answered "6 is fine". The 6 s plans remove
  1.6-18.9 min per lecture (17: 78 cuts, 18:54; 19: 16, 2:21; 20: 26, 3:38; 21: 20, 2:38;
  22: 13, 1:38; 23: 17, 2:51), all chapter verifiers valid.
- **Alternatives rejected:**
  - *4 s (#17, `*_v2_4s`)* - closer to the user's Դաս 16 hand edit (4 s plan for 16: 122 cuts,
    13:09 against the user's 16.0 min) and recommended, but the user chose 6 s. 17-23 at 4 s:
    301 cuts, 42.3 min against 170 cuts, 32.0 min at 6 s.
  - *Content cuts only (#22)* - the user found Դաս 16 needed many more cuts after watching it.
- **What would change this:** the user adding many cuts by hand to a 6 s plan on review, as on Դաս 16.

## 22. Papikian's and Tserunyan's new lectures keep their pauses, like the older uploads: content cuts only

- **Decision:** Lectures 16-23 of Հանրահաշիվ և թվերի տեսություն and 15-27 of Մետրիկական
  տարածություններ և տոպոլոգիա get content cuts only (for Metric the generous non-math cuts of its
  standard); no `--min-silence 4` pause cuts and no hum joins. Arnak's rule (#17) does not apply to
  these series. Both versions are kept in each output folder: `*_v1_content_only` (active) and
  `*_v2_4s` (pauses from 4 s + hums).
- **Metric** (the user: "yes revert the metric one", 2026-10-22): edited Դաս 5 / 10 / 14 have
  0.93 / 0.44 / 0.79 pauses of 3 s+ per minute, longest 11.4 / 9.0 / 10.9 s, against 0.94 and
  10.6 s in raw Դաս 15: never silence-trimmed either. The 4 s rule would have removed 1215 cuts,
  3 h 1 min over the 13.
- **Date / status:** 2026-10-21/22, active for Metric; superseded by #23 for Papikian (the user: "match the style of older papikian videso no
  need to overdo it", after first asking for the 4 s rule because 1-5 cuts per video looked "suspiciously low").
- **Why:** The older uploads were never silence-trimmed. Pause stats (10 ms speech-band levels,
  floor + 20 dB): edited Դաս 5 / 10 / 15 have 0.36 / 0.57 / 1.37 pauses of 3 s+ per minute and
  longest pauses of 9.9 / 16.2 / 14.1 s, against 1.49 and 17.3 s in raw Դաս 16; a trimmed series
  (Complex Analysis Դաս 25) has 0 and 2.9 s. With the 4 s rule the new lectures would have lost
  3-22 min each (423 cuts over the 7) and sat visibly tighter than 1-15 in the same playlist.
- **Alternatives rejected:**
  - *The 4 s rule (#17)* - consistent with the user's own Arnak edit, not with this playlist.
    Kept as `*_v2_4s` in each output folder.
- **What would change this:** the user deciding to re-edit the older lessons too, or asking for
  pause cuts on these after watching one.

## 21. studio.html with a timeline hides the per-cut cards and keeps them as the page's data

- **Decision:** when the page has the timeline (#19), the per-cut cards are no longer shown or
  listed in the contents: they sit in a `<div id="cards" hidden>`. STUDIO_JS still builds the cut
  list (`plan`, the edits in localStorage keyed by card id) from them, and the timeline edits that
  list. The page's keys (Space, S, +/-, arrows) now act on the timeline wherever the focus is.
- **Date / status:** 2026-10-21, superseded by #41 on 2026-10-25 (the cards are shown again under the timeline). Was active (the user, after reviewing lesson 12 on the timeline: "i
  dont need the old view this wide timeline is perfect for me").
- **Why:** the timeline shows everything a card did (cut, reason, captions, playback with the cuts
  skipped) across the whole lecture. Hiding keeps the saved edits of pages already open
  (localStorage keys by card id), `--check-studio`'s card count and all of STUDIO_JS's tested code.
- **Alternatives rejected:** deleting the cards and building the cut list from a JSON blob
  (rewrites STUDIO_JS's model and its storage keys, for no visible gain); a show/hide toggle for
  the cards (not asked for).
- **What would change this:** the next real rework of STUDIO_JS (then move the cut list to JSON
  and drop the cards and their per-cut clips and spectrograms), or the user wanting a cut's own
  close-up view back.

## 20. umath course thumbnails are drawn locally from fitted templates, not in Canva

- **Decision:** `scripts/make_umath_thumbnails.py` draws the lesson line and the topic on a
  text-free plate per series (`thumbnails/umath/templates/`, built from the YouTube thumbnails by
  `scripts/non_essential/build_umath_plates.py`), with fonts, sizes, letter spacing and baselines
  fitted to those thumbnails. Pillow only, like `make_thumbnails_final.py`; fonts from fonter.am.
- **Date / status:** 2026-10-21, active (the user: "try to replicate it with your tools so that
  for the new videos you can locally create them instead of going through Canva").
- **Why:** Between lessons only the number and the topic change, so a plate plus two text lines
  reproduces the design. Measured fits (grayscale NCC): topic lines 0.83-0.96, lesson lines
  0.77-0.97; the comparison sheet (`--compare`) looks the same as YouTube's except the linear
  algebra topic's round stroke ends. Details: `_knowledge/umath_thumbnails.md`.
- **Alternatives rejected:**
  - *Keep using Canva* - the user wants it local; one script call per lesson instead of a manual edit.
  - *Re-render the series titles too* - they never change; baked in, they match the original exactly.
  - *A per-pixel minimum or median of the references for the Metric background* - the minimum
    picked up JPEG ringing (ghost outlines of old text), the median left a haze; the mean of the
    text-free references per pixel was clean.
- **What would change this:** the user restyling a series in Canva (refit, or rebuild the plate);
  finding the linear algebra topic's rounded font on fonter.am (swap it in for Mardoto Medium).

## 19. studio.html opens with a timeline of the whole lecture, built on the page's own code

- **Decision:** studio.html gets a timeline section: Python draws spectrogram tiles of the whole
  lecture once (`timeline_tiles()`, JPEG, 80 px/s and 8 px/s), and hand-written canvas JS shows
  them with every cut, the unticked suggestions and the silences of 2 s+ that no cut covers. It
  edits the same cut list as the per-cut cards. No new dependency.
- **Date / status:** 2026-10-21, active. The user's idea ("i wont miss sections which you didnt
  include at all"); they chose this way over wavesurfer.js.
- **Why:** The cards show only 20 s around each planned cut, so pauses nobody proposed are never on
  screen. Arnak lesson 11: the owner added 19 cuts on the page, and 18 more pauses of 4 s+ turned up
  later in stretches nobody had seen. The first build on Arnak 12 showed 49 silences of 2 s+ that no
  cut covers. Tiles: 11.6-13.8 MB and 16-23 s per 65-82-min lecture, drawn once per WAV.
- **Alternatives rejected:** wavesurfer.js (Regions, Spectrogram in "windowed" mode, Minimap). It
  decodes and analyses the audio in the browser (my estimate ~280 MB of RAM for a 73-min lecture at
  16 kHz, on a laptop that has run out of RAM before), and its region model would need syncing with
  the cards' list and numbering. A separate timeline page: two edit states for one list.
- **What would change this:** the timeline replacing the cards altogether (then wavesurfer's
  ready-made zoom and regions save more than the syncing costs); browsers or this laptop handling
  in-browser decoding of a 2-hour lecture comfortably.

## 18. Cuts are entered in Studio by a JS loop from the repo, run through the Playwright MCP in batches

- **Decision:** `scripts/studio_enter_cuts.js` holds the entry loop; `cut_list.py entry-js` fills
  it with a video's `studio_cuts_to_enter.txt` and writes batch files (14 cuts each, plus a
  read-only dry run) that run via `browser_run_code_unsafe(filename=...)` in the user's signed-in
  Studio tab. The read-back stays `cut_list.py diff`.
- **Date / status:** 2026-10-21, active. The user's choice ("we will have a lot more cut jobs"),
  made before Arnak lesson 11's 70-cut entry.
- **Why:** Until now the loop was retyped into each session's tool call (ML48-ML52, Arnak 10) and
  drifted: the playhead selector changed twice, and the lesson 10 version (under an hour, MM:SS:FF)
  differed from ML52's. Batches measured ~6 s per cut (ML51: 15 cuts in 87 s), and stopping
  between batches is what caught ML49's "playhead box not unique" after one cut.
- **Alternatives rejected:** (a) one tool call per click: ~5 per cut, ~350 calls for 70 cuts,
  an hour or more. (b) A standalone Python Playwright script: its own browser needs its own Google
  sign-in (often refused in automated browsers), and it runs blind, so a mid-run surprise is found
  only at the end. (c) One call for the whole list: over ~120 s the MCP moves it to the background.
- **What would change this:** Studio's editor changing its labels or buttons (the dry run fails
  first); YouTube offering cut entry through the API; or the MCP's ~120 s limit changing, which
  would allow larger batches.

## 17. Arnak's pauses are cut from 4 s, and a hum between two cut pauses goes with them

- **Decision:** Cut plans for Arnak's raw recordings run `find_edit_points.py --min-silence 4`
  (pre-ticked) on top of the content cuts. When two planned cuts are separated only by a sound
  under 1.2 s with no real caption word (his "ըըը"), one content cut joins them. "Any questions?"
  prompts stay; only the silence after them is cut (the user, same evening).
- **Date / status:** 2026-10-21, active; supersedes #16.
- **Why:** The user's 48-cut list for lesson 11 ("he often just says ommm, that's why you may think
  he said something"). Inside the three stretches they clearly reviewed (14:45-20:35, 43:20-49:40,
  1:02-1:08) they cut 93% of the 4-6 s pauses, 57% of 3-4 s, 11% of 2-3 s and every 8 s+ one;
  outside them nothing beyond the plan, so #16's 8 s matched only the unreviewed parts. The hums
  are as loud as his speech (frame median -30 dB inside their cuts vs -25 dB elsewhere; a threshold
  10 dB higher catches 14% of hum frames and already 4% of speech frames), so no threshold turns
  them into silence. A wider caption-based merge (pause + any un-worded sound + pause) matched 2 of
  7 of the owner's choices on lesson 11 and would have swallowed a 7 s stretch they kept; the narrow
  join changes nothing on their own list (0 joins), so it cannot contradict them. Result:
  12: 45 cuts, 7.3 min; 13: 14 cuts, 4.0 min; 2025 recording: 43 cuts, 6.8 min.
- **Alternatives rejected:**
  - *3 s (the Metric Academy default)* - they cut only 57% of the 3-4 s pauses they reviewed.
  - *Louder silence threshold to catch hums* - hums and speech overlap in level (above).
  - *The wide caption-based hum merge* - wrong in 2 of 7 cases on lesson 11.
- **What would change this:** the user removing many of the 4-6 s cuts on the next review, or
  keeping the joined hums.

## 16. Arnak's silent writing stretches are cut: every silence of 8 s or more

- **Status update:** superseded by #17 on 2026-10-21.
- **Decision:** Cut plans for Arnak's raw recordings run `find_edit_points.py --min-silence 8`
  (pre-ticked silence cuts, 0.35 s pad) on top of the content cuts. Single words he says while
  writing stay (the detector only cuts silence). Supersedes the "writing stays, --min-silence
  150" plans of the same afternoon.
- **Date / status:** 2026-10-20, active (the user: "he says something and then slowly writes it
  ... it just basically says nothing ... I'd like those kind of parts to be removed").
- **Why:** The user's own Studio edits of lesson 10 (0:36-7:49) cut every silence of 9 s or more
  (9.1, 9.3, 11.3, 11.4, 11.6, 12.0, 12.4, 19.6, 40.4 s) plus one of 6.2 s, and left 3.3, 3.7, 4.5,
  4.9, 5.9, 7.0 and 7.5 s. 8 s reproduces 9 of those 10 cuts and none of the kept ones. Their cut
  edges matched the detector's within a frame or two at 2:26, 2:37, 3:24, 5:06, 6:14. New plans:
  11: 27 cuts, 9.5 min; 12: 19, 5.3 min; 13: 3 (unchanged); 2025 recording: 19, 5.1 min;
  10: the user's 13 + 2 (17:03, 17:27).
- **Alternatives rejected:**
  - *5 s* - would also cut the 5.9-7.5 s pauses the user left in lesson 10.
  - *Keep the writing pauses (this afternoon's plan)* - the user rejected it on seeing the video.
- **What would change this:** the user cutting the 5-8 s pauses in a review, or keeping some of
  the 8 s+ ones.

## 15. ASOF intro and outro go around the raw Zoom file by stream copy; cuts happen in Studio

- **Decision:** For Papikian's Algebra and Number Theory lectures 16-23 (downloaded from PSU
  Kaltura, never on YouTube), `scripts/concat_intro_outro.py` re-encodes only the intro
  (`assets/asof/hoy_nazan_asof.mp4`) and outro (`assets/asof/OutroScene.mp4`) to the lecture's
  1280x720, 25 fps and color tags, re-encodes the lecture audio to AAC 48 kHz stereo 160k,
  copies the lecture video untouched, and joins the three through MPEG-TS. Content cuts are made
  after upload in YouTube Studio's Trim & cut, not in the file.
- **Date / status:** 2026-10-20, active (the user: "lets have better music, just concat the 3
  here, then i upload to youtube we get transcript and decide cuts which then youtube studio
  editor will do").
- **Why:** Measured on Lecture 16 (5571.8 s): the video copy costs 0.04 s per minute, the AAC
  audio encode 7.7 s per minute; whole run 657 s, output 5587.87 s against 5587.86 s expected.
  The Zoom file has a keyframe only every ~30 s, so a stream-copy cut inside the file cannot land
  where a sentence ends; Studio's editor can. The intro and outro are the pair the user picked by
  eye, the ones on YouTube's Դաս 15.
- **Alternatives rejected:**
  - *Full re-encode with ffmpeg's concat filter* - a long all-cores run on this laptop and one
    more generation of quality loss, for no gain.
  - *Copy the lecture audio too (32 kHz mono) and convert the music down to it* - about 30 s per
    lecture, but the user chose the better music.
  - *Plain MP4 concat demuxer without the TS step* - an MP4 track holds one set of H.264
    parameters (the intro's x264 ones), while the lecture's Zoom stream uses its own.
  - *Opus instead of AAC* - libopus measured 1.87 s per minute (4x faster), but needs MKV or
    Opus-in-MP4 instead of YouTube's recommended AAC in MP4. Not tried end to end.
- **What would change this:** a decode error or a visible or audible glitch at a join after
  YouTube processes the upload; a lecture recording in another format; the ~11 min per lecture
  becoming a bottleneck (then Opus).

## 14. Arnak's videos use his own words: titles from his notes' headers, his terms over the glossary

- **Decision:** For Բազմաչափ վիճակագրություն, each title's topic is the section header(s) he
  writes at the start of the lesson's notes (or slides), and titles, chapters, descriptions and
  thumbnails use his terms: հիմնական (not գլխավոր) բաղադրիչ, կանոնիկ, կորելյացիա. Long pairs are
  shortened to fit 100 characters (lesson 8: "... Կանխատեսում"; lesson 9: "... Հիմնական
  բաղադրիչներ").
- **Date / status:** 2026-10-20, active (the user: "in his notes he starts the lesson by writing
  a title, pls look into it and copy it"; then "lets use professors words" for the chapters).
- **Why:** Lesson 5's existing thumbnail topic is word for word his section 5 ("Էմպիրիկ միջին և
  էմպիրիկ շեղում"), so the earlier lessons were already titled from his notes; 6-9 had been
  retitled by an agent and drifted. Mixed terms (title "հիմնական", chapters "գլխավոր") would name
  the same idea two ways inside one video.
- **Alternatives rejected:**
  - *Glossary terms everywhere (the repo default for other courses)* - consistent with the
    glossary, but not with the lecturer's notes, which viewers see on screen.
  - *His headers verbatim with abbreviations (ՀԲՎ, ՆՔ)* - cryptic in search; spelled out except
    where the 100-character limit forces ՆՔ (lesson 8).
- **What would change this:** the lecturer asking for standard spelling (կոռելյացիա), or a
  course whose notes carry no section headers.

## 13. sort-playlist can also order by the lesson number in the title

- **Decision:** `sort-playlist <id> --by lesson` orders by the number in a leading "Դաս N"
  (`^Դաս (\d+)`); equal numbers keep their current order. A title without it raises, so an
  extra video (a 2025 recording, a bonus) forces a decision instead of landing anywhere.
  `--by published` (#12) stays the default.
- **Date / status:** 2026-10-20, active (the user had asked to fix the playlist orders; the
  Arnak and Ashot playlists were left open).
- **Why:** #12's trigger happened. Arnak's lessons 4 and 5 were published after 6-9, so publish
  date gives 1, 2, 3, 6, 7, 8, 9, 4, 5. Checked as dry runs only: on the Complex Analysis
  playlist both orders give 0 moves of 25; on Arnak's it raises on "2025-ի Դաս 12 (...)".
- **Alternatives rejected:**
  - *Unnumbered titles go last, with a warning* - quietly decides where an extra video sits.
  - *An explicit order file per playlist* - one more file to keep in step with every rename.
- **What would change this:** titles that number lessons differently (e.g. "Lecture 3"), or
  parts like "Դաս 10, մաս 2" that need an order other than the current one.
- **Revisited 2026-10-20:** within one number, a title of the form "Դաս 12 (2025) | ..." (another
  year's recording of that lesson) sorts after the lesson's own video. The user chose that title
  for the 2025 recording and its place right after the 2026 lesson 12. Also: the API can only
  reorder playlists whose ordering is set to Manual in Studio (learning 2026-10-20-2221).

## 12. Playlists are ordered through the API, by publish date

- **Decision:** `yt_publish.py sort-playlist <id> [--apply]` orders a playlist oldest-published
  first with `playlistItems.update` (position only). It is a dry run without `--apply`, moves
  only out-of-place items, and re-reads the playlist to confirm the order.
- **Date / status:** 2026-10-20, active (the user asked to fix the Կոմպլեքս անալիզ playlist);
  revisited 2026-10-20: #13 adds `--by lesson`, publish date stays the default.
- **Why:** That playlist read 19..1, 22, 24, 20, 21, 23, 25. Publish timestamps run in lesson
  order (1-19 Sep-Dec 2025, 20-23 on 12-13 Jul 2026 in order, 24 and 25 today), so publish
  date gives 1-25 with no title parsing. 21 moves, ~1,050 quota units; 0 moves on a rerun.
- **Alternatives rejected:**
  - *The user sets "Date published (oldest)" in Studio* - one click, but the Data API has no
    field for that setting, so it can't be done or checked from here.
  - *Sort by the lesson number in the title* - tied to "Դաս N" titles; publish date is generic.
- **What would change this:** a series whose publish order differs from lesson order (a
  re-upload, a late lesson); then sort by the title's number instead.

## 11. yt_publish.py serves several channels: one OAuth client, one token per channel

- **Decision:** `--channel` (fixed choices, default `metric`) picks the token file in
  `scripts/.secrets/`: `token.json` for Metric Academy, `token_umath.json` for Համալսարանական
  մաթեմատիկա. Both use the existing `youtube-publisher` OAuth client. `auth` checks the
  token's channel against a fixed id per name and deletes the token on a mismatch.
- **Date / status:** 2026-10-20, active (the user asked for the same access on the second
  channel, which they manage).
- **Why:** The client only identifies the app; the token identifies the account. The app is
  already in Production, so a second token needs one consent and no new GCP setup. With a
  single `token.json`, authorizing the second channel would have overwritten Metric Academy's.
  Checked after the change: `recent 2` without `--channel` still lists ML52 and ML51, and
  `auth` on Metric matches `UC5BavugdnUkti3Es7-deZDg`. The id check exists because the first two
  `umath` sign-ins landed on no channel and on the personal channel (Brand Account picker).
- **Alternatives rejected:**
  - *A second GCP project per channel (the runbook's new-account path)* - 10-15 min of
    console setup for no gain; it would only matter if one channel needed its own quota.
  - *A free-form `--token` path* - a typo would start a fresh consent and leave a stray token.
- **What would change this:** a channel hitting the shared 10,000 units/day, or a channel
  owned by someone else who should not authorize this project's app.

## 10. Chapters for an edited video start right after Save, on the raw transcript mapped through the cuts

- **Decision:** After the user saves a Studio edit, `scripts/map_transcript_to_edit.py` maps
  the raw `transcript.txt` through the entered cut list (`studio_cuts_to_enter.txt`) into
  `edited_predicted/`. Chapters, title, description and the correctness review are written
  on it at once. YouTube's processed video and its regenerated captions are only a check
  before publishing: the length must match the prediction, and `--audit-boundaries` is run on the
  real `edited/` captions.
- **Date / status:** 2026-10-17, active (the user asked why we wait for YouTube's render).
- **Why:** The mapping is deterministic, and it was measured against YouTube's real edited
  captions (a separate recognizer pass) on two videos:
  - ML51: 461 confidently matched lines, median offset 0.0 s, 99% within 1 s, worst 2 s.
  - ML50: 406 lines, median 0.0 s, 100% within 1 s, worst 1 s.
  - Edited lengths matched the cut lists every time measured (ML48 5327 s; ML50 2184 s for
    2184.00 predicted; ML51 2446 s for 2445.96). Processing plus new captions took 30+ min of waiting.
- **Alternatives rejected:**
  - *Wait for the edited captions (the old way)* - the same result 30-60 min later.
  - *Publish the predicted chapters before processing ends* - the live video stays raw
    until then, so the chapters would point to the wrong places; publish after the check.
- **What would change this:** a processed length that differs from the prediction by more
  than a frame or two, or audited boundaries that move more than 1-2 s (then Studio is doing
  something the cut list does not describe).

## 9. studio.html can play a 360p proxy of the recording, made on request

- **Decision:** `find_edit_points.py --video-preview` encodes the local recording to a
  640x360, 15 fps H.264 copy with a keyframe every 2 s and mono AAC
  (`<output_dir>/video/<id>_360p.mp4`, Quick Sync by default). studio.html plays it in
  a pinned panel instead of the WAV. It is opt-in, and reused once made.
- **Date / status:** 2026-10-12, active (the user picked "real video, synced" over a
  frame strip).
- **Why:**
  - Zoom's recording has a keyframe every ~26 s (mean of 11 gaps, max 31 s). Played
    directly, 8 seeks took 0.35-11 s (median ~2 s) and Play took 2.4 s to start.
  - On a proxy with 2 s keyframes, 8 seeks took 11-138 ms and Play started in 64 ms.
  - A 90 s clip encoded in 19 s with Quick Sync. The full encode is heavy (2-3x
    realtime measured with the CPU at 100% from other work), hence opt-in.
- **Alternatives rejected:**
  - *Play the Zoom file directly* - no encode, but seconds per seek.
  - *Frame strip + live frame* - cheaper, but the user wanted real video.
  - *Encode only the cut windows* - about half the length here (long cuts dominate) and
    a player that switches files per card.
- **What would change this:** Zoom recordings with frequent keyframes (then play the
  original), or the encode proving too slow to bother with.

## 8. Videos outside the ML series get their own thumbnail, rendered from HTML

- **Decision:** The Claude Code workshop thumbnail is an HTML page
  (`thumbnails/src/claude_code_thumb.py` builds it) screenshotted at 1280x720 with
  Playwright, not a `make_thumbnails_final.py` lesson. The locked ML design stays for
  the ML series.
- **Date / status:** 2026-10-12, active (the user: "come up with something new... u dont
  need to use the old templates").
- **Why:** The concept is text-led (a lyric card of Claude's rap verse, the Claude
  symbol, a falling mic). HTML gives text highlight bars, the workshop's own fonts
  (IBM Plex, Noto Sans Armenian, embedded as base64) and a colour emoji mic directly;
  the matplotlib template has none of that, and its title font has no lowercase Armenian.
- **Alternatives rejected:**
  - *The ML template* - the user asked for something new, and "ML NN" doesn't apply.
  - *PIL by hand* - text highlights, emoji and kerning would all be manual work.
- **What would change this:** more non-series videos (then make the HTML route a
  skill), or the user wanting them in the ML look after all.

## 7. The Claude Code workshop cuts silences of 4.5 s and longer; the default stays 3 s

- **Decision:** KdtXO7Pj9DI's edit points use `--min-silence 4.5`. The 3 s default in #3
  is unchanged.
- **Date / status:** 2026-10-11, active (the user's pick for this video).
- **Why:** At 3 s the plan was 68 Studio cuts. Counted from `edit_points.json` with the
  same 20 pre-ticked content cuts:

  | Minimum silence | Studio cuts | Edited video |
  |---|---|---|
  | 3 s | 68 | 1:40:52 |
  | 3.5 s | 55 | 1:41:24 |
  | 4 s | 47 | 1:41:48 |
  | 4.5 s | 42 | 1:42:06 |
  | 5 s | 38 | 1:42:22 |

  4.5 s drops 26 cuts to type for 74 s more video. Kept pauses stay at full length.
- **Alternatives rejected:**
  - *3 s (the default)* - 68 cuts.
  - *4 s (my recommendation)* - 5 more cuts for 18 s less video.
  - *5 s* - 4 fewer cuts than 4.5 s for 16 s more video.
- **What would change this:** the user picking a higher threshold on the next videos too
  (then raise the default in #3); the kept 3-4.5 s pauses sounding slow in the edited video.

## 6. Private things on screen are blurred by the user, not cut

- **Decision:** Edit points report private on-screen spots (raw and post-cut times, what
  is visible) and leave them in the video. No default cut covers them; the user blurs
  them in YouTube Studio.
- **Date / status:** 2026-10-11, active (the user's call, Claude Code workshop video).
- **Why:**
  - The user said: "im gonna blur that parts and not cut".
  - The spots sit inside demos: Telegram 0:26:14-0:26:26, the calendar week view
    0:35:07-0:35:13, the home address 1:17:45-1:18:38. Cutting them would cut the demo
    narration with them.
- **Alternatives rejected:** *cut each spot* - loses the demo explanation around it.
- **What would change this:** a spot too long or too spread out to blur, or Studio's
  Blur tool failing on it.

## 5. Edit-point audio comes from the local Zoom recording, checked against YouTube's length

- **Decision:** `find_edit_points.py --audio <file>` converts the recording the user
  uploaded (the Zoom download in `~/Downloads`), instead of downloading the audio from
  YouTube. It refuses a file whose length differs from the YouTube video's by more than 2 s.
- **Date / status:** 2026-10-04, active. YouTube download stays as the fallback when no
  `--audio` is given.
- **Why:**
  - The user asked for it. They download from Zoom and upload that exact file, so it is
    the same timeline. ML49: Zoom file 5391.16 s, YouTube 5391 s.
  - It is faster: 12 s to convert, against about 30 s of download plus about 45 s of
    conversion on ML48.
  - The length check catches picking the wrong file: ML48's recording was rejected for
    ML49, 6352.8 s against 5391 s.
- **Alternatives rejected:**
  - *Always download from YouTube* - slower, and unnecessary when the original is on disk.
  - *Auto-pick the newest Zoom file without a check* - one wrong pick puts every cut on
    the wrong audio.
- **What would change this:** the user editing the file before uploading (then the
  timelines differ and the length check fires), or recording somewhere other than Zoom.

## 4. Lecture corrections go in the description, above the chapters, with minutes instead of timestamps

- **Decision:** The confirmed corrections from the stage-6 review go in the video
  description, in a `⚠️ Ուղղումներ՝` block just above `⏳ Թեմաներ՝`. Each line starts
  with the minute in words, `N-րդ րոպեին - ...` (rounded to the nearest minute), never a
  `H:MM:SS` timestamp. A comment is posted only when the user asks for one.
- **Date / status:** 2026-10-03, active, revisited 2026-10-15. Supersedes #1 in part.
  - Revisited 2026-10-15 (ML50/ML51): each line now starts with a `- ` bullet,
    `- N-րդ րոպեին - ...`. The user asked for it "so its easier to read, also in future":
    the corrections are long, and without a marker they run together.
- **Why:** On ML48 the user looked for the corrections in the description, asked for
  them "before chapters", then asked for "at minute x" wording instead of timestamps.
  There is room for them: ML48 went from 2,586 to 3,139 characters out of 5,000.
  - Keeping timestamps out of that block also avoids any risk of YouTube reading them
    as chapters. With `H:MM:SS` lines above the list, ML48 still parsed 35/35 chapters,
    so the minute wording is the user's preference, not a measured necessity.
- **Alternatives rejected:**
  - *Comment only (#1)* - the user expected the corrections in the description.
  - *Clickable timestamps* - the user asked for minutes.
- **What would change this:**
  - a description near the 5,000 cap (then shorten the corrections or move them to a comment);
  - the user wanting clickable links again.

## 3. Edit points default to a 3 s minimum silence; Studio entry is by the user, Playwright only on request

- **Decision:** `find_edit_points.py` defaults to cutting silences of 3 s and
  longer (was 2 s). Cut lists are rounded inward to whole frames and numbered the way
  Studio numbers them. The user applies cuts in Studio themselves unless they ask for
  Playwright for that video, and Playwright never presses Save.
- **Date / status:** 2026-10-03, active. Revises the 2 s default in #2.
- **Why:**
  - **3 s:** on ML48, 2 s gave 68 edits for 16.4 min removed and 3 s gave 24 edits for
    15.2 min. The 44 extra edits bought 1.2 min, and the user picked 3 s.
  - **Frames and numbering:** Studio's time boxes are `H:MM:SS:FF` and its list is sorted
    by start time, so frame-exact times numbered like Studio let the user match the
    review page to Studio directly.
  - **Save stays with the user:** Studio edits can't be undone after Save. After I
    entered ML48's cuts, the user adjusted them by hand and asked that Studio not be
    changed through Playwright again.
- **Alternatives rejected:**
  - *Keep 2 s* - too many manual edits for little time.
  - *0.1 s rounding* - Studio counts frames, so 0.1 s times don't map exactly.
  - *Playwright by default, or pressing Save* - irreversible and outward-facing.
- **What would change this:**
  - the user preferring every pause tightened (lower the threshold);
  - a channel frame rate other than 25 fps (the frame rate is read per video already);
  - a Studio change that shifts the timeline during editing (then enter cuts last-first).

## 2. Edit points for unedited recordings: audio silences + transcript content cuts, applied by hand in Studio

- **Decision:** `scripts/find_edit_points.py` proposes cuts from two sources -
  silence runs in the audio (2 s and longer, leaving 0.35 s of pause on each side)
  and content cuts I pick from the transcript (`content_cuts.json`: dead air,
  "any questions?" + silence, logistics, pre/post-lecture chat). It writes
  `edit_points.json` first, then a review page with a spectrogram and two clips per
  cut ("after the cut" and "what gets removed", boosted) and a cut list ordered
  last-first for the YouTube Studio editor.
- **Date / status:** 2026-10-03, active (first used on ML48); revisited 2026-10-03, see #3 (default 3 s, frame-exact Studio list).
- **Why:** The user edits in YouTube Studio's built-in editor, so the output has to
  be times typed into Studio's boxes, not an EDL or a rendered file. Last-first
  order keeps every remaining time valid whether or not Studio re-times the
  timeline after a cut. The ML48 audio is noise-gated (26% of 10 ms frames sit
  near -94 dB), so silence is unambiguous: silence-run counts barely moved
  between -80 and -60 dB (102-122 runs of 2 s or more). The silence threshold is
  the noise floor (5th percentile) + 20 dB.
  Captions alone give cut edges only to about 1-2 s, so content-cut edges get
  snapped outward to the speech edge in the audio; an edge that lands on speech
  raises instead of being moved silently.
- **Alternatives rejected:**
  - *Screen/frame checks on a low-res video copy* - the user said they won't help.
  - *Captions only* - mushy edges, and auto-captions miss quiet student speech
    entirely (ML48 0:00:30-0:00:45 has speech with no captions).
  - *Rendering the edit with ffmpeg* - the user uses Studio's editor.
  - *matplotlib spectrograms and MP3 clips* - ~2.5 s per cut here; numpy + PIL
    images and WAV clips are an order of magnitude faster per cut.
- **What would change this:** the user moving to a desktop editor (then export
  an EDL/markers instead); Studio limiting the number of cuts; recordings
  without a noise gate (then check the floor + 20 dB threshold against the
  run counts again); the 2-3 s silence cuts proving not worth typing (ML48:
  they are 44 of 68 edits but only 1.2 of 16.4 min removed).

## 1. Lecture corrections go out as a confirmed YouTube comment

- **Decision:** After a video is published, the pipeline reviews the lecture for
  the lecturer's own mistakes and posts them as one comment from the channel -
  but only after the user confirms that comment's content. The user pins it by hand.
- **Date / status:** 2026-10-01; superseded in part by #4 on 2026-10-03 (corrections now go in the description; a comment only when asked).
- **Why:** The user asked for it after the ML47 review found real slips (two
  reversed percentages at 0:28:38 and 0:31:34, a wrong claim about what the
  checkpoint holds at 1:21:20). A posted comment is public and the publisher has
  no delete, so a human gate before posting is the safety net.
- **Alternatives rejected:**
  - *Corrections in the description* - the description holds the abstract and
    chapters under a 5,000-char cap (ML46 already hit it), and viewers read
    comments for errata more than descriptions.
  - *Pinning via the API* - the YouTube Data API has no pin method
    (comments: list/insert/update/delete/setModerationStatus only).
  - *Posting automatically* - a wrong correction is worse than none, and only
    Studio can delete it.
  - *Including caption-ambiguous items* - auto-captions garble numbers, so
    "maybe ASR" findings stay out of the comment unless the user confirms
    they said it.
- **What would change this:** the API gaining a pin method (then pin on post);
  the user preferring corrections in the description or a card; or reviews
  that keep finding nothing (then drop the stage to save time).
