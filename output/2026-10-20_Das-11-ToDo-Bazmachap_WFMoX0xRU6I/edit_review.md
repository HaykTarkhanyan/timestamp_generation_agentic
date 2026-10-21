# Lesson 11 (WFMoX0xRU6I): edit plan review

Raw upload 1:13:04 (4384 s). Audio from the local Zoom file
`MV Stats 11 video/GMT20260428-143134_Recording.m4a` (4383.5 s). Noise floor -93.8 dB,
threshold -73.8 dB, 37% of frames silent. 21 silences of 10 s or more (7.1 min raw) in a first
run at `--min-silence 10`; the final plan was run at `--min-silence 150`, so it holds only the
two content cuts below. Nothing has been entered in Studio or published.

## Planned cuts (raw timeline, Studio frames at 25 fps)

| Cut | Start | End | Length | Kind | Ticked | Reason |
|---|---|---|---|---|---|---|
| 1 | 0:00:00:00 | 0:02:34:20 | 154.80 s | safe | yes | Before the first content sentence. Zoom gallery with two students' name tiles, the lecturer's webcam, "let's wait a few minutes for the others", greetings, the iPad screen-share setup (notes on screen from about 0:02:26), then "OK, we can start the lesson". Edge: "դասը" ends at 2:34.4, "Հիշեցնեմ, որ նախորդ դասին..." starts at 2:35.1. |
| 2 | 1:11:48:10 | 1:13:03:13 (end) | 75.12 s | safe | yes | After the last content sentence ("...ոչ այդքան արդյունավետ չափման միավորով ենք", ends 1:11:48.1). Holds a 0.3 s sound at 1:11:49.6, "little time left, the graphical representation next time" (1:11:52.5-1:11:59), "any questions?", next meeting next Tuesday, a student asks about last lesson's missing recording and the lecturer explains, goodbyes. |

Removed: 229.92 s (3:50). New length: 1:09:14 (4154 s predicted).

No mid-lecture cuts: no screen-sharing failure, no "can you see my screen", no dead iPad, no
logistics between 0:02:35 and 1:11:48.

## Silences of 15 s or more that stay (all writing)

Checked with one frame near the start and one near the end of each; the notes change in every case.

| Raw time | Length | What is on screen |
|---|---|---|
| 0:18:12-0:18:31 | 18.2 s | Writes the line "where P_v is the projection matrix onto v" |
| 0:20:07-0:20:31 | 23.6 s | Writes the heading of part (b) of the theorem |
| 0:43:51-0:44:12 | 21.2 s | Writes "on the other hand, by Pythagoras' theorem" |
| 0:57:26-0:57:52 | 25.8 s | Opens a new note page and writes the "3 Empirical PCA" heading |
| 0:59:27-0:59:50 | 22.7 s | Writes the heading of the empirical PCA definition |
| 1:06:09-1:06:26 | 17.1 s | Writes the remark on variables of different nature |
| 1:06:47-1:07:16 | 29.3 s | Same remark, continues writing |
| 1:07:48-1:08:07 | 19.6 s | Same remark, finishes the paragraph (correlation matrix) |

The four silences before 0:02:30 (16.1, 18.2, 25.5 and 81.5 s) are inside cut 1. Silences of
10-15 s (0:14:57, 0:15:59, 0:35:23, 0:36:02, 0:43:26, 0:46:17, 0:49:07, 1:03:30, 1:06:29) stay
per the owner's rule; 0:35:23 is the new page plus the "Ապացույց" heading.

