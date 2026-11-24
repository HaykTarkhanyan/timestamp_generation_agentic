"""Every transcript of one of our YouTube channels as JSON, one file per playlist (the user, 2026-11-24: "i want to
get ALL transcripts from this channel, in a json format playlist by playlist").

Lists the channel's playlists and uploads in any visibility with yt_publish.py's token, then gets each video's
caption track once:
  - public and unlisted: yt-dlp, the original auto-caption track (`<lang>-orig`); no API quota;
  - private, any yt-dlp failure, and ids passed with --api: the API as the owner (captions.list 50 +
    captions.download 200 = 250 units per video; the default quota is 10,000 a day for all three channels, so
    ~40 videos a day this way).
Raw VTTs are kept in <out>/_vtt/ (the artifact of record); a rerun only fetches what is missing there and rebuilds
every JSON from the cache.

Writes <out> (default transcripts/<channel>/, git-ignored: unlisted and private videos, and the repo is public):
    playlists/<slug>_<playlist id>.json   one per playlist, videos in playlist order; a video in two playlists is
                                          in both files
    playlists/_no_playlist.json           uploads that are in no playlist
    index.json                            counts, one row per playlist, every video without a transcript and why
    _vtt/<id>.<lang>-orig.vtt (yt-dlp), _vtt/<id>.<lang>.api.vtt (API)

Each video: position, video_id, title, url, privacy, published_at, duration_s, channel_title, and transcript =
{language (YouTube's label), kind (asr/standard), source (yt-dlp/api), chars_per_min, armenian_share, usable,
unusable_reason, segments [{start, end, text}] in seconds, text}, or null with transcript_error. usable = at least
half the letters are Armenian (MIN_ARMENIAN_SHARE below); the others are YouTube's ASR run in the wrong language.

Runtime, measured 2026-11-24 on umath with 3 workers: 15 s of listing, then 496 videos in 12 min (~1.5 s a
video); a rerun with everything cached takes ~3 min (it retries the videos with no track). Logs i/n, elapsed and
ETA after every video. From the repo root:

    python scripts/non_essential/fetch_channel_transcripts.py --channel umath --skip-playlists PLz3NrXxHz_CDi6dfEomwnDGHn-R2mrMv3
    pilot: ... --videos ID ID ... --out transcripts/umath_pilot [--api ID ...]
"""
import argparse
import html
import json
import logging
import re
import subprocess
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / ".claude" / "skills" / "youtube-timestamps" / "scripts"))
import yt_publish  # noqa: E402
from fetch_subtitles import slugify, vtt_cues  # noqa: E402

