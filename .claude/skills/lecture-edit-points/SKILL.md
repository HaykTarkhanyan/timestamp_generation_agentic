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
DECISIONS.md #2 and #3.

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
   "yes", fillers, a sentence trailing off) belong inside the cut.

**Keep:** student questions and their answers, content tangents, and course-plan announcements.

**Put every edge inside a pause.** Check each one with:

```bash
python scripts/find_edit_points.py --output-dir <output_dir> --speech-map 0:16:00 0:16:50
```

Each line is 10 s, one character per 0.1 s: `#` sound, `.` a click, `_` silence. Pick
an edge on `_`. The script then snaps it to the speech edge and keeps the pad. It
**raises** if an edge sits on speech; move the edge and rerun, never work around it.

## Stage 4: review pages

Open the Studio-numbered page for the user:

```bash
powershell -NoProfile -Command "Start-Process '<output_dir>\edit_review\studio.html'"
```

- **`studio.html`:**
  - Cut 1..N with Studio's exact `H:MM:SS:FF` times (the frame rate comes from yt-dlp and is kept in the JSON).
  - One player per cut over the full lecture WAV, with a bar to click or drag on the spectrogram.
  - A "skip the cut (hear the result)" toggle, and "play here" buttons on flagged sounds.
  - It reads `../audio/<id>_16k.wav`, so the audio folder has to stay where it is.
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
  New Cut below.
- **Numbering:** Studio sorts the list by start time and renumbers it Cut 1..N. Our
  `studio_cuts()` numbering matches.
- **"New Cut" greys out when the playhead sits inside an existing cut.** Move the
  playhead with the time box outside the panel.
- **Reading cuts back:** the timeline markers carry
  `aria-label="Start trim marker H:MM:SS:FF"` / `"End trim marker ..."`. The first pair
  is the whole-video trim box.
- **Verify by diffing every marker against the plan in a script, not by eye.** On ML48
  I left a cut out of a batch; only the full diff caught it.
- **Never press Save, and never navigate the Studio tab away** (it holds unsaved
  edits). Open anything else in a new tab. "Discard changes" drops everything.

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
