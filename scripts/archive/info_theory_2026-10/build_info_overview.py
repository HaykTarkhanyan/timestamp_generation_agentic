"""Build _knowledge/info_theory/videos_overview.html: all 9 Ashot videos at a glance (thumbnail, title, date,
length, speed, visibility, slides, chapters), from the live YouTube data. Standalone: thumbnails inlined as
base64 JPEG (local PNGs for Դաս 4-8, i.ytimg.com for 0-3). ~10 s, ~3 quota units. Repo root."""
import base64
import html
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
sys.path.insert(0, str(REPO / "scripts"))
import yt_publish  # noqa: E402

yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
yt = yt_publish.get_service()
PL = "PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy"
FOLDER = "https://drive.google.com/drive/folders/" + json.loads(
    (REPO / "_knowledge/info_theory/drive_folder_ids.json").read_text(encoding="utf-8"))["folder"]["id"]
LESSONS = {0: "U3BbIALq4aM", 1: "4IO6iU7rRTA", 2: "N3LL6k55sao", 3: "bHyOK-SSawI", 4: "fHPN7fJEusA",
           5: "0WSFqm9E-Pc", 6: "LRQ6r_DaAVU", 7: "S8vcM74HZVE", 8: "LOHGyVgaIuI"}
SPEED = {0: "1x", 1: "1x", 2: "1x", 3: "1.25x", 4: "1.25x", 5: "1x", 6: "1.25x", 7: "1.25x", 8: "1.25x"}
NOTES = {6: "Camera stopped at 44:42; from there to the end his slides are shown over the lecture audio.",
         5: "Not sped up (1x), unlike 3, 4 and 6-8."}

r = yt.videos().list(part="snippet,status,contentDetails", id=",".join(LESSONS.values())).execute()
live = {v["id"]: v for v in r["items"]}


def thumb(n, vid):
    local = REPO / f"thumbnails/umath/info_theory_{n:02d}.png"
    if local.exists():
        im = Image.open(local)
    else:
        req = urllib.request.Request(f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read()))
    im = im.convert("RGB").resize((480, 270), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def secs(ts):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(ts.split(":"))))


def hms(s):
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


rows, cards, sections = [], [], []
for n, vid in LESSONS.items():
    v = live[vid]
    title, desc = v["snippet"]["title"], v["snippet"]["description"]
    topic = title.split(" | ")[1]
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"]["duration"])
    length = int(m[1] or 0) * 3600 + int(m[2] or 0) * 60 + int(m[3] or 0)
    date = re.search(r"Ամսաթիվ՝ ([^\n]+)", desc)[1]
    pages = ", ".join(re.findall(r"սլայդներ ([\d-]+)", desc))
    decks = re.findall(r"https://drive\.google\.com/file/d/[\w-]+/view", desc)
    priv = v["status"]["privacyStatus"]
    chap = [ln.rstrip() for ln in desc.split("⏳ Թեմաներ", 1)[1].splitlines() if re.match(r"^\s*\d+:\d", ln)]
    url, studio = f"https://youtu.be/{vid}", f"https://studio.youtube.com/video/{vid}/edit"
    img = thumb(n, vid)
    e = html.escape
    deck_links = " ".join(f'<a href="{d}">deck {i + 1}</a>' if len(decks) > 1 else f'<a href="{d}">deck</a>'
                          for i, d in enumerate(decks))
    cards.append(f"""<div class="card"><a href="{url}"><img src="{img}" alt="Դաս {n} thumbnail"></a>
<div class="meta"><b>Դաս {n}</b> <span class="badge {priv}">{priv}</span> <span class="badge sp">{SPEED[n]}</span></div>
<div class="topic">{e(topic)}</div>
<div class="small">{e(date)} · {hms(length)} · slides {e(pages)}</div>
<div class="small"><a href="{url}">watch</a> · <a href="{studio}">Studio</a> · {deck_links} · <a href="#d{n}">chapters ({len(chap)})</a></div></div>""")
    rows.append(f"<tr><td>{n}</td><td>{e(topic)}</td><td>{e(date)}</td><td class=num>{hms(length)}</td>"
                f"<td>{SPEED[n]}</td><td><span class='badge {priv}'>{priv}</span></td><td>{e(pages)}</td>"
                f"<td class=num>{len(chap)}</td><td><a href='{url}'>{vid}</a></td></tr>")
    items = "".join(f'<li class="{"sub" if c.startswith(" ") else ""}"><a href="{url}?t={secs(c.split()[0])}">{e(c.split()[0])}</a> '
                    f'{e(c.strip().split(" ", 1)[1])}</li>' for c in chap)
    note = f'<p class="note">{e(NOTES[n])}</p>' if n in NOTES else ""
    sections.append(f"""<details open id="d{n}"><summary><h2>Դաս {n} · {e(topic)}</h2></summary>
<div class="detail"><a href="{url}"><img src="{img}" alt=""></a><div>
<p class="title">{e(title)}</p>
<p>{e(date)} · {hms(length)} · {SPEED[n]} · <span class="badge {priv}">{priv}</span></p>
<p>Slides {e(pages)}: {deck_links} · <a href="{FOLDER}">folder</a> · <a href="{studio}">edit in Studio</a></p>{note}
</div></div><ol class="chapters">{items}</ol></details>""")

