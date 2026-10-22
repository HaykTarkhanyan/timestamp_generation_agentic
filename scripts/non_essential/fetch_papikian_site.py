"""Snapshot Mihran Papikian's Google Site into the repo: every page's text, every link with its
context, and every Drive PDF (course notes, homework, exams, research papers). Recordings (Kaltura,
Drive videos) are listed, not downloaded.

    python scripts/non_essential/fetch_papikian_site.py --plan       # parse only, list the files (~5 s)
    python scripts/non_essential/fetch_papikian_site.py --download   # also the PDFs (~5 min, ~400 MB)

Writes into _knowledge/papikian_site/: pages/<page>.txt, manifest.json, and the PDFs under
algebra_number_theory_2024/, galois_theory_2025/, research/. The PDFs are git-ignored (too big for
the repo), so --download is how a fresh clone gets them back; it also refreshes the snapshot if the
site changed. A non-PDF download is logged as an ERROR and the run exits 1.
Measured 2026-10-22: 104 PDFs, 401.8 MB, 301 s.
"""
import hashlib
import json
import logging
import re
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "_knowledge" / "papikian_site"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "fetch_papikian_site.log", encoding="utf-8")])
log = logging.getLogger("fetch_papikian_site")
BASE = "https://sites.google.com/view/mpapikian"
PAGES = {  # page slug -> folder for its PDFs
    "home": None, "research": "research", "curriculum-vitae": None, "meetings-organized": None,
    "teaching": "galois_theory_2025", "teaching/algebra-and-number-theory": "algebra_number_theory_2024",
}
UA = {"User-Agent": "Mozilla/5.0"}
BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "section"}


def get(url: str) -> tuple[bytes, dict]:
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
    return r.read(), dict(r.headers)


class Page(HTMLParser):
    """Visible text plus links in document order; each link keeps the text of its block before it."""

    def __init__(self):
        super().__init__()
        self.text, self.links, self.block, self.href, self.atext, self.skip = [], [], [], None, [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.text.append("\n")
            self.block = []
        if tag == "a" and a.get("href"):
            self.href, self.atext = a["href"], []

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "a" and self.href:
            self.links.append({"context": " ".join("".join(self.block).split()),
                               "text": " ".join("".join(self.atext).split()), "href": self.href})
            self.href = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self.href:
            self.atext.append(data)
        else:
            self.block.append(data)


def real_url(href: str) -> str:
    """Google Sites wraps some links in google.com/url?q=..."""
    if href.startswith("https://www.google.com/url?"):
        return urllib.parse.parse_qs(urllib.parse.urlparse(href).query)["q"][0]
    return href


def drive_id(url: str) -> str | None:
    m = re.search(r"drive\.google\.com/file/d/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def slug(s: str, n: int = 80) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s[:n].rstrip("_")


def label_of(page: str, ctx: str, text: str) -> str:
    """'Lecture 12 (November 1): ' + 'Notes' -> 'Lecture 12 (November 1): Notes'; ANT anchors are whole."""
    ctx = ctx.rstrip(" ,:")
    if page == "teaching" and ctx and text in ("Notes", "Recording"):
        ctx = re.sub(r":.*$", "", ctx)  # 'Lecture 2 (September 20): Notes,' -> 'Lecture 2 (September 20)'
        return f"{ctx}: {text}"
    return text or ctx


def file_name(page: str, label: str) -> str:
    m = re.match(r"Lecture (\d+)\b.*?(Notes|Problems)$", label)
    if m:
        return f"lecture_{int(m.group(1)):02d}_{m.group(2).lower()}.pdf"
    m = re.match(r"Homework (\d+)", label)
    if m:
        return f"homework_{int(m.group(1))}.pdf"
    return f"{slug(label)}.pdf"


def main(download: bool) -> int:
    t0 = time.time()
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    manifest, failures, by_id = [], [], {}
    for page, folder in PAGES.items():
        html = get(f"{BASE}/{page}")[0].decode("utf-8")
        p = Page()
        p.feed(html)
        lines = [" ".join(l.split()) for l in "".join(p.text).split("\n")]
        (OUT / "pages" / f"{page.replace('/', '__')}.txt").write_text(
            "\n".join(l for l in lines if l) + "\n", encoding="utf-8")
        for l in p.links:
            url = real_url(l["href"])
            if url.startswith(("/view/", "#")) or "google.com/policies" in url:
                continue  # site navigation and section anchors
            label = label_of(page, l["context"], l["text"])
            did = drive_id(url)
            kind = ("recording" if "kaltura" in url or label.endswith("Recording") or "Recording (" in label
                    else "drive_file" if did else "link")
            e = {"page": page, "label": label, "url": url, "kind": kind}
            if kind == "drive_file" and folder:
                if did in by_id:
                    e["file"] = by_id[did]["file"]
                    e["same_file_as"] = by_id[did]["label"]
                else:
                    name, k = file_name(page, label), 2
                    while any(x.get("file") == f"{folder}/{name}" for x in manifest):
                        name = re.sub(r"(_\d+)?\.pdf$", f"_{k}.pdf", name)
                        k += 1
                    e["file"] = f"{folder}/{name}"
                    by_id[did] = e
            manifest.append(e)

    todo = [e for e in manifest if e.get("file") and "same_file_as" not in e]
    log.info(f"{len(manifest)} links, {len(todo)} PDFs to fetch")
    for e in manifest:
        if e["kind"] != "link" or e["page"] != "home":
            log.info(f'  {e["kind"]:10s} {e.get("file", ""):58s} {e["label"][:70]}')
    if not download:
        return 0

    for i, e in enumerate(todo, 1):
        did = drive_id(e["url"])
        try:
            data, hdr = get(f"https://drive.usercontent.google.com/download?id={did}&export=download&confirm=t")
            if not data.startswith(b"%PDF"):
                raise ValueError(f"not a PDF: {hdr.get('Content-Type')}, starts {data[:40]!r}")
        except Exception as ex:  # noqa: BLE001 - recorded and reported below, the run exits 1
            e["error"] = str(ex)
            failures.append(e)
            log.error(f"{i}/{len(todo)} {e['label']}: {ex}")
            continue
        path = OUT / e["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        cd = hdr.get("Content-Disposition", "")
        m = re.search(r"filename\*=UTF-8''([^;]+)", cd) or re.search(r'filename="([^"]+)"', cd)
        e.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                 original_name=urllib.parse.unquote(m.group(1)) if m else None)
        el = time.time() - t0
        log.info(f"{i}/{len(todo)} {len(data) / 1e6:6.2f} MB {e['file']}  ({el:.0f} s elapsed, "
              f"~{el / i * (len(todo) - i):.0f} s left)")
    for e in manifest:  # duplicates inherit the size of the file they point to
        if "same_file_as" in e:
            src = next(x for x in manifest if x.get("file") == e["file"] and "same_file_as" not in x)
            e["bytes"] = src.get("bytes")
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(e.get("bytes", 0) for e in todo)
    log.info(f"done in {time.time() - t0:.0f} s: {len(todo) - len(failures)} PDFs, {total / 1e6:.1f} MB, "
          f"{len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main("--download" in sys.argv))
