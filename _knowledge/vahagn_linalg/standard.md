# Գծային հանրահաշիվ (Vahagn Mikaelian, 2021): series standard for the new pieces 21.1-28.4

Taken from the 72 published pieces (`output/vahagn_linalg_overview/overview.json`, read 2026-10-24) and the
user's instructions of 2026-10-25. Read before drafting or reviewing any piece.

## Title

`Դաս <section> | <topic> | Գծային հանրահաշիվ`, the section from the file name with Armenian letters for the
parts: `21.1`, `23.1-ա` (file `23.1.a`), `23.1-բ`, `28.3-ա`. The topic is Armenian, one or two parts joined
by `։` (`Մատրիցի ռանգ։ Կրոնեկեր-Կապելիի թեորեմ`), at most ~60 characters so the title stays under 100.
Notation in titles as published: `R^2`, `F^n`, `Z_p^n`, `Ax=b`.

## Description (exact template; the 🎬 header and divider are local only, stripped on push)

```
🎬 Վերնագիր՝ <title>

──────────────────────────────

ԵՊՀ Ինֆորմատիկայի և կիրառական մաթեմատիկայի ֆակուլտետի դասախոս պրոֆ․ Վահագն Միքայելյանի դասախոսությունը «Բարձրագույն հանրահաշիվ» առարկայից՝ գծային հանրահաշվի վերաբերյալ։

🗓️ Ամսաթիվ՝ <D month, 2021>


📚 Դասախոսությունների ֆայլը՝
http://bit.ly/LinAlgebra
Դասագրքեր և այլ նյութեր՝
https://mathteam.notion.site/algebra


⏳ Թեմաներ
00:00 ...


👇 Բոլոր դասախոսությունները՝
https://www.youtube.com/playlist?list=PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM
```

No abstract, no hashtags, no correction notes (DECISIONS #25). Month names in the genitive-free form the
series uses: հունվար, փետրվար, մարտ, ապրիլ, մայիս, հունիս.

## Date

The lecture date is the raw file's `creation_time` (Yerevan date): each file was exported right after its
lecture, Tue ~14:2x / Thu ~11:0x (status.md, checked on 20.1). Table in `status.md`.

## Chapters

- `MM:SS` (all pieces are under an hour), first `00:00`, 30 s+ apart.
- **One level of nesting where it helps** (the user, 2026-10-25: "use 1 level hierarchy whenever its useful"):
  4 spaces before the time, a parent has 2+ children, never deeper. A piece that is one straight line of
  argument stays flat. The published 1.1-20.3 are flat; the new pieces differ on purpose.
- Labels as published: short Armenian, prefixes with the Armenian `․`: `Օրինակ․ ...`, `Ապացույց․ ...`,
  `Թեորեմ․ ...`, `Հետևանք․ ...`, `Հիշեցում․ ...`, `Սահմանում․ ...`, `Հարց․ ...` (a student's question).
- Notation as published: `ker(T)`, `im(T)`, `rank(A)`, `nullity(A)`, `rref(A)`, `col(A)`, `row(A)`, `R^5 → R^3`,
  `P_3`, `[T]_B`, `I_n`, `⇔`, `⇒`. No ASCII `<` `>` (use `＜` `＞`).
- Terms: his own words where he uses them (դիագոնալիզացիա / դիագոնալիզացվող, not the glossary's
  անկյունագծայնացում; երկրաչափական / հանրահաշվական պատիկություն; Գրամ-Շմիդտ; օրթոգոնալիզացիա), else `glossary.csv`: միջուկ (kernel), պատկեր (image), դեֆեկտ
  (nullity), ռանգ (rank), ինյեկտիվ / սյուրյեկտիվ / բիեկտիվ, պրոյեկցիա, պտույտ, ածանցյալ, զրոյական տարածություն,
  աստիճանաձև տեսք (REF), բերված աստիճանաձև տեսք (RREF), ազատ փոփոխական.
- Drafted on the **raw** timeline in `edited_predicted/timestamps_raw.txt` (times may carry tenths), then
  mapped through the cut list with `scripts/remap_chapters.py --from-cuts raw --from
  edited_predicted/timestamps_raw.txt --to-cuts <list>` (the 4 s plan now, the user's reviewed list later).

## Thumbnail

`python scripts/make_umath_thumbnails.py --series linalg --lesson <section> --topic "<short topic>"`
-> `thumbnails/umath/linalg_<section>.png`. Short topic, two lines at most.
