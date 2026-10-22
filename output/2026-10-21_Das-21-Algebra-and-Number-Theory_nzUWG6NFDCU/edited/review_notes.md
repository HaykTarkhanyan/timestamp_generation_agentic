# Das 21 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 26 chapters, 5 moved, 0 unmatched.
`old -> new | the real words at the new stamp`:

- `04:46 -> 04:45 MOVED Հարց․ որտե՞ղ է էական, որ O_K-ն ամբողջներ | մեկ էլ երկրորդ հարցը էլի որ տամ`
- `07:24 -> 07:25 MOVED Ապացույց․ նյոթերյան ⇔ ամեն իդեալ վ․ծ․ է | ոնց որ այս հատկությունը որ նստի համարժեք ա որ բոլոր`
- `32:14 -> 32:13 MOVED Դիսկրիմինանտը և հետքի երկգծային ձևը | հատկությունները սրանք շատ հեշտ է ցույց տալ բայց այս դիսկրիմի`
- `53:33 -> 53:34 MOVED Ճյուղավորման ինդեքս, e(P) ≥ 2 ⇔ p | disc | կոչվում է ramification index ու`
- `56:13 -> 56:14 MOVED m-ը քառակուսի է mod p ⇒ (p) = P_1P_2 | այն դեպքում եթե pն չի բաժանում mը`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 26 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 21 | Դեդեկինդի տիրույթներ։ Պարզ թվերը թվային դաշտերում | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 21 | Դեդեկինդի տիրույթներ։ Պարզ թվերը թվային դաշտերում | Հանրահաշիվ և թվերի տեսություն`). Both reviews: keep. Dedekind domains (04:45-30:35) and the decomposition of primes (42:13-end, ~32 min) take most of the time.

**Taken** (`T2 time label -> final time label | source: why`):

- `04:45 Հարց․ որտե՞ղ է էական, որ O_K-ն ամբողջների օղակ է` -> `04:45 Հարց․ որտե՞ղ է էական, որ O_K-ն ամբողջ թվերի օղակ է` | claude: Դաս 17 and 18-19 say 'ամբողջ թվերի օղակ'
- `05:33 Դեդեկինդի տիրույթ (Dedekind domain)․ նյոթերյան օղակ` -> `05:33 Դեդեկինդի տիրույթ․ պայման 1՝ նյոթերյան օղակ` | both: Noetherian is the first of three conditions (05:33), not the definition; no English gloss (Claude)
- `14:02 Պայման 2․ պարզ իդեալները մաքսիմալ են, Կրուլի չափողականություն` -> `14:02 Պայման 2․ P ≠ 0 պարզ ⇒ մաքսիմալ (Կրուլի չափողականություն 1)` | claude: in a domain (0) is prime and not maximal; the condition is on nonzero primes, i.e. Krull dimension 1 (he says so at 14:58)
- `18:41 Հարց․ նյոթերյան լինելը և վերջավոր չափողականությունը` -> `16:37 Հարցեր․ Կրուլի չափողականություն և նյոթերյան օղակներ` | claude: the student Q&A on Krull dimension starts at 16:37.8 'Իսկ...' (equal chain lengths?), ~6.7 min to 23:20; 18:41 is its third question
- `23:23 Պայման 3 և թեորեմ․ R դեդեկինդյան ⇔ իդեալների միակ վերլուծում` -> `23:23 Պայման 3․ ամբողջ փակ։ Թեորեմ․ Դեդեկինդի տիրույթ ⇔ միակ վերլուծում` | both: name condition 3, 'R is integrally closed in its field of fractions' (23:31); one name for the notion
- `40:30 Հետևանք․ N(α) = ±p ⇒ α-ն չբերվող է` -> `40:30 Հետևանք․ Nr(α) = ±p ⇒ α-ն չբերվող է` | claude: the element norm is Nr(α) in 35:49 and 36:48
- `48:23 pO_K = P_1^e_1⋯P_g^e_g և n = Σe_if_i` -> `48:23 pO_K = P_1^(e_1)⋯P_g^(e_g) և n = Σ e_i f_i` | claude: compound exponents in parentheses, as in Դաս 16
- `53:34 Ճյուղավորման ինդեքս, e(P) ≥ 2 ⇔ p | disc(K)` -> `53:34 Ճյուղավորման ինդեքս․ ինչ-որ e_i ≥ 2 ⇔ p | disc(K), օրինակ ℤ[√-5]` | both: p | disc(K) means SOME prime above p ramifies, not every P (cubic field of disc -23: (23) = P_1²P_2); merged with the 33 s 54:09 example
- `56:14 m-ը քառակուսի է mod p ⇒ (p) = P_1P_2` -> `56:14 p ∤ 2m, m-ը քառակուսի է mod p ⇒ (p) = P_1P_2` | both: fails at p = 2 (m = 5 is a square mod 2, yet 2 is inert in ℚ(√5)); the notes say 'p = odd prime'; he says p ∤ m at 56:16. (p | m ⇒ (p) = P² at 54:42 holds for p = 2 too)
- `58:02 m-ը քառակուսի չէ mod p ⇒ (p)-ն պարզ է` -> `58:02 p ∤ 2m, m-ը քառակուսի չէ mod p ⇒ (p)-ն պարզ է` | both: same restriction as 56:14
- `(new)` -> `01:04:50 f(x)-ը չբերվող է mod p ⇒ p-ն մնում է պարզ` | claude: 01:04:50.4 'Ոնց որ ամենագլխավոր թեորեմն է այսօրվա': the general argument, f irreducible mod p ⇒ p stays prime (~2 min), before Dedekind
- `01:06:45 Դեդեկինդի թեորեմը․ p-ի վերլուծումը f(x) mod p-ով` -> `01:06:45 Դեդեկինդի թեորեմը․ p ∤ [O_K : ℤ[α]] ⇒ p-ի վերլուծումը f(x) mod p-ով` | codex: he excludes the primes dividing the index at 01:08:56
- `54:09 Օրինակ․ ℤ[√-5]-ում (2) = P² և (5) = Q²` -> removed | claude: 33 s, merged into 53:34

**Not taken:**

- codex: 07:25: move to 07:42. 07:25 states the equivalence the chapter proves; 07:42 is the first proof step
- codex: 27:43: relabel as the failure of unique factorization. 'factorization is not unique in ℤ[2i]' is true and is the point of the exercise
- codex: 36:48: add a 37:42 chapter on quadratic units. a 1.3 min sub-part of the same corollary (Claude: fine inside it)
- codex: 48:23: split at 51:42. the label names both the factorization and n = Σ e_i f_i; the 48:57-50:44 PID question can stay inside (Claude)
- codex: 01:11:48: split at 01:12:26. it would leave a 38 s chapter; the label names both

**Open, for the user:**

- Lecturer slip (31:21): N(I) = D(I)/D(O_K) is missing a square; it is N(I)² = D(I)/D(O_K) (Դաս 20: N(I) = |det|, D(I) = det²·D). Correction note?
- Lecturer slip (23:10): 'Noetherian ⇒ finite Krull dimension' is false (Nagata); at 21:01 he had read on Wikipedia that it can be infinite. Correction note?
- Lecturer slip (14:21): 'every prime ideal is maximal' needs 'nonzero'. The label now says P ≠ 0; a note is optional.
- Lecturer overstatement (01:13:02): the completely split primes determine K when K is Galois over ℚ (in general they determine its Galois closure). Correction note?
- The quadratic rule for p = 2 (56:14-58:02) is not covered; the labels now say p ∤ 2m. A note is optional.