Also kept on purpose (owner's rules for this lecturer): the "questions?" prompts and their pauses
(0:07:18, 0:22:07, 0:30:27, 0:49:03), "մի վայրկյան" at 0:16:59 and the self-correction at 1:04:01.
"Ja." at 1:07:16 is the captioner's version of "Հա"; he goes on with the lecture.

## Privacy

- Screen: the iPad Notes app for the whole lecture. Frames about every 5 minutes, at every long
  silence and at both page changes (0:35:00-0:35:32, 0:56:50-0:57:35) show only the notes, the
  Notes "..." menu, the "Lignes et grilles" picker and the on-screen keyboard. No browser, mail,
  Telegram or file paths seen.
- Student names, inside cut 1 (removed): the Zoom gallery at 0:00:05 and 0:01:20 shows two
  students' full names.
- Student names, kept: while a student speaks, the floating Zoom tile at the bottom right shows a
  placeholder icon with the student's Zoom display name, readable at full resolution. Seen at raw
  0:13:28, 0:22:17 and 0:25:50 (edited 10:53, 19:42, 23:15). Student questions run at raw
  13:25-14:20, 22:15-24:06, 25:43-26:25, 27:34-27:46, 30:34-31:01, 52:23-54:00 (edited 10:50-11:45,
  19:40-21:31, 23:08-23:50, 24:59-25:11, 27:59-28:26, 49:48-51:25). Not seen in two frames during
  the last question (0:52:35, 0:53:35). Not verified frame by frame; the owner's call whether to blur.
- Harmless: Apple Notes' "Titre conseillé" (suggested title) at the top of a page, e.g. 0:35:00 and
  0:55:00. These are handwriting-recognition gibberish; one looks like an email address but is
  recognized handwriting, not a real address.

Edited time = raw time - 154.8 s for everything between the two cuts.

## Chapters

32 chapters on the predicted edited timeline (`edited_predicted/timestamps.txt`), MM:SS under one
hour and HH:MM:SS from 01:00:00. The verifier passes (`--min-gap 30 --audit-boundaries`, no
issues), and every boundary sits on or just after the sentence that names the topic.

## Uncertain

- Cut 2's start: I followed lesson 10, where "let's end here, continue next week" was cut. To keep
  "little time left, the graphical representation next time" as a closing line, move the start to
  1:12:00.0 (keeps about 11 s more).
- The student follow-up at raw 30:34-31:01 is too garbled to label. It stays inside the 24:10
  chapter; the next chapter starts at the calculation the lecturer gives in reply (28:35).
- The lecturer says "հիմնական բաղադրիչներ"; labels and titles use the glossary's "գլխավոր".
  "Ագահ մոտեցում" is my rendering of his "greedy approach" (glossary: greedy algorithm = ագահ ալգորիթմ).
- Times are predicted from the cut list. Check them against YouTube's regenerated captions after
  the cuts are saved in Studio.

## Revision 2 (2026-10-20 evening): silent writing is cut too (DECISIONS #16)

Plan now: 27 cuts (`studio_cuts.txt`), 9.5 min removed, 1:13:04 -> 1:03:36: the 2 content cuts plus every silence of 8 s or more (the 8 silences of 15 s+ that v1 kept as writing are now cut).
The v1 plan (content cuts only) is kept as `studio_cuts_v1_content_only.txt` and
`edited_predicted/timestamps_v1_content_only.txt`. Chapters were moved through the new cut list
(old edited time -> raw -> new edited time) and verified. Times on the edited timeline in the
sections above are v1 times; the raw times still hold.

## Revision 3 (agent review, 2026-10-20)

Plan now: **28 ticked cuts, 9:39 removed (578.9 s), 1:13:04 -> 1:03:25** (`studio_cuts.txt`;
the automatic 8 s plan was 27 cuts, 9:27). Checked: sorted, no overlaps, smallest gap between
cuts 4.1 s. Six more cuts are in `index.html` as unticked judgment cuts. Raw times below, as
snapped by `find_edit_points.py`.

Deviations from the automatic 8 s plan:

- **End cut starts later:** 1:11:48.4 -> 1:11:59.4. Keeps the closing sentence "Լավ, մեզ շատ քիչ
  ժամանակ մնաց, ... գրաֆիկական ներկայացման մասին ... մյուս անգամ խոսեմ" (1:11:52.7-1:11:59.1), as the
  owner kept lesson 10's "continue next week". "Any questions? If not, let's end here", next
  Tuesday, the recording question and goodbyes still go. Revision 1's "Uncertain" point is settled
  this way.
- **Cut 4 extended:** 0:15:58.96-0:16:12.84 -> 0:15:58.96-0:16:16.87 (+4.0 s). After the 14.6 s
  pause comes a 1.1 s sound at 16:13.2 that has no caption word and is strongly voiced (likely
  "ըը"/"մմ"), then a 2.9 s pause before "սա նույնն է". Same pattern as the owner's lesson 10 cut at
  4:02 (pause + "ըը" + 3 s pause). Listen to the sound.
- **New cut 0:16:50.40-0:17:09.26 (18.9 s), safe, ticked:** false restart while thinking.
  "...նա է, Բացի նրանից, որ" (abandoned), 7 s, "մի վայրկյան", 5.7 s, "հա ը", 1.7 s, then he restarts
  with "եկեք գրենք, հետո կբացատրեմ ուրեմն երկրորդը նա է...". Frames at 16:50 and 17:09 are the same
  (only "γ(1)" on the page), so nothing is written during it. Revision 1 kept "մի վայրկյան" under the
  old "pauses stay" rule.
- **Start unchanged** (0:00-2:34.8).
- **No merges between silence cuts:** no two 8 s cuts are separated by only a filler. The closest
  pairs (1:06:25 and 1:06:40, gaps 4.1 s and 7.0 s) hold real sentences.

Judgment cuts, unticked (tick them on `index.html` if wanted):

| Raw | Length | What |
|---|---|---|
| 0:07:16.08-0:07:28.72 | 12.6 s | "if there are questions, better ask now", 4.7 s, "OK, no questions, let's move on". End edge is a 0.1 s gap before "ուրեմն" |
| 0:37:19.80-0:37:30.47 | 10.7 s | 5.6 s pause + uncaptioned 0.9 s sound + 4.8 s pause while writing |
| 0:48:59.45-0:49:33.60 | 34.2 s | "are the explanations clear, any questions?", silence (already cut 9.6 s of it), "apparently no questions, or you'll get it reading at home" |
| 0:53:30.56-0:53:40.39 | 9.8 s | inside the student exchange: 7 s pause + uncaptioned 0.9 s voiced sound + 2.5 s before the answer |
| 1:03:59.52-1:04:09.42 | 9.9 s | "եկեք չէ, այսպենս լավ չի" and 7.6 s while he erases "(η̂1" (frames 1:04:01 and 1:04:09); the erase shows on screen, which is why it is not ticked |
| 1:04:56.69-1:05:06.62 | 9.9 s | 4.9 s pause + uncaptioned 0.6 s voiced sound + 5 s pause |

Left as they are: the "questions?" prompts at 0:22:07 and 0:30:27 (a student asks right after,
and student questions stay); 0:56:49 "we still have a little time, so on to part 3" (the section
transition); every pause under 8 s that is not part of the above.

How the uncaptioned sounds were judged: per-word times from the YouTube VTT show no word in them,
and a pitch check gives 73-89% voiced frames (real words here: 50-72%), so they are vocal sounds,
most likely fillers. The check can't tell a filler from a mumbled word, so listen before entering.

Chapters: remapped through the new list (`remap_chapters.py` from `timestamps_v1_content_only.txt`),
transcript mapped (`map_transcript_to_edit.py --cuts studio_cuts.txt`, 3805 s predicted). Verifier
(`--min-gap 30 --audit-boundaries`): valid, no issues, **32 chapters, smallest gap 42 s, none
dropped**. The chapter block in `edited_predicted/description.txt` matches `timestamps.txt`.

## Revision 4 (2026-10-21): the owner's own list

The owner reviewed studio.html and returned 48 cuts (`studio_cuts_edited.txt`; 27 unchanged, 2
widened, 19 new): `cut_list.py check` OK, `to-enter` wrote `studio_cuts_to_enter.txt` (48 cuts,
10.9 min, 1:13:04 -> 1:02:08). Chapters moved onto it and verified (32, smallest gap 42 s).
Their new cuts cluster in 14:45-20:35, 43:20-49:40 and 1:02-1:08. `proposed_additions_4s.txt` lists
24 pauses of 4 s+ that the list does not touch (18 outside those stretches, 6 inside them and
probably kept on purpose). Proposals only; the owner's list is unchanged.

## Revision 5 (2026-10-21): 48 + 22 = 70 cuts, one pass in Studio

Nothing had been entered in Studio (the 48-cut list came from studio.html; YouTube still 1:13:04),
so the extra cuts go in on the raw timeline together with the 48. The 18 proposals got their own
page (`../2026-10-21_Das-11-extra-18-raw-timeline_WFMoX0xRU6I/`); the owner returned 22 (15
unchanged, 3 widened, 4 new; `cut_list.py check` OK). None overlaps or touches the 48.
`studio_cuts_edited.txt` now holds all 70 (the 48 are in `studio_cuts_edited_v1_48.txt` and
`studio_cuts_to_enter_v1_48.txt`); `to-enter`: 70 cuts, 12.9 min, 1:13:04 -> 1:00:12, frame check OK.
Transcript mapped (3612.84 s predicted), chapters remapped (old ones in `edited_predicted/*_v2_48cuts.*`):
verifier valid, 32 chapters, smallest gap 38 s. Six chapter starts sat in a pause that is now cut
and moved to the cut's end, where the topic sentence starts.

Entered in Studio on 2026-10-21 by the batch files (`cut_list.py entry-js`, DECISIONS #18): dry run +
5 batches, ~10 min. Read back (`studio_final_cuts.json`), `cut_list.py diff`: Studio 70 cuts, list 70
cuts, identical frame for frame; whole video 0:00:00:00 - 1:13:03:13. Not saved (the owner saves).

## After Save (2026-10-21)

The owner saved with a few tiny edits of their own: YouTube 59:59 (3599 s) against 1:00:12.8
predicted. Matching the regenerated captions (`edited/`) to the predicted ones puts them at raw
0:44:32-0:44:45 (~8 s) and 0:47:24-0:48:07 (~6 s); the hum gaps at 21:50 and 37:25 stayed open.
Chapters moved by each topic sentence's caption offset (`edited/timestamps.txt`: 14 moved, -1 to
-14 s), verifier valid, all 32 boundaries 0-4 s before their sentence. `edited/description.txt`
pushed 02:15 and read back identical.
