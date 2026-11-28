# Check chapters on the caption line they sit in, not by matching the predicted first line

**Symptom.** LLM [08] (2026-11-27): after YouTube processed the edit, a quick scratch script "snapped" the 48 chapters to
the regenerated captions by taking, for each chapter, the first predicted line at or after it and finding the most
similar real line within 12 s. It proposed 19 moves of 1-3 s. Checked by hand, at least 3 were wrong:

| chapter | proposed | real caption line at the chapter |
|---|---|---|
| 25:12 Հարց՝ հեղինակին ավելացնե՞լ... | -> 25:14 | 25:11 "այդ բանի հետ կապված..." (the question itself) |
| 46:42 Embedding-ներ՝ ... | -> 46:44 | 46:42 "Դե ժողովուրդ մեր հաջորդ քայլը..." |
| 50:35 Bi-encoder և cross-encoder | -> 50:37 | 50:34 "բայց այս պրոցեսի մեջ մի հատ պահն է..." |

**Cause.** After `remap_chapters.py` a chapter often sits at a cut's end, not on a predicted line start, and the
predicted transcript drops a line that started inside a cut (the [08] "արի դե ժողովուրդ մեր հաջորդ քայլը" line). So
"the first predicted line after the chapter" is often the topic's second line, and the matcher moved the chapter
onto it. YouTube also re-splits lines (the real 46:42 line merges what were two predicted lines), so similarity
scores of 0.65-0.75 picked neighbours.

**What worked.** Print, per chapter, the real line it falls in (start <= t) and the next one, and read them
(`scripts/non_essential/chapter_caption_lines.py --output-dir output/<dir>`). Move a chapter only when:
- the topic sentence starts in the next line, 1 s after the chapter (4 cases: 1:48, 21:48, 32:43, 53:46, all +1 s), or
- the chapter sits 1-3 s into the topic's own line (10 cases, -1 s; 11:33 -> 11:30, where "օքեյ դե չանքինգը..." starts).

Leave it when the line it falls in mixes the previous tail with the topic's first words and the chapter lands on
those words (4:51, 12:39, 30:59, 48:25, 52:21). Result on [08]: 14 moved, re-pushed, 48 chapters parsed; after the
push every moved chapter reads +0 s on its topic line.

**Consequence.** Don't write chapter times back from an automatic matcher; use it, at most, to list candidates.
