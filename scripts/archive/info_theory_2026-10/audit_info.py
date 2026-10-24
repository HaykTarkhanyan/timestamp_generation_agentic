"""Read-only audit of Ashot's 9 videos on umath: title, privacy, duration, date line, slides block (deck id +
pages vs slides_map), chapters (start 00:00, increasing, 30 s gaps, inside the video), forbidden ASCII < >,
length, custom thumbnail, playlist membership. ~5 quota units, ~5 s. Prints PASS/FAIL lines."""
import json
import re
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
PL = "PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy"
ids = json.loads((REPO / "_knowledge/info_theory/drive_folder_ids.json").read_text(encoding="utf-8"))
FID = {k.split(" - ")[0]: v["id"] for k, v in ids["files"].items()}
FOLDER = ids["folder"]["id"]
MONTHS = {2: "փետրվար", 3: "մարտ", 4: "ապրիլ", 5: "մայիս"}
# lesson -> (video id, (day, month), [(pages, deck key)])
EXPECT = {
    0: ("U3BbIALq4aM", (6, 2), [("1-15", "Դաս 0-1")]),
    1: ("4IO6iU7rRTA", (13, 2), [("16-36", "Դաս 0-1"), ("2-7", "Դաս 1-4")]),
    2: ("N3LL6k55sao", (20, 2), [("8-27", "Դաս 1-4")]),
    3: ("bHyOK-SSawI", (27, 2), [("28-54", "Դաս 1-4")]),
    4: ("fHPN7fJEusA", (6, 3), [("55-82", "Դաս 1-4")]),
    5: ("0WSFqm9E-Pc", (13, 3), [("1-21", "Դաս 5-8")]),
    6: ("LRQ6r_DaAVU", (27, 3), [("22-39", "Դաս 5-8")]),
    7: ("S8vcM74HZVE", (17, 4), [("40-71", "Դաս 5-8")]),
    8: ("LOHGyVgaIuI", (8, 5), [("72-96", "Դաս 5-8")]),
}

in_playlist = {it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PL)}
r = yt.videos().list(part="snippet,status,contentDetails", id=",".join(v[0] for v in EXPECT.values())).execute()
live = {v["id"]: v for v in r["items"]}
fails = 0


def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    fails += not ok


def secs(ts):
    p = [int(x) for x in ts.split(":")]
    return sum(x * 60 ** i for i, x in enumerate(reversed(p)))


for n, (vid, (day, mon), slides) in EXPECT.items():
    v = live[vid]
    t, d = v["snippet"]["title"], v["snippet"]["description"]
    dur = yt_publish.__dict__.get("iso_seconds") or None
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
    length = int(m[1] or 0) * 3600 + int(m[2] or 0) * 60 + int(m[3] or 0)
    tag = f"Դաս {n} {vid}"
    check(re.fullmatch(rf"Դաս {n} \| .+ \| Ինֆորմացիայի տեսություն", t) is not None and len(t) <= 100, f"{tag} title: {t} ({len(t)})")
    check(f"🗓️ Ամսաթիվ՝ {day} {MONTHS[mon]}, 2026" in d, f"{tag} date {day} {MONTHS[mon]}")
    for pages, deck in slides:
        check(f"սլայդներ {pages}" in d and FID[deck] in d, f"{tag} slides {pages} -> {deck}")
    other = [k for k in FID if k not in {s[1] for s in slides} and FID[k] in d]
    check(not other, f"{tag} no wrong deck links {other}")
    check(FOLDER in d and "[կավելացվի շուտով]" not in d and "TODO" not in d, f"{tag} folder link, no placeholder")
    check("<" not in d and ">" not in d and len(d) <= 5000, f"{tag} no ASCII <>, {len(d)} chars")
    check("ԵՊՀ Մաթեմատիկայի և մեխանիկայի ֆակուլտետի դասախոս Աշոտ Հարությունյանի" in d and "🎶 Երաժշտությունը" in d,
          f"{tag} lecturer line and music line")
    chap = [ln for ln in d.split("⏳ Թեմաներ", 1)[1].splitlines() if re.match(r"^\s*\d+:\d", ln)]
    times = [secs(ln.split()[0]) for ln in chap]
    gaps_ok = all(b - a >= 30 for a, b in zip(times, times[1:]))
    check(times and times[0] == 0 and gaps_ok and times[-1] < length - 10,
          f"{tag} {len(chap)} chapters, first {chap[0].split()[0]}, last {chap[-1].split()[0]} of {length // 60}:{length % 60:02d}")
    th = v["snippet"].get("thumbnails", {})
    check("maxres" in th or "standard" in th, f"{tag} thumbnail sizes {sorted(th)}")
    check(vid in in_playlist, f"{tag} in playlist; privacy {v['status']['privacyStatus']}")
print(f"\n{fails} failure(s); playlist has {len(in_playlist)} videos")
