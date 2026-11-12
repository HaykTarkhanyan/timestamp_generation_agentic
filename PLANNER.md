# Planner

Live task board for the YouTube work: what is running, what waits on whom, what is next.
Claude updates it at every status change and reads it at the start of a session. Parked topics
go to `DEFERRED_TODO.md`, decisions to `DECISIONS.md`, per-course detail to `_knowledge/`.

**Status:** `DONE` · `RUNNING` (in progress now) · `WAIT-YT` (YouTube is processing) ·
`YOU` (waits on you) · `DECIDE` (your decision needed) · `TODO` (Claude, can start) · `LATER`

Last update: 2026-11-10 01:46 (local). Rows checked against `_work_sessions/` up to 2026-10-28; two sessions edit
this file, so update your own rows AND look over the others before saving.

## Now

| What | Status | Next step |
|---|---|---|
| Nested chapters on Metric + umath (DECISIONS #46, Q81/Q82) | `DONE` 2026-11-03 | 456 of 457 updated and read back identical over 4 runs (29 Oct: 111 + 185, 3 Nov: 80 + 80); 0 changed since the 2026-10-26 snapshot. 1 skipped: `RtcShFCGIIs`, a Vahagn upload deleted 2026-10-28 (the first 3 Nov run crashed on it; `push_nest.py` now logs a missing video as SKIPPED). Vahagn's 25 new pieces were drafted nested already. Log: `snapshots/nest_plans/push_nest_log.jsonl` |
| ML [54] chapters on YouTube's captions | `DONE` | 2026-10-29: 26 boundaries audited, 3 moved back 1 s (8:12, 28:35, 30:13), pushed with the nested version, read back |
| End-screen learnings from 2026-10-28 | `DONE` | 9 files `_learnings/2026-10-29-0120_*` |
| Commit | `DONE` | See the 2026-10-29 session log |

## Metric Academy ML (channel metric)

| Video | Status | Open |
|---|---|---|
| [52] CNN: Playing Zmeyka `q8JM6nR03-Q` | `DONE` 2026-10-17 | - |
| [53] RNN `p0EVWRZLtMI` | `DONE` 2026-10-21, rechecked on YouTube's captions 2026-10-24 | - |
| [54] LSTM `m88ZdQhxHp8` | `DONE` 2026-10-24, rechecked 2026-10-29 | - |
| LLM [01] Tokenization `bhuxuKVhdSA` (recorded 2026-10-28) | `DONE` | 53 cuts, 43 chapters, title, thumbnail (DECISIONS #55), playlist "Large Language Models", Telegram line. Visibility and the materials page: fine (the user, 2026-11-03). No end screen (DECISIONS #56). 2026-11-09 (Q28): chapters rechecked on YouTube's captions, 20 moved back 1-2 s, re-pushed, read back. 2026-11-10 (Q37): nested (25 of 43 indented), pushed, read back |
| LLM [02] tokenization practical `hmE4QH_dSXI` + LLM [03] decoding `MF_jn0GXPWA` (one Zoom recording 2026-11-09, 2:15:39, uploaded twice, each keeps its half) | `RUNNING` 2026-11-09 20:50: both uploaded and saved unlisted by Claude (read back); split at the break (994 s silence at 0:53:09). [02]: your 51 cuts -> 50 (2+3 merged), 2:15:39 -> 0:35:39, entered 2026-11-10 00:58, diff identical, NOT saved (waits on your word); chapters remapped (20, nested), C1 bits vs bytes waiting for your OK; titles + thumbnails set 01:20; both C1 corrections approved; descriptions pushed 01:3x and read back (final/LLM02.txt, LLM03.txt); both added to the playlist (01, 02, 03 read back); Telegram lines given. [03] chapters checked on its regenerated captions 01:45 (10 moved back 1 s), re-pushed, read back. Done apart from making them public (yours). [02] SAVED 2026-11-10 01:03 by Claude at your word (dialog 35:39), processed: 2140 s. [03]: your 63 cuts -> 60, 2:15:39 -> 0:55:40, entered 01:10, diff identical, SAVED 01:16 by Claude (Q40, dialog 55:40; DECISIONS #58), processing; chapters remapped (33, nested), C1 top-k order waiting for your OK, materials TODO. Both studio.html pages opened 21:05; playlist only after Save (DECISIONS #57); LLM03.png made (temperature, quantum, bigger dog) | Split point + cut plans -> `YOU` review both studio.html pages (Q30: nothing saved before your review); chapters, titles, descriptions drafted on the predicted timeline; materials: [02] tokenization page, [03] TODO until its page exists (Q31); fun thumbnails ([03]: your sentence, if you send it) |
| LLM [04] LLM APIs practical `xdiq1N3KBPg` (recorded 2026-11-11, 56:47) | `DONE` 2026-11-12 00:57 | Zoom -> Downloads (370 MB), uploaded and saved Unlisted; your 60 cuts -> 58, saved by Claude (DECISIONS #58, dialog 41:11), processed 2472 s; title "[04] LLM APIs" (yours), thumbnail LLM04 option d (request + usage, no meme: "were overdoing the fun"); description with 34 nested chapters (17 moved back 1 s on YouTube's captions), materials = the notebook on GitHub, corrections (Q6 both: Stripe/OpenRouter minute 2, reasoning tokens minute 39), read back, all 34 parsed; playlist [01]-[04] read back. Course repo e3fa3ee (pushed): `llms/02_decoding/04_llm_api.ipynb` + `results/04_api_ledger.json`. 2026-11-12: [03]'s materials line now links `llms/02_decoding/decoding.html` (Q2). Making it public: yours |

ML48, ML49 and the Claude Code workshop: the other session's local `corrections.txt` / `description.txt` edits were
checked against live on 2026-11-03 (leading spaces and the title header ignored). ML49 and the workshop matched;
ML48 matched except "Ֆուրիե" -> "Ֆուրյե" (the 2026-10-23 glossary fix, live only), now applied locally. Committed.

## umath courses

| Course | Status | Detail |
|---|---|---|
| Tserunyan, Մետրիկական տարածություններ և տոպոլոգիա | `DONE` 2026-10-27 | All 25 public, nested, playlist in lesson order, Drive linked, email to her sent. Lectures 1 and 7 were never recorded |
| Papikian, Հանրահաշիվ և թվերի տեսություն | `DONE` 2026-10-22 | 21 public, playlist sorted, Drive linked |
| Arnak, Բազմաչափ վիճակագրություն 1 | `DONE` 2026-10-21 | End screens done 2026-10-28 (14/14, DECISIONS #52) |
| Ashot, Information Theory | `DONE` 2026-10-25 | All 9 public. Everything else settled (the user, 2026-10-29) |
| Sevak, Complex Analysis | `DONE` | His Honors Linear Algebra channel: chapters posted as comments (`LATER`: what else to do with it) |
| Vahagn Mikaelian, Linear Algebra | `DONE` 2026-10-28 | 97/97 public, playlist sorted 1.1-28.4, 44 replaced/raw uploads deleted, end screens 97/97. Closing email sent by the user (said 2026-11-03). Older pieces' date slips (16.2-գ, 17.1-19.2 say 2020; 20.3 27 vs 29 Apr) and two chapter slips in 11.1 / 11.2-բ: left as they are (the user, 2026-10-29: "i dont care") |
| umath end screens, all tiers | `DONE` 2026-10-28 | `_knowledge/umath_endscreens_plan.md` |
| Vahagn Mikaelian, Groups | `LATER` | Not checked |
| Papikian, Galois Theory (ARCS-ai 2025) | `LATER` | Publish or not |

## Decisions and reviews for you

| Item | Status | Detail |
|---|---|---|
| Audit rows marked "user" / "verify" (#1, #3, #5, #8, #13-15, #23-27, #33, #45-61) | `LATER` | You: "tell later" (2026-10-23) |
| 40 NEAR glossary typo candidates | `LATER` | Claude reviews them first |
| Complex Analysis Դաս 20, 21, 23: lecture date or re-recording date | `LATER` | `DEFERRED_TODO.md`, 2026-10-20 |
| "Copy only the needed files, never copy-then-delete" in the global CLAUDE.md | `DECIDE` | Offered on 2026-10-20 after the `rm` incident |
| `scripts/.secrets/studio_storage_state.json` (Google session cookies, git-ignored) | `DONE` | Kept as is (the user, 2026-10-29: "i dont care") |
