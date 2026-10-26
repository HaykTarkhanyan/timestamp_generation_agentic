"""Standalone review page for the Vahagn linear algebra drafts: per piece the thumbnail, title candidates, the
predicted length and cut plan, the chapters (on the cut list's timeline), the description, the checks, the Codex
verdicts, and a link to the piece's studio.html. Table of contents on top, every piece a collapsible section.

    python scripts/non_essential/vahagn_review_page.py
Expected: ~5 s. Reads _knowledge/vahagn_linalg/{pieces.json, drafts_status.json, codex_review.json (if present)}
and each output dir's edited_predicted/; writes _knowledge/vahagn_linalg/review_21-28.html (thumbnails embedded as
JPEG data URIs, so the file can be sent on its own; the studio.html links only work on this machine).
"""
import base64
import html
import io
import json
import logging
import sys
import time
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
K = REPO / "_knowledge/vahagn_linalg"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_review_page.log", encoding="utf-8")])
log = logging.getLogger(__name__)
e = html.escape


def thumb_uri(path: Path) -> str:
    im = Image.open(path).convert("RGB")
    im.thumbnail((640, 360))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def mmss(s) -> str:
    s = int(round(s or 0))
    return f"{s // 60}:{s % 60:02d}"


def main() -> None:
    t0 = time.time()
    pieces = json.loads((K / "pieces.json").read_text(encoding="utf-8"))["pieces"]
    status = json.loads((K / "drafts_status.json").read_text(encoding="utf-8"))
    codex = json.loads((K / "codex_review.json").read_text(encoding="utf-8")) if (K / "codex_review.json").exists() else {}
    toc, sections = [], []
    for p in pieces:
        sec, st = p["section"], status.get(p["section"])
        anchor = "s" + sec.replace(".", "-")
        if not st:
            toc.append(f'<li><a href="#{anchor}">Դաս {e(p["label"])}</a> <span class="m">(no draft yet: {e(p.get("note", ""))})</span></li>')
            sections.append(f'<details id="{anchor}"><summary>Դաս {e(p["label"])} - no draft yet</summary>'
                            f'<p class="m">{e(p.get("note", ""))}</p></details>')
            continue
        out = REPO / st["output_dir"]
        ep = out / "edited_predicted"
        titles = (ep / "titles.txt").read_text(encoding="utf-8").splitlines()
        chapters = (ep / "timestamps.txt").read_text(encoding="utf-8")
        desc = (ep / "description.txt").read_text(encoding="utf-8").split("──────────────────────────────\n\n", 1)[-1]
        raw_len = json.loads((out / "metadata.json").read_text(encoding="utf-8"))["duration"]
        checks = (f'verifier {"valid" if st["verifier_valid"] else "NOT valid: " + e("; ".join(st["verifier_issues"]))}, '
                  f'glossary DENY {st["glossary"]["DENY"]} / NEAR {st["glossary"]["NEAR"]} / ENG {st["glossary"]["ENG"]}, '
                  f'{st["chapters"]} chapters ({st["nested"]} nested)')
        moved = "".join(f"<li>{e(m)}</li>" for m in st["moved_into_cut_ends"])
        cx = codex.get(sec, {})
        cx_rows = "".join(f'<tr><td>{e(f.get("time", ""))}</td><td>{e(f.get("finding", ""))}</td>'
                          f'<td class="{e(f.get("verdict", ""))}">{e(f.get("verdict", ""))}</td><td>{e(f.get("note", ""))}</td></tr>'
                          for f in cx.get("findings", []))
        cx_html = (f'<table class="cx"><colgroup><col style="width:9%"><col style="width:46%"><col style="width:9%">'
                   f'<col style="width:36%"></colgroup><tr><th>time</th><th>Codex finding</th><th>verdict</th><th>note</th></tr>'
                   f'{cx_rows}</table>' if cx_rows else '<p class="m">no Codex review recorded</p>')
        studio = (out / "edit_review/studio.html").resolve().as_uri()
        toc.append(f'<li><a href="#{anchor}">Դաս {e(p["label"])}</a> {e(p["titles"][0])} '
                   f'<span class="m">({mmss(raw_len)} → {mmss(st["predicted_length_s"])}, {p["date"]})</span></li>')
        sections.append(f"""<details open id="{anchor}"><summary>Դաս {e(p["label"])} · {e(p["titles"][0])}</summary>
<div class="row"><img src="{thumb_uri(REPO / st['thumbnail'])}" alt="thumbnail {e(sec)}">
<div><p><b>Title candidates</b> (1 = recommended)</p><ol>{''.join(f'<li>{e(t)}</li>' for t in titles)}</ol>
<p class="m">Date {e(p['date'])} · raw {mmss(raw_len)} → predicted {mmss(st['predicted_length_s'])} with
<code>{e(st['cut_list'])}</code> · video <code>{e(st['video_id'])}</code> (raw upload, captions only) ·
<a href="{studio}">studio.html</a></p><p class="m">{checks}</p>
{f'<p class="m">Chapters moved to where speech resumes after a cut:</p><ul class="m">{moved}</ul>' if moved else ''}</div></div>
<div class="row2"><div><p><b>Chapters</b> (on the cut timeline)</p><pre>{e(chapters)}</pre></div>
<div><p><b>Description</b> (as it would be pushed)</p><pre>{e(desc)}</pre></div></div>
<p><b>Codex review</b></p>{cx_html}
</details>""")
    page = f"""<!doctype html><html lang="hy"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn 21-28 review</title><style>
body{{font-family:system-ui,sans-serif;max-width:1200px;margin:24px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.15em;font-weight:600;cursor:pointer;padding:6px 0}} details{{border-top:1px solid #ddd;padding:4px 0 14px}}
.row{{display:flex;gap:18px;flex-wrap:wrap}} .row img{{width:384px;max-width:100%;border:1px solid #ccc;border-radius:6px}}
.row2{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} @media(max-width:800px){{.row2{{grid-template-columns:1fr}}}}
pre{{white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:6px;font-size:.88em}} .m{{color:#555;font-size:.9em}}
table.cx{{table-layout:fixed;width:100%;border-collapse:collapse;font-size:.88em}} .cx td,.cx th{{border:1px solid #ddd;padding:4px 6px;vertical-align:top}}
td.take{{background:rgba(0,160,0,.18)}} td.reject{{background:rgba(217,0,18,.15)}} td.partial{{background:rgba(242,168,0,.25)}}
</style></head><body>
<h1>Գծային հանրահաշիվ 21.1-28.4 · drafts for review</h1>
<p class="m">Built {time.strftime('%Y-%m-%d %H:%M')} from the local drafts (DECISIONS #35: rendered locally, uploaded as new
videos). Nothing here is on YouTube yet. Chapters follow the current cut list of each piece (the 4 s plan until the piece
is reviewed on studio.html), and move with it after the review.</p>
<nav><b>Contents</b><ol>{''.join(toc)}</ol></nav>
{''.join(sections)}
</body></html>"""
    dest = K / "review_21-28.html"
    dest.write_text(page, encoding="utf-8")
    log.info(f"wrote {dest.relative_to(REPO)} ({dest.stat().st_size / 1e6:.1f} MB) in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
