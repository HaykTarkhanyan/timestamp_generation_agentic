"""Move drafted chapters onto a new cut list: each chapter time goes back to the raw timeline through
the cut list it was drafted on, then forward through the new one. Use it whenever the cut list
changes after the chapters were drafted (the owner's review, extra cuts), instead of redrafting.

    python scripts/remap_chapters.py --output-dir output/<dir> --from-cuts studio_cuts_v1_content_only.txt
        [--from edited_predicted/timestamps_v1_content_only.txt] [--to-cuts studio_cuts_to_enter.txt]
    # ~1 s

--from-cuts is the cut list the --from chapters are timed on ("raw" if they are on the raw timeline).
Writes edited_predicted/timestamps.txt and the chapter block (under "⏳ Թեմաներ") of
edited_predicted/description.txt, both derived from --from, which is never touched. A chapter that
starts inside a new cut moves to that cut's end, where the speech resumes; each such move is logged.
Raises on chapters closer than YouTube's 10 s floor; warns under 30 s. Times are written MM:SS under
an hour and HH:MM:SS from there, as in the drafts. Paths are relative to --output-dir.
Until 2026-10-21 this was a throwaway script (Arnak lessons 11-13 and the 2025 recording).
"""
import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/remap_chapters.log", encoding="utf-8")])
log = logging.getLogger(__name__)

CUT = re.compile(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)")
CHAPTER = re.compile(r"^(\s*)((?:\d+:)?\d+:\d{2})(\s.*)$")
YOUTUBE_MIN_GAP, MIN_GAP = 10, 30


def read_cuts(path: Path, fps: float) -> list[tuple[float, float]]:
    if not path.exists():
        raise FileNotFoundError(path)
    tc = lambda s: (lambda h, m, sec, f: ((h * 60 + m) * 60 + sec) + f / fps)(*map(int, s.split(":")))
    cuts = sorted((tc(m[1]), tc(m[2])) for line in path.read_text(encoding="utf-8").splitlines() if (m := CUT.match(line)))
    if not cuts:
        raise ValueError(f"no 'Cut N  start  ->  end' lines in {path}")
    return cuts


def to_raw(t: float, cuts: list[tuple[float, float]]) -> float:
    for s, e in cuts:
        if s <= t + 1e-6:
            t += e - s
        else:
            break
    return t


def to_edited(t: float, cuts: list[tuple[float, float]]) -> tuple[float, tuple[float, float] | None]:
    """Edited time of raw time t, and the cut t fell inside (it then moves to that cut's end)."""
    removed, inside = 0.0, None
    for s, e in cuts:
        if t < s:
            break
        if t < e:
            t, inside = e, (s, e)
        removed += e - s
    return t - removed, inside


def parse(ts: str) -> int:
    return sum(int(v) * 60 ** i for i, v in enumerate(reversed(ts.split(":"))))


def fmt(s: int) -> str:
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def remap(d: Path, src_name: str, from_cuts: str, to_cuts: str) -> int:
    fps = float(json.loads((d / "edit_points.json").read_text(encoding="utf-8"))["fps"])
    old = [] if from_cuts == "raw" else read_cuts(d / from_cuts, fps)
    new = read_cuts(d / to_cuts, fps)
    out, times = [], []
    for line in (d / src_name).read_text(encoding="utf-8").splitlines():
        m = CHAPTER.match(line)
        if not m:
            raise ValueError(f"{d / src_name}: unparsed chapter line {line!r}")
        raw = to_raw(parse(m[2]), old)
        edited, inside = to_edited(raw, new)
        t = 0 if parse(m[2]) == 0 else int(edited + 0.5)
        if inside and t:
            log.info(f"moved to the end of cut {inside[0]:.2f}-{inside[1]:.2f} s (raw): {m[3].strip()[:60]}")
        times.append(t)
        out.append(f"{m[1]}{fmt(t)}{m[3]}")
    gaps = [(b - a, out[k + 1].strip()) for k, (a, b) in enumerate(zip(times, times[1:]))]
    too_close = [(g, c) for g, c in gaps if g < YOUTUBE_MIN_GAP]
    if too_close:
        raise ValueError(f"chapters under YouTube's {YOUTUBE_MIN_GAP} s floor after remapping: {too_close}")

    desc = d / "edited_predicted" / "description.txt"
    lines = desc.read_text(encoding="utf-8").splitlines()
    # the umath series write "⏳Թեմաներ" (no space after the hourglass), the ML series "⏳ Թեմաներ՝"
    i = next((k for k, line in enumerate(lines) if line.startswith(("⏳ Թեմաներ", "⏳Թեմաներ"))), None)
    if i is None:
        raise ValueError(f"{desc}: no '⏳ Թեմաներ' / '⏳Թեմաներ' header")
    j = next((k for k in range(i + 1, len(lines)) if not lines[k].strip()), len(lines))
    if j - i - 1 != len(out):
        raise ValueError(f"{desc}: chapter block has {j - i - 1} lines, {src_name} has {len(out)}")
    lines[i + 1:j] = out
    (d / "edited_predicted" / "timestamps.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    desc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for g, c in gaps:
        if g < MIN_GAP:
            log.warning(f"only {g} s before: {c[:60]}")
    log.info(f"{len(out)} chapters from {src_name} ({from_cuts} -> {to_cuts}); smallest gap {min(g for g, _ in gaps)} s; "
             f"wrote edited_predicted/timestamps.txt and the chapter block of {desc.name}")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--from", dest="src", default="edited_predicted/timestamps_v1_content_only.txt",
                    help="the drafted chapters (default: %(default)s)")
    ap.add_argument("--from-cuts", required=True, help='the cut list --from is timed on, or "raw"')
    ap.add_argument("--to-cuts", default="studio_cuts_to_enter.txt", help="the new cut list (default: %(default)s)")
    a = ap.parse_args()
    t0 = time.time()
    code = remap(a.output_dir, a.src, a.from_cuts, a.to_cuts)
    log.info(f"done in {time.time() - t0:.1f} s")
    sys.exit(code)


if __name__ == "__main__":
    main()
