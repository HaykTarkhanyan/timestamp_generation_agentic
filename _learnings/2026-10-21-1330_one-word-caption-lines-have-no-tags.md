# A one-word caption line has no timing tag, and both caption parsers dropped it

**Symptom**
Arnak lesson 12, 37:34: the plan joined two pause cuts across a "hum" (`hum_join.py`), and the user's
review kept the joined cut. The "hum" is the word "կորելացիա": he says "այստեղ արդեն կասենք
բացասական ... կորելացիա" ("here we'd say negative ... correlation"), so the video would have lost
the key word. The word was missing from `transcript.txt` too, so the plan's reader never saw it.
The timeline's "10:29 hum-split pause" was a pause, the word "գումար", a pause.

**Cause**
YouTube's auto-caption VTT puts a timing tag only *between* words:
```
00:10:32.040 --> 00:10:34.670 align:start position:0%
սա կարելի է ուղղակի այսպես գրել
գումար
```
A new line of one word therefore has no `<c>` tag at all, like the 10 ms placeholder cues.
- `fetch_subtitles.py` `parse_vtt` kept only cues with a `<c>` tag, so it dropped the line as a placeholder.
- `find_edit_points.py` `caption_words()` read a line's first word with `(\S+)<`, which needs a `<`
  after it, so it dropped one-word lines too. On every other line it kept the next word's timing
  tag stuck to the first word ("ըը<00:42:51.680>"), so a hum at a line start never matched `FILLER`.
  `FILLER` was also case-sensitive ("Ըը" at a sentence start) and had no room for punctuation ("Ըհը,").

Fixed 2026-10-21. A placeholder repeats the settled line with a blank line under it, so the test is
"no `<c>` tag and the last line blank" (`parse_vtt`), and `([^\s<]+)` on the cue's second text
line (`caption_words`). `FILLER` is now `re.IGNORECASE` and allows trailing punctuation.

**Evidence**
One-word lines per video, and the transcripts before and after the fix (no old line lost, no
consecutive duplicates):

| Video | One-word lines | transcript.txt lines |
|---|---|---|
| Arnak 11 | 127 | 1062 -> 1189 |
| Arnak 12 | 131 | 1116 -> 1247 |
| Arnak 13 | 114 | 1109 -> 1224 |
| Arnak 2025 Դաս 12 | 139 | 1366 -> 1505 |

Every hum join ever written (`content_cuts.json`, reason "Hum between ..."): 2, and both held a
real word with the fixed parser: lesson 12 37:33.91-37:35.77 ("կորելացիա"), lesson 13
28:22.71-28:24.65 ("Ներողություն"). No other output folder had a join.
Hum-split pause marks on the timeline, before and after: 12: 109 -> 106 groups; 13: 71 -> 70 (17 -> 11
split by a hum); 2025: 142 -> 139 (47 -> 24 split by a hum). `hum_join.py` with the fix: 0 joins in 13 and 2025.

**Consequences**
- Lesson 12: the user split cut 43 around the word before the Studio entry. Lesson 11 had no joins.
- Lesson 13: the join became an unticked "your call" cut; transcripts of 13 and 2025 rebuilt from
  their VTTs (old ones kept as `transcript_before_oneword_fix.txt`).
- Any `transcript.txt` made before 2026-10-21 is missing ~2% of its lines, on top of the lines the
  2026-10-20 fix restored (`_learnings/2026-10-20-1102_vtt-cleaner-dropped-first-line-after-pause.md`).
  Rebuild it before reusing it for chapters or a correctness review.
- A one-word line is often exactly the word said alone between two pauses, which is what
  pause-based cutting removes first. Read the transcript at every join.
