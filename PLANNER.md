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

| LLM [05] tool calling `7FhEiQBUgK0` + LLM [06] MCP, skills, orchestration `C4Zcf1K51FI` (one Zoom recording 2026-11-18, 2:02:31, lecture both) | `DONE` 2026-11-18 23:32 (materials links open) | Zoom ready 20:00, downloaded (473 MB); uploaded twice ([06] from a renamed copy: the same file joined the first upload, learning 2026-11-18-2203), saved Unlisted 20:40; break 0:59:32-1:15:33. [05]: your 94 cuts -> 88 (Q6 tiny cuts kept, `cut_list.py --min-cut`), saved 22:07 (dialog 45:08), processed; title "[05] Tool Calling & Agents" (Q4), thumbnail LLM05 Ararat (Q2), description + 38 chapters (21 moved back 1 s on YouTube's captions) + the 3-cents correction (Q8, kept Q9), in the playlist ([01]-[05] read back). [06]: your 100 cuts -> 96, saved 22:50 (dialog 37:12), processed 2233 s; title "[06] MCP, Skills & Orchestration", thumbnail LLM06 servers + skills (Q3), description + 38 chapters live (23 moved back 1-4 s on YouTube's captions). Blur: 3 custom blurs entered by Claude via Playwright (2:34:13-2:52:12, 3:25:13-3:55:05, 3:51:00-4:11:13), saved by you 23:2x; thumbnail redone (symmetric boxes, `cheese-making/` skill); in the playlist 23:32 ([01]-[06] read back). Materials: both TODO until llm_1_2's uncommitted tools_agents edits are committed, then rename xx_ -> 05_/06_ and link (Q5, Q7). Making both public: yours |
| LLM [07] Kargin sketch agent (project) `X_Yzd3Z5jvw` (recorded 2026-11-25, 1:11:52) | `DONE` 2026-11-26 00:02 | Your 65 cuts -> 62 (4+5+6, 50+51 merged; the 0.48 s cut kept), entered (115 + 124 s), diff identical, SAVED 23:41 by Claude (DECISIONS #58, dialog 51:19), processed by 23:54 (3080 s). Chapters remapped to 42 (the old-site chapter dropped: your cut 4 left it 22 s), title, description, thumbnail pushed 23:55, all 42 chapters parsed; 00:02 rechecked on YouTube's regenerated captions (9 moved 1 s, 5 kept as predicted), re-pushed, 42 parsed; 00:08 review: no clear mistakes, one note added (Q17: minute 34, parallel tool calls); in the playlist ([01]-[07] read back). Making it public: yours. Earlier: Zoom ready ~19:00, downloaded (337 MB, 93 s); uploaded and saved Unlisted 19:36 (checks ~35 min), Armenian captions at once; no break. Plan: 41 cuts, 19.7 min (1:11:52 -> 52:11), 2 unticked (closing course plan, projects advice); frame sweep: nothing private. studio.html opened. Drafted on the plan: 43 chapters (verified), abstract, 4 titles, description (final/LLM07.txt, materials = the notebook + sketch_finder/ on GitHub), no corrections; thumbnail LLM07 = the fishing trip (Q16; rejected: the minibus punchline, "not the best for this course", and the mayor example, "no political example"); title "[07] Kargin Agent: Tool Use" (Q13, the user's direction). -> `YOU` review the cuts on studio.html, nothing else. Then: enter + save (DECISIONS #58), remap chapters, push metadata, playlist after Save |
| LLM [08] RAG 1: retrieval (chunking, BM25, embeddings) `s7MCThtCnfo` (recorded 2026-11-27, 1:15:26; deck `llms/04_rag/08_rag_retrieval`) | `WAIT-YT` 2026-11-27 22:55 | Your 50 cuts -> 48 (2+3, 35+36 merged), entered (449 + 100 s), diff identical, SAVED 22:52 by Claude (DECISIONS #58, dialog 1:02:06 = frames), processing. Title + thumbnail set 22:54. Chapters remapped to 47 + "Հաջորդ դասերը" (the kept closing plan) = 48, verified; correction now minute 52; `final/LLM08.txt` ready (3745 chars). The nickname rewrite example stays ("a one off choice not a rule"). -> after processing: push the description, check chapters on the regenerated captions, playlist. Earlier: Zoom ready ~18:39 (the 08:00 PM Yerevan card; the 06:30 PM one is another meeting), downloaded 96 MB in 10 s; uploaded, checks done ~18:51, saved Unlisted (yt-dlp: unlisted, 4526 s); captions 19:02; no break. Frame sweep: nothing private. Plan: 29 cuts, 12.2 min (1:15:26 -> 1:03:15), 4 unticked (today's plan, slide pointer, ATE-2 slide remark, closing course plan). studio.html opened. Drafted on the plan: 47 chapters (verified, lint clean), abstract, 4 titles, description `final/LLM08.txt` (materials = the slides PDF on GitHub; `rag.qmd` is not on the site yet), review.md: one clear mistake (cross-encoder pairs n(n-1)/2, min 53 on the plan; Q4: add it, in the description). Q2 title "[08] RAG: Chunking, BM25 & Embeddings". Q3 thumbnail: a/b (press, BM25 0.000) -> "something more visual pls maybe for vector search" -> c, the nearest dot in the deck's toy space (`thumbnails/LLM08.png`). Q5 materials: the future `llms/04_rag/rag.html` (404 today) + course repo inbox note `_claude_inbox/2026-11-27-2200_rag-page-for-video-08.md` (bdbb8904, pushed). Q1 done 21:59: [05]/[06]/[07] materials -> `llms/03_tools_agents/tools_agents.html`, pushed from the live text (local copies identical before), read back, chapters 38/38/42 still parse; local copies synced. -> `YOU` review the cuts. Then: enter + save (DECISIONS #58), remap chapters, push metadata, playlist after Save |

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
