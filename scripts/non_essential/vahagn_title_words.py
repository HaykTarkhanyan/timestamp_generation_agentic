"""Check every Armenian word of the Vahagn titles against what he said, the glossary and the series' own wording (the
user, 2026-10-27: "its important that u dont invent words in armenian which the prof didnt use or they are not in
glossary").

    python scripts/non_essential/vahagn_title_words.py        # ~5 s
    -> _knowledge/vahagn_linalg/title_words.json, output/vahagn_linalg_overview/title_words.html

Per word of each title's topic (the part between the pipes): found in this piece's transcript (auto-captions), in
another piece's (21.1-28.4), in the 72 published pieces' titles and chapters (1.1-20.3, overview.json), in the
glossary (Armenian side). Inflection counts as the same word (case, number and article endings: -ը, -ի, -ների, -յով,
-ման for -ում, -ության for -ություն); derivation does not (-ություն, -ական, -վող, -ացիա are other words), so a derived
form he never said is flagged. Words found nowhere are listed with the closest words he did say. Notation (Latin,
digits) is listed apart. glossary_check.py runs on the titles too (DENY / NEAR / ENG).
"""
import html
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
K = REPO / "_knowledge/vahagn_linalg"
OUT_HTML = REPO / "output/vahagn_linalg_overview/title_words.html"
GLOSSARY = REPO / ".claude/skills/youtube-timestamps/assets/glossary.csv"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_title_words.log", encoding="utf-8")])
log = logging.getLogger(__name__)

ARM = re.compile(r"[Ա-Ֆա-և]+")
TS = re.compile(r"^(\d+:\d\d(?::\d\d)?)\s+(.*)$")
# inflection only, longest first; (ending, what replaces it)
ENDINGS = sorted([(e, "") for e in ("ներից", "ներով", "ներում", "ներին", "ների", "ները", "ներն", "ներ", "երից", "երով",
                                    "երում", "երին", "երի", "երը", "երն", "եր", "ից", "ով", "ում", "ին", "ի", "ը", "ն",
                                    "յի", "յով", "յից", "յում", "յին", "յը", "ն")]
                 + [("ության", "ություն"), ("ությամբ", "ություն"), ("ությունը", "ություն"), ("ությունն", "ություն"),
                    ("ման", "ում"), ("մանը", "ում")],
                 key=lambda p: -len(p[0]))


# caption misspellings, applied to the transcripts before matching: he says դիագոնալիզացիա / դիագոնալիզացվող, the captions
# write դիագանալ-, վիագանալ-, դիագալիզ- (read in 24.2.a 01:16-01:29, his definition, and 24.4 00:03; 2026-10-27)
CAPTION_FIXES = [("դիագանալ", "դիագոնալ"), ("վիագանալ", "դիագոնալ"), ("դիագալիզ", "դիագոնալիզ")]
# read by hand, 2026-10-27: the words whose evidence needed reading (proposals use only his words)
FINDINGS = [
    ("Q115", "23.3.a", "Բնութագրիչ բազմանդամ։ Սեփական արժեքների որոնումը",
     "Բնութագրիչ բազմանդամ։ Ինչպես գտնել սեփական արժեքները",
     "«որոնումը» is mine, not his: he uses the verb once, in another sense (15:20 «փոփոխական չենք որոնում իրեն»). "
     "He says «ինչպես գտնել լամդաները» (00:46) and «սեփական արժեքները գտնել» (18:07). Recommend the change."),
    ("Q116", "28.2.b", "Որոշիչի մոդուլը QR ֆակտորիզացիայով", "Դետերմինանտի մոդուլը QR ֆակտորիզացիայով",
     "He never says «որոշիչ» in 21-28; he says «դետերմինանտ» throughout (01:11 «մատրիցի դետերմինանտը գնահատել», 02:04). "
     "«որոշիչ» is the glossary's term (determinant) and the series' own (published 17.1: «որոշիչներ / դետերմինանտ»), so "
     "both pass your rule. Recommend keeping «Որոշիչի» for the glossary and the series; change it for his spoken word."),
    ("Q117", "22.3", "Արտապատկերումների գումարն ու սկալյար բազմապատիկը։ h(T)",
     "Արտապատկերումների գումարն ու սկալյար բազմապատիկը։ h(T), h ∈ F[x]",
     "No invented word, but «h(T)» alone is cryptic. It is a polynomial applied to the map: 08:35 «պատահական բազմանդամ եմ "
     "վերցնում», 09:18 «h-ը ազդում է ոչ թե x փոփոխականի վրա, այլ T արտապատկերման վրա». A wording in his Armenian does "
     "not fit under 100 characters; the board notation h ∈ F[x] (the 08:30 chapter) does. Recommend the change."),
    ("Q118", "27.2", "Գրամ-Շմիդտի պրոցես", "Գրամ-Շմիթի պրոցես",
     "The captions write what he pronounces: «գրամ շմիթի պրոցեսը» (01:24), «գրամշմիտ» (28.4). «Շմիդտ» is my spelling of "
     "the name Schmidt; not in the glossary, and no Armenian source found online to confirm either form. Recommend «Շմիդտ» "
     "(the name's letters d-t), unverified."),
]


