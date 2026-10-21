# Կոմպլեքս անալիզ uploads are already edited: no cut pass needed

The user asked whether Դաս 25 (`VppTi0mtRWI`) needed cuts and didn't remember editing it. It is already edited, and the series probably all is (it credits two pieces of music in every description).

**Evidence (Դաս 25, 2026-10-20)**
- **Ends:** continuous sound from 0:00 to the first word at 0:09 (intro music), and after "Այսքանով դասը ավարտենք" at 57:02 a 2 s gap, then 7 s of continuous sound to the end at 57:13 (outro). No pre-lecture chat, no goodbyes.
- **Length:** 3433 s, the same as the June fetch, so no Studio edit was saved since June.
- **Pauses are capped.** `find_edit_points.py` found 5 silences of 3 s or more, 0.3 min in total. Histogram of silent runs (20 ms frames, threshold floor + 20 dB), against the raw ML48 Zoom recording:

| Pause length | Դաս 25 (57 min) | ML48 raw (106 min) |
|---|---|---|
| 1.5-2.0 s | 112 | 55 |
| 2.0-2.5 s | 52 | 28 |
| 2.5-3.0 s | 12 | 13 |
| 3.0 s and up | 0 | 29 (longest 30.2 s) |

A board lecture with no pause over 2.8 s and a pile-up just below it is silence-trimmed footage; natural speech has the long tail ML48 shows.

**Consequence:** for this series, skip the lecture-edit-points stages and go straight to chapters on the live timeline. If one lesson ever shows long pauses or a chatty start, check it then. The only content-cut candidate left in Դաս 25 was a 10 s "Հարցեր կա՞ն" prompt at 19:58, which the user's ML rule would cut; on someone else's produced video it was left alone.
