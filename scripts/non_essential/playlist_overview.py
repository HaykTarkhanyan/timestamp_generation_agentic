"""One page to check a YouTube playlist at a glance: every video's thumbnail, title, visibility, length,
chapter count and description, plus a signed-out check of every link in the descriptions.

    python scripts/non_essential/playlist_overview.py --channel umath --playlist PLz3NrXxHz_CB0PhhZrFvhE4gbd6dotQFI \
        --out output/arnak_overview
    # ~1 min for 14 videos and ~40 links; writes <out>/overview.json (the record) and <out>/overview.html
    python scripts/non_essential/playlist_overview.py --out output/arnak_overview --html-only   # page from the JSON

The link check opens each URL without cookies, as a viewer would: a Google Drive link that lands on a
sign-in page is not public. For Drive files the page title gives the file name, and a name that starts
with a number ("05 Էմպիրիկ միջին.pdf") must match the video's "Դաս N" (a linked PDF of the wrong lesson
is the mistake this catches). The HTML is standalone (thumbnails embedded as JPEG data URIs).
"""
import argparse
import base64
import html
import io
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/playlist_overview.log", encoding="utf-8")])
log = logging.getLogger(__name__)

URL_RE = re.compile(r"https?://[^\s<>\"']+")
TRAIL = ".,;:)]»։՝"                       # punctuation that ends a sentence, not the URL
LESSON = re.compile(r"^Դաս (\d+)")
CHAPTER = re.compile(r"^\s*(?:\d+:)?\d{1,2}:\d{2}\s")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def get(url: str, limit: int = 400_000) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, r.geturl(), r.read(limit)


def check_link(url: str) -> dict:
    if re.match(r"https?://(www\.)?(youtube\.com/(watch|playlist)|youtu\.be/)", url):
        # a YouTube page's HTML has no usable <title> signed out; oEmbed names the video or playlist,
        # and fails (401/404) for a private or deleted one
        try:
            _, _, body = get("https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe=""))
            t = json.loads(body)["title"]
            log.info(f"OK  {url} -> {t}")
            return {"url": url, "ok": True, "status": 200, "title": t, "note": f"YouTube: {t}"}
        except urllib.error.HTTPError as e:
            log.error(f"link failed: {url}: oEmbed {e.code}")
            return {"url": url, "ok": False, "status": e.code, "note": f"YouTube oEmbed {e.code}: private, deleted or wrong id"}
    try:
        status, final, body = get(url)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        log.error(f"link failed: {url}: {e}")
        return {"url": url, "ok": False, "status": getattr(e, "code", None), "note": f"failed: {e}"}
    m = re.search(rb"<title>(.*?)</title>", body, re.S | re.I)
    title = html.unescape(m.group(1).decode("utf-8", "replace")).strip() if m else ""
    out = {"url": url, "status": status, "final": final, "title": title}
    if "accounts.google.com" in final or "ServiceLogin" in final:
        out.update(ok=False, note="asks to sign in: not public")
    elif "drive.google.com" in url:
        name = re.sub(r"\s*[-–]\s*Google Drive\s*$", "", title)     # files end " - Google Drive", folders " – "
        out.update(ok=bool(name) and name != "Google Drive", name=name,
                   note=name if name and name != "Google Drive" else "Drive page without a file name")
    else:
        out.update(ok=status == 200, note=title[:80])
    log.info(f"{'OK ' if out['ok'] else 'BAD'} {url} -> {out['note']}")
    return out


def thumb_data(thumbs: dict) -> str:
    for k in ("maxres", "standard", "high", "medium", "default"):
        if k in thumbs:
            _, _, raw = get(thumbs[k]["url"], limit=5_000_000)
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            im.thumbnail((640, 360))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=85)
            return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    raise ValueError(f"no thumbnail in {list(thumbs)}")


def iso_len(d: str) -> str:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d)
    h, mi, s = (int(x or 0) for x in m.groups())
    return f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"


def links_in(text: str) -> list[str]:
    return list(dict.fromkeys(u.rstrip(TRAIL) for u in URL_RE.findall(text)))