def forms(w: str) -> set[str]:
    """The word and what it is with one inflection ending taken off (at least 3 letters left)."""
    out = {w}
    for e, rep in ENDINGS:
        if w.endswith(e) and len(w) - len(e) >= 3:
            out.add(w[:-len(e)] + rep)
    return out


def words(text: str) -> list[str]:
    return ARM.findall(text.replace("՞", "").replace("՛", "").replace("՜", "").lower())


def index(lines: list[tuple[str, str]]) -> dict[str, list[tuple[str, str]]]:
    """lemma form -> [(time, line)]"""
    idx: dict[str, list] = {}
    for t, ln in lines:
        for w in set(words(ln)):
            for f in forms(w):
                idx.setdefault(f, []).append((t, ln))
    return idx


def transcript(d: Path) -> list[tuple[str, str]]:
    out = []
    for ln in (d / "transcript.txt").read_text(encoding="utf-8").splitlines():
        m = TS.match(ln)
        if m:
            text = m[2]
            for a, b in CAPTION_FIXES:
                text = text.replace(a, b)
            out.append((m[1], text))
    return out


def common_prefix(a: str, b: str) -> int:
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    return n


def main() -> None:
    st = json.loads((K / "drafts_status.json").read_text(encoding="utf-8"))
    order = lambda s: [int(p) if p.isdigit() else p for p in s.split(".")]
    secs = sorted(st, key=order)
    titles = {s: (REPO / st[s]["output_dir"] / "edited_predicted/titles.txt").read_text(encoding="utf-8").splitlines()[0]
              for s in secs}
    trans = {s: transcript(REPO / st[s]["output_dir"]) for s in secs}
    own = {s: index(trans[s]) for s in secs}
    vocab_said = {w for s in secs for ln in trans[s] for w in words(ln[1])}
    ov = json.loads((REPO / "output/vahagn_linalg_overview/overview.json").read_text(encoding="utf-8"))
    pub_lines = []
    for v in ov["videos"]:
        if v.get("title", "").startswith("Դաս"):
            pub_lines.append((v["title"].split(" | ")[0], v["title"]))
            for ln in (v.get("description") or "").splitlines():       # the chapter lines of the description
                if re.match(r"^\s*\d+:\d\d", ln):
                    pub_lines.append((v["title"].split(" | ")[0], ln.strip()))
    pub = index(pub_lines)
    gl_lines = []
    for ln in GLOSSARY.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#") or "," not in ln:
            continue
        en, _, rest = ln.partition(",")
        gl_lines.append((en.strip('"'), re.sub(r"\$[^$]*\$", "", rest).strip().rstrip(",")))
    gl = index(gl_lines)

    res = {}
    for s in secs:
        topic = titles[s].split(" | ")[1]
        items = []
        for raw in re.findall(r"[Ա-և՞՛-]+|[A-Za-z0-9^()\-+=_]+", topic):
            for part in [p for p in raw.split("-") if p]:
                ws = words(part)
                if not ws:
                    items.append({"word": part, "notation": True,
                                  "here": [(t, ln) for t, ln in trans[s] if part.lower() in ln.lower()][:3]})
                    continue
                w = ws[0]
                fs = forms(w)
                hit = lambda idx: sorted({x for f in fs for x in idx.get(f, [])})
                here = hit(own[s])
                other = {o: hit(own[o]) for o in secs if o != s}
                other = {o: v for o, v in other.items() if v}
                p, g = hit(pub), hit(gl)
                close = []
                if not here:
                    close = sorted({v for v in vocab_said if common_prefix(v, w) >= max(4, min(len(w), len(v)) - 3)},
                                   key=lambda v: -common_prefix(v, w))[:8]
                items.append({"word": part, "lemma_forms": sorted(fs), "notation": False,
                              "here_n": len(here), "here": here[:3],
                              "other_n": sum(len(v) for v in other.values()), "other": {o: v[:1] for o, v in list(other.items())[:4]},
                              "published": p[:3], "glossary": g[:3], "close_said": close,
                              "status": "here" if here else "course" if (other or p) else "glossary" if g else "none"})
        res[s] = {"title": titles[s], "topic": topic, "words": items}
        bad = [i["word"] for i in items if not i["notation"] and i["status"] == "none"]
        log.info(f"{s:7} {topic}" + (f"   NOT FOUND: {bad}" if bad else ""))

    tmp = K / "_titles_tmp.txt"
    tmp.write_text("\n".join(titles[s] for s in secs) + "\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(REPO / ".claude/skills/youtube-timestamps/scripts/glossary_check.py"), str(tmp)],
                       capture_output=True, text=True, encoding="utf-8", cwd=REPO)
    tmp.unlink()        # this run's own temp file, by its literal name
    gcheck = (r.stdout + r.stderr).strip()
    log.info(f"glossary_check exit {r.returncode}:\n{gcheck}")
    (K / "title_words.json").write_text(json.dumps({"titles": res, "glossary_check": gcheck,
                                                    "glossary_check_exit": r.returncode}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    page(res, gcheck, r.returncode)


COL = {"here": "#0033A0", "course": "#F2A800", "glossary": "#F2A800", "none": "#D90012"}
WHY = {"here": "he says it in this piece", "course": "he says it in another piece, or the published titles/chapters use it",
       "glossary": "only in the glossary", "none": "NOT FOUND: not in any transcript, published title/chapter or the glossary"}


def page(res: dict, gcheck: str, gexit: int) -> None:
    e = html.escape
    rows, secs_html = [], []
    for s, r in res.items():
        sid = "t" + s.replace(".", "_")
        # word by word, never by replacing text: replacing «ու» also hit it inside «Արտապատկերումների» (2026-10-27)
        status = {i["word"]: i["status"] for i in r["words"] if not i["notation"]}
        colored, pos = "", 0
        for m in re.finditer(r"[Ա-և՞՛]+", r["topic"]):
            st_ = status.get(m[0])
            colored += e(r["topic"][pos:m.start()]) + (
                f"<span class='w' style='border-color:{COL[st_]};color:{'#8a5a00' if st_ in ('course', 'glossary') else COL[st_]}' "
                f"title='{WHY[st_]}'>{e(m[0])}</span>" if st_ else e(m[0]))
            pos = m.end()
        colored += e(r["topic"][pos:])
        flags = sum(1 for i in r["words"] if not i["notation"] and i["status"] == "none")
        rows.append(f"<tr><td><a href='#{sid}'>{s}</a></td><td class='tt'>{colored}</td><td>{'⚠ ' + str(flags) if flags else ''}</td></tr>")
        det = []
        for i in r["words"]:
            if i["notation"]:
                ev = "".join(f"<div class='ev'>{e(t)}  {e(ln)}</div>" for t, ln in i["here"]) or "<div class='ev'>not in the captions (formulas are read off the screen)</div>"
                det.append(f"<li><b>{e(i['word'])}</b> <span class='note'>notation</span>{ev}</li>")
                continue
            ev = ""
            if i["here"]:
                ev += f"<div class='src'>said in this piece ({i['here_n']}x):</div>" + "".join(
                    f"<div class='ev'>{e(t)}  {e(ln)}</div>" for t, ln in i["here"])
            if i["other"]:
                ev += f"<div class='src'>said in other pieces ({i['other_n']}x):</div>" + "".join(
                    f"<div class='ev'>{e(o)} {e(v[0][0])}  {e(v[0][1])}</div>" for o, v in i["other"].items())
            if i["published"]:
                ev += "<div class='src'>published titles/chapters (1.1-20.3):</div>" + "".join(
                    f"<div class='ev'>{e(t)}: {e(ln)}</div>" for t, ln in i["published"])
            if i["glossary"]:
                ev += "<div class='src'>glossary:</div>" + "".join(f"<div class='ev'>{e(en)} = {e(hy)}</div>" for en, hy in i["glossary"])
            if i["close_said"]:
                ev += f"<div class='src'>closest words he says:</div><div class='ev'>{e(', '.join(i['close_said']))}</div>"
            det.append(f"<li><b style='color:{COL[i['status']]}'>{e(i['word'])}</b> <span class='note'>{WHY[i['status']]}</span>{ev}</li>")
        secs_html.append(f"<details id='{sid}'><summary>{s}: {e(r['topic'])}</summary><ul>{''.join(det)}</ul></details>")
    n_none = sum(1 for r in res.values() for i in r["words"] if not i["notation"] and i["status"] == "none")
    fnd = []
    for q, s, cur, new, why in FINDINGS:
        if res[s]["topic"] not in (cur, new):
            raise ValueError(f"{q}: {s}'s title is now «{res[s]['topic']}», neither «{cur}» nor «{new}»")
        done = res[s]["topic"] == new
        old_full = res[s]["title"].replace(res[s]["topic"], cur)
        fnd.append(f"<li><b>{q}</b> {s}: {'changed (your answer)' if done else 'kept'}"
                   f"<div class='ev'>was:      {e(old_full)}  ({len(old_full)} chars)</div>"
                   f"<div class='ev'>{'now:     ' if done else 'proposed:'} {e(old_full.replace(cur, new))}  "
                   f"({len(old_full.replace(cur, new))} chars)</div><div class='why'>{e(why)}</div></li>")
    OUT_HTML.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn title words</title><style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:20px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.05em;font-weight:600;cursor:pointer}} details{{margin:10px 0}} h2{{margin-top:28px}}
