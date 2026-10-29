# Studio opens another channel's video under the last-used channel: check the session before Save

**Symptom:** For Ուղեղամպրոպ webinar 1 (`vkrjiV7SZ08`), `https://studio.youtube.com/video/vkrjiV7SZ08/editor`
opened the editor and took all 39 cuts (dry run and diff OK), but the page was running as Համալսարանական
մաթեմատիկա: the account button read "Համալսարանական մաթեմատիկա · You're a manager", "Channel content" pointed at
`/channel/UCMFONp28jEDHXDBWJyRVYcA`, and `ytcfg.get('CHANNEL_ID')` returned that id. The user spotted it
("why is it saying umath?") just before Save.

**Cause:** One Google account manages Metric, umath, 509 Academy and Ուղեղամպրոպ. Studio keeps the channel last
used (umath, from the Tserunyan work) and still opens an editor link for a video of another managed channel.
Nothing on the editor itself flags the mismatch.

**What we did:** Discard changes, account button > Switch account > Ուղեղամպրոպ (lands on its dashboard), reopen
the editor, check `ytcfg.get('CHANNEL_ID')` = `UCflbCf38rkyrOaRH8ZiloTg`, re-enter (dry run, 1 batch, 299 s; the
first pass on the umath session took 140 s), `cut_list.py diff` identical, Save: dialog "55:14" as predicted,
"Video editing is in progress". Whether a Save from the wrong session would have worked was not tested.

**Consequences:**
- Before entering cuts, check the session channel: `ytcfg.get('CHANNEL_ID')` in the editor tab must be the
  video's channel (`CHANNEL_IDS` in `scripts/yt_publish.py`). Switching channels drops unsaved cuts, so check
  first, not before Save.
- The same video showed "This video is in a draft state" (the upload dialog was not finished). The editor and Save
  worked anyway; the draft has to be completed in the upload dialog before it can be published.
