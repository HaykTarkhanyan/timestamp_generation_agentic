"""Snapshot Anush Tserunyan's course page (Metric Spaces and Topology, ASOF, spring 2023) into the
repo: the page's HTML and visible text, every link, and every PDF it links (lecture notes 1-27,
homework 1-12, course info).

    python scripts/non_essential/fetch_tserunyan_site.py --plan       # parse only, list the files (~2 s)
    python scripts/non_essential/fetch_tserunyan_site.py --download   # also the PDFs (~1-3 min, guess)

Writes into _knowledge/tserunyan_site/: pages/course.html, pages/course.txt, manifest.json, and the
PDFs under lectures/, homework/, other/. The PDFs are git-ignored, so --download is how a fresh
clone gets them back. A non-PDF download is logged as an ERROR and the run exits 1.
"""
import hashlib
import json
import logging
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "_knowledge" / "tserunyan_site"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "fetch_tserunyan_site.log", encoding="utf-8")])
log = logging.getLogger("fetch_tserunyan_site")
BASE = "https://www.math.mcgill.ca/atserunyan/Courses/2023_S.Yerevan.Metric&Top/"
UA = {"User-Agent": "Mozilla/5.0"}
BLOCK = {"p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "section"}
FOLDERS = {"Lectures": "lectures", "Homework": "homework", "Other files": "other"}


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


class Page(HTMLParser):
    """Visible text plus links in document order."""

    def __init__(self):
        super().__init__()
        self.text, self.links, self.href, self.atext, self.skip = [], [], None, [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BLOCK:
            self.text.append("\n")
        if tag == "a" and a.get("href"):
            self.href, self.atext = a["href"], []

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "a" and self.href:
            self.links.append({"text": " ".join("".join(self.atext).split()), "href": self.href})
            self.href = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self.href:
            self.atext.append(data)


def main() -> int:
    download = "--download" in sys.argv
    if not download and "--plan" not in sys.argv:
        log.error("pass --plan or --download")
        return 2
    t0 = time.time()
    html = get(BASE)
    (OUT / "pages").mkdir(parents=True, exist_ok=True)
    (OUT / "pages" / "course.html").write_bytes(html)
    page = Page()
    page.feed(html.decode("utf-8"))
    text = "\n".join(" ".join(line.split()) for line in "".join(page.text).splitlines())
    text = "\n".join(line for line in text.splitlines() if line)
    (OUT / "pages" / "course.txt").write_text(text + "\n", encoding="utf-8")

    entries = []
    for link in page.links:
        href = link["href"]
        top = href.split("/")[0]
        if href.lower().endswith(".pdf") and top in FOLDERS:
            name = href.split("/")[-1]
            entries.append({"text": link["text"], "href": href, "url": urllib.parse.urljoin(BASE, urllib.parse.quote(href)),
                            "file": f"{FOLDERS[top]}/{name}"})
        else:
            entries.append({"text": link["text"], "href": href, "url": href, "file": None})
    pdfs = [e for e in entries if e["file"]]
    log.info(f"{len(page.links)} links, {len(pdfs)} PDFs")

    bad = 0
    if download:
        for i, e in enumerate(pdfs, 1):
            data = get(e["url"])
            if not data.startswith(b"%PDF"):
                log.error(f"not a PDF: {e['url']} ({len(data)} bytes, starts {data[:20]!r})")
                bad += 1
                continue
            path = OUT / e["file"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            e["bytes"], e["sha256"] = len(data), hashlib.sha256(data).hexdigest()
            elapsed = time.time() - t0
            log.info(f"{i}/{len(pdfs)} {e['file']} {len(data) / 1e6:.1f} MB, {elapsed:.0f}s elapsed, "
                     f"~{elapsed / i * (len(pdfs) - i):.0f}s left")
    (OUT / "manifest.json").write_text(json.dumps({"source": BASE, "links": entries}, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    total = sum(e.get("bytes", 0) for e in pdfs)
    log.info(f"done in {time.time() - t0:.0f}s, {total / 1e6:.1f} MB of PDFs, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
