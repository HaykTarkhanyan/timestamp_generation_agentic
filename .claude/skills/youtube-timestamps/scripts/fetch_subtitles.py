"""Fetch auto-generated YouTube subtitles via yt-dlp and produce a clean transcript.

Usage:
    python fetch_subtitles.py <youtube-url> [--output-base output] [--lang hy]

The output directory is generated automatically as
    <output-base>/<YYYY-MM-DD>_<latin-slug>_<video-id>/
where <latin-slug> is the video title transliterated from Armenian to Latin,
slugified, and truncated. Pass --output-dir to override with an exact path.

Outputs (in the output directory):
    <video-id>.<lang>.vtt   raw subtitles from yt-dlp
    transcript.txt          cleaned, deduplicated, "MM:SS  text" per line
    metadata.json           id, title, duration, uploader, url
    logs/fetch_subtitles.log

Stdout: JSON with paths and convenience fields (including output_dir).
"""
import argparse
import json
import logging
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"


def setup_console_logging() -> None:
    """Console logging only. Called before the output dir name is known."""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stderr)],
    )


def add_file_logging(output_dir: Path) -> None:
    """Attach a file handler once the output dir exists (dir name needs metadata)."""
    log_dir = output_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_dir / "fetch_subtitles.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(handler)


# Pragmatic Armenian -> Latin map for readable folder slugs (not a strict
# transliteration standard). Digraphs are handled before single chars.
ARM_TO_LAT = {
    "ա": "a", "բ": "b", "գ": "g", "դ": "d", "ե": "e", "զ": "z", "է": "e",
    "ը": "e", "թ": "t", "ժ": "zh", "ի": "i", "լ": "l", "խ": "kh", "ծ": "ts",
    "կ": "k", "հ": "h", "ձ": "dz", "ղ": "gh", "ճ": "ch", "մ": "m", "յ": "y",
    "ն": "n", "շ": "sh", "ո": "o", "չ": "ch", "պ": "p", "ջ": "j", "ռ": "r",
    "ս": "s", "վ": "v", "տ": "t", "ր": "r", "ց": "c", "ւ": "v", "փ": "p",
    "ք": "q", "օ": "o", "ֆ": "f",
}
ARM_DIGRAPHS = {"ու": "u", "ՈՒ": "U", "Ու": "U", "եւ": "ev", "և": "ev"}


def transliterate_armenian(text: str) -> str:
    for arm, lat in ARM_DIGRAPHS.items():
        text = text.replace(arm, lat)
    out: list[str] = []
    for ch in text:
        lat = ARM_TO_LAT.get(ch.lower())
        if lat is None:
            out.append(ch)
        else:
            out.append(lat.capitalize() if ch != ch.lower() else lat)
    return "".join(out)


