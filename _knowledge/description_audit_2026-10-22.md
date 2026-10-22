# Description audit, both channels (2026-10-22): read every description line by line

User: "u do in line, check all". After the glossary scan (word level, `glossary_scan_channels.py`) and the
read of all 654 titles, read the remaining descriptions (chapter lines + summaries) for errors of meaning:
wrong math, wrong statements, wrong terms, typos the word check misses. Papikian (21 videos) was read
earlier the same day and is skipped.

- Dump (session scratchpad, rebuilt by `audit_dump.py`): `audit/desc_dump.txt` = 614 public/unlisted
  videos, 8,427 kept lines (boilerplate dropped: URLs, hashtags, lines repeated in 3+ descriptions),
  9,041 lines in all, math courses first; `audit/desc_full.json` = full texts.
- Method: read in chunks; each suspect goes below with video id, the line, the problem; certain ones
  are fixed (backup JSON first, exact replacement, read back), judgment calls are listed for the user.
- Backups of everything changed by this audit: `_knowledge/descriptions_before_audit_2026-10-22.json`.

## Progress (dump line ranges read)

- [x] 1-3600 (complex analysis, analysis 1-4, functional analysis, linear algebra, metric spaces, ODE, Մաթֆիզ, group theory)
- [x] 3601-5000
- [x] 5001-9041 (rest of ML-math, Claude Code workshop, Libraries, Python, ML) - all 614 videos read

## Findings

| # | Video | Line | Problem | Status |
|---|---|---|---|---|
| 1 | Mp5ByuSYRSg Կոմպլեքս 10 | 27:57 Անալիտիկ + սահմանափակ = հաստատուն | Liouville needs analytic on all of ℂ (entire) | verify |
| 2 | Mp5ByuSYRSg Կոմպլեքս 10 | 11:44 ∫φ(ξ) / (ξ-z)^n dz | integration variable is ξ: dξ | fix |
| 3 | DqUPATmU_9s Կոմպլեքս 24 | 12:38 բոլոր կարգի ածանցյալներն ինքնըստինքյան են | label incomplete (…զուգամիտում են?) | verify |
| 4 | TVBNxru2ViI Կոմպլեքս 7 | 36:50 ∮(z-a)^n dz = 0, երբ n≠1 | n ≠ -1 (next chapter is n = -1) | fix |
| 5 | zs24P_p5i2k Կոմպլեքս 9 | 06:00 ∳1/(z-a) dz = 2πi կամայական γ փակ կորով | false as stated (= 2πi·n(γ,a)) | verify |
| 6 | QaLdQd1Yk4s Անալիզ 1 (ԿՎՏԳ) 16 | 43:22 ((1+x)^α - 1)/x → 1 | limit is α | fix |
| 7 | AksWeYUV_IE Անալիզ 1 (ԿՎՏԳ) 2 | 23:07 1 + 2 + 2^1 + 2^2 + ... + 2^n = 2^(n+1) - 1 | 2 counted twice | fix |
| 8 | AksWeYUV_IE / gDsag7H4M6o Անալիզ 1 (ԿՎՏԳ) 2, 3 | 15:13 0.110100... vs 00:00 0.101001000... | same exercise, two numbers | verify |
| 9 | EzawDGD3C_I Անալիզ 2 (ԿՎՏԳ) 1 | 21:33 դիֆերենցելի f-ի խզման կետերը 2-րդ սեռի են | about f' (f is continuous) | fix |
| 10 | KcNutUPEREg Անալիզ 1 (ԿՎՏԳ) 4 | 18:05 վերին/ստորին եզրերից մեծագույն/փոքրագույնը | pairing reversed (sup = least upper bound) | fix |
| 11 | PyL9O4pqIV8 Անալիզ 3 11 | "16:35 Թեորեմ 3…" twice, 2nd after 26:15 | duplicate, out of order: can break YouTube chapters | fix |
| 12 | 3V1f_mO-rtw Անալիզ 2 (ԿՎՏԳ) 3 | 17:37 x^2-ու վերլուծությունը | typo: x^2-ի | fix |
| 13 | bpz1VxfsE9U Անալիզ 2 (ԿՎՏԳ) 5 | 37:12 Ապացույց․ f''≥0 դեպքը | likely f''≠0 / f''＞0 (next: f''=0) | verify |
| 14 | rRJYD0xDXGY Անալիզ 4 4 | 11:43 Հատկություն 2․ |f|≤M ⇒ ∫fdg ≤ M | standard: |∫fdg| ≤ M·V(g) | verify |
| 15 | LxRMQf0jkEE Անալիզ 4 (ԿՎՏԳ) 10 | 11:51 Π (1+a_n) զուգամետ ⇔ ∑ a_n զուգամետ | needs a_n ≥ 0 | verify |
| 16 | uLs66q1-lPA Գծային հանրահաշիվ 11.1 | "26:08 Գծորեն անկախ մատրիցներ" twice, 2nd after 27:15 | duplicate, out of order | fix |
| 17 | 0HvOnlHjMCA Գծային հանրահաշիվ 11.2-բ | 42:19 dim(V) հատ վեկտորները կազմում են բազիս | needs "անկախ" | fix |
| 18 | xNX_Vq_Vtow Ֆունկցիոնալ անալիզ 4 | "44:23 Քայլ 2․ ρ˜" + newline "-ի կառուցումը" | label split by a line break | fix |
| 19 | FMAC50oo6sI Ֆունկցիոնալ անալիզ 22 | 08:09 BL(X, Y)-ը լրիվությունը | grammar: -ի | fix |
| 20 | A4gEdKaoh9E Դիֆ. հավ. (ԿՎՏԳ) 5 | "37:22 Նախորդ օրինակը ՌԿ մեթոդով" after 58:54 | out of order + duplicate time: real time needed | verify |
| 21 | xWszR-0HXxU Դիֆ. հավ. (ԿՎՏԳ) 7 | 27:56 y'' + 2y' + 2 = 0 | 2y (complex-roots case) | fix |
| 22 | T9m_X49Zb3I, Ti-bMRQHckk Մաթֆիզ 4, 5 | "վերահրապարկվել … տարբերուկում" | typos: վերահրապարակվել, տարբերակում | fix |
| 23 | bBAkdRssPj8 Մաթֆիզ 5 | "(BRIGHTNESS PROBLEMS)" old version, public | re-upload Ti-bMRQHckk exists; visibility is the user's | user |

