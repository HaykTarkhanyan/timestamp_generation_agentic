"""Tserunyan 16-27: re-plan with the content cuts + silences of 5 s or more (no hum join), keep the result as
*_v3_5s, remap the reviewed chapters (edited_predicted/timestamps_raw.txt) onto it and run the verifier.
Դաս 15: remap onto the user's hand edit (studio_cuts_edited.txt). Sequential; ~30-60 s per lecture.

    python metric_replan5.py 15 16 ... 27      (from the repo root)
"""
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
BK = Path(__file__).parent / "replan5_backup"
VERIFY = REPO / ".claude/skills/youtube-timestamps/scripts/verify_timestamps.py"


def run(cmd: list, log: Path | None = None) -> str:
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    out = r.stdout + r.stderr
    if log:
        log.write_text(out, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"failed ({r.returncode}): {' '.join(map(str, cmd))}\n{out[-2000:]}")
    return out


t_all = time.time()
for n in sys.argv[1:]:
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep = d / "edited_predicted"
    (BK / n).mkdir(parents=True, exist_ok=True)
    for f in ("studio_cuts.txt", "edit_points.json", "content_cuts.json"):
        if not (BK / n / f).exists():
            shutil.copy2(d / f, BK / n / f)
    for f in ("timestamps.txt", "description.txt"):
        if not (BK / n / f).exists():
            shutil.copy2(ep / f, BK / n / f)
    if n == "15":
        cuts = "studio_cuts_edited.txt"
    else:
        out = run(["scripts/find_edit_points.py", "--output-dir", d, "--min-silence", "5"], d / "logs_replan5.txt")
        shutil.copy2(d / "studio_cuts.txt", d / "studio_cuts_v3_5s.txt")
        shutil.copy2(d / "content_cuts.json", d / "content_cuts_v3_5s.json")
        cuts = "studio_cuts.txt"
    rm = run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
              "--from-cuts", "raw", "--to-cuts", cuts], d / "logs_remap5.txt")
    v = subprocess.run([sys.executable, str(VERIFY), str(ep / "timestamps.txt"), "--metadata", str(ep / "metadata.json"),
                        "--transcript", str(ep / "transcript.txt"), "--min-gap", "30"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (ep / "verify_report_5s.txt").write_text(v.stdout + v.stderr, encoding="utf-8")
    head = (d / cuts).read_text(encoding="utf-8").splitlines()
    summary = next((l for l in head if l.startswith("# ") and "cuts" in l), "")
    moved = sum(1 for l in rm.splitlines() if "inside" in l.lower())
    print(f"Das {n}: {cuts}: {summary[:110]} | chapters moved out of cuts: {moved} | "
          f"verifier {'valid' if v.returncode == 0 else 'INVALID'} | {time.time() - t0:.0f} s", flush=True)
print(f"all done in {time.time() - t_all:.0f} s")
