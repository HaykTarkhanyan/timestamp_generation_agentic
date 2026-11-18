# [05] Tool calling - correctness review (Opus 5.5, 2026-11-18)

Sources: the deck `llms/tools_agents/xx_tools_1.tex`, the saved runs `results/tools_1_run.json` and the notebook
`xx_tools_1_solution.ipynb` (course repo, commit 59baee7b). Times are on the saved 45:08 timeline (raw in brackets).

## Maybe (ASR or a slip of the tongue): not in the corrections unless you confirm

| Time | Said | Source | Note |
|---|---|---|---|
| 44:31 [0:55:15] | "all of today's examples cost us about three cents" | The 61 recorded calls of session 1 sum to $0.00341 (0.34 cents); the notebook says a full re-run is "under a cent" | Same pattern as [04]'s "two cents" (you skipped it). Draft line below if you want it |

## Checked and correct

- GPT-4o mini, asked today's date without tools, said "October 4, 2023" (slide 2, 12 Nov run).
- 17 × 23 answered directly as 391 with no tool call (`two_tools`).
- "Yerevan is warmer, -1 vs Gyumri -3": the run says -0.9 vs -3.1 °C.
- Sister cities: Tbilisi 0.5, Baku 8.2, Sofia 8.3, Krakow 4.8 °C; Sofia warmest, as said ("Georgia" was said for Tbilisi, harmless).
- Armenia vs Cyprus, 12 November, 21:00 in Yerevan, 3.6 °C (slide 23).
- Planted instruction: Llama 3.1 8B obeyed 2 of 6, the four other models 0 of 6 (slide 30); unprompted, Llama e-mailed "17 times 23 is 391" to assistant@assistant.com.
- Llama 3.1 8B pinned to Groq, GPT-4o mini to OpenAI (`pin()` in the setup cell).
- Sleeper agents: Anthropic's paper (January 2024) on backdoored models that survive safety training.

Caveat found after publishing: `results/tools_1_run.json` was last written at 16:48, before class, and the notebook ran
with `RERUN = False`, so the class's live calls and any prep runs are not in the 0.34 cents. Asked again (Q9), the user
kept the line: they meant the notebook's examples, so the saved run is the right comparison.

## Correction (approved Q8, kept Q9; live in the description)

- 45-րդ րոպեին - ասացի, որ այսօրվա բոլոր օրինակները մոտ 3 ցենտ արժեցան. նոթբուքի պահված կանչերը միասին 0.34 ցենտ են (0.0034 դոլար)։
