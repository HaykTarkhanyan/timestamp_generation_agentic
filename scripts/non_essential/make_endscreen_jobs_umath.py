"""End-screen job files for umath (Համալսարանական մաթեմատիկա) course playlists: one
.playwright-mcp/endscreen_umath_<course>_NN_<id>.js per video from endscreen_template.js (next to this file): the next
lesson, the course playlist and Subscribe, last 10 s; the last lesson gets "Best for viewer". Plan and open questions:
_knowledge/umath_endscreens_plan.md.
Run: python scripts/non_essential/make_endscreen_jobs_umath.py ashot   (~15 s, reads the playlist through the API, read-only)
Then the files (best bundled with make_endscreen_batch.py), Studio switched to umath first.

"Next" goes by the "Դաս N |" number at the start of each title, which must run without gaps or repeats; a course whose
titles do not fit that ("Դաս N.M", "Դաս N-M", unnumbered items) needs its own rule in COURSES before it can run.
"""
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

COURSES = {
    "ashot": {"playlist_id": "PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy", "playlist": "Ինֆորմացիայի տեսություն"},
    "sevak": {"playlist_id": "PLz3NrXxHz_CBSe18p368oUfe8kZeP9pBS", "playlist": "Կոմպլեքս անալիզ"},
    # Դաս 1-14 had Video + Playlist and no Subscribe: rebuilt to the standard (the user's Q26, 2026-10-28)
    "papikian": {"playlist_id": "PLz3NrXxHz_CDF0l5rTCoxEqYoG3_na6Cs", "playlist": "Հանրահաշիվ և թվերի տեսություն",
                 "rebuild": {"through_lesson": 14, "kinds": ["Video", "Playlist"]}},
    # lecture 7 was never recorded (umath_todo), so Դաս 6 -> Դաս 8; Դաս 1-2 to 13 had Video + Playlist and no Subscribe:
    # rebuilt like Papikian's (Q27)
    "tserunyan": {"playlist_id": "PLz3NrXxHz_CA3NjE0D_amd_QcTMx5HJvZ", "playlist": "Տոպոլոգիա և մետրիկական տարածություններ",
                  "missing": [7], "rebuild": {"through_lesson": 13, "kinds": ["Video", "Playlist"]}},
    # Դաս 1 done by hand 2026-10-21 (skipped as ALREADY if it matches); "Դաս 12 (2025) |" is a second recording of
    # lesson 12: it points where Դաս 12 points (Դաս 13) and nothing points at it (agreed 2026-10-21)
    # portrait or square lessons (1440x1662 to 1920x1920, yt-dlp 2026-10-28) have no 3-element template: Video +
    # Playlist without Subscribe (Q31, DECISIONS #52)
    "arnak": {"playlist_id": "PLz3NrXxHz_CB0PhhZrFvhE4gbd6dotQFI", "playlist": "Բազմաչափ վիճակագրություն",
              "extra": " (2025)", "video_playlist": [2, 3, 4, 5, 6, 9, 10, 11, 12]},
    # "Դաս N.M |" and "Դաս N.M-ա |" sections: next = the next playlist item, once the playlist is checked to run in
    # lesson order (sorted 2026-10-27; sections 25 and 26 were never recorded, so 24.4 -> 27.1). The unlisted 21.1-28.4
    # are linked like the rest, 20.3 -> 21.1 included (the user's Q22, 2026-10-28)
    "vahagn": {"playlist_id": "PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM", "playlist": "Գծային հանրահաշիվ", "order": "playlist"},
    # Tier 2 (2026-10-28): the four "(տվյալագետների համար)" courses and the two plain ones are two professors' separate
    # courses (the user), each its own chain. ma3k has no Դաս 4 (lecture dates 3 = 10 Sept, 5 = 17 Sept 2024; the user
    # knows it is missing), so 3 -> 5. ma4's playlist is unlisted: not run until the user says whether end screens may
    # link it (Q41). All end in YSU's outro (white from 5.4-5.6 s before the end, measured on 6 videos of both
    # professors): end screens in the last 5 s, so they do not cover the blackboard (the user). ma1's first batch ran at
    # 10 s before that: its retime jobs rebuild only those
    "ma1": {"playlist_id": "PLz3NrXxHz_CCD63TcOD38ooOYglJMggwp", "playlist": "Մաթեմատիկական անալիզ 1 (տվյալագետների համար)",
            "seconds": 5, "retime_from": 10},
    "ma2": {"playlist_id": "PLz3NrXxHz_CDMp_ENH22qoEXYv-31tLQJ", "playlist": "Մաթեմատիկական անալիզ 2 (տվյալագետների համար)",
            "seconds": 5},
    "ma3k": {"playlist_id": "PLz3NrXxHz_CBamqkX-nPy-hN2iaHmouyo", "playlist": "Մաթեմատիկական անալիզ 3 (տվյալագետների համար)",
             "missing": [4], "seconds": 5},
    "ma4k": {"playlist_id": "PLz3NrXxHz_CA_BlztieZUekYxbVh9XDYG", "playlist": "Մաթեմատիկական անալիզ 4 (տվյալագետների համար)",
             "seconds": 5},
    "ma3": {"playlist_id": "PLz3NrXxHz_CB7AYnBOd-xSUmoCJ3197oM", "playlist": "Մաթեմատիկական անալիզ 3", "seconds": 5},
    "ma4": {"playlist_id": "PLz3NrXxHz_CD1urZ5q3bgm_YNWuT2osgS", "playlist": "Մաթեմատիկական անալիզ 4", "seconds": 5},
    # measured on 2 videos each (2026-10-28): mf and pp end in the white YSU outro (from 5.5 and 5.1-5.2 s before the
    # end): 5 s; gt (screen recordings) ends in a 7.0 s dark logo outro: 6 s, inside it
    "mf": {"playlist_id": "PLz3NrXxHz_CBpHt8Q_OGiDkrEj5Zkvfvs", "playlist": "Մաթեմատիկական ֆիզիկայի հավասարումներ", "seconds": 5},
    "pp": {"playlist_id": "PLz3NrXxHz_CBEiHFVt1rTBmSJ_03c5sUk", "playlist": "Պատահական պրոցեսներ", "seconds": 5},
    "gt": {"playlist_id": "PLz3NrXxHz_CD3eQ0refAvsxao-emXnA1O", "playlist": "Խմբերի տեսություն (ներածություն)", "seconds": 6},
    # fa (all 23 measured): Դաս 8-25 end in the white YSU outro (white for the last 4.7-5.8 s), Դաս 3-7 have no outro:
    # 5 s for all, Studio's minimum, the least possible over the lecture where there is no outro
    "fa": {"playlist_id": "PLz3NrXxHz_CC3ivN6Pglpml6oQ0rpBZXg", "playlist": "Ֆունկցիոնալ անալիզ", "seconds": 5},
    # the last Tier 2 four (2026-10-28), 5 s each: ode's 16th item is an 11-min solution with no lesson number, kept
    # out of the chain with Best for viewer; nt's titles carry the lecture dates (15.02 ... 29 մարտ 2022) in playlist
    # order and lafund has no numbers, so both follow the playlist ("playlist_raw": no title check)
    "ode": {"playlist_id": "PLz3NrXxHz_CDZA_JkkeA4wtQo_Gtinr9A", "seconds": 5, "unnumbered_extra": True,
            "playlist": "Սովորական դիֆերենցիալ հավասարումներ (տվյալագետների համար)"},
    "nt": {"playlist_id": "PLz3NrXxHz_CDIn0muSTw4udrxFnlSTzK2", "playlist": "Թվերի տեսություն", "seconds": 5,
           "order": "playlist_raw"},
    "prob": {"playlist_id": "PLz3NrXxHz_CBq0Qzt2iy3aIM43USBuvIP", "playlist": "Հավանականությունների տեսություն", "seconds": 5},
    "lafund": {"playlist_id": "PLz3NrXxHz_CDyZSI0hXZQVXQfKyMXHChA", "playlist": "Գծային հանրահաշվի հիմունքներ", "seconds": 5,
               "order": "playlist_raw"},
}
# "Դաս N |", a combined recording "Դաս N-M |" (Papikian, Tserunyan), which covers lessons N to M, or a second
# recording "Դաս N (YYYY) |" (Arnak), allowed only where the course names it as its "extra"
LESSON = re.compile(r"^Դաս (\d+)(?:-(\d+))?( \(\d{4}\))? \|")
# Vahagn's sections: "Դաս N.M |" or a part "Դաս N.M-ա |" (ա, բ, գ ... in alphabet order)
SECTION = re.compile(r"^Դաս (\d+)\.(\d+)(?:-(\S))? \|")
LETTERS = "աբգդեզէ"

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_jobs_umath")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_jobs_umath.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

