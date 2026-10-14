---
name: lecture-edit-points
description: Find edit points in an UNEDITED lecture recording that is already on YouTube - dead air, "any questions?" followed by silence, logistics, thinking-aloud stretches, pre-lecture chat and the outro - review them by ear on a local page, and apply them in YouTube Studio's built-in Trim & cut editor. Use whenever the user says a video is unedited / raw, wants to "edit out", "cut", "trim" pointless parts or silences, asks for edit points or cut points, or wants the cuts entered in YouTube Studio (optionally via Playwright). Run it BEFORE the youtube-timestamps chapters for that video, since every cut shifts the times after it.
---

# Lecture edit points

The user records lectures live (online, noise-gated audio), uploads them unedited,
and edits them in **YouTube Studio's own editor** (not a desktop editor). This skill
turns a raw upload into a reviewed list of cuts, numbered and timed exactly like
Studio's Trim & cut list.

```
fetch captions -> silence pass (audio) -> content cuts (LLM) -> review pages -> apply in Studio -> read back -> chapters
```

**Read first:** `_learnings/2026-10-03-1548_edit-point-preferences-from-ml48-studio.md`
(what the user changed in my ML48 cuts - the rules below come from it) and
DECISIONS.md #2, #3 and #6.

## Stage 1: captions

```bash
python scripts/yt_publish.py recent 5          # the id, if the user didn't paste a link
python .claude/skills/youtube-timestamps/scripts/fetch_subtitles.py https://youtu.be/<ID> --lang hy
```

Unlisted videos work without cookies. Note the `output_dir` it prints.

**Captions take a while after upload.** ML49 had none 20 minutes after the upload
(`yt-dlp --list-subs <url>` says "has no automatic captions"). The silence pass doesn't
need them, so start it right away, and run a light background check (one
`--list-subs` every 5 minutes, exit when captions exist) that wakes you for Stage 3.

## Stage 2: silence pass

**Audio comes from the user's own recording, not from YouTube.** The user downloads the
Zoom cloud recording and uploads that file, so it sits in `C:\Users\hayk_\Downloads`
as `GMT<YYYYMMDD>-<HHMMSS>_Recording_<WxH>.mp4` (the newest one is usually the video).
Don't list or search Downloads recursively, it holds 1,000+ media files and `ls -lt` hung.
List only the newest top-level items:

```bash
powershell -NoProfile -Command 'Get-ChildItem -LiteralPath "C:\Users\hayk_\Downloads" -Filter "GMT*_Recording*" | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name, Length, LastWriteTime'
```

```bash
python scripts/find_edit_points.py --output-dir <output_dir> --audio "C:/Users/hayk_/Downloads/GMT..._Recording_1920x1080.mp4"
```

`--audio` converts the file to `audio/<id>_16k.wav` (ML49: 12 s, no download) and
**refuses it if its length differs from the YouTube video's by more than 2 s** (tested:
ML48's recording was rejected for ML49, 6352.8 s vs 5391 s). The source path is saved
next to the WAV (`audio/<id>_16k.source.txt`) and goes into `edit_points.json` as
`audio_source`. Passing a different `--audio` once the WAV exists raises; delete the
WAV to rebuild it. Without `--audio` the
script falls back to downloading the audio from YouTube (yt-dlp, ~80 MB for 1h45m,
a few minutes). It writes `edit_points.json` (the record, including `audio_source`),
`studio_cuts.txt` and the two review pages. The pages need `transcript.txt`, so before
the captions exist, use `--speech-map 0:00:00 0:00:10` just to convert the audio.

**Order of runs:** this first run is silence-only. It warns that `content_cuts.json` is
missing, which is expected. It also gives you the audio that `--speech-map` needs in
Stage 3. After writing `content_cuts.json`, rerun the same command (a fresh analysis,
not `--report-only`, which never rereads `content_cuts.json`) and rerun it after every
edit to that file.

