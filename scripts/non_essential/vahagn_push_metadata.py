"""Put the local drafts onto the Vahagn 'fixed' uploads (DECISIONS #38): title, description, unlisted, thumbnail,
the course playlist. Dry run unless --apply. Reads everything back after applying.

    python scripts/non_essential/vahagn_push_metadata.py --chapters raw                  # dry run, all 25
    python scripts/non_essential/vahagn_push_metadata.py --chapters raw --apply          # uncut uploads
    python scripts/non_essential/vahagn_push_metadata.py --chapters edited --description-only --apply 21.1
        # after a piece's cuts are saved in Studio: its chapters on the edited timeline

--chapters raw puts timestamps_raw.txt into the description (right for an upload whose cuts are not entered yet);
edited keeps the remapped chapters of edited_predicted/description.txt (right once the Studio cuts are saved).
The upload -> section map is built once from the upload titles ('VidSection 23 1 a fixed') and kept in
_knowledge/vahagn_linalg/uploads_fixed.json, since the titles change on the first push.
Quota: 150 units per video (update 50, thumbnail 50, playlist insert 50), 50 with --description-only.
Expected: ~3 s per video (~1.5 min for 25).
"""
import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

PLAYLIST = "PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM"
WRITABLE = ("embeddable", "license", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")
MAP_FILE = REPO / "_knowledge/vahagn_linalg/uploads_fixed.json"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_push_metadata.log", encoding="utf-8")])
log = logging.getLogger(__name__)


def iso_s(d: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d)
    return int(m[1] or 0) * 3600 + int(m[2] or 0) * 60 + int(m[3] or 0)


def upload_map(yt) -> dict:
    """section -> video id of the 'fixed' uploads; built from the titles once, then read from MAP_FILE."""
    if MAP_FILE.exists():
        return json.loads(MAP_FILE.read_text(encoding="utf-8"))
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    found, token = {}, None
    for _ in range(3):   # the 150 newest uploads are plenty
        resp = yt.playlistItems().list(part="snippet", playlistId=pl, maxResults=50, pageToken=token).execute()
        for it in resp["items"]:
            m = re.fullmatch(r"VidSection (.+) fixed", it["snippet"]["title"])
            if m:
                sec = m[1].replace(" ", ".")
                if sec in found:
                    raise RuntimeError(f"{sec}: two uploads ({found[sec]}, {it['snippet']['resourceId']['videoId']})")
                found[sec] = it["snippet"]["resourceId"]["videoId"]
        token = resp.get("nextPageToken")
        if not token:
            break
    MAP_FILE.write_text(json.dumps(found, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info(f"mapped {len(found)} 'fixed' uploads -> {MAP_FILE.relative_to(REPO)}")
    return found


REPLACED_FILE = REPO / "_knowledge/vahagn_linalg/uploads_replaced.json"


def remap_dehum(yt, ids: dict) -> list[str]:
    """Point the sections that got a buzz-free re-upload ('VidSection 23 3 b dehum', DECISIONS #48) at it. The old
    upload's id goes to REPLACED_FILE (section -> list of ids replaced), for taking it out of the playlist and deleting
    it later. Returns every section with a dehum upload, remapped now or by an earlier run: the dry run already writes
    the map, so returning only the new ones left the --apply run with none, which then meant all 25 sections."""
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    found, token = {}, None
    for _ in range(3):
        resp = yt.playlistItems().list(part="snippet", playlistId=pl, maxResults=50, pageToken=token).execute()
        for it in resp["items"]:
            m = re.fullmatch(r"VidSection (.+) dehum", it["snippet"]["title"])
            if m:
                sec = m[1].replace(" ", ".")
                if sec in found:
                    raise RuntimeError(f"{sec}: two dehum uploads ({found[sec]}, {it['snippet']['resourceId']['videoId']})")
                found[sec] = it["snippet"]["resourceId"]["videoId"]
        token = resp.get("nextPageToken")
        if not token:
            break
    replaced = json.loads(REPLACED_FILE.read_text(encoding="utf-8")) if REPLACED_FILE.exists() else {}
    changed = []
    for sec, new in sorted(found.items()):
        if sec not in ids:
            raise RuntimeError(f"dehum upload for unknown section {sec}")
        if ids[sec] != new:
            replaced.setdefault(sec, []).append(ids[sec])
            ids[sec] = new
            changed.append(sec)
    MAP_FILE.write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
    REPLACED_FILE.write_text(json.dumps(replaced, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info(f"{len(found)} dehum uploads found, {len(changed)} sections now point at them: {changed}")
    if not found:
        raise SystemExit("no 'VidSection X dehum' upload found")
    return sorted(found)


def drop_replaced(yt) -> None:
    """Take the replaced uploads out of the course playlist (50 units each); the videos themselves stay."""
    replaced = {v for ids in json.loads(REPLACED_FILE.read_text(encoding="utf-8")).values() for v in ids}
    items = [it for it in yt_publish._playlist_items(yt, PLAYLIST) if it["contentDetails"]["videoId"] in replaced]
    for it in items:
        yt.playlistItems().delete(id=it["id"]).execute()
        log.info(f"removed {it['contentDetails']['videoId']} ({it['snippet']['title']}) from the playlist")
    left = [it for it in yt_publish._playlist_items(yt, PLAYLIST) if it["contentDetails"]["videoId"] in replaced]
    if left:
        raise RuntimeError(f"still in the playlist after removal (reads can lag; reread): {[it['snippet']['title'] for it in left]}")
    log.info(f"{len(items)} replaced uploads out of the playlist ({len(items) * 50} units)")


def description(out: Path, chapters: str) -> str:
    ep = out / "edited_predicted"
    text = yt_publish.strip_title_header((ep / "description.txt").read_text(encoding="utf-8").strip("\n"))
    if chapters == "edited":
        return text
    lines = text.split("\n")
    i = lines.index("⏳ Թեմաներ")
    j = lines.index("", i)
    edited = [ln for ln in (ep / "timestamps.txt").read_text(encoding="utf-8").splitlines() if ln.strip()]
    if lines[i + 1:j] != edited:
        raise ValueError(f"{out.name}: the description's chapter block is not edited_predicted/timestamps.txt")
    raw = [ln for ln in (ep / "timestamps_raw.txt").read_text(encoding="utf-8").splitlines() if ln.strip()]
    return "\n".join(lines[:i + 1] + raw + lines[j:])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*")
    ap.add_argument("--chapters", choices=["raw", "edited"], required=True)
    ap.add_argument("--description-only", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--remap-dehum", action="store_true", help="first point the sections with a 'VidSection X dehum' "
                    "upload at it (old ids kept in uploads_replaced.json); local files only")
    ap.add_argument("--drop-replaced", action="store_true", help="with --apply: also take the replaced uploads out of "
                    "the playlist")
    args = ap.parse_args()
    yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
    yt = yt_publish.get_service()

    ids = upload_map(yt)
    if args.remap_dehum:
        with_dehum = remap_dehum(yt, ids)
        if not args.sections:
            args.sections = with_dehum
    status = json.loads((REPO / "_knowledge/vahagn_linalg/drafts_status.json").read_text(encoding="utf-8"))
    fixed = json.loads((REPO / "_knowledge/vahagn_linalg/audio_fix.json").read_text(encoding="utf-8"))
    secs = args.sections or sorted(status, key=lambda s: [int(p) if p.isdigit() else p for p in s.split(".")])
    if set(secs) - set(ids) or set(secs) - set(status):
        raise SystemExit(f"no upload or no draft for {sorted((set(secs) - set(ids)) | (set(secs) - set(status)))}")
    live = {}
    for k in range(0, len(secs), 50):
        chunk = [ids[s] for s in secs[k:k + 50]]
        for it in yt.videos().list(part="snippet,status,contentDetails", id=",".join(chunk)).execute()["items"]:
            live[it["id"]] = it
    in_pl = {it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PLAYLIST)}

    plan = []
    for s in secs:
        vid, out = ids[s], REPO / status[s]["output_dir"]
        it = live[vid]
        # edited chapters go on a video whose Studio cuts are saved and processed: its length is the cut list's
        dur = iso_s(it["contentDetails"]["duration"])
        want = status[s]["predicted_length_s"] if args.chapters == "edited" else fixed[s]["duration_s"]
        if abs(dur - want) > 1.5:
            raise RuntimeError(f"{s} {vid}: YouTube {dur} s vs {'the cut list' if args.chapters == 'edited' else 'fixed file'} "
                               f"{want:.1f} s - {'cuts not saved or not processed yet?' if args.chapters == 'edited' else 'wrong upload?'}")
        title = (out / "edited_predicted/titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
        desc = description(out, args.chapters)
        if len(title) > yt_publish.MAX_TITLE_CHARS or len(desc) > yt_publish.MAX_DESCRIPTION_CHARS:
            raise ValueError(f"{s}: title {len(title)} / description {len(desc)} chars over the limit")
        if "<" in title + desc or ">" in title + desc:
            raise ValueError(f"{s}: ASCII < or > (YouTube rejects it)")
        thumb = REPO / status[s]["thumbnail"]
        plan.append((s, vid, it, title, desc, thumb, vid in in_pl))
        log.info(f"{s:7} {vid}  {it['status']['privacyStatus']} -> {'(kept)' if args.description_only else 'unlisted'}  "
                 f"{title}  | desc {len(desc)} chars, {args.chapters} chapters"
                 + ("" if args.description_only else f" | thumb {thumb.name} | playlist {'already' if vid in in_pl else 'add'}"))
    units = sum(50 if args.description_only else 100 + (0 if p[6] else 50) for p in plan)
    log.info(f"{len(plan)} videos, ~{units} quota units")
    if not args.apply:
        log.info("dry run: nothing changed (add --apply)")
        return

    from googleapiclient.http import MediaFileUpload
    t0 = time.time()
    for i, (s, vid, it, title, desc, thumb, present) in enumerate(plan, 1):
        sn = {k: it["snippet"][k] for k in ("categoryId", "defaultLanguage", "defaultAudioLanguage") if k in it["snippet"]}
        sn.update(title=it["snippet"]["title"] if args.description_only else title, description=desc)
        body, parts = {"id": vid, "snippet": sn}, "snippet"
        if not args.description_only:
            st = it["status"]
            body["status"] = {k: st[k] for k in WRITABLE if k in st}
            body["status"].setdefault("selfDeclaredMadeForKids", st["madeForKids"])
            body["status"]["privacyStatus"] = "unlisted"
            parts = "snippet,status"
        yt.videos().update(part=parts, body=body).execute()
        if not args.description_only:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb))).execute()
            if not present:
                yt.playlistItems().insert(part="snippet", body={"snippet": {
                    "playlistId": PLAYLIST, "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
        el = time.time() - t0
        log.info(f"{i}/{len(plan)} {s} {vid} done  ({el:.0f} s elapsed, ~{el / i * (len(plan) - i):.0f} s left)")

    time.sleep(5)   # reads can lag a few seconds
    back = {}
    for k in range(0, len(plan), 50):
        chunk = [p[1] for p in plan[k:k + 50]]
        for it in yt.videos().list(part="snippet,status", id=",".join(chunk)).execute()["items"]:
            back[it["id"]] = it
    in_pl = {it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PLAYLIST)}
    bad = []
    for s, vid, it, title, desc, thumb, _ in plan:
        b = back[vid]
        if b["snippet"]["description"].strip() != desc.strip():
            bad.append((s, "description differs"))
        if not args.description_only:
            if b["snippet"]["title"] != title:
                bad.append((s, f"title {b['snippet']['title']!r}"))
            if b["status"]["privacyStatus"] != "unlisted":
                bad.append((s, b["status"]["privacyStatus"]))
            extra = {k: (it["status"].get(k), b["status"].get(k)) for k in set(it["status"]) | set(b["status"])
                     if k != "privacyStatus" and it["status"].get(k) != b["status"].get(k)}
            if extra:
                bad.append((s, f"status also changed: {extra}"))
            if vid not in in_pl:
                bad.append((s, "not in the playlist"))
    log.info(f"read back: {len(plan) - len({b[0] for b in bad})} of {len(plan)} as intended")
    if bad:
        log.error(f"CHECK (reads can lag; reread before concluding): {bad}")
        raise SystemExit(1)
    if args.drop_replaced:
        drop_replaced(yt)


if __name__ == "__main__":
    main()
