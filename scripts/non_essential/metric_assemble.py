"""Tserunyan: build <folder>/edited/description.txt and edited/titles.txt from edited_predicted/ (the reviewed
draft: title header, links, abstract) and edited/timestamps.txt (chapters snapped to the edited captions).
Replaces the title header and the chapter block under the '⏳Թեմաներ' header; everything else stays as drafted.
Chapter indentation (nested sub-chapters) is kept. Fails loudly if the layout is not found; checks no ASCII
< or > and <= 5000 chars without the header. ~1 s. From the repo root:

    python scripts/non_essential/metric_assemble.py 15 [16 ...]

Moved 2026-10-25 from the scratchpad of the session that finished Դաս 15 (2026-10-23).
"""
import logging
import shutil
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "metric_assemble.log", encoding="utf-8")])
log = logging.getLogger("metric_assemble")

t0 = time.time()
for n in sys.argv[1:]:
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep, ed = d / "edited_predicted", d / "edited"
    shutil.copy2(ep / "titles.txt", ed / "titles.txt")
    title = (ed / "titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
    draft = (ep / "description.txt").read_text(encoding="utf-8").splitlines()
    chapters = [l.rstrip() for l in (ed / "timestamps.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    if not draft[0].startswith("🎬 Վերնագիր՝ "):
        raise ValueError(f"{d.name}: no title header on line 1")
    heads = [i for i, l in enumerate(draft) if l.startswith(("⏳Թեմաներ", "⏳ Թեմաներ"))]
    if len(heads) != 1:
        raise ValueError(f"{d.name}: {len(heads)} chapter headers")
    head = heads[0]
    end = next(i for i in range(head + 1, len(draft)) if not draft[i].strip())
    if end - head - 1 != len(chapters):
        raise ValueError(f"{d.name}: draft has {end - head - 1} chapter lines, snapped list has {len(chapters)}")
    out = [f"🎬 Վերնագիր՝ {title}"] + draft[1:head + 1] + chapters + draft[end:]
    text = "\n".join(out) + "\n"
    body = "\n".join(out[4:])
    if "<" in text or ">" in text:
        raise ValueError(f"{d.name}: ASCII < or > in the description")
    if len(body) > 5000:
        raise ValueError(f"{d.name}: {len(body)} chars, over YouTube's 5000")
    (ed / "description.txt").write_text(text, encoding="utf-8")
    nested = sum(1 for c in chapters if c.startswith(" "))
    log.info(f"Das {n}: {len(chapters)} chapters ({nested} nested), {len(body)} chars, title: {title}")
log.info(f"done in {time.time() - t0:.1f} s")
