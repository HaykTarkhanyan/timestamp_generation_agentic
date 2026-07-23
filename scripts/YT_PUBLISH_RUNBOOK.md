# YouTube Publisher: new-account setup runbook

Step-by-step to wire up `yt_publish.py` for a **new channel / Google account**, with the
exact clicks and every gotcha we hit the first time. Follow top to bottom; budget ~10-15 min.

The result: two commands (`set-description`, `set-thumbnail`) that edit that channel's
videos. No delete capability (see `YT_PUBLISH_SETUP.md` for why that lives in the code).

---

## Fill these in as you go

| Thing | Value |
|---|---|
| Google account that **owns the channel** | `________________` |
| GCP project name | `youtube-publisher` (or your choice) |
| Project ID (auto-assigned) | `________________` |
| OAuth Client ID | `________________` |
| Secret file | `scripts/.secrets/client_secret.json` |
| Token file (created by auth) | `scripts/.secrets/token.json` |

> The account must be the one that **owns the videos**. If the channel is a Brand Account,
> use the Google account that manages it. Editing fails silently-ish (404 "no video found")
> if you authorize the wrong account.

---

## 0. Dependencies (once per machine)

```bash
uv pip install --python "C:/Users/hayk_/AppData/Local/Programs/Python/Python310/python.exe" \
  google-api-python-client google-auth-oauthlib google-auth-httplib2
```

## 1. Create the GCP project

Open `https://console.cloud.google.com/projectcreate`, name it `youtube-publisher`, **Create**.
Wait ~5s; the console switches to the new project. Note the Project ID (e.g. `youtube-publisher-503222`).
No billing account is needed for the YouTube Data API.

## 2. Enable YouTube Data API v3

Go to `https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=<PROJECT_ID>`
and click **Enable**. It redirects to the API overview when done.

## 3. Configure the OAuth consent screen (Google Auth Platform)

`https://console.cloud.google.com/auth/overview?project=<PROJECT_ID>` -> **Get started**, then:
- **App name**: `youtube-publisher`; **User support email**: the channel account.
- **Audience**: **External** (Internal is greyed out for personal Gmail accounts).
- **Contact email**: the channel account.
- Tick the User Data Policy agreement -> **Continue** -> **Create**.

## 4. Publish to Production  (IMPORTANT: do not skip)

`https://console.cloud.google.com/auth/audience?project=<PROJECT_ID>` -> **Publish app** -> **Confirm**.

**Why:** refresh tokens issued while the app is in *Testing* status **expire after 7 days**, so
you would have to re-authorize weekly. In *Production* the token persists indefinitely.
The only cost is a one-time "Google hasn't verified this app" screen during consent (step 8),
which you click through. That is expected for a personal app using the sensitive
`youtube.force-ssl` scope. The 100-user cap on unverified apps is irrelevant (you are 1 user).

## 5. Create the OAuth client (Desktop)

`https://console.cloud.google.com/auth/clients/create?project=<PROJECT_ID>` ->
**Application type: Desktop app** -> **Create**. Copy the **Client ID** from the dialog.

## 6. Get the client secret  (GOTCHA - read this)

Google now **hashes** client secrets. The full secret is shown **only once**:
- in the "Download JSON" button at creation, **or**
- in the copy button when you add a secret later.

The detail page shows it masked forever (`****xxxx`) and says "viewing and downloading is no
longer available." So do **not** rely on being able to read it back.

**The reliable way to grab the plaintext secret** (works even if you lost the download):
1. Open the client: `https://console.cloud.google.com/auth/clients/<CLIENT_ID>?project=<PROJECT_ID>`
2. Open **Information and summary** (top-right toggle) -> **Client secrets** section.
3. Click **Add secret**. A new secret appears with a **Copy to clipboard** button whose tooltip/label
   is the full plaintext value: `GOCSPX-................`. Copy that.
4. (Optional cleanup) Disable + delete the old secret so only one remains.

