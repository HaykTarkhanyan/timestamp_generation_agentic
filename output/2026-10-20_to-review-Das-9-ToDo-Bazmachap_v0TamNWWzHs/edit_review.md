# Դաս 9 (v0TamNWWzHs, 1:06:16): does it need editing?

**Verdict: no. The YouTube version looks already edited.** Chapters in `timestamps.txt` are on
the current timeline. There is no local raw file for this lesson (`todo/` has arnak-04..08 only),
so the evidence is the audio alone.

## Evidence

- **Produced ends.** 0:00-0:06 channel intro (same level profile as Դաս 6-8), first words at 0:06
  ("Այսօրվա դասախոսության հիմնական նպատակը..."). The lecture closes properly at 1:06:05 ("we will
  continue next week with PCA"), then the outro to 1:06:15.
- **Pauses are capped below 4 s.** Floor -88.99 dB, threshold -68.99 dB (`audio/silences.json`).

| Silent run | 0.5-1 | 1-1.5 | 1.5-2 | 2-2.5 | 2.5-3 | 3-4 | 4-6 | 6-10 | 10+ |
|---|---|---|---|---|---|---|---|---|---|
| YouTube | 420 | 114 | 45 | 28 | 14 | 16 | 0 | 0 | 0 |
| raw arnak-07 (for comparison) | 369 | 119 | 44 | 16 | 14 | 16 | 9 | 2 | 5 |

Silences of 3 s or more (16, 54.1 s in total, longest 3.86 s): 15:12, 15:34, 16:20, 16:57, 20:49,
23:49, 25:36, 26:12, 34:25, 35:15, 35:53, 50:01, 51:32, 54:12, 55:23, 1:03:51 (all 3.0-3.9 s).
Zero runs of 4 s or more in 66 min, against 16 in the raw Դաս 7 (67 min): the long tail has been
trimmed.

## Content-cut candidates

| Start | End | What is said | Recommendation |
|---|---|---|---|
| 02:55 | 03:46 | Corrects a slip in the assumption he had written | keep (content) |
| 22:28 | 22:59 | A student asks what "the condition" is; he shows it | keep |
| 30:01 | 33:29 | A student asks whether the threshold should depend on the data; long answer on test statistics | keep |
| 46:28 | 46:46 | A student notes the missing squares on σ and σ̂; he thanks and fixes it | keep |
| 51:32 | 51:44 | 3.5 s silence, "questions on hypothesis testing? ... apparently none" | optional cut (~12 s, "any questions?" + silence); I would leave it on someone else's produced video |
| 51:52 | 52:10 | Counts aloud which chapter number comes next | keep (harmless, 18 s) |
| 1:03:38 | 1:04:28 | Asks which line to project on; a student answers | keep |

Small self-corrections while writing (02:13 "one second", 35:04 "σ should be below", 45:55) are a
few seconds each; keep.

If the optional 51:32-51:44 cut is made, every chapter from 51:48 on moves ~12 s earlier. Record it
in `studio_cuts_to_enter.txt` and remap with `scripts/map_transcript_to_edit.py` (DECISIONS.md
#10), or shift by the cut length.

## Privacy

No raw file to check frames. Nothing in the transcript points at mail, chats or screen-share
switching.
