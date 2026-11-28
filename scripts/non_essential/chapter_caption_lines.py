"""Show, for every chapter, the caption line of YouTube's regenerated transcript it falls in and the next line.

After a Studio edit is processed, the chapters drafted on edited_predicted/ are checked on the real captions. Read the
two lines per chapter: if the topic sentence starts in the next line (+1 s) or the chapter sits 1-3 s into the topic's
own line, move the chapter to that line's start; leave it where it lands on the topic words.

Do not snap automatically by matching each chapter's predicted first line against the real transcript: on LLM [08]
(2026-11-27) that proposed 19 moves, at least 3 of them wrong (25:12, 46:42, 50:35 already sat on the topic line),
because a chapter remapped to a cut's end is not on a predicted line start. See
_learnings/2026-11-28-0129_check-chapters-on-the-caption-line-they-sit-in.md.

    python scripts/non_essential/chapter_caption_lines.py --output-dir output/<dir>
        # reads <dir>/edited/transcript.txt and <dir>/edited_predicted/timestamps.txt; ~1 s
"""
import argparse
import logging
import re
import sys
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/chapter_caption_lines.log", encoding="utf-8")])
log = logging.getLogger(__name__)
sys.stdout.reconfigure(encoding="utf-8")

LINE = re.compile(r"^((?:\d+:)?\d+:\d{2})\s{2}(.*)$")
CHAPTER = re.compile(r"^\s*((?:\d+:)?\d+:\d{2}) (.*)$")


def secs(t: str) -> int:
    return sum(int(v) * 60 ** i for i, v in enumerate(reversed(t.split(":"))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--transcript", default="edited/transcript.txt")
    ap.add_argument("--timestamps", default="edited_predicted/timestamps.txt")
    args = ap.parse_args()
    t0 = time.time()
    real = [(secs(m.group(1)), m.group(2)) for line in
            (args.output_dir / args.transcript).read_text(encoding="utf-8").splitlines() if (m := LINE.match(line))]
    if not real:
        raise ValueError(f"no caption lines in {args.output_dir / args.transcript}")
    for line in (args.output_dir / args.timestamps).read_text(encoding="utf-8").splitlines():
        m = CHAPTER.match(line)
        if not m:
            raise ValueError(f"not a chapter line: {line!r}")
        t = secs(m.group(1))
        i = max((k for k, (s, _) in enumerate(real) if s <= t), default=0)
        a = real[i]
        b = real[i + 1] if i + 1 < len(real) else (a[0], "")
        log.info(f"{m.group(1)} {m.group(2)[:34]:34} | {a[0] - t:+d}s {a[1][:44]:44} | {b[0] - t:+d}s {b[1][:40]}")
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
