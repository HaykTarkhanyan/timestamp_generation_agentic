# Դաս 18-19 (course lecture 19): independent review of chapters and title (Claude, 2026-10-22)

**Verdict:** publishable after a few fixes. Boundaries are accurate. The main issue is in the core proof: the 50:12 chapter is labelled as "K's discriminant as volume", but most of it is the start of the finiteness proof, and K's discriminant is only defined at 59:50. 22 chapters for 68 min is fine.

Word times come from `VyWS3Ppv2ao.hy.vtt`.

## Chapter findings (most severe first)

| time | current label | problem | suggested fix | evidence | certainty |
|---|---|---|---|---|---|
| 50:12 | K-ի դիսկրիմինանտը որպես O_K-ի «ծավալ» | label/coverage: only 50:12-51:44 is the volume intuition (determinant = volume, lattice). 51:47-55:57 (~4 min) is the set-up of the main proof: pick integral ω_1..ω_n independent over ℚ, take O = ⊕ ℤω_i ⊂ O_K, adjoin ω ∉ O, and show O' = O + ℤω still has rank n. K's discriminant is not defined until 59:50 | keep 50:12 as `Դիսկրիմինանտը որպես ծավալ`; add **51:47** `Ապացույց․ O = ⊕ ℤω_i ⊂ O_K, O' = O + ℤω-ն n ռանգի է` | `0:50:58 ... էս օկայի ծավալն ա ցույց տալիս` / `0:51:47 եթե ընտրե N հատ էլեմենտ` / `0:53:13 ո՞նց կարող ենք ցույց տալ որ էս Այս օկան վերջավոր գեներատված է z-ի վրա` / `0:53:51 ... ռանքը այս օշեխիզ z-ի վրա n-ն ա, ոչ թե n գումարած 1` / `0:59:50 ու եթե ընտրենք ինչ-որ բազի սոկայի այդ ժամանակ կայի դիսկրինանտը սահմանվում է` | judgment |
| 55:57 | Դիսկրիմինանտը նվազում է ⇒ պրոցեսը վերջավոր է | math: D can be negative (the lecture's own ℤ[i] example gives -4), so what strictly decreases is \|D\|: D(ω) = det(A)²⋅D(ω') with \|det A\| ≥ 2 | `\|D\|-ն նվազում է ⇒ պրոցեսը վերջավոր է` | `0:58:44 երկուսից մեծ թիվ է, դա նշանակում է, որ դիսկրինանտը փոքրանում է` / `1:05:49 ... մինուս չորս ենք ստանում` | certain (low severity) |
| 39:33 | (inside 34:14 "Հարց․ σ_i σ_j կոմպոզիցիայի իմաստը") | coverage: after the student exchange (34:16-39:30) the lecturer returns to the proof that D ∈ ℚ (assume K Galois, σ permutes rows, D is fixed, so it is rational) for ~2.4 min. That part sits under the Q&A label | add **39:33** `Ապացույց․ D ∈ ℚ (Գալուայի դեպքում)` | `0:39:33 քանի որ գալու մասին ես չեմ խոսել, եկեք պատկերացնենք, որ ինքը ... գալու է` / `0:40:13 ... այս դիսկրիմինանտը չի փոխվում, որովհետև ուղղակի տողերն եմ իրար մեջ` / `0:40:51 ինչ-որ էլեմենտ կայի, որը բոլոր սիգմաների տակ չի շարժվում ... պետք ա լինի Q` | judgment |
| 59:34 | Թեորեմ․ O_K-ն n ռանգի ազատ ℤ-մոդուլ է | label/coverage: the definition of disc(K) as the discriminant of an integral basis, independent of the basis, is given here (59:50-1:00:40) and is not named anywhere | `Թեորեմ․ O_K-ն n ռանգի ազատ ℤ-մոդուլ է․ disc(K)` | `0:59:50 ու եթե ընտրենք ինչ-որ բազի սոկայի այդ ժամանակ կայի դիսկրինանտը սահմանվում է` / `1:00:12 կախված չի, թե ինչ բազում` | judgment (low) |
| 01:03:55 | Ճյուղավորված պարզերը բաժանում են disc(K)-ն | math/label: the lecturer states both directions ("exactly these primes"), but the label gives one. Դաս 21 states it as ⇔ | `p-ն ճյուղավորվում է ⇔ p \| disc(K)` | `1:04:04 ... այն պարզ թվերը, որոնք բաժանում են դեմ, հենց այն պարզ թվերն են, որոնք ... ramify` / `1:05:11 այս պարզ թվերը հենց այն պարզ թվերն են, որ այս դիսկրիմինտն են բաժանում` | judgment (low) |
| 15:36 | Քանի՞ ներդրում K ↪ ℂ կա | boundary: "how do we define conjugates (be careful in two places)" opens at 15:11, and 15:36 continues the same thought | **15:11** | words: `15:11.72 Հիմա` `15:12.08 համալուծները` `15:13.04 ենք` `15:13.24 սահմանում` ... `15:36.24 հիմա` | judgment (low) |
| 01:00:49 | Պատկերավոր․ ցանցի ծավալը ℝ²-ում | Armenian: "Պատկերավոր" is an adjective ("figurative") and reads oddly as a step word | `Երկրաչափական պատկեր․ ցանցի ծավալը ℝ²-ում` (or `Նկար․ ...`) | label | judgment (low) |
| 41:56 | D ≠ 0 ⇔ ω_i-երը գծորեն անկախ են | math precision: independent over ℚ (the lecturer says so twice) | `D ≠ 0 ⇔ ω_i-երը գծորեն անկախ են ℚ-ի վրա` | `0:42:15 ... բազիս են կազմում q-ի վրա կ-ի բազիսը` / `0:42:49 գծորեն անկախ են qի վրա` | certain (low) |
| 09:30 | Պրիմիտիվ էլեմենտ․ K = ℚ(α), α ∈ O_K | consistency: Դաս 17 uses "Պրիմիտիվ տարրի թեորեմ" for the same object | `Պրիմիտիվ տարր․ K = ℚ(α), α ∈ O_K` | Դաս 17 chapter 33:24 | judgment (low) |

