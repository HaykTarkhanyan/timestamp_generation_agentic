# Tserunyan 15-27: inline review of chapters and titles (2026-10-23)

One reader (Claude, inline, no subagents), on the raw upload timeline: every chapter of
`edited_predicted/timestamps_raw.txt` checked against the full raw `transcript.txt` and the headings
of her lecture notes (`_knowledge/tserunyan_site/lectures/`). Terms checked against the published
lectures 12-14 (կոչնչին, չնչին, Բեռնշտայնի, Լեհական). Fine boundary alignment is left to
`snap_chapters_to_captions.py` after the Studio edit; here a boundary moves only when it is off by
more than ~3 s or sits on the wrong sentence. Originals: `timestamps_raw_before_review.txt`,
`titles_before_review.txt` in each folder.

## Դաս 15 (29 chapters)

- 42:25 `B = G ∪ M` -> `B = G ⊔ M`: she writes the disjoint-union square ("disjoint union ... քառակուսի").
- Everything else holds against the transcript and the notes (Claim, Prop σ-algebra, TFAE, Remark
  continuum many, 100% lemma, Obs, Cor Cantor copy, Cor Bernstein, ∀*/∃*, Kuratowski-Ulam stated
  without proof, Cor no BM well-order). Title: option 1 kept.

## Դաս 16 (29 chapters)

- 3:29.5 -> 3:26.0: start on her turn sentence "այս նոտայի վրա ուզում եմ մի քիչ երկար մնամ" (product topology).
- Everything else holds (Cor proof via initial segments, the Claim, contradiction; Borel/BM
  transformations, rotation, rational vs irrational (α/2π), x + α/2π mod 1, baker map k-to-1 and
  not continuous but Borel, complete binary trees rooted at infinity, left shift, generic
  ergodicity, no BM 2-coloring). Title: option 1 kept.

## Դաս 17 (31 chapters)

- 22:17 "(proper colouring)" -> "(proper coloring)": one spelling in the series (Դաս 16 has "(colorings)").
- Everything else holds (irrational rotations generically ergodic via the 100% lemma and dense
  orbits, proper / Borel / BM colorings, 2-colorable iff no odd cycles with AC, Borel 3-coloring of
  the rotation graph, T_2α argument, dense-orbit equivalence, Hamming graph bipartite, E_0, H_∞ has
  no countable BM coloring via one-bit flips, G_0 and the Kechris-Solecki-Todorcevic dichotomy).
  Title: option 1 kept.

## Դաս 18 (26 chapters)

- 1:07:51 -> 1:07:22: start on her turn "ալջայից հեռու գնանք, վերադառնանք տոպոլոգիային"; the 29 s
  before the old stamp already introduce the definitions that only use open sets.
- 15:09 "Egorov" for Lusin: proposed correction note in `edited_predicted/corrections_proposed.txt`
  (see `finish_15-27.md` A2).
