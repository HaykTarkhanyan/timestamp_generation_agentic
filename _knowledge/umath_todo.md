# Համալսարանական մաթեմատիկա: courses todo

One list across the umath channel's courses. Newest state first in each course; tick items as
they get done. Private source links (Zoom shares, the Drive access key) are in the git-ignored
`scripts/.secrets/umath_source_links.md`, not here: this repo is public.

Last updated: 2026-10-25 21:05 (Tserunyan section).

## Both channels: description audit (2026-10-22)

All 614 public/unlisted descriptions read line by line; details and findings #1-#61 in
`_knowledge/description_audit_2026-10-22.md`.

- [ ] Push the 60 remaining batch-2 fixes after the API quota reset (09:00 Munich): scratchpad
      `audit_fix_batch2.py push`, then `check`; planned texts also in
      `_knowledge/description_audit_2026-10-22_batch2_pending.json`
- [ ] Rerun `scripts/non_essential/glossary_scan_channels.py` after that push (expect 0 DENY)
- [ ] User decisions: the "user" and "verify" rows of the findings table
- [x] Dropped (the user, 2026-10-23: "why would we need that?"; every push script reads the live text first). Local copies older than live (ML 2-10, 18-20, ML-math 51-52, Complex 20-25; Papikian not yet compared):
      sync from live? Rerun the comparison after the quota reset (audit file, "Local vs live")

## Arnak Dalalyan - Բազմաչափ վիճակագրություն

Status (user, 2026-10-20): only editing and thumbnails remain; the professor has not been messaged.
Details in `_knowledge/arnak_multivariate/status.md`.

- [ ] Review the cut plans (`studio.html` in each output folder) for lesson 10 part 2, 11, 12, 13
      and the 2025 file, then apply them in Studio's Trim & cut
- [ ] After the cuts are saved: recheck chapters, then push the descriptions of 10-13
- [ ] 2025 recording: private frames until its cuts 2-3 are saved; students' names in the Zoom
      strip need a blur
- [ ] Thumbnails: `status.md` says 6-13 were pushed on 2026-10-20 22:02-22:07, so check which
      ones still remain (the 2025 file?)
- [ ] Message the professor (promised on 25 Apr: chapters fixed, title and thumbnail, then public)

## Ashot Harutyunyan - Ինֆորմացիայի տեսություն

Active again 2026-10-23: **todo list in `_knowledge/info_theory/todo.md`** (Դաս 6-8, consistency with 0-5, 1.25x).
Recording timeline in `_knowledge/info_theory/recording_timeline.md`; lessons 4 and 5 got chapters, titles and dates on 2026-10-20.
2026-10-24: Դաս 6-8 rendered, uploaded and finished; all 9 descriptions carry the slides block (Drive folder, page
ranges) and nested chapters; playlist sorted 0-8. **Waiting on Ashot's OK**, then Դաս 4-8 public.
All 9 at a glance: `_knowledge/info_theory/videos_overview.html`.

## Sevak - Կոմպլեքս անալիզ

Done (25 lessons, playlist in lesson order).

- [x] The Gmail reply to him: sent by the user (2026-10-23)

### His own channel: Honors Linear Algebra (fall 2026, ongoing) - for later

Stored 2026-10-22 by the user's request ("pls also store this for future"):
https://www.youtube.com/@sevakmkrtchyan-u1h (channel `UClkaOimplNdkXoTZgjM8k5g`, "Sevak Mkrtchyan";
same name as the Complex Analysis lecturer, not confirmed to be the same person). Checked
2026-10-22 through the API: channel created 16 Sep 2026, 14 subscribers, 10 videos "Linear
algebra lecture1" ... "lecture10" (59-79 min each), uploaded 16 Sep - 14 Oct 2026, about two a
week, so a course in progress; one playlist "Honors Linear Algebra" (`PLAF_dbBrwgc4`, 10 items).
No descriptions, no chapters; titles in English. "Honors" suggests an ASOF/ARCS-ai honors course
like Papikian's. Not on the umath channel.
- [x] Transcripts of all 10 fetched 2026-10-22 (Armenian auto-captions; lectures are in Armenian):
      `_knowledge/sevak_linalg_honors/` (README there). A credit course for students from several
      universities (a question at the end of lecture 1); the organizer is not named
