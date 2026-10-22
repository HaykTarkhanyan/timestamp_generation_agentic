# Das 20 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 27 chapters, 9 moved, 0 unmatched.
`old -> new | the real words at the new stamp`:

- `16:39 -> 16:40 MOVED Հարց․ ինչո՞ւ դիսկրիմինանտը կախված չէ բազ | առանց ինչը իսկմինանտը`
- `29:28 -> 29:29 MOVED Կոտորակային իդեալ (fractional ideal) | սահմանում ենք ֆրակցիաների չգիտեմ`
- `47:32 -> 47:33 MOVED Ապացույց | որ էս փաստը ճիշտ չի էդ ժամանակ ըը`
- `54:13 -> 54:14 MOVED Ապացույցի ավարտը․ (b) ⊇ P_1 ⋯ P_k | վերցնում ենք ուղղակի ցանկացած էլեմենտ pից`
- `57:53 -> 57:52 MOVED Թեորեմ․ ամեն իդեալ միակ ձևով պարզ իդեալն | եթե հլա որ իմ հետ եք եկեք կարևոր`
- `01:07:08 -> 01:07:09 MOVED Հետևանք․ I · Ĩ = O_K, իդեալները կազմում  | որ մենք ունենք խումբ չէ`
- `01:13:52 -> 01:13:51 MOVED Խնդիրներ | բաները մի հատ էլի պրակտիկայի ժամանակ այսօր նայեք եք`
- `01:14:24 -> 01:14:25 MOVED Իդեալների դասերի խումբ Cl(K) | մյուս մյուս անգամ էլ հիմա մենք ունենք էս խումբը`
- `01:17:57 -> 01:17:58 MOVED K-ի ζ-ֆունկցիան և Cl(K)-ն | որ կանենք ըը առանց ապացույցի`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 26 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 20 | Կոտորակային իդեալներ։ Իդեալների միակ վերլուծումը | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 20 | Իդեալների վերլուծումը պարզ իդեալների արտադրյալի | Հանրահաշիվ և թվերի տեսություն`). Codex's proposal (candidate 2). Claude would keep the old title, optionally adding 'միակ'. Chosen because it names both halves: fractional ideals and the inverse P̃ (29:29-57:52, about half the lecture) and the main theorem with the uniqueness he stresses (00:34, 58:12). It also avoids 'վերլուծումը ... արտադրյալի', which Codex found unnatural without 'տեսքով'.

**Taken** (`T2 time label -> final time label | source: why`):

- `00:00 Նպատակը․ իդեալը որպես պարզ իդեալների արտադրյալ` -> `00:00 Նպատակը․ I ≠ 0 իդեալը որպես պարզ իդեալների արտադրյալ` | codex: the zero ideal has no factorization
- `08:23 Հետևանք․ պարզ իդեալը մաքսիմալ է, O_K/P-ն վերջավոր դաշտ է` -> `08:23 Հետևանք․ P ≠ 0 պարզ իդեալը մաքսիմալ է, O_K/P-ն վերջավոր դաշտ է` | both: the zero ideal is prime but not maximal
- `29:29 Կոտորակային իդեալ (fractional ideal)` -> `29:29 Կոտորակային իդեալ` | claude: no other chapter carries an English gloss
- `38:37 Թեորեմ․ P պարզ ⇒ P · P̃ = O_K` -> `38:37 Թեորեմ․ P ≠ 0 պարզ ⇒ P · P̃ = O_K` | both: false for P = 0; the proof uses that P is maximal
- `41:38 Եթե P · P̃ = P, ապա P̃-ն ամբողջ է ⇒ P̃ = O_K` -> `41:38 Եթե P · P̃ = P, ապա P̃-ի տարրերն ամբողջ են ⇒ P̃ = O_K` | codex: the step is that every element of P̃ is integral (43:43-45:16)
- `46:42 Լեմմա․ ամեն իդեալ պարունակում է պարզ իդեալների արտադրյալ` -> `46:14 Լեմմա․ ամեն I ≠ 0 պարունակում է ոչ զրոյական պարզ իդեալների արտադրյալ` | both: Claude: the lemma is introduced at 46:14.0 'դրա համար պետք է մեզ մի հատ լեմմա'; 46:42 is its restatement. Codex: nonzero ideal, nonzero primes (applied to (b), b ≠ 0, at 54:13)
- `47:33 Ապացույց` -> `47:08 Ապացույց` | claude: 47:08.5 'Եկեք ուղղակի ապացույցը մի հատ արագ նայենք'; 47:33 is mid-step
- `57:52 Թեորեմ․ ամեն իդեալ միակ ձևով պարզ իդեալների արտադրյալ է` -> `57:52 Թեորեմ․ ամեն I ≠ 0 իդեալ միակ ձևով պարզ իդեալների արտադրյալ է` | both: the zero ideal is excluded
- `01:07:09 Հետևանք․ I · Ĩ = O_K, իդեալները կազմում են խումբ` -> `01:07:09 Հետևանք․ I · Ĩ = O_K, ոչ զրոյական կոտորակային իդեալների խումբը` | both: false as written: ordinary ideals have no inverses (24:21); the group is the nonzero fractional ideals (01:08:29)
- `01:14:25 Իդեալների դասերի խումբ Cl(K)` -> `01:14:25 Իդեալների դասերի խումբ H(K)` | claude: Դաս 23 and its notes write H(K)
- `01:17:58 K-ի ζ-ֆունկցիան և Cl(K)-ն` -> `01:17:58 K-ի ζ-ֆունկցիան և H(K)-ն` | claude: same group as 01:14:25: H(K), not Cl(K) (missed in the reconcile, caught in the final check)
- `01:13:51 Խնդիրներ` -> removed | both: 34 s of practice-session logistics (book problems 8.4-8.8); the text falls under the example

**Not taken:**

- codex: 01:10:05: split at 01:12:03. the chapter builds P_1, P_2, P_3 to reach (6) = P_1^2 P_2 P_3, which its label names
