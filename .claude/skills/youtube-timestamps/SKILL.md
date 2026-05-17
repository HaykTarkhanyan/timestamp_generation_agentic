---
name: youtube-timestamps
description: Fetch YouTube subtitles via yt-dlp and propose chapter timestamps (YouTube-style chapters / table of contents) plus a short abstract for a given video URL. Use this whenever the user wants to generate timestamps, chapters, a table of contents, section markers, or a summary/abstract for a YouTube video, even if they only paste a URL without explicitly saying "timestamps". Handles auto-generated subtitles in any language (default Armenian / hy). Four explicit workflows: fetch subtitles, generate timestamps from the transcript, verify the proposed timestamps, write a short abstract.
---

# YouTube Timestamp Generator

Generate YouTube-style chapter timestamps and a short abstract for a video by fetching its (auto-generated) subtitles and reasoning about content structure. Built for Armenian (`hy`) by default, works for any language yt-dlp can pull.

The workflow is split into **four explicit stages**. Run them in order — do not try to do everything in one shot. Each stage's output is the next stage's input, and the user can inspect/edit between stages.

```
fetch  ->  generate  ->  verify  ->  abstract
(yt-dlp)   (LLM)         (script)    (LLM)
```

## Working directory

Create a per-video working directory and put all artifacts there. Pattern: `output/<video-id>/`. Keeps runs isolated and makes it easy to rerun a stage without losing prior work.

```
output/<video-id>/
├── <video-id>.hy.vtt      # raw subtitles from yt-dlp
├── transcript.txt         # cleaned, deduplicated transcript with timestamps
├── metadata.json          # id, title, duration, uploader, url
├── timestamps.txt         # proposed chapters (stage 2)
├── verify_report.json     # output of stage 3
├── abstract.txt           # short abstract (stage 4)
└── logs/fetch_subtitles.log
```

---

## Stage 1: Fetch subtitles

```bash
python .claude/skills/youtube-timestamps/scripts/fetch_subtitles.py \
    <youtube-url> \
    --output-dir output/<video-id> \
    --lang hy
```

If the user gives a URL without specifying a video id, parse it from the URL (`v=` parameter or short-link path) and use it as the output dir name.

### Private / unlisted / age-gated videos

If yt-dlp fails with `Private video. Sign in if you've been granted access`, rerun with `--cookies-from-browser`:

```bash
python .claude/skills/youtube-timestamps/scripts/fetch_subtitles.py \
    <youtube-url> --output-dir output/<id> --lang hy \
    --cookies-from-browser chrome
```

Use the browser the user is actually signed into YouTube with: `chrome`, `firefox`, `edge`, or `brave`. No file handling — it reads the live browser session.

### Language fallback

If `hy` auto-subs are not available, the script fails loudly (no `.vtt` produced). List available subs with `yt-dlp --list-subs <url>` and ask the user which to use.

### What it outputs (JSON on stdout)

- `vtt` — raw subtitle file path
- `transcript` — cleaned transcript path (this is what stage 2 reads)
- `metadata` — metadata JSON path
- `duration_seconds`, `title`, `transcript_lines` — convenience fields

### How the VTT cleaner works

YouTube auto-generated VTT uses a two-line scrolling window:

- "Real" cues contain per-word timing tags (`<00:00:01.000><c>word</c>`) and two text lines: the previous settled line on top, the new line being spoken on the bottom.
- Between them are 10-millisecond "placeholder" cues containing only the just-settled line, with no timing tags.

The cleaner keeps only cues that contain `<c>` tags (the real ones), takes the **last** text line of each (the new content), strips the timing tags, and de-duplicates consecutive identical lines. For non-auto manual subtitles (no `<c>` tags anywhere), it falls back to a simple prefix-dedup pass.

Result: one `MM:SS  text` (or `H:MM:SS  text` for >1hr videos) per settled segment.

---

## Stage 2: Generate timestamps

