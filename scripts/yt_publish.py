"""Update YouTube video titles, descriptions and thumbnails, and post comments.

By design this tool exposes ONLY these write operations (never destructive):
  - set-title       (videos.update, part=snippet)
  - set-description (videos.update, part=snippet)
  - set-thumbnail   (thumbnails.set)
  - add-comment     (commentThreads.insert) - the lecture-correction comment of
                    the youtube-timestamps skill's last stage, posted only after
                    the user confirms its content. The API cannot pin comments.
  - update-comment  (comments.update) - replace the text of one of the channel's own
                    comments in place (YouTube marks it edited); refuses anyone else's.
  - sort-playlist   (playlistItems.update, position only) - order a playlist by
                    publish date, oldest first, or with --by lesson by the "Դաս N"
                    number that starts each title. Dry run unless --apply; ~1 s and
                    50 quota units per moved video.
plus one read-only helper:
  - recent          (list the channel's newest uploads, so you can grab a video id)

There is no videos.delete call anywhere in this file. Deleting a video is
not possible through this tool even though the OAuth token technically has the
scope for it (YouTube has no "edit-but-not-delete" scope - see YT_PUBLISH_SETUP.md).

One-time setup: see scripts/YT_PUBLISH_SETUP.md

Several channels share one OAuth client, each with its own token. --channel picks it
(before the command); the default is Metric Academy:
  python scripts/yt_publish.py --channel umath recent    # Համալսարանական մաթեմատիկա

Usage:
  python scripts/yt_publish.py auth
  python scripts/yt_publish.py recent [N]
  python scripts/yt_publish.py set-title       <VIDEO_ID> titles.txt
  python scripts/yt_publish.py set-description  <VIDEO_ID> final/ML18.txt
  python scripts/yt_publish.py set-thumbnail   <VIDEO_ID> thumbnails/ML18.png
  python scripts/yt_publish.py add-comment     <VIDEO_ID> output/<dir>/correction_comment.txt
  python scripts/yt_publish.py update-comment  <COMMENT_ID> output/<dir>/correction_comment.txt
  python scripts/yt_publish.py sort-playlist   <PLAYLIST_ID> [--by published|lesson] [--apply]

set-description uploads the description WITHOUT its leading title header. The
local final/ML*.txt files open with "🎬 Վերնագիր՝ <title>", a blank line, a
divider and a blank line, so one file carries both title and description for
copy-paste - but the title is its own YouTube field, and the user was deleting
that header by hand in YouTube Studio after every push (ML36-41).
"""

import argparse
import logging
import re
import sys
import time
from pathlib import Path

# Single scope. force-ssl is required for videos.update (description) and also
# covers thumbnails.set. It is delete-capable at the API level, but this tool
# never calls delete.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SECRETS_DIR = SCRIPT_DIR / ".secrets"
CLIENT_SECRET_FILE = SECRETS_DIR / "client_secret.json"
# --channel -> its OAuth token and the channel id that token must belong to. All
# channels use the one client_secret.json above.
TOKEN_FILES = {
    "metric": SECRETS_DIR / "token.json",        # Metric Academy (the original token)
    "umath": SECRETS_DIR / "token_umath.json",   # Համալսարանական մաթեմատիկա
    "brainstorm": SECRETS_DIR / "token_brainstorm.json",  # Ուղեղամպրոպ
}
CHANNEL_IDS = {
    "metric": "UC5BavugdnUkti3Es7-deZDg",
    "umath": "UCMFONp28jEDHXDBWJyRVYcA",
    "brainstorm": "UCflbCf38rkyrOaRH8ZiloTg",
}
TOKEN_FILE = TOKEN_FILES["metric"]  # set from --channel in main()

# sort-playlist --by lesson: the lesson number that starts a title, "Դաս 12 | ..." -> 12.
# "Դաս 12 (2025) | ..." (another year's recording of that lesson) sorts after the lesson's own video.
LESSON_NUMBER = re.compile(r"^Դաս (\d+)")
OTHER_YEAR = re.compile(r"^Դաս \d+ \(\d{4}\)")

