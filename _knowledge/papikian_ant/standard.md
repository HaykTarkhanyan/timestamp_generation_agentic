# Հանրահաշիվ և թվերի տեսություն (Papikian): the series standard

Read off the existing Դաս 13, 14 and 15 (`Xws84WaDw04`, `cHCKLOSxctg`, `hWpA9f5fmUg`) on
2026-10-21, to process lectures 16, 17, 19-23 the same way. It differs from the ML channel: no
abstract, no hashtags, no model tags, no Telegram line, no `final/ML<NN>.txt`.

## Title

`Դաս N | <topic>[։ <topic 2>] | Հանրահաշիվ և թվերի տեսություն` - no leading zero, two topics
joined by the Armenian full stop `։` (U+0589). Examples:

- `Դաս 13 | PID-ի վրա վերջավոր ծնված մոդուլների կառուցվածքը | Հանրահաշիվ և թվերի տեսություն`
- `Դաս 14 | Գծային օպերատորներ։ Ժորդանյան նորմալ տեսք | Հանրահաշիվ և թվերի տեսություն`
- `Դաս 15 | Դրինֆելդի մոդուլներ | Հանրահաշիվ և թվերի տեսություն`

N is the course's lecture number. The course page has no lecture 11 or 18 at all (no notes, no
recording; 11's week lists the midterm solutions, 18 would be Fri 22 Nov 2024). The missing number
goes into the next lecture's label, in the title and the thumbnail alike: lecture 12 is
"Դաս 11-12" (public, `khvL7pQif3c`, thumbnail "ԴԱՍ 11-12"), so lecture 19 is **"Դաս 18-19"**
(DECISIONS #24) and 20-23 keep their numbers. No note about the gap in the description.

## Description (exact layout; two blank lines between blocks)

```
Փենսիլվանիայի նահանգային համալսարանի պրոֆեսոր Միհրան Պապիկյանի դասախոսությունը ASOF հիմնադրամի կողմից անցկացվող «Հանրահաշիվ և թվերի տեսություն» դասընթացի շրջանակներում։

🗓️ Ամսաթիվ՝ 15 նոյեմբեր, 2024


📚 Դասախոսության ֆայլը՝
https://sites.google.com/view/mpapikian/teaching/algebra-and-number-theory#h.gej4b75dpiyv
Տնային աշխատանք՝
https://drive.google.com/file/d/1uKmNo0ZS8Wvz-s3tPHG16SQ9LuWmV6bA
Դասագրքեր և այլ նյութեր՝
https://mathteam.notion.site/algebra


⏳Թեմաներ
00:00 ...
01:01:12 ...


👇 Բոլոր դասախոսությունները՝
https://www.youtube.com/playlist?list=PLz3NrXxHz_CDF0l5rTCoxEqYoG3_na6Cs


🎶 Երաժշտությունները
1. Հոյ նազան - https://www.youtube.com/watch?v=wUTLWjED89I
2. Կաքավիկ - https://www.youtube.com/watch?v=N68VnEJcHAM
```

- One blank line between the lecturer line and the date (as on Դաս 13-15), two everywhere else.
- `⏳Թեմաներ` has no space after the emoji and no colon.
- Date line per lecture (Kaltura recording dates): 16 = `15 նոյեմբեր, 2024`, 17 = `19 նոյեմբեր, 2024`,
  19 = `26 նոյեմբեր, 2024`, 20 = `3 դեկտեմբեր, 2024`, 21 = `6 դեկտեմբեր, 2024`,
  22 = `10 դեկտեմբեր, 2024`, 23 = `13 դեկտեմբեր, 2024`.
- Homework line: each video links the homework current at the time (13: the project, 14: the
  Lecture 14 problems, 15: Homework 5). Homework 5 (due 3 Dec) is the last one on the course
  page, so lectures 16, 17 and 19 link it as above; lectures 20-23 drop the two homework lines.
- The music credits stay: the intro and outro are the same clips (`assets/asof/`).
- Locally, `description.txt` starts with the repo's title header (`🎬 Վերնագիր՝ <title>`, blank,
  divider, blank), which `yt_publish.py set-description` strips before upload.