(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs" / "fetch_channel_transcripts.log", encoding="utf-8")])
log = logging.getLogger("fetch_channel_transcripts")

API_UNITS = {"captions.list": 50, "captions.download": 200}
BOT_BLOCK = "confirm you're not a bot"
MAX_BOT_BLOCKS = 5  # consecutive yt-dlp bot blocks before the run stops sending yt-dlp requests


class QuotaExceeded(RuntimeError):
    pass


class NoTrack(RuntimeError):
    """yt-dlp read the video and it has no auto-caption track; the API has none either (pilot 2026-11-24, 2 of 2),
    so no 50-unit captions.list is spent on it."""


# A transcript is usable when at least this share of its letters is Armenian script. YouTube ran ASR on some of our
# Armenian lectures as Romanian, English or Turkish: noise ([Muzică], "foreign", "um") or fluent-looking gibberish
# ("para decir la Ossa gardener Nahor..."). Measured on all 367 umath transcripts (2026-11-24): every such track has
# an Armenian share of 0.0, every real one 0.65-1.0 (the lowest are topology lectures full of Latin math). The track's
# language label is no test: kAhHrwS_-Kk is labelled "de" (the video's metadata language) and is 99% Armenian.
# Neither is density: the gibberish runs to 713 chars/min, a real but quiet solution video has 110.
MIN_ARMENIAN_SHARE = 0.5


# YouTube's Armenian ASR cannot output the question mark ՞ and writes an unknown-token marker where it belongs, cut
# into pieces by the word timing and HTML-escaped in the VTT: "ի&lt;un&gt;նչ" = ի՞նչ, "հա&lt;un" = հա՞. In 279 of
# 308 usable umath transcripts, ~4,700 words (2026-11-24). Where the marker also took the next letter, the only
# possible word is restored (ի<unչ = ի՞նչ, the most common case). YouTube's ">>" speaker-change marks are dropped.
_MARK = r"<(?:unk|un|k)?>?"  # <unk> <unk <un> <un <k> <k <> <
_SWALLOWED_N = re.compile(rf"([իԻոՈ]){_MARK}([չց])")
_MARK_RE = re.compile(_MARK)
_CLOSER_RE = re.compile(r"(?:unk|nk|un|k)?>")  # the rest of a marker cut at a cue boundary
_TRUNCATED = {"կարո՞": "կարո՞ղ", "ինչպե՞": "ինչպե՞ս", "Ինչպե՞": "Ինչպե՞ս", "ինչո՞": "ինչո՞ւ", "Ինչո՞": "Ինչո՞ւ",
              "ո՞ն": "ո՞նց", "Ո՞ն": "Ո՞նց"}
_TRUNCATED_RE = re.compile(r"(?<!\S)(" + "|".join(map(re.escape, _TRUNCATED)) + r")(?=[\s,.:։]|$)")


def clean_caption_text(t: str) -> str:
    t = html.unescape(t).replace(">>", " ")
    t = _SWALLOWED_N.sub(r"\1՞ն\2", t)
    t = _CLOSER_RE.sub("", _MARK_RE.sub("՞", t))
    t = _TRUNCATED_RE.sub(lambda m: _TRUNCATED[m.group(1)], re.sub("՞+", "՞", t))
    return re.sub(r"\s+", " ", t).strip()


def armenian_share(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    return sum("԰" <= c <= "֏" for c in letters) / max(len(letters), 1)


def iso_seconds(duration: str) -> int:
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not m:
        raise ValueError(f"Unexpected ISO 8601 duration: {duration!r}")
    d, h, mi, s = (int(g or 0) for g in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def paged(method, **kw) -> list[dict]:
    items, tok = [], None
    while True:
        r = method(maxResults=50, pageToken=tok, **kw).execute()
        items += r.get("items", [])
        tok = r.get("nextPageToken")
        if not tok:
            return items


class Fetcher:
    """Gets one video's VTT into the cache: yt-dlp first, the API for private videos and as the fallback."""

    def __init__(self, yt, vtt_dir: Path, force_api: set[str]):
        self.yt, self.vtt_dir, self.force_api = yt, vtt_dir, force_api
        self.api_lock = threading.Lock()  # googleapiclient's httplib2 transport is not thread-safe
        self.api_units = 0
        self.quota_out = False
        self.bot_blocks = 0  # consecutive
        self.ytdlp_off = False

    def cached(self, vid: str) -> Path | None:
        api = sorted(self.vtt_dir.glob(f"{vid}.*.api.vtt"))
        if vid in self.force_api:
            return api[0] if api else None
        hits = sorted(self.vtt_dir.glob(f"{vid}.*-orig.vtt")) + api
        return hits[0] if hits else None

    def get(self, vid: str, privacy: str) -> tuple[Path, list[str]]:
        """Returns (vtt path, notes on what failed before it). Raises when no source worked."""
        if hit := self.cached(vid):
            return hit, []
        notes = []
        if privacy in ("public", "unlisted") and vid not in self.force_api:
            if self.ytdlp_off:
                notes.append("yt-dlp skipped (stopped after repeated bot blocks)")
            else:
                try:
                    return self.ytdlp(vid), notes
                except NoTrack:
                    raise
                except Exception as exc:  # noqa: BLE001 - recorded and retried through the API below
                    log.warning(f"{vid}: yt-dlp failed, trying the API: {exc}")
                    notes.append(f"yt-dlp: {exc}")
        return self.api(vid), notes

    def ytdlp(self, vid: str) -> Path:
        cmd = ["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", ".*-orig", "--sub-format", "vtt",
               "--no-progress", "-o", str(self.vtt_dir / "%(id)s.%(ext)s"), f"https://www.youtube.com/watch?v={vid}"]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        if r.returncode != 0:
            err = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else f"exit {r.returncode}"
            if BOT_BLOCK in r.stderr:
                self.bot_blocks += 1
                if self.bot_blocks >= MAX_BOT_BLOCKS and not self.ytdlp_off:
                    self.ytdlp_off = True
                    log.error(f"{self.bot_blocks} yt-dlp bot blocks in a row: no more yt-dlp requests this run")
            raise RuntimeError(err)
        self.bot_blocks = 0
        hits = sorted(self.vtt_dir.glob(f"{vid}.*-orig.vtt"))
        if not hits:
            raise NoTrack("no auto-caption track on YouTube")
        if len(hits) > 1:
            log.warning(f"{vid}: {len(hits)} original tracks {[h.name for h in hits]}, using {hits[0].name}")
        return hits[0]

    def api(self, vid: str) -> Path:
        from googleapiclient.errors import HttpError
        with self.api_lock:
            if self.quota_out:
                raise QuotaExceeded("API quota used up earlier in this run")
            try:
                tracks = self.yt.captions().list(part="snippet", videoId=vid).execute().get("items", [])
                self.api_units += API_UNITS["captions.list"]
                asr = [t for t in tracks if t["snippet"]["trackKind"] == "asr"]
                std = [t for t in tracks if t["snippet"]["trackKind"] == "standard"]
                pick = (asr or std or [None])[0]
                if pick is None:
                    raise RuntimeError(f"API: no caption track (tracks: {[t['snippet'] for t in tracks]})")
                if len(asr) > 1:
                    log.warning(f"{vid}: {len(asr)} asr tracks {[t['snippet']['language'] for t in asr]}, "
                                f"using {pick['snippet']['language']}")
                data = self.yt.captions().download(id=pick["id"], tfmt="vtt").execute()
                self.api_units += API_UNITS["captions.download"]
            except HttpError as exc:
                if exc.resp.status == 403 and b"quota" in exc.content.lower():
                    self.quota_out = True
                    log.error("YouTube API quota exceeded: the rest of the API fetches fail this run")
                    raise QuotaExceeded("API quota exceeded") from exc
                raise
        lang = pick["snippet"]["language"]
        kind = "" if pick["snippet"]["trackKind"] == "asr" else ".standard"
        path = self.vtt_dir / f"{vid}.{lang}{kind}.api.vtt"
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path


def transcript_from(vtt: Path, duration_s: int) -> dict:
    parts = vtt.name.split(".")  # <id>.<lang>-orig.vtt | <id>.<lang>[.standard].api.vtt
    source = "api" if parts[-2] == "api" else "yt-dlp"
    lang = parts[1].removesuffix("-orig")
    segments = [{"start": round(s, 3), "end": round(e, 3), "text": c} for s, e, t in vtt_cues(vtt)
                if (c := clean_caption_text(t))]
    if not segments:
        raise RuntimeError(f"{vtt.name}: no cues parsed")
    text = " ".join(s["text"] for s in segments)
    share = round(armenian_share(text), 3)
    usable = share >= MIN_ARMENIAN_SHARE
    return {"language": lang, "kind": "standard" if "standard" in parts else "asr", "source": source,
            "chars_per_min": round(len(text) / max(duration_s / 60, 1), 1), "armenian_share": share,
            "usable": usable, **({} if usable else {"unusable_reason": (
                f"not Armenian: {share:.0%} of letters Armenian, YouTube recognized the speech as '{lang}'")}),
            "segments": segments, "text": text}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", required=True, choices=sorted(yt_publish.TOKEN_FILES))
    ap.add_argument("--workers", type=int, default=3, help="parallel yt-dlp downloads (API calls stay serial)")
    ap.add_argument("--out", type=Path, help="default transcripts/<channel>")
    ap.add_argument("--videos", nargs="+", help="pilot: only these video ids (playlist files hold only them)")
    ap.add_argument("--api", nargs="+", default=[], help="fetch these ids through the API even when public")
    ap.add_argument("--skip-playlists", nargs="+", default=[],
                    help="playlist ids to leave out entirely (umath: the 235 Armenian Public TV lessons, "
                         "PLz3NrXxHz_CDi6dfEomwnDGHn-R2mrMv3; 0 of 6 sampled had a usable transcript)")
    args = ap.parse_args()
    t0 = time.time()
    out = args.out or REPO / "transcripts" / args.channel
    (out / "_vtt").mkdir(parents=True, exist_ok=True)
    (out / "playlists").mkdir(exist_ok=True)

    yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES[args.channel]
    yt = yt_publish.get_service()
    me = yt.channels().list(part="snippet,contentDetails", mine=True).execute()["items"][0]
    if me["id"] != yt_publish.CHANNEL_IDS[args.channel]:
        raise RuntimeError(f"token belongs to {me['id']}, expected {yt_publish.CHANNEL_IDS[args.channel]}")

    # ---- listing (about 1 unit per 50 rows)
    uploads = [i["contentDetails"]["videoId"] for i in
               paged(yt.playlistItems().list, part="contentDetails",
                     playlistId=me["contentDetails"]["relatedPlaylists"]["uploads"])]
    playlists = paged(yt.playlists().list, part="snippet,contentDetails,status", mine=True)
    log.info(f"{me['snippet']['title']}: {len(dict.fromkeys(uploads))} uploads, {len(playlists)} playlists")
    if unknown := set(args.skip_playlists) - {p["id"] for p in playlists}:
        raise ValueError(f"--skip-playlists not on the channel: {sorted(unknown)}")
    skipped = [p["snippet"]["title"] for p in playlists if p["id"] in args.skip_playlists]
    playlists = [p for p in playlists if p["id"] not in args.skip_playlists]
    if skipped:
        log.info(f"skipping {len(skipped)} playlists: {skipped}")
    items = {}
    for p in playlists:
        items[p["id"]] = sorted(paged(yt.playlistItems().list, part="snippet,contentDetails,status",
                                      playlistId=p["id"]), key=lambda i: i["snippet"]["position"])
    ids = list(dict.fromkeys(uploads + [i["contentDetails"]["videoId"] for v in items.values() for i in v]))
    meta = {}
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,contentDetails,status", id=",".join(ids[k:k + 50])).execute()["items"]:
            meta[v["id"]] = v
    log.info(f"listing done: {len(ids)} unique videos ({len(meta)} visible to the token), {time.time() - t0:.0f}s")
    not_uploads = Counter(v["snippet"]["channelTitle"] for i, v in meta.items() if i not in set(uploads))
    log.info(f"in playlists but not in the uploads list, by channel: {dict(not_uploads)}")
    manual = [i for i, v in meta.items() if v["contentDetails"].get("caption") == "true"]
    if manual:
        log.warning(f"{len(manual)} videos have uploaded captions; this script takes the auto track: {manual}")

    wanted = [i for i in ids if i in meta]
    if args.videos:
        unknown = set(args.videos) - set(meta)
        if unknown:
            raise ValueError(f"--videos not on the channel or its playlists: {sorted(unknown)}")
        wanted = [i for i in wanted if i in set(args.videos)]

    # ---- transcripts (one fetch per unique video)
    fetcher = Fetcher(yt, out / "_vtt", set(args.api))
    results: dict[str, dict] = {}
    t1 = time.time()

    def one(vid: str) -> dict:
        try:
            vtt, notes = fetcher.get(vid, meta[vid]["status"]["privacyStatus"])
            tr = transcript_from(vtt, iso_seconds(meta[vid]["contentDetails"]["duration"]))
            return {"transcript": tr, **({"fallback_notes": notes} if notes else {})}
        except Exception as exc:  # noqa: BLE001 - every failure is logged at ERROR and listed in index.json
            log.error(f"{vid}: no transcript: {exc}")
            return {"transcript": None, "transcript_error": str(exc)}

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(one, vid): vid for vid in wanted}
        for n, fut in enumerate(as_completed(futs), 1):
            vid = futs[fut]
            results[vid] = fut.result()
            tr = results[vid]["transcript"]
            el = time.time() - t1
            what = (f"{tr['source']} {tr['language']} {len(tr['segments'])} segs, {tr['armenian_share']:.0%} "
                    f"Armenian{'' if tr['usable'] else ' UNUSABLE'}" if tr else "MISSING")
            log.info(f"{n}/{len(wanted)} {vid} {what}, {el:.0f}s elapsed, ~{el / n * (len(wanted) - n):.0f}s left")

    # ---- JSON, derived from the cache
    def record(vid: str, position: int | None) -> dict:
        v = meta[vid]
        return {"position": position, "video_id": vid, "title": v["snippet"]["title"], "url": f"https://youtu.be/{vid}",
                "privacy": v["status"]["privacyStatus"], "published_at": v["snippet"]["publishedAt"],
                "duration_s": iso_seconds(v["contentDetails"]["duration"]),
                "channel_title": v["snippet"]["channelTitle"], **results[vid]}

    fetched = time.strftime("%Y-%m-%d %H:%M")
    index_rows, in_playlist = [], set()
    for p in playlists:
        rows, unavailable = [], []
        for it in items[p["id"]]:
            vid = it["contentDetails"]["videoId"]
            in_playlist.add(vid)
            if vid not in meta:
                unavailable.append({"position": it["snippet"]["position"], "video_id": vid,
                                    "title": it["snippet"]["title"]})
            elif vid in results:
                rows.append(record(vid, it["snippet"]["position"]))
        if args.videos and not rows:
            continue
        name = f"{slugify(p['snippet']['title'])}_{p['id']}.json"
        doc = {"channel": me["snippet"]["title"], "channel_id": me["id"], "playlist_id": p["id"],
               "title": p["snippet"]["title"], "description": p["snippet"]["description"],
               "privacy": p["status"]["privacyStatus"], "url": f"https://www.youtube.com/playlist?list={p['id']}",
               "fetched_at": fetched, "pilot_subset": bool(args.videos), "video_count": len(items[p["id"]]),
               "videos_with_transcript": sum(1 for r in rows if r["transcript"]),
               "videos_usable": sum(1 for r in rows if r["transcript"] and r["transcript"]["usable"]), "videos": rows,
               "unavailable_items": unavailable}
        (out / "playlists" / name).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        index_rows.append({"playlist_id": p["id"], "title": p["snippet"]["title"], "file": f"playlists/{name}",
                           "privacy": doc["privacy"], "videos": doc["video_count"],
                           "with_transcript": doc["videos_with_transcript"], "usable": doc["videos_usable"],
                           "unavailable": len(unavailable)})
    loose = [record(vid, None) for vid in dict.fromkeys(uploads) if vid not in in_playlist and vid in results]
    (out / "playlists" / "_no_playlist.json").write_text(json.dumps(
        {"channel": me["snippet"]["title"], "channel_id": me["id"], "title": "Uploads in no playlist",
         "fetched_at": fetched, "pilot_subset": bool(args.videos), "videos": loose}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    missing = [{"video_id": vid, "title": meta[vid]["snippet"]["title"],
                "privacy": meta[vid]["status"]["privacyStatus"], "error": r["transcript_error"]}
               for vid, r in results.items() if r["transcript"] is None]
    trs = {vid: r["transcript"] for vid, r in results.items() if r["transcript"]}
    sources = dict(Counter(t["source"] for t in trs.values()))
    unusable = [{"video_id": vid, "title": meta[vid]["snippet"]["title"],
                 "channel_title": meta[vid]["snippet"]["channelTitle"], "privacy": meta[vid]["status"]["privacyStatus"],
                 "default_audio_language": meta[vid]["snippet"].get("defaultAudioLanguage"),
                 "reason": t["unusable_reason"]} for vid, t in trs.items() if not t["usable"]]
    index = {"channel": me["snippet"]["title"], "channel_id": me["id"], "fetched_at": fetched,
             "pilot_subset": bool(args.videos), "unique_videos": len(results),
             "with_transcript": len(trs), "usable": len(trs) - len(unusable), "by_source": sources,
             "by_language": dict(Counter(t["language"] for t in trs.values())),
             "usable_rule": f"armenian_share >= {MIN_ARMENIAN_SHARE} (share of letters in Armenian script)",
             "api_units_this_run": fetcher.api_units, "no_playlist": len(loose), "skipped_playlists": skipped,
             "playlists": index_rows,
             "missing": missing, "unusable": unusable, "elapsed_s": round(time.time() - t0)}
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info(f"wrote {out}: {len(index_rows)} playlist files + _no_playlist ({len(loose)}), "
             f"{index['with_transcript']}/{len(results)} transcripts {sources} ({index['usable']} usable, "
             f"{len(unusable)} noise), ~{fetcher.api_units} API units, "
             f"{time.time() - t0:.0f}s")
    if missing:
        log.error(f"{len(missing)} videos have no transcript (index.json 'missing'); rerun to retry them")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
