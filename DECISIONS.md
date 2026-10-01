# Decisions

Numbered, newest at the top. Superseded entries stay, marked as such.

## 1. Lecture corrections go out as a confirmed YouTube comment

- **Decision:** After a video is published, the pipeline reviews the lecture for
  the lecturer's own mistakes and posts them as one comment from the channel -
  but only after the user confirms that comment's content. The user pins it by hand.
- **Date / status:** 2026-10-01, active.
- **Why:** The user asked for it after the ML47 review found real slips (two
  reversed percentages at 0:28:38 and 0:31:34, a wrong claim about what the
  checkpoint holds at 1:21:20). A posted comment is public and the publisher has
  no delete, so a human gate before posting is the safety net.
- **Alternatives rejected:**
  - *Corrections in the description* - the description holds the abstract and
    chapters under a 5,000-char cap (ML46 already hit it), and viewers read
    comments for errata more than descriptions.
  - *Pinning via the API* - the YouTube Data API has no pin method
    (comments: list/insert/update/delete/setModerationStatus only).
  - *Posting automatically* - a wrong correction is worse than none, and only
    Studio can delete it.
  - *Including caption-ambiguous items* - auto-captions garble numbers, so
    "maybe ASR" findings stay out of the comment unless the user confirms
    they said it.
- **What would change this:** the API gaining a pin method (then pin on post);
  the user preferring corrections in the description or a card; or reviews
  that keep finding nothing (then drop the stage to save time).
