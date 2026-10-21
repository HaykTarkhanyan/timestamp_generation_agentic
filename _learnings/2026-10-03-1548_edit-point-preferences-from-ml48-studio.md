# Edit-point preferences, learned from the user's ML48 Studio adjustments

I entered 24 cuts in YouTube Studio for ML48 (3 s silence threshold plus my
content cuts). The user then moved cuts by hand and said they like the result.
They kept all 24 cuts and every one of my silence-only cuts. Every change made a
cut longer, in a few repeatable ways. Total removed: mine 15.2 min, theirs
17.1 min (+114 s); new length 1:28:47. The final list is in
`output/2026-10-03_48-cnn-operation-Meqenayakan-usucum_pWrFBaTtD9s/studio_final_cuts.json`.

**Rules for the content-cut stage (`content_cuts.json`):**

1. **Cut the prompt itself, not only the silence after it.** "Any questions?",
   "OK so far, people?", "think carefully, ask now if unclear" all go.
   - Cut 5 start -3.2 s and Cut 3 start -2.3 s.
   - Cut 2 start -8.5 s, which also took the "I'll send it in the chat" tail.
   - **If a student then asks, cut right up to the student's first word and keep the
     question.** Cut 7 grew from 8 s to 33 s (0:42:51.8 to 0:43:24.8): the
     prompt and its silences went, the question stayed.
2. **Thinking aloud while answering is cut in full**, up to where the clean
   explanation restarts: "wait, wait, let me think so I don't say something
   wrong", mumbling, half-sentences.
   - Cuts 10-13 became one 65 s stretch, 1:01:01.2 to 1:02:06.4.
   - My judgment cut there (1:01:28-1:01:51) was unticked by default. That was too
     timid: default these to cut.
3. **Swallow short non-content sounds at or between cut edges** instead of
   stopping the cut at them:
   - "but OK" (Cut 2 end +2 s) and "yes" (Cut 18 end +1.6 s);
   - the tail of a false restart (Cut 8 end +3 s);
   - a trailing-off sentence end, "...or post-" (Cut 17 start -4 s);
   - a 1.5 s filler between two silences (Cuts 19 and 20 joined).
   - Rule of thumb: a non-content sound under about 2 s next to a cut belongs inside the cut.
4. **Start on the first content sentence, end on the last one.**
   - Cut 1 end +4.5 s (to 0:08:21.2) dropped a lead-in before "we just finished neural nets".
   - Cut 24 start -9.8 s (to 1:42:59.6) dropped "oops" and "that's all I had planned for today".
   - The video now ends on the last explanation sentence.
5. **Unchanged:** all 9 cuts that were pure silence with no talk next to them
   (Cuts 4, 6, 9, 14, 15, 16, 21, 22, 23). The 0.35 s pause kept on each side and
   the 3 s minimum silence are right as they are.

**How this was measured:** I read the trim markers from the Studio editor page
(read only, before Save) and diffed them against my list frame by frame.
Positive d_end or negative d_start means the user cut more.

## ML49 (2026-10-04): same direction, plus pauses inside a demo

From 16 entered cuts to 17: +25.6 s removed, final length 1:10:07. File:
`output/2026-10-04_49-cnn-archit-Meqenayakan-usucum_OojZjVYzMiM/studio_final_cuts.json`.

- **Short sounds next to a cut get swallowed again (rule 3):**
  - Cut 2 and Cut 3 were joined into 0:14:27.7-0:14:46.8. That removed 4 s of uncaptioned
    speech between them and the "Դե" before the lecture starts.
  - Cut 13's end moved +2.6 s, to 1:22:20.2.
  - Cut 14 widened from 4.0 s to 12.0 s (1:23:53.7-1:24:05.7).
- **Pauses inside a live demo are cut too.** I had suggested keeping the two 3 s pauses in
  the snake demo, because viewers watch the screen there. The user added one cut over both,
  1:27:49.0-1:27:57.0. The screen activity doesn't save a pause.
- **A misread to avoid:** the user answered "lets keep the snake demo" to my suggestion to
  untick those pauses. I read it as "keep the demo uncut" and removed the cuts. They meant
  the opposite. Restate verbal changes as concrete cut times before rebuilding.

## ML50 (2026-10-14): edited on studio.html, same direction

From my 12 cuts to 15 (6 changed, 3 new), 0:36:47 -> 0:36:24 (+23 s removed). File:
`output/2026-10-14_50-transfer-ggradcam-Meqenayakan_yBi1pbk4j2M/studio_cuts_edited.txt`.

