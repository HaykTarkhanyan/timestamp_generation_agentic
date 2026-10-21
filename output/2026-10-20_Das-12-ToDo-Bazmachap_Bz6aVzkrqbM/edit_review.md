# Lesson 12 (Bz6aVzkrqbM, 5 May 2026): edit plan

Plan only, nothing applied in Studio. Audio: the local Zoom file
`MV Stats 12 video/GMT20260505-143535_Recording.m4a` (4118.2 s, upload 4119 s).
Rules: the light rules for this lecturer (questions stay, pauses stay unless dead air).

## Planned cuts (3 ticked, removes 1:43, 1:08:38 -> 1:06:55)

| Studio cut | Raw | Kind | Reason |
|---|---|---|---|
| 1 | 0:00:00.0 - 0:00:11.4 | safe | dead air, then "I've pressed record, so we can start" |
| 2 | 0:41:31.4 - 0:42:35.9 | safe | switching the share from the iPad to the computer ("do you see it now?", ~27 s of silence), "how much time do we have left?" |
| 3 | 1:08:10.9 - end | safe | "if there are no questions, let's stop, see you next Tuesday", goodbyes |
| - | 0:08:01.2 - 0:08:16.8 | judgment, unticked | 17 s on a static page: he asked "what is this equal to?" and waits for the students |

## Silences of 15 s or more that stay (frames at start and end compared)

| Raw | Length | On screen |
|---|---|---|
| 0:21:08 | 15.2 s | writes the heading of section "բ)", the correlation circle |
| 0:23:52 | 17.3 s | writes the exercise and its explanation |
| 0:30:14 | 21.4 s | writes the theorem |
| 0:30:43 | 27.4 s | goes on writing the theorem |
| 0:36:13 | 18.2 s | writes the cos φ ≈ 1 case |
| 0:37:51 | 20.7 s | writes the cos φ ≈ -1 and 0 cases |

0:41:46 (27.4 s) is inside cut 2. 0:08:00 (16.9 s) is the unticked judgment cut.

## Kept on purpose

Every student question (about 18:05, 19:11, 38:56, 54:45, 56:51, 1:00:42, 1:04:21, 1:05:04). At
1:01:06 he says he joined from Beijing at midnight, as the reason for a slip a student caught: part
of an answer, kept.

## Privacy

Nothing private seen: iPad notes, then the R slides in a presentation window with no browser chrome (frames checked at raw 42:13, 47:00, 50:00, 1:02:00; the screen switch itself is inside cut 2). A student's first name is said at
raw 0:56:51 ("do you agree with ..."); it is not in any chapter or description.

## Chapters

37 chapters on the predicted edited timeline (`edited_predicted/timestamps.txt`, from
`map_transcript_to_edit.py --cuts studio_cuts.txt`). If the cuts change, rerun the mapper and shift
the chapters.

## Revision 2 (2026-10-20 evening): silent writing is cut too (DECISIONS #16)

Plan now: 19 cuts (`studio_cuts.txt`), 5.3 min removed, 1:08:38 -> 1:03:18: the 3 content cuts plus every silence of 8 s or more (the unticked 8:01 judgment cut is now a regular silence cut).
The v1 plan (content cuts only) is kept as `studio_cuts_v1_content_only.txt` and
`edited_predicted/timestamps_v1_content_only.txt`. Chapters were moved through the new cut list
(old edited time -> raw -> new edited time) and verified. Times on the edited timeline in the
sections above are v1 times; the raw times still hold.

## Revision 3 (agent review, 2026-10-20)

Plan now: **20 ticked cuts, 5:21 removed (321.2 s), 1:08:38 -> 1:03:17** (`studio_cuts.txt`;
the automatic 8 s plan was 19 cuts, 5:20). Checked: sorted, no overlaps, smallest gap between
cuts 2.1 s. One more cut is in `index.html` as an unticked judgment cut. Raw times below, as
snapped by `find_edit_points.py`.

Deviations from the automatic 8 s plan:

