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
