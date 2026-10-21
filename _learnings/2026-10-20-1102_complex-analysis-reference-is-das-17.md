# Կոմպլեքս անալիզ: Դաս 17 is the reference for title, description and chapters

The user pointed to Դաս 17 (`https://youtu.be/0VcwMteJCxo`) as the model when redoing Դաս 24. It is hand-made, unlike the June drafts for Դաս 20-25, so match it rather than those.

What it does:
- **Title:** `Դաս 17 | Հարմոնիկ շարունակություն։ Պուասոնի ինտեգրալ | Կոմպլեքս անալիզ` - two topics joined by the Armenian full stop `։` (U+0589).
- **Description:** the layout in `2026-06-18-1124_channel-description-templates-differ-per-series.md`, two blank lines between blocks, date as `18 նոյեմբեր, 2025`. No abstract, hashtags or model tags.
- **Chapters sit on exact seconds** (03:08, 10:22, 15:04), not rounded minutes. 15 chapters for 66 minutes. The June drafts used round numbers (15:00, 28:00, 45:30, 49:00, 53:00) that missed the topic start by 10-90 s.
- **Labels use math notation and steps:** `u-ի`, `P_u`, `log(r)`, `Քայլ 1․ ...`. The separator is `․` (U+2024 ONE DOT LEADER), not an ASCII period.
- **YouTube strips leading symbols from chapter titles:** the label `∮ *du մեծությունը անկախ է r-ից` shows as `du մեծությունը ...` in the parsed chapters, while a mid-label `→` survives. Start every label with a letter.

Also seen: the live descriptions of Դաս 24 and 25 had the four title candidates pasted above the lecturer line. When giving the user paste-ready text, make it obvious which part is the title and which is the description.
