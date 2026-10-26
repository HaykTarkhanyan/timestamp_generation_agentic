"""Predict the edited video's transcript right after a Studio edit is saved, without waiting for
YouTube to process it: map every line of the raw transcript.txt through the Studio cut list.
Chapters, the description and the correctness review can then start at once; YouTube's own
edited captions only confirm them afterwards.

    python scripts/map_transcript_to_edit.py --output-dir output/<dir>
        # ~1 s; writes <output-dir>/edited_predicted/{transcript.txt,metadata.json}
    python scripts/map_transcript_to_edit.py --output-dir output/<dir> --times 0:14:13 1:20:41
        # also prints where those raw times land on the edited timeline

A raw time t maps to t minus the length of every cut that ends at or before t. A line that starts
inside a cut is dropped (cut edges sit in pauses, so it is the removed speech); the count is
logged. Caption times are whole seconds, so a line stamped less than SNAP_S before a cut's end
is the speech right after the cut: it moves to the cut's end instead. YouTube's edited length has matched the cut list every time it was measured: ML48 5327 s,
ML50 2184 s (2184.00 predicted), ML51 2446 s (2445.96 predicted).

The cut list defaults to studio_cuts_to_enter.txt (what was entered and checked in Studio), the
lines "Cut N  H:MM:SS:FF  ->  H:MM:SS:FF", at the frame rate stored in edit_points.json.
"""
import argparse
import json
import logging
import re
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler("logs/map_transcript_to_edit.log", encoding="utf-8")])
log = logging.getLogger(__name__)

LINE = re.compile(r"^((?:\d+:)?\d+:\d{2})\s{2}(.*)$")


def secs(t: str) -> float:
    parts = [float(p) for p in t.split(":")]
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def fmt(t: float, hours: bool) -> str:
    t = int(round(t))
    return f"{t // 3600}:{t // 60 % 60:02d}:{t % 60:02d}" if hours else f"{t // 60:02d}:{t % 60:02d}"


def read_cuts(path: Path, fps: float) -> list[tuple[float, float]]:
    frames = lambda tc: (lambda h, m, s, f: ((h * 60 + m) * 60 + s) + f / fps)(*map(int, tc.split(":")))
    text = path.read_text(encoding="utf-8")
    cuts = sorted((frames(m[1]), frames(m[2])) for line in text.splitlines()
                  if (m := re.match(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)", line)))
    # an empty list only when the file says so (find_edit_points writes "# 0 cuts at ..." when every cut is a
    # suggestion, e.g. a lecturer on camera, DECISIONS #45); any other file without cut lines is the wrong file
    if not cuts and not re.search(r"^# 0 cuts\b", text, flags=re.M):
        raise ValueError(f"no 'Cut N  start  ->  end' lines in {path}")
    for (s0, e0), (s1, e1) in zip(cuts, cuts[1:]):
        if s1 < e0:
            raise ValueError(f"cuts overlap in {path}: {s0:.2f}-{e0:.2f} and {s1:.2f}-{e1:.2f}")
    if any(e <= s for s, e in cuts):
        raise ValueError(f"a cut in {path} ends before it starts")
    return cuts


SNAP_S = 1.5   # caption times are whole seconds: a line stamped up to this long before a cut's end is the speech after it


def to_edited(t: float, cuts: list[tuple[float, float]], snap: float = 0.0) -> float | None:
    """The edited-timeline time of raw time t, or None if t is inside a cut (more than `snap`
    seconds before the cut's end; within that, t moves to the cut's end)."""
    removed = 0.0
    for s, e in cuts:
        if t < s:
            break
        if t < e:
            if e - t > snap:
                return None
            t = e
        removed += e - s
    return t - removed


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--cuts", default="studio_cuts_to_enter.txt", help="cut list file inside the output dir")
    ap.add_argument("--times", nargs="*", default=[], help="raw times (H:MM:SS[.s]) to map and print")
    args = ap.parse_args()
    t0 = time.time()
    d = args.output_dir
    fps = float(json.loads((d / "edit_points.json").read_text(encoding="utf-8"))["fps"])
    meta = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
    cuts = read_cuts(d / args.cuts, fps)
    removed = sum(e - s for s, e in cuts)
    duration = meta["duration"] - removed
    hours = duration >= 3600
    out, dropped, total = [], 0, 0
    for line in (d / "transcript.txt").read_text(encoding="utf-8").splitlines():
        m = LINE.match(line)
        if not m:
            continue
        total += 1
        t = to_edited(secs(m[1]), cuts, snap=SNAP_S)
        if t is None:
            dropped += 1
            continue
        out.append(f"{fmt(t, hours)}  {m[2]}")
    if not out:
        raise ValueError(f"no transcript lines survived the cuts in {d / 'transcript.txt'}")
    od = d / "edited_predicted"
    od.mkdir(exist_ok=True)
    (od / "transcript.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    pmeta = dict(meta, duration=int(round(duration)), predicted_from=f"{args.cuts} ({len(cuts)} cuts)")
    (od / "metadata.json").write_text(json.dumps(pmeta, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info(f"{len(cuts)} cuts remove {removed:.2f} s: {meta['duration']} s -> {duration:.2f} s predicted")
    log.info(f"{total} transcript lines, {dropped} inside cuts dropped, {len(out)} written to {od / 'transcript.txt'}")
    for raw in args.times:
        t = to_edited(secs(raw), cuts)
        if t is None:
            raise ValueError(f"raw time {raw} is inside a cut")
        log.info(f"raw {raw} -> edited {fmt(t, hours)} ({t:.1f} s)")
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