# YouTube hard limits - validate up front so we fail loudly, not mid-upload.
MAX_TITLE_CHARS = 100
MAX_DESCRIPTION_CHARS = 5000
MAX_THUMBNAIL_BYTES = 2 * 1024 * 1024
THUMBNAIL_EXTS = {".jpg", ".jpeg", ".png"}
MAX_COMMENT_CHARS = 10000


def _setup_logging() -> logging.Logger:
    # Windows consoles default to cp1252, which can't encode Armenian titles and would
    # otherwise print them as \uXXXX escapes. Force UTF-8 so `recent` output is readable.
    # StreamHandler() logs to stderr by default, so reconfigure both streams.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

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


TITLE_HEADER_MARK = "🎬"
DIVIDER_CHAR = "─"


def strip_title_header(text: str) -> str:
    """Drop the local-only title header block from a description file's text.

    Expected layout when present: "🎬 ..." / "" / "────..." / "" / body. A file
    with no header (it starts elsewhere) is returned unchanged - there is
    nothing to strip. A file that starts with the header mark but does not
    follow that layout raises, rather than guessing which lines to cut."""
    if not text.startswith(TITLE_HEADER_MARK):
        log.info("No title header at the top of the description; uploading as is")
        return text
    lines = text.split("\n")
    divider = lines[2].strip() if len(lines) > 4 else ""
    if not (divider and set(divider) == {DIVIDER_CHAR}
            and lines[1].strip() == "" and lines[3].strip() == ""):
        raise ValueError(
            "Description starts with the title header mark but not the expected "
            "'🎬 title / blank / divider / blank' layout - refusing to guess what to strip"
        )
    body = "\n".join(lines[4:]).lstrip("\n")
    log.info(f"Stripped title header ({len(text) - len(body)} chars): {lines[0]!r}")
    return body


def set_description(video_id: str, desc_file: str) -> None:
    path = Path(desc_file)
    if not path.exists():
        raise FileNotFoundError(f"Description file not found: {path}")
    text = strip_title_header(path.read_text(encoding="utf-8").strip("\n"))
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


