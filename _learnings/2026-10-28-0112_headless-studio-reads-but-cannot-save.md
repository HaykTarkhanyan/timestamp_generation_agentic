# Headless Chrome can read YouTube Studio but cannot save; background tabs do not work either

**Goal (2026-10-28):** run two end-screen batches at once.

**Second tab in the MCP browser:** a probe opened an editor in a new tab and put the first tab in front. The
background tab loaded (5 s), but ran at ~2 animation frames per second (62 in a foreground or headless page), and a
mouse click on the playlist element did not select it. Unusable for edits.

**Separate headless Chrome** (`scripts/non_essential/run_endscreen_headless.js`: the MCP's playwright-core, channel
"chrome", Google and YouTube cookies from `page.context().storageState()` of the MCP browser):
- default user agent `HeadlessChrome/155.0.0.0`: Studio shows "You are using an unsupported browser or an old browser
  version that may cause YouTube Studio to ..." and the editor never loads;
- `--ua` with the normal string (`... Chrome/155.0.0.0 Safari/537.36`): dashboard and editors load as the right
  channel; a 25-video survey took ~12.7 s per video, the same as the visible browser, while that browser ran its own
  batch;
- **saving fails**: the first edit opens `ytcp-auth-confirmation-dialog`, "Verify it's you. To continue, we need to
  confirm it's really you." with a Next button that leads to a Google sign-in challenge. 3 attempts on Sevak Դաս 1,
  nothing saved. The MCP profile, where the user signed in, never shows it.

**Cause (likely, not proven):** the copied cookies look like a new device to Google, and Studio asks for a step-up
verification before any change. Not pursued: entering credentials is not something to automate.

**Consequences:** saves only in the visible MCP browser; read-only surveys of the next course can run headless at the
same time. The exported cookie file in `scripts/.secrets/` is a full Google session: delete it when headless is no
longer used. The MCP browser itself is the installed Google Chrome (its profile is `mcp-chrome-<workspace hash>`;
the MCP's own Chromium build 1247 is not installed).
