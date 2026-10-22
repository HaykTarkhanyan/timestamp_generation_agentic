# Դաս 22: independent review of chapters and title (Claude, 2026-10-22)

**Verdict:** good. The math in all labels is correct. One theorem chapter starts on the middle of its own statement (48:44, 21 s late), and a 2.3-min student exchange has no chapter of its own. The rest are notation and consistency details. 27 chapters for 75 min is within the standard.

Word times come from `txvgnlhu78E.hy.vtt`.

## Chapter findings (most severe first)

| time | current label | problem | suggested fix | evidence | certainty |
|---|---|---|---|---|---|
| 48:44 | Թեորեմ․ Spl(f)-ը տրվում է կոնգրուենցիաներով ⇔ Gal(f)-ը աբելյան է | boundary: the stamp is mid-statement ("Մենք կարող ենք այս PL-ը նկարագրել որպես կոնգրուենցիա ..."). The step starts at 48:23 and the theorem at 48:36. The chapter is only 39 s long, so 21 s matters | **48:23** (or 48:36) | words: `48:23.48 Հիմա` `48:25.80 այսինքն` `48:26.24 մենք` `48:26.68 ուզում` `48:26.92 էինք` `48:27.52 հասկանալ,` ... `48:36.28 Պարզվում` `48:36.68 է,` `48:37.08 այս` `48:37.32 SPL-ը` `48:37.92 կապված` ...; line `0:48:44 Մենք կարող ենք այս PL-ը նկարագրել որպես` | certain |
| 38:48 | (inside 36:21 "Բարձր աստիճանի բազմանդամներ․ Φ_q ցիկլոտոմիկ բազմանդամը") | coverage: a 2.3-min student exchange (other quadratics reduce to x² - disc; why monic; Spl depends on O_K, not on f) sits inside the cyclotomic chapter | add **38:48** `Հարց․ ընդհանուր քառակուսային բազմանդամներ, ինչո՞ւ մոնիկ` | `0:38:48 իսկ ըհը եթե մեր բազմդամը ինչ-որ քառակուսային բազմամ է, բայց x քառակուսի մինուս q չի` / `0:39:14 Իսկ մենք մենակ մոնիկներն էինք նայում` / `0:39:26 ... կապված է օկայի հետ` / `0:41:11 օքեյ հիմա ցիկլատոմիկների համար` | judgment |
| 14:14 | Թեորեմ․ f-ը p-Այզենշտայնի է ⇒ ⟨p⟩ = Pⁿ | notation/consistency: chapter 00:00 of this lecture writes pO_K, and Դաս 20-21 write (p), (6), (2, 1+√-5). ⟨p⟩ appears only here and in Դաս 23. The notes write "(p) = pO_K" and "(p) = Pⁿ" | `Թեորեմ․ f-ը p-Էյզենշտեյնի է ⇒ pO_K = P^n` | notes, lecture 22: "Then (p) = pO_K is a prime ideal", "(p) = Pⁿ for some prime ideal"; chapter 00:00 label | certain (low) |
| 14:14 | (same) | Armenian (spelling, not sure): "Այզենշտայն" follows the German pronunciation. Armenian textbooks usually write the criterion as "Էյզենշտեյնի հայտանիշ". I could not check this offline | `p-Էյզենշտեյնի` | label | judgment (low, unverified) |
| 09:53 + 10:41 | Հարց․ բազմանդամի աստիճանը որպես վալուացիա (valuation) / Գլոբալ դաշտեր․ ... | coverage/style: 09:53 is a 48-s chapter, and the answer continues into 10:41 (function fields, global fields, Ostrowski for them, ending with "Ռուբեն, ճիշտ ա"). It also carries an English gloss | merge: `09:53 Հարց․ աստիճանը որպես վալուացիա, գլոբալ դաշտեր` (drop 10:41), or keep both but drop "(valuation)" | `0:09:53 Մեկ էլ ինձ միշտ հետաքրքրել ա ինչ-որ բազմաթամի աստիճան ...` / `0:10:38 Հիմա ըըը թվերի տեսության մեջ ...` / `0:13:29 այսինքն ինչ որ դու ասում ես Ռուբեն ճիշտ ա` | judgment (low) |
| 56:33 | Օրինակ․ Spl(x² - 17)-ի խտությունը 1/2 է | label: the chapter also gives the cyclotomic case, density 1/(q-1), which the Chebotarev chapter then compares against | `Օրինակներ․ Spl(x² - 17)-ի խտությունը 1/2, Spl(Φ_q)-ինը՝ 1/(q-1)` | `0:58:13 ցիկատոմիկի համար մենք ուզում ենք P-ն լինի մեկ մոդուլը Q` / `0:58:25 1Q-1 վրա` | judgment (low) |

Checked and fine: ord_p properties, the Ostrowski exercise (the lecturer names it at 08:28 and the notes call it "Ostrowski's theorem"), Eisenstein ⇒ total ramification and its proof, Dedekind with ind(θ), the x⁴ - 10x² + 1 example inside the 23:10 Q&A (~3.2 min, correct as a chapter), Spl(f), Legendre symbol, quadratic reciprocity, q = 17 and q = 11, mod q / 4q (and mod 8 for 2), p ∈ Spl(Φ_q) ⇔ p ≡ 1 mod q, x³ - 2 ↔ p = a² + 27b², K_f ⊆ K_g ⇔ Spl(g) ⊆* Spl(f), natural density, Chebotarev (1925 matches the notes "Chebotarev Density (1925)"), Dirichlet as corollary, conjugacy-class form, Frobenius, Langlands. Every other stamp is within 1.5 s of its first word.

## Title

Current: `Դաս 22 | Փոխադարձության օրենքներ։ Չեբոտարյովի խտության թեորեմ` (61 chars). **Keep.** From 26:24 to the end (~49 of 75 min) the lecture follows "what is a reciprocity law" and closes with Chebotarev, Frobenius and Langlands. The first 26 min (ord_p, Eisenstein, Dedekind) set this up. Candidate 4 ("Քառակուսային փոխադարձություն ...") is narrower, since the lecture goes well beyond the quadratic case.
