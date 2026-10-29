# Studio's "Choose specific video" search box can ignore typing: set its value from the page

**Symptom:** in the end-screen video picker (2026-10-27, Python Libraries [07]) the search found nothing: the dialog
kept listing the 50 newest uploads. Checks: the input read `""` after `keyboard.type`, after `locator.fill` and after
`focus()` + typing; `document.activeElement` stayed `BODY`; a pointer click was intercepted
(`<div class="edit-overlay ...ytve-endscreen-editor-preview-overlay-item"> intercepts pointer events`). The same code
had worked one video earlier, and a bigger window (1500x950) did not help.

**Cause:** not found. The input (`#search-yours`, inside the dialog's tab header) does not keep keyboard focus while the
end-screen editor is open; the editor appears to take focus back.

**What works** (now in both end-screen templates):

```js
const i = document.querySelector('tp-yt-paper-dialog #search-yours');
i.value = query; i.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
for (const t of ['keydown', 'keypress', 'keyup'])
  i.dispatchEvent(new KeyboardEvent(t, { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, composed: true }));
```

`'Logging'` set this way returned 2 cards, `[08] Logging...` first. Used for every end screen since (several hundred).

**Consequences:** results can take ~10 s to arrive (0 cards at 2 s and 6 s, the match at 10 s), so poll for a card
whose text starts with the full target title rather than waiting a fixed time.
