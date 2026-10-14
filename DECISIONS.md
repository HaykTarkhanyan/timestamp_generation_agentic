# Decisions

Numbered, newest at the top. Superseded entries stay, marked as such.

## 9. studio.html can play a 360p proxy of the recording, made on request

- **Decision:** `find_edit_points.py --video-preview` encodes the local recording to a
  640x360, 15 fps H.264 copy with a keyframe every 2 s and mono AAC
  (`<output_dir>/video/<id>_360p.mp4`, Quick Sync by default). studio.html plays it in
  a pinned panel instead of the WAV. It is opt-in, and reused once made.
- **Date / status:** 2026-10-12, active (the user picked "real video, synced" over a
  frame strip).
- **Why:**
  - Zoom's recording has a keyframe every ~26 s (mean of 11 gaps, max 31 s). Played
    directly, 8 seeks took 0.35-11 s (median ~2 s) and Play took 2.4 s to start.
  - On a proxy with 2 s keyframes, 8 seeks took 11-138 ms and Play started in 64 ms.
  - A 90 s clip encoded in 19 s with Quick Sync. The full encode is heavy (2-3x
    realtime measured with the CPU at 100% from other work), hence opt-in.
- **Alternatives rejected:**
  - *Play the Zoom file directly* - no encode, but seconds per seek.
  - *Frame strip + live frame* - cheaper, but the user wanted real video.
  - *Encode only the cut windows* - about half the length here (long cuts dominate) and
    a player that switches files per card.
- **What would change this:** Zoom recordings with frequent keyframes (then play the
  original), or the encode proving too slow to bother with.

## 8. Videos outside the ML series get their own thumbnail, rendered from HTML

- **Decision:** The Claude Code workshop thumbnail is an HTML page
  (`thumbnails/src/claude_code_thumb.py` builds it) screenshotted at 1280x720 with
  Playwright, not a `make_thumbnails_final.py` lesson. The locked ML design stays for
  the ML series.
