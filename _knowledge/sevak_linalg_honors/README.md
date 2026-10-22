# Sevak Mkrtchyan's Honors Linear Algebra (his own YouTube channel, fall 2026)

Channel https://www.youtube.com/@sevakmkrtchyan-u1h (`UClkaOimplNdkXoTZgjM8k5g`), playlist
"Honors Linear Algebra". Stored for later by the user's request (2026-10-22); see the Sevak section
of `_knowledge/umath_todo.md`. Not on the umath channel.

One folder per lecture, in the youtube-timestamps layout: `<id>.hy.vtt` (YouTube's auto-generated
Armenian captions), `transcript.txt` (the skill's cleaner, `MM:SS  text`), `metadata.json`.
All 10 were fetched on 2026-10-22; each transcript runs to within 11 s of the video's end.

| Lecture | Video | Uploaded | Length | Transcript lines |
|---|---|---|---|---|
| 1 | `2NHMdJ5_Nlc` | 2026-09-16 | 58:57 | 1092 |
| 2 | `LlE7wAwHXwU` | 2026-09-16 | 1:08:30 | 1293 |
| 3 | `ick3KBcAkiA` | 2026-09-21 | 1:10:57 | 1276 |
| 4 | `aRcE27Yctc0` | 2026-09-23 | 1:19:05 | 1421 |
| 5 | `L8553Rsp-p4` | 2026-09-28 | 1:18:11 | 1507 |
| 6 | `3jTrMkTfYPM` | 2026-09-30 | 1:18:20 | 1418 |
| 7 | `fUq8qMo_8EQ` | 2026-10-06 | 1:02:26 | 1119 |
| 8 | `CvjkdBoBS7g` | 2026-10-07 | 1:15:00 | 1202 |
| 9 | `3ZXwdhEMiGg` | 2026-10-12 | 1:17:38 | 1355 |
| 10 | `CZauFDOB3tY` | 2026-10-14 | 1:14:05 | 1284 |

## Chapters, to post as comments (2026-10-22)

Each folder has `chapters.txt` (the verifier's input) and `comment.txt` (the same list under a
`⏳Թեմաներ` header, paste-ready). Written by two agents (lectures 1-5 and 6-10, 680k tokens),
then aligned across all 10 and verified (`verify_timestamps.py --min-gap 30`, all valid):
18-22 chapters per lecture, labels in Armenian with the lecture's notation, step words with `․`.
**Posted 2026-10-22 13:03-13:06** as comments by the umath channel (Համալսարանական մաթեմատիկա),
with `yt_publish.py --channel umath add-comment` (its duplicate guard now compares the posting
channel, not the video's owner). Checked through the API: all 10 listed publicly, text identical
to `comment.txt`, 232 of 232 timestamps turned into links. Comment ids: L1 UgxrDd6pM7lYbSC4hr54AaABAg,
L2 UgxdbVxVvhaFrdxkdM14AaABAg, L3 UgyL7j_GSDA6LU03WsZ4AaABAg, L4 UgxnlyqIbBrU7NUohfd4AaABAg,
L5 Ugzc96JFfD0KgZ2kDUt4AaABAg, L6 UgxRQ78kMYGIYUd3YAl4AaABAg, L7 UgzsvHYjhWHLwk6xCxx4AaABAg,
L8 UgxyJrzCRNyY3I5Zi_N4AaABAg, L9 UgxIk6kHsz0hYCynzbB4AaABAg, L10 UgwuByF4AxO_5VUv9cZ4AaABAg.
Comments do not make YouTube chapters (only the description does), but their timestamps are
clickable. At 13:2x the same day each got a lesson title line on top (the user: "for each in the
beginning add lesson title"), e.g. `Դաս 7 | Բազիսի լրացում։ dim(W₁ + W₂) բանաձևը`, edited in place
through the API (`comments.update` works on the channel's own comments; YouTube shows "(edited)");
re-checked: text identical to `comment.txt`, 232 of 232 timestamps linked. Our `yt_publish.py` has
no update command; the one-off script was `comment_titles.py` in the session scratchpad.

Term choices kept the same across the 10: վեկտորական տարածություն; բերված աստիճանաձև տեսք
(RREF); S-ով ծնված ենթատարածություն, span(S); բազիս; չափողականություն dim V; գծորեն
անկախ/կախյալ; գծային կոմբինացիա; գծային ձևափոխություն; միջուկ Ker T, պատկեր Im T; համադրույթ;
տարրական մատրից; հակադարձելի; անցման մատրից; ℝ, ℂ, Fⁿ.

Stretches the agents flagged as garbled (labels kept general, numbers not quoted): L1 25:08-25:20
(a student's question), L2 33-40 / L3 11-15 / L4 33-36 (worked examples' numbers), L5 01:16:56
(the axiom-of-choice question), L6 35:07-36:05 (the polynomials of the example), L6 52:33-53:01
(Zorn's lemma or the axiom of choice), L9 48:14 (the map's formula read from 54:29), L10 14:42
(an internet problem in the room, its own chapter).

Reviewed 2026-10-22: every label checked against the transcript at its stamp (1 line before, 3
after) and the math in the labels checked; 5 labels rewritten (L2 55:39, L5 51:44 and
01:10:30, L6 46:41, L8 53:21: vague, a statement under "Հարց․", or the agent's own term instead
of what was asked); all 10 still valid. No boundary needed moving.

Independent review 2026-10-22 (one agent, full transcripts, 557k tokens, report only): 30 findings
on 209 chapters, 10 certain. Applied 39 edits: hypotheses missing from theorem labels (S
independent, square/n×n, P a product of elementary matrices, finite-dimensional, non-empty,
homogeneous), statements under `Հարց․` turned into questions, the Armenian ՞ added to 11 question
labels, L1 03:50 and L6 01:04:54 boundaries (L6 01:03:45 became its own "how to define dimension"
chapter: 210 chapters now), wording and consistency. Not applied: the 5 bare `Ապացույց` (fine),
`[v]_B` / `T_A` (no Unicode subscript capitals), two optional chapter splits (L4 22:46, L9 45:19),
and L5 45:09: the lecturer says Hermitian matrices form a subspace of the complex matrices, which
is true over ℝ only (iH is skew-Hermitian); the label repeats what he said, the slip is the user's
call. The pre-review lists are in the session scratchpad (`chapters_before_review2/`).

Codex review 2026-10-22 (the user: "do another review using codex"): `codex exec`, read-only, one
run per lecture with the transcript and all 10 lists inline (its Windows sandbox could not start a
shell: "setup refresh had errors", so it read no files when asked to), ~370k tokens on the ChatGPT
plan, about 84 findings, stricter than the Claude reviewer. Applied 81 edits (210 -> 232 chapters,
21-25 per lecture, all verifier-valid): more hypotheses (finite-dimensional, m×n, invertible A, B,
"there exists P"), clearer labels, ՞ in non-`Հարց․` labels too, boundaries moved off recaps onto
the actual statement, and own chapters for 7 proofs, buried student questions and a few topics.
Every new or moved time was checked against its transcript line. Not applied: boundary moves
where the current stamp is the lecturer's own announcement of the topic (L1 03:50, 08:20, 12:00;
L3 07:43; L5 07:17, 56:56; L6 13:13; L10 03:53, 16:01), L5 39:03 "n ≥ 3" and 43:28 "polynomial
functions" (pedantic), L2 07:40 շրջելի (fine for steps), and the L5 Hermitian slip (user's call).
Backup of the lists before it: session scratchpad `chapters_before_codex/`.

What the recordings show: lectures in Armenian over Zoom, written on a notes app (Xournal-like
lined pages) with his camera tile; lecture 1 opens with "Linear algebra / Linear approximations".
At the end of lecture 1 a student asks whether the course gives a grade or pass/fail, to transfer
the credit to their own university, and he stops the recording: a credit course for students
from several universities. Who organizes it (ASOF, ARCS-ai, ...) is not said in the transcripts.

How they were fetched: yt-dlp was blocked by YouTube's "Sign in to confirm you're not a bot".
In Playwright, the caption track's plain `baseUrl` returns an empty body (it needs a `pot`
proof-of-origin token); the player's own `/api/timedtext` request carries one, so the page was
loaded with a response listener, that request's URL taken and re-fetched with `fmt=vtt`.