This stage is **your reasoning**, not a script. Read `transcript.txt` and `metadata.json`, then propose a YouTube-format chapter list.

### Output format

Write proposed chapters to `output/<video-id>/timestamps.txt`, one per line:

```
0:00 <Label>
2:34 <Label>
7:15 <Label>
```

Or for videos >1hr (use `H:MM:SS` for **every** chapter, including `0:00:00` — never mix formats):

```
0:00:00 <Label>
0:12:34 <Label>
1:07:15 <Label>
```

Use the same language as the transcript for labels. 2-7 words. Descriptive, not generic — "Intro" / "Outro" are OK only when nothing more specific fits.

### Cleaning ASR garbage in labels

Armenian auto-subs frequently produce mid-word script splices like `Pվ value հեcking` (p-value hacking with Latin/Armenian fragments mashed together) or `survivor բesին` (survivor bias). Do **not** copy these verbatim into labels. For each technical term that appears garbled:

1. Decide whether the term has a standard Armenian translation. **Check the bundled glossary first**: `.claude/skills/youtube-timestamps/assets/glossary.csv` is a curated English→Armenian math/stats translation table (~1060 entries). Grep case-insensitively and fuzzily — the file uses LaTeX-style markup for some entries (e.g. `$p$-value` rather than `p-value`):
   ```bash
   grep -i "p.value\|null hyp\|variance\|regression" .claude/skills/youtube-timestamps/assets/glossary.csv
   # $p$-value,$p$-արժեք,
   # null hypothesis,զրոյական վարկած,
   # variance,"դիսպերսիա, վարիացիա",
   # linear regression,գծային ռեգրեսիա,
   ```