> Why we do this: browser-download of the JSON does not always land where you can find it.
> Playwright/automation downloads in particular do **not** go to your Downloads folder, and the
> MCP does not persist them. Reading the plaintext off the copy button and building the JSON
> by hand (next step) sidesteps the whole download-hunt.

## 7. Write `scripts/.secrets/client_secret.json`

This path is gitignored (`**/.secrets/`), so it never gets committed. Structure for a Desktop client:

```json
{
  "installed": {
    "client_id": "<CLIENT_ID>.apps.googleusercontent.com",
    "project_id": "<PROJECT_ID>",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "GOCSPX-................",
    "redirect_uris": ["http://localhost"]
  }
}
```

## 8. Authorize

```bash
python scripts/yt_publish.py auth
```

This starts a local server and opens a browser. Complete the consent **as the channel-owner account**:
1. Choose the account -> 2. "Google hasn't verified this app" -> **Advanced** ->
**Go to youtube-publisher (unsafe)** -> 3. Grant *"See, edit, and permanently delete your YouTube
videos, ratings, comments and captions"* (`youtube.force-ssl`) -> **Continue**.

The browser redirects to `http://localhost:<port>/...` and `token.json` is saved (with a
`refresh_token`). You will not be asked again.

### If consent times out or the browser is on the wrong account
- The flow waits up to **600s** (`timeout_seconds=600` in `get_service`).
- Run unbuffered to print the URL so you can open it yourself in the right browser/account:
  ```bash
  python -u scripts/yt_publish.py auth
  ```
  Copy the `Please visit this URL to authorize this application: https://...` line and open it
  in a browser already signed in to the channel account. The `redirect_uri` port belongs to the
  still-running process, so complete it before the timeout.
- Tip: if you drive it in an automation browser (e.g. Playwright), a **fresh** Google login is
  usually blocked as "not secure", but it works fine if that browser profile is **already** logged
  into the channel account. Navigate that browser to the printed auth URL and click through.

## 9. Use it

```bash
python scripts/yt_publish.py set-description <VIDEO_ID> final/ML18.txt
python scripts/yt_publish.py set-thumbnail  <VIDEO_ID> thumbnails/ML18.png
```

`VIDEO_ID` is the `youtu.be/<id>` id, which is also the suffix on our `output/..._<id>` folder names.

---

## Gotchas summary (all of these bit us once)

1. **Secret hashing** - full secret only at creation or via Add-secret copy button. Step 6.
2. **Downloads vanish** - build `client_secret.json` from the copied plaintext, don't hunt for the file.
3. **7-day token expiry** - publish to Production (step 4), or you re-auth weekly.
4. **Wrong account** - authorize the account that owns the videos, not your personal one.
5. **Consent timeout** - longer timeout + unbuffered URL (step 8).
6. **Automation-browser login** - Google blocks fresh sign-in; use an already-logged-in profile.

## Reference

- **Scopes:** `videos.update` (edit description) and `videos.delete` require the **same** scope
  (`youtube.force-ssl`); there is no "edit-but-not-delete" scope. That is why the no-delete
  guarantee lives in the code, not in permissions. `thumbnails.set` also works under this scope.
- **Quota:** `set-description` and `set-thumbnail` cost 50 units each; default is 10,000/day.
- **Thumbnails:** jpg/png, <= 2 MB, 1280x720 (16:9). Custom thumbnails require a phone-verified channel.
- **Descriptions:** 5000-char limit. `videos.update` replaces the whole snippet, so the script
  fetches the current one and swaps only the description (preserving title/category/tags).

## Worked example (the account we set up first)

| | |
|---|---|
| Account | `metric.am.academy@gmail.com` (Metric Academy channel) |
| Project | `youtube-publisher` / `youtube-publisher-503222` |
| Client ID | `468185191424-f1nbn6fncumd3do97qug3cqo7b7evs8e.apps.googleusercontent.com` |

(The client secret is not recorded here on purpose; it lives only in `scripts/.secrets/`, gitignored.)
