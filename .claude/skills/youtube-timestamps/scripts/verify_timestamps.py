"""Verify a proposed YouTube chapter list against the fetched transcript.

Usage:
    python verify_timestamps.py output/<id>/timestamps.txt \
        --metadata output/<id>/metadata.json \
        --transcript output/<id>/transcript.txt \
        [--min-gap 30]

Exit code:
    0  all checks passed
    1  one or more issues (still prints the report)

Output: JSON to stdout (and writes verify_report.json next to the input).
"""
import argparse
import json
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


# Sub-chapters are indented with spaces before the timestamp (see SKILL.md);
# YouTube parses those fine, so accept and ignore the leading indent here.
TS_LINE_RE = re.compile(r"^[ 	]*(\d{1,2}(?::\d{2}){1,2})\s+(.+)$")
TRANSCRIPT_LINE_RE = re.compile(r"^(\d{1,2}(?::\d{2}){1,2})\s{2,}(.+)$")


def parse_ts(s: str) -> int:
    parts = [int(p) for p in s.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise ValueError(f"bad timestamp {s!r}")


def load_chapters(path: Path) -> tuple[list[tuple[int, str, str]], list[str]]:
    """Return (parsed chapters, issues from parsing)."""
    chapters: list[tuple[int, str, str]] = []
    issues: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = TS_LINE_RE.match(line)
        if not m:
            issues.append(f"Unparseable line: {raw!r}")
            continue
        try:
            ts = parse_ts(m.group(1))
        except ValueError as e:
            issues.append(str(e))
            continue
        chapters.append((ts, m.group(1), m.group(2).strip()))
    return chapters, issues


def load_transcript(path: Path) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = TRANSCRIPT_LINE_RE.match(line.strip())
        if not m:
            continue
        try:
            out.append((parse_ts(m.group(1)), m.group(2).strip()))
        except ValueError:
            continue
    return out


def nearest_transcript_context(
    transcript: list[tuple[int, str]], ts: int, window: int = 15
) -> list[str]:
    """Lines whose timestamp is within [ts-window, ts+window]."""
    return [text for t, text in transcript if ts - window <= t <= ts + window]


def boundary_audit(
    transcript: list[tuple[int, str]], ts: int, window: int = 10
) -> list[tuple[str, bool, str]]:
    """For boundary precision: lines in [ts-window, ts+window] with which side they're on.

    Returns list of (ts_str, is_at_or_after_boundary, text). Lets a human eyeball
    whether the topic transition actually happens AT the proposed boundary or a few
    seconds off.
    """
    out: list[tuple[str, bool, str]] = []
    for t, text in transcript:
        if ts - window <= t <= ts + window:
            mm, ss = divmod(t, 60)
            hh, mm = divmod(mm, 60)
            stamp = f"{hh}:{mm:02d}:{ss:02d}" if hh else f"{mm}:{ss:02d}"
            out.append((stamp, t >= ts, text))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timestamps_file")
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--min-gap", type=int, default=30,
                        help="Minimum seconds between consecutive chapters (default 30)")
    parser.add_argument("--audit-boundaries", action="store_true",
                        help="Print precise +/-10s transcript context around each chapter, "
                             "marking which lines are AT or AFTER the boundary. Useful for "
                             "checking that the topic transition actually starts at the chapter "
                             "stamp rather than 5-10s earlier or later.")
    args = parser.parse_args()

    ts_path = Path(args.timestamps_file)
    metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    duration = int(metadata["duration"])

    chapters, issues = load_chapters(ts_path)
    transcript = load_transcript(Path(args.transcript))

    if not chapters:
        issues.append("No chapters parsed from input.")

    if chapters:
        if chapters[0][0] != 0:
            issues.append(
                f"First chapter must start at 0:00 (YouTube requirement); got {chapters[0][1]}"
            )
        if len(chapters) < 3:
            issues.append(
                f"Need at least 3 chapters for YouTube to render them; got {len(chapters)}"
            )

    for i in range(1, len(chapters)):
        prev_ts, prev_str, _ = chapters[i - 1]
        curr_ts, curr_str, _ = chapters[i]
        if curr_ts <= prev_ts:
            issues.append(f"Not strictly increasing: {prev_str} -> {curr_str}")
        elif curr_ts - prev_ts < args.min_gap:
            issues.append(
                f"Gap below --min-gap ({args.min_gap}s): {prev_str} -> {curr_str} "
                f"({curr_ts - prev_ts}s)"
            )

    for ts, ts_str, label in chapters:
        if ts > duration:
            issues.append(f"Past video end ({duration}s): {ts_str} {label}")

    contexts = [
        {
            "timestamp": ts_str,
            "label": label,
            "transcript_near": nearest_transcript_context(transcript, ts),
        }
        for ts, ts_str, label in chapters
    ]

    report = {
        "valid": len(issues) == 0,
        "issues": issues,
        "chapter_count": len(chapters),
        "duration_seconds": duration,
        "min_gap_seconds": args.min_gap,
        "contexts": contexts,
    }

    out_path = ts_path.parent / "verify_report.json"
    out_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))

    if args.audit_boundaries:
        print("\n=== BOUNDARY AUDIT (>>> = at or after the chapter stamp) ===")
        for ts, ts_str, label in chapters:
            print(f"\n--- {ts_str}  {label} ---")
            for stamp, after, text in boundary_audit(transcript, ts):
                marker = ">>>" if after else "   "
                print(f"{marker} {stamp:>8}  {text}")

    sys.exit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