table{{border-collapse:collapse;width:100%;table-layout:fixed}} td{{border-bottom:1px solid #eee;padding:6px 8px;vertical-align:top}}
col.c1{{width:70px}} col.c3{{width:60px}} .tt{{font-size:1.05em}}
.w{{border-bottom:2px solid;padding:0 1px}} .note{{color:#666;font-size:.85em;font-weight:400}}
.src{{font-size:.8em;color:#555;margin-top:4px}} .ev{{font-family:ui-monospace,monospace;font-size:.82em;color:#333;margin-left:12px;white-space:pre-wrap}}
li{{margin:8px 0}} .why{{margin:4px 0 0 12px;color:#333}} pre{{background:#f6f6f6;padding:10px;white-space:pre-wrap}}
</style></head><body>
<h1>Vahagn 21.1-28.4: every word of the titles, checked</h1>
<nav><b>Contents</b><ul><li><a href="#fnd">Findings to decide (Q115-Q118)</a></li><li><a href="#how">How to read this</a></li><li><a href="#sum">The 25 titles</a></li>
<li><a href="#det">Evidence per title</a></li><li><a href="#gl">Glossary check</a></li></ul></nav>
<details open id="fnd"><summary>Findings to decide (Q115-Q118)</summary><p>Every other word of the 25 titles is
his (in that piece's captions or another piece's) or the glossary's; the evidence is below. These four needed reading:</p>
<ul>{''.join(fnd)}</ul></details>
<details open id="how"><summary>How to read this</summary><p>Each word of each title's topic is coloured by where it was
found. <b style="color:#0033A0">Blue</b>: he says it in that piece (auto-captions). <b style="color:#8a5a00">Orange</b>: he says it in
another piece, or the course's published titles/chapters (1.1-20.3) use it, or only the glossary has it.
<b style="color:#D90012">Red</b>: found nowhere, so possibly an invented word. Endings count as the same word (մատրիցը = մատրից);
derived words do not (օրթոգոնալություն is not օրթոգոնալ). The captions garble words, so a red word may still be his:
the evidence lists the closest words he does say. Hover a word for its source; open a title below for the lines.
Words found nowhere: <b>{n_none}</b>.</p></details>
<details open id="sum"><summary>The 25 titles</summary><table><colgroup><col class="c1"><col><col class="c3"></colgroup>
{''.join(rows)}</table></details>
<details open id="det"><summary>Evidence per title</summary>{''.join(secs_html)}</details>
<details open id="gl"><summary>Glossary check (glossary_check.py, exit {gexit})</summary><pre>{e(gcheck) or "no findings"}</pre></details>
</body></html>""", encoding="utf-8")
    log.info(f"page: {OUT_HTML}")


if __name__ == "__main__":
    main()
