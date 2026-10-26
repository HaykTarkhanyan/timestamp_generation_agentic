# archive

One-off scripts kept as a record of how something was done. Not expected to still run (paths, video ids
and the scratchpad layout of the session that wrote them are baked in), and never imported by live code.
They use `print`, not logging: promote one to `non_essential/` (and give it logging) before reusing it.

## info_theory_2026-10/ (Ashot Harutyunyan, Ինֆորմացիայի տեսություն, Դաս 4-8; moved 2026-10-24 from the session scratchpad)

| script | what it did | when you would look at it again |
| --- | --- | --- |
| `ashot_align.py` | First, coarse audio alignment: 1 s loudness envelopes of the 17 h recorder file and the camera, best correlation (Դաս 6: 201 s, Դաս 7: 230 s). | Superseded by `scripts/align_audio.py` (cross-correlation at 8 kHz, drift fit). Only for the streaming trick on a 17 h file. |
| `blank_video.py` | Black 640x360 1 fps video carrying a lecture's audio, uploaded private to get YouTube's auto-captions without uploading the 5 GB camera file. | The next course with raw files and no captions. Worth promoting to `non_essential/`. |
| `aligned_preview.py` | 360p studio.html preview for a lecture whose sound is a separate recorder: camera keyframes placed by the align JSON, black where the camera has no picture. | The next classroom recording with a separate recorder (edit-point review). Worth promoting. |
| `prproj_tracks.py` | Read a Premiere `.prproj` (gzipped XML): which media each track uses, mute / volume, Lumetri values. Used to copy Դաս 2-5's intro, outro, speed and audio choices (DECISIONS #28). | When a lecturer's earlier videos were cut in Premiere and the new ones must match. |
| `deck_titles.py`, `deck_pages_text.py` | Page titles of every slide deck and which pages each deck added; text of a page range plus the check that page numbers stay the same across the cumulative decks. | Mapping slides to lessons for another course with cumulative decks (`_knowledge/info_theory/slides_map.md`). |
| `codex_info_prompts.py`, `codex_info_run.sh` | Codex review of the chapter lists and titles: one prompt per lesson with the slides and the transcript inline, `codex exec -s read-only`, ~55-62 s per lesson. | Pattern for the next independent review (see `_learnings/2026-10-24-2041_codex-chapter-review-useful-but-check-each-claim.md`). |
| `stage_ashot_drive.py` | Copied the 4 final decks under their Drive names plus a README into `.playwright-mcp/drive_upload_ashot/` for the Playwright upload (DECISIONS #33). | Rebuilding the Drive folder. |
| `ashot_materials.py` | Put the 📚 block (page range, deck link, folder link) into the live descriptions of Դաս 0-5, 7, 8, checking local copies against live first. | Same change on another course. |
| `nest_info_chapters.py` | Nested the chapter lists of all 9 videos (4 spaces, one level, a parent has 2+ children) and wrote videos over an hour as H:MM:SS, from the live descriptions (DECISIONS #34). | Nesting another course's chapters. |
| `audit_info.py` | Read-only audit of the 9 videos: title format, date line, slide links and pages, chapters, `<` `>`, length, thumbnail, playlist. | Before making Դաս 4-8 public. |
| `build_info_overview.py`, `info_playlist_dump.py` | Built `_knowledge/info_theory/videos_overview.html` (all 9 videos at a glance, standalone) from the live data; dumped the playlist's titles and descriptions to JSON. | Refresh the overview page after a change. |

## tserunyan_2026-10/ (Anush Tserunyan, Մետրիկական տարածություններ և տոպոլոգիա, Դաս 15-27; copied 2026-10-25 from the session scratchpads)

Copied because their only copies sat in a session temp folder, where a Temp cleanup would have lost them; the
three still needed for the push went to `non_essential/` (`metric_assemble.py`, `metric_readback.py`,
`metric_review_page.py`).

| script | what it did | when you would look at it again |
| --- | --- | --- |
| `metric_replan5.py` | Re-planned 16-27 with content cuts + silences of 5 s or more, no hum join, kept as `*_v3_5s`, remapped the reviewed chapters onto each plan and ran the verifier; Դաս 15 onto the user's own edit (DECISIONS #26). 30-60 s per lecture. | Re-planning a course at another silence threshold. |
| `preview_queue.py` | Built the 360p studio.html video previews one after another and checked after each that the page's cut list was still the 5 s plan (two queues ran in parallel; Claude Code killed both once for low RAM). 11-21 min per lecture. | Building many previews in a row; run one queue at a time on this laptop. |
| `metric_nest.py` | Nested all 13 chapter masters by hand-picked line numbers (DECISIONS #39), checked the rules (one level, 2+ children), regenerated the derived files and proved only the indentation changed; Դաս 15's snapped list too. ~65 s. | Nesting the published Դաս 1-14 at the end (their lists come from the live descriptions, not from masters). |
| `user_pause_fit.py`, `user_pause_merge_fit.py`, `user_nonsilent_words.py` | Measured the user's Դաս 15 and 16 edits: silences re-detected in memory at 2-5 s and matched to their cuts (share cut per pause length), a join-across-short-sounds variant (worse at every setting), and what fills the added cuts that are not silence (fillers, clicks, Zoom's digital silence). ~20 s per lecture each. | The evidence behind DECISIONS #40 and `_learnings/2026-10-25-2052_tserunyan-edits-keep-her-math-talk-cut-pauses-from-4s.md`; the pattern for reading the next course's first reviewed list. |
| `metric_replan4.py` | Re-planned 17-27 from the user's answers (DECISIONS #40): unticked her math/talk content cuts, moved the 17/18 end cuts after her next-time line, kept Դաս 27's farewell, ran `find_edit_points.py --min-silence 4` (previews reused), kept `*_v4_4s`, remapped the nested chapters with `--hms`, verifier. 960 s for 11. | Re-planning again after the next review. |
| `metric_end_words.py`, `word_times.py` | Caption words with times around each end cut, and in any window (`word_times.py <lesson> <from> <to>`), to place cut edges at her sentences; check `--speech-map` too, captions run ~1 s off. | Placing a content-cut edge by her words. |
| `same_chapters.py` | Proves two chapter lists differ only in time format (same indents, seconds, labels). | After a reformat such as `--hms`. |

## vahagn_2026-10/ (Vahagn Mikaelian, Գծային հանրահաշիվ 21.1-28.4; copied 2026-10-25 from the session scratchpad)

| script | what it did | when you would look at it again |
| --- | --- | --- |
| `make_prompts.py` | One Codex review prompt per piece: series rules, title candidates, raw-timeline chapters, full transcript, all inline. Run with `codex exec -s read-only --skip-git-repo-check --ephemeral -C <dir> -o review_<s>.md - < prompt_<s>.md` (~50-75 s each). | The next Codex chapter review of a umath course. |
| `apply_review.py`, `verdicts_b1..b6.json` | Merged the checked Codex verdicts (take / partial / reject, with reasons) into `_knowledge/vahagn_linalg/codex_review.json` and title changes into `pieces.json`. | Same, as the bookkeeping pattern. |
| `lint_raw_chapters.py` | Lint of every `timestamps_raw.txt`: 00:00 start, increasing, 30 s gaps, a parent needs 2+ children, nothing too close to the end, no ASCII `<` `>`. | Before assembling drafts of nested chapter lists. |
| `find_removed.py`, `speed_test.py` | Tried to recover the previous editor's cuts by matching published vs raw loudness envelopes; the speed test showed the published pieces are 1x. Failed: the published audio was denoised and re-levelled (DECISIONS #35). | Only with unprocessed published audio. |
| `noise_spectrum.py`, `floors.py` | Noise character (band SNR, hum peaks) and floor / speech levels of a file; found the 47/70 Hz mains hum on 11 pieces (DECISIONS #37). | When a silence plan looks wrong on a noisy recording. |
| `loudness_samples.py` | Built `output/vahagn_linalg_overview/audio/loudness_samples.html`: 40 s of 21.1 and 23.3.b at own level / -20 / -16 / -14 LUFS after Ashot's chain (gain from the whole piece), 23.3.b untouched, published 20.3 as YouTube serves it. The user picked -16 (DECISIONS #38). | Choosing a level for another series. || `review_diff.py` | After a studio.html review: every returned cut against the sound (find_edit_points' own frames) and the transcript, the pauses of 1.5 s+ left uncut, and how well each minimum pause length matches the user's list. Showed on 21.1 + 21.2 that no threshold fits and 4 s costs fewest actions (`_learnings/2026-10-25-2050_...`). | To understand a returned review; reusable as is: `python review_diff.py <output dir>`. || `pause_visual.py` | Tested whether the user keeps the pauses where the screen changes (from the 360p preview): no, kept pauses are as still as cut ones (same learning). | Only if the screen theory comes up again. |
