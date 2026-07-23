# YouTube publisher setup (one-time)

`scripts/yt_publish.py` updates a video's **thumbnail** and **description**. It has
**no delete capability** - see the note at the bottom for why that guarantee
comes from the code, not from YouTube's permissions.

> Setting this up for a **new channel / account**? Follow `YT_PUBLISH_RUNBOOK.md` instead -
> it's the full step-by-step with every gotcha (secret hashing, 7-day token expiry, consent flow).

## 1. Install dependencies

```bash
uv pip install --python "C:/Users/hayk_/AppData/Local/Programs/Python/Python310/python.exe" \
  google-api-python-client google-auth-oauthlib google-auth-httplib2
```

## 2. Create a Google Cloud OAuth client (browser, ~5 min)

1. Go to https://console.cloud.google.com and create (or pick) a project.
2. **APIs & Services > Library** > search **YouTube Data API v3** > **Enable**.
3. **APIs & Services > OAuth consent screen**:
   - User type: **External**, fill in app name + your email.
   - Under **Test users**, add your own Google account (the one that owns the
     channel). This lets the unverified app work for you without review.
4. **APIs & Services > Credentials** > **Create Credentials** > **OAuth client ID**:
   - Application type: **Desktop app** > Create > **Download JSON**.
5. Save that file as: `scripts/.secrets/client_secret.json`

   (`scripts/.secrets/` is gitignored - credentials never get committed.)

## 3. Authorize once

```bash
python scripts/yt_publish.py auth
```

A browser opens; approve the consent. A refresh token is saved to
`scripts/.secrets/token.json`, so you won't be asked again.

## 4. Use it

`VIDEO_ID` is the part after `youtu.be/` - it's also the suffix on our output
folder names (e.g. `output/2026-07-22_18-Random-Forest..._dQThBIudT14`).

```bash
# update description from a paste-ready file
python scripts/yt_publish.py set-description dQThBIudT14 final/ML18.txt

# set the custom thumbnail
python scripts/yt_publish.py set-thumbnail  dQThBIudT14 thumbnails/ML18.png
```

## Notes

- **Quota:** each `set-description` and `set-thumbnail` costs 50 units; the
  default daily quota is 10,000. A whole batch of lessons is nowhere near it.
- **Custom thumbnails** require a phone-verified channel. You already use custom
  thumbnails, so you're set.
- **Description edits replace the whole box.** The script preserves the existing
  title, category, and tags and swaps only the description text.

## Why "unable to delete" is enforced here, not by Google

YouTube's OAuth scopes are coarse: `videos.update` (edit description) and
`videos.delete` require the **same** scope (`youtube.force-ssl`). There is no
"edit-but-not-delete" scope. So the token this tool holds is technically
delete-capable. The guarantee that it *won't* delete comes from two things:

1. **This script has no `videos.delete()` call** anywhere in it.
2. `.claude/settings.json` denies the quick inline bypass routes
   (`python -c`, `curl`, `wget`) so those can't be used to hand-roll a delete.

This is a practical guardrail, not a cryptographic wall: anyone (or any agent)
who can write a new Python file and run it could still call delete with the same
token. If you ever want a hard, injection-proof guarantee, move the token into a
separate local service that only exposes description/thumbnail routes.
