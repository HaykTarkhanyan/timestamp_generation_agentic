# End-screen time boxes: the minutes' width follows the video's length

**Symptom:** the Vahagn batch (2026-10-28) stopped at 4.2 (10:01 long): the start "9:50:14" never matched Studio's
"09:50:14". After a fix that always padded the minutes, 6.1 (7:46 long) failed the other way: "07:35:18" against
Studio's "7:35:18".

**Cause:** under an hour Studio writes M:SS:FF or MM:SS:FF, and the minutes take the width of the end time, which comes
from the video's length. A 10:01 video shows "09:..." for the start, a 7:46 one shows "7:...".

**Fix:** `back()` in `endscreen_template.js` pads the start's minutes to the width of the end time's minutes field.
Related: learning 2026-10-27-1813 (Studio's trim time boxes under ten minutes are M:SS:FF).
