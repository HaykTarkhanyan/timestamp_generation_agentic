# LEARNINGS

Non-obvious lessons, gotchas, and decisions for this repo. Append, don't rewrite.

## Channel description templates differ per series

The user runs at least THREE distinct video series with different description templates. The skill (`SKILL.md`) currently only knows two. Future runs need to pick the right one from context, not blindly use the ML template.

### 1. Մաթեմատիկա ML-ի համար (math-for-ML)
Title: `Դաս NN | <topic> | Մաթեմատիկա ML-ի համար`

### 2. Մեքենայական ուսուցում (ML series, current)
Title: `[NN] <topic> | Մեքենայական ուսուցում`. Full template with Telegram link, materials URL, abstract, hashtags, `(Opus 4.8)` model attribution.

### 3. Կոմպլեքս անալիզ (Complex Analysis)
Title: `Դաս N | <topic1>։ <topic2> | Կոմպլեքս անալիզ` (no leading zero on N, Armenian semicolon between clauses).

Description template, baked-in lines NEVER change:
```
Ռոչեստրի համալսարանի պրոֆեսոր Սևակ Մկրտչյանի դասախոսությունը ASOF հիմնադրամի կողմից անցկացվող «Կոմպլեքս անալիզ» դասընթացի շրջանակներում։


🗓️ Ամսաթիվ՝ <DD month, YYYY>   (Armenian month names)


⏳Թեմաներ            (note: NO space after the hourglass emoji)
<timestamps>


👇 Բոլոր դասախոսությունները՝
https://www.youtube.com/playlist?list=PLz3NrXxHz_CBSe18p368oUfe8kZeP9pBS


🎶 Երաժշտությունները
1. Հոյ նազան - https://www.youtube.com/watch?v=wUTLWjED89I
2. Կաքավիկ - https://www.youtube.com/watch?v=N68VnEJcHAM
```

Differences from ML template:
- NO Telegram link block
- NO materials URL block
- NO abstract / Նկարագիր section
- NO hashtags
- NO `(Opus 4.8)` model attribution tags
- Has the lecturer attribution sentence (Sevak Mkrtchyan, Rochester / ASOF)
- Has fixed music credits footer
- Section separator is THREE newlines (`\n\n\n` = 2 blank lines), not 2

### Timestamp format for Complex Analysis series
- `MM:SS` with leading zero for chapters under 1hr: `00:00`, `56:09`
- `HH:MM:SS` for chapters past 1hr: `01:08:48`
- The series MIXES both formats within a single video when video crosses 1hr (e.g., `00:00 ... 56:09 ... 01:08:48`). The skill's "don't mix formats" rule does not apply here, since YouTube accepts both regardless.
- Verifier regex (`\d{1,2}`) accepts both `0:00` and `00:00` styles.

## Fetching YouTube descriptions/titles

`WebFetch` on youtube.com always redirects through `consent.youtube.com` from German IPs (consent flow). The HTML it returns has no actual video data. ALWAYS use yt-dlp's metadata extractor instead:

```python
import yt_dlp
with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
    info = ydl.extract_info(f'https://www.youtube.com/watch?v={vid}', download=False)
    # info['title'], info['description'], info['upload_date'], info['duration'], info['tags']
```

Same for playlists - use `extract_flat=True` to dump video list without downloading each.

Windows console / Git Bash will mangle Armenian/Greek/math glyphs when Python prints to stdout. Two fixes:
- `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` at the top, OR
- Redirect stdout to a file and read it back with `encoding='utf-8'` explicitly.

## Verifier `--audit-boundaries` output is two concatenated objects

`scripts/verify_timestamps.py --audit-boundaries` prints two distinct sections to stdout:
1. The structural-check JSON report (with `contexts`).
2. A `--- BOUNDARY AUDIT ---` plaintext section showing per-chapter ±10s windows.

`json.load()` chokes because section 2 is not JSON. To parse just the report: read the whole thing as text, find the closing brace of the first JSON object, slice. Or just `grep` the audit section for the timestamp you care about.

## Armenian auto-subs are useful but math-garbled

yt-dlp's `--write-auto-sub` returns Armenian transcripts that are good enough for topic detection but break on math notation. Common patterns:
- Per-word timing tags split mid-word: `p-value` becomes `pվ value` or similar.
- Named theorems are inconsistent: `Արցելա-Ասկոլի` may appear as `արզելաասկոլայինը` (one mashed word) or with random Latin letters mixed in.
- Latin technical terms are often code-switched in: `sin(πz)`, `exp(z)`, `cos`, etc. appear as-is.

Strategy for picking chapter labels: ignore the math fragments, latch onto the conversational Armenian transition phrases (`Հիմա անցնենք X-ին`, `Եկեք փորձենք`, `Ուրեմն`). The glossary at `.claude/skills/youtube-timestamps/assets/glossary.csv` covers ~1060 stats/ML terms but not analysis-specific named theorems (Weierstrass, Mittag-Leffler, Riemann, Harnack, Perron, Arzela-Ascoli) - those need manual transliteration to Armenian convention.

## Boundary precision rules (learned from review pass)

