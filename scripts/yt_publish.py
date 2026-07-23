"""Update YouTube video thumbnails and descriptions.

By design this tool exposes ONLY two write operations:
  - set-thumbnail   (thumbnails.set)
  - set-description (videos.update, part=snippet)

There is no videos.delete call anywhere in this file. Deleting a video is
not possible through this tool even though the OAuth token technically has the
scope for it (YouTube has no "edit-but-not-delete" scope - see YT_PUBLISH_SETUP.md).

One-time setup: see scripts/YT_PUBLISH_SETUP.md

Usage:
  python scripts/yt_publish.py auth
  python scripts/yt_publish.py set-description <VIDEO_ID> final/ML18.txt
  python scripts/yt_publish.py set-thumbnail  <VIDEO_ID> thumbnails/ML18.png
"""

import argparse
import logging
import sys
from pathlib import Path

# Single scope. force-ssl is required for videos.update (description) and also
# covers thumbnails.set. It is delete-capable at the API level, but this tool
# never calls delete.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SECRETS_DIR = SCRIPT_DIR / ".secrets"
CLIENT_SECRET_FILE = SECRETS_DIR / "client_secret.json"
TOKEN_FILE = SECRETS_DIR / "token.json"

# YouTube hard limits - validate up front so we fail loudly, not mid-upload.
MAX_DESCRIPTION_CHARS = 5000
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024
THUMBNAIL_EXTS = {".jpg", ".jpeg", ".png"}


def _setup_logging() -> logging.Logger:
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    logger = logging.getLogger("yt_publish")
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
    stream = logging.StreamHandler()
    stream.setFormatter(fmt)
    file_handler = logging.FileHandler(log_dir / "yt_publish.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(stream)
    logger.addHandler(file_handler)
    return logger


log = _setup_logging()


def get_service():
    """Build an authorized YouTube API client, running the OAuth flow if needed."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.valid:
        pass
    elif creds and creds.expired and creds.refresh_token:
        log.info("Refreshing expired access token")
        creds.refresh(Request())
    else:
        if not CLIENT_SECRET_FILE.exists():
            raise FileNotFoundError(
                f"OAuth client secret not found at {CLIENT_SECRET_FILE}. "
                "See scripts/YT_PUBLISH_SETUP.md to create it."
            )
        log.info("No valid token - starting local server for one-time consent")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True, timeout_seconds=600)

    SECRETS_DIR.mkdir(exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def set_description(video_id: str, desc_file: str) -> None:
    path = Path(desc_file)
    if not path.exists():
        raise FileNotFoundError(f"Description file not found: {path}")
    text = path.read_text(encoding="utf-8").strip("\n")
    if len(text) > MAX_DESCRIPTION_CHARS:
        raise ValueError(
            f"Description is {len(text)} chars, exceeds YouTube limit of {MAX_DESCRIPTION_CHARS}"
        )

    yt = get_service()
    resp = yt.videos().list(part="snippet", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        raise ValueError(f"No video found with id {video_id!r} (or not owned by this account)")

    snippet = items[0]["snippet"]
    title = snippet.get("title", "")
    old_len = len(snippet.get("description", ""))
    snippet["description"] = text  # swap only the description; keep title/categoryId/tags

    yt.videos().update(part="snippet", body={"id": video_id, "snippet": snippet}).execute()
    log.info(
        f"Updated description for {video_id} ({title!r}): {old_len} -> {len(text)} chars"
    )


def set_thumbnail(video_id: str, image_path: str) -> None:
    from googleapiclient.http import MediaFileUpload

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Thumbnail image not found: {path}")
    if path.suffix.lower() not in THUMBNAIL_EXTS:
        raise ValueError(f"Thumbnail must be one of {sorted(THUMBNAIL_EXTS)}, got {path.suffix}")
    size = path.stat().st_size
    if size > MAX_THUMBNAIL_BYTES:
        raise ValueError(
            f"Thumbnail is {size} bytes, exceeds YouTube limit of {MAX_THUMBNAIL_BYTES}"
        )

    yt = get_service()
    yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(str(path))).execute()
    log.info(f"Set thumbnail for {video_id} from {path} ({size} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update YouTube thumbnails/descriptions (no delete).")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="Run the one-time OAuth consent and store the token")

    p_desc = sub.add_parser("set-description", help="Replace a video's description")
    p_desc.add_argument("video_id")
    p_desc.add_argument("desc_file", help="Path to a UTF-8 text file with the new description")

    p_thumb = sub.add_parser("set-thumbnail", help="Set a video's custom thumbnail")
    p_thumb.add_argument("video_id")
    p_thumb.add_argument("image_path", help="Path to a jpg/png thumbnail (<= 2MB)")

    args = parser.parse_args()

    if args.command == "auth":
        get_service()
        log.info("Authorized. Token stored - you won't need to consent again.")
    elif args.command == "set-description":
        set_description(args.video_id, args.desc_file)
    elif args.command == "set-thumbnail":
        set_thumbnail(args.video_id, args.image_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log.error(f"Failed: {exc}", exc_info=True)
        sys.exit(1)
