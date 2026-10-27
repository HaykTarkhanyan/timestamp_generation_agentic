"""Overall review of the 25 Vahagn pieces before publishing (the user, 2026-10-27, Q125: "one page for all 25"), read
live from YouTube: per piece the thumbnail, title, length, visibility, playlist position, chapter list and a link, and
whether the live title and description are exactly the local drafts (edited chapters).

    python scripts/non_essential/vahagn_overall_review.py        # ~10 s, ~3 quota units
    -> output/vahagn_linalg_overview/overall_review.html (standalone: thumbnails embedded)

Studio shows the re-uploads as "Draft" (the upload dialog was never finished); the API cannot see that, so the page
says it once at the top. Read-only.
"""
import base64
import html
import io
import json
import logging
import re
import sys
import time
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts/non_essential"))
import yt_publish  # noqa: E402
import vahagn_push_metadata as push  # noqa: E402   (description() builds exactly what was pushed)

K = REPO / "_knowledge/vahagn_linalg"
OUT = REPO / "output/vahagn_linalg_overview/overall_review.html"
PLAYLIST = "PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM"
CH = re.compile(r"^\s*\d+:\d\d(?::\d\d)?\s")
log = logging.getLogger("vahagn_overall_review")      # console through push's basicConfig, plus its own file
(REPO / "logs").mkdir(exist_ok=True)
_fh = logging.FileHandler(REPO / "logs/vahagn_overall_review.log", encoding="utf-8")
_fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(_fh)


def iso_s(d: str) -> int:
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d)
    return sum(int(v or 0) * k for v, k in zip(m.groups(), (3600, 60, 1)))


def thumb_b64(p: Path) -> str:
    im = Image.open(p).convert("RGB")
    im.thumbnail((480, 270))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def main() -> None:
    t0 = time.time()
    ids = json.loads((K / "uploads_fixed.json").read_text(encoding="utf-8"))
    st = json.loads((K / "drafts_status.json").read_text(encoding="utf-8"))
    order = lambda s: [int(p) if p.isdigit() else p for p in s.split(".")]
    secs = sorted(ids, key=order)
    if len(secs) != 25:
        raise ValueError(f"{len(secs)} pieces in uploads_fixed.json, expected 25")
    yt_publish.TOKEN_FILE = yt_publish.TOKEN_FILES["umath"]
    yt = yt_publish.get_service()
    live = {it["id"]: it for it in yt.videos().list(part="snippet,status,contentDetails",
                                                    id=",".join(ids[s] for s in secs)).execute()["items"]}
    missing = [s for s in secs if ids[s] not in live]
    if missing:
        raise RuntimeError(f"not found on YouTube: {missing}")
    pl = [it["contentDetails"]["videoId"] for it in yt_publish._playlist_items(yt, PLAYLIST)]

    rows, parts = [], []
    for s in secs:
        vid, it = ids[s], live[ids[s]]
        out = REPO / st[s]["output_dir"]
        want_title = (out / "edited_predicted/titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
        want_desc = push.description(out, "edited")
        title, desc = it["snippet"]["title"], it["snippet"]["description"]
        dur = iso_s(it["contentDetails"]["duration"])
        pred = st[s]["predicted_length_s"]
        checks = {"title = draft": title == want_title, "description = draft": desc.strip() == want_desc.strip(),
                  "length = cut list": abs(dur - pred) <= 1.5, "in playlist": vid in pl}
        bad = [k for k, ok in checks.items() if not ok]
        pos = pl.index(vid) + 1 if vid in pl else None
        chapters = [ln for ln in desc.splitlines() if CH.match(ln)]
        rows.append((s, vid, title, dur, it["status"]["privacyStatus"], pos, bad))
        sid = "p" + s.replace(".", "_")
        e = html.escape
        ch_html = "".join(f"<div class='ch{' sub' if ln.startswith('    ') else ''}'>{e(ln.strip())}</div>" for ln in chapters)
        parts.append(f"""<details open id="{sid}"><summary>{e(title)}</summary>
<div class="piece"><img src="data:image/jpeg;base64,{thumb_b64(REPO / st[s]['thumbnail'])}" alt="thumbnail {e(s)}">
<div><p><a href="https://youtu.be/{vid}" target="_blank">youtu.be/{vid}</a> · {dur // 60}:{dur % 60:02d} ·
{e(it['status']['privacyStatus'])} · playlist #{pos}</p>
<p class="{'bad' if bad else 'ok'}">{'Differs: ' + e(', '.join(bad)) if bad else 'Title, description, length, playlist: as drafted'}</p>
<div class="chs">{ch_html}</div></div></div>
<details><summary class="small">Full description as on YouTube</summary><pre>{e(desc)}</pre></details></details>""")
        log.info(f"{s:7} {vid}  {dur // 60}:{dur % 60:02d}  {it['status']['privacyStatus']}  #{pos}  {len(chapters)} chapters"
                 + (f"  DIFFERS: {bad}" if bad else ""))

    e = html.escape
    table = "".join(f"<tr><td><a href='#p{s.replace('.', '_')}'>{e(s)}</a></td><td>{e(t.split(' | ')[1])}</td>"
                    f"<td class='num'>{d // 60}:{d % 60:02d}</td><td>{e(p)}</td><td class='num'>{pos}</td>"
                    f"<td class='{'bad' if bad else 'ok'}'>{e(', '.join(bad)) if bad else 'ok'}</td></tr>"
                    for s, v, t, d, p, pos, bad in rows)
    n_bad = sum(1 for r in rows if r[6])
    OUT.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn 21-28 review</title><style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:20px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.05em;font-weight:600;cursor:pointer}} details{{margin:12px 0}} .small{{font-size:.85em;font-weight:400}}
