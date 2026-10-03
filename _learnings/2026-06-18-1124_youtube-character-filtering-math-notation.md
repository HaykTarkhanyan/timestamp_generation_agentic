# YouTube character filtering (math notation)

Already in `SKILL.md`, but worth re-stating: YouTube REJECTS descriptions containing ASCII `<` or `>` even between spaces as math operators. Use Unicode lookalikes:
- `>` (U+003E) -> `＞` (U+FF1E FULLWIDTH GREATER-THAN)
- `<` (U+003C) -> `＜` (U+FF1C FULLWIDTH LESS-THAN)

Other Unicode that works fine in titles + descriptions: arrows (`→` `↔`), subscripts (`z₀`), superscripts (`x²`), Greek letters (`π` `ρ` `θ` `γ`), Armenian semicolon (`։`).
