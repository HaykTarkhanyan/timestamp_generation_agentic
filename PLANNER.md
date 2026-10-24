# Planner

Live task board for the YouTube work: what is running, what waits on whom, what is next.
Claude updates it at every status change and reads it at the start of a session. Parked topics
go to `DEFERRED_TODO.md`, decisions to `DECISIONS.md`, per-course detail to `_knowledge/`.

**Status:** `DONE` · `RUNNING` (in progress now) · `WAIT-YT` (YouTube is processing) ·
`YOU` (waits on you) · `DECIDE` (your decision needed) · `TODO` (Claude, can start) · `LATER`

Last update: 2026-10-24 20:45 (Munich)

## Now

| What | Status | Next step |
|---|---|---|
| Video previews for Tserunyan 15-27 | `DONE` | All 13 pages play the 360p video (16:03); every cut list unchanged; two queue runs were killed for low RAM and restarted one at a time |
| Tserunyan 16-27: review the 5 s cut plans on studio.html | `YOU` | Give the list with "pw": Claude enters and saves it if the diff and length check pass (DECISIONS #27) |
| Audit batch 2 (60 descriptions) | `DONE` | 2026-10-23 12:01, all 80 of the batch read back matching |
| Glossary scan of both channels | `DONE` | 13:32 after the term fixes: 664 items, 0 DENY, 40 NEAR, 383 ENG |
| Ashot Դաս 4-8: send the message, wait for his OK | `YOU` | Message drafted (Armenian, links + titles); all 9 videos finished and audited, 4-8 unlisted. After his OK: Claude makes 4-8 public (status fields kept) and reads back |
| Commit this session's work | `DONE` | 2026-10-24 20:5x, pushed; Metric Academy leftovers from other sessions (ML48/49/52-54, Claude Code, fonts) left out again |

## Tserunyan - Մետրիկական տարածություններ և տոպոլոգիա (channel umath)

25 videos: Դաս 1-2, 3-6, 8-14 public (lectures 1 and 7 never recorded); 15-27 unlisted, being finished.
Detail: `_knowledge/tserunyan_metric/finish_15-27.md`. Release: all 15-27 public together (you, 2026-10-23).

| Video | Plan | Review (you) | In Studio + saved | Chapters, title, description, thumbnail | Preview |
|---|---|---|---|---|---|
| 15 `ANoJdXQEOOA` | your edit, 92 -> 91 cuts, -14.8 min | `DONE` | `DONE` 03:57 by Claude, diff identical, 1:26:01 | `DONE` 12:08, read back (30 chapters) | `DONE` |
| 16 `3K76N175zvM` | 70 cuts, -16.0 min | `YOU` | | drafts ready | `DONE` |
| 17-27 | 47-110 cuts, -8.5 to -18.7 min (`finish_15-27.md`) | `YOU` | | drafts ready | `DONE` |

| Tserunyan task | Status | Detail |
|---|---|---|
| Course files on the math-team Drive | `DONE` | 41 files (notes, homework named by topic, info sheet with the TA email redacted), anyone with the link (`drive_materials.md`) |
| Drive block in the descriptions of the 12 public videos | `DONE` | 12:03, all 12 read back |
| Դաս 15 blur (participant on the projector) | `DONE` | Left as is (you, 2026-10-23) |
| Playlist sort into lesson order | `TODO` | After 15-27 are public |
| Correction notes | `DONE` | None on umath (DECISIONS #25) |

## Metric Academy ML (channel metric)

| Video | Plan | Review (you) | In Studio | Saved | Chapters + description | Thumbnail | Telegram line |
|---|---|---|---|---|---|---|---|
| [52] CNN: Playing Zmeyka `q8JM6nR03-Q` | `DONE` | `DONE` | `DONE` | `DONE` | `DONE` 2026-10-17, 40 chapters, 2 corrections | `DONE` | `DONE` ("Project") |
| [53] RNN `p0EVWRZLtMI` (lecture) | `DONE` | `DONE` | `DONE` | `DONE` 2026-10-21 21:06 | `DONE` 22:00 (38 chapters); rechecked on YouTube's captions 2026-10-24, 5 moved back 1 s, re-pushed | `DONE` | `DONE` |
| [54] LSTM `m88ZdQhxHp8` (lecture) | `DONE` 2026-10-24 00:22: 22 cuts, -15.2 min (55:43 -> 40:33), audio from YouTube | `DONE` your 33 -> 31 cuts | `DONE` 00:52, diff identical | `DONE` 00:53 by Claude at your request, dialog 39:19 | `DONE` processed 01:15 (2360 s); description with correction C1 pushed 01:15, read back: 26 chapters. `TODO` check the chapters on YouTube's new captions (none at 01:16) | `DONE` 00:33, "RNN: Long Short-Term Memory" (Kargin + LSTM cell) | `DONE` given 01:02 ("Lecture") |

ML48, ML49 and the Claude Code workshop have uncommitted edits to `corrections.txt` / `description.txt`
from another session; whether those are live has not been checked.

## Papikian - Հանրահաշիվ և թվերի տեսություն (channel umath): `DONE` 2026-10-22

All 21 videos edited, chaptered, described and public; Drive folder linked. 2026-10-23: playlist set to
"Manually sorted" in Studio and sorted 1-23 (20 moves, read back); Դաս 4 date line 23 -> 24 September 2024
(read back); homework files renamed by topic. Open: the term decisions below (`LATER`).

## Arnak - Բազմաչափ վիճակագրություն 1 (channel umath): `DONE` 2026-10-21

All 13 lectures + the 2025 recording edited, chaptered, described and public; playlist sorted, PDF folder
linked. Only open item: end screens for 2-13 + 2025 (`LATER`, `DEFERRED_TODO.md`).

## Other courses (channel umath)

| Course | Status | Detail |
|---|---|---|
| Ashot, Information Theory | `YOU` | Դաս 6-8 rendered (1.25x, ffmpeg), uploaded, chaptered (nested, DECISIONS #34), titled, thumbnailed; slides folder on the math-team Drive linked from all 9 with page ranges (#33); Դաս 4/5 labels fixed; playlist sorted 0-8. Waiting: your message to him, then his OK -> 4-8 public. Open: Q36 (15 May), Q46 end screens, Q38 Դաս 5 speed, delete 3 private caption uploads. Todo: `_knowledge/info_theory/todo.md`, overview: `_knowledge/info_theory/videos_overview.html` |
| Sevak, Complex Analysis | `DONE` | His email answered by you (2026-10-23); his Honors Linear Algebra channel: chapters posted as comments |
| Vahagn Mikaelian, Linear Algebra + Groups | `LATER` | ~24 missing pieces, Դաս 21.2 "Todo" title, playlist sort (67 of 73); Groups not checked |
| Papikian, Galois Theory (ARCS-ai 2025) | `LATER` | Publish or not |

## Decisions and reviews for you

| Item | Status | Detail |
|---|---|---|
| Audit rows marked "user" / "verify" (#1, #3, #5, #8, #13-15, #23-27, #33, #45-61) | `LATER` | You: "tell later" (2026-10-23) |
| Open glossary terms | `DONE` | 2026-10-23 13:26-13:32 (the user's Q21): division ring = բաժանումով օղակ, Համիլտոն-Քեյլի and պրիմար բաժանարարներ / ինվարիանտ ֆակտորներ (his own words in Դաս 14) kept; Դաս 22 Eisenstein -> Դաս 7's Այզընշտայն; Ֆուրյե, կոռելացիա, բազմանդամային օղակ, չհատվող ցիկլեր, ℤ[i] fixed live on 25 videos; ML [08] suffix, ML [41] -> 'Մեկ նեյրոնից ցանց'; the BRIGHTNESS Դաս 5 duplicate unlisted; all read back; glossary + denylist updated; rescan 0 DENY (40 NEAR, 383 ENG). Backup: `_knowledge/descriptions_before_term_fixes_2026-10-23.json`. Left: 40 NEAR typo candidates (Claude reviews them first) |
| "Copy only the needed files, never copy-then-delete" in the global CLAUDE.md | `DECIDE` | Offered on 2026-10-20 after the `rm` incident |
