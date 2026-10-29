# Planner

Live task board for the YouTube work: what is running, what waits on whom, what is next.
Claude updates it at every status change and reads it at the start of a session. Parked topics
go to `DEFERRED_TODO.md`, decisions to `DECISIONS.md`, per-course detail to `_knowledge/`.

**Status:** `DONE` · `RUNNING` (in progress now) · `WAIT-YT` (YouTube is processing) ·
`YOU` (waits on you) · `DECIDE` (your decision needed) · `TODO` (Claude, can start) · `LATER`

Last update: 2026-10-29 01:30 (Munich). Rows checked against `_work_sessions/` up to 2026-10-28; two sessions edit
this file, so update your own rows AND look over the others before saving.

## Now

| What | Status | Next step |
|---|---|---|
| Nested chapters on Metric + umath (DECISIONS #46, Q81/Q82) | `TODO` | **111 of 457 done** 2026-10-29 01:10-01:20 on the user's go ("use todays quota"): all Metric, all read back OK, 0 skipped; stopped on quotaExceeded at #112 (the rest of 28 Oct Pacific's quota). Left: 346, ~2 days at ~190 a day: rerun `python snapshots/nest_plans/push_nest.py` after each quota reset (08:00 Munich until 1 Nov, then 09:00) until it reports all done. It skips anything edited since the 2026-10-26 snapshot; those need a fresh plan. Log: `snapshots/nest_plans/push_nest_log.jsonl` |
| ML [54] chapters on YouTube's captions | `DONE` | 2026-10-29: 26 boundaries audited, 3 moved back 1 s (8:12, 28:35, 30:13), pushed with the nested version, read back |
| End-screen learnings from 2026-10-28 | `DONE` | 9 files `_learnings/2026-10-29-0120_*` |
| Commit | `DONE` | See the 2026-10-29 session log |

## Metric Academy ML (channel metric)

| Video | Status | Open |
|---|---|---|
| [52] CNN: Playing Zmeyka `q8JM6nR03-Q` | `DONE` 2026-10-17 | - |
| [53] RNN `p0EVWRZLtMI` | `DONE` 2026-10-21, rechecked on YouTube's captions 2026-10-24 | - |
| [54] LSTM `m88ZdQhxHp8` | `DONE` 2026-10-24, rechecked 2026-10-29 | - |
| LLM [01] Tokenization `bhuxuKVhdSA` (recorded 2026-10-28) | `YOU` | All done and read back (53 cuts, 43 chapters, title, thumbnail DECISIONS #55, playlist "Large Language Models", Telegram line). Making it public is yours; the materials link (`llms/` page) is a 404 until the site rebuild (yours). No end screen (DECISIONS #56) |

ML48, ML49 and the Claude Code workshop have uncommitted edits to `corrections.txt` / `description.txt`
from another session; whether those are live has not been checked. Left out of commits.

## umath courses

| Course | Status | Detail |
|---|---|---|
| Tserunyan, Մետրիկական տարածություններ և տոպոլոգիա | `DONE` 2026-10-27 | All 25 public, nested, playlist in lesson order, Drive linked, email to her sent. Lectures 1 and 7 were never recorded |
| Papikian, Հանրահաշիվ և թվերի տեսություն | `DONE` 2026-10-22 | 21 public, playlist sorted, Drive linked |
| Arnak, Բազմաչափ վիճակագրություն 1 | `DONE` 2026-10-21 | End screens done 2026-10-28 (14/14, DECISIONS #52) |
| Ashot, Information Theory | `DONE` 2026-10-25 | All 9 public. Everything else settled (the user, 2026-10-29) |
| Sevak, Complex Analysis | `DONE` | His Honors Linear Algebra channel: chapters posted as comments (`LATER`: what else to do with it) |
| Vahagn Mikaelian, Linear Algebra | `DONE` 2026-10-28 | 97/97 public, playlist sorted 1.1-28.4, 44 replaced/raw uploads deleted, end screens 97/97. Closing email: Gmail draft in his thread (2026-10-28 14:28), sending is yours. Older pieces' date slips (16.2-գ, 17.1-19.2 say 2020; 20.3 27 vs 29 Apr) and two chapter slips in 11.1 / 11.2-բ: left as they are (the user, 2026-10-29: "i dont care") |
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
