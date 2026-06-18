---
name: youtube-timestamps
description: Fetch YouTube subtitles via yt-dlp and propose chapter timestamps (YouTube-style chapters / table of contents), a short abstract, hashtags, and a handful of title suggestions for a given video URL, then assemble the description + timestamps + hashtags into one paste-ready file. Use this whenever the user wants to generate timestamps, chapters, a table of contents, section markers, a summary/abstract, hashtags, or video title ideas for a YouTube video, even if they only paste a URL without explicitly saying "timestamps". Handles auto-generated subtitles in any language (default Armenian / hy). Five explicit workflows: fetch subtitles, generate timestamps from the transcript, verify the proposed timestamps, write an abstract, and assemble a combined YouTube description (abstract + timestamps + hashtags) alongside a small set of suggested video titles.
---

# YouTube Timestamp Generator

Generate YouTube-style chapter timestamps, a short abstract, and hashtags for a video by fetching its (auto-generated) subtitles and reasoning about content structure, then assemble everything into one paste-ready description. Built for Armenian (`hy`) by default, works for any language yt-dlp can pull.

The workflow is split into **five explicit stages**. Run them in order — do not try to do everything in one shot. Each stage's output is the next stage's input, and the user can inspect/edit between stages.

```
fetch  ->  generate  ->  verify  ->  abstract  ->  assemble
(yt-dlp)   (LLM)         (script)    (LLM)        (LLM: + hashtags -> description.txt)
```

## Working directory