Checked and fine: the n embeddings theorem, the ℚ(∛2) example (one real image and two equal complex images), independence of the σ_i from the choice of α (symmetric polynomial argument), the Vandermonde/disc(f) chapter including b² - 4c, ω_i ∈ O_K ⇒ D ∈ ℤ, D(u) = det(A)²⋅D(ω), disc of ℚ(√d) (d or 4d), the 2 = (1+i)² example and ℚ(ζ_p). The opening student question (01:41-02:30) is too short for a chapter. "Հարց․ արդյո՞ք O_K-ն վ․ծ․ ℤ-մոդուլ է" is the lecturer's driving question ("Այսօրվա հարցը էդ ենք նայելու", 06:47), so the label fits.

## Title

Current: `Դաս 18-19 | Թվային դաշտի դիսկրիմինանտ։ Ամբողջ թվերի օղակը` (57 chars).

**Proposed (judgment call):** `Դաս 18-19 | Համալուծներ և դիսկրիմինանտ։ O_K-ն ազատ ℤ-մոդուլ է` (61 chars).

Why: the second half of the current title names the object but not the result. The lecture's stated goal (06:24-06:51) is to decide whether O_K is a finitely generated ℤ-module, and it ends with the theorem that O_K is free of rank n (59:34). The other main block, conjugates/embeddings K ↪ ℂ (15:36-32:15, ~17 min), is missing from the current title. Also, "Թվային դաշտի դիսկրիմինանտ" is only defined in the last minutes. Most of the time is spent on the discriminant of n elements, so the bare "դիսկրիմինանտ" is the more accurate word.
