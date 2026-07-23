#!/usr/bin/env python
"""Resolve the GitHub-Pages materials URL for a lesson from the local course repo.

The published notes mirror the repo: a lecture's `.tex` lives in a section folder
(e.g. `ml/03_classification/13_threshold_tuning.tex`), and that folder's chapter
page is what the channel links as "materials" — e.g.
    https://hayktarkhanyan.github.io/python_math_ml_course/ml/03_classification/03_classification.html
So the whole section shares one materials page (lessons 11-16 all map to
03_classification.html; lesson 17 maps to 04_trees.html).

Given a lesson number NN, find the `ml/<folder>/` that contains `<NN>_*.tex`, take
that folder's chapter `.qmd` (stem == folder name), and build the URL.

Usage:
  python .../resolve_materials_url.py --lesson 17          # print the URL
  python .../resolve_materials_url.py --fill output/<dir>  # replace the TODO line in that description.txt
  python .../resolve_materials_url.py --all                # backfill every output/*/description.txt

Fails loudly (raises / logs ERROR) if the lesson can't be resolved — never
guesses a URL. In --fill/--all, a description that already has a real URL is left
untouched, and one whose lesson doesn't resolve keeps its TODO placeholder.
"""
import argparse
import logging
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_REPO = Path("C:/Users/hayk_/OneDrive/Desktop/01_python_math_ml_course")
BASE_URL = "https://hayktarkhanyan.github.io/python_math_ml_course"
TODO_LINE = "TODO: paste materials URL here"
NUM_RE = re.compile(r"\[(\d{1,2})\]")
TEX_NUM_RE = re.compile(r"^(\d+)_")
LOG_DIR = Path("logs")

log = logging.getLogger("resolve_materials_url")


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "resolve_materials_url.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def resolve(lesson: int, repo: Path = DEFAULT_REPO) -> str:
    """Return the materials URL for lesson NN, or raise loudly if not found."""
    ml = repo / "ml"
    if not ml.is_dir():
        raise FileNotFoundError(f"No ml/ directory in course repo: {ml}")
    # map every lecture number to the folder(s) whose `<num>_*.tex` defines it
    num_to_folders: dict[int, set[Path]] = {}
    for folder in sorted(p for p in ml.iterdir() if p.is_dir()):
        for tex in folder.glob("*.tex"):
            m = TEX_NUM_RE.match(tex.name)
            if m:
                num_to_folders.setdefault(int(m.group(1)), set()).add(folder)
    if not num_to_folders:
        raise FileNotFoundError(f"No numbered ml/*/*.tex lectures found under {ml}")
    if lesson in num_to_folders:
        num = lesson
    else:
        # Practicals (e.g. the bank-marketing session) have no own numbered .tex;
        # they belong to their chapter, so map to the nearest lower-numbered
        # lecture's folder (lesson 16 -> lecture 15's chapter, 03_classification).
        lower = [n for n in num_to_folders if n < lesson]
        if not lower:
            raise ValueError(f"No lecture <= {lesson} found under {ml}")
        num = max(lower)
        log.info(f"Lesson {lesson} has no own .tex; using chapter of lecture {num}")
    folders = num_to_folders[num]
    if len(folders) > 1:
        raise ValueError(
            f"Lecture {num} is ambiguous across folders: {[f.name for f in folders]}")
    folder = next(iter(folders))
    chapter = folder / f"{folder.name}.qmd"
    if chapter.exists():
        stem = chapter.stem
    else:
        qmds = list(folder.glob("*.qmd"))
        if len(qmds) == 1:
            stem = qmds[0].stem
        else:
            raise ValueError(
                f"Cannot pick a chapter .qmd in {folder} (found {[q.name for q in qmds]})")
    return f"{BASE_URL}/ml/{folder.name}/{stem}.html"


def fill(output_dir: Path, repo: Path = DEFAULT_REPO) -> str | None:
    """Replace the TODO materials line in output_dir/description.txt with the
    resolved URL. Returns the URL if it wrote one, None if it left the file as-is
    (already had a real URL). Raises if the description or [NN] is missing."""
    desc = output_dir / "description.txt"
    if not desc.exists():
        raise FileNotFoundError(f"No description.txt in {output_dir}")
    text = desc.read_text(encoding="utf-8")
    if TODO_LINE not in text:
        log.info(f"{desc}: no TODO placeholder (already filled?), skipping")
        return None
    first_line = text.splitlines()[0]
    m = NUM_RE.search(first_line)
    if not m:
        raise ValueError(f"No [NN] lesson number in first line of {desc}: {first_line!r}")
    url = resolve(int(m.group(1)), repo)
    desc.write_text(text.replace(TODO_LINE, url), encoding="utf-8")
    log.info(f"{desc}: materials URL -> {url}")
    return url


def main():
    setup_logging()
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--lesson", type=int, help="Print the materials URL for lesson NN")
    g.add_argument("--fill", help="Fill the TODO in a single output/<dir>/description.txt")
    g.add_argument("--all", action="store_true",
                   help="Backfill every output/*/description.txt")
    ap.add_argument("--course-repo", default=str(DEFAULT_REPO),
                    help="Path to the course repo (default: the Desktop clone)")
    args = ap.parse_args()
    repo = Path(args.course_repo)

    if args.lesson is not None:
        print(resolve(args.lesson, repo))
    elif args.fill:
        fill(Path(args.fill), repo)
    else:
        dirs = sorted(p.parent for p in Path("output").glob("*/description.txt"))
        done = 0
        for d in dirs:
            try:
                if fill(d, repo):
                    done += 1
            except (ValueError, FileNotFoundError) as e:
                log.error(f"Skipping {d.name}: {e}")
        log.info(f"Filled {done}/{len(dirs)} description(s)")


if __name__ == "__main__":
    main()
