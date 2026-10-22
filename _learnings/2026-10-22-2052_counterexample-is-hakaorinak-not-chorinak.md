# Counterexample is "հակաօրինակ", never "չօրինակ"

**Symptom:** chapter labels on the umath channel used "Չօրինակ․ ..." and "Օրինակներ և չօրինակներ" for
counterexamples / non-examples. The user caught it after the Papikian 16-23 push: "չօրինակ means
antiexamples? if so thats wrong, correct is հակաօրինակ".

**Cause:** a coined word (by analogy with "չբերվող") that slipped into the Papikian series standard as a
step word (`_knowledge/papikian_ant/standard.md` listed `Չօրինակ․ ...`) and from there into new labels.
The glossary had the right term all along: `glossary.csv` line 223, `counterexample,հակաօրինակ,`.
Neither the Claude nor the Codex review flagged it.

**Consequences / what was fixed (2026-10-22 20:49-20:52):** a scan of every title and description on both
channels (umath 476 uploads, metric 247), all 44 comments the channels wrote on their own videos, and the
10 Sevak chapter comments found it in 6 live descriptions: Papikian Դաս 5 (2), 13 (2), 17; Tserunyan
metric Դաս 12; Mikaelian linear algebra Դաս 5.1. All replaced with "հակաօրինակ" (case kept), read back,
re-scan 0 hits. The Sevak comments never had it. Backups of the changed descriptions:
`_knowledge/papikian_ant/descriptions_before_drive_2026-10-22.json` (Papikian) and
`_knowledge/descriptions_before_hakaorinak_2026-10-22.json` (the other three).

Also changed on the user's question (20:54): Metric Academy `kh10WTvYTR0` (Մաթեմատիկա ML-ի համար, Դաս 2)
had "օրինակներ և ոչ օրինակներ" in its summary, the same "examples and non-examples" sense; now
"օրինակներ և հակաօրինակներ", the established Armenian pair. Old text in the same backup JSON. Note: the
first read-back right after the update still returned the old text; a second read a few seconds later
matched, so read back again before calling a mismatch.

**Check before posting labels:** look up step words in the glossary, not only content terms.

## Follow-up: full glossary cross-check (2026-10-22 21:00, user: "cross ref with glossary, maybe there are other mistakes as well")

Read all 528 chapter labels of the Papikian playlist and the 232 labels of the 10 Sevak comments
against `glossary.csv`. The glossary agrees with almost every term (coset, CRT, conjugacy class,
Jordan normal form, multiple root, residue/remainder, torsion-free, splitting field, UFD, PID,
row echelon, augmented, invertible, transition matrix, Hermitian, composition, span, ...).
Fixed (each confirmed on the lecture's captions; old text in
`_knowledge/papikian_ant/descriptions_before_label_fixes_2026-10-22.json`; read back: match):

