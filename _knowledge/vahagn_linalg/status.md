# Գծային հանրահաշիվ (Vahagn Mikaelian, YSU, spring 2021): state of the videos

Playlist `PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM` on Համալսարանական մաթեմատիկա. Checked 2026-10-24 through
the YouTube API (`output/vahagn_linalg_overview/overview.html`, `playlist_overview.py`) and his Drive.

## Source

- His Drive folder `0B0uKw1SkNt5AUkJnMlUxTGd1M0E` (`bit.ly/LinAlgebraYSU`, now titled "Գծային հանրահաշիվ,
  2026"). Opens only for the user's personal account (Playwright `drive/u/1`); the Metric Academy (u/0)
  and math-team (u/2) accounts get "You need access", and signed out it asks to sign in. The link needs
  `resourcekey=0-UeF9nxlvJcVM7uBFRmniPw` (Drive adds it for an account with access).
- Subfolder "Դասախոսությունների տեսագրություններ" `1duYcBdV7T89qR90RFOhLyzX4YjndxNS5` holds Videos
  Part 1-9; file IDs of Parts 7-9 in `drive_files.json`. Other subfolders, not on YouTube: practicals
  (Գործնականների տեսագրություններ), consultations (Կոնսուլտացիաներ, 2024), textbooks, an old conspect.
- The description link `http://bit.ly/LinAlgebra` («Դասախոսությունների ֆայլը») is a different link:
  signed out it lands on his book "Linear Algebra: Theory and Algorithms" on ResearchGate. It works.
  (`playlist_overview.py` reports it as 403 because bit.ly refuses scripted requests.)

## What the files are

- `VidSection <book section>.mp4`: screen recordings of his annotated PDF book, 1366x768, 25 fps, AAC,
  already split by section. No intro or outro on YouTube (first frames of published 20.3 = the raw file).
- **The published pieces were edited:** 20.1 raw 27:15 -> YouTube 22:50, 20.3 raw 15:22 -> 13:07
  (about 15% removed). He warned (email, 4 Nov 2025) about off-topic student questions in the recordings.
- **Lecture dates from the files' `creation_time`:** every file was exported right after a lecture,
  Tuesdays ~14:2x and Thursdays ~11:0x Yerevan time. Checked on 20.1 (27 Apr, matches its description).
  20.3 was exported on 29 Apr but its description says 27 Apr: one of the two is wrong.

## Downloaded 2026-10-24 (Playwright, account u/1)

`C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg\Videos Part 7|8|9\` (1.4 GB):
exactly the 24 missing pieces, for upload. 20.1, 20.3 and 21.2 (already on YouTube) are in
`vahagn_linalg\already_on_youtube\`. Durations from ffprobe; date = the file's creation date (Yerevan).

| Section | Raw length | Date (2021) | YouTube |
|---|---|---|---|
| 20.1 | 27:15 | Tue 27 Apr | `Kh2Etr0epP0` public (22:50); downloaded only for comparison |
| 20.3 | 15:22 | Thu 29 Apr | `pCzP2OJnUns` public (13:07), says 27 Apr; for comparison |
| 21.1 | 22:07 | Thu 29 Apr | missing |
| 21.2 | 27:41 | Thu 29 Apr | `brEvgF3isUE` **private**, raw upload (27:42), title "Todo" |
| 22.1 | 17:49 | Tue 4 May | missing |
| 22.2 | 24:16 | Tue 4 May | missing |
| 22.3 | 13:22 | Tue 4 May | missing |
| 23.1.a | 14:39 | Tue 4 May | missing |
| 23.1.b | 20:36 | Thu 6 May | missing |
| 23.2 | 21:40 | Thu 6 May | missing |
| 23.3.a | 29:28 | Thu 6 May | missing |
| 23.3.b | 9:37 | Thu 6 May | missing |
| 23.4 | 18:42 | Tue 11 May | missing |
| 24.1 | 15:56 | Tue 11 May | missing |
| 24.2.a | 16:44 | Tue 11 May | missing |
| 24.2.b | 10:21 | Thu 13 May | missing |
| 24.3 | 26:32 | Thu 13 May | missing |
| 24.4 | 18:01 | Thu 13 May | missing |
| 27.1 | 27:29 | Tue 18 May | missing |
| 27.2 | 18:07 | Tue 18 May | missing |
| 28.1.a | 20:24 | Tue 18 May | missing |
| 28.1.b | 23:17 | Thu 20 May | missing |
| 28.2.a | 24:55 | Tue 25 May | missing (exported after 28.3 and 28.4) |
| 28.2.b | 9:42 | Tue 25 May | missing |
| 28.3.a | 22:06 | Thu 20 May | missing |
| 28.3.b | 5:14 | Thu 20 May | missing |
| 28.4 | 24:51 | Thu 20 May | missing |

24 missing pieces, 7.6 h raw. Sections 25 and 26 are not in the folder.

**Uploaded by the user 2026-10-24 19:31-19:50 UTC**, private, titled by file name ("VidSection 23 3 a").
Checked 2026-10-25: all 24 there once, processed, YouTube length = local file +-1 s. Video IDs in
`uploads.json`. **Set unlisted 2026-10-25** (API, only privacyStatus, read back) so yt-dlp can fetch the
captions; all 24 transcripts fetched into `output/2026-10-25_VidSection-*`. Their metadata already matches the
published pieces (category 27, language/audio hy, YouTube license, not made for kids: channel defaults).

## Plan now (DECISIONS #38, 2026-10-25 evening)

Only the sound is fixed locally (`scripts/non_essential/vahagn_audio_fix.py --target-lufs -16`: Ashot's chain, gain to
-16 LUFS, peaks at -1 dBFS, picture copied), into `vahagn_linalg\audio_fixed\` (results `audio_fix.json`). The user
uploads those as new videos; the reviewed cut lists go in through YouTube Studio's editor (same timeline as the raw
files); then titles, descriptions, thumbnails, playlist. The 25 caption uploads go afterwards. Level picked on
`output/vahagn_linalg_overview/audio/loudness_samples.html` (published 20.3 plays at -29.7 LUFS for comparison).
**Done 2026-10-25 20:24:** all 25 in 31.8 min (8.06 h, 1.36 GB; ~15x realtime on average, not the 27x of the 28.3.b
test); out -16.5..-17.4 LUFS (23.3.b lowest: gain +14.1 dB, the limiter took more), peaks -0.5..-0.8 dBFS; picture and
lengths checked per file. Named `VidSection <section> fixed.mp4` (YouTube shows "VidSection 21 1 fixed", the raw
caption uploads "VidSection 21 1"). **Uploaded by the user 2026-10-25 19:29-19:53 UTC** (private; ids in
`uploads_fixed.json`, each length = its fixed file within 1.5 s). **Pushed 21:00-21:03** with
`scripts/non_essential/vahagn_push_metadata.py --chapters raw --apply` (3,750 units): title, description with the
chapters on the RAW timeline (the uploads are uncut), unlisted, thumbnail, playlist; read back 25/25. After a piece's
cuts are saved in Studio: `--chapters edited --description-only --apply <section>` (50 units).
- **Playlist (checked 21:05):** it sorts itself by date, so the 25 sit in upload order (28.4 ... 28.1-ա, 24.2-բ, 24.2-ա,
  24.1, 23.4, 23.3-բ, 27.2, 27.1, 24.4, 24.3, 22.1, 21.2, 21.1, 23.3-ա, 23.2, 23.1-բ, 23.1-ա, 22.3, 22.2), then 20.3 ...
  1.1. Also in it and visible (both unlisted): old `Դաս 21.2 | Todo` brEvgF3isUE (position 26) and the raw
  `VidSection 21.2.mp4` nrKtWsRzEHA (98). `yt_publish.py sort-playlist --by lesson` reads only a whole lesson number,
  so it cannot order 23.1-ա / 23.1-բ.

## Plan before (DECISIONS #35, superseded by #38)

These uploads are only a caption source. Each piece is cut and its sound fixed locally (`render_lecture.py`,
1x, no intro/outro, no dip), then uploaded as a new video; the raw uploads go afterwards.

- **Sound** (raw 21.1: mono AAC 32 kHz, -24.1 LUFS, speech 53 dB over the quiet frames, faint 47/94 Hz hum,
  little above 4 kHz): four A/B samples in `output/2026-10-25_VidSection-21-1_LXdnQ7wFjcw/audio_samples/`
  (raw / level to -16 LUFS / + light cleanup / + treble and compression). Waiting for the user's pick.
- **Sound, the user's pick (2026-10-25):** first "raw is fine", then option 3 (80 Hz low cut + light afftdn,
  `render_lecture.py --denoise`) since a local render costs little. Open: the level (Q82: -16 LUFS as sampled, ~11
  dB louder than the published pieces, or no gain, ~-24 LUFS). The first number was inflated: YouTube keeps the
  level (our raw 21.1 upload: -24.2 LUFS vs the file's -24.1), and published 20.1/20.3 are ~3 dB under their raw
  files, not 6 (the mono downmix of YouTube's stereo cost 3 dB). Their noise floor is 11-17 dB lower than
  YouTube's codec alone explains (21.1: raw -80.2 -> YouTube -87.6; 20.3: -79.8 -> -96.7; 20.1: -68.9 -> -92.0),
  so they were denoised.
- **Noise floors of the 24** (first channel, 5th pct of 10 ms frames): 14 pieces at -77..-82 dB like 21.1; 10 at
  -56..-59 dB (23.1.b, 23.2, 23.3.a, 24.4, 28.1.a-28.4) and 23.3.b at -47.6 dB with speech at only -43.6 (Q83:
  sample one before rendering those).
- **Render timing (2026-10-25):** `render_lecture.py --speed 1 --dip 0 --denoise --gain-db 8.9 --encoder qsv`
  with ffmpeg 9, 1080p: 3.0x realtime (2 min window in 38 s), 0.3 Mbps video, text as sharp as the raw
  (crops compared). All 24 = ~7.1 h of output = ~2.4 h of rendering, one piece at a time after its review.
- **Cuts:** 21.1 first, on studio.html. The user asked for **4 s** (15 cuts, 1.3 min, 22:07 -> 20:48) with
  the 360p video preview (made in 189 s); 2 s gave 67 cuts / 3.0 min, 3 s 26 / 1.8 min
  (`studio_cuts_v_2s.txt`, `studio_cuts_v_3s.txt`). No content cuts in
  21.1: no logistics or off-topic talk; students' answers aren't on the recording (only his mic), so the waits
  after his questions are plain silences. The previous editor removed ~15-16%.
- **Calibration attempt failed (2026-10-25):** matching the published 20.3 against its raw by loudness
  envelopes found only 82-136 of ~1,570 windows (the published sound was denoised and re-levelled, which
  changes the envelope). Not pursued; the user's review of 21.1 sets the rule instead.

## Drafts and review pages (2026-10-25, the user away: "proceed and come up with titles and descriptions ...")

- **Studio pages** for all 25 pieces (`scripts/non_essential/vahagn_plan_queue.py`, 4 s, 360p previews; DECISIONS
  #37). The 11 recordings with mains hum (noise floor ~-65 dB: 23.1.b, 23.2, 23.3.a, 23.3.b, 24.4, 28.1.a-28.4) are
  analysed from a 150 Hz high-passed copy (`--highpass`, audio/hp150_source.wav): raw, the hum made 23.3.b 91%
  "silent" (45 cuts, 5.6 of 9.6 min); filtered 21 cuts, 1.9 min. Their previews keep the raw sound.
- **Content cuts:** only 23.1.a's aside on Germany around 1900 (04:13.5-05:02.1, unticked "your call");
  `content_cut_notes.md`. 21.1 reviewed by the user (19 cuts, `studio_cuts_to_enter.txt`); 21.2 reviewed 2026-10-25
  (16 planned -> 33: 17 short pauses added at prompts, fillers and transitions, 4 widened; 2.5 min, 27:41 -> 25:10;
  chapters remapped, valid). What the reviews show: `_learnings/2026-10-25-2050_vahagn-review-cuts-follow-speech-not-pause-length.md`.
- **Chapters** on the raw timeline in each `edited_predicted/timestamps_raw.txt` (one level of nesting, DECISIONS
  #36), drafted from the full transcripts, self-reviewed (missing hypotheses added), then **Codex-reviewed** (25 runs,
  ~25 min, read-only, everything inline): every finding checked against the transcript, verdicts and reasons in
  `codex_review.json` (reports also in each `edited_predicted/review_codex.md`). Titles changed on Codex's advice: 21.2,
  22.3, 23.3.b, 23.4, 24.2.b, 28.1.b, 28.2.b, 28.3.b.
- **Assembly:** `scripts/non_essential/vahagn_build_drafts.py` writes titles, the description (series template), the
  chapters mapped onto the current cut list, verifier + glossary results and the thumbnail; summary in
  `drafts_status.json`. Review page: `review_21-28.html` (`scripts/non_essential/vahagn_review_page.py`).
- **Assembly run 2026-10-25 19:00:** all 25 valid, 0 DENY, 0 NEAR. 8 ENG hits are `nullity(T)` in formulas (21.1,
  21.2) and the like: his book writes `rank(T) + nullity(T) = dim(V)` on screen while he says «դեֆեկտ», so formulas
  keep the book's notation (standard.md). 23.2 failed the 30 s gap after the remap (the 10.6 s pause at 12:39 shrank
  12:19 -> 12:49 to 20 s): the 25 s «φ = 181°» child was folded into the 10:53 one. 33 chapters moved from a pause
  to where speech resumes after the cut covering them (listed per piece on the review page). Predicted lengths with
  the 4 s plans: 25 pieces, 8.06 h raw -> 7.61 h (26.8 min of pauses cut; 21.1 with the user's 19 cuts). At the
  measured 3x realtime that is ~2.5 h of rendering.
- **Batch review (DECISIONS #44, 2026-10-25):** the 23 unreviewed pieces are reviewed one lecture day per page:
  `output/vahagn_b0504` (22.1-23.1.a), `b0506` (23.1.b-23.3.b), `b0511` (23.4-24.2.a), `b0513` (24.2.b-24.4), `b0518`
  (27.1-28.1.a), `b0520` (28.1.b, 28.3.a, 28.3.b, 28.4), `b0525` (28.2.a, 28.2.b). The download is
  `studio_cuts_edited_vahagn_<name>.txt`; `python scripts/non_essential/vahagn_batch_review.py split <name> --file <it>`
  does every step below for all the batch's pieces at once. Reviewed and split: b0504 (63 cuts -> 22.1 8, 22.2 18,
  22.3 18, 23.1.a 21; 5.1 min of 70) and b0506 (camera on: 70 of 75 planned cuts removed, 13 kept/added), b0511
  (camera on, all suggestions: 5 cuts taken -> 23.4 3, 24.1 2, 24.2.a 2; 0.5 min), b0513 (5 taken -> 24.2.b 2,
  24.3 3, 24.4 2; 0.4 min), b0518 (4 taken), b0520 (5 taken, incl. a 40 s cut over 28.3.a's camera-off stretch),
  b0525 (3 taken). **All 25 reviewed 2026-10-26:** 8.06 h raw -> 7.85 h (12.7 min cut). Final check (start/end
  padding, cuts with words inside, off-topic markers in the transcripts) in the session of 2026-10-26: one likely
  mistake (23.1.b's opening cut takes "Ուրեմն, ինչպես տեսանք, սեփական"), 7 ends left uncut, 3 off-topic candidates
  (23.1.a Germany aside, kept by the user; 23.3.a 9:49-9:59 lecture-or-practical exchange; 28.2.b 7:51-end film).
- **Noise that comes and goes (investigated 2026-10-26, the user: "some lectures have a static noise ... it comes only
  at some point"):** pause background per 10 s window in a 3-7.5 kHz band (scratchpad `static_probe.py`): 8-17 dB
  rises over the piece's usual pause level in 6-16% of the windows of the 11 hum pieces (23.1.b-23.3.b, 24.4,
  28.1.a-28.4) and 22.1 (8%); 0-1% in the other 13. In those stretches the pause background sits ~7 dB higher
  (relative to speech) than in the rest of the same video, and the light denoise (-8 to -10 dB everywhere) keeps the
  gap (28.4: -20.6 vs -28.1 dB; 23.3.a -22.2 vs -29.7). Not yet confirmed by ear that these are what the user hears.
- **Webcam (DECISIONS #45, 2026-10-26):** his camera box is on screen from 6 May (23.1.b) to the end; in the 15
  unreviewed pieces every cut is now an unticked suggestion, except in 28.3.a 18:09-18:37 (camera off). Each piece's
  stretches in its `camera_on.json`.
- **After the user's review of a piece on studio.html:** save the list as `studio_cuts_edited.txt`, run
  `cut_list.py check` / `to-enter`, rerun `vahagn_build_drafts.py <section>` (it picks up `studio_cuts_to_enter.txt`
  and remaps the chapters), then enter the cuts in Studio on the new upload of that piece (DECISIONS #38; the
  Playwright loop takes the `[n, start, end]` array `to-enter` prints).

## Published pieces: problems found 2026-10-24

- Դաս 16.2-գ dated "4 մայիս, 2020", Դաս 17.1-19.2 (9 videos) "27 ապրիլ, 2020": year 2020 in a 2021
  course, and 16.2-գ's 4 May falls after 17-20's 27 Apr. Part 6's files would settle it.
- Դաս 20.3: 27 Apr in the description, 29 Apr in the file.
- Դաս 21.2: private, title/date/chapters "Todo".
- Audit 2026-10-22: Դաս 11.1 has "26:08 Գծորեն անկախ մատրիցներ" twice; Դաս 11.2-բ 42:19 label needs "անկախ".
- Playlist order: newest first, 21.2 at the end (dry run 2026-10-20: 67 of 73 move).
