# The end-screen video picker shows every upload with that title: match the card by video id

**Symptom:** the Vahagn batch (2026-10-28) stopped at 21.2 with "two cards start with Դաս 22.1 ...". 11 playlist
videos (22.1-28.4) shared their title with an older replaced upload that was still on the channel (e.g. `4w73Zzmn5YU`).
The unlisted and private twins were never visible to viewers, but Studio's "Search your videos" lists them.

**Cause:** the picker's search covers all of the channel's uploads, whatever their visibility, and the template
matched cards by title only.

**Fix:** the generator writes `next.id`, and the template counts only the card whose thumbnail URL holds that id
(`vi_webp/<id>/` in the card's HTML). It also checks the preview element's id before Save. Videos 61-73 were
rechecked (13/13; none of their targets had a twin), and 21.2-28.4 ran clean by id (24 videos, 19.2 min).

**Consequences:** before an end-screen run on a course that was re-uploaded, either delete the replaced uploads
first (done for Vahagn on 2026-10-28: 44 deleted) or pass the target's id. A title match alone is not enough.
