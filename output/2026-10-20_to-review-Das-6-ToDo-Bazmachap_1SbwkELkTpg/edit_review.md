# Դաս 6 (1SbwkELkTpg, 58:57): does it need editing?

**Verdict: no. The YouTube version is already edited.** Chapters in `timestamps.txt` are on the
current timeline and need no remap unless one of the optional cuts below is made.

## Evidence

- **Produced ends.** 0:00-0:06 is the channel intro (same level profile as Դաս 7-9; the intro clip
  `intro-attemt-2.mp4` is 6.46 s), speech starts at 0:06. Last word "Կտեսնենք" at 58:47, then
  continuous sound 58:50-58:57 (the 7.5 s outro clip). No pre-lecture chat, no goodbyes.
- **Shorter than the raw file.** Local raw `arnak-06.mp4` is 4018.3 s (66:58); YouTube is 3537 s
  (58:57), so about 8 min was removed even with intro and outro added.
- **Pauses are capped.** 20 ms RMS frames, floor (p5, digital zero ignored) -90.15 dB, threshold
  -70.15 dB. Raw numbers: `audio/silences.json`.

| Silent run | 0.5-1 | 1-1.5 | 1.5-2 | 2-2.5 | 2.5-3 | 3-4 | 4-6 | 6-10 | 10+ |
|---|---|---|---|---|---|---|---|---|---|
| count | 568 | 147 | 71 | 18 | 9 | 4 | 1 | 0 | 0 |

Silences of 3 s or more (5, 18.2 s in total, longest 4.0 s): 13:56 (3.7 s), 27:58 (4.0 s),
28:19 (3.4 s), 44:00 (3.5 s), 57:45 (3.6 s). Each falls in a caption gap inside a derivation
(the lecturer writing), none is dead air worth a cut. For comparison, the raw Դաս 7 / Դաս 8 recordings have 32 and 19 such pauses
(longest 25 s and 37 s).

## Content-cut candidates

| Start | End | What is said | Recommendation |
|---|---|---|---|
| 05:33 | 05:39 | "I think there should be no questions about the statement" | keep (no pause after it, leads straight into the proof) |
| 30:02 | 30:27 | "the proof is over, any questions?" then a student points out the missing factor n in the 4th/5th claim, the lecturer agrees | keep (student question with answer) |
| 32:03.5 | 32:15.3 | "Այս ը մեր դասախոսությունների..." (sentence dropped), "until I open the new file, if you have questions you can think and ask" | optional cut (~12 s of file switching), I would keep it: short and natural |

Nothing else qualifies: no Zoom or audio trouble, no logistics.

If the optional cut is made, every chapter after 32:03 moves 12 s earlier (32:15 becomes 32:03,
33:36 becomes 33:24, and so on). Record it in `studio_cuts_to_enter.txt` and remap with
`scripts/map_transcript_to_edit.py` (DECISIONS.md #10), or just shift by the cut length.

## Privacy

The video is the lecturer's iPad screen recording (raw is 1664x1920 portrait), so only the
iPad status bar is visible (date, battery). Nothing private was found.

## Date: not decided (`🗓️ Ամսաթիվ՝ TODO` left in description.txt)

This is most likely last year's recording:
- The iPad status bar reads "Mercredi 12 mars". 12 March is a Wednesday in 2025, a Thursday in 2026.
- New evidence: the raw file's container and stream `creation_time` is `2025-03-12T16:19:07Z`.
  The same field on the other raw files matches their known 2026 dates (arnak-04 2026-02-24,
  arnak-05 2026-03-10, arnak-07 2026-03-24, arnak-08 2026-04-07), so it is trustworthy here too.
- It fits the gap: Դաս 5 is 10 մարտ 2026 and Դաս 7 is 24 մարտ 2026, so this video fills the
  17 March 2026 Tuesday slot. Դաս 7 opens with a 2026 student asking about exactly what Դաս 6
  says at 01:26-01:40 (Σ̂ₙ as the covariance of a discrete variable), so the 2026 class had this
  material.

Options for the date line: `12 մարտ, 2025` (when it was recorded) or `17 մարտ, 2026` (the slot it
fills in the 2026 course). The user's call.