## Chapters

- 20-27 chapters for 80-100 minutes, on **exact seconds** where the topic is named.
- Time format as in the series: `MM:SS` zero-padded under an hour (`00:00`, `02:25`), `HH:MM:SS`
  after (`01:01:12`), mixed within one list.
- Labels: Armenian, with the lecture's math notation (`ℤ`, `ℚ`, `F[x]`, `⊕`, `≃`, `⇒`, `↔`,
  `φ[a]`, `a_1 | ... | a_m`), and step words with the separator `․` (U+2024 ONE DOT LEADER):
  `Հիշեցում․ ...`, `Օրինակ․ ...`, `Ապացույց․ ...`, `Թեորեմ․ ...`, `Լեմմա․ ...`, `Հարց․ ...`,
  `Քայլ 1․ ...`, `Չօրինակ․ ...`, `Դիտողություն`. Abbreviation used: `վ․ծ․` (վերջավոր ծնված).
- Start every label with a letter (YouTube strips leading symbols), no ASCII `<` or `>`.
- No nesting in this series so far: flat lists.
- Glossary: `.claude/skills/youtube-timestamps/assets/glossary.csv`; keep the terms the series
  already uses (PID, UFD, Դրինֆելդի մոդուլ, Քարլիցի մոդուլ, ոլորման էլեմենտներ).

## Edges and cuts

- Every new file is ASOF intro (0:00-0:08.55) + the raw Zoom recording + outro (last 7.51 s).
  No cut may touch the intro or the outro: the last cut ends where the outro starts, never `"end"`.
- Papikian starts lecturing at once (content at 0:09-0:10 on 14, 15 and raw 16), so there is
  normally no start chat. The edited videos end where the Zoom recording ended, mid-sentence.
- The earlier editor removed 0-6 min per lecture against the Kaltura length, and **not from
  pauses**. `find_edit_points.py` on 2026-10-21 (threshold floor + 20 dB, silences of 3 s+):

  | Silence length | Edited Դաս 15 (YouTube audio, 77.5 min) | Raw Դաս 16 (local, 93.1 min) |
  |---|---|---|
  | 3-5 s | 38 | 70 |
  | 5-10 s | 49 | 54 |
  | 10-15 s | 10 | 11 |
  | 15-30 s | 1 (18.3 s) | 3 (longest 16.6 s) |
  | 30 s+ | 0 | 0 |
  | per minute | 1.66 | 1.90 |

  **Final (2026-10-22, DECISIONS #22): no pause cuts after all.** The user: "match the style of
  older papikian videos no need to overdo it". The older uploads were never silence-trimmed
  (pause stats in #22), so the plans went back to content cuts only; the 4 s versions are kept as
  `*_v2_4s`. The note below is the intermediate step, kept for the record.
  **(Superseded) 2026-10-21: the user cuts pauses.** The first plans (content cuts only, 1-5 per
  video) looked "suspiciously low" to the user; their own edit of Arnak's lesson 11 (DECISIONS #17)
  cut 70 places, 12.9 of 73 min, mostly pauses from 4 s plus the hums between them. So these
  lectures get the same rule: `--min-silence 4` pre-ticked + `hum_join.py --write` + rerun, content
  cuts kept, chapters remapped from the content-only plan (kept as `*_v1_content_only`).
  The earlier reasoning, kept for the record: he writes on the iPad while silent, so a pause is
  writing time and cutting it makes the handwriting jump; the earlier editor kept every pause.
  Old rule: run `find_edit_points.py --min-silence 150`
  (the Arnak setting) and put only content cuts in `content_cuts.json`: logistics, "can you
  hear me", tech trouble, a break, everything after the last content sentence (up to the outro).
  Check any silence of 15 s+ with a frame from the local file; keep it if he is writing.
- Local audio for the analysis: the joined files in
  `Desktop\misc\YSU OpenCourseWare\papikian\Das NN - Algebra and Number Theory - Papikian - <date>.mp4`
  (`--audio`; their length equals the YouTube video's).
