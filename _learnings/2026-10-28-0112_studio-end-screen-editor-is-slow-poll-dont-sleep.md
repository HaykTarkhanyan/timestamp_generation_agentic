# Studio's end-screen editor is slow and uneven: poll for the state, never trust a fixed wait

Each of these stopped a batch on 2026-10-27 with a fixed wait, and each was fixed by polling:

| What | Seen | Fixed wait that failed | Now |
| --- | --- | --- | --- |
| Editor load | ML [45]: no "Add end screens" button after 9 s, page title still "YouTube Creator Studio" | 9 s | wait for "End screen" in the page, up to 40 s |
| Video search | ML [17]: 0 results; same query a minute later: 1 result at 2 s; "Random Forest": 0 at 2 s and 6 s, 1 at 10 s | 4 s | poll for the matching card, up to 20 s |
| Save | ML [12]: editor did not show the saved end screen at 7 s; a fresh reload showed it saved | 7 s | poll for "End screen Edit" + "Playlist:", up to 30 s |
| Element titles after load | 5 of 56 ML videos listed `Video: ...` / `Playlist: ...` for 0-3 s | 2.5 s | wait until no label ends in "...", up to 30 s |

Two more traps from the same run:
- **Wi-Fi drops** (`ERR_NAME_NOT_RESOLVED`, `ERR_NETWORK_CHANGED` in the console) made one Save fail with Studio's
  banner "There was a problem in processing your video. As a result your recent edits were not saved." (ML [46]).
  Batches now retry a failed video twice after 60 s; a retry of a video that did save stops at "ALREADY" instead of
  adding a second end screen.
- **Double spaces** in titles ("գուշակել  |", "թ-մ  |") are collapsed by `innerText`, so an exact title match fails
  on the card and on the panel label. Compare with whitespace collapsed on both sides.

Measured rates (visible browser, umath and Metric, 2026-10-27/28): ~50 s per new end screen, ~35-48 s per video-only
edit, ~10-13 s per read-only check.
