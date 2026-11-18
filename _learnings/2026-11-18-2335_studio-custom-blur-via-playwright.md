# Entering custom blurs in YouTube Studio with Playwright (LLM [06], 2026-11-18)

The user asked for the blurs to be entered so they only check and press Save. What worked, on the processed 37:12
video (`C4Zcf1K51FI`), in a Playwright window with the video preview at 462 x 260 CSS px:

- **Getting in:** editor -> "Add blur" -> "Custom blur" makes a blur at the playhead (default box in the middle,
  "Track object", ~7 min long). Further blurs: the button's accessible name is **"Add a blur region"** (a
  `getByRole('button', {name: /Blur/})` picked the wrong element once a blur existed).
- **"Fix blur position"** before resizing, so the box doesn't track.
- **Times:** the selected blur's start and end are the first two visible inputs (`MM:SS:FF` under an hour), the
  playhead the last. Click, Ctrl+A, `keyboard.type` with a 40 ms delay, Tab; the inputs' `aria-label` reads back
  ("2 minutes 34 seconds 13 frames"). Set the start before the end when the new start is earlier.
- **The box:** handles are `ytve-blur-editor-preview-overlay-item.selected .drag.{top,bottom,left,right,...}`. Every
  blur's handles stay in the DOM with a size, so pick the `.selected` item. **The top handle (and the box near the top)
  sits under the player's invisible `.action-overlay.ytcp-video-player-controls`**: drags there selected page text or
  resized the box wildly (one attempt blurred the whole frame; I deleted that blur). What worked: move the box by its
  middle, then drag bottom/left/right; for the top edge, add a temporary style
  `.action-overlay.ytcp-video-player-controls { pointer-events: none !important; }`, drag the top handle, remove the
  style. Mouse drags need `steps` (15-20).
- **Positions from the recording, not by eye:** gridded frames of the local recording gave the paragraph's band as a
  fraction of the height (51-75%, after a terminal scroll 31-64%); targets = `video.y + f * video.height`. Read the
  handles back as fractions after each drag.
- **Check by stepping the playhead** through each stretch and clipping the preview: that found the terminal scrolling
  ~2 s earlier than the 2 s frame sampling suggested (raw 1:20:30-1:20:33), fixed by starting the scrolled blur at
  3:51 so the two boxes overlap through the scroll.
- Save left to the user. After a blur Save Studio re-processes; the unblurred version plays until then, so the video
  joins a public playlist only after that processing.
