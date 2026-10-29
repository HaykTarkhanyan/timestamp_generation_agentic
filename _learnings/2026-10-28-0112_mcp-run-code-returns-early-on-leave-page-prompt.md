# A Playwright MCP call returns early on a "leave page?" prompt, but its code keeps running

**Symptom:** twice on 2026-10-27 (ML batch `[46]`-`[54]`, Math for ML batch 2) `browser_run_code_unsafe` came back at
once with no result, only:

```
### Modal state
- ["beforeunload" dialog with message ""]: can be handled by browser_handle_dialog
```

`browser_handle_dialog` then said there was no modal state. Watching `page.url()` showed the batch still moving from
video to video; it finished on its own, but its return value (done / skipped / retried) was lost. Stopping the MCP
task with TaskStop did not stop the code either.

**Cause:** the MCP reports a modal dialog as soon as one opens and ends the tool call, while the async function keeps
running inside the Playwright server. The batch's own `page.on('dialog')` handler accepts the prompt a moment later.

**Consequences:**
- When a call returns early like this, watch the page (a read-only loop on `page.url()` until the last video shows a
  saved end screen) and then check those videos with `make_endscreen_verify.py`.
- Start a batch from a clean page (no unsaved edits) so its first navigation does not raise the prompt.
- To really stop running code, close the browser (`browser_close`): the code fails at once, and the next call opens a
  new browser with the same profile and login. This also resets the viewport to the window size.