def set_title(video_id: str, title_file: str) -> None:
    """Set a video's title from the first non-empty line of a UTF-8 file (e.g. titles.txt).

    Reads from a file rather than a CLI argument on purpose: passing non-ASCII (Armenian)
    text as a command argument from Git Bash to native Windows Python mangles the encoding.
    """
    path = Path(title_file)
    if not path.exists():
        raise FileNotFoundError(f"Title file not found: {path}")
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise ValueError(f"Title file is empty: {path}")
    title = lines[0]
    if len(title) > MAX_TITLE_CHARS:
        raise ValueError(f"Title is {len(title)} chars, exceeds YouTube limit of {MAX_TITLE_CHARS}")

    yt = get_service()
    resp = yt.videos().list(part="snippet", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        raise ValueError(f"No video found with id {video_id!r} (or not owned by this account)")

    snippet = items[0]["snippet"]
    old_title = snippet.get("title", "")
    snippet["title"] = title  # swap only the title; keep description/categoryId/tags

    yt.videos().update(part="snippet", body={"id": video_id, "snippet": snippet}).execute()
    log.info(f"Updated title for {video_id}: {old_title!r} -> {title!r}")


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


def _read_comment_file(comment_file: str) -> str:
    path = Path(comment_file)
    if not path.exists():
        raise FileNotFoundError(f"Comment file not found: {path}")
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    if not text:
        raise ValueError(f"Comment file is empty: {path}")
    if len(text) > MAX_COMMENT_CHARS:
        raise ValueError(f"Comment is {len(text)} chars, exceeds YouTube limit of {MAX_COMMENT_CHARS}")
    return text


def add_comment(video_id: str, comment_file: str) -> None:
    """Post a top-level comment on a video, as the channel, from a UTF-8 file.

    Reads a file rather than a CLI argument for the same reason as set_title
    (Armenian arguments get mangled on the way to Windows Python). Refuses to post
    a comment whose exact text this channel already has on the video: there is no
    delete in this tool, so a re-run must never leave a duplicate behind. Pinning
    is not available in the YouTube Data API - pin it by hand in YouTube Studio."""
    text = _read_comment_file(comment_file)

    yt = get_service()
    items = yt.videos().list(part="snippet", id=video_id).execute().get("items", [])
    if not items:
        raise ValueError(f"No video found with id {video_id!r} (or not owned by this account)")
    channel_id = items[0]["snippet"]["channelId"]
    title = items[0]["snippet"].get("title", "")
    # the duplicate check looks for comments by the posting channel, which is not the video's
    # owner when commenting on someone else's video (Sevak's lectures, 2026-10-22)
    me = yt.channels().list(part="id", mine=True).execute()["items"][0]["id"]

    page = None
    while True:
        resp = yt.commentThreads().list(part="snippet", videoId=video_id, maxResults=100,
                                        textFormat="plainText", pageToken=page).execute()
        for thread in resp.get("items", []):
            top = thread["snippet"]["topLevelComment"]["snippet"]
            same_author = top.get("authorChannelId", {}).get("value") == me
            same_text = top.get("textOriginal", "").replace("\r\n", "\n").strip() == text
            if same_author and same_text:
                raise ValueError(f"This exact comment is already on {video_id} "
                                 f"(comment {thread['id']}) - not posting a duplicate")
        page = resp.get("nextPageToken")
        if not page:
            break

    body = {"snippet": {"channelId": channel_id, "videoId": video_id,
                        "topLevelComment": {"snippet": {"textOriginal": text}}}}
    resp = yt.commentThreads().insert(part="snippet", body=body).execute()
    log.info(f"Posted comment {resp['id']} on {video_id} ({title!r}), {len(text)} chars. "
             f"The API cannot pin it - pin it in YouTube Studio if wanted.")


def update_comment(comment_id: str, comment_file: str) -> None:
    """Replace the text of one of this channel's own comments with a UTF-8 file's text.

    The API only edits comments the posting channel wrote, so anything else is refused
    up front. Identical text is a no-op (an update would only add YouTube's "(edited)"
    mark). The comment is read back afterwards and must match the file. The comment id
    is printed by add-comment; on YouTube it is the lc= part of the comment's link."""
    text = _read_comment_file(comment_file)
    yt = get_service()
    me = yt.channels().list(part="id", mine=True).execute()["items"][0]["id"]
    items = yt.comments().list(part="snippet", id=comment_id, textFormat="plainText").execute().get("items", [])
    if not items:
        raise ValueError(f"No comment found with id {comment_id!r}")
    snippet = items[0]["snippet"]
    author = snippet.get("authorChannelId", {}).get("value")
    if author != me:
        raise ValueError(f"Comment {comment_id} was written by channel {author}, not this one ({me}): "
                         f"the API can only edit this channel's own comments")
    old = snippet.get("textOriginal", "").replace("\r\n", "\n").strip()
    if old == text:
        log.info(f"Comment {comment_id} already has exactly this text - nothing to update")
        return

    # Check the stored text in the update's own response: comments.list right after an update still
    # returns the old text for a few seconds (2026-10-22, lecture 7 round trip), so a re-read fails falsely
    resp = yt.comments().update(part="snippet", body={"id": comment_id, "snippet": {"textOriginal": text}}).execute()
    if resp["snippet"].get("textOriginal", "").replace("\r\n", "\n").strip() != text:
        raise RuntimeError(f"Comment {comment_id} was updated, but YouTube stored text different from {comment_file}")
    log.info(f"Updated comment {comment_id}: {len(old)} -> {len(text)} chars (YouTube shows it as edited)")


def _playlist_items(yt, playlist_id: str) -> list:
    items, page = [], None
    while True:
        resp = yt.playlistItems().list(part="snippet,contentDetails", playlistId=playlist_id,
                                       maxResults=50, pageToken=page).execute()
        items += resp.get("items", [])
        page = resp.get("nextPageToken")
        if not page:
            return items


def sort_playlist(playlist_id: str, apply: bool, by: str = "published") -> None:
    """Order a playlist oldest first: by publish date (what Studio's "Date published
    (oldest)" sort shows), or by the lesson number that starts each title ("Դաս 12 | ...";
    equal numbers keep their current order). Without apply it only logs the moves. With
    apply it moves the out-of-place items, re-reads the playlist and raises if the order is
    still wrong."""
    yt = get_service()
    items = _playlist_items(yt, playlist_id)
    if not items:
        raise ValueError(f"Playlist {playlist_id!r} is empty or not found")
    log.info("Order now: " + " | ".join(it["snippet"]["title"].split(" | ")[0] for it in items))

    if by == "published":
        unpublished = [it["snippet"]["title"] for it in items
                       if "videoPublishedAt" not in it["contentDetails"]]
        if unpublished:
            raise ValueError(f"No publish date for {unpublished} (private or deleted?) - can't sort")
        target = sorted(items, key=lambda it: it["contentDetails"]["videoPublishedAt"])
    else:
        unnumbered = [it["snippet"]["title"] for it in items if not LESSON_NUMBER.match(it["snippet"]["title"])]
        if unnumbered:
            raise ValueError(f"No 'Դաս N' at the start of {unnumbered} - can't sort by lesson")
        target = sorted(items, key=lambda it: (int(LESSON_NUMBER.match(it["snippet"]["title"]).group(1)),
                                               bool(OTHER_YEAR.match(it["snippet"]["title"]))))
    order = [it["id"] for it in items]
    moves = 0
    for pos, item in enumerate(target):
        if order[pos] == item["id"]:
            continue
        order.remove(item["id"])
        order.insert(pos, item["id"])  # the API inserts the same way: later items shift down
        moves += 1
        log.info(f"{'Move' if apply else 'Would move'} {item['snippet']['title']!r} to position {pos}")
        if apply:
            body = {"id": item["id"], "snippet": {"playlistId": playlist_id, "position": pos,
                                                  "resourceId": item["snippet"]["resourceId"]}}
            yt.playlistItems().update(part="snippet", body=body).execute()

    if not apply:
        log.info(f"Dry run: {moves} of {len(items)} videos would move. Rerun with --apply.")
        return
    # The list lags behind the updates: read 11 s after 21 moves, it still showed the old
    # order, and 30 s later the new one (2026-10-20). So retry before calling it a failure.
    for _ in range(6):
        time.sleep(5)
        after = _playlist_items(yt, playlist_id)
        if [it["id"] for it in after] == [it["id"] for it in target]:
            break
    else:
        raise RuntimeError(f"Playlist order 30 s after the moves still does not match the "
                           f"{by} order")
    log.info(f"Moved {moves} of {len(after)} videos. Order now: "
             + " | ".join(it["snippet"]["title"].split(" | ")[0] for it in after))


def list_recent(n: int) -> None:
    """List the channel's n most recent uploads (read-only) as: id  url  [published]  title."""
    yt = get_service()
    channels = yt.channels().list(part="contentDetails", mine=True).execute().get("items", [])
    if not channels:
        raise ValueError("No channel found for the authorized account")
    uploads_playlist = channels[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    resp = yt.playlistItems().list(
        part="snippet,contentDetails", playlistId=uploads_playlist, maxResults=n
    ).execute()
    videos = resp.get("items", [])
    if not videos:
        raise ValueError("No uploads found on this channel")

    for item in videos:
        vid = item["contentDetails"]["videoId"]
        published = item["contentDetails"].get("videoPublishedAt", "?")
        title = item["snippet"].get("title", "")
        log.info(f"{vid}  https://youtu.be/{vid}  [{published}]  {title}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update YouTube titles, descriptions, thumbnails; post comments (no delete).")
    parser.add_argument("--channel", choices=sorted(TOKEN_FILES), default="metric",
                        help="Which channel's token to use (default: metric)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="Run the one-time OAuth consent and store the token")

    p_recent = sub.add_parser("recent", help="List the channel's most recent uploads (read-only)")
    p_recent.add_argument("n", nargs="?", type=int, default=5, help="How many to list (default 5)")

    p_title = sub.add_parser("set-title", help="Set a video's title (from a file's first line)")
    p_title.add_argument("video_id")
    p_title.add_argument("title_file", help="UTF-8 file whose first non-empty line is the new title")

    p_desc = sub.add_parser("set-description", help="Replace a video's description")
    p_desc.add_argument("video_id")
    p_desc.add_argument("desc_file", help="Path to a UTF-8 text file with the new description")

    p_thumb = sub.add_parser("set-thumbnail", help="Set a video's custom thumbnail")
    p_thumb.add_argument("video_id")
    p_thumb.add_argument("image_path", help="Path to a jpg/png thumbnail (<= 2MB)")

    p_comment = sub.add_parser("add-comment", help="Post a top-level comment as the channel")
    p_comment.add_argument("video_id")
    p_comment.add_argument("comment_file", help="UTF-8 file with the comment text")

    p_upd = sub.add_parser("update-comment", help="Replace the text of one of the channel's own comments")
    p_upd.add_argument("comment_id", help="as printed by add-comment (the lc= part of a comment link)")
    p_upd.add_argument("comment_file", help="UTF-8 file with the new comment text")

    p_sort = sub.add_parser("sort-playlist", help="Order a playlist by publish date or lesson number")
    p_sort.add_argument("playlist_id")
    p_sort.add_argument("--by", choices=["published", "lesson"], default="published",
                        help="publish date (default) or the 'Դաս N' number at the start of each title")
    p_sort.add_argument("--apply", action="store_true", help="Make the moves (default: dry run)")

    args = parser.parse_args()
    global TOKEN_FILE
    TOKEN_FILE = TOKEN_FILES[args.channel]
    log.info(f"Channel: {args.channel} (token {TOKEN_FILE.name})")

    if args.command == "auth":
        yt = get_service()
        # Show which channel the token belongs to: picking the wrong account at consent
        # is the classic mistake (YT_PUBLISH_RUNBOOK.md gotcha 4).
        mine = yt.channels().list(part="snippet", mine=True).execute().get("items", [])
        got = f"{mine[0]['snippet']['title']!r} ({mine[0]['id']})" if mine else "no channel"
        if not mine or mine[0]["id"] != CHANNEL_IDS[args.channel]:
            TOKEN_FILE.unlink()  # a token for the wrong account; drop it so the next auth asks again
            raise ValueError(f"Authorized as {got}, but --channel {args.channel} is "
                             f"{CHANNEL_IDS[args.channel]} - removed {TOKEN_FILE.name}. Run auth "
                             f"again and pick that channel (a Brand Account is its own entry).")
        log.info(f"Authorized as channel {got}. "
                 f"Token stored in {TOKEN_FILE.name} - you won't need to consent again.")
    elif args.command == "recent":
        list_recent(args.n)
    elif args.command == "set-title":
        set_title(args.video_id, args.title_file)
    elif args.command == "set-description":
        set_description(args.video_id, args.desc_file)
    elif args.command == "set-thumbnail":
        set_thumbnail(args.video_id, args.image_path)
    elif args.command == "add-comment":
        add_comment(args.video_id, args.comment_file)
    elif args.command == "update-comment":
        update_comment(args.comment_id, args.comment_file)
    elif args.command == "sort-playlist":
        sort_playlist(args.playlist_id, args.apply, args.by)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log.error(f"Failed: {exc}", exc_info=True)
        sys.exit(1)
