# Դաս 8 (mwdDFKOw2Vw, 42:46): does it need editing?

**Verdict: no. The YouTube version is already edited, including the extra piece the old
description note mentioned.** The captions fetched today are already on the edited timeline, so
the new chapters in `timestamps.txt` need no remap (the old note about shifted times is dropped).

## Evidence

- **Produced ends.** 0:00-0:06 channel intro, first words at 0:06. The last caption is at 42:36
  ("...in Python they are ready and can be used"), the outro follows from about 42:38.
- **Shorter than the raw file.** Raw `arnak-08.mp4` is 2778.6 s (46:19), YouTube 2565 s. Audio
  alignment: offset +20.5 s at 0:07 (pre-lecture removed), +193.3 s at 42:20; ~28 s of raw after
  the last kept word is gone too. The largest single removed piece (~81 s) sits at about 17:00-17:10
  of the YouTube timeline, inside the proof of theorem 1; most likely the "piece cut afterwards".
- **Captions match the current cut.** The three pauses of 3 s or more fall exactly in caption gaps
  (5:09-5:14, 9:55-10:02, 19:51-19:59), and the captions end at 42:36, right before the outro.
- **Pauses are capped.** Floor -87.33 dB, threshold -67.33 dB (`audio/silences.json`; raw stats in
  `audio/raw_arnak-08_silences.json`).

| Silent run | 0.5-1 | 1-1.5 | 1.5-2 | 2-2.5 | 2.5-3 | 3-4 | 4-6 | 6-10 | 10+ |
|---|---|---|---|---|---|---|---|---|---|
| YouTube | 264 | 51 | 11 | 8 | 1 | 2 | 1 | 0 | 0 |
| raw arnak-08 | 242 | 52 | 15 | 8 | 3 | 4 | 5 | 3 | 7 |

YouTube silences of 3 s or more (3, 11.1 s in total, longest 4.4 s): 5:11 (3.3 s),
9:57 (3.4 s), 19:54 (4.4 s). The raw has 19 (182.6 s, longest 37.0 s).

## Content-cut candidates

| Start | End | What is said | Recommendation |
|---|---|---|---|
| 06:12 | 06:58 | The slides were made by AI from his handwritten notes, may have small notation slips; he will send better slides after class | keep (explains the slide slips to viewers); optional cut of ~45 s |
| 10:02 | 11:04 | Anecdote: the AI translated "unbiased" as "անաչառ", which he likes | keep (content tangent) |
| 12:44 | 14:28 | "why do we need the estimator's distribution?", a student answers | keep |
| 23:19 | 24:37 | "who can justify this equality?", a student answers, he gives two more arguments | keep |
| 25:39 | 26:32 | A student asks again how the joint normality follows | keep |
| 33:06 | 33:12 | "questions about the theorems? ~15 minutes left" | keep (6 s) |
| 34:38 | 34:46 | Points out a typo on the slide (should be Xᵀy) | keep (a correction viewers need) |

If the optional 06:12-06:58 cut is made, every chapter from 07:01 on moves ~46 s earlier. Record it
in `studio_cuts_to_enter.txt` and remap with `scripts/map_transcript_to_edit.py` (DECISIONS.md
#10), or shift by the cut length.

## Privacy

Raw frames every 2.5 min (19 frames, 0:00:25-0:45:25) show full-screen Beamer slides with the
lecturer's Zoom thumbnail and the Zoom clock. Nothing private seen. The only screen fiddling in
the transcript is a 4 s "let me see if I can show this" at 05:20.
