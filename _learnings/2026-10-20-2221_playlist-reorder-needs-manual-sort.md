# Reordering a playlist through the API needs the playlist's sort set to Manual

**Symptom:** `yt_publish.py sort-playlist <Arnak's playlist> --by lesson --apply` failed on the first
move (2026-10-20 22:21):

```
HttpError 400 ... "Playlist sort type need to be MANUAL to support position."
reason: 'manualSortRequired'
```

**Cause:** in Studio the playlist's "Default video ordering" was an automatic one (not Manual).
`playlistItems.update` with a `position` only works on Manual playlists, and the Data API has no
field to change that setting. The Complex Analysis playlist sorted fine the same day because it
was already Manual.

**Consequences:**
- Nothing moved: the failure is on the first update, so the order is left as it was (re-read
  right after: unchanged).
- Fix: Studio, Content, Playlists, the playlist, Edit, "Default video ordering", Manual. Then
  rerun the command.
- An automatic "Date published (oldest)" ordering is not a substitute for courses where lessons
  were published out of order (Arnak 4 and 5 went up after 6-9).

**Where the setting is (2026-10-21, Studio's newer playlist page):** Content, Playlists, the playlist,
left menu **Details**, dropdown **"Default video order"**, option **"Manually sorted in YouTube"**
(the others: Date published newest/oldest, Most popular, Date added newest/oldest), then the page's
Save ("Changes saved"). The user could not find it from the playlist's Videos page. Arnak's playlist
was on "Date published (newest)"; after the switch, `sort-playlist --by lesson --apply` moved 8 of 14
and read back 1-11, 12, 12 (2025), 13.
