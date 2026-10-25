"""After a Studio edit is processed: put every chapter on the real word where its anchor text starts, using the per-word timing of
the new captions (find_edit_points.caption_words). Anchor = the first predicted-transcript line at or after
the chapter time; in the real word stream within anchor -6..+6 s, the start word of the 5-word window
that contains most of the anchor's first 4 words (at least 2, ties to the nearest) gives the new time,
floored to the second. Writes <folder>/edited/timestamps.txt (run verify_timestamps.py on it after) and logs every move, every
unmatched chapter and the real words at each final stamp. ~2 s. Repo root.

    python scripts/non_essential/snap_chapters_to_captions.py output/<folder> [...] [--hms]

--hms writes every time as H:MM:SS (0:03:58), for videos over an hour (Ashot, Tserunyan: DECISIONS #34, #39);
without it MM:SS under an hour and HH:MM:SS after, as before.

Needs <folder>/edited_predicted/{transcript,timestamps}.txt (remap_chapters.py) and the new captions in
<folder>/edited/ (fetch_subtitles.py --output-dir <folder>/edited). Measured 2026-10-22: 7 lectures in ~2 s."""
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from find_edit_points import caption_words  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler(REPO / "logs" / "snap_chapters_to_captions.log", encoding="utf-8")])
log = logging.getLogger("snap_chapters_to_captions")


def secs(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


HMS = "--hms" in sys.argv


def fmt(s):
    if HMS:
        return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def nw(s):
    return re.sub(r"[^\w]", "", s.lower())


def load(path):
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*(\d+:\d\d(?::\d\d)?)\s+(.*)", line)
        if m:
            out.append((secs(m.group(1)), m.group(2)))
    return out


for d in map(Path, [a for a in sys.argv[1:] if a != "--hms"]):
    vid = d.name.split("_", 2)[2]
    pred = load(d / "edited_predicted" / "transcript.txt")
    words = sorted((t, nw(w)) for t, w in caption_words((d / "edited" / f"{vid}.hy.vtt").read_text(encoding="utf-8")) if nw(w))
    out, report, moved, unmatched = [], [], 0, 0
    for line in (d / "edited_predicted" / "timestamps.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        indent = line[:len(line) - len(line.lstrip())]  # nested sub-chapters keep their 4 spaces
        ts, label = line.strip().split(" ", 1)
        t = secs(ts)
        if t == 0:
            out.append(f"{fmt(0)} {label}")
            continue
        k = next(i for i, (pt, _) in enumerate(pred) if pt >= t)
        anchor_t = pred[k][0]
        aw = [nw(w) for w in (pred[k][1] + " " + (pred[k + 1][1] if k + 1 < len(pred) else "")).split() if len(nw(w)) > 1][:4]
        best = None
        for i, (wt, _) in enumerate(words):
            if abs(wt - anchor_t) > 6:
                continue
            window = {w for _, w in words[i:i + 5]}
            score = sum(1 for w in aw if w in window)
            # the window must start ON an anchor word, so the stamp lands on the topic's first word
            if words[i][1] not in aw:
                continue
            key = (score, -abs(wt - anchor_t))
            if score >= 2 and (best is None or key > best[0]):
                best = (key, wt)
        kept_late = False
        if best:
            new_t = max(int(best[1]) + (t - anchor_t), 1)
            # a match more than 1 s later is usually a later word of the sentence (the new captions garble
            # the first one: Դաս 22 "Չեբոտարյովը", Դաս 23 a question): keep the original stamp then
            if new_t - t > 1:
                new_t, kept_late = t, True
        else:
            new_t, unmatched = t, unmatched + 1
        moved += new_t != t
        here = " ".join(w for wt, w in words if new_t <= wt < new_t + 4)[:60]
        report.append(f"   {fmt(t)} -> {fmt(new_t)} {'MOVED' if new_t != t else '     '} "
                      f"{'UNMATCHED ' if not best else ''}{'KEPT(late match) ' if kept_late else ''}{label[:40]} | {here}")
        out.append(f"{indent}{fmt(new_t)} {label}")
    (d / "edited" / "timestamps.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    log.info(f"\n#### {d.name[11:17]}: {len(out)} chapters, {moved} moved, {unmatched} unmatched")
    log.info("\n".join(r for r in report if "MOVED" in r or "UNMATCHED" in r))