- [x] Chapters for all 10 written 2026-10-22, verified: `comment.txt` in each lecture folder
- [x] Chapters reviewed twice more (an independent Claude agent, then Codex) and posted
      2026-10-22 13:03-13:06 as comments by the umath channel on all 10 videos ("lets post");
      all listed publicly, text identical to `comment.txt`, 232 of 232 timestamps linked
- [ ] Optional: pin them (the API cannot; by hand, and only the video owner can pin)
- [ ] Decide what to do with it (re-upload to umath with permission, or chapters/descriptions
      for his own uploads, or just link it); check the language and who runs the course

## Mihran Papikian - Հանրահաշիվ և թվերի տեսություն (ASOF, fall 2024)

**Parked 2026-10-21 (user).** Checked at 02:43: all 7 still unlisted, raw length, placeholder
titles; no Studio edit saved yet. Next is the user's review of the 7 cut plans.

Playlist `PLz3NrXxHz_CDF0l5rTCoxEqYoG3_na6Cs`. Source: PSU Kaltura links on
https://sites.google.com/view/mpapikian/teaching/algebra-and-number-theory (22 recordings).
On YouTube before: Դաս 1-15 (course lectures 1-10, 12 as "11-12", 13, 14, 15 parts 1+2).
Lectures 11 (midterm, probably) and 18 have no recording. Checked twice against the site.

