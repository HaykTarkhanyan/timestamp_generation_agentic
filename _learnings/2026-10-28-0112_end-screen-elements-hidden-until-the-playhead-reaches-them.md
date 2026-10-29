# In Studio's end-screen editor, existing elements are hidden until the playhead reaches them

**Symptom:** rebuilding Math for ML Դաս 0's old end screen (2026-10-27) failed three times in a row at the same step:

```
locator.boundingBox: Timeout 30000ms exceeded.
  - waiting for locator('.ytp-ce-element:visible').first()
```

An earlier exploration clicked the centre of `.ytp-ce-element.ytp-ce-video` and the panel still said "Subscribe
element"; a screenshot showed only the Subscribe circle while the DOM still counted `video=2` (those two had already
been deleted and stay in the page with no size).

**Cause:** "End screen > Edit" opens the editor with the playhead at 0:00:00:00. The end-screen elements are drawn in
the preview with `visibility: hidden` until the playhead is inside their time range, so Playwright's `:visible` never
matches them. Deleted elements stay in the DOM with a zero-size box. The add flow never hit this because applying a
template moves the playhead to the end.

**What worked (8 rebuilds by hand, then in `endscreen_template.js`):**
- Opening the editor selects the first element, and the panel's trash icon (`ytcp-icon-button[aria-label="Delete
  element"]`) deletes it and selects the next one: delete through the panel only, no clicks on the preview.
- To select an element, click the centre of the first one with a non-zero box (`getBoundingClientRect().width > 0`),
  not `:visible`.
- With every element deleted, the panel lists the templates ("1 video, 1 playlist, 1 subscribe" among them), and Save
  becomes enabled: saving at that point removes the end screen altogether.

**Consequences:** any script that edits an existing end screen must not rely on visibility. The rewritten rebuild mode
follows the manual steps but had not run as a script by 2026-10-28.
