"""Tserunyan 22-27: content cuts only, no pause cuts at all (the user, 2026-10-26, with the Դաս 21 list: "new plan no
more waiting to write cuts for the rest of the videos in this playlist only. im fed up with them now. just content
related staff pls, update the next htmls"). Content cuts unchanged (DECISIONS #40, Q52). Per lecture:
find_edit_points.py --min-silence 100000 (no silence is that long, so no pause cuts; previews reused),
*_v6_content copies, chapters remapped (--hms), verifier. Sequential, ~30-60 s per lecture. Repo root."""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
VERIFY = REPO / ".claude/skills/youtube-timestamps/scripts/verify_timestamps.py"
WAITS = {26: "0:58:01.6", 27: "1:01:51.6"}


def run(cmd, log):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    log.write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"failed ({r.returncode}): {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-2000:]}")


t_all = time.time()
for n in range(22, 28):
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    cuts = json.loads((d / "content_cuts.json").read_text(encoding="utf-8"))["cuts"]
    v4 = json.loads((d / "content_cuts_v4_4s.json").read_text(encoding="utf-8"))["cuts"]
    diff = [(a["start"], a["default"], b["default"]) for a, b in zip(cuts, v4) if a != b]
    expected = [(WAITS[n], False, True)] if n in WAITS else []
    if len(cuts) != len(v4) or diff != expected:
        raise ValueError(f"Das {n}: content cuts differ from the v4 plan beyond Q52: {diff}")
    run(["scripts/find_edit_points.py", "--output-dir", d, "--min-silence", "100000"], d / "logs_content_only.txt")
    data = json.loads((d / "edit_points.json").read_text(encoding="utf-8"))
    if any(c["source"] == "silence" for c in data["cuts"]):
        raise ValueError(f"Das {n}: silence cuts left in the plan")
    shutil.copy2(d / "studio_cuts.txt", d / "studio_cuts_v6_content.txt")
    run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
         "--from-cuts", "raw", "--to-cuts", "studio_cuts.txt", "--hms"], d / "logs_remap_content.txt")
    ep = d / "edited_predicted"
    v = subprocess.run([sys.executable, str(VERIFY), str(ep / "timestamps.txt"), "--metadata", str(ep / "metadata.json"),
                        "--transcript", str(ep / "transcript.txt"), "--min-gap", "30"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (ep / "verify_report_content.txt").write_text(v.stdout + v.stderr, encoding="utf-8")
    head = (d / "studio_cuts.txt").read_text(encoding="utf-8").splitlines()[1]
    sugg = sum(1 for c in data["cuts"] if not c["default"])
    print(f"{time.strftime('%H:%M')} Das {n}: {head[2:]} | {sugg} unticked suggestions | verifier "
          f"{'valid' if v.returncode == 0 else 'INVALID'} | {time.time() - t0:.0f} s", flush=True)
print(f"all done in {time.time() - t_all:.0f} s", flush=True)