- **Fumbles start earlier than the captions show.** My "forgot the term" cut began at
  0:22:52; the user started it at 0:22:43, where the captions only had garble ("կարո ենք
  բանդուն", "վայ մոդունդ"), and split it to keep 0:23:05.6-0:23:10.3 (probably the term itself).
  Garbled captions right before a fumble are part of the fumble.
- **Thanks exchanges after a student question go** (new cut 0:19:12.7-0:19:15.9, "OK OK
  thanks" / "thank you"): rule 3 applies to the closing of an answer too.
- **A mumbled transition goes in full:** 0:37:41-0:38:10 ("we'll try fine-tuning on ResNet,
  the future models... we'll talk") became a new 3.7 s cut plus a cut widened from 6 s to 16 s.
- Three cut ends moved 0.04-0.9 s later: trailing bits get swallowed (rule 3 again).

## ML51 (2026-10-14): where the user kept more

From my 21 cuts to 23 (5 changed, 2 new). File:
`output/2026-10-14_51-vision-tasks-Meqenayakan-usucum_bPYSyraccrE/studio_cuts_edited.txt`.

- **A candid remark about the course stays; only the prompt goes.** My judgment cut
  1:35:07-1:35:56 ("honestly I'm a bit tired of these topics... I want us to get back to
  current topics, but if questions remain, welcome") became 1:35:43.6-1:35:56.5: the remark
  is kept, only "people" and the silence after it are cut.
- **The last content sentence is kept whole:** the outro cut moved from 1:42:14.7 to
  1:42:16.2, keeping all of "let me not dig into the term".
- **Two tiny new cuts (1.8-1.9 s)** mid-explanation, at 1:02:46.6 and 1:07:21.4.
- **The user cut the 1:23:22 mumble on their own** ("...uh, but yes, that's nothing"),
  while I was adding the same cut from the ML50 learning, a sign the rule is right.
- **Asked whether to add two thanks-exchange cuts at 1:40** (my reassurance to a student,
  "a very natural, pragmatic question", and the student's "thanks"), they declined - but only
  because they didn't want to check the list again: "i declined extra thanks just becuase didnt
  want to check again, that was a one time thing". The ML50 "thanks exchanges go" rule stands;
  put such cuts in the plan before the user reviews, not after. (I first wrote this down as a
  preference against the rule; that was a misread.)
- **Process lesson:** they reviewed the page I had built before adding three cuts (they
  hadn't reloaded), so the pasted list's "was" times matched the old plan. Check every
  pasted list against the plan it came from, and after a rebuild say plainly that an open
  tab is out of date.
- **End frame, both videos:** the page said 1:50:10:06, Studio's End trim marker was :07.
  Enter the last cut to Studio's marker (as on ML49).

## ML52 (2026-10-16): a practical - the on-screen fumbles stay

From my 48 Studio cuts to 41 entered (1:39:00 -> 1:16:26, 22.6 min removed; mine was 24.2).
The user's list had 49 cuts (20 changed, 1 new); 5 of them were shrunk to under 0.5 s and 3
pairs touched or overlapped by a frame. Files: `output/2026-10-16_52-Meqenayakan-usucum_q8JM6nR03-Q/`
`studio_cuts_edited.txt` (their paste) and `studio_cuts_to_enter.txt` (what went into Studio).

- **Kept, against rules 5 and 6:** hunting the folder for an example (16:19-16:45), the false
  start "I can show the capture process now... OK no" (only the pause before it was cut), "if
  I'm not mistaken... I won't check now" (54:51), the cosine/normalization aside (56:08), a
  forgotten class name (1:08:42), looking for frames in the data folder (1:26:56), and one plain
  2.7 s pause (15:29). In a practical the screen is the content: the viewer watches the notebook
  while the file or the word is being found. On practicals, default these cuts to unticked;
  on lectures, rule 5 stands (ML48, ML49).
- **Cut, as planned:** every "questions?" prompt with its silence, the whole pre-lecture block
  (including a 9-min off-topic Q&A about a student's job), an inaudible exchange (49:02), the
  end-of-class scheduling. The closing course-plan announcement stayed (it was unticked).
- **The end of the live demo stayed:** my cut started at 1:20:23 ("ah no, OK"); theirs at 1:20:41,
  "until you ask questions I'll just play".
- Six pause cuts got 1-2.5 s longer, and a new 2.4 s pause cut (rule 3 again).
- **Mechanics:** studio.html has no delete button, so the user shrinks a cut to nothing. Treat
  cuts under 0.5 s as dropped, merge cuts that overlap or leave at most one frame between them,
  and say both back before entering. Studio's End trim marker matched the list this time
  (1:38:59:15).

## Arnak Dalalyan, lesson 10 (2026-10-20): silent writing goes, questions and one-word narration stay

Another channel (Համալսարանական մաթեմատիկա), another lecturer, but the same reading of what a
viewer should not sit through. I had planned only start/end trims, assuming the long pauses were
fine because he writes on the iPad during them. The user, in Studio, cut 0:36-7:49 themselves and
explained: "he says something and then slowly writes it ... it just basically says nothing".

- **Cut:** every silence of 9 s or more while he writes (9.1-40.4 s, ten of them) and one of
  6.2 s; at 4:02 the 40 s pause, a 3 s pause and the "ըը" between them in one cut.
- **Kept:** 3.3-7.5 s pauses; a single word said while writing ("that can stay"); his remark
  that the first part was not recorded and last year's will be uploaded (0:11-0:31; only the
  "I thought I had pressed it" before it went); "let's end here, continue next week" (only the
  goodbyes went).
- **Edges:** within a frame or two of `find_edit_points.py`'s own (0.35 s pad).
- **Rule taken:** `--min-silence 8` for his raw recordings (DECISIONS #16). Student questions still
  stay, as before.

## Arnak Dalalyan, lesson 11 (2026-10-21): pauses from about 4 s go, and his "ommm"

The user reviewed the 8 s plan on studio.html and sent back 48 cuts (19 new, 2 widened), with:
"he often just says ommm thats why u may thing he said something".

- **Where they listened, they cut most pauses of 4 s and up:** inside the three stretches with new
  cuts, 93% of 4-6 s pauses, 57% of 3-4 s, 11% of 2-3 s, all 8 s+. Outside them, nothing new: an
  untouched stretch on a returned list means "not reviewed", not "keep". Measure inside the
  reviewed windows before reading a rule off a list.
- **The hums are not quieter than speech** (median -30 vs -25 dB), so the detector hears them as
  speech and splits one empty stretch into two cuts. The two widened cuts (+2.0 and +2.4 s at
  15:09 and 15:31) took a hum in.
- **Rule taken:** `--min-silence 4` plus a narrow join of two cuts across an un-worded sound under
  1.2 s (DECISIONS #17). The lesson 10 data (kept 3.3-7.5 s pauses) came from the first 8 minutes
  only.