- Everything else holds (BM functions continuous on a comeager set, topology, coarsest / finest,
  {∅, {0}, X}, cofinite, Zariski on F^n, finer Euclidean topology, Hilbert basis theorem, nonempty
  Zariski opens meet, closure, generated topology bottom-up, prebasis, basis, Cor "prebasis iff
  finite intersections form a basis" as in her notes, basis at x). Title: option 1 kept.

## Դաս 19 (29 chapters)

- 28:14 -> 26:45: the hereditary-properties chapter starts where she says "some concepts descend
  from X to Y" (first / second countability yes, separability no); the old stamp sat 89 s late,
  at the flower example inside it.
- 22:37 -> 22:20: metrizable starts on "ժող մոռացա մի բան ասեմ այնտեղ վերևը".
- `ℝ∖ℚ`, `ℤ ∖ {±1}` -> `ℝ\ℚ`, `ℤ \ {±1}` (the series standard writes `ℝ\ℚ`, Դաս 15 `F \ M`);
  1:32:16 label + "(clopen)", which she says (the live lectures use "(clopen)" too).
- Everything else holds (first / second countable, separable, flower topology, bases criterion,
  (pre)bases in ℝ, ℝ^2, A^ℕ, ℚ zero-dimensional, T_0-T_4, metric spaces normal, cofinite T_1 not
  T_2, profinite topology Hausdorff and metrizable, Furstenberg). Title: option 1 kept.

## Դաս 20 (26 chapters)

- 51:09 "Հարց․ ինչու ոչ բոլոր կոորդինատներում" -> "ինչո՞ւ" (a question; Դաս 17 writes "Հարց․ ինչո՞ւ").
- 22:15 `2^ℕ ∖ D` -> `2^ℕ \ D` (series symbol).
- Everything else holds (continuity at a point and neighborhoods, prebasis suffices, (-∞, a) and
  (b, +∞), homeomorphism and embedding, continuous injective but not an embedding via binary
  expansions, weak topology, product of X_i and AC, finite vs infinite I, cylinders, ℝ^[0,1],
  pointwise convergence, uniform metric too fine with x^n, product topology defined via projections,
  box topology, "snakes through finitely many hoops", proof). Title: option 1 kept.

## Դաս 21 (26 chapters)

- 1:23:44 "Հարց․ որտեղ է" -> "Հարց․ որտե՞ղ է" (a question).
- Everything else holds (universal property, Hausdorff products, countable products of second
  countable / metrizable spaces with d = Σ 2^-i d_i, Polish defined topologically, G_δ subspaces
  (Alexandrov), indicator of U continuous iff clopen, Urysohn's lemma via dyadic layers, f = inf,
  the density question, the continuity proof). Her notes also state a proposition on uncountable
  products that she did not reach in the recording: no chapter for it. Title: option 1 kept.

## Դաս 22 (28 chapters)

- No change beyond the three "Ինչու՞" -> "Ինչո՞ւ" glossary fixes (A4). Everything holds (Urysohn as
  an extension, Tietze for bounded f via f_n with ranges [0, 2^(n-1)/3^n], the 2/3 shrinking, the
  partial-sums correction, unbounded Tietze with g = f/(1 + |f|), the ±1 problem, solution 1 via
  ℝ̄ (she says "two point compactification"), solution 2 via Urysohn, open ranges kept, compactness:
  open covers, closed sets with the finite intersection property, the equivalence). Students'
  names spoken at the start (raw 1:11-1:50) and the participant list at the end are inside
  ticked cuts 1 and 8. Title: option 1 kept.

## Դաս 23 (27 chapters)

- 1:25:41 "T1" -> "T_1" (series notation, Դաս 19).
- Everything else holds (basic open covers suffice via refinement, finite topologies, Zariski
  question, ℝ and unbounded compatible metrics not compact, ℕ^ℕ, 2^ℕ compact with two proofs:
  maximal words + König's lemma via heavy vertices and pigeonhole, heavy words; [a, b] by halving,
  closed subsets of compact, relative topology subtlety, compact not closed example, compact closed
  in Hausdorff, non-closed sets in ℝ, the T_1 question). Title: option 1 kept.

## Դաս 24 (28 chapters)

- 26:20 "Աղավնաբնի սկզբունք" -> "Դիրիխլեի սկզբունք (pigeonhole principle)", 1:13:48 "աղավնաբնի" ->
  "Դիրիխլեի": the glossary term (pigeonhole principle,Դիրիխլեի սկզբունք).
- 1:19:13 "ենթահաջորդականությունը կոշի է" -> "Կոշիի է" (glossary: Կոշիի հաջորդականություն).
- Everything else holds (non-Hausdorff examples are nonmetrizable, ℝ^[0,1] Hausdorff, uncountable
  products of nontrivial spaces not first countable via the pigeonhole on cylinders, continuous
  images of compacts, continuous injection from compact to Hausdorff is an embedding, sequential
  compactness, Heine-Borel, totally bounded and ε-nets, the TFAE, (2) ⇒ (3), (3) ⇒ (2) via the
  diagonal subsequence, (1) ⇒ (2), the (2), (3) ⇒ (1) teaser on [0, 1]). Title: option 1 kept.

## Դաս 25 (28 chapters)

- 1:28:52 "Հարց․ 1-ին հաշվելիում կոմպակտ ⇒ հաջորդականորեն կոմպակտ" -> "Հարց․ 1-ին հաշվելիում
  կոմպակտից հետևո՞ւմ է հաջորդական կոմպակտությունը": a student's question she leaves open (nets
  next time), not a statement.
- Everything else holds (complete + totally bounded ⇒ compact via refining covers and pigeonhole,
  closed and bounded in ℝ^n, order topology, ω_1 not compact (not even Lindelöf) but sequentially
  compact and first countable, the supremum question, Tychonoff ⇔ AC, 10^[0,1] compact but not
  sequentially compact via decimal digits). Title: option 1 kept.

## Դաս 26 (29 chapters)

- One vocabulary for the series (Դաս 18-20, 23 and the glossary: basis = բազիս, cylinder = գլան):
  4:30 "շրջակայքերի բազա" -> "բազիս"; 44:33 "բազային" -> "բազիսային"; 48:01 "ցիլինդրներով" ->
  "գլաններով"; 56:58 "նախաբազան" -> "նախաբազիսը"; 1:10:59 "ոչ նախաբազային" -> "ոչ նախաբազիսային";
  title option 3 "նախաբազային" -> "նախաբազիսային".
- 51:16 "Նախաբազա (subbasis)" -> "Նախաբազիս (prebasis, subbasis)": she says she calls it prebasis
  and that the literature (and Google) say subbasis; both terms help a search.
- Everything else holds (first countable properties (a)-(d), Tychonoff, X × Y via the students'
  rectangles and fibers, why the first attempt fails, the tube argument, finite products by
  induction, refinement and coarsening, basic covers suffice, Alexander's lemma via a maximally
  coarse cover from Zorn, [0, 1] by Alexander, the Tychonoff proof). Title: option 1 kept.

## Դաս 27 (29 -> 30 chapters)

- New chapter 16:48 "Օրինակ․ ուղղորդված բազմությունների արտադրյալ A × B": she calls it an important
  example ("ս կարևոր օրինակ է") and builds the subnet on it at 1:06:29 (neighborhoods × A); it sat
  unlabeled inside the neighborhood-basis example. Gaps 163 s and 128 s.
- "շրջակայքերի բազա" -> "բազիս" at 14:04, 28:53, 30:33 (series term); 1:19:01 "Հարց․ ինչու" -> "ինչո՞ւ".
- Note for the user (cut plan, not chapters): ticked cut 8 (1:37:23-1:41:42, 4.3 min) is her
  farewell to the class: thanks, an invitation to stay in touch, congratulations to the TA Aram on
  his best-student award, thanks to Aram. Untick it, or keep part, if the course should end with her
  closing words.
- Everything else holds (directed sets without antisymmetry, finite subsets, reverse inclusion,
  nets, eventually / frequently, convergence, closure and continuity via nets, cluster points,
  subnets and why the naive definition fails, cluster point ⇔ convergent subnet with the AC
  construction, compact ⇔ every net has a convergent subnet ⇔ a cluster point). Title: option 1 kept.