def slugify(title: str, max_len: int = 35) -> str:
    """Transliterate -> keep [A-Za-z0-9] runs as hyphens -> truncate on a word boundary."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", transliterate_armenian(title)).strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0]
    return slug or "video"


def run_yt_dlp(args: list[str]) -> subprocess.CompletedProcess:
    """Run yt-dlp and surface stderr loudly on failure."""
    logging.info(f"yt-dlp {' '.join(args[1:])}")
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        logging.error(f"yt-dlp failed (exit {result.returncode})")
        logging.error(f"stderr: {result.stderr}")
        raise RuntimeError(f"yt-dlp failed: {result.stderr.strip()}")
    return result


def auth_args(cookies_from_browser: str | None) -> list[str]:
    return ["--cookies-from-browser", cookies_from_browser] if cookies_from_browser else []


def fetch_metadata(url: str, cookies_from_browser: str | None) -> dict:
    result = run_yt_dlp(
        ["yt-dlp", "--dump-json", "--skip-download", *auth_args(cookies_from_browser), url]
    )
    full = json.loads(result.stdout)
    return {
        "id": full["id"],
        "title": full["title"],
        "duration": full["duration"],
        "url": url,
        "uploader": full.get("uploader"),
    }


def fetch_subtitles(
    url: str, lang: str, output_dir: Path, video_id: str, cookies_from_browser: str | None
) -> Path:
    out_template = str(output_dir / "%(id)s.%(ext)s")
    run_yt_dlp([
        "yt-dlp",
        "--write-auto-sub",
        "--sub-lang", lang,
        "--sub-format", "vtt",
        "--skip-download",
        "-o", out_template,
        *auth_args(cookies_from_browser),
        url,
    ])
    vtt_path = output_dir / f"{video_id}.{lang}.vtt"
    if not vtt_path.exists():
        raise RuntimeError(
            f"Expected VTT not found: {vtt_path}. "
            f"Auto-subs for lang={lang!r} may not exist. "
            f"Run `yt-dlp --list-subs {url}` to check."
        )
    return vtt_path


TS_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})\.\d+\s*-->\s*(\d{2}):(\d{2}):(\d{2})\.\d+"
)
TAG_RE = re.compile(r"<[^>]+>")


def parse_vtt(vtt_path: Path) -> str:
    """Parse VTT into 'MM:SS  text' lines, deduplicating YouTube's rolling captions.

    YouTube auto-generated VTT uses a two-line scrolling window:
        Cue A (with <c> per-word timing): top = previous settled line, bottom = new line
        Cue B (a 10ms "placeholder", no timing tags): the just-settled bottom line alone
    So we keep only cues with <c> tags (the "real" ones) and take their LAST text line.

    For manual subtitles (no <c> tags anywhere) we fall back to a simple prefix-dedup
    that handles the older incremental-growth pattern.
    """
    content = vtt_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    is_auto = "<c>" in content

    cues: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        m = TS_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        start = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        i += 1
        block: list[str] = []
        while i < len(lines) and lines[i].strip():
            block.append(lines[i])
            i += 1

        if is_auto:
            if not any("<c>" in line for line in block):
                continue  # skip placeholder cue
            new_line = TAG_RE.sub("", block[-1]).strip()
            new_line = re.sub(r"\s+", " ", new_line)
            if new_line:
                cues.append((start, new_line))
        else:
            text = " ".join(TAG_RE.sub("", line).strip() for line in block).strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                cues.append((start, text))

    if not is_auto:
        # Older incremental-growth pattern: drop cues that are prefixes of the next.
        filtered: list[tuple[int, str]] = []
        for idx, (ts, text) in enumerate(cues):
            if idx + 1 < len(cues):
                nxt = cues[idx + 1][1]
                if nxt.startswith(text) and nxt != text:
                    continue
            filtered.append((ts, text))
        cues = filtered

    settled: list[tuple[int, str]] = []
    for ts, text in cues:
        if settled and settled[-1][1] == text:
            continue
        settled.append((ts, text))

    has_hours = bool(settled) and settled[-1][0] >= 3600
    out_lines: list[str] = []
    for ts, text in settled:
        mm, ss = divmod(ts, 60)
        hh, mm = divmod(mm, 60)
        stamp = f"{hh}:{mm:02d}:{ss:02d}" if has_hours else f"{hh * 60 + mm:02d}:{ss:02d}"
        out_lines.append(f"{stamp}  {text}")
    return "\n".join(out_lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument(
        "--output-base", default="output",
        help="Base dir under which a '<date>_<slug>_<id>' folder is created (default: output).",
    )
    parser.add_argument(
        "--output-dir",
        help="Exact output dir, overriding the auto-generated '<date>_<slug>_<id>' name.",
    )
    parser.add_argument("--lang", default="hy")
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser to pull auth cookies from for private/unlisted/age-gated videos "
             "(e.g. chrome, firefox, edge, brave). Passed straight to yt-dlp.",
    )
    args = parser.parse_args()

    # Console logging first: the output dir name needs the title from metadata.
    setup_console_logging()
    metadata = fetch_metadata(args.url, args.cookies_from_browser)
    logging.info(f"Title: {metadata['title']}")
    logging.info(f"Duration: {metadata['duration']}s")

    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        date = datetime.now().strftime("%Y-%m-%d")
        out_dir = Path(args.output_base) / f"{date}_{slugify(metadata['title'])}_{metadata['id']}"
    out_dir.mkdir(parents=True, exist_ok=True)
    add_file_logging(out_dir)
    logging.info(f"Output dir: {out_dir}")

    meta_path = out_dir / "metadata.json"
    meta_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    vtt_path = fetch_subtitles(
        args.url, args.lang, out_dir, metadata["id"], args.cookies_from_browser
    )
    logging.info(f"VTT saved: {vtt_path}")

    transcript = parse_vtt(vtt_path)
    transcript_path = out_dir / "transcript.txt"
    transcript_path.write_text(transcript, encoding="utf-8")
    line_count = transcript.count("\n")
    logging.info(f"Transcript saved: {transcript_path} ({line_count} lines)")

    print(json.dumps({
        "output_dir": str(out_dir),
        "vtt": str(vtt_path),
        "transcript": str(transcript_path),
        "metadata": str(meta_path),
        "duration_seconds": metadata["duration"],
        "title": metadata["title"],
        "transcript_lines": line_count,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
