# A YouTube OAuth token belongs to one channel, not to the Google account

**Symptom:** Authorizing `yt_publish.py --channel umath` as the user's personal Google
account, which manages Համալսարանական մաթեմատիկա, gave the wrong token twice:

| Try | `channels.list(mine=True)` after consent |
|---|---|
| 1 | no items (a token with no channel) |
| 2 | the user's personal channel (same Google account, other entry in the channel list) |
| 3 | `'Համալսարանական մաթեմատիկա'` (UCMFONp28jEDHXDBWJyRVYcA) |

**Cause:** One Google account managing several Brand Accounts is several identities. After
the account picker, Google shows a second list of channels, and the token is issued for the
entry picked there. "Pick the right Google account" was correct and not enough.

**Consequences:**
- Each channel gets its own token, and `auth` compares the token's channel with
  `CHANNEL_IDS` in `scripts/yt_publish.py`. On a mismatch it deletes the token, so a wrong
  one is never reused. Before that check, a channel-less token was saved and would have been
  reused silently.
- Opening the consent URL with `&prompt=select_account%20consent` appended makes Google show
  both pickers instead of reusing a previous choice.
- Steps are in `scripts/YT_PUBLISH_RUNBOOK.md`, "Another channel on the same project".
