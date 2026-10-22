# Դաս 20: independent review of chapters and title (Claude, 2026-10-22)

**Verdict:** publishable after small fixes. The labels follow the proof structure well. One "Ապացույց" stamp is 25 s late. Several labels drop the "nonzero" hypothesis, and one ("իդեալները կազմում են խումբ") is false as written. 27 chapters for 80 min is within the standard.

Word times come from `VCK3I6CkJI8.hy.vtt`.

## Chapter findings (most severe first)

| time | current label | problem | suggested fix | evidence | certainty |
|---|---|---|---|---|---|
| 01:07:09 | Հետևանք․ I · Ĩ = O_K, իդեալները կազմում են խումբ | math: ordinary ideals do not form a group (no inverses, which is exactly what 24:21 says). The group consists of the nonzero *fractional* ideals | `Հետևանք․ I · Ĩ = O_K, ոչ զրոյական կոտորակային իդեալները կազմում են խումբ` | `0:25:43 ... բայց նորից մենք` / `0:25:47 չունենք չենք հակադարձ չէ՞` (chapter 24:21); `0:29:28 սահմանում ենք ֆրակցիաների ... իդեալ`; Դաս 21 recap `0:03:18 այսինքն իդեալները, ֆրակցիոնալ իդեալները ... ունենք ակադարձ ... ոչ զրո` | certain |
| 47:33 | Ապացույց | boundary: 25 s late. The proof is announced at 47:08, and the stamp lands on "ու ուղղակի ենթադրենք" in the middle of its first step | **47:08** | words: `47:08.52 Եկեք` `47:09.52 ուղղակի` `47:10.56 ապացույցը` `47:11.16 մի` `47:11.28 հատ` `47:11.60 արագ` `47:11.88 նայենք` ... `47:31.48 ու` `47:31.56 Ուղղակի` `47:32.48 ենթադրենք` | certain |
| 08:23 / 38:37 / 46:42 / 57:52 | Հետևանք․ պարզ իդեալը մաքսիմալ է ... / Թեորեմ․ P պարզ ⇒ P · P̃ = O_K / Լեմմա․ ամեն իդեալ պարունակում է ... / Թեորեմ․ ամեն իդեալ միակ ձևով ... | math: (0) is a prime ideal of O_K and is not maximal; P = 0 gives P⋅P̃ = 0; the zero ideal contains no product of nonzero primes. The 01:50 lemma correctly says I ≠ 0, so the same hypothesis should carry through | `Հետևանք․ P ≠ 0 պարզ իդեալը մաքսիմալ է ...`, `Թեորեմ․ P ≠ 0 պարզ ⇒ P · P̃ = O_K`, `Լեմմա․ ամեն I ≠ 0 իդեալ պարունակում է ...`, `Թեորեմ․ ամեն I ≠ 0 իդեալ միակ ձևով ...` | `0:02:40 ... այս իդեալը վերցնել, որը կազմված Z0-ից ... ստանում ենք անվերջ` (the reason for I ≠ 0); Դաս 21 recap `0:03:31 ոչ զրո` | certain (low severity: the lecturer is also loose here) |
| 46:42 | Լեմմա․ ամեն իդեալ պարունակում է պարզ իդեալների արտադրյալ | boundary: the lemma is introduced at 46:14 ("for this we need a lemma ... a technical lemma"), and 46:42 is its restatement | **46:14** | words: `46:14.04 դրա` `46:14.24 համար` `46:14.56 պետք` `46:14.80 է` `46:14.92 մեզ` `46:15.20 մի` `46:15.32 հատ` `46:15.56 լեմա` ... `46:41.60 Լեման` `46:42.20 նրանում` | judgment |
| 01:14:25 | Իդեալների դասերի խումբ Cl(K) | consistency: Դաս 23 (and its notes: "H(K) is called Ideal Class Group") write H(K) for the same group | `Իդեալների դասերի խումբ H(K)` | Դաս 23 chapter 04:25 `Իդեալների դասերի խումբ՝ H(K) = I(K)/P(K)`; lecture 23 notes line "H(K) is called Ideal Class Group" | certain (consistency) |
| 01:13:51 | Խնդիրներ | coverage: 34 s of homework logistics (book problems 8.4-8.8) between the example and the class-group preview. Too thin for its own chapter | drop it (the text then falls under 01:10:05), or fold into the next one: `01:13:51 Խնդիրներ․ իդեալների դասերի խումբ (նախադիտում)` | `1:13:48 լավ Լավ, հիմա աս բաները մի հատ էլի պրակտիկայի ժամանակ` / `1:14:12 գրքից մի հատ նայեք ... 8 յոթը ... ութ ութը` / `1:14:24 Իմ մյուս, մյուս անգամ էլ` | judgment (low) |
| 29:29 | Կոտորակային իդեալ (fractional ideal) | style: an English gloss in parentheses. No other chapter in the series has one except Դաս 21 05:33 and Դաս 22 09:53 | `Կոտորակային իդեալ` | label | judgment (low) |

Checked and fine: lemma and proof that O_K/I is finite, N(I) = |O_K/I|, N(I) = |det(c_ij)| (and the discriminant relation used in the example: D(I) = -80 = 2²⋅(-20) gives N(I) = 2), the basis-change student question (16:40, ~1.7 min with the follow-up remark), I + J and I⋅J, Ĩ = {α ∈ K \| αI ⊆ O_K}, the P⋅P̃ = P ⇒ P̃ = O_K step, (b) ⊇ P_1⋯P_k, the uniqueness argument, and (6) = P_1² P_2 P_3 with P_1² = (2), P_2P_3 = (3). All other stamps sit within 1.5 s of their first word.

## Title

Current: `Դաս 20 | Իդեալների վերլուծումը պարզ իդեալների արտադրյալի` (56 chars). **Keep.** It names the main theorem, which the whole lecture builds toward (00:16 "կապացուցենք այդ գլխավոր թեորեմներից մեկը"). Optional: `Դաս 20 | Իդեալների միակ վերլուծումը պարզ իդեալների արտադրյալի` (61 chars), which adds the uniqueness the lecturer stresses ("միաձև", 00:34, 58:12).