User mid-audit (21:5x): "those aren't edited by us" + "only fix the safe ones". Most of the math courses
(analysis 1-4, functional analysis, ODE, linear algebra, group theory, Մաթֆիզ, random processes, most ML-math)
were made by others (no output/ folder in this repo); ours: the 53 ML videos, Arnak, 6 complex analysis,
2 information theory, 2 metric spaces, a few one-offs. So: only safe fixes (typos, unambiguous slips, broken
chapter order); everything that needs judgment is listed for the user.

**Batch 1 pushed 21:5x, read back: all 16 match** (`audit_fix_batch1.py`; backup
`_knowledge/descriptions_before_audit_2026-10-22.json`): #2, #4, #6, #7, #9, #10, #11, #12, #16, #17, #18
(the split was a stray carriage return after ρ˜), #19, #20 (captions: the RK redo of the example starts
at 1:00:41), #21, #22 (both videos). Left for the user: #1, #3, #5, #8, #13, #14, #15, #23.
| 24 | QMvIy2auywg Բազմաչափ վիճ. 3 (ours) | 35:28 X1 ⫫ X2 գաուսյան ⇒ X1+X2 և X1-X2 անկախ | needs equal variances | verify |
| 25 | QMvIy2auywg, _P_HhQhJalQ Բազմաչափ վիճ. 3, 4 (ours) | "չկոռելացված" vs the series' "կորելյացված" (Դաս 10-13) | consistency with the lecturer's term | user |
| 26 | o_ldYAd8c70 LaTeX-ի ներածություն | "58:07 Սլայդեր (beamer)" and "58:07 Գծապատկերներ (tikz)" | same time twice: breaks chapters; real time needed | verify |
| 27 | nU3fzO94lBw Բնական թվե՞րն… | 06:22 Քայլ 2․ |ℕ| = |[0, 1]| | before the diagonal argument: "suppose" or ≠? | verify |
| 28 | VrqiYwPn5Ps Թվերի տեսություն, Տեսական N3 | ֆունցկիա | typo: ֆունկցիա | fix |
| 29 | ymZ9DpOsC7A Թվերի տեսություն, Գործնական N3 | խնդրիների ֆայլը | typo: խնդիրների | fix |
| 30 | 9pTflZVOzLc Վիճակագրության մոլորությունները | «Վիճակագրության մոլորություները» | typo: մոլորությունները | fix |
| 31 | 5VEnDdm8RZo Հանրահաշիվ (one-off) | "с) Սեփական արժեքներ" | Cyrillic с → c | fix |
| 32 | jfhySW3I46I Հանրահաշիվ (one-off) | "C-ի hակադարձ" | Latin h → հ | fix |
| 33 | fxYxoHIz-P0 Գործնական 21 ML-math | "(Gemini-ն ա սարքել, ես էլ չեմ ստուգել)" in a public description | user's own note | user |
| 34 | ZKdCO6o3i4E Գործնական 9 | "28։45" (Armenian ։) and "Ի՞նչպես" | not a timestamp → 28:45; Ինչպե՞ս | fix |
| 35 | H8M6p-uSxCM Գործնական 10 | մուտլիմոդալությունը | typo | fix |
| 36 | 8W9iOV7IVnA Գործնական 22 | գործիքներիև | missing space | fix |
| 37 | hF2jwMKdmE0 Գործնական 12 | BGFS (x2) | BFGS | fix |
| 38 | bLQJIKmkqmE Գործնական 2 | "10(с)" Cyrillic; summary numbered 5. twice | c; 6. | fix |
| 39 | YhT1p1sGFp8 Գործնական 18 | Երկրաչափակ, բաշում, Բայեսյի, համապատասխացնենք, Պուասանողյան, կակնալենք | typos | fix |
| 40 | D9JIZXNzios Գործնական 19 | Անակնալի; "գործնականից տստ մաթ" | Անակնկալի; ըստ | fix |
| 41 | I4EMKTQbVno Գործնական 4 | "P^(-1) hակադարձը" (Latin h); Համիլոն-Քելիի | հակադարձը; Համիլտոն-Քելիի | fix |
| 42 | XFF03oPjAyE Գործնական 8 | գրադինտն է | գրադիենտն է | fix |
| 43 | OHXH7zn65zU ML-math Դաս 10 | 01:04:11 Թեյլորը բազմանդամը | Թեյլորի բազմանդամը | fix |
| 44 | tFiDNbpZNFw ML-math Դաս 12 | գրադիենտի որպես ամենաարագ աճի ուղղություն | գրադիենտը որպես | fix |
| 45 | W9ZncUE8Fno ML-math Դաս 18 | "BFGS ... երկրորդ կարգի սիմետրիկ մատրից"; "31:02 Գաուս-Նյուտոն՝ քառակուսային ֆունկցիաների համար" | BFGS adds a rank-2 update; Gauss-Newton is for sums of squares (least squares) | user |
| 46 | 5FdGFaG0pXg ML-math Դաս 31 | "կոռելացված լինելը բավարար չէ ասելու համար, որ ... փոխկապակցված են" | correlated already means associated; the point is causation (պատճառահետևանքային կապ) | user |
| 47 | Ye0ZsTDnPx4 ML-math Դաս 41 | "Gemini-ն ա սարքել, չեմ ուղղել դեռ՝" + "(sufficiency, consistency) գործում են ավտոմատ կերպով" | same kind as #33; the claim is an overstatement | user |
| 48 | DDdzHnQsyrA, xQKwAcaM410 ML-math Դաս 42, 43 | likelihood = "Հավանականության ֆունկցիա"; consistency = "համապատասխանություն" | glossary: ճշմարտանմանություն, ունակություն (Դաս 41 uses ունակություն) | user |
| 49 | PYHNsndAnXE Դաս 47, deBUJ8pMomU Գործնական 24 | titles "Հիփոթեզների", chapters "Հիպոթեզ" | title spelling | user |
| 50 | 1KB7Riu_p_o ML-math Դաս 49 (ours) | "0:53:14 Հակընթացիկ հավանականություններ"; "Ծաղկաքաղ և գերրիմանդերինգ" | not a word: the transcript there is the birthday paradox (հակաինտուիտիվ?); gerrymandering spelling unusual | verify |
| 51 | oU0uip1w9HM ML-math Դաս 52 (ours) | "28:13 Հեռավորությունները զուգակցվում են" | զուգակցվել = combine; meant "become nearly equal" | user |
| 52 | F4iUxmfeeBY ML-math Դաս 9 | "31:28 Փակ հատվածի վրա էքստրեմում միշտ կա" | needs a continuous function (Weierstrass) | verify |
| 53 | Public to-do notes | r44t7RPPm7U "ToDo - Plotly-ի թայմսեթեմփերը..."; qaw4HsDa1pw "(ToDo - անուններով նշել...)"; 2BtFmBMSnsA first 2 lines are an edit to-do list; -HC6RJ6cNT0 "Montag - ToDo"; ZOOWqchxETU "[Python-Dotenv վիդեո (ToDo)]()" (that video exists: tqR3DhSkNlQ); wgw9eexila0 "[վերլուծություն (ToDo)](ToDo)" (exists: 3JJDA0xXvSE) | user's notes; two could link the existing videos | user |
| 54 | tvZzjcaGs1U Python [16], WpqHzsHwqvA Python [14] | chapters every 5:00 exactly (0:05:00 ... 1:20:00), generic labels | look generated, not checked against the video | verify |
| 55 | lwQdNzTKiFI [2023] [11] | title "Բաժիններ 3, 5, 7" | content is sections 1, 11, 15, 17 (title copied from [05]) | user |
| 56 | Iu7GGVvrsbs [2023] [20] | "52:50 isinstance, issubset" | probably issubclass (class topic) | verify |
| 57 | Fwk1PyLotOg [2023] [02] | "2.1 հանրահաշվական պրոգրեսիա" | arithmetic progression = թվաբանական (the 2025 version says so) | user |
| 58 | BwL0nWJLFPg ML 13 (ours) | "100 ընդդեմ 10 դոլարի՝ ստացվում ա ~0.08" | C_FP/(C_FP+C_FN) = 10/110 ≈ 0.09; the lecture says "ստացանք 0.09, տեսական 0.08" | verify |
| 59 | Gx885YnVLis, GmjPLKl5UPA ML 27, 28 (ours) | "չափականության անեծք" | glossary and ML-math Դաս 52: չափողականություն | user |
| 60 | KdtXO7Pj9DI Claude Code workshop (ours) | "OpenAI-ի մոտ 10 000 ագենտը աշխատել են" | "10 000 ագենտ"; local corrections.txt is mid-edit, so not touched | user |
| 61 | 3V1f_mO-rtw (batch 1, #12) | "x^2-ու" -> "x^2-ի" | second thought: "-ու" matches the spoken "x քառակուսու", so the change was not needed; both are acceptable | user (revert?) |

**Batch 2 (22:4x)**: `audit_fix_batch2.py` (scratchpad), 80 videos, 104 exact replacements + a sweep
"Ինչու՞" -> "Ինչո՞ւ" (13 descriptions) + one joined label; backup in the same
`_knowledge/descriptions_before_audit_2026-10-22.json`. Fixes #28-#44 above plus, from lines 5001-9041:
typos (backtracing, գրադինետը, Optimazation, ըստ բաշխան, Էմպրիկի x3, Բեզելի, մետաղադրակ, մտապած, մոտեցմով,
թարմանություններ, հրամանակ, տռանսրիպտը, պրոկետը, ցանկցած x2, գրաֆիկիների, փոխարիներում, վերծություն, Stremlit,
պռոֆեսինոլ, աշախտող, գրադարն, բարձացնի, բավարավում, կանցելը, օգվելուց, պատելու, Աշխատցնել, enviroment, Flaks,
Constrains, Tuning off, մեկնաբանութուններ, Սկիբզ, աշխտաել, պոլինդրոմ, Excetpion, ագրգացնող ֆունցկիաներ, attibutes,
Itetrators, հայտաբերում, Կազմակերպական, ռեգուլարիզացիա, sarup, սարթափի, կարանանք, դենդոգրամ x3, կրկելի,
"դեն կլինիչ" -> "իսկ" (transcript: the tree model is not hurt), "հաշվարկային եքա բեռ" -> "հաշվարկային բեռ");
mixed scripts (Latin O in Օրինակ, Cyrillic С in Collections); math (p/1-p -> p/(1-p)); "nq" -> "ne",
"Python Enhancement Protocol" -> "Proposal"; broken links ("https:// colab", "https:// profound"); list numbering
(_C3sP0X7U_E 2,2,3 -> 2,3,4; bLQJIKmkqmE 5,5 -> 5,6); PYHNsndAnXE "P value ի" -> "P-value-ի", $H_0$ -> H₀;
chapter order: 7XsIyFTImwk "01:02:23 Սորտավորում" -> 01:12:23 (no captions; video frames: still element removal at
1:12:20, sorting cell on screen at 1:12:25), 2GMufITVgt4 "00:23:20 Մինի հայտարարություն 2" -> 01:23:20 (captions
1:23:22 "մի հատ էլ մինի հայտարարություն"), 6SgQl7BqeZ0 duplicate out-of-order "01:08:35 Property decorator" removed,
pI6pgobJ4yo label split by a line break joined.
**The YouTube API daily quota ran out after 20 of the 80** (403 quotaExceeded). Pushed and read back: the 16 of
#28-#44 plus UjGD31i8Ji4, JsSnSHZtG_o, 4exAPAxCXCw, 7Isz4vXSj8U. **Pending 60**, quota resets at 09:00 Munich time:
rerun `python <scratchpad>/audit_fix_batch2.py push` then `check` (push skips videos that already match and
refuses any whose live text differs from both the backup and the plan). If the scratchpad is gone, the planned
texts are in `_knowledge/description_audit_2026-10-22_batch2_pending.json` ({id: channel, title, description}).
Denylist: added ինչու՞, ֆունցկիա, գրադինետ, գրադինտ, էմպրիկ, դենդոգրամ.
Local copies synced (scratchpad `sync_local.py`): the same replacements went into 51 repo files, i.e. each
video's description.txt / abstract.txt / timestamps.txt (folder or edited/) and the matching final/MLnn.txt, so a
later push from the repo does not bring the typos back. Transcripts, old _vN versions and edited_predicted/
were left alone. Offline denylist check of all descriptions with batch 2 applied: 0 DENY.

**Local vs live, all our videos (23:0x, offline: snapshot + batch-2 plan; Papikian not in the snapshot)**:
94 local description files match live, 26 differ. Typo-level gaps fixed locally (`sync_small.py`, 13 files):
Գաոսյան (ML-math 51, 52), վայրեջք (ML 1 abstract/timestamps), Սյուրեկտ (Complex 23 draft), "ICE pl-եր" (ML 23);
the denylist over all 270 local description/abstract/timestamps/final files now gives 0 DENY. Still different,
not synced (whole-file, the user's call): ML 18-20 live have a "Նշում՝ ... bootstrapping-ի փոխարեն boosting եմ
ասում" note missing locally (output + final/ML18-20); ML 2-10 live have the materials URL (or "TODO") where local
has "TODO: paste materials URL here", and ML 6 live relabelled 12:02; ML-math 51, 52 live use a newer template
(materials, Telegram, hashtags); Complex analysis 20-25 local description.txt are older drafts (live chapters were
redone); ML 1 local says "(Opus 4.8)" vs live "(Opus 4.7)", which looks like a local pending edit, left alone.
Papikian 16-23 and the rest of the playlist: compare after the quota reset.
