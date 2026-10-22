# Das 19 (folder lecture number): review notes

## T2 (2026-10-22): chapters moved onto the real captions of the edited video

New auto-captions fetched into `edited/` after the edit was processed. Timeline check: where caption
lines match the predicted edited transcript exactly, they are 0 +-1 s apart (the cut list was right).
Each chapter was moved onto the first word of its topic using the captions' per-word timing; a match
more than 1 s later was not taken (a garbled first word, the match was a later word). 22 chapters, 2 moved, 0 unmatched.
`old -> new | the real words at the new stamp`:

- `43:50 -> 43:49 MOVED D(1, α, ..., α^(n-1))․ Վանդերմոնդի որոշի | շատ լավ մի հատ կարևոր օրինակ`
- `46:20 -> 46:21 MOVED ω_i ∈ O_K ⇒ D ∈ ℤ | լավ մյուս մյուս հատկությունը դիսկրինանտի նա է`

## T3-T5 (2026-10-22): independent reviews, reconciled

Claude (`review_claude.md`) and Codex (`review_codex.md`) reviewed the T2 chapters and titles; every
claim was checked against `transcript.txt` and the per-word caption times before it was taken.
Result: 24 chapters, verifier-valid (`verify_report_final.txt`).

**Title:** `Դաս 18-19 | Համալուծներ և դիսկրիմինանտ։ O_K-ն ազատ ℤ-մոդուլ է | Հանրահաշիվ և թվերի տեսություն` (was `Դաս 18-19 | Թվային դաշտի դիսկրիմինանտ։ Ամբողջ թվերի օղակը | Հանրահաշիվ և թվերի տեսություն`). Both reviews proposed 'Համալուծներ և դիսկրիմինանտ' first (conjugates take ~17 min and the old title left them out; disc(K) itself is defined only in the last minutes). Second half: Claude 'O_K-ն ազատ ℤ-մոդուլ է', Codex 'O_K-ի ℤ-բազիսը', the same result; the first states the theorem the lecture proves (59:34) and answers its opening question (06:24).

**Taken** (`T2 time label -> final time label | source: why`):

- `09:30 Պրիմիտիվ էլեմենտ․ K = ℚ(α), α ∈ O_K` -> `09:30 Պրիմիտիվ տարր․ K = ℚ(α), α ∈ O_K` | claude: Դաս 17 says 'Պրիմիտիվ տարր'
- `15:36 Քանի՞ ներդրում K ↪ ℂ կա` -> `15:11 Համալուծներ․ քանի՞ ներդրում K ↪ ℂ կա` | both: conjugates are introduced before 15:36: Codex 15:03 ('to define the discriminant we need conjugates'), Claude 15:11.7 'Հիմա համալուծները ո՞նց ենք սահմանում', the cleaner start
- `34:14 Հարց․ σ_i σ_j կոմպոզիցիայի իմաստը` -> `34:14 Հարց․ ե՞րբ է սահմանված σ_i ∘ σ_j կոմպոզիցիան` | codex: the student asks whether the composition is defined at all (34:35-35:39)
- `(new)` -> `39:33 Ապացույց․ D ∈ ℚ (Գալուայի դեպքում)` | claude: 39:33.8 'քանի որ Գալուայի մասին ես չեմ խոսել...': back to the proof, D is fixed by every σ, so D ∈ ℚ, ~2.4 min under the Q&A label; he leaves the general case to the students (41:34)
- `41:56 D ≠ 0 ⇔ ω_i-երը գծորեն անկախ են` -> `41:56 D ≠ 0 ⇔ ω_i-երը գծորեն անկախ են ℚ-ի վրա` | both: independence over ℚ (he says it at 42:12 and 42:43)
- `50:12 K-ի դիսկրիմինանտը որպես O_K-ի «ծավալ»` -> `50:12 Դիսկրիմինանտը որպես O_K-ի «ծավալ»` | both: the discriminant of K is defined only at 59:50; here it is the volume picture
- `(new)` -> `51:47 Ապացույց․ O = ⊕ ℤω_i ⊂ O_K, O' = O + ℤω-ն n ռանգի է` | both: 51:47.7 'եթե ընտրենք N հատ էլեմենտ': the main proof starts, ~4 min (ℤ-span of n independent integral ω_i, adjoin ω, the rank stays n)
- `55:57 Դիսկրիմինանտը նվազում է ⇒ պրոցեսը վերջավոր է` -> `55:57 |D|-ն նվազում է ⇒ պրոցեսը վերջավոր է` | both: discriminants can be negative (-4 at 1:05:49); it is |D| that drops
- `59:34 Թեորեմ․ O_K-ն n ռանգի ազատ ℤ-մոդուլ է` -> `59:34 Թեորեմ․ O_K-ն n ռանգի ազատ ℤ-մոդուլ է, disc(K)-ի սահմանումը` | claude: disc(K) as the discriminant of an integral basis, independent of the basis, is defined here (59:50-1:00:40) and was named nowhere
- `01:00:49 Պատկերավոր․ ցանցի ծավալը ℝ²-ում` -> `01:00:49 Երկրաչափական պատկեր․ ցանցի ծավալը ℝ²-ում` | claude: 'Պատկերավոր' is an adjective and reads oddly as a step word
- `01:03:55 Ճյուղավորված պարզերը բաժանում են disc(K)-ն` -> `01:03:55 Թեորեմ․ p-ն ճյուղավորվում է ⇔ p | disc(K)` | both: he states both directions: the primes dividing disc(K) are exactly the ramified ones (1:05:05)

**Not taken:**


**Open, for the user:**

- Lecture content, not a label: D ∈ ℚ is proved only for Galois K; the composition σ_i ∘ σ_j the student questions (34:16-39:30) is not defined in general, and he leaves the general case to the students (41:34-41:55). A description note is possible but not needed: he says so himself.
