# Vahagn reviews: the user's extra cuts follow what is said, not how long the pause is

**Symptom**
On Vahagn 21.2 (studio.html, 4 s plan of 16 cuts) the user returned 33 cuts: 12 unchanged, 4 widened or moved,
17 new, 2.5 min removed instead of 1.6. The new cuts are pauses of 1.0-3.5 s, yet 48 other pauses of 2 s+ (6 of them
over 3 s: 12:20.1, 17:49.2, 20:52.1, 24:32.0, 25:19.3, 27:22.9) were left in.

**What the new and widened cuts have in common** (transcript at each, `scripts/archive/vahagn_2026-10/review_diff.py`)
- A prompt to the class cut together with the wait after it: "Հը՞" 7:15, "Ի՞նչ ստացվեց" 9:05, "ինչ եք կարծում" 3:08;
  cut 27 widened 2.9 s earlier to take in "ով է ուզում ասել". Same as the ML rule 3 in
  `2026-10-03-1548_edit-point-preferences-from-ml48-studio.md`.
- Two pauses joined across 0.3-1.2 s of filler ("ը ը", "այո էդ ըը"): cuts 3, 8, 13, 15, 19, 22 and the widened 28.
  Same as the ML rule 7 (short non-content sounds at cut edges belong inside the cut).
- Transitions: "Հաջորդ" at the very start (cuts 1-2: 0:00-0:02.3 and 0:03.2-0:04.2), "մինչև այս օրինակը ավարտենք"
  13:00, "տեսեք / հետևանք" 13:16.
- Cuts 16 and 29 had their start moved 0.76 s later (keeps the end of a word or a breath before the cut).

**Disproven: a lower pause threshold.** No minimum pause length reproduces the list (same frames and threshold as
find_edit_points):

| min pause | 21.2 pauses | cut by user | left | user cuts holding no such pause |
|---|---|---|---|---|
| 2.0 s | 79 | 31 | 48 | 5 |
| 3.0 s | 32 | 26 | 6 | 8 |
| 4.0 s | 16 | 16 | 0 | 17 |

21.1 (the user's first review, 19 cuts) goes the other way: at 3 s it would have needed 10 removals and 3 additions
against 4 additions at 4 s. Summed over both reviews, 4 s costs 21 actions and 3 s 27, so the 4 s plan stays
(DECISIONS #37).

**Disproven: he is writing on the screen during the pauses the user keeps.** Picture change per pause from the 360p
preview (5 fps, 160x90, pixels changing by 25+ levels): the kept pauses have a median of 0.00 of their frames
changing, the cut ones 0.08; 12:20.1, 24:32.0 and 25:19.3 (kept, 3.6-3.8 s) change 0 pixels, while cut pauses at
10:47 and 26:57 change 37k and 28k pixels (scrolling). The screen does not decide it.

**Consequences**
The pause rule cannot find these cuts; the transcript can. Prompt-plus-wait and filler-between-pauses spots are
findable in the captions, so they can be proposed as content cuts. The 6 kept pauses over 3 s have no explanation
yet (asked the user, Q90). Scripts: `scripts/archive/vahagn_2026-10/review_diff.py`, `pause_visual.py`.
