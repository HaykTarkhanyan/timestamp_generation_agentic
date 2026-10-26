"""Tserunyan 16-27 end step (the user's Q57/Q70), local only, no YouTube writes. Per lecture, one at a time:
fetch the edited captions with yt-dlp into edited/ (no API quota), check they belong to the edited video (length
= the predicted one, last caption inside it), snap the chapters (--hms), verifier, metric_assemble.py, glossary
check, title <= 100 chars and the description's title line = titles.txt line 1. A failing lecture is reported
and the run goes on; exit 1 at the end if any failed. ~15-25 s per lecture, ~4 min for 12. Repo root."""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
SK = REPO / ".claude/skills/youtube-timestamps/scripts"
LESSONS = [int(a) for a in sys.argv[1:]] or list(range(16, 28))


def run(cmd, ok=(0,)):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode not in ok:
        raise RuntimeError(f"exit {r.returncode}: {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-1500:]}")
    return r.returncode, r.stdout + r.stderr


def secs(t):
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


failed, t_all = [], time.time()
for n in LESSONS:
    t0 = time.time()
    try:
        (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
        vid = d.name.split("_", 2)[2]
        ep, ed = d / "edited_predicted", d / "edited"
        run([SK / "fetch_subtitles.py", f"https://www.youtube.com/watch?v={vid}", "--output-dir", ed, "--lang", "hy"])
        dur = json.loads((ed / "metadata.json").read_text(encoding="utf-8"))["duration"]
        pred = json.loads((ep / "metadata.json").read_text(encoding="utf-8"))["duration"]
        last = [l for l in (ed / "transcript.txt").read_text(encoding="utf-8").splitlines() if l.strip()][-1]
        last_t = secs(last.split(" ", 1)[0])
        if abs(dur - pred) > 2 or last_t > dur:
            raise RuntimeError(f"captions look stale: video {dur} s, predicted {pred} s, last caption at {last_t} s")
        _, snap = run(["scripts/non_essential/snap_chapters_to_captions.py", d, "--hms"])
        (ed / "logs").mkdir(exist_ok=True)
        (ed / "logs" / "snap_batch.txt").write_text(snap, encoding="utf-8")
        moved = len(re.findall(r"moved", snap, re.I))
        unmatched = len(re.findall(r"unmatched", snap, re.I))
        code, ver = run([SK / "verify_timestamps.py", ed / "timestamps.txt", "--metadata", ed / "metadata.json",
                         "--transcript", ed / "transcript.txt", "--min-gap", "30"], ok=(0, 1))
        (ed / "verify_report_final.txt").write_text(ver, encoding="utf-8")
        if code:
            raise RuntimeError(f"verifier INVALID, see {ed / 'verify_report_final.txt'}")
        run(["scripts/non_essential/metric_assemble.py", n])
        gcode, glo = run([SK / "glossary_check.py", ed / "timestamps.txt", ed / "titles.txt", ed / "description.txt"],
                         ok=(0, 1))
        (ed / "glossary_report.txt").write_text(glo, encoding="utf-8")
        kinds = {k: len(re.findall(rf"\b{k}\b", glo)) for k in ("DENY", "NEAR", "ENG")}
        title = (ed / "titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
        desc0 = (ed / "description.txt").read_text(encoding="utf-8").splitlines()[0]
        if len(title) > 100:
            raise RuntimeError(f"title is {len(title)} chars, YouTube allows 100")
        if desc0 != f"🎬 Վերնագիր՝ {title}":
            raise RuntimeError(f"description title line differs from titles.txt: {desc0!r}")
        chapters = sum(1 for l in (ed / "timestamps.txt").read_text(encoding="utf-8").splitlines() if l.strip())
        print(f"{time.strftime('%H:%M:%S')} Das {n}: video {dur // 3600}:{dur % 3600 // 60:02d}:{dur % 60:02d}, "
              f"{chapters} chapters, snap log 'moved' x{moved} 'unmatched' x{unmatched}, verifier valid, glossary "
              f"{kinds}{' (DENY: fix before push)' if gcode else ''}, title {len(title)} chars | {time.time() - t0:.0f} s",
              flush=True)
    except Exception as e:
        failed.append(n)
        print(f"{time.strftime('%H:%M:%S')} ERROR Das {n}: {e} | {time.time() - t0:.0f} s", flush=True)
print(f"done in {time.time() - t_all:.0f} s; failed: {failed or 'none'}", flush=True)
sys.exit(1 if failed else 0)
