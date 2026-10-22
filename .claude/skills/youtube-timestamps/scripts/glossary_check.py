"""Cross-check chapter labels, titles and descriptions against the glossary (assets/glossary.csv).

Usage:
    python glossary_check.py output/<dir>/timestamps.txt [output/<dir>/titles.txt ...]

Runtime: ~1 s per file (measured 2026-10-22).

Three kinds of finding, one line each (`file:line KIND word -> suggestion | the line`):
  DENY  a term from assets/glossary_denylist.csv: a wrong word the user has corrected before
        (e.g. 'չօրինակ' -> 'հակաօրինակ'). Exit code 1: fix these before publishing.
  NEAR  an Armenian word one letter away from a glossary term (after its suffix is dropped) that is
        not itself a glossary word: usually a typo ('կոմումատիվ' -> 'կոմուտատիվ'). Review.
  ENG   an English glossary term in the text without any of the glossary's Armenian forms on the
        same line, e.g. '(splitting field)' next to a different Armenian term. Review.
NEAR and ENG are warnings (exit 0); they need a human or model to decide.

When the user corrects a term, add it to assets/glossary_denylist.csv so it is caught next time.
The checker only sees words: it does not catch wrong math ('gcd = 1' for '≠ 1'); read every label too.
"""
import argparse
import csv
import logging
import re
import sys
from functools import lru_cache
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ASSETS = Path(__file__).resolve().parents[1] / "assets"
REPO = Path(__file__).resolve().parents[4]
ARM_WORD = re.compile(r"[Ա-Ֆա-և]+")
NOT_ARM_BEFORE = r"(?<![Ա-Ֆա-և])"
log = logging.getLogger("glossary_check")


def _armenian_forms(cell: str) -> list[str]:
    """'1․ ընդլայնում (հանրահաշվական օբյեկտի), 2․ շարունակություն' -> ['ընդլայնում', 'շարունակություն']."""
    cell = re.sub(r"\([^)]*\)|\[[^\]]*\]|\$[^$]*\$", " ", cell)
    parts = re.split(r"[,/;]|\d․", cell)
    return [p.strip().lower() for p in parts if ARM_WORD.search(p)]


@lru_cache(maxsize=1)
def load_glossary():
    """English entries (compiled once), the Armenian vocabulary bucketed by first two letters, the denylist."""
    entries = []  # (english, compiled pattern, [armenian forms], [stems])
    vocab = set()
    with open(ASSETS / "glossary.csv", encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) < 2 or not row[0].strip():
                continue
            forms = _armenian_forms(row[1])
            if not forms:
                continue
            eng = row[0].strip()
            if len(eng) >= 6 and not eng.startswith("$"):
                pat = re.compile(r"(?<![A-Za-z])" + re.escape(eng.lower()) + r"(?![A-Za-z])")
                stems = [f.split()[0][:max(4, len(f.split()[0]) - 2)] for f in forms]
                entries.append((eng, pat, forms, stems))
            for f in forms:
                vocab.update(w for w in ARM_WORD.findall(f) if len(w) >= 5)
    buckets, stems = {}, {}
    for v in vocab:
        if len(v) >= 7:
            buckets.setdefault(v[:2], []).append(v)
        for k in range(5, len(v) + 1):  # prefix -> shortest glossary word that has it
            stems[v[:k]] = min(stems.get(v[:k], 99), len(v))
    deny = []
    with open(ASSETS / "glossary_denylist.csv", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            deny.append((re.compile(NOT_ARM_BEFORE + re.escape(row["wrong"].lower())), row["wrong"], row["right"], row["why"]))
    return entries, frozenset(vocab), buckets, stems, deny


def _dist1(a: str, b: str) -> bool:
    """True if a and b differ by exactly one substitution, insertion or deletion."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b):
        a, b = b, a
    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1:]


@lru_cache(maxsize=None)
def _near(word: str):
    """The glossary word this one looks like a misspelling of, or None."""
    _, vocab, buckets, stems, _ = load_glossary()
    # a glossary word with another ending: it shares all but the last <= 3 letters of a glossary word
    # (իդեալ -> իդեալների, տարրերի -> տարրերն, վերլուծում -> վերլուծվում); a typo inside the stem
    # (կոմումատիվ for կոմուտատիվ) does not
    if len(word) < 7 or word in vocab or any(stems.get(word[:k], 99) <= k + 3 for k in range(5, len(word) + 1)):
        return None
    for v in buckets.get(word[:2], ()):
        if _dist1(word[:len(v)], v) or _dist1(word[:len(v) + 1], v) or _dist1(word, v):
            return v
    return None


HAS_LATIN = re.compile(r"[A-Za-z]{6}")
URL = re.compile(r"https?://\S+")


def check_line(line: str) -> list[tuple[str, str, str]]:
    """[(kind, found, suggestion)] for one line of text (links are skipped)."""
    entries, _, _, _, deny = load_glossary()
    low = URL.sub(" ", line).lower()
    out = []
    for pat, wrong, right, why in deny:
        if pat.search(low):
            out.append(("DENY", wrong, f"{right} ({why})"))
    for w in set(ARM_WORD.findall(low)):
        v = _near(w)
        if v:
            out.append(("NEAR", w, v))
    if HAS_LATIN.search(line):
        for eng, pat, forms, stems in entries:
            if pat.search(low) and not any(s in low for s in stems):
                out.append(("ENG", eng, " / ".join(forms)))
    return out


def check_text(text: str) -> list[tuple[int, str, str, str, str]]:
    """[(line number, kind, found, suggestion, line)] for a whole text."""
    return [(i, k, f, s, line.strip()) for i, line in enumerate(text.splitlines(), 1) for k, f, s in check_line(line)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    args = ap.parse_args()
    (REPO / "logs").mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout),
                                  logging.FileHandler(REPO / "logs" / "glossary_check.log", encoding="utf-8")])
    deny_hits = 0
    for path in args.files:
        findings = check_text(path.read_text(encoding="utf-8"))
        for i, kind, found, sugg, line in findings:
            (log.error if kind == "DENY" else log.warning)(f"{path}:{i} {kind} {found} -> {sugg} | {line}")
        deny_hits += sum(1 for f in findings if f[1] == "DENY")
        log.info(f"{path}: {len(findings)} finding(s)")
    return 1 if deny_hits else 0


if __name__ == "__main__":
    sys.exit(main())
