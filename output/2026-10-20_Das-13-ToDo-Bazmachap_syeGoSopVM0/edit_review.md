# Lesson 13 (syeGoSopVM0, 19 May 2026): edit plan

Plan only, nothing applied in Studio. Audio: the local Zoom file
`MV Stats 13 video/GMT20260519-144153_Recording.m4a` (3924.9 s, upload 3925 s).
Rules: the light rules for this lecturer (questions stay, pauses stay unless dead air).

## Planned cuts (3, removes 3:03, 1:05:25 -> 1:02:22)

| Studio cut | Raw | Kind | Reason |
|---|---|---|---|
| 1 | 0:00:00.0 - 0:00:04.5 | safe | dead air before "OK, now we can start" |
| 2 | 0:53:02.6 - 0:55:28.9 | safe | iPad battery died mid-proof: "sorry, my iPad's charge... give me a moment", ~2 min of camera view with no speech, then "can you see my other screen?" / "yes". The trailing "therefore" after "orthonormal basis" goes with the cut |
| 3 | 1:04:52.7 - end | safe | after the course wrap-up: a student asks about project requirements, "let me stop the recording" |

Kept on purpose:
- 0:02:49-0:03:57: "I use last year's notes; I listen to my recordings at 1.75x, you can too". About the format, useful to viewers.
- 0:30:11 "one minute, let me turn on..." (a few seconds).
- 1:04:20-1:04:52: "questions? ... we covered all the material I planned for this course". This is the last lecture, so the wrap-up stays.
- The 14 s silence at 1:05:10 is inside cut 3. No other silence is 10 s or longer.

## After cut 2 the screen changes

From raw 0:55:29 (edited 52:58) he shares Chrome with last year's notes (`YSU MV Stats 13.pdf` from
his Downloads) instead of the iPad. The description says the end of the proof uses last year's notes.

## Optional blur: browser tab strip, raw 0:55:29 - end (edited 52:58 - end)

Chrome's tab strip is visible the whole time: Gmail ("Boîte de réception..."), Outlook "Mail",
another "Mail", Google Drive, "YSU", and others, all truncated. No mailbox content and no addresses
were seen (9 frames from 0:55:30 to 1:04:50, he stays on the PDF tab). The address bar shows his
macOS user name in the PDF path. Same kind of strip as lesson 7, which was blurred.

## Chapters

30 chapters on the predicted edited timeline: `edited_predicted/timestamps.txt` (from
`map_transcript_to_edit.py --cuts studio_cuts.txt`). If the cuts change, rerun the mapper and shift
the chapters. Titles in `edited_predicted/titles.txt`, description in `edited_predicted/description.txt`
(PDF link is a TODO: the Drive folder has no lesson 13 PDF).

## Revision 2 (2026-10-20 evening): silent writing is cut too (DECISIONS #16)

Plan unchanged: 3 cuts, 3.1 min. Only 2 silences reach 8 s and both are inside the content cuts (he reads last year's notes and hardly pauses).
The v1 plan (content cuts only) is kept as `studio_cuts_v1_content_only.txt` and
`edited_predicted/timestamps_v1_content_only.txt`. Chapters were moved through the new cut list
(old edited time -> raw -> new edited time) and verified. Times on the edited timeline in the
sections above are v1 times; the raw times still hold.

## Revision 3 (agent review, 2026-10-20)

Final plan: **3 cuts, 3.05 min removed (183 s), 1:05:25 -> 1:02:22.** Same pre-ticked list as the
automatic 8 s plan, so the chapters did not move (30 chapters, verifier valid, no gap under 30 s).

Why nothing more is cut: only 2 silences reach 8 s and both are inside the content cuts. He reads
last year's notes instead of writing, so the longest other pauses are 7.5 s (1:04:12), 7.4 s
(0:28:16), 6.4 s (0:07:29), 5.7 s (0:43:33), 5.5 s (0:13:26), 5.3 s (0:27:32). All under 8 s, so
they stay, as in lesson 10. No two cuts sit close enough to merge.

Start and end: unchanged. The cut at the start stops before "OK, now we can start today's lesson,
the last one this year"; the cut at the end starts after "I think we covered enough material", so
the course wrap-up stays. The format remark at 0:02:49-0:03:57 (last year's notes, watch at 1.75x)
stays.

Added to `content_cuts.json` as `judgment` cuts, **unticked** (they show on `index.html` only, not
in `studio_cuts.txt`):

| Raw | Length | What | Why unticked |
|---|---|---|---|
| 0:28:16.1 - 0:28:27.9 | 11.8 s | 7.4 s pause, "sorry", 4 s pause | Neither pause reaches 8 s; tick it if the two pauses should go as one silent stretch |
| 0:30:06.8 - 0:30:15.5 | 8.7 s | false start ("if here K, if this rho"), "one minute, let me turn on...", 2 s pause; he restarts with "look, computing this rho..." | Short, and "turn on" may change something on screen |
| 1:04:12.7 - 1:04:30.7 | 18.0 s | 7.5 s pause, "OK? If there are questions, I still have time to stay and answer", 3 s pause | The wrap-up right after starts with "otherwise, we finished all the material...", which needs this sentence |

## Revision 4 (2026-10-21): pauses from 4 s, hums joined (DECISIONS #17)

Plan now: 14 cuts (`studio_cuts.txt`), 4.0 min removed, 1:05:25 -> 1:01:27. One hum join at 0:28:22.7-0:28:24.7 (1.1 s; this is the 'sorry' between the two pauses at 28:16, so listen). 30 chapters, smallest gap 50 s.
The 8 s plan reviewed by the agent is kept as `studio_cuts_v3_8s_reviewed.txt`, its content cuts
before the hum joins as `content_cuts_v3_before_hum_rule.json`. All content cuts (start, end,
"any questions?" silences, screen switches, the agent's unticked judgment cuts) are unchanged.
Chapters moved again from the v1 chapters and verified.
