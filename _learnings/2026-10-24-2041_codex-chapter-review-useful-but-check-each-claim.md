# Codex as second reader of chapter lists: real catches, plus suggestions that must be refused

Ashot's Դաս 4-8 (2026-10-24): one `codex exec -s read-only` run per lesson, title + chapters + that lesson's
slide text + the full transcript inline (`scripts/archive/info_theory_2026-10/codex_info_prompts.py`),
55-62 s each. It replies in Armenian when the material is Armenian.

**Real catches, confirmed in the transcript:**
- Դաս 5 05:02 said AEP is "an analogue of the law of large numbers"; at 05:30 the lecturer corrects himself:
  "not an analogue, a direct consequence of the weak law". The published label contradicted him.
- Դաս 4 45:20 "Ֆանոյի անհավասարությունը խիստ է": his own word, but "խիստ անհավասարություն" means a strict
  inequality; he meant the bound cannot be improved.
- Missing hypotheses: "typical" sequences (not all long ones) have probability ≈ 2^(-nH); X' independent of X
  in the collision bound; the average codeword length is ≤ n(H+ε), not equal to it.
- One real boundary: Դաս 7's student question starts at 09:34, not 09:43.

**Refused:**
- Replacing the fullwidth `＜` with ASCII `<` in labels ("format consistency"). YouTube rejects ASCII `<` `>`
  anywhere in a description. Say so in the prompt next time.
- Reopening a title the user had already chosen (Դաս 6, "put Kraft back"), and adding "ասիմպտոտիկ" to Դաս 5's
  title. A reviewer's taste does not override a decision the user made.
- Moving a chapter start onto the lecturer's answer instead of the student's question that opens the topic
  (Դաս 6 53:19 -> 53:36); the label became a "Հարց․" label instead.

**Takeaway:** worth the minute per lesson for wording and hypotheses. Check every item against the transcript,
keep the series rules (fullwidth `＜`, the user's titles) out of its reach.
