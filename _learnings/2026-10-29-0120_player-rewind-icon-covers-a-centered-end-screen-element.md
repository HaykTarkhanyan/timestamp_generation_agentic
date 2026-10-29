# The player's rewind icon can cover the center of an end-screen element

**Symptom:** Հավանականություն Դաս 4 (2026-10-28): a click at the center of the Subscribe element, which sat in the
middle of the player, did not select it.

**Cause:** the player's rewind icon was drawn on top of that point, so the click went to the player, not to the
end-screen overlay.

**Fix:** `select()` in `endscreen_template.js` tries 7 points inside the element (center first, then 0.3/0.7
offsets) and clicks the first one where `document.elementFromPoint` lands inside the end-screen overlay and not on
another element. If every point is covered, it fails loudly instead of clicking blind.
