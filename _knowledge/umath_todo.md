# Համալսարանական մաթեմատիկա: courses todo

One list across the umath channel's courses. Newest state first in each course; tick items as
they get done. Private source links (Zoom shares, the Drive access key) are in the git-ignored
`scripts/.secrets/umath_source_links.md`, not here: this repo is public.

Last updated: 2026-10-20 23:45.

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

Parked: too much work for now. Recording timeline in `_knowledge/info_theory/recording_timeline.md`;
lessons 4 and 5 got chapters, titles and dates on 2026-10-20.

## Sevak - Կոմպլեքս անալիզ

Done (25 lessons, playlist in lesson order).

- [ ] The Gmail reply drafted to him on 2026-10-20 was left unsent: send or delete it

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
- [ ] Դաս 16: once YouTube has processed the edit (length 1:17:10), check the chapters against
      the edited video, then push title and description
- [x] Դաս 17, 19-23: 6 s plans (`*_v3_6s`) chosen by the user 2026-10-22 ("6 is fine", DECISIONS #23)
- [ ] Դաս 17, 19-23: review the cut plans with the video previews, apply in Studio
- [ ] After the cuts are saved: remap chapters if the cut list changed, then push titles and
      descriptions (DECISIONS #10: wait until YouTube has processed the edit)
- [ ] Thumbnails: `python scripts/make_umath_thumbnails.py --series ant --lesson N --topic "..."`
      (local copy of the Canva template, `_knowledge/umath_thumbnails.md`); upload with
      `yt_publish.py --channel umath set-thumbnail`. Long titles need a shorter thumbnail topic.
- [ ] Possible correction notes: Դաս 23 slide "m^n ≤ N(I) ＜ m^(n+1)" should be (m+1)^n
      (~0:41:39); Դաս 16 "Carlitz wrote ~1000 papers" and "1936" unchecked
- [x] Lecture 19 is "Դաս 18-19", like "Դաս 11-12" (user, 2026-10-22, DECISIONS #24); drafts updated
- [ ] Decide: homework line (draft: 16, 17, 19 link Homework 5; 20-23 have none) (later)
- [x] Series standard written: `_knowledge/papikian_ant/standard.md` (no pause cuts: he writes
      during pauses; the earlier editor kept them too)
- [ ] Per video: content cuts, chapters, title, description, thumbnail
- [ ] Fix Դաս 4's date line: 23 -> 24 September 2024 (the Kaltura recording is dated 2024-09-24)
- [ ] Sort the playlist into lesson order (dry run: 13 moves; it is newest-first now)
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
- [ ] Decide: homework line for Դաս 27 (no homework dated after 19 May)
- [x] Per video: cut plan, chapters, title, description: drafted 2026-10-21 by 4 agents (2.01M
      tokens), generous pre-ticked cuts by the user's request. 81 min pre-ticked over 13 lectures
      (3.4-9.9% each), 22 min more as unticked suggestions. Drafts in each folder's `edited_predicted/`
- [x] Re-planned 2026-10-21 with the 4 s pause + hum rule ("yes do the same for metric"): 1215
      cuts, 3 h 1 min of 20.9 h (14%, 12-20% per lecture); content-only plans kept as
      `*_v1_content_only`; chapters remapped, all 13 verifiers valid (smallest gap 33 s).
      Դաս 18-21 were pushed in `3eb3a7d` before this: their new plans are uncommitted
- [x] 2026-10-22: back to content cuts only, like the older uploads (DECISIONS #22). The 4 s plans
      are kept as `*_v2_4s`, the active ones are `*_v1_content_only`
- [ ] Review the 13 cut plans (`edit_review/studio.html`), apply in Studio; then
      `scripts/remap_chapters.py --from-cuts studio_cuts.txt` if the list changed, then push
- [ ] Blur check in kept video: Դաս 15 edited 1:30:17-1:30:37 (screen share drops: a remote
      participant's name tag, Zoom page); Դաս 22 students' names in her notes from edited ~0:55:42.
      If a start cut is unticked: Դաս 20 (TA's email), 26 (her Gmail address), 27 (her bedroom) need blur
- [ ] Possible correction: Դաս 18 ~0:15:09 says "Egorov" for what is Lusin's theorem
- [ ] Per video: transcript, cuts in Studio, chapters, title, description, thumbnail
- [ ] Sort the playlist into lesson order (dry run: 11 moves)
- [ ] If the team finds lecture 1's recording, add it

## Vahagn Mikaelian - Գծային հանրահաշիվ (YSU, 2021 recordings)

Playlist `PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM` (73 videos, short pieces named by book section).
Source: his Drive folder bit.ly/LinAlgebraYSU, subfolder "Դասախոսությունների տեսագրություններ",
Videos Part 1-9 (90 files). He warned (email, 4 Nov 2025) that the recordings contain off-topic
student questions ("the dean's office told us that...") that must be cut.

On YouTube: Part 1-5 in full (1.1 to 16.2.b, 57 pieces), Part 6's three full lectures 07-09 cut
into Դաս 16.2-գ to 19.2 (10 pieces), Part 7's 20.1-20.3 and 21.2.

- [ ] Missing, Part 7: 21.1, 22.1, 22.2, 22.3
- [ ] Missing, Part 8: 23.1.a, 23.1.b, 23.2, 23.3.a, 23.3.b, 23.4, 24.1, 24.2.a, 24.2.b, 24.3, 24.4
- [ ] Missing, Part 9: 27.1, 27.2, 28.1.a, 28.1.b, 28.2.a, 28.2.b, 28.3.a, 28.3.b, 28.4
- [ ] Դաս 21.2 is titled "Todo": give it a real title (and chapters)
- [ ] Check what intro/outro the existing pieces use (a YSU course, so probably not the ASOF one)
- [ ] Download tool for Drive folders: `gdown` is not installed yet
- [ ] Sort the playlist into lesson order (dry run: 67 of 73 move)
- [ ] Not on YouTube at all, decide later: practical-session recordings, consultations
- Sections 25 and 26 are not in the folder (probably never recorded)

## Vahan - Խմբեր

- [ ] Not checked yet
