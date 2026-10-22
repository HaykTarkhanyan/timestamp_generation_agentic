# YouTube captions when yt-dlp is bot-blocked: catch the player's own timedtext request in Playwright

**Symptom.** On 2026-10-22 every yt-dlp call for a public video failed, metadata and `--list-subs`
alike, while the same `fetch_subtitles.py` command had worked two days earlier:

```
ERROR: [youtube] 2NHMdJ5_Nlc: Sign in to confirm you're not a bot. Use --cookies-from-browser or --cookies ...
```

The YouTube Data API (`yt_publish.py`'s token) still answered: channel, uploads, durations. It does
not hand out other channels' caption text, though.

**What did not work, in the Playwright page:**
- `ytInitialPlayerResponse.captions.playerCaptionsTracklistRenderer.captionTracks[0].baseUrl` +
  `&fmt=vtt`, fetched from the page: **HTTP 200 with a 0-byte body**. The URL has no `pot`
  (proof-of-origin token), and YouTube answers such requests with an empty body, not an error.
- Looking for the player's request in `performance.getEntriesByType('resource')` afterwards: the
  only `/api/timedtext` entry was my own test fetch. The player's request was not listed, most
  likely because YouTube fills the page's 250-entry resource timing buffer before captions load.
- `page.waitForResponse(...)` started after the page had loaded: timed out, because captions come
  up by themselves (the signed-in account shows them by default) and the request was already over.

**What worked.** Attach a response listener before `page.goto`, wait for the player's
`/api/timedtext` response for that video id, take its URL (it has `pot=...` and `fmt=json3`), swap
in `fmt=vtt` and fetch it from the page: a full VTT in the same format yt-dlp writes (two-line
cues with per-word `<c>` timing tags), so `parse_vtt()` from
`.claude/skills/youtube-timestamps/scripts/fetch_subtitles.py` cleans it as usual.

```js
const seen = [];
const onResp = r => { if (r.url().includes('/api/timedtext') && r.url().includes(id)) seen.push(r); };
page.on('response', onResp);
await page.goto(`https://www.youtube.com/watch?v=${id}`);
// wait until seen.length (if nothing after ~15 s, click .ytp-subtitles-button), then page.off(...)
const u = seen.at(-1).url();
const vtt = await page.evaluate(async x => (await fetch(x)).text(), u.replace(/([?&])fmt=[^&]*/, '$1fmt=vtt'));
```

Measured: Sevak Mkrtchyan's 10 linear algebra lectures (59-79 min, Armenian auto-captions), 9 of them
in one `browser_run_code_unsafe` call in 80 s, 304-417 KB of VTT each; every transcript ends within
11 s of the video's end. No click was needed for any of them.

**Consequences.**
- Getting a big result out of Playwright: `browser_run_code_unsafe` prints its return value into
  the context, so the VTTs were kept in the page's IndexedDB (same origin across navigations) and
  saved with one `browser_evaluate(..., filename=...)`, which writes the value JSON-encoded.
- Pause the video after each page (`document.querySelector('video').pause()`); it autoplays with sound.
- Not tried: `--cookies-from-browser` for yt-dlp (needs the user's browser; Chrome's app-bound
  cookie encryption gets in the way) or exporting the Playwright context's cookies to a
  cookies.txt (would put a Google session on disk). The page route needs neither.
- Used for: `_knowledge/sevak_linalg_honors/` (README there).