key = sys.argv[1]
course = COURSES[key]
yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
items = [(it["contentDetails"]["videoId"], it["snippet"]["title"])
         for it in yt_publish._playlist_items(yt_publish.get_service(), course["playlist_id"])]
tpl = (Path(__file__).parent / "endscreen_template.js").read_text(encoding="utf-8")


def write_retime(job, name):
    """With the course's retime_from: a job that rebuilds only our own end screen of that length at its seconds."""
    if not course.get("retime_from"):
        return
    kinds = ["Video", "Playlist"] if job.get("layout") == "video+playlist" else ["Subscribe", "Video", "Playlist"]
    out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_retime_{name}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job | {"rebuild": kinds, "retimeFrom": course["retime_from"]},
                                                     ensure_ascii=False)), encoding="utf-8")


if course.get("order") in ("playlist", "playlist_raw"):
    # "playlist_raw": titles without lesson numbers (dated lectures, a preface): the playlist order is taken as given
    if course["order"] == "playlist":
        keys = []
        for vid, t in items:
            m = SECTION.match(t)
            if not m or (m[3] and m[3] not in LETTERS):
                raise ValueError(f"No 'Դաս N.M |' or 'Դաս N.M-ա |' at the start of {t!r}")
            keys.append((int(m[1]), int(m[2]), LETTERS.index(m[3]) + 1 if m[3] else 0))
        if keys != sorted(set(keys)):
            raise ValueError(f"{key}: the playlist is not in lesson order or repeats a section: sort it first")
    for i, (vid, t) in enumerate(items):
        nxt = items[i + 1] if i + 1 < len(items) else None
        job = {"id": vid, "lesson": f"{i + 1:02d} {t[:40]}", "playlist": course["playlist"], "playlistId": course["playlist_id"], "channel": yt_publish.CHANNEL_IDS["umath"],
               "next": {"prefix": nxt[1], "query": nxt[1], "id": nxt[0]} if nxt else None}
        if course.get("seconds"):
            job["seconds"] = course["seconds"]
        out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_{i + 1:02d}_{vid}.js"
        out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
        write_retime(job, f"{i + 1:02d}_{vid}")
        log.info(f"{out.name}: {t[:30]} -> {nxt[1][:30] if nxt else 'Best for viewer'}")
    log.info(f"{key}: {len(items)} job files written (playlist order)")
    sys.exit(0)
