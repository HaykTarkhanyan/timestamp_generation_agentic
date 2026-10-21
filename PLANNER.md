# Planner

Live task board for the YouTube work: what is running, what waits on whom, what is next.
Claude updates it at every status change and reads it at the start of a session. Parked topics
go to `DEFERRED_TODO.md`, decisions to `DECISIONS.md`, per-course detail to `_knowledge/`.

**Status:** `DONE` · `RUNNING` (in progress now) · `WAIT-YT` (YouTube is processing) ·
`YOU` (waits on you) · `DECIDE` (your decision needed) · `TODO` (Claude, can start) · `LATER`

Last update: 2026-10-21 16:45 (Munich)

## Now

| What | Status | Next step |
|---|---|---|
| Arnak 2025: title, description, thumbnail pushed (16:04) | `DONE` | "Sparse PCA" -> his "Նոսր ՀԲՎ" (title keeps "(Sparse PCA)"), 3 chapters and the note too. Read back: new title, 35 chapters, 4385 s. Thumbnail from your Canva export (`thumbnails/umath/bazmachap_12_2025.png`) |
| Lessons 12, 13: descriptions pushed (14:30, 15:46) | `DONE` | Read back: 37 and 30 chapters, both 3625 s |
| Blurs | `DONE` | 2025 names strip and lesson 7 by you; 11 and 13 not needed (your call). My Playwright attempt on 13 was discarded, nothing saved |
| Bug: caption parsers dropped one-word lines | `DONE` | Fixed in `caption_words` + `FILLER` and in `fetch_subtitles.py`; transcripts of 13 and 2025 rebuilt; learning `2026-10-21-1330`. The "10:29 hum pause" in 12 was the word "գումար" |

## Arnak - Բազմաչափ վիճակագրություն 1 (channel umath): `DONE` 2026-10-21

All 13 lectures + the 2025 recording edited, chaptered, described and public; playlist sorted, PDF folder
linked; closing email to Arnak sent by you (16:4x). Only open item: end screens for 2-13 + 2025 (`LATER`).

Pipeline per video: plan -> your review -> cuts entered (Claude, batch files) -> Save (you) ->
YouTube processing -> chapters checked on the new captions + description pushed (Claude) -> blur (you).

| Video | Plan | Review | In Studio | Saved | Chapters + description | Blur (you) | Visibility |
|---|---|---|---|---|---|---|---|
| 1-5 | finished earlier | | | | `DONE` (PDF links moved to the new folder) | - | public |
| 6-9 | no cuts needed (longest pause 4.8 s) | | | | `DONE` (titles, thumbnails, PDF links) | 6 `DONE`; 7 `DONE` (you, 2026-10-21) | public |
| 10 `Hv7Jux-KYBk` | `DONE` 15 cuts | `DONE` | `DONE` | `DONE` (996 s) | `DONE` | - | public |
| 11 `WFMoX0xRU6I` | `DONE` 70 cuts | `DONE` (48 + 22) | `DONE` diff identical | `DONE` + your 2 edits (raw 44:32, 47:24), 59:59 | `DONE` 02:15, read back | not needed (you) | public |
| 12 `Bz6aVzkrqbM` | `DONE` 45 cuts, -7.3 min | `DONE` 66 cuts, -8.2 min | `DONE` diff identical | `DONE` 13:33, processed 13:49 (3625 s) | `DONE` 14:30, read back (37 chapters) | - | public |
| 13 `syeGoSopVM0` | `DONE` 15 cuts, -3.9 min (false hum join undone) | `DONE` 34 cuts, -5.0 min | `DONE` diff identical | `DONE`, processed 14:43 (3625 s) | `DONE` 15:46, read back (30 chapters) | not needed (you) | public |
| 2025 Դաս 12 `kJMKNFHYlFU` | `DONE` 43 cuts, -6.8 min | `DONE` 73 cuts, -8.8 min | `DONE` diff identical | `DONE`, processed 15:27 (4385 s) | `DONE` 16:04, read back (35 chapters), new title + thumbnail | `DONE` (you) | public |

| Arnak task | Status | Detail |
|---|---|---|
| Lesson 11: 2 hum gaps left open (21:50, 37:25, ~3 s) | `DONE` | Left as is: "lesson 11 is good enough" (2026-10-21) |
| Playlist order by lesson number | `DONE` | 16:12: "Default video order" set to "Manually sorted in YouTube" (Studio, playlist Details), then `sort-playlist --by lesson --apply`: 1-11, 12, 12 (2025), 13 |
| Make 6-13 + 2025 public | `DONE` | 16:35 via the API (status fields kept), read back: all 14 public |
| End screens (Subscribe + playlist + next video, last 10 s) | `LATER` | Parked (you). Lesson 1 done and saved; 2-13 + 2025 left, scripts ready in `scripts/non_essential/` (DEFERRED_TODO) |
| Leftover folder `output/2026-10-21_Das-11-second-edit-18_WFMoX0xRU6I/` | `DONE` | Deleted 16:10 (you: "delete it"), ~280 MB |
| PDF folder link in the playlist description | `DONE` | 16:14, read back |
| Overview page of all 14 videos | `DONE` | `output/arnak_overview/overview.html` (`scripts/non_essential/playlist_overview.py`); 16 links checked signed out, all OK, every PDF matches its lesson |

## Ashot - Information Theory (channel umath)

| Task | Status | Detail |
|---|---|---|
| Դաս 4, 5: chapters, titles, dates, thumbnails | `DONE` | Pushed and read back on 2026-10-20 |
| Դաս 5 thumbnail shows on YouTube | `TODO` | The API said inProgress on 2026-10-20; recheck |
| Playlist order (`PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy`) | `DECIDE` | Dry run: 3 moves. OK to apply? |
| Դաս 6, 7, 8: download, edit, upload | `YOU` | Sign in to the Drive with the recordings in the Playwright window |

## Repo housekeeping

| Task | Status | Detail |
|---|---|---|
| Studio entry loop as a repo file | `DONE` | `scripts/studio_enter_cuts.js` + `cut_list.py entry-js` (DECISIONS #18); first run: lesson 11 |
| Chapter remap and hum join as repo scripts | `DONE` | `scripts/remap_chapters.py`, `scripts/hum_join.py`, identical to the scratch versions |
| Timeline features: cards hidden, keys, free scroll while playing | `DONE` | User's requests after lesson 12 (DECISIONS #21); tested in Playwright on 13's page; 13 and 2025 rebuilt |
| Timeline view on studio.html | `DONE` | Whole lecture, zoomable spectrogram, uncovered silences in yellow (hum-split pauses as one), editable (DECISIONS #19); pages of 12, 13, 2025 rebuilt |
| Video preview for lesson 12 | `DONE` | 53.5 MB, 12.6 min encode; `--video` added for the .m4a + .mp4 case; fixed the preview code reading `audio_source` from the wrong place in the JSON |
| Video preview for 13, 2025 | `DONE` | 13: 63 MB in 7.7 min (its .m4a and .mp4 0 ms apart); 2025: 73 MB in 14.9 min. Pages rebuilt, not opened |
| Commit today's work | `DONE` | This session's files committed 2026-10-21 ("Arnak course done ..."); Metric, Algebra, ML48-52 and the thumbnail generator are other sessions', left uncommitted |
| "Copy only the needed files, never copy-then-delete" in the global CLAUDE.md | `DECIDE` | Offered on 2026-10-20 after the `rm` incident |
