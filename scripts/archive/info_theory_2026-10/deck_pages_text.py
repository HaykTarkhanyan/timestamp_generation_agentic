"""Print the first 3 text lines of each page in a page range of one deck; also check that the cumulative decks
keep page numbers (page i of an earlier deck == page i of a later one, by text). ~2 s.

    python -I deck_pages_text.py <slides dir> <deck key> <first> <last>
"""
import sys
from pathlib import Path

import fitz

d = Path(sys.argv[1])


def deck(key):
    return fitz.open(next(p for p in d.glob("*.pdf")
                          if p.stem.replace("InformationTheory-ASDS-2026-", "").replace("-posted", "") == key))


doc = deck(sys.argv[2])
a, b = int(sys.argv[3]), int(sys.argv[4])
for i in range(a - 1, min(b, len(doc))):
    lines = [ln.strip() for ln in doc[i].get_text().splitlines() if ln.strip()]
    print(f"p{i + 1}: " + " | ".join(lines[:3])[:160])

# Stable numbering across the part: L-6 -> L-8 -> L-10 -> L-11
chain = ["L-6", "L-8", "L-10", "L-11"]
docs = {k: deck(k) for k in chain}
for early, late in zip(chain, chain[1:]):
    n = len(docs[early])
    same = sum(docs[early][i].get_text() == docs[late][i].get_text() for i in range(n))
    print(f"{early} ({n} p) vs {late} ({len(docs[late])} p): {same}/{n} pages identical by text at the same number")