- **End cut starts later:** 1:08:10.9 -> 1:08:27.54. Keeps the closing sentence "Լավ, եկեք, եթե
  հարցեր չկա, մենք այսօր այստեղ կանգ առնենք, կհանդիպենք մյուս երեքշաբթի" (1:08:15.9-1:08:27.2), as
  the owner kept lesson 10's "let's end here, continue next week". It has two pauses inside (5.1 s
  and 4.6 s), both under 8 s. Only the thanks and goodbyes go. Shorter option if wanted: start the
  cut at 1:08:20.95, right after "կանգ առնենք," (drops the 4.6 s pause and "next Tuesday").
- **New cut 0:29:04.04-0:29:21.69 (17.6 s), safe, ticked:** tool fiddling while thinking aloud.
  "փորձենք, չնայած ես այստեղ երևի կարող եմ ... սիրուն շրջանակի ... ըհը այսպիսի" while he opens the
  tool palette (frame 29:13) and inserts a circle shape (frame 29:21; 29:04 shows only the axes).
  Keeps "...չափանի տարածությունում" before it and "ենթադրենք միավոր շրջանակի ենք գծում" after it.
  The circle appears at once in the edit.
- **Start and the screen-share cut unchanged** (0:00-0:11.4, 0:41:31.4-0:42:36.0).
- **No merges:** cuts 6/7 (gap 2.1 s) and 12/13 (gap 2.3 s) are separated by words he says while
  writing ("հետևյալ մեծությունը" at 14:41.3, "երրորդ փոփոխականը" at 28:38.6), so they stay apart.

Judgment cut, unticked:

| Raw | Length | What |
|---|---|---|
| 0:14:05.92-0:14:26.39 | 20.5 s | joins cuts 4 and 5 over a 4.2 s gap that holds two uncaptioned ~1 s sounds (14:14.3, 14:16.7) while he writes the definition. Tick it if they are fillers rather than words |

Checked and left as they are:

- 0:08:00.7-0:08:16.9 (an automatic silence cut): he asks "and what is this equal to?" and waits.
  The speech map is silent there, so no student speaks; he then says "yes, uh-huh, it equals
  zero, right", probably answering a chat message. Cutting the wait is fine; the question and his
  answer stay.
- 37:34.3: a 1.0 s sound between pauses of 5.2 s and 4.1 s. It is most likely the word "կորելացիա"
  that the captions miss ("...ունեն ուժեղ, բայց այստեղ կասենք բացասական [կորելացիա]"), so no cut.
- Every student question and the 1:01:06 "joined from Beijing at midnight" remark (part of an
  answer), as in Revision 1.

Chapters: remapped through the new list (`remap_chapters.py` from `timestamps_v1_content_only.txt`),
transcript mapped (`map_transcript_to_edit.py --cuts studio_cuts.txt`, 3797 s predicted). Verifier
(`--min-gap 30 --audit-boundaries`): valid, no issues, **37 chapters, smallest gap 32 s
(06:12 -> 06:44), none dropped**. The next smallest is 35 s (27:09 theorem -> 27:44 correlation as a
cosine; the two writing cuts at 30:14 and 30:43 fall between them). The chapter block in
`edited_predicted/description.txt` matches `timestamps.txt`.

## Revision 4 (2026-10-21): pauses from 4 s, hums joined (DECISIONS #17)

Plan now: 45 cuts (`studio_cuts.txt`), 7.3 min removed, 1:08:38 -> 1:01:19. One hum join at 0:37:33.9-0:37:35.8 (1.1 s sound between two cut pauses). 37 chapters, smallest gap 33 s.
The 8 s plan reviewed by the agent is kept as `studio_cuts_v3_8s_reviewed.txt`, its content cuts
before the hum joins as `content_cuts_v3_before_hum_rule.json`. All content cuts (start, end,
"any questions?" silences, screen switches, the agent's unticked judgment cuts) are unchanged.
Chapters moved again from the v1 chapters and verified.
