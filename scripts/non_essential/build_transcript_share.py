"""Shareable copy of a channel's transcripts: public videos with a usable transcript only, plus a README.md that
explains the data to the recipient and their LLM (the user, 2026-11-24: "put it in a folder ill share and also one
md with instructions on whats there"; Q10 public only, Q11 usable videos only).

Reads transcripts/<channel>/ (from fetch_channel_transcripts.py) and writes transcripts/share/<name>/ and a .zip:
    README.md        what the data is, its limits, the JSON layout, how to use it (numbers filled from the data)
    index.json       one row per playlist file: title, url, file, videos included / in the playlist
    playlists/*.json one per public playlist that keeps at least one video; slim records (no internal flags)
    other_videos.json  public usable videos that are in no shared playlist
~2 s. From the repo root:

    python scripts/non_essential/build_transcript_share.py --channel umath
"""
import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs" / "build_transcript_share.log", encoding="utf-8")])
log = logging.getLogger("build_transcript_share")

README = """# Transcripts of the YouTube channel "{channel}"

{channel} ("University Mathematics") is an Armenian YouTube channel of university mathematics lectures and short
problem solutions, in Armenian. This folder holds the transcripts of its **public** videos, grouped by playlist, as
JSON. Fetched on {date}.

**In numbers:** {n_videos} videos, {hours:.0f} hours of video, {chars_m:.1f} million characters of transcript, in
{n_files} playlist files plus `other_videos.json`.

## Read this first: what the text is

- **Machine transcripts, not checked by a person.** They are YouTube's automatic captions (speech recognition).
  Nobody has proofread them.
- **Spoken Armenian, with no reliable punctuation.** It reads like speech: repetitions, filler words ("ուրեմն",
  "այսինքն"), unfinished sentences.
- **Math is garbled.** Formulas are spoken aloud and come out as words, Latin letters and fragments, e.g.
  "f-ը a-ից", "sin(πz)". Named theorems and surnames are often misspelled or run together. Do not treat a formula
  in the text as correct; work out the intended meaning from context.
- **What was on the board is missing.** Only speech is transcribed. When the lecturer says "this one" or "here",
  the thing they point at is not in the text.
- The speaker is mostly the lecturer; student questions appear without any marker.

## What is not included

- Videos whose automatic captions are missing or unusable. YouTube made no captions for some videos, and for others
  it recognized the Armenian speech as another language (Romanian, English, Turkish), which produces nonsense. These
  are mostly videos uploaded in 2024 or earlier, so **some courses are incomplete or absent**. The table below shows,
  per playlist, how many of its videos are included.
- These playlists have no usable transcript at all and are left out entirely: {absent}.
- Unlisted and private videos, and the channel's playlist of Armenian Public TV lessons (not the channel's own videos).

## Playlists

| Playlist | Videos included | Videos in the playlist | File |
|---|---|---|---|
{table}

`other_videos.json`: {n_other} public videos that are in none of these playlists.

A video can sit in more than one playlist; it then appears in each of those files ({n_multi} videos do).

## Files

```
README.md            this file
index.json           the playlist table above, as JSON
playlists/*.json     one file per playlist
other_videos.json    videos that are in no playlist (same layout, no playlist fields)
```

## JSON layout

A playlist file:

```json
{{
  "channel": "{channel}",
  "playlist_id": "PL...",
  "title": "Playlist title (Armenian)",
  "description": "Playlist description",
  "url": "https://www.youtube.com/playlist?list=PL...",
  "videos_in_playlist": 97,
  "videos_included": 97,
  "videos": [ ...video records, in playlist order... ]
}}
```

A video record:

```json
{example}
```

- `position`: the video's place in the YouTube playlist, counting from 0. Gaps mean a video was left out (see above).
- `segments`: the transcript as caption lines; `start` and `end` are seconds from the start of the video. A segment
  is a caption line, not a sentence.
- `text`: all segment texts joined with spaces: the whole transcript as one string.
- `duration_s`: video length in seconds; `published_at`: upload time (UTC). The upload date is not always the date
  the lecture was given.

## How to use it

- **Link to a moment in a video:** `https://youtu.be/<video_id>?t=<seconds>`, using a segment's `start` rounded down.
- **One lecture into an LLM:** give it the video's `text`. An hour of lecture is about {chars_per_hour:,} characters
  (median). Armenian text usually takes more tokens than English text of the same length, so check the size with
  your model's tokenizer before sending a whole playlist.
- **Searching:** the speech recognition spells terms inconsistently, so search for a word stem or several variants
  rather than one exact spelling.
- **Load everything in Python:**

```python
import json, pathlib
videos = []
for f in sorted(pathlib.Path("playlists").glob("*.json")):
    pl = json.loads(f.read_text(encoding="utf-8"))
    for v in pl["videos"]:
        videos.append({{"playlist": pl["title"], **v}})
print(len(videos), "video entries (a video in two playlists counts twice)")
```
"""


