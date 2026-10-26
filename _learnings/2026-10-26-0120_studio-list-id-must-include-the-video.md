# studio.html's list id must include the video, or pages with the same cuts share their edits

**Symptom**
The user, opening the Vahagn batch pages for 20 and 25 May: "when i open the htmls they already show a few cuts
called mine, i think u have a bug somewhere". Both pages opened with the cuts the user had added on the 18 May page.

**Cause**
studio.html keeps the user's edits in localStorage under `studio-edits-<list id>`, and `list_id()` in
find_edit_points.py hashed only the pre-ticked cut list. Once every cut on a camera page became a suggestion
(DECISIONS #45), the five camera batches b0511-b0525 all had zero pre-ticked cuts, so all got list id `97d170e1` and
each page loaded what the previous one had saved.

**Consequences**
- Fixed 2026-10-26: `list_id(scuts, video_id)` hashes the video id with the cuts (b0520 -> `cf3e1038`, b0525 ->
  `9168ac7d`). Pages built before keep their old id until rebuilt.
- The 13 and 18 May lists returned before the fix were checked: none of their cuts matches a cut of the batch before
  (the user had deleted the inherited ones), and none lands on speech.
- Any page whose plan can be identical to another page's (empty plans above all) needs the video in its storage key;
  the same goes for any other per-page localStorage key (the timer already uses `studio-timer-<video id>`).
