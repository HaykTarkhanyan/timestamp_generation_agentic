# Decisions

Numbered, newest at the top. Superseded entries stay, marked as such.

## 2. Edit points for unedited recordings: audio silences + transcript content cuts, applied by hand in Studio

- **Decision:** `scripts/find_edit_points.py` proposes cuts from two sources -
  silence runs in the audio (2 s and longer, leaving 0.35 s of pause on each side)
  and content cuts I pick from the transcript (`content_cuts.json`: dead air,
  "any questions?" + silence, logistics, pre/post-lecture chat). It writes
  `edit_points.json` first, then a review page with a spectrogram and two clips per
  cut ("after the cut" and "what gets removed", boosted) and a cut list ordered
  last-first for the YouTube Studio editor.
- **Date / status:** 2026-10-03, active (first used on ML48).
- **Why:** The user edits in YouTube Studio's built-in editor, so the output has to
  be times typed into Studio's boxes, not an EDL or a rendered file. Last-first
  order keeps every remaining time valid whether or not Studio re-times the
  timeline after a cut. The ML48 audio is noise-gated (26% of 10 ms frames sit
  near -94 dB), so silence is unambiguous: silence-run counts barely moved
  between -80 and -60 dB (102-122 runs of 2 s or more). The silence threshold is
  the noise floor (5th percentile) + 20 dB.
  Captions alone give cut edges only to about 1-2 s, so content-cut edges get
  snapped outward to the speech edge in the audio; an edge that lands on speech
  raises instead of being moved silently.
- **Alternatives rejected:**
  - *Screen/frame checks on a low-res video copy* - the user said they won't help.
  - *Captions only* - mushy edges, and auto-captions miss quiet student speech
    entirely (ML48 0:00:30-0:00:45 has speech with no captions).
  - *Rendering the edit with ffmpeg* - the user uses Studio's editor.
  - *matplotlib spectrograms and MP3 clips* - ~2.5 s per cut here; numpy + PIL
    images and WAV clips are an order of magnitude faster per cut.
- **What would change this:** the user moving to a desktop editor (then export
  an EDL/markers instead); Studio limiting the number of cuts; recordings
  without a noise gate (then check the floor + 20 dB threshold against the
  run counts again); the 2-3 s silence cuts proving not worth typing (ML48:
  they are 44 of 68 edits but only 1.2 of 16.4 min removed).

## 1. Lecture corrections go out as a confirmed YouTube comment

- **Decision:** After a video is published, the pipeline reviews the lecture for
  the lecturer's own mistakes and posts them as one comment from the channel -
  but only after the user confirms that comment's content. The user pins it by hand.
- **Date / status:** 2026-10-01, active.
- **Why:** The user asked for it after the ML47 review found real slips (two
  reversed percentages at 0:28:38 and 0:31:34, a wrong claim about what the
  checkpoint holds at 1:21:20). A posted comment is public and the publisher has
  no delete, so a human gate before posting is the safety net.
- **Alternatives rejected:**
  - *Corrections in the description* - the description holds the abstract and
    chapters under a 5,000-char cap (ML46 already hit it), and viewers read
    comments for errata more than descriptions.
  - *Pinning via the API* - the YouTube Data API has no pin method
    (comments: list/insert/update/delete/setModerationStatus only).
  - *Posting automatically* - a wrong correction is worse than none, and only
    Studio can delete it.
  - *Including caption-ambiguous items* - auto-captions garble numbers, so
    "maybe ASR" findings stay out of the comment unless the user confirms
    they said it.
- **What would change this:** the API gaining a pin method (then pin on post);
  the user preferring corrections in the description or a card; or reviews
  that keep finding nothing (then drop the stage to save time).