def slim(v: dict) -> dict:
    t = v["transcript"]
    return {"position": v["position"], "video_id": v["video_id"], "title": v["title"], "url": v["url"],
            "published_at": v["published_at"], "duration_s": v["duration_s"],
            "segments": t["segments"], "text": t["text"]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", default="umath")
    args = ap.parse_args()
    t0 = time.time()
    src = REPO / "transcripts" / args.channel
    date = time.strftime("%Y-%m-%d")
    out = REPO / "transcripts" / "share" / f"{args.channel}_transcripts_{date}"
    if out.exists():
        raise FileExistsError(f"{out} exists; remove it or rename it first")
    (out / "playlists").mkdir(parents=True)
    index = json.loads((src / "index.json").read_text(encoding="utf-8"))
    channel = index["channel"]

    def keep(v: dict) -> bool:
        return v["privacy"] == "public" and v["transcript"] is not None and v["transcript"]["usable"]

    rows, shared_ids, placed, absent = [], {}, set(), []
    for row in index["playlists"]:
        pl = json.loads((src / row["file"]).read_text(encoding="utf-8"))
        if pl["privacy"] != "public":
            log.info(f"left out ({pl['privacy']} playlist): {pl['title']}")
            continue
        vids = [slim(v) for v in pl["videos"] if keep(v)]
        others = {v["channel_title"] for v in pl["videos"] if keep(v)} - {channel}
        if others:
            raise ValueError(f"{pl['title']}: usable videos from other channels {others}; add channel_title to slim()")
        if not vids:
            log.info(f"left out (no usable public video): {pl['title']}")
            absent.append(f"{pl['title']} ({pl['video_count']} videos)")
            continue
        name = Path(row["file"]).name
        (out / "playlists" / name).write_text(json.dumps(
            {"channel": channel, "playlist_id": pl["playlist_id"], "title": pl["title"],
             "description": pl["description"], "url": pl["url"], "videos_in_playlist": pl["video_count"],
             "videos_included": len(vids), "videos": vids}, ensure_ascii=False, indent=1), encoding="utf-8")
        rows.append({"title": pl["title"], "url": pl["url"], "file": f"playlists/{name}",
                     "videos_included": len(vids), "videos_in_playlist": pl["video_count"]})
        for v in vids:
            shared_ids[v["video_id"]] = shared_ids.get(v["video_id"], 0) + 1
            placed.add(v["video_id"])

    # public usable videos that are in no shared playlist (loose uploads, or only in a left-out playlist)
    all_recs = {}
    for f in (src / "playlists").glob("*.json"):
        for v in json.loads(f.read_text(encoding="utf-8"))["videos"]:
            all_recs[v["video_id"]] = v
    other = sorted((slim(v) for k, v in all_recs.items() if keep(v) and k not in placed),
                   key=lambda r: r["published_at"])
    for r in other:
        r["position"] = None
    (out / "other_videos.json").write_text(json.dumps(
        {"channel": channel, "title": "Public videos in none of the playlists", "videos": other},
        ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "index.json").write_text(json.dumps(
        {"channel": channel, "fetched": index["fetched_at"][:10], "playlists": rows,
         "other_videos": {"file": "other_videos.json", "videos": len(other)}}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    uniq = {k: all_recs[k] for k in list(placed) + [r["video_id"] for r in other]}
    rows.sort(key=lambda r: -r["videos_included"])
    table = "\n".join(f"| {r['title']} | {r['videos_included']} | {r['videos_in_playlist']} | `{r['file']}` |"
                      for r in rows)
    ex = slim(next(iter(all_recs[k] for k in placed)))
    ex["segments"] = ex["segments"][:2] + ["..."]
    ex["text"] = ex["text"][:90] + "..."
    example = json.dumps(ex, ensure_ascii=False, indent=2).replace('"..."', "...")
    cph = sorted(len(v["transcript"]["text"]) / v["duration_s"] * 3600 for v in uniq.values() if v["duration_s"] > 600)
    readme = README.format(
        absent="; ".join(absent), chars_per_hour=int(round(cph[len(cph) // 2], -3)),
        channel=channel, date=index["fetched_at"][:10], n_videos=len(uniq),
        hours=sum(v["duration_s"] for v in uniq.values()) / 3600,
        chars_m=sum(len(v["transcript"]["text"]) for v in uniq.values()) / 1e6, n_files=len(rows), table=table,
        n_other=len(other), n_multi=sum(1 for n in shared_ids.values() if n > 1), example=example)
    (out / "README.md").write_text(readme, encoding="utf-8")
    zip_path = shutil.make_archive(str(out), "zip", root_dir=out.parent, base_dir=out.name)
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    log.info(f"wrote {out}: {len(uniq)} videos, {len(rows)} playlist files + {len(other)} other, "
             f"{size / 1e6:.1f} MB; zip {Path(zip_path).stat().st_size / 1e6:.1f} MB; {time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
