# Studio cut entry: skip the start box, send fewer events, check the channel

**Symptom.** Entering Tserunyan Դաս 16's 120 cuts (2026-10-25) took about 55 min, and per cut it got slower all the
way: 7.9 s with 0-14 cuts already in Studio, 10.8 s (14-28), 14.5 s (28-42), 62 s for 3 re-entered cuts at 53-56,
then 15.9, 18.1, 32.3 and 30.8 s per cut for the later batches. A Cut click at 53 cuts timed out after 30 s, though
it had taken effect. The user: "pls think about how you can speed up this entering process, i think you have a
redundant step at least".

**What was measured (msPerCut, now returned by every batch).**
- The page was not throttled: visible, focused, ~30 frames/s when idle; nothing else heavy was running (Chrome
  ~37% of the machine, "system" ~13%). Studio itself answers every click and key press more slowly as cuts pile up:
  at ~100 cuts each action took 2-4 s, so a cut cost ~30 s whatever was typed (cut 99 alone: 37 s).
- **The start box was the redundant step.** New Cut already starts the cut at the playhead, which the loop has just
  set to the cut's start. The box's `value` is empty until typed into (so the first test, on `inputValue`, never
  matched: 14 of 14 retyped); its `aria-label` holds the time (" 1 hour 8 minutes 11 seconds 23 frames" on cut 85).
  Comparing the label skipped the start on all 35 later cuts of Դաս 16 and all 122 of Դաս 17, every one checked
  exactly in Studio's markers afterwards.
- **insertText instead of one keystroke per character**: one cut tested at ~100 cuts in (no gain there, the clicks
  dominate), then the whole of Դաս 17.

**Result on Դաս 17** (same 4 changes: no start, insertText with read-back and slow retype as fallback, polling
instead of fixed 700/800 ms sleeps, batches of 41 instead of 14):

| cuts already in | old loop, Դաս 16 | new loop, Դաս 17 |
| --- | --- | --- |
| 0-41 | 7.9-14.5 s per cut | 3.5 s per cut (145 s for 41) |
| 41-82 | 15.9-62 s | 6.6 s (271 s for 41) |
| 82-122 | 18-32 s | 17.1 s (683 s for 40) |

Դաս 17 in all: 122 cuts in 18.3 min of batches (3 calls), against ~55 min for Դաս 16's 120; diff identical frame for
frame, Save dialog 1:35:17 as predicted, saved 2026-10-26 ~00:22. The growth with the cuts already in Studio remains
(3.5 -> 6.6 -> 17.1 s per cut): that part is Studio's, not the loop's.

**Also learned that night.**
- **The Studio tab can be on the wrong channel and still open the video.** One Google login manages Metric, umath
  and Ուղեղամպրոպ; the umath video's editor opened under Metric ("You're a manager"), and the user spotted it. Check
  the account button before the dry run; switching reloads the tab and drops unsaved cuts (skill updated).
- **Headless would not help**: it removes the hidden-window stall (no window), but this slowdown is Studio's own
  work per event, the same headless; switching mid-video would also lose the unsaved cuts and the login.