The fetch script (stage 1) creates the per-video working directory itself and prints its path as `output_dir`. The folder name is `<YYYY-MM-DD>_<latin-slug>_<video-id>` (today's date + the title transliterated from Armenian to Latin and slugified + the video id), e.g. `output/2026-05-23_Das-50-Informaciayi-tesutyun_MxakqkjXtQY/`. Read `output_dir` from the stage-1 JSON and use it for every later stage — don't hardcode a path. Keeping the date + a readable slug in the name makes runs easy to find later; the id keeps them unique.

```
output/<YYYY-MM-DD>_<latin-slug>_<video-id>/
├── <video-id>.hy.vtt      # raw subtitles from yt-dlp
├── transcript.txt         # cleaned, deduplicated transcript with timestamps
├── metadata.json          # id, title, duration, uploader, url
├── timestamps.txt         # proposed chapters (stage 2) — verifier input, intermediate
├── verify_report.json     # output of stage 3
├── abstract.txt           # short abstract (stage 4) — intermediate
├── description.txt        # FINAL deliverable #1: abstract + timestamps + hashtags (stage 5)
├── titles.txt             # FINAL deliverable #2: 3-5 suggested YouTube titles (stage 5)
└── logs/fetch_subtitles.log
```

---

## Stage 1: Fetch subtitles

```bash
python .claude/skills/youtube-timestamps/scripts/fetch_subtitles.py \
    <youtube-url> \
    --lang hy
```

The script picks the output directory itself (`<output-base>/<date>_<slug>_<id>`, default base `output`) and prints it as `output_dir` in the JSON. Grab that path and reuse it for stages 2-5. To force an exact path, pass `--output-dir <path>`.

### Private / unlisted / age-gated videos

If yt-dlp fails with `Private video. Sign in if you've been granted access`, rerun with `--cookies-from-browser`:

```bash
python .claude/skills/youtube-timestamps/scripts/fetch_subtitles.py \
    <youtube-url> --lang hy \
    --cookies-from-browser chrome
```

Use the browser the user is actually signed into YouTube with: `chrome`, `firefox`, `edge`, or `brave`. No file handling — it reads the live browser session.

### Language fallback

If `hy` auto-subs are not available, the script fails loudly (no `.vtt` produced). List available subs with `yt-dlp --list-subs <url>` and ask the user which to use.

### What it outputs (JSON on stdout)

- `output_dir` — the auto-named working directory; reuse it for stages 2-5
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

Write proposed chapters to `<output-dir>/timestamps.txt`, one per line:

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
    <output-dir>/timestamps.txt \
    --metadata <output-dir>/metadata.json \
    --transcript <output-dir>/transcript.txt \
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
    <output-dir>/timestamps.txt \
    --metadata <output-dir>/metadata.json \
    --transcript <output-dir>/transcript.txt \
    --audit-boundaries
```

Use this to confirm the topic transition actually happens **at** the chapter stamp, not 5-10s before or after. If you see the topic-naming sentence sitting in the "before" block, the boundary is late; tighten it.

### What to do on failure

If verification fails or a spot-check looks wrong, **go back to stage 2 and revise**. Don't silently "fix" timestamps without re-checking against the transcript — the whole point of separate stages is that each one is auditable.

---

## Stage 4: Abstract

Write a short abstract of the video to `<output-dir>/abstract.txt`. Keep it tight (3-5 sentences). Tone should match the lecturer's register — for casual Armenian lectures, write casual Armenian ("Սովորում ենք, թե ոնց...") rather than stiff academic prose. The goal is: someone scanning the abstract should know whether to watch the video.

Cover:
1. What the video is (lesson number / series context, if any).
2. What gets taught or shown (key terms, named methods, main thread).
3. Optionally: 2-3 concrete examples the speaker uses, since these are usually what makes the abstract recognizable to people who've seen the video.

Same glossary rule as stage 2: when introducing an English technical term in the abstract, check `assets/glossary.csv` first. Prefer the Armenian form if one exists.

---

## Stage 5: Assemble combined description (+ hashtags)

This stage produces the **final deliverable**: one paste-ready `<output-dir>/description.txt`. It opens with the **chosen video title** on the very first line (so the user copies title + description from a single file — see below), then a divider, then the channel template that stacks the abstract, the timestamps, and a hashtag line — in that order, because that is the order a YouTube description wants them (summary up top, chapters in the middle so YouTube parses them into clickable chapters, hashtags at the very bottom).

### Generate hashtags

Pick **8-12 hashtags**, mixing Armenian and English (Armenian topic tags for the channel's audience plus the English technical terms people actually search). Rules that matter:

- Hashtags cannot contain spaces — concatenate multi-word terms (`#machinelearning`, `#ինֆորմացիայիտեսություն`), don't insert hyphens or spaces.
- Put the 3 most important first: YouTube surfaces only the first 3 above the video title.
- Derive them from the actual content (the named methods/topics from stage 2) plus the series/channel. Don't pad with generic junk like `#video` or `#youtube`.
- Same glossary spirit as stage 2: a clean English term beats a garbled half-translation, but prefer the Armenian form when it's the natural one for the audience.

### Assemble the file

ALWAYS use this exact layout for `description.txt` (the user's actual channel template). **YouTube rejects descriptions that contain ASCII `<` or `>` anywhere — even as math operators between spaces, not just as paired tags**. So before writing the file: scan the timestamps and abstract for any ASCII `<` or `>` and swap them for Unicode lookalikes that render identically (or near-identically) but use different code points YouTube doesn't filter:

- `>` (U+003E ASCII GREATER-THAN — **rejected**) → `＞` (U+FF1E FULLWIDTH GREATER-THAN — **accepted**)
- `<` (U+003C ASCII LESS-THAN — **rejected**) → `＜` (U+FF1C FULLWIDTH LESS-THAN — **accepted**)
- `≥` and `≤` (U+2265, U+2264) are already single Unicode glyphs — keep them as-is.

Concrete examples:
- `p > n`  →  `p ＞ n`
- `n < p`  →  `n ＜ p`
- `0 < ε < 1`  →  `0 ＜ ε ＜ 1`

Same rule applies to placeholders: use `TODO: …` instead of `<...>`. Never emit any ASCII `<` or `>` in the description.

```
🎬 Վերնագիր՝ The chosen video title goes here

──────────────────────────────

🔗 Դասընթացին միանալու հղումը՝
https://t.me/metric_academy

📚 Նյութը՝
TODO: paste materials URL here

⏳ Թեմաներ՝ (Opus 4.8)
0:00 First chapter label
2:34 Second chapter label
...

📌 Նկարագիր (Opus 4.8)
The stage-4 abstract goes here.

#Hashtag1 #Hashtag2 ...
```

**Fixed elements that NEVER change:**
- The **title header on top**: the first line is `🎬 Վերնագիր՝ <chosen title>`, followed by a blank line, a divider line (`──────────────────────────────`), and a blank line, then the rest of the template. The user wants this so they can copy ONE file and set both the YouTube title and description from it. Use the title the user picked from `titles.txt` (or, running unattended, your top recommendation from that file). Put the title verbatim — pure Armenian if that is what was chosen; the channel suffix (`| Մեքենայական ուսուցում`) is optional, add it only if the chosen title already includes it.
- The two emoji-header lines (`🔗 Դասընթացին միանալու հղումը՝` and `📚 Նյութը՝`) and the Telegram URL (`https://t.me/metric_academy`) are baked in. Always include them verbatim.
- The emoji headers above timestamps (`⏳ Թեմաներ՝`) and abstract (`📌 Նկարագիր`) are required.

**Per-lesson elements:**
- **Materials URL** — the GitHub Pages link to the lesson notes. The skill cannot guess this URL. Use the literal string `TODO: paste materials URL here` (NO angle brackets — YouTube strips them) so the user can spot it before posting. Example URL from the user's channel: `https://hayktarkhanyan.github.io/python_math_ml_course/ml_new/01_regression__main_concepts/01_linear_regression__concepts.html`.
- **Model attribution** — the LLM that generated each section, in parentheses. The user wants honest attribution per section because timestamps and abstract may be generated by different models / different runs. Default to `(Opus 4.8)` (current model). If the same model generated both sections, put the same tag on both; if different, write each section's actual generator.

The abstract often opens with a casual greeting in the lecturer's voice — e.g. `Դե, բարի գալուստ :^)` for an intro lesson. Keep that opening if you wrote one in stage 4.

Keep the `timestamps.txt` and `abstract.txt` intermediates on disk (the verifier reads `timestamps.txt`); `description.txt` is what the user pastes into YouTube.

### Title suggestions

Always also write **3-5 candidate YouTube titles** to `<output-dir>/titles.txt`, one per line. The title is a separate YouTube field (not part of the description), so it lives in its own file — never paste it into `description.txt`.

Why this is required: lecturers often upload with a placeholder title (`ToDo`, `Untitled`, etc.) and forget to rename. Surfacing a few options every time makes it trivial to pick one.

How to pick them:

- **Match the channel's existing template.** The user's two active series each have their own naming pattern:
  - **Մաթեմատիկա ML-ի համար** (math-for-ML series): `Դաս NN | <topic> | Մաթեմատիկա ML-ի համար`
  - **Մեքենայական ուսուցում** (ML series, newer): `[NN] <topic> | Մեքենայական ուսուցում`
  Look at the current title in `metadata.json` (and surrounding context — does the lesson talk about ML practice or math foundations?) to decide which template to use. Pattern consistency is what makes a suggestion feel like a real candidate rather than a generic rewrite. Keep the lesson number and series suffix; vary the middle `<topic>` segment.
- **Cover a few angles.** A literal/descriptive one (what topics are covered), a hook-oriented one (the most surprising or memorable thread, e.g. the Gaussian/CLT connection), and a search-friendly one with the recognizable English ML terms (KL, MLE, Mutual Information, etc.).
- **Stay under ~70 characters** in the visible portion. YouTube's hard limit is 100; longer titles get truncated in search results and on mobile.
- Same glossary rule as stage 2: prefer the Armenian form when one exists, but keep English for terms readers actually search for (KL, MLE, Cross Entropy, Mutual Information).

Example for ML 01 (Linear Regression intro) using the new ML-series template — this is what the user actually shipped:
`[01] Մեքենայական ուսուցման ներածություն. Գծային ռեգրեսիա | Մեքենայական ուսուցում`

If the existing title is already good (a real, content-describing title — not a placeholder), say so explicitly in the wrap-up; still write `titles.txt`, but flag that the current title is fine to keep.

---

## Defaults and conventions

- **Language**: default `hy`. Override with `--lang` on fetch.
- **Output dir**: auto-named `<output-base>/<date>_<latin-slug>_<id>` by the fetch script (default base `output`). Override the base with `--output-base`, or the whole path with `--output-dir`. The Armenian→Latin slug map lives in `scripts/fetch_subtitles.py` (`ARM_TO_LAT`).
- **Min gap**: default 30s on verifier. Use `--min-gap 10` for denser chapters.
- **Auth**: `--cookies-from-browser <browser>` on fetch for private/unlisted videos.
- **Logging**: `logs/fetch_subtitles.log` inside the working dir, plus stderr.
- **Encoding**: everything UTF-8. Scripts force `sys.stdout.reconfigure(encoding="utf-8")` because Windows defaults to cp1252 which mangles non-Latin scripts.
- **Glossary**: `assets/glossary.csv` — ~1060 English→Armenian math/stats term mappings. Consult before deciding whether to use an English or Armenian technical term in labels/abstract.

## When you're done

Present to the user:
1. The full `description.txt` content (as one code block, ready to paste into YouTube) — abstract, then timestamps, then hashtags.
2. The 3-5 `titles.txt` candidates (as a separate code block). If the existing video title is already a real, content-describing one, say so and recommend keeping it; otherwise highlight which of the suggestions you'd pick and why.
3. A 1-2 sentence note on how you chose chapter boundaries and which terms you translated via glossary vs. kept in English.
4. Any uncertainty flags from stage 2.
5. The verifier's `issues` list if non-empty.