table{{border-collapse:collapse;width:100%;table-layout:fixed}} td,th{{border-bottom:1px solid #eee;padding:5px 8px;text-align:left}}
col.c1{{width:70px}} col.c3{{width:70px}} col.c4{{width:80px}} col.c5{{width:70px}} col.c6{{width:170px}} .num{{text-align:right}}
.ok{{color:#0033A0}} .bad{{color:#D90012;font-weight:600}} .piece{{display:flex;gap:16px;flex-wrap:wrap}}
.piece img{{width:320px;max-width:100%;border:1px solid #ddd;align-self:flex-start}} .ch{{font-size:.9em}} .sub{{margin-left:22px;color:#333}}
pre{{white-space:pre-wrap;background:#f6f6f6;padding:10px;font-size:.85em}} .note{{background:#fff7e0;border-left:4px solid #F2A800;padding:8px 12px}}
</style></head><body>
<h1>Գծային հանրահաշիվ 21.1-28.4: overall review before publishing</h1>
<p class="note">Read live from YouTube {time.strftime('%Y-%m-%d %H:%M')}. All 25 are unlisted, and Studio shows them as
<b>Draft</b> (the upload dialog was never finished): publishing will mean finishing each draft. Pieces whose title,
description, length or playlist entry differ from the local drafts: <b>{n_bad}</b>.</p>
<nav><b>Contents</b><ul><li><a href="#sum">All 25 at a glance</a></li><li><a href="#pieces">Each piece</a></li></ul></nav>
<details open id="sum"><summary>All 25 at a glance</summary><table><colgroup><col class="c1"><col><col class="c3"><col class="c4">
<col class="c5"><col class="c6"></colgroup><tr><th>Piece</th><th>Topic</th><th class="num">Length</th><th>Visibility</th>
<th class="num">Playlist #</th><th>Checks</th></tr>{table}</table></details>
<details open id="pieces"><summary>Each piece</summary>{''.join(parts)}</details>
</body></html>""", encoding="utf-8")
    log.info(f"{len(secs)} pieces, {n_bad} differ; page {OUT} ({OUT.stat().st_size / 1e6:.1f} MB), {time.time() - t0:.0f} s")
    if n_bad:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