by_lesson = {}   # first lesson number -> (video id, title, last lesson number)
extras = []      # (lesson number, video id, title) of second recordings
unnumbered = []  # (video id, title) of items without a lesson number, where the course allows them
for vid, t in items:
    m = LESSON.match(t)
    if not m and course.get("unnumbered_extra"):
        unnumbered.append((vid, t))
        continue
    if not m:
        raise ValueError(f"No 'Դաս N |' or 'Դաս N-M |' at the start of {t!r}: give {key} its own rule")
    if m[3]:
        if m[3] != course.get("extra"):
            raise ValueError(f"{t!r} is a second recording ({m[3].strip()}): give {key} an 'extra' rule")
        extras.append((int(m[1]), vid, t))
        continue
    n, last = int(m[1]), int(m[2] or m[1])
    if last < n or n in by_lesson:
        raise ValueError(f"Bad or repeated lesson number in {t!r}")
    by_lesson[n] = (vid, t, last)
covered = sorted([k for n, (_, _, last) in by_lesson.items() for k in range(n, last + 1)] + course.get("missing", []))
if covered != list(range(covered[0], covered[0] + len(covered))):
    raise ValueError(f"Lesson numbers have gaps or overlaps (lessons known to be missing go in 'missing'): {covered}")
starts = sorted(by_lesson)
for i, n in enumerate(starts):
    vid, t, last = by_lesson[n]
    nxt = by_lesson[starts[i + 1]] if i + 1 < len(starts) else None
    job = {"id": vid, "lesson": f"{n:02d} {t[:40]}", "playlist": course["playlist"], "playlistId": course["playlist_id"], "channel": yt_publish.CHANNEL_IDS["umath"],
           "next": {"prefix": nxt[1], "query": nxt[1], "id": nxt[0]} if nxt else None}
    if n in course.get("video_playlist", []):
        job["layout"] = "video+playlist"
    if course.get("seconds"):
        job["seconds"] = course["seconds"]
    out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_{n:02d}_{vid}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    rb = course.get("rebuild")
    if rb and n <= rb["through_lesson"]:
        out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_rebuild_{n:02d}_{vid}.js"
        out.write_text(tpl.replace("__JOB__", json.dumps(job | {"rebuild": rb["kinds"]}, ensure_ascii=False)), encoding="utf-8")
    write_retime(job, f"{n:02d}_{vid}")
    log.info(f"{out.name}: {t[:40]} -> {nxt[1][:40] if nxt else 'Best for viewer'}")
