# Համալսարանական մաթեմատիկա (umath): end screens plan

Status: planned 2026-10-28 (the user: "next well need to do the same for umath, but not now, just plan it").
Generator: `scripts/non_essential/make_endscreen_jobs_umath.py <course>`.

**Progress (2026-10-28, paused by the user after Sevak):**

| Course | State | Left to do (job files ready in `.playwright-mcp/`) |
| --- | --- | --- |
| Ashot, Ինֆորմացիայի տեսություն (9) | done, 9/9 (0-2 already matched, 3-8 added) | - |
| Sevak, Կոմպլեքս անալիզ (25) | done, 25/25 (had none; one clean batch) | - |
| Papikian, Հանրահաշիվ և թվերի տեսություն (21) | **done 21/21** (2026-10-28): 15-23 added, 1-14 (13) rebuilt in one clean batch | - |
| Tserunyan, Տոպոլոգիա (25) | **done 25/25** (2026-10-28): 14-27 added, 1-2..13 rebuilt (the rebuild mode's first script run; 1-2 rechecked after a reload, all batches clean) | - |
| Arnak, Բազմաչափ վիճակագրություն (14) | **done 14/14** (2026-10-28): landscape lessons Subscribe + next + playlist; portrait/square 2-6, 9-12 Video + Playlist (no 3-element template exists for them, DECISIONS #52); 3-6, 9-12 rechecked 8/8 | - |
| Vahagn, Գծային հանրահաշիվ (97) | **done 97/97** (2026-10-28): playlist order, unlisted 21.1-28.4 linked (Q22, DECISIONS #53) | - |

**Tier 1 complete: 191/191 (2026-10-28).** Kept at 10 s (Q50): Sevak, Papikian and Tserunyan end on a hand-drawn card
from ~7-8 s before the end, and the user did not want the layout matched to its boxes.
**Tier 2 complete (2026-10-28):** all 199 of ours have end screens (the 2 in Գծ. հանրահաշվի հիմունքներ belong to
"3blue1brown հայերեն"); ՍԴՀ Դաս 15 (2 playlists, no video) left as it was. Record:
`output/endscreens/umath_progress_2026-10-28.json` (`tier2`).
**Tier 3 (2026-10-28):** 282 videos, 238 of them on other channels (Բաց դասեր 235, Հետաքրքիր զրույցներ 3). Our 44 surveyed
(`output/endscreens/umath_tier3_survey_2026-10-28.json`): 24 short lessons with Subscribe + Best for viewer +
"Կարճ տեսանյութեր", the Կիրառություններ loop (6), 3 hand-made ones (left, Q52), 11 with none. Of those 11: the 3
seminars got Subscribe + next seminar + Սեմինարներ at 10 s (Q51, done); the 6 short lessons are ultra-wide (~2.27:1) and
Studio refuses end screens on them ("unsupported aspect ratio"); the 2 unlisted thesis days are skipped.
**umath end screens are finished (2026-10-28).** Vahagn's replaced and raw uploads (incl. the 11 same-title twins) were deleted 2026-10-28
(Q38, `_knowledge/vahagn_linalg/status.md`).

Studio is on the umath channel. Record: `output/endscreens/umath_progress_2026-10-28.json`. Same goal as Metric Academy (DECISIONS #51): Subscribe + the next video + the course playlist in the last 10 s,
the last lesson "Best for viewer". Tools and lessons from the Metric run: `scripts/non_essential/README.md` (end-screen
rows) and `_work_sessions/2026-10-27-1300_metric-end-screens.toml`.

## Inventory (read-only API, 2026-10-28)

30 playlists, 705 entries, **674 unique videos**. Record: `output/endscreens/umath_playlists_2026-10-28.json`
(every playlist with its video ids, privacy counts, first and last title). Only the short-video playlists share videos
(31 of the 32 in "Կարճ տեսանյութեր" are also in a topic playlist); no course playlist overlaps another.

**Tier 1: courses we produced or curated recently** (numbered lessons, notes in `_knowledge/umath_todo.md`), 191 videos

| Playlist | Videos | What to watch for |
| --- | --- | --- |
| Գծային հանրահաշիվ (Vahagn) | 97 (72 public, 25 unlisted) | "Դաս N.M" numbering; umath_todo still lists "sort the playlist into lesson order" as open; 25 unlisted |
| Տոպոլոգիա և մետրիկական տարածություններ (Tserunyan) | 25 | combined lessons ("Դաս 1-2"); playlist in lesson order |
| Կոմպլեքս անալիզ (Sevak) | 25 | playlist in lesson order |
| Հանրահաշիվ և թվերի տեսություն (Papikian) | 21 | numbers run to Դաս 23 with 21 items: check gaps or combined lessons |
| Բազմաչափ վիճակագրություն (Arnak) | 14 | lesson 1 done by hand 2026-10-21; jobs for 2-13 + 2025 exist but from the old template (regenerate); agreed then: 1-11 -> next, 12 -> 13, 12 (2025) -> 13, 13 -> Best for viewer |
| Ինֆորմացիայի տեսություն (Ashot) | 9 | **done 2026-10-28** (all 9 public, lesson order) |

**Tier 2: older numbered lecture courses**, 201 videos: Ֆունկցիոնալ անալիզ 23 (starts at Դաս 3), Մաթեմատիկական
անալիզ 1/2/3/4 (տվյալագետների համար) 22/20/22/20, Մաթեմատիկական անալիզ 3 16 (starts at Դաս 9), Մաթեմատիկական անալիզ 4
12 (unlisted playlist), Սովորական դիֆերենցիալ հավասարումներ 16 (last item has no lesson number), Պատահական պրոցեսներ
14 (Դաս 19-32), Մաթֆիզ հավասարումներ 12, Խմբերի տեսություն 10, Թվերի տեսություն 10 (dated titles, no lesson numbers),
Հավանականությունների տեսություն 2, Գծային հանրահաշվի հիմունքներ 2.

**Tier 3: not courses**, 313 entries: Բաց դասեր 235 (dated open lessons 2017-18), Կարճ տեսանյութեր 32 and four topic
short-video playlists (11, 10, 6, 4), Մաթեմատիկայի կիրառություններ 6, Սեմինարներ 4, Հետաքրքիր զրույցներ 3, MS ASDS
Thesis Presentation 2 (unlisted). End screens may not be available on Shorts at all (not checked yet).

## What differs from the Metric run

1. **Channel.** Jobs carry `UCMFONp28jEDHXDBWJyRVYcA`, and Studio must be switched to umath first (account button >
   Switch account); the template refuses to run under another channel. Switch back to Metric afterwards
   (`_learnings/2026-10-27-0359_studio-session-channel-can-differ-from-the-video.md`).
2. **"Next" rule.** Lesson numbers come in several shapes: "Դաս N", "Դաս N.M" (Vahagn), "Դաս N-M" (Tserunyan),
   "Դաս N (2025)" (Arnak), "Դաս 0" (Ashot), and some titles have none. Simplest rule where it holds: the playlist's
   own order, after a read-only check that the playlist is in lesson order (and `yt_publish.py sort-playlist` where it
   is not; that needs the playlist on "Manually sorted", `_learnings/2026-10-20-2221_playlist-reorder-needs-manual-sort.md`).
   The end-screen playlist link opens at the playlist's top video, so lesson order also makes that link right.
3. **Unlisted videos** (Vahagn's 25): linking to one sends viewers to a video not meant to be found. Skip them in
   the chain, or link anyway.
4. **Existing end screens**: unknown except Arnak lesson 1. Survey first, read-only (as for Python - Դասեր), then
   sort into add / edit (Best for viewer or a wrong target -> next, times kept) / rebuild (other shapes) / leave.
5. **Studio quirks already handled in the scripts**: search box set from inside the page, double-space titles,
   slow saves and searches (polling), Wi-Fi drops (batch retries), the "leave page?" early return (watch, verify).
   Rebuild: in edit mode the elements stay hidden until the playhead reaches them; the rewritten rebuild mode has not
   run as a script yet, so test it on one video first (or rebuild by hand as on 2026-10-27).

## Parallel and headless (tested 2026-10-28)

- A second tab in the MCP browser does not work: background tabs run at ~2 animation frames per second and a click on
  an end-screen element does not select it.
- A separate headless Chrome (`scripts/non_essential/run_endscreen_headless.js`, the MCP's own playwright-core, the
  installed Chrome, Google/YouTube cookies exported to the gitignored `scripts/.secrets/studio_storage_state.json`):
  - with the default user agent ("HeadlessChrome") Studio shows "You are using an unsupported browser" and the editor
    never loads; with `--ua` set to the normal Chrome string it loads (~12.7 s per video for a survey, at full speed
    while the visible browser runs its own batch);
  - **saving is blocked**: the first edit opens Google's "Verify it's you" dialog (the copied cookies count as a new
    device; the MCP profile, where the user signed in, never gets it). Nothing was saved.
- So: saves only in the visible browser; read-only surveys of the next course can run headless at the same time.

## Steps

1. Decide Q20-Q24 below.
2. Read-only: check each chosen playlist is in lesson order; sort where not (Vahagn first).
3. Read-only Studio survey of the chosen playlists (~10 s per video) -> add / edit / rebuild / leave lists.
4. One generator for umath with a per-playlist config (playlist id and title, lesson rule, skips), in the shape of
   `make_endscreen_jobs_ml.py`, writing jobs with the umath channel id.
5. Switch Studio to umath. Test one add, then batches of ~20 (`make_endscreen_batch.py`), then edit batches, then
   rebuilds (one test first). Keep the Playwright window visible; on this laptop the viewport must stay within
   1280x576 or Studio is cut off on the right.
6. No final recheck when a batch returns a clean result (the user agreed 2026-10-28): the template already checks the
   channel, reads back all three elements before Save and waits for the saved end screen after it, and in the Metric
   run a full recheck never caught a bad save the batch had reported as good. Run `make_endscreen_verify.py` only on
   videos whose batch lost its result (early return on a "leave page?" prompt), retried, or failed. The survey in
   step 3 stays: that is what finds the older end screens.
7. Records in `output/endscreens/umath_*.json`, a DECISIONS entry, a session log; switch Studio back to Metric.

**Time** (Metric rates: ~1 min per new end screen, ~40 s per edit, ~10 s per verified video): Tier 1 about 3-3.5 h of
Studio time plus ~35 min of survey; Tier 2 about the same again.

## Open questions (answer before starting)

- **Q20 Scope:** Tier 1 only, Tier 1 + 2, or everything?
- **Q21 Layout:** same as Metric (10 s; next + playlist + Subscribe; last lesson Best for viewer)?
- **Q22 Unlisted lessons** (Vahagn's 25): skip them in the "next" chain, or link to them?
- **Q23 Arnak:** keep the 2026-10-21 rules (12 -> 13, 12 (2025) -> 13, 13 -> Best for viewer)?
- **Q24 Existing end screens that differ:** same handling as Metric (Best for viewer -> next; anything else asked case by
  case)?
