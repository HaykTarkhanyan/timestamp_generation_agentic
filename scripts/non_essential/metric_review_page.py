"""Review page for Tserunyan 15-27: titles, thumbnails, nested chapters (with the review's changes), cut plans
(the user's own list where there is one), descriptions. Writes _knowledge/tserunyan_metric/review_15-27.json,
then review_15-27.html from it (standalone: thumbnails inlined as base64 JPEG). ~5 s. From the repo root:

    python scripts/non_essential/metric_review_page.py

Moved 2026-10-25 from the scratchpad of the session that wrote it (2026-10-23). Dropped on the way: the
"Decisions for you" block (decided since; open items live in _knowledge/umath_todo.md) and the Դաս 15 blur
frames, which only existed in that scratchpad (a participant's name and face; Q6 decided: no blur).
"""
import base64
import html
import io
import json
import logging
import re
import time
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "metric_review_page.log", encoding="utf-8")])
log = logging.getLogger("metric_review_page")

t0 = time.time()
KNOW = REPO / "_knowledge" / "tserunyan_metric"
CHAPTER = re.compile(r"^(\s*)((?:\d+:)?\d+:\d{2}(?:\.\d+)?)\s+(.*)$")
CUT = re.compile(r"Cut\s+(\d+)\s+(\S+)\s+->\s+(\S+)")
THUMB_TEXT = {"18": "Տոպոլոգիական տարածություն։ Զարիսկու տոպոլոգիա",
              "25": "Կոմպակտ և հաջորդականորեն կոմպակտ"}


def secs(ts: str) -> float:
    return sum(float(v) * 60 ** i for i, v in enumerate(reversed(ts.split(":"))))