The skill's rule "land 0-3s AFTER a transition phrase, not before" is critical. Common mistakes when the speaker:
- Says "let's prove this" - put boundary at "let's prove", not at the lead-in summary 30s earlier
- States a theorem after preamble - put boundary at the NAMING of the theorem, not at "and there is a more general result"
- Asks an audience question and answers - that 30s Q&A interlude is NOT a chapter, but the topic shift after it IS

Self-review on Δας 22 caught 4 boundaries that were 10-45s too early. Always run `--audit-boundaries` after generating timestamps and read the context windows for each chapter to verify the transition phrase is actually inside the window.

## Existing draft timestamps may be LLM contamination

When a video's description already contains plausible-looking timestamps that "weren't there yesterday", check for tell-tale LLM artifacts. Found in Δας 21's existing description:
```
Կցանկանա՞ք, որ օգնեմ վիդեոյի համար գրել նաև կարճ նկարագրություն (description) կամ ընտրել համապատասխան YouTube թեգեր։
```
This is a follow-up question from an LLM chat session, accidentally pasted into the YouTube description. Treat the existing timestamps as LLM-drafted (probably unreviewed) rather than human-authored.

## Upload date is NOT a proxy for recording date

Δας 20, 21, 23, 25 in the Complex Analysis playlist were all uploaded as a single batch on 2026-03-18 with empty date placeholders (`, 2025`). Their actual recording dates are unknown and span late 2025. Δας 22 and 24 have real dates (`9 դեկ` and `16 դեկ` 2025). Lesson number reflects the COURSE order; upload order is unreliable.

Implication: when a published video has `🗓️ Ամսաթիվ՝ , YYYY` placeholder, ask the user or leave a `TODO: fill date` marker. Do not infer from upload_date.

## YouTube character filtering (math notation)

Already in `SKILL.md`, but worth re-stating: YouTube REJECTS descriptions containing ASCII `<` or `>` even between spaces as math operators. Use Unicode lookalikes:
- `>` (U+003E) -> `＞` (U+FF1E FULLWIDTH GREATER-THAN)
- `<` (U+003C) -> `＜` (U+FF1C FULLWIDTH LESS-THAN)

Other Unicode that works fine in titles + descriptions: arrows (`→` `↔`), subscripts (`z₀`), superscripts (`x²`), Greek letters (`π` `ρ` `θ` `γ`), Armenian semicolon (`։`).

## Parallel I/O fetches are safe; parallel compute is not

The CLAUDE.md heavy-compute warning is about CPU-pegging numerics (Monte Carlo, dense grid sweeps). It does NOT apply to I/O-bound fan-out like running 5-6 yt-dlp subtitle fetches in parallel via Bash `&`. Each yt-dlp call is a small HTTP request + a brief CPU pass. Six in parallel completed in ~30s on this machine without CPU spike.

Rule of thumb: parallel HTTP/disk/LLM API calls = safe. Parallel `numpy` / matplotlib rendering / sympy / numerical sims = ask first.

## Thumbnail design system + conventions live in `thumbnails/README.md`

Full spec for the ML lecture thumbnails (generated by `scripts/make_thumbnails_final.py`) is documented in [`thumbnails/README.md`](thumbnails/README.md). Key conventions, summarized:

- **Numbering**: thumbnails map 1:1 to lesson number. `ML01`–`ML03` = theory; `ML04`/`ML05` = the two practical sessions (continue the count, don't reuse `[04]`).
- **`Գործնական` badge**: practical/coding lessons get an orange pill, top-right, Armenian text in the title font. Driven by `"practical": True` in the lesson config; theory lessons must NOT have it. Earlier mistake: wrote it in Latin (`Gorcnakan`) — user wants Armenian (`Գործնական`).
- **Font gotcha**: Adamathuz (title font) is uppercase-Armenian only with NO Latin glyphs, so titles/badge must be pure Armenian; Latin terms (`sklearn`, `log`) go in panels. Use Sylfaen for mixed-case Armenian inside panels.
- **Illustration philosophy**: one bold **hero** chart (instant topic read, good when small) vs labelled 3-panel **concept board** (multi-topic, each panel self-contained). Vary across adjacent lessons so videos look distinct. Prefer redrawing the course's own figures (`figures/grad_desc_alpha`) and driving charts from real lesson data (`House_Rent_Dataset.csv`) baked in as constants.
- The script keeps unused illustration variants as named draw functions so swapping a thumbnail's art is a one-line `LESSONS` change.
- **Title auto-sizing**: single-line titles (the "not text-heavy" cases) auto-grow to fill the width (cap 74pt, never below the configured `title_size`), measured via matplotlib `get_window_extent` in `_fit_single_line_size()`. Multi-line titles keep their tuned size. If a short single-line title is already width-maxed and still looks small, wrap it to two lines and bump `title_size` (ML04 = `"Գծային ռեգրեսիան\nզրոյից"` at 78). Full spec in `thumbnails/README.md` (Title sizing).
- ML06 embeds two real course-slide plots as images (not redrawn): the degree-6 polynomial overfit demo and the k=5 fold CV grid, cropped from `ml_new/02_main_concepts_continued/L01d_validation_and_cv.pdf` (slide 2 figure `l01d_open_2_poly.pdf` + slide 24) into `thumbnails/assets/`. NOTE: the right deck for the [06] evaluation lecture is `02_main_concepts_continued`, NOT `01_regression__main_concepts` (which has a different degrees-1/3/9 plot).
