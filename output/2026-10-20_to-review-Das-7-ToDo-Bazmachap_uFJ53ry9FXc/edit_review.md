# Դաս 7 (uFJ53ry9FXc, 1:01:38): does it need editing?

**Verdict: no cuts needed, the YouTube version is already edited. One privacy spot to decide on
(mail tab titles, 0:31-2:41), which per DECISIONS.md #6 is a blur, not a cut.** Chapters in
`timestamps.txt` are on the current timeline.

## Evidence

- **Produced ends.** 0:00-0:06 channel intro, first words at 0:06 (a student's question).
  Outro from 1:01:30 to the end. The last sentence is cut short ("Լավ, այդ ապացույցը ես մանրամասն
  գրած ձեզ..." at 1:01:25, the verb is gone); harmless, but it is an abrupt ending.
- **Shorter than the raw file.** Raw `arnak-07.mp4` is 4055.3 s (67:35), YouTube 3698 s. Audio
  alignment (20 ms envelope cross-correlation, scores 0.98-1.00) shows the offset growing from
  +91 s at 0:07 to +310 s at 1:01:00, so pieces were removed throughout, e.g. 62.7 s at 0:31 and
  38.8 s at 2:41 (the screen-share switch to the iPad).
- **Pauses are capped.** Floor -88.55 dB, threshold -68.55 dB (`audio/silences.json`; the raw
  file's stats are in `audio/raw_arnak-07_silences.json`).

| Silent run | 0.5-1 | 1-1.5 | 1.5-2 | 2-2.5 | 2.5-3 | 3-4 | 4-6 | 6-10 | 10+ |
|---|---|---|---|---|---|---|---|---|---|
| YouTube | 369 | 114 | 43 | 13 | 10 | 6 | 2 | 0 | 0 |
| raw arnak-07 | 369 | 119 | 44 | 16 | 14 | 16 | 9 | 2 | 5 |

YouTube silences of 3 s or more (8, 28.4 s in total, longest 4.8 s): 6:37 (3.3 s), 15:56 (3.4 s),
17:11 (3.1 s), 24:45 (3.1 s), 31:29 (4.8 s), 39:52 (3.6 s), 50:52 (4.0 s), 54:40 (3.2 s).
The raw has 32 (195.6 s, longest 25.3 s).

## Content-cut candidates

| Start | End | What is said | Recommendation |
|---|---|---|---|
| 0:06 | 6:40 | A student asks why Σ̂ₙ is the covariance matrix of a discrete variable; the lecturer answers with a fair n-sided die | keep (student question, real content) |
| 2:34 | 2:42 | "let me switch, connect with the iPad" | keep (8 s, the raw switch was already cut) |
| 6:44 | 10:38 | "any questions on the regression chapter?", a student asks whether g or the h's are assumed linear; answer | keep |
| 10:40 | 12:16 | A student asks which book follows the course order; the lecturer: books are in the syllabus, the order is his own | keep (student question; logistics-flavoured but useful to viewers) |
| 12:18 | 13:25 | Lecture format: part of today's text is pre-written, so he will go faster; asks students to interrupt, mentions that viewers of the recording may have the same questions | keep (addresses viewers too); optional cut of ~67 s if a tighter start is wanted |
| 31:21 | 32:04 | "why squares? does anyone have an answer?", 4.8 s silence at 31:29, then a student answers | keep; at most trim the silence to ~1 s (~3.5 s saved, not worth a Studio cut) |
| 37:25 | 41:31 | A student asks how least squares differs from maximum likelihood | keep |
| 52:16 | 54:38 | A student asks why a sum of squares is convex | keep |

No Zoom or audio trouble remains.

If the optional 12:18-13:25 cut is made, every chapter from 13:28 on moves ~67 s earlier. Record
it in `studio_cuts_to_enter.txt` and remap with `scripts/map_transcript_to_edit.py`
(DECISIONS.md #10), or shift by the cut length.

## Privacy: mail tab titles are still in the YouTube version

- The raw recording shows the lecturer's browser (Google Drive PDF viewer, "YSU MV Stats 5.pdf"
  page 4) while he answers the opening question. Its tab strip shows two Outlook "Mail - ..." tabs
  and a Gmail "Spam - ..." tab whose title starts with his e-mail address; other tabs: a news site,
  course pages, "Lecture Slides". A Zoom self-view with his name sits top right.
- Mapped through the audio alignment, this browser view is on YouTube from **about 0:31 to 2:41**
  (raw 3:05-5:13; before 0:31 and after 2:41 the iPad notes are shown, checked on raw frames at
  1:40, 2:01, 3:06 and 6:00).
- **No mailbox content is visible.** A contact sheet of raw 3:04-5:14 every 10 s (14 frames) shows
  the same Drive PDF page in every frame; the mail tabs are never opened.
- Caveat: this assumes the edit kept the full frame. I could not look at YouTube's own frames, only
  at the raw file plus the audio mapping; one look at 0:31-2:41 in Studio settles it.
- Suggestion: blur the tab strip at the very top of the frame from 0:31 to 2:41 in Studio, or leave
  it, since only tab titles show. A cut would remove the answer to the opening question.
