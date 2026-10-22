# Das 22 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 27 chapters, 5 moved, 0 unmatched.
`old -> new | the real words at the new stamp`:

- `14:15 -> 14:14 MOVED Թեորեմ․ f-ը p-Այզենշտայնի է ⇒ ⟨p⟩ = Pⁿ | օքեյ հիմա եթե վերադառնանք ըըը`
- `33:12 -> 33:13 MOVED Օրինակներ․ q = 17 և q = 11 | եթե qն ըըը 17`
- `46:17 -> 46:16 MOVED Միշտ կա՞ նման նկարագրություն․ Գալուայի խ | հիմա հիմա կարող եք հարցնել`
- `50:19 -> 50:18 MOVED Թեորեմ․ K_f ⊆ K_g ⇔ Spl(g) ⊆* Spl(f) | ստացվում հիմա վերջին մասը որ ուզում եմ`
- `01:07:50 -> 01:07:51 MOVED Ոչ աբելյան դեպքը․ Ֆրոբենիուսի էլեմենտ | լավ հիմա`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 27 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 22 | Փոխադարձության օրենքներ։ Չեբոտարյովի խտության թեորեմ | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 22 | Փոխադարձության օրենքներ։ Չեբոտարյովի խտության թեորեմ | Հանրահաշիվ և թվերի տեսություն`). Both reviews: keep. From 26:24 to the end (~49 of 75 min) the lecture follows 'What is a reciprocity law?' and closes with Chebotarev, Frobenius and Langlands.

**Taken** (`T2 time label -> final time label | source: why`):

- `06:27 Խնդիր․ Օստրովսկու թեորեմը` -> `06:27 Խնդիր․ Օստրովսկու թեորեմը և վալուացիաները` | both: takes in the 48 s valuation question (09:53), removed to make room for the 38:48 Q&A
- `14:14 Թեորեմ․ f-ը p-Այզենշտայնի է ⇒ ⟨p⟩ = Pⁿ` -> `14:14 Թեորեմ․ f-ը p-Այզենշտայնի է ⇒ pO_K = Pⁿ` | claude: pO_K as in this lecture's 00:00 and the notes ('(p) = Pⁿ'); ⟨ ⟩ appears nowhere else
- `23:10 Հարց․ քանի՞ p-ի համար է f-ը չբերվող mod p` -> `23:10 Հարց․ անվե՞րջ շատ p-ի համար է f-ը չբերվող mod p` | codex: the question is whether there are infinitely many (23:14 'ապացուցվա՞ծ ա, որ անվերջ շատ են')
- `(new)` -> `38:48 Հարց․ ընդհանուր քառակուսային բազմանդամներ, ինչո՞ւ մոնիկ` | both: 38:48.8 'իսկ ըհը, եթե մեր բազմանդամը...': 2.3 min student exchange (other quadratics reduce to x² - disc; why monic; Spl depends on O_K, not on f)
- `48:44 Թեորեմ․ Spl(f)-ը տրվում է կոնգրուենցիաներով ⇔ Gal(f)-ը աբելյան է` -> `48:36 Թեորեմ․ Spl(f)-ը տրվում է կոնգրուենցիաներով ⇔ Gal(f)-ը աբելյան է` | claude: 48:44 is mid-statement; the theorem starts at 48:36.3 'Պարզվում է, որ այս Spl-ը կապված...'
- `56:33 Օրինակ․ Spl(x² - 17)-ի խտությունը 1/2 է` -> `56:33 Օրինակներ․ Spl(x² - 17)-ի խտությունը 1/2, Spl(Φ_q)-ինը՝ 1/(q-1)` | claude: the chapter also gives the cyclotomic density 1/(q-1) (58:13), which Chebotarev then compares against
- `09:53 Հարց․ բազմանդամի աստիճանը որպես վալուացիա (valuation)` -> removed | both: 48 s; folded into 06:27 (Codex) instead of into 10:41 (Claude), since the question is about ord-like functions

**Not taken:**

- codex: 26:27: relabel as 'Լրիվ տրոհվող պարզ թվերը․ Spl(f)'. 'Ի՞նչ է փոխադարձության օրենքը' is the title of the Monthly article he follows from 26:27 ('What is a reciprocity law?'), and the chapter opens with it
- codex: 36:21: move to 37:41. 36:19 'մյուս ընդհանուր բազմանդամների համար' opens the higher-degree question the label names
- codex: 14:14: move to 14:37. 14:14 'Օքեյ, հիմա եթե վերադառնանք' is the turn back to the theorem
- codex: 01:07:51: move to 01:08:15. 01:07:51 'լավ հիմա, վերջին սլայդն է' opens the sketch
- claude: 14:14: spelling 'Էյզենշտեյնի' instead of 'Այզենշտայնի'. unverified (Claude said so too; a web search found no Armenian source); left as is, question for you

**Open, for the user:**

- Spelling: 'Այզենշտայնի' (German pronunciation) or 'Էյզենշտեյնի' (the Russian-style form Armenian textbooks may use)? Not verified.
