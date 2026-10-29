# A Studio upload left in the upload dialog stays a "Draft" whatever the API sets; finish it as Unlisted

**Symptom**
The 25 Vahagn re-uploads (uploaded by the user, the upload dialog closed early) had title, description, thumbnail and
`privacyStatus: unlisted` pushed through the API and read back fine, yet Studio's course page listed all 25 as
"Draft" with "Edit draft", and every video page carried "This video is in a draft state". The API has no field for it.

**What finishing does (2026-10-28, 21.1 by hand, then 24 by a driver)**
Edit draft opens the upload dialog with the current metadata: the pushed title and description, "not made for kids"
and no age restriction already set; Initial check done. Next x3 reaches Visibility, where nothing is preselected.
Choose Unlisted, Save: Studio says "Video published" (its word for a finished upload, not for Public). Afterwards the
draft banner is gone, Studio shows Unlisted, and the API still reads unlisted with title and description unchanged.

**Guards that made it safe to run unattended**
Per video: session channel (`ytcfg.get('CHANNEL_ID')`) = the video's channel; the dialog's title box equals the pushed
title (a draft can carry the upload's file-name title, and Save would write it back); "not made for kids" set; before
Save, UNLISTED checked and PUBLIC / PRIVATE not; after Save, the reloaded page without the draft banner. Then the
API read of all of them. Driver: `.playwright-mcp/vahagn_finish_drafts.js` (~25 s a video).

**Consequence**
Re-uploads made through Studio and then edited through the API need this step before publishing; check the course or
channel content list for "Draft" right after the metadata push, not on publishing day.