- [x] Download the 7 missing lectures (16, 17, 19-23) from Kaltura, original Zoom flavor
- [x] Join the ASOF intro and outro (`scripts/concat_intro_outro.py`, DECISIONS #15); files in
      `Desktop\misc\YSU OpenCourseWare\papikian\Das NN - Algebra and Number Theory - Papikian - <date>.mp4`
- [x] Upload the 7 files (user, 2026-10-20; unlisted): 16 `Xe6XRo8O8yk`, 17 `6VxoPJLkCJA`,
      19 `VyWS3Ppv2ao`, 20 `VCK3I6CkJI8`, 21 `nzUWG6NFDCU`, 22 `txvgnlhu78E`, 23 `5tm6tnp8_4A`
- [x] Transcripts fetched for all 7 (Դաս 20's captions came ~1.5 h after upload)
- [x] Cut plans, chapters, titles, descriptions drafted 2026-10-21 by 3 agents (1.07M tokens):
      cut plan in each folder's `edit_review/studio.html`, drafts in `edited_predicted/`
- [x] Re-planned 2026-10-21 with the user's lesson-11 rule (4 s pauses + hums, DECISIONS #17) after
      "its suspiciously low": 423 cuts, 55.5 min over the 7 (16: 122, 17: 115, 19: 30, 20: 46,
      21: 40, 22: 35, 23: 35). Content-only plans kept as `*_v1_content_only`; chapters remapped,
      all verifiers valid (16 and 21: one too-short chapter merged in the v1 source)
- [x] 2026-10-22: back to content cuts only, to match the older uploads (DECISIONS #22; they were
      never silence-trimmed). The 4 s plans are kept as `*_v2_4s`. Դաս 16 has a video preview.
- [x] Դաս 16: the user's own edit (`studio_cuts_edited.txt`, 128 cuts after one merge, 16.0 min)
      entered in Studio by Playwright 2026-10-22 02:58, diff identical frame for frame; saved by the
      user the same night
- [x] Դաս 16: edit processed (1:17:10); chapters checked against the edited video (2026-10-22, below)
- [x] Դաս 17, 19-23: 6 s plans (`*_v3_6s`) chosen by the user 2026-10-22 ("6 is fine", DECISIONS #23)
- [x] Դաս 17: the user's 100-cut edit (`studio_cuts_edited_user.txt`; overlaps 74+75, 80+81,
      94+95 and a 0.24 s sliver 90+91 merged -> 96 cuts, 22.9 min, 1:27:36 -> 1:04:42) entered by
      Playwright 2026-10-22, read back against the user's list frame by frame, saved by the user
- [x] Դաս 18-19 (33 cuts -> 1:07:52), 20 (65 -> 1:19:56), 21 (82 -> 75 after merging the chain
      33-39 and 63+64 -> 1:14:30), 22 (72 -> 71, -> 1:15:12), 23 (88 -> 83: two overlaps and three
      silent/filler slivers of 1.1-1.5 s merged, -> 1:07:42): user's lists saved, checked, chapters
      remapped (all valid), entered by Playwright, read back against the user's lists, saved
      2026-10-22 (18-19 by the user; 20-23 by Claude with the user's permission after all checks
      passed: entry diff identical, user-list diff identical apart from the noted merges, Save dialog
      length = prediction). 20 and 22 needed `--type-shift -1` (learning 2026-10-22-1640)
- [x] All 7 processed by 17:46 (YouTube lengths = predictions, +1 s rounding)
- [x] 2026-10-22 run (`_knowledge/papikian_ant/finish_16-23.md`): new captions; chapters snapped
      onto them (cut list confirmed 0 +-1 s); independent Claude and Codex reviews, every claim checked
      against the transcript, then reconciled: 4 titles changed (16, 17, 18-19, 20), 67 chapters
      changed + 6 added + 6 merged away, all 7 lists verifier-valid. Final files in each `<folder>/edited/` (`titles.txt`,
      `timestamps.txt`, `description.txt`, `review_notes.md`); thumbnails `thumbnails/umath/ant_*.png`
      (16, 17, 18-19, 20-23); one review page `_knowledge/papikian_ant/review_16-23.html`
- [x] Pushed 2026-10-22 18:24 on the user's go ("upload everything, never change the visibility"):
      titles, descriptions (homework line as drafted, no correction notes) and thumbnails of all 7;
      read back from the API: all match the local files, all still unlisted. Final check before the
      push caught one leftover (Դաս 20 01:17:58 Cl(K) -> H(K))
- [x] All course files (notes, homework, midterm solutions, project, lecture 14 problems) in one
      public math-team Drive folder; the 📚 block of all 21 videos links them, plus his site as a backup (2026-10-22 18:40 / 20:41,
      read back: all match). `_knowledge/papikian_ant/drive_materials.md`
- [x] All 21 videos public (2026-10-22 20:43, user: "make all videos public"; 16-23 via videos.update(part=status), own status fields sent back; read back 21 of 21 public)
- [x] 2026-10-22 20:49-20:52: midterm link on Դաս 10, project link on Դաս 11-12; "Չօրինակ" -> "Հակաօրինակ" on both channels (learning 2026-10-22-2052)
- [x] 2026-10-22 21:00 glossary cross-check of all Papikian labels and the Sevak comments: 7 fixes live (learning 2026-10-22-2052)
- [x] Open terms decided and applied 2026-10-23 13:26-13:32 (the user's Q21): division ring = բաժանումով օղակ, Համիլտոն-Քեյլի and պրիմար բաժանարարներ / ինվարիանտ ֆակտորներ (his own words in Դաս 14) kept; Դաս 22 Eisenstein -> Դաս 7's Այզընշտայն; Ֆուրյե, կոռելացիա, բազմանդամային օղակ, չհատվող ցիկլեր, ℤ[i] fixed live on 25 videos; ML [08] suffix, ML [41] -> 'Մեկ նեյրոնից ցանց'; the BRIGHTNESS Դաս 5 duplicate unlisted; all read back; glossary + denylist updated; rescan 0 DENY (40 NEAR, 383 ENG). Backup: `_knowledge/descriptions_before_term_fixes_2026-10-23.json`
- [x] 2026-10-22 21:35: glossary check in the workflow (glossary_check.py, denylist, SKILL.md); scan of both channels: 0 DENY; 10 description typos + 7 title typos fixed (learning 2026-10-22-2052)
- [x] Open terms from the scan: done, see above
- [ ] Optional: plain read of the ~7,450 chapter labels outside Papikian
- [x] Sort the playlist into lesson order (2026-10-23, see below)
- [x] No correction notes (the user, 2026-10-23: none on umath, DECISIONS.md #25). Slips found: Դաս 23 slide "m^n ≤ N(I) ＜ m^(n+1)" should be
      (m+1)^n (~0:41:39); Դաս 16 "Carlitz wrote ~1000 papers" and "1936" unchecked; Դաս 21: N(I)
      missing a square (31:21), "Noetherian ⇒ finite Krull dimension" (23:10), split primes
      determine K only if Galois (01:13:02). Full list on the review page
- [ ] Դաս 22: Armenian spelling of Eisenstein ("Այզենշտայնի" kept; "Էյզենշտեյնի"?) unverified
- [x] Lecture 19 is "Դաս 18-19", like "Դաս 11-12" (user, 2026-10-22, DECISIONS #24); drafts updated
- [ ] Decide: homework line (draft: 16, 17, 19 link Homework 5; 20-23 have none) (later)
- [x] Series standard written: `_knowledge/papikian_ant/standard.md` (no pause cuts: he writes
      during pauses; the earlier editor kept them too)
- [ ] Per video: content cuts, chapters, title, description, thumbnail
- [x] Դաս 4's date line 23 -> 24 September 2024: pushed 2026-10-23 12:43, read back (old text in `_knowledge/papikian_ant/description_das4_before_date_fix_2026-10-23.json`)
- [x] Playlist sorted into lesson order 2026-10-23 12:41 (set to "Manually sorted" in Studio first; 20 of 21 moved, read back 1-23)
- [ ] Optional: link each lecture's own notes PDF in its description instead of the course page

## Mihran Papikian - Galois Theory (ARCS-ai, fall 2025): candidate, not started

Found 2026-10-22 on his Teaching page (https://sites.google.com/view/mpapikian/teaching). The user:
"we may want to get it later as well". Not on the channel (no playlist; searching the channel's
videos for "Գալուա" / "Galois" finds nothing).

- ARCS-ai Honors Course (Advanced Research in Computational Sciences and AI, ԲԱԳԻՆ), YSU Krisp
  AI lab; lectures over Zoom in Armenian, notes and homework in English; recitations by the TA
  in person. 12 weeks from 16 Sep 2025, Wed and Sat; 90-min lecture + 60-min recitation.
- 23 lectures (17 Sep - 17 Dec 2025) + an oral final (20 Dec). Recordings for 22 (none for
  lecture 1): 20 on PSU Kaltura like the ANT course, lectures 15 and 16 as Google Drive videos.
- Notes, homework 1-8 and the final exam PDF are downloaded in
  `_knowledge/papikian_site/galois_theory_2025/`; every link, recordings included, is in
  `_knowledge/papikian_site/manifest.json`.
- [ ] Decide whether to publish it, and with which intro and outro (it is ARCS-ai, not ASOF)
- [ ] If yes: download the 22 recordings (Kaltura's small `mp42` flavor is the Zoom original,
      `_learnings/2026-10-20-2208_kaltura-small-720p-flavor-is-the-zoom-original.md`), then the
      usual cut plans, chapters, titles, descriptions, thumbnails, a new playlist

## Anush Tserunyan - Մետրիկական տարածություններ և տոպոլոգիա (ASOF, spring 2023)

**DONE 2026-10-27** (the user: "make Anush as done"). Դաս 15-27 cut in Studio, chaptered (nested, H:MM:SS), titled,
thumbnailed, pushed and public; Դաս 1-14 nested; playlist in lesson order; notes and homework on the math-team Drive;
email to her sent 2026-10-27 11:11 UTC. Nothing open; only if the team ever finds lecture 1's recording.

Lessons from finishing Papikian, step by step: `_knowledge/umath_course_playbook.md`.
Playlist `PLz3NrXxHz_CA3NjE0D_amd_QcTMx5HJvZ`. Course page
https://www.math.mcgill.ca/atserunyan/Courses/2023_S.Yerevan.Metric&Top/ (27 lectures; 1 and 7
never recorded). On YouTube before: Դաս 1-2 (= lecture 2), 3-6, 8-14. Source: McGill Zoom
share links from the filming team's Telegram (still downloadable, no passcode).

- [x] Download lectures 15-27 (13 files, 3.39 GB, 1920x1342, Zoom original)
- [x] Join intro and outro (2026-10-20/21, three queues, 47 min; all 13 lengths as expected,
      join checks clean). Intro and outro padded with white to 1920x1342, not stretched.
      Files: `Desktop\misc\YSU OpenCourseWare\metric_spaces\Das NN - Metric Spaces and Topology - Tserunyan - <date>.mp4`
- [x] Raw downloads deleted 2026-10-21 (3.39 GB; re-downloadable from the Zoom links)
- [x] Upload the 13 files (user, 2026-10-20, unlisted): 15 `ANoJdXQEOOA`, 16 `3K76N175zvM`,
      17 `uqI8xFU3fkc`, 18 `UdfgVV4qofs`, 19 `zTxIdWu_4pk`, 20 `4L-qOijveyU`, 21 `KNoSL5it7gA`,
      22 `B7V06PBa79g`, 23 `qtZsHmGWQD8`, 24 `OnsBx1KRAFk`, 25 `3E1Tmzyoy_s`, 26 `8i6uYydDd4E`,
      27 `FSV22FEP16A`
- [x] Transcripts fetched for all 13 (2026-10-21 01:42; 1195-1613 lines each)
- [x] Series standard: `_knowledge/tserunyan_metric/standard.md` (2026-10-21). Unlike Papikian, the
      earlier editor cut 12-21% per lecture (start chat, room-mic conversations, logistics; no pauses)
- [x] Homework line for Դաս 27: links hw12, the course's last homework (the user's Q10, 2026-10-23)
- [x] Per video: cut plan, chapters, title, description: drafted 2026-10-21 by 4 agents (2.01M
      tokens), generous pre-ticked cuts by the user's request. 81 min pre-ticked over 13 lectures
      (3.4-9.9% each), 22 min more as unticked suggestions. Drafts in each folder's `edited_predicted/`
- [x] Re-planned 2026-10-21 with the 4 s pause + hum rule ("yes do the same for metric"): 1215
      cuts, 3 h 1 min of 20.9 h (14%, 12-20% per lecture); content-only plans kept as
      `*_v1_content_only`; chapters remapped, all 13 verifiers valid (smallest gap 33 s).
      Դաս 18-21 were pushed in `3eb3a7d` before this: their new plans are uncommitted
- [x] 2026-10-22: back to content cuts only, like the older uploads (DECISIONS #22). The 4 s plans
      are kept as `*_v2_4s`, the active ones are `*_v1_content_only`
- [x] 2026-10-22/23, without the user (`_knowledge/tserunyan_metric/finish_15-27.md`): her course page
      saved (`_knowledge/tserunyan_site/`, 40 PDFs); all 13 chapter lists and titles reviewed inline
      against transcripts and her notes (`review_15-27.md`: 27 of 366 chapters changed, 1 added); glossary
      0 DENY; blur frames checked; thumbnails `thumbnails/umath/metric_15..27.png`; review page
      `_knowledge/tserunyan_metric/review_15-27.html`
- [x] Դաս 15: the user's cut list saved in Studio (2026-10-23 03:57), then captions, snapped chapters,
      title, description and thumbnail pushed and read back (12:05-12:08); unlisted
- [x] Դաս 16 reviewed by the user on studio.html (2026-10-25): 121 cuts (56 new, 5 content cuts unticked),
      `cut_list.py check` OK, entry list `studio_cuts_to_enter.txt` 120 cuts, 1:42:35 -> 1:29:35; chapters
      remapped onto it (H:MM:SS, verifier valid)
- [x] Դաս 16 entered in Studio and saved (2026-10-26 ~00:01, under the umath channel: the tab had been on Metric,
      switched on the user's Q56): 120 cuts, diff identical frame for frame, dialog 1:29:34 as predicted
- [x] Դաս 17 reviewed by the user (2026-10-25): 124 cuts (21 new, 12 changed, 2 removed), `cut_list.py check` OK,
      entry list 122 cuts (119+120, 123+124 merged), 1:49:34 -> 1:35:17; chapters remapped, verifier valid
- [x] Դաս 17 entered in Studio and saved (2026-10-26 ~00:22): 122 cuts in 18.3 min with the faster loop,
      diff identical, dialog 1:35:17 as predicted
- [x] Դաս 18 reviewed by the user (86 cuts -> 83, 1:15:03) and saved in Studio 2026-10-26 ~01:12; this upload stores
      cuts a frame late, entered with `--type-shift -1` after cut 1 came out shifted (deleted, re-entered)
- [x] Դաս 19 reviewed by the user (88 cuts: 53 new, 20 changed -> 87 to enter) and saved in Studio 2026-10-26 ~01:56,
      1:27:14 as predicted, no frame shift; the user keeps 7 s for 20-27 (Q61)
- [x] Դաս 20 reviewed (19 cuts: 2 new, 7 changed, 6 removed) and saved in Studio 2026-10-26 ~02:00, 1:25:13 as
      predicted; frame-late upload like 18 (`--type-shift -1`)
- [x] Դաս 21 reviewed (all 17 pause cuts removed, 6 content cuts kept) and saved in Studio 2026-10-26 ~02:08, 1:29:20
- [x] Դաս 22-27 re-planned with content cuts only, no pause cuts (DECISIONS #43, the user: "im fed up with them")
- [x] Դաս 22 reviewed (37 cuts: 30 new, mostly pauses, 6 changed) and saved in Studio 2026-10-26 ~12:39, 1:19:55 as
      predicted, no frame shift (162 s of entry). The user: the added pauses are a "one time thingy", 23-27 stay
      content cuts only (DECISIONS #43 unchanged)
- [x] Դաս 23 reviewed (7 cuts: 2 suggestions taken, 4 changed, 1 removed) and saved in Studio 2026-10-26 ~12:52,
      1:23:03 as predicted, no frame shift. Two suggestions left out on purpose (Q64 "Save as is"): the 24 s
      "allergy to the real numbers" aside and the 6.9 min König's lemma discussion
- [x] Դաս 24 reviewed (2 cuts: start and end, both changed; 4 ticked cuts in 0:23-0:33 removed) and saved in Studio
      2026-10-26 ~13:06, 1:28:11 as predicted, no frame shift. Q65 "save as is": the 0:52 poll, 1:26 false start
      and 1:31 course plan suggestions stay
- [x] Դաս 25 reviewed (7 cuts: 6 changed, 1 new, 4 ticked removed; cuts 1+2 overlapped by 6 frames, merged -> 6)
      and saved in Studio 2026-10-26 ~13:10, 1:31:14 as predicted, no frame shift; no suggestions in this plan
- [x] Դաս 26 reviewed (3 cuts, all changed; the ticked 1:19:15 questions + Alexander false start removed) and saved
      in Studio 2026-10-26 ~13:14, 1:41:47 as predicted, no frame shift; start cut still covers the Gmail tab.
      Q67 "save as is": the 0:42 drawing, 0:58 "Any ideas?" and 1:00 thinking-aloud suggestions stay
- [x] Դաս 27 reviewed (1 cut: the start, now to 0:02:13:19, still past the bedroom; the other 5 ticked cuts removed)
      and saved in Studio 2026-10-26 ~13:22, 1:39:45 as predicted, no frame shift. Q68 "save as is": the 0:07
      name fumble, 1:01 wait, 1:34 wrap-up and the farewell stay. **All 16-27 are now saved in Studio**
- Not a preference to carry over (the user, Q69, 2026-10-26: "those arent learning, i just got fed up with this
  course"): the light 23-27 reviews (15 of 33 ticked cuts removed, 2 of 16 suggestions taken) say nothing about
  how to plan the next course
- (26 and 27 were done under the user's Q66 "Keep holding Save": each list compared with the suggestions, cuts
  entered, the left-out suggestions asked about, then saved)
- **Standing "pw" for 20-27** (the user's Q63, 2026-10-26: "Yes, 20 now and all pasted lists"): every list the user
  pastes is checked, entered in Studio and saved when the frame diff is identical and the dialog shows the predicted
  length (DECISIONS #27 checks); report after each
- [x] Դաս 19-27 re-planned with pauses from 7 s (DECISIONS #42, the user's "automated are toooo much extra work")
- [x] At the end, for all of 16-27 together (the user's Q57, 2026-10-26: "we do all together in the end"), once
      YouTube has processed each edit: fetch the edited captions into `edited/`,
      `map_transcript_to_edit.py`, remap `--hms`, snap `--hms`, verifier, `metric_assemble.py`, glossary, push
      title/description/thumbnail, `metric_readback.py` (with Դաս 15's re-push, Q41)
  - 2026-10-26 ~14:25, local part DONE for all 12 (Q70 "start, stop before push"): all 12 edits applied on YouTube
    (API lengths match), edited captions fetched with yt-dlp (24, 26, 27 only on the second try ~10 min later),
    snapped `--hms`, 12/12 verifier-valid, 0 DENY, `edited/description.txt` assembled, 13 dates match the files.
    Codex review of all 13 titles + descriptions (the user's ask): titles kept, 9 label fixes taken in 15, 17, 18,
    21, 26, 27, the Դաս 24 "ոչ տրիվիալ" finding rejected (`codex_desc_review_2026-10-26.json`). Review page rebuilt.
    **Next: the user's go for the push (16-27 title/description/thumbnail + Դաս 15 description), then readback**
- [x] studio.html shows the timeline and every cut on its own again (DECISIONS #41): 18-27 rebuilt, 18 checked in
      Playwright; 26 and 27 keep her thinking-invitation waits (Q52, DECISIONS #40 refinement): 84 and 138 cuts
- [x] Դաս 17-27 re-planned from the user's 16 edit (2026-10-25, DECISIONS #40): pauses from 4 s, her math/talk
      cuts as suggestions, ends after her next-time line, Դաս 27's farewell kept. 74-139 cuts, 9.6-16.3 min
      each; all 11 verifier-valid, video previews kept; review page rebuilt
- [x] (done 2026-10-26, all 12 saved, processed and pushed) Դաս 17-27: the user reviews each on `edit_review/studio.html` and sends the list with "pw"; Claude enters
      and saves it (DECISIONS #27), then after processing the steps in `_knowledge/tserunyan_metric/finish_15-27.md`
      (captions, remap from `timestamps_raw.txt` with `--hms`, snap with `--hms`, verifier,
      `metric_assemble.py`, glossary, push, `metric_readback.py`). Keep the start cuts of Դաս 20, 26, 27
      ticked: they hide the TA's email, her Gmail inbox and her bedroom (else blur)
- [x] Blur decided 2026-10-23: Դաս 15's 18 s Zoom gallery left as is (Q6); Դաս 22 student first names stay,
      they are in her public PDF (Q11)
- [x] No correction notes on umath (DECISIONS.md #25, 2026-10-23). Slips kept unpublished in `lecturer_slips_not_published.txt` (17, 18 "Egorov" for Lusin, 19, 24, 27)
- [x] Chapters nested, 15-27 (2026-10-25, DECISIONS #39): 252 of 376 under 61 parents, in the masters
      `edited_predicted/timestamps_raw.txt` (flat copies `timestamps_raw_flat.txt`) and Դաս 15's `edited/`
- [x] Times H:MM:SS throughout (Q40, 2026-10-25): Դաս 15's `edited/` redone, 16-27 drafts too
- [x] Re-push Դաս 15's description (now nested, H:MM:SS) together with the 16-27 pushes (Q41): done 2026-10-26
- [x] **15-27 pushed 2026-10-26 14:28-14:31** (the user's Q71 "Push all 13"; scratchpad `metric_push.py`): 16-27
      title + description + thumbnail, Դաս 15 description; `metric_readback.py` after each: 13/13 title OK,
      description OK, chapter lines 26-34, all still unlisted
- [x] 2026-10-27 terms (DECISIONS #49, the user's Q84 A / Q85 A): "Գեներիկ էրգոդիկություն" -> "Էրգոդիկություն ըստ
      Բեռի" in Դաս 16, 17 (titles, thumbnails, 6 chapters), "Պրոֆինիտ տոպոլոգիա" -> "Թվաբանական պրոգրեսիաների
      տոպոլոգիա" in Դաս 19 (2 chapters); she says both in English. Masters + snapped lists edited, assembled, 0 DENY,
      pushed 11:48 and read back (API + viewer: titles, 29/34/30 chapters parsed, served thumbnails ours), still unlisted.
      Both words in the glossary denylist. Review page rebuilt
- [x] Drive renamed 2026-10-27 11:59-12:00 (Q87, Playwright at `drive/u/2`, right-click -> Rename): notes 16 and 17 to
      the new titles, and our homework name "Տնային 8 - ..., գեներիկ էրգոդիկություն, ..." -> "..., էրգոդիկություն ըստ
      Բեռի, ..."; IDs unchanged, `drive_folder_ids.json` keys updated; folder search finds no "Պրոֆինիտ"
- [x] **15-27 public** 2026-10-27 11:58 (Q25, the user: "yes make public"; `scripts/archive/tserunyan_2026-10/make_public.py`):
      videos.update(part=status), own writable fields sent back; read back 13/13 public, no other status field changed;
      backup `_knowledge/tserunyan_metric/status_before_public_2026-10-27.json`; ~650 quota units. Playlist was already public
- [x] Message her (Q74): **sent by the user 2026-10-27 11:11 UTC** (no earlier thread with her in this mailbox), to
      her McGill address from her course sheet, Aprikyan in cc as for Papikian, Armenian, playlist + Drive folder with
      the full URLs ("put the urls as well"); the user edited the wording before sending
- [x] At the end: nest the published Դաս 1-14 the same way and write their times H:MM:SS (DECISIONS #39): done
      2026-10-26 16:25-16:27 (the user's Q75): 160 of 295 chapters under 50 parents, labels and seconds unchanged,
      12/12 read back identical (one retry: a read right after the write served the old text), YouTube parses every
      chapter. Backup `_knowledge/tserunyan_metric/descriptions_before_nest_2026-10-26.json`, preview
      `nest_1-14_preview.html`
- [x] Scripts the push needs are in the repo now: `scripts/non_essential/metric_assemble.py`,
      `metric_readback.py`, `metric_review_page.py` (finished ones in `scripts/archive/tserunyan_2026-10/`)
- [x] Playlist sorted into lesson order 2026-10-26 14:38 (the user's Q72): it was on "Date published (newest)",
      switched to "Manually sorted in YouTube" in Studio first (as in learning 2026-10-20-2221); 15 of 25 moved,
      read back 1-2, 3-6, 8-27 (lecture 7 was never recorded)
- Q73 "Not yet": 15-27 stay unlisted for now; Q74: the message to her comes later, after they are public
- [x] 2026-10-26 live check of 15-27 as a viewer (yt-dlp): 13/13 titles OK, YouTube parses every chapter (nested
      included), the served thumbnails are ours (mean difference 0.1 of 255), all unlisted
- Note for every session: DECISIONS.md numbers collided (two #39, two #40 from two sessions at once); the Vahagn
  ones are #44 and #45 now (the user's Q76). **Next free number: #50** (2026-10-27). Check the top of the file before numbering
- If the team ever finds lecture 1's recording, add it (not an open task)

## Vahagn Mikaelian - Գծային հանրահաշիվ (YSU, 2021 recordings)

Playlist `PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM` (73 videos, short pieces named by book section).
Source: his Drive folder bit.ly/LinAlgebraYSU, subfolder "Դասախոսությունների տեսագրություններ",
Videos Part 1-9 (90 files). He warned (email, 4 Nov 2025) that the recordings contain off-topic
student questions ("the dean's office told us that...") that must be cut.

On YouTube: Part 1-5 in full (1.1 to 16.2.b, 57 pieces), Part 6's three full lectures 07-09 cut
into Դաս 16.2-գ to 19.2 (10 pieces), Part 7's 20.1-20.3 and 21.2.

**2026-10-24: state, dates, Drive IDs and problems in `_knowledge/vahagn_linalg/status.md`.**

- [x] Missing pieces downloaded 2026-10-24 via Playwright (Drive opens only for the user's personal
      account, `drive/u/1`): Part 7 21.1, 22.1, 22.2, 22.3; Part 8 23.1.a-24.4 (11); Part 9 27.1-28.4 (9)
- [ ] Upload, edit (the published pieces had ~15% cut), chapters, titles, descriptions, thumbnails
- [ ] Դաս 21.2 is titled "Todo": give it a real title (and chapters)
- [x] Intro/outro: none (published 20.3 starts on the raw file's first frame)
- [ ] Sort the playlist into lesson order (dry run: 67 of 73 move)
- [ ] Not on YouTube at all, decide later: practical-session recordings, consultations
- Sections 25 and 26 are not in the folder (probably never recorded)

## Vahagn Mikaelian - Խմբեր

The same lecturer as the linear algebra course above ("Vahan" was a typo, the user 2026-10-23).

- [ ] Not checked yet