for n, vid, t in extras:
    if n not in by_lesson:
        raise ValueError(f"{t!r} is a second recording of lesson {n}, which the playlist does not have")
    i = starts.index(n)
    nxt = by_lesson[starts[i + 1]] if i + 1 < len(starts) else None
    job = {"id": vid, "lesson": f"{n:02d}x {t[:40]}", "playlist": course["playlist"], "playlistId": course["playlist_id"], "channel": yt_publish.CHANNEL_IDS["umath"],
           "next": {"prefix": nxt[1], "query": nxt[1], "id": nxt[0]} if nxt else None}
    if course.get("seconds"):
        job["seconds"] = course["seconds"]
    out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_{n:02d}x_{vid}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    write_retime(job, f"{n:02d}x_{vid}")
    log.info(f"{out.name}: {t[:40]} -> {nxt[1][:40] if nxt else 'Best for viewer'}")
for i, (vid, t) in enumerate(unnumbered, 1):
    # outside the chain: nothing points at it, and it points at Best for viewer
    job = {"id": vid, "lesson": f"u{i} {t[:40]}", "playlist": course["playlist"], "playlistId": course["playlist_id"],
           "channel": yt_publish.CHANNEL_IDS["umath"], "next": None}
    if course.get("seconds"):
        job["seconds"] = course["seconds"]
    out = REPO / ".playwright-mcp" / f"endscreen_umath_{key}_u{i}_{vid}.js"
    out.write_text(tpl.replace("__JOB__", json.dumps(job, ensure_ascii=False)), encoding="utf-8")
    write_retime(job, f"u{i}_{vid}")
    log.info(f"{out.name}: {t[:40]} -> Best for viewer (unnumbered, outside the chain)")
log.info(f"{key}: {len(by_lesson) + len(extras) + len(unnumbered)} job files written")