- **Date / status:** 2026-10-12, active (the user: "come up with something new... u dont
  need to use the old templates").
- **Why:** The concept is text-led (a lyric card of Claude's rap verse, the Claude
  symbol, a falling mic). HTML gives text highlight bars, the workshop's own fonts
  (IBM Plex, Noto Sans Armenian, embedded as base64) and a colour emoji mic directly;
  the matplotlib template has none of that, and its title font has no lowercase Armenian.
- **Alternatives rejected:**
  - *The ML template* - the user asked for something new, and "ML NN" doesn't apply.
  - *PIL by hand* - text highlights, emoji and kerning would all be manual work.
- **What would change this:** more non-series videos (then make the HTML route a
  skill), or the user wanting them in the ML look after all.

## 7. The Claude Code workshop cuts silences of 4.5 s and longer; the default stays 3 s

- **Decision:** KdtXO7Pj9DI's edit points use `--min-silence 4.5`. The 3 s default in #3
  is unchanged.
- **Date / status:** 2026-10-11, active (the user's pick for this video).
- **Why:** At 3 s the plan was 68 Studio cuts. Counted from `edit_points.json` with the
  same 20 pre-ticked content cuts:

  | Minimum silence | Studio cuts | Edited video |
  |---|---|---|
  | 3 s | 68 | 1:40:52 |
  | 3.5 s | 55 | 1:41:24 |
  | 4 s | 47 | 1:41:48 |
  | 4.5 s | 42 | 1:42:06 |
  | 5 s | 38 | 1:42:22 |

  4.5 s drops 26 cuts to type for 74 s more video. Kept pauses stay at full length.
- **Alternatives rejected:**
  - *3 s (the default)* - 68 cuts.
  - *4 s (my recommendation)* - 5 more cuts for 18 s less video.
  - *5 s* - 4 fewer cuts than 4.5 s for 16 s more video.
- **What would change this:** the user picking a higher threshold on the next videos too
  (then raise the default in #3); the kept 3-4.5 s pauses sounding slow in the edited video.

## 6. Private things on screen are blurred by the user, not cut

- **Decision:** Edit points report private on-screen spots (raw and post-cut times, what
  is visible) and leave them in the video. No default cut covers them; the user blurs
  them in YouTube Studio.
- **Date / status:** 2026-10-11, active (the user's call, Claude Code workshop video).
- **Why:**
  - The user said: "im gonna blur that parts and not cut".
  - The spots sit inside demos: Telegram 0:26:14-0:26:26, the calendar week view
    0:35:07-0:35:13, the home address 1:17:45-1:18:38. Cutting them would cut the demo
    narration with them.
- **Alternatives rejected:** *cut each spot* - loses the demo explanation around it.
- **What would change this:** a spot too long or too spread out to blur, or Studio's
  Blur tool failing on it.

## 5. Edit-point audio comes from the local Zoom recording, checked against YouTube's length

- **Decision:** `find_edit_points.py --audio <file>` converts the recording the user
  uploaded (the Zoom download in `~/Downloads`), instead of downloading the audio from
  YouTube. It refuses a file whose length differs from the YouTube video's by more than 2 s.
- **Date / status:** 2026-10-04, active. YouTube download stays as the fallback when no
  `--audio` is given.
- **Why:**
  - The user asked for it. They download from Zoom and upload that exact file, so it is
    the same timeline. ML49: Zoom file 5391.16 s, YouTube 5391 s.
  - It is faster: 12 s to convert, against about 30 s of download plus about 45 s of
    conversion on ML48.
  - The length check catches picking the wrong file: ML48's recording was rejected for
    ML49, 6352.8 s against 5391 s.
- **Alternatives rejected:**
  - *Always download from YouTube* - slower, and unnecessary when the original is on disk.
  - *Auto-pick the newest Zoom file without a check* - one wrong pick puts every cut on
    the wrong audio.
- **What would change this:** the user editing the file before uploading (then the
  timelines differ and the length check fires), or recording somewhere other than Zoom.

## 4. Lecture corrections go in the description, above the chapters, with minutes instead of timestamps

- **Decision:** The confirmed corrections from the stage-6 review go in the video
  description, in a `⚠️ Ուղղումներ՝` block just above `⏳ Թեմաներ՝`. Each line starts
  with the minute in words, `N-րդ րոպեին - ...` (rounded to the nearest minute), never a
  `H:MM:SS` timestamp. A comment is posted only when the user asks for one.
- **Date / status:** 2026-10-03, active, revisited 2026-10-15. Supersedes #1 in part.
  - Revisited 2026-10-15 (ML50/ML51): each line now starts with a `- ` bullet,
    `- N-րդ րոպեին - ...`. The user asked for it "so its easier to read, also in future":
    the corrections are long, and without a marker they run together.
- **Why:** On ML48 the user looked for the corrections in the description, asked for
  them "before chapters", then asked for "at minute x" wording instead of timestamps.
  There is room for them: ML48 went from 2,586 to 3,139 characters out of 5,000.
  - Keeping timestamps out of that block also avoids any risk of YouTube reading them
    as chapters. With `H:MM:SS` lines above the list, ML48 still parsed 35/35 chapters,
    so the minute wording is the user's preference, not a measured necessity.
- **Alternatives rejected:**
  - *Comment only (#1)* - the user expected the corrections in the description.
  - *Clickable timestamps* - the user asked for minutes.
- **What would change this:**
  - a description near the 5,000 cap (then shorten the corrections or move them to a comment);
  - the user wanting clickable links again.

## 3. Edit points default to a 3 s minimum silence; Studio entry is by the user, Playwright only on request

- **Decision:** `find_edit_points.py` defaults to cutting silences of 3 s and
  longer (was 2 s). Cut lists are rounded inward to whole frames and numbered the way
  Studio numbers them. The user applies cuts in Studio themselves unless they ask for
  Playwright for that video, and Playwright never presses Save.
- **Date / status:** 2026-10-03, active. Revises the 2 s default in #2.
- **Why:**
  - **3 s:** on ML48, 2 s gave 68 edits for 16.4 min removed and 3 s gave 24 edits for
    15.2 min. The 44 extra edits bought 1.2 min, and the user picked 3 s.
  - **Frames and numbering:** Studio's time boxes are `H:MM:SS:FF` and its list is sorted
    by start time, so frame-exact times numbered like Studio let the user match the
    review page to Studio directly.
  - **Save stays with the user:** Studio edits can't be undone after Save. After I
    entered ML48's cuts, the user adjusted them by hand and asked that Studio not be
    changed through Playwright again.
- **Alternatives rejected:**
  - *Keep 2 s* - too many manual edits for little time.
  - *0.1 s rounding* - Studio counts frames, so 0.1 s times don't map exactly.
  - *Playwright by default, or pressing Save* - irreversible and outward-facing.
- **What would change this:**
  - the user preferring every pause tightened (lower the threshold);
  - a channel frame rate other than 25 fps (the frame rate is read per video already);
  - a Studio change that shifts the timeline during editing (then enter cuts last-first).

## 2. Edit points for unedited recordings: audio silences + transcript content cuts, applied by hand in Studio

- **Decision:** `scripts/find_edit_points.py` proposes cuts from two sources -
  silence runs in the audio (2 s and longer, leaving 0.35 s of pause on each side)
  and content cuts I pick from the transcript (`content_cuts.json`: dead air,
  "any questions?" + silence, logistics, pre/post-lecture chat). It writes
  `edit_points.json` first, then a review page with a spectrogram and two clips per
  cut ("after the cut" and "what gets removed", boosted) and a cut list ordered
  last-first for the YouTube Studio editor.
- **Date / status:** 2026-10-03, active (first used on ML48); revisited 2026-10-03, see #3 (default 3 s, frame-exact Studio list).
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
- **Date / status:** 2026-10-01; superseded in part by #4 on 2026-10-03 (corrections now go in the description; a comment only when asked).
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
