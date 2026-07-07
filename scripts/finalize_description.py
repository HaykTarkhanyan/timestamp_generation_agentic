#!/usr/bin/env python
"""Copy a finished per-video description.txt into the shared final/ folder,
renamed by lesson number (ML<NN>.txt) to match the thumbnail naming — so every
paste-ready description lives in one place, next to nothing else to dig through.

The lesson number is read from the [NN] prefix of the chosen title on the first
line of description.txt (e.g. "🎬 Վերնագիր՝ [11] ...").

Usage:
  python scripts/finalize_description.py --output-dir output/<date>_<slug>_<id>
  python scripts/finalize_description.py --all      # backfill every output/*/
"""
import argparse
import logging
import re
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FINAL_DIR = Path("final")
LOG_DIR = Path("logs")
NUM_RE = re.compile(r"\[(\d{1,2})\]")

log = logging.getLogger("finalize_description")


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "finalize_description.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def finalize(output_dir: Path) -> Path:
    """Copy output_dir/description.txt -> final/ML<NN>.txt. Raises loudly if the
    description is missing or has no [NN] lesson number."""
    desc = output_dir / "description.txt"
    if not desc.exists():
        raise FileNotFoundError(f"No description.txt in {output_dir}")
    first_line = desc.read_text(encoding="utf-8").splitlines()[0]
    m = NUM_RE.search(first_line)
    if not m:
        raise ValueError(
            f"No [NN] lesson number in first line of {desc}: {first_line!r}")
    FINAL_DIR.mkdir(exist_ok=True)
    dest = FINAL_DIR / f"ML{int(m.group(1)):02d}.txt"
    shutil.copyfile(desc, dest)
    log.info(f"Copied {desc} -> {dest}")
    return dest


def main():
    setup_logging()
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--output-dir", help="A single per-video output folder")
    g.add_argument("--all", action="store_true",
                   help="Backfill every output/*/description.txt")
    args = ap.parse_args()

    if args.all:
        dirs = sorted(p.parent for p in Path("output").glob("*/description.txt"))
        if not dirs:
            log.warning("No output/*/description.txt found")
        done = 0
        for d in dirs:
            try:
                finalize(d)
                done += 1
            except (ValueError, FileNotFoundError) as e:
                # No [NN] (e.g. older math-series folders) — log loudly, skip.
                log.error(f"Skipping {d.name}: {e}")
        log.info(f"Finalized {done}/{len(dirs)} description(s)")
    else:
        finalize(Path(args.output_dir))


if __name__ == "__main__":
    main()