- **Silence threshold:** noise floor (5th percentile) + 20 dB. Check the log line.
  ML48 was noise-gated: floor -94 dB, 26% of frames silent. Run counts barely moved
  between -80 and -60 dB, so the threshold was not sensitive. If a recording is not
  gated (floor above about -75 dB), check the run counts at a few thresholds before
  trusting it.
  - **The floor ignores exact digital silence** (all-zero samples, -120 dB), since 2026-10-14.
    ML50's 11-min break was pure digital silence, 10% of the frames, and dragged the floor to
    -120 dB: the threshold became -100 dB and only 2 pauses were found. Without it the floor was
    -94.1 dB and 61-62 pauses of 3 s+ came out at any threshold from -90 to -65 dB. The log line
    now says how much digital silence was excluded; if a run still finds almost no pauses,
    suspect the floor first.
- **Default minimum silence: 3 s** (the user's choice). Each cut leaves 0.35 s of pause on each side.
  At 2 s ML48 needed 68 edits for 16.4 min removed; at 3 s it was 24 edits for 15.2 min.
- **To cut shorter pauses too**, rerun with `--min-silence 2` (or any value). The analysis
  only looks at silences at least that long, so the page's minimum-silence menu can raise
  the threshold but never lower it below the value of the run.
- Clicks under 0.2 s count as silence. Louder ones become "short sound - listen" flags.

## Stage 3: content cuts (your judgment)

Read `transcript.txt` in full, then write `<output_dir>/content_cuts.json`:

```json
{"cuts": [
  {"start": "0:00:00.0", "end": "0:08:16.8", "kind": "safe", "default": true,
   "reason": "Dead air, then the pre-lecture chat"},
  {"start": "1:43:09.4", "end": "end", "kind": "safe", "default": true, "pad": 0.6,
   "reason": "Outro after the last content sentence"}
]}
```

`kind` is `safe` (dead air, logistics) or `judgment` (the user's call). `default` sets
whether the cut is pre-ticked. `"end": "end"` means up to the end of the video. Write
`reason` in English; the user reads it on the review page. After writing the file,
rerun the full Stage 2 command (see "Order of runs").

**What to cut** (from the user's own ML48 adjustments; when in doubt, cut more, they did):

1. **Start:** dead air, pre-lecture chat (homework feedback is `judgment`, recommend
   cutting it), remarks about attendance, opening slides or tabs. Up to the first content sentence.
2. **End:** everything after the last content sentence, including "that's all for
   today", scheduling the next class, feedback questions and goodbyes.
3. **"Questions?" / "OK so far, people?" prompts:** cut the phrase together with the
   silence after it. If a student does ask, end the cut right before the student's first word
   and keep the question and the answer.
4. **Logistics mid-lecture:** negotiating a break, "can you hear me", tech fiddling.
5. **Thinking aloud while answering** ("wait, let me think so I don't say something
   wrong", mumbling): cut it in full, up to where the clean explanation restarts. Pre-tick it.
6. **Self-interruptions and false restarts:** cut through the restart.
7. **Short non-content sounds (under about 2 s) at or between cut edges** ("but OK",
   "yes", fillers, a sentence trailing off) belong inside the cut. ML49 confirmed it again:
   the user joined two cuts over 4 s of chatter and widened a 4 s cut to 12 s.
8. **Pauses inside a live demo are cut too** (ML49: the user cut the pauses in the
   gesture-controlled snake demo that I had suggested keeping).

**Keep:** student questions and their answers, content tangents, and course-plan announcements.

**One recording uploaded as two videos** (ML50 + ML51, 2026-10-14): the user splits a long
session by uploading the same file twice and cutting each copy down to its part. Give each
video its own output dir and `content_cuts.json`, with the same `--audio`. Video 1's last cut
runs from its last content sentence to `"end"`, and video 2's first cut from `0:00:00` to its
first content sentence; the break between the parts is cut in both. Find the split in the
transcript (the "let's take a break, then the other part" line), and expect the plan for both
parts at the start of video 1.

**Put every edge inside a pause.** Check each one with:

```bash
python scripts/find_edit_points.py --output-dir <output_dir> --speech-map 0:16:00 0:16:50
```

Each line is 10 s, one character per 0.1 s: `#` sound, `.` a click, `_` silence. Pick
an edge on `_`. The script then snaps it to the speech edge and keeps the pad. It
**raises** if an edge sits on speech; move the edge and rerun, never work around it.

### Private things on screen: the user blurs them, don't cut them

The user's choice (2026-10-11, Claude Code workshop): they blur these themselves in Studio.

- **Find them in the transcript.** Listen for remarks like "I'll edit this out later",
  "this needs blurring", or "Claude, remind me". Also look for opened private apps
  (Telegram, the calendar, mail) and files with personal data (the global CLAUDE.md
  holds the home address).
- **Pin each one down roughly with frames from the local recording.** One fast-seek frame each, a few per spot on a contact sheet:
  `ffmpeg -v error -ss H:MM:SS -i <recording> -frames:v 1 -vf scale=640:-1 f.jpg`.
  - Within a second or two is enough; the user finds the exact frames in Studio.
  - Don't decode keyframes only to prove something never shows up: a static screen
    has one keyframe about every 30 s.
- **Report each spot** with three things:
  - what is visible;
  - its raw time;
  - its time after the default cuts (subtract every cut that ends before it).

  It is not known whether Studio's Blur tool shows the original or the trimmed timeline
  while cuts are unsaved, so give both.
- **Say a visible secret (password, key) plainly** and tell the user to change it. The
  raw upload is already on YouTube.
- **No default cut may cover a private spot.** A remark about the spot ("I'll delete this
  later") can be a `judgment` cut, off by default when it overlaps the spot.

## Stage 4: review pages

**When the user changes the list in words, restate it as concrete cuts before rebuilding.**
For example: "so I remove the cuts at 1:27:48 and 1:27:54, giving 16 cuts - right?". On ML49
"lets keep the snake demo" meant "keep those cuts", and I removed them. `studio.html` carries
a stamp (cut count, list ID, build time), so tell the user to reload an open tab after any rebuild.

Open the Studio-numbered page for the user:

```bash
powershell -NoProfile -Command "Start-Process '<output_dir>\edit_review\studio.html'"
```

- **`studio.html`:**
  - Cut 1..N with Studio's exact `H:MM:SS:FF` times (the frame rate comes from yt-dlp and is kept in the JSON).
  - One player per cut over the full lecture WAV, with a bar to click or drag on the spectrogram
    (20 s either side of the cut; Play starts 3 s before the cut and runs to the window's end -
    it used to stop 3 s after the cut, which the user took for a bug once the window grew; arrow keys move the bar).
  - Zoom: +/- buttons or Ctrl+wheel (1x to 64x), the spectrogram scrolls sideways and follows the
    bar while playing. Studio-page spectrograms are drawn at 80 px/s (max 16000 px) so zooming
    shows detail, not bigger pixels.
  - A "skip the cuts (hear the result)" toggle, and "play here" buttons on flagged sounds.
  - **The user can edit the list there** (added 2026-10-11 at their request):
    - Drag a cut's edge, or press Start = bar / End = bar.
    - "Add a cut at the bar" makes a new cut inside that window. Every Cut number on the page follows Studio's order.
    - Neighbouring cuts show in grey.
    - Edits stay in the browser's localStorage, keyed by the list ID.
    - A copyable list at the bottom marks cuts CHANGED (with the old times) or NEW. If the
      user pastes it back, those are the times to use. `--check-studio` compares Studio with
      `edit_points.json`, so cuts changed on the page show up there as differences.
  - It reads `../audio/<id>_16k.wav`, so the audio folder has to stay where it is.
  - **Video preview** (added 2026-10-12 at the user's request, opt-in): `--video-preview` makes
    `<output_dir>/video/<id>_360p.mp4` from the local recording, and studio.html then plays it
    in a panel that stays at the top while scrolling (with a Hide video button) instead of the WAV.
    Everything else on the page works the same. Made once; later runs reuse it automatically.
    - **Heavy: ask the user first and run it in the background.** Measured 2-3x realtime with the
      CPU at 100% from other work (up to ~1 h for a 2 h recording); a 90 s clip took 19 s.
      Quick Sync (`h264_qsv`) is the default; `--video-encoder x264` encodes on the CPU instead.
    - Why a proxy and not the Zoom file itself: Zoom puts a keyframe only every ~26 s, so seeks in
      the original took 0.35-11 s (median ~2 s). The proxy has one every 2 s: seeks took 11-138 ms.
    - It needs the local recording (`audio_source` in the JSON). If the audio came from YouTube,
      rerun the analysis with `--audio <recording>` first.
- **`index.html`:** every source cut with tick/untick and a minimum-silence menu. Its
  copyable list follows the ticks, in the same Studio numbering and frame times.
- **`studio_cuts.txt`:** the pre-ticked cuts, same numbering and frames, last first,
  for typing into Studio.

Tell the user how many edits there are and how many minutes they remove. If they're
thinking about a lower threshold, rerun at that value and compare the counts (ML48:
going from 3 s to 2 s added 44 edits to save another 1.2 min).

## Stage 5: apply in Studio

**Default: the user applies the cuts.** Only use Playwright when the user asks for it
**for this video**. Before touching Studio, get a yes on all of these:

- the exact list;
- they keep the original recording (Studio edits can't be undone after Save);
- they sign in themselves in the Playwright window (never handle their password);
- **you stop before Save.**

If the Playwright tools are missing, tell the user to run `/mcp`; don't work around it.

How Studio's editor behaves (measured on ML48, 2026-10-03):

- **Getting in:** `https://studio.youtube.com/video/<ID>/editor`, then the "Add trim"
  button (Trim & cut), then "New Cut".
- **Times:** the boxes take `H:MM:SS:FF` at the video's frame rate. ML48 was 25 fps;
  the script reads the rate per video. Studio keeps the **original timeline** while you
  edit, so the times in the list stay valid.
- **Typing a time:** `fill()` does not stick. Click the box, press Ctrl+A, type the time with
  `keyboard.type`, then press Tab. The editing row's boxes are `#panel-container input:visible`.
- **Order for each cut:**
  1. Move the playhead to the cut's start with the time box outside the panel.
  2. Press New Cut. A new cut starts at the playhead.
  3. Set the end, then the start.
  4. Confirm with the panel's "Cut" button.

  On ML48 the playhead was always before the target cut, so typing the end first was
  safe. What Studio does when a typed end lands before the cut's current start was not
  tested; starting at the cut's start avoids that case. It also avoids the greyed-out
  New Cut below. **ML49 used this order for all 16 cuts, ascending, with no problems.**
- **The playhead box's label says "1 hour" once the time is between 1 and 2 hours**
  (" 1 hour 3 minutes 19 seconds 14 frames"), not "hours". Select it with
  `input[aria-label*="hour"]:visible:not(#panel-container input)`, never `*="hours"`. On ML49
  `*="hours"` stopped finding the box after the first cut past 1:00:00.
- **The end trim's last frame comes from Studio.** Read the whole-video "End trim marker"
  and make sure the final cut ends exactly there. `studio_cuts()` now rounds the end
  trim to the nearest frame; ML49's list had said `1:29:51:03` against Studio's `:04`.
- **Numbering:** Studio sorts the list by start time and renumbers it Cut 1..N. Our
  `studio_cuts()` numbering matches.
- **"New Cut" greys out when the playhead sits inside an existing cut.** Move the
  playhead with the time box outside the panel.
- **Reading cuts back:** the timeline markers carry
  `aria-label="Start trim marker H:MM:SS:FF"` / `"End trim marker ..."`. The first pair
  is the whole-video trim box.
- **Verify with `--check-studio`, not by eye.** Save the markers with Playwright
  (`browser_evaluate` of the `[aria-label^="Start trim marker"], [aria-label^="End trim marker"]`
  labels, with `filename=.playwright-mcp/<name>.json`), then run:

  ```bash
  python scripts/find_edit_points.py --output-dir <output_dir> --check-studio .playwright-mcp/<name>.json
  ```

  It prints the counts in Studio, in the plan and on `studio.html` (all must match), plus the
  list ID. It lists every cut that is only in one place and exits 1 on any mismatch. Report
  the three counts and the list ID to the user. On ML48 I left a cut out of a batch, and only
  a full diff caught it.
- **Never press Save, and never navigate the Studio tab away** (it holds unsaved
  edits). Open anything else in a new tab. "Discard changes" drops everything.
- **Don't call `setViewportSize` on the user's Studio tab.** On ML51 it shrank the page the
  user was watching ("why did u minimize yt studio? it was full just now"). Inside the page the
  screen size is emulated too, so the real window size can't be read back. A later "restore"
  made it smaller still, and only a reload undoes it, which an unsaved tab can't have.
  `Emulation.clearDeviceMetricsOverride` from a new CDP session does nothing (it only clears its
  own session's override). What worked: read the real window with CDP `Browser.getWindowForTarget`
  (ML51: maximized, 2576x1456 bounds; `outerHeight` 1434) and `setViewportSize` to about the
  content area, 2554x1310 (window minus ~125 px of tab strip, address bar and automation bar).
  The entry routine has so far only run at 1500x950 (untested at the window's own size); try the
  window as it is first, and tell the user before resizing anything.

## Stage 6: read back and learn

After the user adjusts cuts by hand, **only read** the page.
1. Save the markers to `<output_dir>/studio_final_cuts.json`.
2. Diff them against `edit_points.json` `studio_cuts`.
3. Add any new pattern to the preferences learning.

Remind the user that nothing is saved until they press Save.

## After Save: chapters

Wait until YouTube finishes processing the edit, then run the youtube-timestamps
skill on the edited video.

**YouTube regenerates the auto-captions for the edited timeline** (verified on ML48:
the new length was 5327 s, as predicted from the cuts, and the captions started at the
first kept sentence). Still compare the fetched `duration_seconds` with the predicted
new length before trusting the transcript.

- Fetch into a subfolder, `--output-dir <output_dir>/edited`, so the raw-timeline
  `transcript.txt` and `metadata.json` that `find_edit_points.py` reads stay intact.
- If you already read the raw transcript for the content cuts, you can pick chapter
  boundaries on the raw timeline. Map each one through `studio_final_cuts.json`
  (subtract the length of every cut that ends before it; raise if it falls inside a
  cut), then check every boundary against the edited captions with the verifier's
  `--audit-boundaries`. On ML48 all 35 mapped boundaries landed on the right sentence;
  5 moved back 1-3 s to the line where the topic is named.

## Gotchas

- `python -c`, `curl` and `wget` are denied by `.claude/settings.json`. Write scratch
  `.py` files instead, and ask the user to run downloads with `!`.
- Playwright blocks `file://`. To test `studio.html` there, serve the output folder
  with `scripts/non_essential/range_server.py`, since plain `http.server` can't seek in the WAV.
- **Runtime:** varies a lot with machine load. A full run took 15 s to 3.5 min on ML48,
  `--speech-map` takes 10-25 s. Converting the Zoom file takes about 12 s; downloading from YouTube instead adds about 1 min.
- Don't delete `audio/`: the review page plays from it. It is gitignored, as is `edit_review/media/`.
