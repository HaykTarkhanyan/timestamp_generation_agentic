# Tserunyan edits: the user keeps her math talk and cuts pauses from about 4 s

**Symptom.** On Դաս 16 the user turned the 70-cut plan (content cuts + silences of 5 s+, DECISIONS #26) into 121
cuts: 56 new, 6 changed, 5 removed (`output/2026-10-21_Das-16-*/studio_cuts_edited.txt`; 13.0 min removed against the
plan's 16.0, 1:42:35 -> 1:29:35). Դաս 15 went the same way: 87 pauses added to a 6-cut content-only plan.

**What they removed and kept (content cuts).**
- Unticked, all of them: her math and talk. Դաս 16: "thinking aloud about which way to draw the fiber" (107 s), "questions
  about this proof? ... hope it was clear, please ask" (35 s; only the two silences inside it were cut), two rounds of
  confusion with the room on orbit sizes (126 s, 101 s), "we're spending time on this for nothing" plus a group-theory
  aside (63 s). Դաս 15: her tangent about why attend lectures instead of reading books.
- Kept as cuts: the practical ones. Դաս 16: searching her colloquium slides and pasting the picture (42 s), fumbling
  with the drawing tool (16 s). Դաս 15: "Aram jan, help please", a time check while looking through her notes, a
  scheduling aside.
- Ends: Դաս 16's end cut now starts after "OK, I won't drag on; next class we'll finish this and finally move on to
  topology" (15.8 s later); the start cut also took "what did we do last time? OK," and a 4.4 s lead-in after it.

**Pauses.** Re-detecting the silences in memory with `find_edit_points`' own functions
(`scripts/archive/tserunyan_2026-10/user_pause_fit.py`, results in DECISIONS #40) and matching them to the user's list, the share of each length they cut:

| pause | Դաս 16 | Դաս 15 |
| --- | --- | --- |
| 5 s+ | 100% | 94% |
| 4-5 s | 80% | 81% |
| 3.5-4 s | 39% | 68% |
| 3-3.5 s | 32% | 35% |
| under 3 s | 8-13% | 32% |

studio.html marks every uncovered pause of 2 s+ in yellow, so the ones left in were seen and declined, not missed.

**Disproven: a hum join would catch the rest.** 13 added cuts on 16 (18 on 15) match no silence of 1 s+: stretches of
Zoom's digital silence (median 25 dB under the room's noise floor) broken by short sounds, fillers ("ըըը", "օքեյ",
"մի րոպե", "նայի"), clicks, garbled caption bits. Joining silence runs across sounds of 0.5-1.5 s, with no caption
word but fillers, matched fewer of the user's cuts at every setting (16, min 3 s: 42/56 without a join, 39 at 0.5 s,
25 at 1 s, 13 at 1.5 s), because the joins swallow real speech and then fail the word test. These are picked by ear.

**Consequences.**
- The re-plan of 17-27 (DECISIONS #40, the user's answers Q44-Q50): pauses from 4 s, math/talk content cuts as
  unticked suggestions, practical cuts and "any questions?" prompts ticked, ends after her next-time line.
- A next-time line often runs straight on from the chatter before it (Դաս 17: sound from 1:48:44.1 to 1:49:03.4 without
  a 0.1 s gap). find_edit_points refuses a content-cut edge on speech, so check `--speech-map` before splitting an end cut.
- This differs from the Metric Academy lessons (`2026-10-03-1548_edit-point-preferences-from-ml48-studio.md`), where
  the user cut thinking aloud in full: what gets cut is decided per lecturer, not once for all courses.

## Դաս 17 (2026-10-25, the first 4 s plan): fewer additions, two new nuances

105 planned cuts -> 124 (21 new, 12 changed, 2 removed), 1:49:34 -> 1:35:17; on Դաս 16 the user had added 56.
- **A thinking invitation keeps its wait.** Planned cut 0:49:58-0:50:18, "~20 s waiting for the students to find how to
  use generic ergodicity": the user cut only the silence before her "քիչ կսպասեմ, որովհետև հավես ա" ("I'll wait a bit,
  it's fun", 0:50:07) and kept the invitation and the ~10 s wait after it. Bare "any questions?" prompts stay cut (Q46).
- **Homework talk about the exercise just done stays.** Planned practical cut 1:35:56-1:36:07 ("I set that exercise
  especially for today... maybe I said it was optional, I don't remember") was removed; a 3.5 s pause before it was
  cut instead. One case so far; the other practical cuts of 17 (two household interruptions) were kept.
- **The ending:** the user ticked the suggestion holding her chatter and next-time line (1:48:44-1:49:04), so the whole
  ending went after all. 11 of the 12 changed cuts grew, their edges moved outward by 0.24-3.08 s (swallowing breaths
  and lead-ins); one (Cut 40) started 1.2 s later.