- Դաս 9 02:50 `gcd(f, Df)=1` -> `≠ 1` (multiple root; the label had copied the lecturer's slip, 3:20)
- Դաս 9 18:58 `չբերվող արտադրիչները բիյեկտիվ են` -> `իզոմորֆիզմը պահպանում է չբերվող արտադրիչները`
- Դաս 10 01:16:42 typo `կոմումատիվ` -> `կոմուտատիվ`
- Դաս 11-12 01:17:51 `α հանրահաշվական ⇒ m_α,ℚ ∈ ℤ[i]` -> `α ամբողջ ⇒ m_α,ℚ ∈ ℤ[x]` (1:17:50-1:19:45)
- Դաս 13 08:50 `ազատ և առանց ոլորման մասերի` -> `ազատ և ոլորման մասերի` (M = free ⊕ Tor(M), 9:11)
- Դաս 8 `ℚ(ξ_n)` -> `ℚ(ζ_n)` (the rest of the lecture's labels use ζ)
- Sevak L9 comment `բիեկցիա` -> `բիյեկցիա` (glossary spelling, `bijective,բիյեկտիվ`); local
  `comment.txt` / `chapters.txt` too.

Most of these were not glossary issues but math or wording slips that a slow read caught; the
glossary pass is worth doing together with a plain read of every label.

Open (no glossary entry, the user decides; then add the terms to the glossary): Դաս 1 "բաժանումով
օղակներ" (division ring; "մարմին"?), Դաս 14 "պրիմար բաժանարարներ -> ինվարիանտ ֆակտորներ"
("տարրական բաժանարարներ -> ինվարիանտ արտադրիչներ"?), Դաս 14 "Համիլտոն-Քեյլիի" ("Համիլտոն-Կելիի"?),
Eisenstein (Դաս 7 "Այզընշտայնի (Էյզենշտեյնի)" vs Դաս 22 "Այզենշտայնի"), Դաս 5 title "Z[i]" (ℤ[i]?).

## Follow-up 2: both channels, and the check in the workflow (2026-10-22 21:10-21:35)

- New `.claude/skills/youtube-timestamps/scripts/glossary_check.py` (DENY / NEAR / ENG, see its
  docstring) + `assets/glossary_denylist.csv`; SKILL.md stage 3 now requires it before publishing,
  and every corrected term goes into the denylist. `scripts/non_essential/glossary_scan_channels.py`
  runs it over everything published (664 videos and comments, ~100 s).
- First version took 5+ minutes on 26 files: ~1000 English-term regexes were recompiled per line
  (Python's re cache holds 512) and every word was compared with the whole vocabulary. Precompiling
  and bucketing by the first two letters made it ~1 s. NEAR was noisy on ordinary endings
  (տարրերն, բաժանվում) until a word sharing all but the last 3 letters of a glossary word counted as fine.
- Fixed from the scan (backups `_knowledge/descriptions_before_typo_fixes_2026-10-22.json`): ածացյալ,
  Պրոեկցիա/պրոեկցիայի (n211, private), սկզունք, հավանականույան, Գաոսյան (Դաս 51 ×2, Դաս 52 ×2),
  մատսպասումը, գրադիենտի վայրեջք (×2), սյուրեկտիվ.
- Fixed from reading all 654 titles (backup `_knowledge/titles_before_typo_fixes_2026-10-22.json`):
  Դաս 52 "Չափողականության անեղծը" -> "անեծքը" (its thumbnail was already right), Դաս 19 "արտահատումն"
  -> "արտահայտումն", "Multi-Start Օptimization" (Armenian Օ) -> "Optimization", "(Մինիմալ )",
  Դաս 49 "խափել" -> "խաբել" (its description says խաբել), "feature enginnering", "Scrapping" ->
  "Scraping", Դաս 44 "ռեգուլարիզացիայի" -> "ռեգուլյարիզացիայի" (its description uses յ).
  The word checker missed most title typos (short words, English words): a plain read of titles found them.
- Left for the user: Ֆուրիեի (math analysis 3/4, 8 videos, 4 titles) vs glossary Ֆուրյեի (Մաթֆիզ titles
  use Ֆուրյե); կորելացիա (~11 ML videos) vs glossary կոռելացիա (ML-math titles use կոռելացիա); Das 15
  "բազմանդամների օղակ" vs glossary "բազմանդամային օղակ"; "ազատ ցիկլերի" (permutations exercise
  2-0d6I0uTUE; glossary disjoint = չհատվող); [41] "Նեյրոնից ցանցեր" intended?; public title
  "(BRIGHTNESS PROBLEMS) Դաս 5 | Ֆուրյեի մեթոդի…" (bBAkdRssPj8) next to a public Ti-bMRQHckk of the same
  lesson; [08] Hyperparameter tuning lacks the course suffix; 385 ENG findings, mostly the ML course's
  deliberate English. Not done yet: a plain read of the ~7,450 chapter labels outside Papikian.