2. If the glossary has it, use the Armenian translation in the label (strip any `$...$` LaTeX from the term you write — that's source markup, not the term itself).
3. If the glossary doesn't have it (e.g. `p-hacking`, `survivorship bias`, `Goodhart's law`), use the clean English term — that's how the lecturer code-switches anyway, and a clean English term is better than a garbled half-Armenian one.

The glossary covers most core math/stats vocabulary (`null hypothesis → զրոյական վարկած`, `variance → դիսպերսիա, վարիացիա`, `confidence interval → վստահության միջակայք`, etc.). Worth scanning before you commit to an English term.

### Rules YouTube enforces (the verifier will check these)

1. **First chapter must be `0:00`** (or `0:00:00` for >1hr videos). No exceptions.
2. **At least 3 chapters total**.
3. **Minimum 10 seconds between chapters**. In practice aim for 30s+ — anything closer feels noisy.
4. **Strictly increasing timestamps**.
5. **All timestamps within video duration** (read `duration_seconds` from metadata).

### How to pick chapter boundaries

Auto-generated subtitles have no punctuation and no paragraphs, so you have to infer structure from content. Look for:

- **Topic shifts**: the speaker pivots to a new subject. In Armenian, listen for cue phrases like "լավ գանք X-ին" ("OK let's get to X"), "հիմա մի հատ ուրիշ X" ("now another X"), "անցնենք X-ի թեմային" ("let's move to the X topic"), "վերջին էֆեկտը..." ("the last effect is...").
- **Question/answer boundaries** in interviews.
- **Lists or enumerated sections** ("first... second... third...").

The right boundary is the line where the speaker **names** the new topic, not the wrap-up line of the previous one. If unsure, prefer landing 0-3s after a transition phrase rather than before — viewers expect to hear the topic name when they click.

### How many chapters?

Depends on content density, not duration. Guidelines:

- **Talks with clear sections** (e.g. a tutorial with 4 phases): 4-8 chapters, matching the actual sections.
- **Enumerative content** (e.g. "50 statistical tricks", "10 tips for X"): scale up. Group related items into named clusters of 2-5 items each. A 90-minute lecture with 50 named items can legitimately need 15-20 chapters.
- **Conversational / no clear structure**: 5-10 chapters at roughly even spacing, marking the topics that actually came up.

There is no hard cap, but more than ~20 chapters in a single video is rare and usually means you should consolidate. The skill's verifier doesn't enforce a maximum — judgment call.

### Honesty about uncertainty

Auto-generated Armenian subs are noisy. If you can't make out the content of a section, say so to the user instead of inventing a confident-sounding label. It's better to flag "between 8:00 and 11:00 the subs are too garbled to summarize confidently" than to write a wrong label.

---

## Stage 3: Verify

```bash
python .claude/skills/youtube-timestamps/scripts/verify_timestamps.py \
    output/<video-id>/timestamps.txt \
    --metadata output/<video-id>/metadata.json \
    --transcript output/<video-id>/transcript.txt \
    --min-gap 30
```

### Structural checks (default)

- Every line parses as `M:SS Label` or `H:MM:SS Label`.
- First timestamp is exactly `0:00` (or `0:00:00`).
- Timestamps strictly increase.
- Gap between consecutive chapters >= `--min-gap` (default 30; YouTube's hard floor is 10).
- No timestamp past video duration.
- Per-chapter context: prints the nearest transcript lines (±15s) so you can spot a mismatched label.

Writes `verify_report.json` and prints it to stdout. Exit code 0 if valid, 1 otherwise.

### Boundary precision audit (optional)

Add `--audit-boundaries` to also get a ±10s window around each chapter, with each line marked `>>>` (at or after the boundary) or blank (before):

```bash
python .claude/skills/youtube-timestamps/scripts/verify_timestamps.py \
    output/<video-id>/timestamps.txt \
    --metadata output/<video-id>/metadata.json \
    --transcript output/<video-id>/transcript.txt \
    --audit-boundaries
```

Use this to confirm the topic transition actually happens **at** the chapter stamp, not 5-10s before or after. If you see the topic-naming sentence sitting in the "before" block, the boundary is late; tighten it.

### What to do on failure

If verification fails or a spot-check looks wrong, **go back to stage 2 and revise**. Don't silently "fix" timestamps without re-checking against the transcript — the whole point of separate stages is that each one is auditable.

---

## Stage 4: Abstract

Write a short abstract of the video to `output/<video-id>/abstract.txt`. Keep it tight (3-5 sentences). Tone should match the lecturer's register — for casual Armenian lectures, write casual Armenian ("Սովորում ենք, թե ոնց...") rather than stiff academic prose. The goal is: someone scanning the abstract should know whether to watch the video.

Cover:
1. What the video is (lesson number / series context, if any).
2. What gets taught or shown (key terms, named methods, main thread).
3. Optionally: 2-3 concrete examples the speaker uses, since these are usually what makes the abstract recognizable to people who've seen the video.

Same glossary rule as stage 2: when introducing an English technical term in the abstract, check `assets/glossary.csv` first. Prefer the Armenian form if one exists.

---

## Defaults and conventions

- **Language**: default `hy`. Override with `--lang` on fetch.
- **Min gap**: default 30s on verifier. Use `--min-gap 10` for denser chapters.
- **Auth**: `--cookies-from-browser <browser>` on fetch for private/unlisted videos.
- **Logging**: `logs/fetch_subtitles.log` inside the working dir, plus stderr.
- **Encoding**: everything UTF-8. Scripts force `sys.stdout.reconfigure(encoding="utf-8")` because Windows defaults to cp1252 which mangles non-Latin scripts.
- **Glossary**: `assets/glossary.csv` — ~1060 English→Armenian math/stats term mappings. Consult before deciding whether to use an English or Armenian technical term in labels/abstract.

## When you're done

Present to the user:
1. The proposed `timestamps.txt` content (as a code block, ready to paste into YouTube).
2. The abstract (also as a code block).
3. A 1-2 sentence note on how you chose chapter boundaries and which terms you translated via glossary vs. kept in English.
4. Any uncertainty flags from stage 2.
5. The verifier's `issues` list if non-empty.
