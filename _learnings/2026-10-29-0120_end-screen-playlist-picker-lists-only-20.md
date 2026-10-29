# The end-screen playlist picker lists only 20 of the channel's playlists

**Symptom:** on umath (2026-10-28) the playlist "Մաթեմատիկական անալիզ 3 (տվյալագետների համար)" was not in the picker's
list, so the template could not click it.

**Cause:** the "Playlist: ..." dialog shows only 20 of the channel's playlists. umath has 30.

**Fix:** if the name is not listed and the job has `playlistId`, type
`https://www.youtube.com/playlist?list=<id>` into the dialog's "Any playlist on YouTube" box (`#search-any`), press
Enter, then click the item by name. It needs real keyboard input (`keyboard.insertText`). Setting the value from the
page, which works for the video search (learning 2026-10-28-0112), searched nothing here.
