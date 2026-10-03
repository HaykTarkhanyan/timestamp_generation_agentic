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
