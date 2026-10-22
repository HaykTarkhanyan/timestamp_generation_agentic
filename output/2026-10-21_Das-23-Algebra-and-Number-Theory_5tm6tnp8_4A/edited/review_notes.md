# Das 23 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 27 chapters, 10 moved, 1 unmatched.
`old -> new | the real words at the new stamp`:

- `04:24 -> 04:25 MOVED Իդեալների դասերի խումբ՝ H(K) = I(K)/P(K) | ու այս խումբը կարևոր դեր է խաղում թվերի տեսության մեջ կոչվու`
- `05:28 -> 05:28       UNMATCHED A ~ B համարժեքության պայմանը | հիմա այստեղ այս էկվիվալենցը`
- `08:18 -> 08:19 MOVED Օրինակ․ ℚ(√-5)-ում ⟨2, 1-√-5⟩ ~ ⟨3, 1+√- | դաշտի մեջ մենք գիտենք որ սա pի չի առաջին`
- `10:13 -> 10:12 MOVED Հարցեր․ վերջավո՞ր է h(K)-ն, ինչպե՞ս է այ | նստած առաջին հարցը այսինքն հիմա հարցերը`
- `15:13 -> 15:14 MOVED Գաուս-Հեգներ-Սթարք․ h(ℚ(√-d)) = 1 ⇔ d =  | կա սենց հայտնի թեորեմ որը`
- `18:27 -> 18:28 MOVED Մինկովսկու թեորեմի ապացույցի գաղափարը | հիմա հիմա մինչև դասի վերջ ուղղակի կնայենք`
- `23:37 -> 23:36 MOVED Մինկովսկու սահմանը՝ M_K | մինկովսկու թեորեմը իսկականում`
- `29:39 -> 29:40 MOVED Հետևանք․ K ≠ ℚ ⇒ |d(K)| ≥ 2, կա ճյուղավո | սենց բան կարող ենք ցույց տալ էլի մինկովսկի`
- `41:10 -> 41:09 MOVED Ապացույց․ α-ի նորմի գնահատումը | հիմա այս մեր աֆան կլինի որ`
- `56:49 -> 56:50 MOVED Դասերի թվի բանաձևը և ռեգուլյատորը | ունենք ունենք ունենք class formula այսինքն`
- `01:01:46 -> 01:01:45 MOVED Օրինակ․ x⁴ + 1, ℚ(ζ_8), h(K) = 1 | մի հատ էլ օրինակ ցույց տամ որ եթե վերցնենք`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 27 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 23 | Իդեալների դասերի խումբ։ Մինկովսկու սահմանը | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 23 | Իդեալների դասերի խումբ։ Մինկովսկու սահմանը | Հանրահաշիվ և թվերի տեսություն`). Both reviews: keep. The class group and its finiteness via Minkowski's bound run from 02:46 to 53:26, about 50 of 68 min.

**Taken** (`T2 time label -> final time label | source: why`):

- `04:25 Իդեալների դասերի խումբ՝ H(K) = I(K)/P(K)` -> `04:25 Իդեալների դասերի խումբ H(K) = I(K)/P(K), A ~ B ⇔ αA = βB` | claude: merged with the 1 min 05:28 chapter and given the criterion he states at 06:16; 27 chapters were dense for 68 min
- `08:19 Օրինակ․ ℚ(√-5)-ում ⟨2, 1-√-5⟩ ~ ⟨3, 1+√-5⟩` -> `08:19 Օրինակ․ ℚ(√-5)-ում (2, 1-√-5) ~ (3, 1+√-5)` | claude: ideals in parentheses as in Դաս 20-21
- `15:14 Գաուս-Հեգներ-Սթարք․ h(ℚ(√-d)) = 1 ⇔ d = 1, 2, 3, 7, ..., 163` -> `15:14 Գաուս-Հեգներ-Սթարք․ h(ℚ(√-d)) = 1 ⇔ d = 1, 2, 3, 7, 11, 19, 43, 67, 163` | codex: the list is finite and known; the ellipsis hid it (squarefree d is the series' convention for ℚ(√d))
- `19:39 Ամեն դաս պարունակում է N ≤ c նորմով ինտեգրալ իդեալ` -> `19:39 Ամեն դասում կա ամբողջ իդեալ I, որ N(I) ≤ c` | codex: N had no argument
- `25:47 Հարց․ որքանո՞վ է լավ այս գնահատականը` -> `25:20 Հարցեր․ դժվա՞ր է ապացուցել, որքանո՞վ է լավ գնահատականը` | claude: the exchange starts at 25:20.5 'Սա ահագին դժվար ա չէ՞ ապացուցում'; 25:48 is the second question
- `29:40 Հետևանք․ K ≠ ℚ ⇒ |d(K)| ≥ 2, կա ճյուղավորված պարզ թիվ` -> `29:40 Հետևանք․ K ≠ ℚ ⇒ |disc(K)| ≥ 2, կա ճյուղավորված պարզ թիվ` | claude: disc(K) as in Դաս 18-19 and 21
- `34:50 Ապացույց․ կա α ∈ I, որ |N(α)| ≤ c·N(I)` -> `34:50 Ապացույց․ կա α ∈ I, որ |Nr(α)| ≤ c·N(I)` | claude: the element norm is Nr(α) in Դաս 17 and 21
- `50:41 Խնդիրներ․ դասերի խմբերի հաշվարկ (դասագիրք, գլուխ 12)` -> `50:41 Խնդիրներ․ դասերի խմբերի հաշվարկ (դասագիրք, էջ 341)` | claude: 'գլուխ 12' is never said; he points to page 341 (51:23)
- `52:26 Մինկովսկու սահմանը ավելի ուժեղ է` -> `52:26 Մինկովսկու M_K-ն ավելի ճշգրիտ է, քան c-ն` | claude: 'stronger' than the constant c proved in class (11 vs 3 for ℚ(√-5))
- `55:50 Հարց․ միավորների խումբը՝ O_K^× ≃ ℤ^(r+s-1) × μ_K` -> `55:50 Միավորների խումբը․ O_K^× ≃ ℤ^(r+s-1) × μ_K` | codex: a theorem stated under 'Հարց․'
- `01:04:09 Հարց․ ցիկլոտոմիկ դաշտեր, Ֆերմայի մեծ թեորեմ և ռեգուլյար պարզեր` -> `01:04:09 Հարց․ ցիկլոտոմիկ դաշտերի դասերի թիվը միշտ մե՞կ է` | codex: the student asks whether every cyclotomic field has class number one (1:04:09)
- `(new)` -> `01:05:20 Կումմեր․ Ֆերմայի մեծ թեորեմը և ռեգուլյար պարզերը` | codex: 1:05:20-end (2.4 min): Kummer, Fermat's last theorem and regular primes
- `05:28 A ~ B համարժեքության պայմանը` -> removed | claude: merged into 04:25

**Not taken:**

- codex: 23:36: move to 24:53. 23:35 'Մինկովսկու թեորեմը իսկականում ավելի ուժեղ թեորեմ ա' opens the theorem that defines the bound
- codex: 34:50: move to 35:39. 34:50 'մինչև լեկցիայի վերջը քննարկեմ թե ոնց ենք ապացուցում' announces the proof
- claude: 17:36: merge into 15:14. a distinct, well-known open problem (Gauss's conjecture), and 15:14 is already long
- claude: 52:26: merge into 50:41 or 45:43. kept, relabelled: a separate comparison of the bounds
- claude: 10:12: 'Երկու հարց․'. 'Հարց․' is a series step word for any question, not only a student's

**Open, for the user:**

- Description correction note (from the earlier review): the slide 'm^n ≤ N(I) ＜ m^(n+1)' may need (m+1)^n.
