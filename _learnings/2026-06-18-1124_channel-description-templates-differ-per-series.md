# Channel description templates differ per series

The user runs at least THREE distinct video series with different description templates. The skill (`SKILL.md`) currently only knows two. Future runs need to pick the right one from context, not blindly use the ML template.

## 1. Մաթեմատիկա ML-ի համար (math-for-ML)
Title: `Դաս NN | <topic> | Մաթեմատիկա ML-ի համար`

## 2. Մեքենայական ուսուցում (ML series, current)
Title: `[NN] <topic> | Մեքենայական ուսուցում`. Full template with Telegram link, materials URL, abstract, hashtags, `(Opus 4.8)` model attribution.

## 3. Կոմպլեքս անալիզ (Complex Analysis)
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

## Timestamp format for Complex Analysis series
- `MM:SS` with leading zero for chapters under 1hr: `00:00`, `56:09`
- `HH:MM:SS` for chapters past 1hr: `01:08:48`
- The series MIXES both formats within a single video when video crosses 1hr (e.g., `00:00 ... 56:09 ... 01:08:48`). The skill's "don't mix formats" rule does not apply here, since YouTube accepts both regardless.
- Verifier regex (`\d{1,2}`) accepts both `0:00` and `00:00` styles.
