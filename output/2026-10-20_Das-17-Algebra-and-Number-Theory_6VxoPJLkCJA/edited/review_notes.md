# Das 17 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 26 chapters, 10 moved, 1 unmatched.
`old -> new | the real words at the new stamp`:

- `05:16 -> 05:15 MOVED Օրինակ․ քառակուսային դաշտերի O_K-ն | ըը շատ լավ հիմա ըըը`
- `10:43 -> 10:42 MOVED Պարզ ≠ չբերվող․ 6 = 2⋅3 = (1+√-5)(1-√-5) | ունեք հիմա ըըը մենք տեսանք ըը որ`
- `18:42 -> 18:43 MOVED Թեորեմ․ O_K-ն նյոթերյան օղակ է | լավ ըըը հիմա ըըը սրա համար ըըը`
- `23:10 -> 23:11 MOVED Նյոթերյան մոդուլ | նախ մի քիչ նույն`
- `32:01 -> 32:02 MOVED Հետևանք․ ℤ[α]-ն նյոթերյան օղակ է | եթե ունենք հիմա`
- `33:23 -> 33:24 MOVED Պրիմիտիվ տարրի թեորեմ | ոնց որ մենք մոտենում ենք մեր նպատակին`
- `36:27 -> 36:26 MOVED Ապացույց․ ինդուկցիա և Գալուայի տեսությու | ըը հիմա այս թեորեմը ոնց եք ապացուցում`
- `51:29 -> 51:30 MOVED Հետևանք․ m⋅α ∈ O_K, K-ն O_K-ի քանորդների | նաև ստանում եք էն որ ոնց որ թե սա նաև`
- `54:49 -> 54:47 MOVED Թվային դաշտի համալուծներ․ K → ℂ ներդրում | լավ մի հատ էլ`
- `58:54 -> 58:53 MOVED σ_i(K)-երը կարող են համընկնել․ Գալուայի  | հիմա աս`
- `01:00:40 -> 01:00:40       UNMATCHED Ամփոփում և հարց O_K-ի մասին | դավ էսօր այսօրվա լեկցիայից`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 24 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 17 | Ամբողջ թվերի օղակը O_K։ Պրիմիտիվ տարրի թեորեմ | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 17 | Թվային օղակներ։ Պրիմիտիվ տարրի թեորեմ | Հանրահաշիվ և թվերի տեսություն`). Both reviews picked candidate 2. 'Թվային օղակներ' fits lectures 17-23 alike; the first half is about O_K itself, and his own summary at 01:02:26 centres on it. 'O_K-ն նյոթերյան է' stays out: at 01:01:07 he says it was proved only for ℤ[α].

**Taken** (`T2 time label -> final time label | source: why`):

- `08:54 β ∈ O_K ⇔ Tr(β), Nr(β) ∈ ℤ` -> `08:54 Քառակուսային K․ β ∈ O_K ⇔ Tr(β), Nr(β) ∈ ℤ` | both: the trace-norm test holds for quadratic fields only; he says so at 08:54 'Քառակուսի ընդլայնումների ժամանակ'
- `11:59 Իդեալի միակ տրոհումը պարզ իդեալների` -> `11:59 Իդեալի միակ վերլուծումը պարզ իդեալների արտադրյալի` | claude: the series says 'վերլուծում' for factorization (Դաս 20, 21, 23; glossary 'միակ վերլուծություն') and keeps 'տրոհվել' for 'split'; 'արտադրյալի' was missing
- `13:58 Օրինակ․ (6) իդեալի տրոհումը ℤ[√-5]-ում` -> `13:58 Օրինակ․ (6) իդեալի վերլուծումը ℤ[√-5]-ում` | claude: same term
- `19:49 Չօրինակ․ ℂ[x^(ℚ≥0)]-ն նյոթերյան չէ` -> `19:49 Հակաօրինակ․ ℂ[x^(ℚ≥0)]-ն նյոթերյան չէ` | user: counterexample is 'հակաօրինակ' (glossary), not 'չօրինակ' (user, after the push; fixed live 20:49)
- `22:02 Հետևանք․ ամեն տարր չբերվողների արտադրյալ է` -> `22:02 Հետևանք․ ամեն ոչ զրոյական, ոչ միավոր տարր չբերվողների արտադրյալ է` | codex: zero and units are not products of irreducibles
- `23:11 Նյոթերյան մոդուլ` -> `23:11 Նյոթերյան մոդուլ․ վ․ծ․ ℤ-մոդուլը նյոթերյան է` | claude: merged with the 24:12 theorem (1.0 + 1.4 min); 26 chapters were dense for 65 min
- `27:51 Հարց․ ինչո՞ւ շղթան չի կարող անվերջ աճել` -> `27:40 Ապացույցի շարունակություն․ ինչո՞ւ շղթան չի կարող անվերջ աճել` | claude: the second half of the proof, his own rhetorical question; 27:40.2 'հիմա ո՞նց եմ շարունակում' opens it, 27:51 was mid-sentence
- `32:02 Հետևանք․ ℤ[α]-ն նյոթերյան օղակ է` -> `31:50 Հետևանք․ ℤ[α]-ն նյոթերյան օղակ է` | claude: 31:50.6 'Հիմա, եթե ինքը նոթերիան է, ինչի՞ համար ենք դա' opens the corollary
- `44:12 α-ն կարելի է ընտրել ամբողջ` -> `44:42 α-ն կարելի է ընտրել ամբողջ` | both: 44:10-44:41 still wraps up the primitive element ('սիրուն թեորեմ... բոլորը ունեն էս տեսք'); the integral α starts at 44:42.8 'Հիմա ստեղից կարող եք'
- `45:55 O_K-ն միշտ չէ, որ մոնոգեն է` -> `45:37 O_K-ն միշտ չէ, որ մոնոգեն է` | claude: the question 'can O_K always come from one element?' is asked from 45:37.1; 45:56 'Այս հարցը' refers back to it
- `47:29 Ապացույց` -> `47:29 Ապացույց․ α-ն կարելի է ընտրել ամբողջ` | both: 'հիմա էս թեորեմի ապացույցը': it proves the integral-α claim (lcm of the denominators, 47:55), not the non-monogenic remark just before, which he postpones
- `54:47 Թվային դաշտի համալուծներ․ K → ℂ ներդրումներ` -> `54:47 Թվային դաշտի ներդրումները․ [K:ℚ] = n ⇒ ճիշտ n ներդրում K → ℂ` | claude: merged with the 50 s 58:03 theorem chapter, which answers the question asked here
- `58:53 σ_i(K)-երը կարող են համընկնել․ Գալուայի դաշտ` -> `58:53 σ_i(K)-երը կարող են համընկնել․ Գալուայի ընդլայնում` | claude: 'Գալուայի դաշտ' usually means a finite field; he defines a Galois extension, and Դաս 18-19 says 'Գալուայի ընդլայնում'
- `24:12 Թեորեմ․ վ․ծ․ ℤ-մոդուլը նյոթերյան է` -> removed | claude: merged into 23:11
- `58:03 Թեորեմ․ [K:ℚ] = n ⇒ ճիշտ n ներդրում K → ℂ` -> removed | claude: merged into 54:47

**Not taken:**

- codex: 18:43: relabel as 'Նպատակ․ ապացուցել, որ O_K-ն նյոթերյան է'. a theorem label states the theorem, it does not claim the proof is in the chapter; the statement is true and he states it at 19:15
- codex: 13:58: 'տրոհման որոնումը'. the chapter is the worked example of (6); that he corrects a factor on the way does not change what it is about
- codex: 33:24: move to 34:38. 33:22 'Հիմա... նուրբ մոմենտ կա' opens the topic with the ℚ(√2, √3) example that motivates the theorem
- codex: 51:30: split off a 53:46 question. the 53:46 question (why K is the fraction field of O_K) is the second half of the same label and lasts ~1 min
- codex: 54:47: move to 55:25. 54:47 'լավ, մի հատ էլ... եկեք դրանք էլ քննարկենք' opens the embeddings topic
- codex: 58:53: move to 59:13. 58:53 'Հիմա աս սիգմաները...' opens the comparison of the images
- both: 01:00:40: split the student question off at 01:02:47 (Codex) / start at 01:00:10 with the preview (Claude). the label already names both parts; the preview is 28 s
- claude: 22:02: merge into 19:49. a different topic (a corollary vs a non-Noetherian example)