def fetch(channel: str, playlist: str) -> dict:
    import yt_publish as yp
    yp.TOKEN_FILE = yp.TOKEN_FILES[channel]
    yt = yp.get_service()
    pl = yt.playlists().list(part="snippet,status", id=playlist).execute()["items"][0]
    ids, token = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=playlist, maxResults=50, pageToken=token).execute()
        ids += [it["contentDetails"]["videoId"] for it in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    vids = {}
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,status,contentDetails", id=",".join(ids[i:i + 50])).execute()["items"]:
            vids[v["id"]] = v
    missing = [i for i in ids if i not in vids]
    if missing:
        raise ValueError(f"playlist items the API did not return (private to another account, deleted?): {missing}")
    all_links = sorted({u for v in vids.values() for u in links_in(v["snippet"]["description"])} |
                       set(links_in(pl["snippet"]["description"])))
    log.info(f"{len(ids)} videos, {len(all_links)} distinct links to check")
    checks = {}
    t0 = time.time()
    for n, u in enumerate(all_links, 1):
        checks[u] = check_link(u)
        if n % 10 == 0:
            el = time.time() - t0
            log.info(f"links {n}/{len(all_links)}, {el:.0f}s elapsed, ~{el / n * (len(all_links) - n):.0f}s left")
    videos = []
    for vid in ids:
        v = vids[vid]
        sn, title = v["snippet"], v["snippet"]["title"]
        desc = sn["description"]
        lesson = LESSON.match(title)
        problems = []
        for u in links_in(desc):
            c = checks[u]
            if not c["ok"]:
                problems.append(f"{u}: {c['note']}")
            num = re.match(r"^(\d+)\s", c.get("name", ""))
            if lesson and num and int(num.group(1)) != int(lesson.group(1)):
                problems.append(f"{u}: file {c['name']!r} is not lesson {lesson.group(1)}")
        if "<" in desc or ">" in desc:
            problems.append("ASCII < or > in the description (YouTube rejects it on edit)")
        videos.append({"id": vid, "title": title, "privacy": v["status"]["privacyStatus"],
                       "length": iso_len(v["contentDetails"]["duration"]), "description": desc,
                       "chapters": sum(1 for l in desc.splitlines() if CHAPTER.match(l)),
                       "links": links_in(desc), "problems": problems, "thumb": thumb_data(sn["thumbnails"]),
                       "thumb_custom": "maxres" in sn["thumbnails"]})
        log.info(f"{title[:60]}: {v['status']['privacyStatus']}, {videos[-1]['chapters']} chapters, "
                 f"{len(problems)} problem(s)")
    return {"fetched": time.strftime("%Y-%m-%d %H:%M"), "playlist": {"id": playlist, "title": pl["snippet"]["title"],
            "description": pl["snippet"]["description"], "privacy": pl["status"]["privacyStatus"],
            "links": links_in(pl["snippet"]["description"])}, "checks": checks, "videos": videos}


CSS = """
:root { --bg: #fff; --fg: #1d1d1f; --muted: #6e6e73; --card: #f5f5f7; --line: #d2d2d7; --ok: #1a7f37; --bad: #D90012; --link: #0033A0; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #161617; --fg: #f5f5f7; --muted: #a1a1a6; --card: #232325; --line: #3a3a3c; --ok: #4ac26b; --bad: #ff6b6b; --link: #8ab4ff; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.5 system-ui, "Segoe UI", sans-serif; }
main { max-width: 1100px; margin: 0 auto; padding: 16px; }
a { color: var(--link); }
h1 { font-size: 24px; margin: 8px 0; }
.sub, .meta { color: var(--muted); font-size: 13px; }
details { border: 1px solid var(--line); border-radius: 8px; margin: 12px 0; background: var(--card); }
summary { cursor: pointer; padding: 10px 14px; font-weight: 600; }
.body { padding: 0 14px 14px; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 14px; }
th, td { border-bottom: 1px solid var(--line); padding: 6px 8px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
.ok { color: var(--ok); font-weight: 600; } .bad { color: var(--bad); font-weight: 600; }
.video { display: grid; grid-template-columns: 320px 1fr; gap: 16px; }
.video img { width: 320px; border-radius: 6px; display: block; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; font: 13px/1.45 system-ui, "Segoe UI", sans-serif; margin: 8px 0 0; }
ul.links { margin: 6px 0; padding-left: 18px; font-size: 13px; }
@media (max-width: 760px) { .video { grid-template-columns: 1fr; } .video img { width: 100%; } }
"""


def linkify(text: str) -> str:
    out, last = [], 0
    for m in URL_RE.finditer(text):
        u = m.group(0).rstrip(TRAIL)
        out.append(html.escape(text[last:m.start()]))
        out.append(f'<a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(u)}</a>')
        last = m.start() + len(u)
    out.append(html.escape(text[last:]))
    return "".join(out)


def link_list(urls, checks) -> str:
    items = []
    for u in urls:
        c = checks[u]
        mark = '<span class="ok">✔</span>' if c["ok"] else '<span class="bad">✘</span>'
        items.append(f'<li>{mark} <a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(u)}</a>'
                     f' <span class="meta">{html.escape(c["note"])}</span></li>')
    return f'<ul class="links">{"".join(items)}</ul>' if items else '<p class="meta">No links.</p>'


def build_html(d: dict) -> str:
    esc = html.escape
    pl, checks, vids = d["playlist"], d["checks"], d["videos"]
    n_bad = sum(1 for c in checks.values() if not c["ok"])
    rows = "".join(
        f'<tr><td class="num">{i}</td><td><a href="#v{i}">{esc(v["title"])}</a></td><td>{esc(v["privacy"])}</td>'
        f'<td class="num">{v["length"]}</td><td class="num">{v["chapters"]}</td>'
        f'<td>{"<span class=ok>OK</span>" if not v["problems"] else "<span class=bad>" + str(len(v["problems"])) + " problem(s)</span>"}</td></tr>'
        for i, v in enumerate(vids, 1))
    sections = [("summary", "Summary", f"""
<p class="sub">Fetched {esc(d["fetched"])} from the YouTube API (the live titles, descriptions and thumbnails).
{len(checks)} distinct links checked signed out: <span class="{'bad' if n_bad else 'ok'}">{n_bad} not working</span>.</p>
<table><colgroup><col style="width:5%"><col style="width:55%"><col style="width:11%"><col style="width:9%"><col style="width:9%"><col style="width:11%"></colgroup>
<thead><tr><th class="num">#</th><th>Title</th><th>Visibility</th><th class="num">Length</th><th class="num">Chapters</th><th>Links</th></tr></thead>
<tbody>{rows}</tbody></table>"""),
                ("playlist", f"Playlist: {pl['title']}", f"""
<p class="meta">{esc(pl["privacy"])} · <a href="https://www.youtube.com/playlist?list={esc(pl["id"])}" target="_blank">open on YouTube</a></p>
{link_list(pl["links"], checks)}<pre>{linkify(pl["description"])}</pre>""")]
    for i, v in enumerate(vids, 1):
        probs = "".join(f'<li class="bad">{esc(p)}</li>' for p in v["problems"])
        sections.append((f"v{i}", f"{i}. {v['title']}", f"""
<div class="video"><a href="https://youtu.be/{esc(v["id"])}" target="_blank"><img src="{v["thumb"]}" alt="thumbnail"></a>
<div><p class="meta">{esc(v["privacy"])} · {v["length"]} · {v["chapters"]} chapters ·
<a href="https://youtu.be/{esc(v["id"])}" target="_blank">youtu.be/{esc(v["id"])}</a> ·
<a href="https://studio.youtube.com/video/{esc(v["id"])}/edit" target="_blank">Studio</a></p>
{f'<ul class="links">{probs}</ul>' if probs else ''}{link_list(v["links"], checks)}</div></div>
<pre>{linkify(v["description"])}</pre>"""))
    toc = "".join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t, _ in sections)
    body = "".join(f'<details open id="{sid}"><summary>{esc(t)}</summary><div class="body">{inner}</div></details>'
                   for sid, t, inner in sections)
    return f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(pl["title"])} overview</title><style>{CSS}</style></head><body><main>
<h1>{esc(pl["title"])}: all videos</h1><nav><ol>{toc}</ol></nav>{body}</main></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--channel", default="umath")
    ap.add_argument("--playlist")
    ap.add_argument("--out", type=Path, required=True, help="folder for overview.json and overview.html")
    ap.add_argument("--html-only", action="store_true", help="rebuild the page from overview.json, no fetching")
    a = ap.parse_args()
    t0 = time.time()
    out = a.out if a.out.is_absolute() else REPO / a.out
    out.mkdir(parents=True, exist_ok=True)
    rec = out / "overview.json"
    if a.html_only:
        d = json.loads(rec.read_text(encoding="utf-8"))
    else:
        if not a.playlist:
            ap.error("--playlist is needed unless --html-only")
        d = fetch(a.channel, a.playlist)
        rec.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "overview.html").write_text(build_html(d), encoding="utf-8")
    probs = sum(len(v["problems"]) for v in d["videos"])
    log.info(f"wrote {rec} and {out / 'overview.html'}: {len(d['videos'])} videos, {probs} problem(s), "
             f"in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
