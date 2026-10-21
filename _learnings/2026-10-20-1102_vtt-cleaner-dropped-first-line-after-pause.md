# The VTT cleaner dropped the first caption line after every pause

**Symptom**
On Կոմպլեքս անալիզ Դաս 24 (`DqUPATmU_9s`), `transcript.txt` had long holes (14:30 to 14:49, 18:13 to 18:24, 52:24 to 52:30) that looked like board-writing silence. The raw VTT had speech there, for example:
```
00:14:47.079 --> 00:14:49.150 align:start position:0%
 
Պարզվում<00:14:47.519><c> է,</c><00:14:47.680><c> որ</c><00:14:48.079><c> հարմոնիկ</c>
```
That is the sentence that introduces Harnack's theorem. The June chapters put it at 15:00 because the line was missing.

**Cause**
After a pause YouTube restarts the two-line caption window, so the cue's top line is a single space. `parse_vtt` in `.claude/skills/youtube-timestamps/scripts/fetch_subtitles.py` read a cue's lines with `while ... lines[i].strip():`, which treats that " " line as the end of the cue. The block came back empty, had no `<c>` tag, and was skipped as a placeholder. Fixed 2026-10-20 to `lines[i] != ""` (a WebVTT cue ends at an empty line only).

**Evidence**
A 3-cue fixture copied from Դաս 24 at 14:30-14:49: the git HEAD parser returned 1 of 3 lines, the fixed one returns all 3. Words lost by the old parser, measured on all 66 VTTs under `output/` (old vs fixed `parse_vtt`, timestamps not counted):

| Series | Lost |
|---|---|
| Կոմպլեքս անալիզ Դաս 20-25 | 8.5%, 10.7%, 22.7%, 8.9%, 17.0%, 7.9% |
| ML lectures and practicals | 0.3% to 4.8%, rising on the recent long ones (ML48-52: 2.7-4.7%) |
| All 66 | median 1.5% |

Դաս 24 after the fix: 956 lines instead of 779, 4,753 words instead of 3,943.

**Consequences**
- The damage tracks how often the speaker pauses. Sevak Mkrtchyan stops to write on the board, so the Complex Analysis transcripts lost a lot; the ML lectures lost little.
- The lost line is often the one that names the next topic, which pulls chapter boundaries late or onto round numbers. Chapters and correctness reviews made before 2026-10-20 used the lossy transcripts.
- Edit-point detection works on the audio, so the cuts were not affected; only the transcript rows on the review pages had the holes.
- There is no test framework in the repo, so the regression check stays a scratch fixture. Adding pytest would be the user's call.
- Old `transcript.txt` files were not regenerated. Re-run `fetch_subtitles.py --output-dir <dir>` on any folder before reusing its transcript.
