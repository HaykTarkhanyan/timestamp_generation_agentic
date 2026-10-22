# Studio stores every cut one frame later than typed on some uploads; enter with --type-shift -1

**Symptom.** Papikian Դաս 20 (`VCK3I6CkJI8`): batch 1 failed on its first cut, "cut 1 (0:00:08:15-0:00:10:14)
not in Studio after Cut". Studio held `0:00:08:16-0:00:10:15`. A single test cut showed it is systematic:
the editing row read back exactly what was typed (`0:00:24:05`, `0:00:28:01`), and after Cut the trim
markers said `0:00:24:06-0:00:28:02`. Դաս 22 (`txvgnlhu78E`) did the same (typed 0:00:08:17-0:00:10:04,
stored 0:00:08:18-0:00:10:05). Դաս 16, 17, 18-19, 21 and 23 stored exactly what was typed.

**Cause: not found in the source files.** All seven were made the same way (ASOF intro + Zoom recording,
stream copy) and ffprobe shows the same structure for the shifted and the exact ones: `r_frame_rate`
25/1, `start_time` 0.021, average frame rate just under 25 (Դաս 19: 40735875/1629451, Դաս 20:
49166625/1966681). So it is something in YouTube's processed copy of that particular upload. Not tested.

**What works.** `python scripts/cut_list.py entry-js --output-dir <dir> --type-shift -1`: the batch files
then type every time one frame early, and every check still compares against the planned times, so a
cut that does not land exactly still stops the batch. Դաս 20 (65 cuts) and 22 (71 cuts) went in with it,
and the diff against the user's list was identical frame for frame on both.

**How to notice it.** Run batch 1 unshifted. On an affected upload it fails on cut 1 within seconds with
"not in Studio after Cut", and the markers show the cut one frame later at both ends. Delete that cut
(the panel's Delete, then "Delete Cut" in the confirmation dialog), regenerate with `--type-shift -1`,
run again. Do not just re-run: the batch's "already in Studio" check compares exact times, so it would
enter cut 1 a second time over the shifted one.

**Two more things from the same session.**
- Rejecting (cancelling) a `browser_run_code_unsafe` call in the chat does not stop the code already
  running in the browser. Դաս 18-19's batch 2 was "rejected" and still entered cuts 16-30 by itself;
  a check moments later found cut 30 half-made, then finished. Read Studio's state before re-running.
- Studio's "New video length" (tooltip and Save dialog) is the remaining length rounded *down* to the
  second (1:07:52 for 1:07:52.80). After processing, the API's `contentDetails.duration` reads one second
  more (1:07:53). Both are fine; compare like with like.