toc = "".join(f'<li><a href="#d{n}">Դաս {n}</a></li>' for n in LESSONS)
page = f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ինֆորմացիայի տեսություն - videos</title><style>
:root{{--bg:#f6f7f9;--fg:#1c1f24;--card:#fff;--muted:#5b6370;--line:#dde1e6;--link:#0033A0}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171a;--fg:#e8eaed;--card:#1f2226;--muted:#a0a7b1;--line:#30353b;--link:#8fb0ff}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,"Segoe UI",sans-serif}}
main{{max-width:1180px;margin:auto}} a{{color:var(--link)}} h1{{margin:.2em 0}}
details{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px;margin:12px 0}}
summary{{cursor:pointer}} summary h2{{display:inline;font-size:1.1em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin:10px 0}}
.card{{border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--bg)}}
.card img{{width:100%;display:block}} .card .meta,.card .topic,.card .small{{padding:2px 10px}}
.card .topic{{font-weight:600}} .small{{color:var(--muted);font-size:.88em;padding-bottom:6px}}
.badge{{font-size:.75em;padding:1px 7px;border-radius:9px;border:1px solid var(--line)}}
.public{{background:#d9f2df;color:#14532d}} .unlisted{{background:#fdf0cf;color:#6b4e00}} .private{{background:#f9d6d6;color:#7a1010}}
.sp{{background:transparent}}
table{{border-collapse:collapse;width:100%;table-layout:fixed;font-size:.9em}} td,th{{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left;overflow-wrap:anywhere}}
td.num{{text-align:right}} .tablewrap{{overflow-x:auto}}
.detail{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}} .detail img{{width:320px;max-width:100%;border-radius:6px}}
.toc{{display:flex;flex-wrap:wrap;gap:4px 16px;list-style:none;padding:0;margin:6px 0}} .title{{font-weight:600}} .note{{color:#D90012}} .chapters{{columns:2 340px;margin-top:10px}} .chapters{{list-style:none;padding-left:0}} .chapters li{{break-inside:avoid}} .chapters li.sub{{padding-left:2em;color:var(--muted)}}
</style></head><body><main>
<h1>Ինֆորմացիայի տեսություն · Աշոտ Հարությունյան</h1>
<p class="small">All 9 videos of the playlist, from the live YouTube data (built 2026-10-24). <a href="https://www.youtube.com/playlist?list={PL}">Playlist</a> · <a href="{FOLDER}">Slides folder</a></p>
<details open id="toc"><summary><h2>Contents</h2></summary><ul class="toc"><li><a href="#glance">At a glance</a></li><li><a href="#table">Table</a></li>{toc}</ul></details>
<details open id="glance"><summary><h2>At a glance</h2></summary><div class="grid">{''.join(cards)}</div></details>
<details open id="table"><summary><h2>Table</h2></summary><div class="tablewrap"><table>
<colgroup><col style="width:6%"><col style="width:32%"><col style="width:12%"><col style="width:8%"><col style="width:7%"><col style="width:10%"><col style="width:10%"><col style="width:6%"><col style="width:13%"></colgroup>
<tr><th>Դաս</th><th>Topic</th><th>Date</th><th>Length</th><th>Speed</th><th>Visibility</th><th>Slides</th><th>Ch.</th><th>Video</th></tr>
{''.join(rows)}</table></div></details>
{''.join(sections)}
</main></body></html>"""
out = REPO / "_knowledge/info_theory/videos_overview.html"
out.write_text(page, encoding="utf-8")
print(out, f"{len(page) / 1e3:.0f} kB")
