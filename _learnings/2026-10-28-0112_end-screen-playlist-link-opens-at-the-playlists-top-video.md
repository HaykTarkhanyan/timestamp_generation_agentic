# An end-screen playlist element opens the playlist at its top video

**Symptom:** the you-should-know plugin warned (2026-10-27) that the ML course playlist, sorted newest first, would
start end-screen viewers at the newest lecture. Web search did not settle it.

**Check:** the watch page of `BaQ0-hrcRtI` (Python - Դասեր, playlist position 1) carries its end screen in
`ytInitialPlayerResponse.endscreen.endscreenRenderer.elements`. The PLAYLIST element's endpoint:

```
{"videoId":"3MuWl8UOeHY","playlistId":"PLfLD2TpGxVUwNhdJWh3lpAJLFBjV6ilqv", ...}
```

`3MuWl8UOeHY` is position 0 of that playlist. So the link opens the playlist at its top video and autoplay runs in
playlist order.

**Consequences:**
- A newest-first course playlist (Metric's ML course and Math for ML) sends end-screen viewers to the newest lecture,
  then backward. The user kept both newest first anyway (Q11, DECISIONS #51).
- The "next video" element should therefore follow lesson order, not playlist order, for newest-first playlists.
- The endpoint is built from the playlist's current order, so re-sorting the playlist later fixes every end screen at
  once; no end screen needs re-editing.