def hms(s: float) -> str:
    s = int(s + 0.5)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def chapters(path: Path) -> list[tuple[str, str, bool]]:
    """(time, label, nested) per line; nested = indented sub-chapter (DECISIONS #39)."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        m = CHAPTER.match(line)
        if not m:
            raise ValueError(f"{path}: unparsed line {line!r}")
        out.append((m[2], m[3].strip(), bool(m[1])))
    return out


def studio_list(path: Path) -> list[tuple[float, float]]:
    """Cut times of a Studio list (H:MM:SS:FF at 25 fps)."""
    return sorted((secs(m[2].rsplit(":", 1)[0]) + int(m[2].rsplit(":", 1)[1]) / 25,
                   secs(m[3].rsplit(":", 1)[0]) + int(m[3].rsplit(":", 1)[1]) / 25)
                  for line in path.read_text(encoding="utf-8").splitlines() if (m := CUT.match(line)))


def jpeg_b64(path: Path, width: int = 720, quality: int = 80) -> str:
    im = Image.open(path).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def review_sections() -> dict[str, str]:
    text = (KNOW / "review_15-27.md").read_text(encoding="utf-8")
    parts = re.split(r"^## Դաս (\d+).*$", text, flags=re.M)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts), 2)}


notes = review_sections()
codex = json.loads((KNOW / "codex_review_15-27.json").read_text(encoding="utf-8"))["lectures"]
lectures = []
for folder in sorted((REPO / "output").glob("2026-10-21_Das-*-Metric-Spaces-and-Topology_*")):
    n = folder.name.split("_")[1].split("-")[1]
    vid = folder.name.split("Topology_")[1]  # ids can contain "_" (3E1Tmzyoy_s)
    ep = folder / "edited_predicted"
    raw_after = chapters(ep / "timestamps_raw.txt")
    raw_before = chapters(ep / "timestamps_raw_before_review.txt")
    edited = chapters(ep / "timestamps.txt")
    if len(edited) != len(raw_after):
        raise ValueError(f"Das {n}: {len(edited)} edited vs {len(raw_after)} raw chapters")
    codex_base = ep / "timestamps_raw_before_codex.txt"
    raw_mid = chapters(codex_base) if codex_base.exists() else raw_after
    mid_lines = {(t, lab) for t, lab, _ in raw_mid}
    before_lines = {(t, lab) for t, lab, _ in raw_before}
    before_times = {t for t, _, _ in raw_before}
    before_labels = {lab for _, lab, _ in raw_before}
    rows = []
    for (rt, lab, nested), (et, _, _) in zip(raw_after, edited):
        if (rt, lab) in before_lines:
            status = ""
        elif rt not in before_times and lab not in before_labels:
            status = "new"
        elif rt not in before_times:
            status = "moved"
        else:
            status = "relabelled"
        rows.append({"edited": et, "raw": rt, "label": lab, "nested": nested, "status": status,
                     "by": "" if not status else ("Claude" if (rt, lab) in mid_lines else "Codex")})
    ep_json = json.loads((folder / "edit_points.json").read_text(encoding="utf-8"))
    studio = studio_list(folder / "studio_cuts.txt")
    ticked = []  # overlapping ticked cuts become one Studio cut (Das 20: three at the start)
    for a, b in sorted((c["start"], c["end"]) for c in ep_json["cuts"] if c["default"]):
        if ticked and a <= ticked[-1][1] + 0.05:
            ticked[-1] = (ticked[-1][0], max(ticked[-1][1], b))
        else:
            ticked.append((a, b))
    if len(ticked) != len(studio) or any(abs(a - c) > 0.06 or abs(b - d) > 0.06
                                         for (a, b), (c, d) in zip(ticked, studio)):
        raise ValueError(f"Das {n}: ticked cuts in edit_points.json do not match studio_cuts.txt:\n"
                         f"  ticked {[(round(a, 2), round(b, 2)) for a, b in ticked]}\n"
                         f"  studio {[(round(a, 2), round(b, 2)) for a, b in studio]}")
    user_file = folder / "studio_cuts_to_enter.txt"
    user = studio_list(user_file) if user_file.exists() else None
    cuts = [{"id": c["id"], "start": hms(c["start"]), "end": hms(c["end"]), "dur": round(c["end"] - c["start"], 1),
             "ticked": c["default"], "kind": c["kind"], "reason": c["reason"]}
            for c in sorted(ep_json["cuts"], key=lambda c: c["start"])]
    titles = [t.strip() for t in (ep / "titles.txt").read_text(encoding="utf-8").splitlines() if t.strip()]
    titles_before = [t.strip() for t in (ep / "titles_before_review.txt").read_text(encoding="utf-8").splitlines() if t.strip()]
    lectures.append({
        "n": n, "video_id": vid, "titles": titles, "titles_changed": titles != titles_before,
        "thumbnail": f"thumbnails/umath/metric_{n}.png", "thumb_text": THUMB_TEXT.get(n),
        "chapters": rows, "cuts": cuts,
        "removed_s": round(sum(b - a for a, b in ticked), 1),  # merged, so overlaps count once
        "user_list": None if user is None else {"cuts": len(user), "removed_s": round(sum(b - a for a, b in user), 1)},
        "duration_s": ep_json["duration"],
        "description": (ep / "description.txt").read_text(encoding="utf-8"),
        "review": notes.get(n, ""),
        "codex": codex.get(n),
    })
data = {"generated": time.strftime("%Y-%m-%d %H:%M"), "lectures": lectures}
(KNOW / "review_15-27.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------- HTML ----------------
E = html.escape


def md_inline(s: str) -> str:
    s = E(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def md_block(text: str) -> str:
    items, cur = [], None
    for line in text.splitlines():
        if line.startswith("- "):
            if cur is not None:
                items.append(cur)
            cur = line[2:]
        elif line.strip() and cur is not None:
            cur += " " + line.strip()
    if cur is not None:
        items.append(cur)
    return "<ul>" + "".join(f"<li>{md_inline(i)}</li>" for i in items) + "</ul>"


def codex_html(l: dict) -> str:
    c = l["codex"]
    if not c:
        return ""
    rows = "".join(f'<tr class="{"" if f["verdict"] == "take" else "unticked"}"><td class="num">{E(f["time"])}</td>'
                   f'<td>{E(f["verdict"])}</td><td>{E(f.get("insert") or (f.get("replace") or ["", ""])[1] or "")}</td>'
                   f'<td>{E(f["why"])}</td></tr>' for f in c["findings"])
    return (f'<p><b>Codex second review</b> <span class="muted">({E(c["codex_report"])}; title: {E(c["title"])}; '
            f'report: <code>edited_predicted/review_codex.md</code>)</span></p>'
            '<table><colgroup><col style="width:12%"><col style="width:8%"><col style="width:35%"><col style="width:45%"></colgroup>'
            f'<tr><th>Time</th><th>Verdict</th><th>Applied as</th><th>Why</th></tr>{rows}</table>'
            f'<p class="muted">Lecturer points (not published, DECISIONS.md #25): {E(c["lecturer_mistakes"])}</p>')


def active_removed(l: dict) -> float:
    return l["user_list"]["removed_s"] if l["user_list"] else l["removed_s"]


total_ch = sum(len(l["chapters"]) for l in lectures)
nested_ch = sum(1 for l in lectures for r in l["chapters"] if r["nested"])
changed = [(l["n"], r) for l in lectures for r in l["chapters"] if r["status"]]
toc = ['<li><a href="#summary">Summary</a></li>'] + \
      [f'<li><a href="#d{l["n"]}">Դաս {l["n"]}</a> <span class="muted">{E(l["titles"][0].split(" | ")[1])}</span></li>'
       for l in lectures]
out = [f"""<!doctype html><html lang="hy"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tserunyan 15-27 review</title>
<style>
:root {{ --bg:#fbfaf7; --fg:#1d1d1f; --muted:#6b6b70; --line:#dedbd3; --card:#fff; --hi:#fff4c2; --new:#dff3e3; --code:#f1efe9; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#17171a; --fg:#e8e6e1; --muted:#9a9aa0; --line:#33333a; --card:#1f1f24; --hi:#4a4220; --new:#1f3d27; --code:#2a2a30; }} }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; margin:0 auto; max-width:1100px; padding:16px; }}
h1 {{ font-size:24px; margin:8px 0 4px; }} summary {{ cursor:pointer; font-weight:600; font-size:18px; padding:6px 0; }}
details {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:4px 14px; margin:12px 0; }}
.muted {{ color:var(--muted); font-size:13px; }} code {{ background:var(--code); padding:0 3px; border-radius:3px; }}
table {{ border-collapse:collapse; width:100%; table-layout:fixed; font-size:14px; margin:8px 0; }}
th, td {{ border-bottom:1px solid var(--line); padding:4px 6px; text-align:left; vertical-align:top; word-wrap:break-word; }}
th {{ font-size:12px; color:var(--muted); font-weight:600; }}
td.num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
td.child {{ padding-left:28px; }}
tr.relabelled td, tr.moved td {{ background:var(--hi); }} tr.new td {{ background:var(--new); }}
tr.unticked td {{ color:var(--muted); }}
pre {{ background:var(--code); padding:10px; border-radius:6px; white-space:pre-wrap; font-size:13px; }}
img {{ max-width:100%; height:auto; border-radius:6px; }}
.grid {{ display:grid; grid-template-columns:minmax(0,360px) minmax(0,1fr); gap:16px; align-items:start; }}
@media (max-width:700px) {{ .grid {{ grid-template-columns:1fr; }} }}
.tag {{ font-size:11px; padding:1px 6px; border-radius:9px; background:var(--code); }}
</style></head><body>
<h1>Tserunyan 15-27: review before Studio and push</h1>
<p class="muted">Generated {data['generated']} from the repo files (data: <code>_knowledge/tserunyan_metric/review_15-27.json</code>).
Chapters are the reviewed, nested masters remapped onto the active cut list (the user's own list where there is one, else
the plan); they get snapped to the edited videos' captions after the Studio edit. Open items:
<code>_knowledge/umath_todo.md</code>.</p>
<nav><b>Contents</b><ol>{''.join(toc)}</ol></nav>
<details open id="summary"><summary>Summary</summary>
<p>{total_ch} chapters in 13 lectures, {nested_ch} of them nested sub-chapters; {len(changed)} changed by the review
({sum(1 for _, r in changed if r['status']=='new')} new, {sum(1 for _, r in changed if r['status']=='moved')} moved,
{sum(1 for _, r in changed if r['status']=='relabelled')} relabelled; highlighted in each table).
The active cut lists remove {hms(sum(active_removed(l) for l in lectures))} in total.</p>
<table><colgroup><col style="width:11%"><col style="width:51%"><col style="width:9%"><col style="width:9%"><col style="width:10%"><col style="width:10%"></colgroup>
<tr><th>Lecture</th><th>Title</th><th>Chapters</th><th>Changed</th><th>Cut</th><th>Cut list</th></tr>"""]
for l in lectures:
    nchg = sum(1 for r in l["chapters"] if r["status"])
    out.append(f'<tr><td><a href="#d{l["n"]}">Դաս {l["n"]}</a></td><td>{E(l["titles"][0].split(" | ")[1])}</td>'
               f'<td class="num">{len(l["chapters"])}</td><td class="num">{nchg}</td><td class="num">{hms(active_removed(l))}</td>'
               f'<td>{"user" if l["user_list"] else "plan"}</td></tr>')
out.append("</table></details>")
for l in lectures:
    thumb = jpeg_b64(REPO / l["thumbnail"])
    alts = "".join(f"<li>{E(t)}</li>" for t in l["titles"][1:])
    tt = f'<p class="muted">Thumbnail text: {E(l["thumb_text"])}</p>' if l["thumb_text"] else ""
    u = l["user_list"]
    cut_note = (f"the user's own list (<code>studio_cuts_to_enter.txt</code>): {u['cuts']} cuts removing {hms(u['removed_s'])}, "
                f"{hms(l['duration_s'])} -> {hms(l['duration_s'] - u['removed_s'])}. The plan below is what it started from"
                if u else f"ticked cuts remove {hms(l['removed_s'])}, {hms(l['duration_s'])} -> {hms(l['duration_s'] - l['removed_s'])}")
    out.append(f"""<details open id="d{l['n']}"><summary>Դաս {l['n']} <span class="muted">({E(l['video_id'])})</span></summary>
<div class="grid"><div><img alt="thumbnail Das {l['n']}" src="data:image/jpeg;base64,{thumb}">{tt}</div>
<div><p><b>{E(l['titles'][0])}</b></p><p class="muted">Other title options:</p><ul>{alts}</ul>
<p class="muted">Claude review:</p>{md_block(l['review'])}</div></div>{codex_html(l)}
<p><b>Chapters</b> <span class="muted">(edited time on the active cut list; raw = upload time; indented = sub-chapter)</span></p>
<table><colgroup><col style="width:11%"><col style="width:11%"><col style="width:66%"><col style="width:12%"></colgroup>
<tr><th>Edited</th><th>Raw</th><th>Label</th><th>Review</th></tr>""")
    for r in l["chapters"]:
        tag = f'<span class="tag">{r["status"]} · {r["by"]}</span>' if r["status"] else ""
        label_cls = ' class="child"' if r["nested"] else ""
        out.append(f'<tr class="{r["status"]}"><td class="num">{E(r["edited"])}</td><td class="num">{E(r["raw"])}</td>'
                   f'<td{label_cls}>{E(r["label"])}</td><td>{tag}</td></tr>')
    out.append(f"""</table><p><b>Cut plan</b> <span class="muted">({cut_note}; grey = unticked suggestion)</span></p>
<table><colgroup><col style="width:7%"><col style="width:10%"><col style="width:10%"><col style="width:8%"><col style="width:10%"><col style="width:55%"></colgroup>
<tr><th>Id</th><th>Start</th><th>End</th><th>Seconds</th><th>Kind</th><th>What it removes</th></tr>""")
    for c in l["cuts"]:
        out.append(f'<tr class="{"" if c["ticked"] else "unticked"}"><td>{E(c["id"])}</td><td class="num">{c["start"]}</td>'
                   f'<td class="num">{c["end"]}</td><td class="num">{c["dur"]}</td><td>{E(c["kind"])}{"" if c["ticked"] else " (off)"}</td>'
                   f'<td>{E(c["reason"])}</td></tr>')
    out.append(f'</table><p><b>Description</b> <span class="muted">(the first 4 lines are local only)</span></p><pre>{E(l["description"])}</pre></details>')
out.append("</body></html>")
page = KNOW / "review_15-27.html"
page.write_text("\n".join(out), encoding="utf-8")
log.info(f"{page} {page.stat().st_size / 1e6:.2f} MB; {total_ch} chapters ({nested_ch} nested), {len(changed)} changed; "
         f"{time.time() - t0:.1f} s")
