# Armenian auto-subs are useful but math-garbled

yt-dlp's `--write-auto-sub` returns Armenian transcripts that are good enough for topic detection but break on math notation. Common patterns:
- Per-word timing tags split mid-word: `p-value` becomes `pվ value` or similar.
- Named theorems are inconsistent: `Արցելա-Ասկոլի` may appear as `արզելաասկոլայինը` (one mashed word) or with random Latin letters mixed in.
- Latin technical terms are often code-switched in: `sin(πz)`, `exp(z)`, `cos`, etc. appear as-is.

Strategy for picking chapter labels: ignore the math fragments, latch onto the conversational Armenian transition phrases (`Հիմա անցնենք X-ին`, `Եկեք փորձենք`, `Ուրեմն`). The glossary at `.claude/skills/youtube-timestamps/assets/glossary.csv` covers ~1060 stats/ML terms but not analysis-specific named theorems (Weierstrass, Mittag-Leffler, Riemann, Harnack, Perron, Arzela-Ascoli) - those need manual transliteration to Armenian convention.
