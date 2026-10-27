"""Push the Q84/Q85 term fix (2026-10-27): Դաս 16, 17 title + description + thumbnail, Դաս 19 description only.
metric_readback.py after each; stops at the first failure or DIFF. Visibility untouched. ~10 s per lecture.
Based on scripts/archive/tserunyan_2026-10/metric_push.py."""
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
PUB = ["scripts/yt_publish.py", "--channel", "umath"]


def run(cmd):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    out = "\n".join(l for l in (r.stdout + r.stderr).splitlines() if "Warning" not in l and "warnings.warn" not in l)
    if r.returncode:
        raise RuntimeError(f"exit {r.returncode}: {' '.join(map(str, cmd))}\n{out[-1500:]}")
    return out


t_all = time.time()
for n in (16, 17, 19):
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    vid = d.name.split("_", 2)[2]
    ed = d / "edited"
    if n != 19:
        run([*PUB, "set-title", vid, ed / "titles.txt"])
    run([*PUB, "set-description", vid, ed / "description.txt"])
    if n != 19:
        run([*PUB, "set-thumbnail", vid, REPO / "thumbnails" / "umath" / f"metric_{n}.png"])
    back = run(["scripts/non_essential/metric_readback.py", vid])
    if "DIFF" in back:
        raise RuntimeError(f"Das {n}: readback DIFF\n{back[-1500:]}")
    summary = " | ".join(l.split(" INFO ", 1)[-1] for l in back.splitlines() if " INFO " in l)
    print(f"{time.strftime('%H:%M:%S')} Das {n} {vid}: {summary} | {time.time() - t0:.0f} s", flush=True)
print(f"all 3 pushed and read back in {time.time() - t_all:.0f} s", flush=True)
