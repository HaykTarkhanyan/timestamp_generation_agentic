# A video with info cards has two Edit buttons in the editor: open the end screen by its own link

**Found on:** Հավանականություն Դաս 4 (2026-10-28), an end-screen rebuild.

**Cause:** when a video has info cards, the editor's entry panel shows a second Edit button (for the cards) next
to the end screen's. A locator for a generic "Edit" can hit either one.

**Fix:** `page.getByRole('link', { name: 'End screen Edit' })`, the end screen's own accessible name. It's now used in
`endscreen_template.js`, `endscreen_edit_template.js` and `make_endscreen_verify.py`.
