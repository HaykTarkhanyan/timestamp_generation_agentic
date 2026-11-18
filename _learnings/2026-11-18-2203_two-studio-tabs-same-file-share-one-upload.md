# Two Studio tabs uploading the same file can end up as one video: upload a renamed copy

**Symptom** (LLM [05]/[06], 2026-11-18): the recording went into Studio from two tabs, Create -> Upload in each, as
on LLM [02]/[03]. Both tabs then showed the same video link (`youtu.be/7FhEiQBUgK0`) and the same progress
("Uploading 21% ... 7 minutes left"). The second tab's dialog was a second window on the first upload. Its title box
took "[06] x" and autosaved it over the first tab's "[05] x".

**Cause:** Studio resumed the upload it already had for that file instead of starting a new one. Most likely it
matches on name, size and modification time. The tab didn't matter. On 2026-11-09 the same file in two tabs gave two
videos, so the matching depends on timing (that time the first upload may already have finished, or Studio behaved
differently).

**Fix that worked:** `cp` the recording to a new name in the scratchpad
(`LLM06_GMT20261118-160036_Recording_2560x1440.mp4`; the copy also gets a new modification time) and upload that
from a fresh tab. That gave its own video, `C4Zcf1K51FI`. The shared upload finished normally. I closed the
duplicate tab only after "Upload complete", retyped "[05] x" in the first tab, and `yt_publish.py recent 3` read
both titles back correctly.

**Consequences:**
- For a lesson pair, upload a renamed copy for the second video from the start; don't upload the same file twice.
- After the second upload starts, check that the two tabs show **different** video links before typing titles.
- `find_edit_points.py --audio` still takes the original file for both videos: the copy is only for the upload.

**Also this session:** `find_edit_points.py --speech-map 0:00:00 2:02:32` over the whole 2-hour WAV failed with
`_ArrayMemoryError: Unable to allocate 7.32 MiB` with 2.5 GB of 15.6 GB RAM free. The full audio as float64 is about
0.9 GB, plus filter copies. Windows' commit limit probably ran out, not physical RAM. Printing the map in 25-minute
windows worked (4 calls, a few seconds each).
