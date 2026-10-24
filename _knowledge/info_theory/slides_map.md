# Ինֆորմացիայի տեսություն: which slides go with which lesson (2026-10-24)

The decks: the user's zip `Desktop\InformationTheory_ASDS_Lecture Slides.zip` (17.6 MB; it was on the
Desktop, not in Downloads), extracted to `Desktop\misc\YSU OpenCourseWare\info\slides\Lecture Slides\`
(10 PDFs, `InformationTheory-ASDS-2026-<deck>-posted.pdf`). Page titles of every deck:
`scripts/archive/info_theory_2026-10/deck_titles.py` (first text line per page; the new pages of each deck by title against the previous one).

Each deck is cumulative within its part ("Lectures 2-5" = the part as of lecture 5) and was posted on the
day of the lecture, so a lesson's slides are the pages that deck added.

| Lesson | Friday | Deck (pages) | That lesson's pages | Topics on those pages |
|---|---|---|---|---|
| Դաս 0 | 6 Feb | Intro-L-1 (14) | 1-14 | introduction to communication science, research in Armenia |
| Դաս 1 | 13 Feb | Intro-L-1-extended (36) | 15-36, plus the first pages of L-3 | probability review (independence, distributions, joint PMF, Markov / Chebyshev, laws of large numbers; image-only slides); then "Quantifying Information", entropy (Դաս 1's chapters end on entropy at 55:55-1:10:35) |
| Դաս 2 | 20 Feb | L-3, "Lectures 2-3" (28) | the rest of 2-28 | self-information and the horse race (Դաս 2 opens with it), conditional and joint entropy, chain rule, mutual information |
| Դաս 3 | 27 Feb | L-4, "2-4" (53) | 28-53 | information divergence (KL), information inequality, Jensen, max entropy, log-sum, convexity, data processing inequality |
| Դաս 4 | 6 Mar | L-5, "2-5" (82) | 54-82 (54-58 carry titles already in L-4) | Fano's inequality, summary of the measures, cross entropy and KL |
| Դաս 5 | 13 Mar | L-6, "Lecture 6" (21) | 1-21 (a new part) | AEP, consequences of AEP: data compression |
| Դաս 6 | 27 Mar | L-8, "6-8" (39) | 22-39 (1-21 = L-6) | data compression agenda, Morse code, nonsingular, extension, uniquely decodable, instantaneous codes, Kraft inequality (goal: minimum expected length) |
| Դաս 7 | 17 Apr | L-10, "6-10" (71) | 40-71 | Kraft proof (40-44), optimal codes, bounds, wrong codes, Kraft for uniquely decodable codes, Huffman coding |
| Դաս 8 | 8 May | L-11, "6-11" (100) | 72-100 | Huffman vs Shannon codes, weighted codewords, Fano codes, optimality of Huffman, Shannon-Fano-Elias, competitive optimality, summary |
| (not filmed) | 22 May | ChannelCapacity-L-13-end (78) | 1-78 | method of types, channel capacity, coding theorem, error correction, Hamming codes |

No L-7 (20 Mar, the substitute), L-9 (10 Apr, the written quiz) or L-12 (15 May, open).

## Page numbers on the final deck of each part (2026-10-24, for the descriptions)

The decks only grow, so a page keeps its number in later decks of the same part (checked by page text:
L-6 -> L-8 20/21 pages identical at the same number, L-8 -> L-10 34/39, L-10 -> L-11 70/71, L-4 -> L-5 46/53;
the rest are small text edits, same titles). So every lesson can point at the last deck of its part:

| Lesson | Final deck | Pages | Checked against |
|---|---|---|---|
| Դաս 0 | Intro-L-1-extended (36) | 1-15 (15 = pairwise vs mutual independence, its last chapter) | rendered page 15 |
| Դաս 1 | Intro-L-1-extended + L-5 | 16-36 (image-only pages) + L-5 2-7 (entropy, Bernoulli, coin) | live chapters |
| Դաս 2 | L-5 "Lectures 2-5" (82) | 8-27 (English letters, horse race ... summary) | live chapters |
| Դաս 3 | L-5 | 28-54 (KL ... DPI corollary Z = g(Y)) | live chapters (ends 52:30 on it) |
| Դաս 4 | L-5 | 55-82 | live chapters (opens on the DPI recap) |
| Դաս 5 | L-11 "Lectures 6-11" (100) | 1-21 | slides_map above |
| Դաս 6 | L-11 | 22-39 | |
| Դաս 7 | L-11 | 40-71 (opens on a recap of 38-39) | transcript, new upload `S8vcM74HZVE` |
| Դաս 8 | L-11 | 72-96 (opens on a recap of 66-68; never reaches 97-100: competitive optimality, summary) | transcript, new upload `LOHGyVgaIuI` |
| (22 May, not filmed) | ChannelCapacity-L-13-end (78) | 1-78 | |

## Դաս 6's audio-only end (recorder 1:03:40-1:20:25)

What the slides must cover: L-8 pages ~33-39 (instantaneous codes -> Kraft inequality, its goal "construct
instantaneous codes with minimum expected length"); the transcript has "ակնթարթային կոդ" at 1:03:58-1:04:21,
"կրաֆթը" at 1:06:00, then the closing remarks (sources with memory, Lempel-Ziv at 1:19:29), for which there
is no slide. Դաս 7 picks up at Kraft's inequality (5:28) and proves it on L-10 pages 40-44.

## Titles for Դաս 6-8 (final, 2026-10-24; Q44, Q63)

His own words from the transcripts: "ակնթարթային կոդ" (instantaneous; also "պրեֆիքսից ազատ / պրեֆիքս
կոդ"), "միարժեք ապակոդավորվող", "կրաֆտի անհավասարություն", "օպտիմալ կոդ", "շենոնյան կոդ", "ֆանոյի կոդեր",
"կումուլյատիվ բաշխման ֆունկցիա" (Shannon-Fano-Elias). Huffman comes out of the ASR garbled ("հաղթման",
"հատման"); the titles use "Հաֆման". glossary_check: 0 findings (none of these terms is in the glossary).

- Դաս 6 | Տվյալների սեղմում։ Կոդերի տեսակներ և ակնթարթային կոդեր | Ինֆորմացիայի տեսություն (88; final, the user 2026-10-24: Kraft is only stated at the end and leads Դաս 7)
- Դաս 7 | Կրաֆտի անհավասարություն և օպտիմալ կոդեր։ Հաֆմանի կոդավորում | Ինֆորմացիայի տեսություն (93; final, pushed)
- Դաս 8 | Հաֆմանի, Շենոնի և Ֆանոյի կոդեր։ Շենոն-Ֆանո-Էլիասի կոդավորում | Ինֆորմացիայի տեսություն (94; final, pushed)
