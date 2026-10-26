"""Tserunyan 19-27: pauses only from 7 s (the user, 2026-10-26, after reviewing Դաս 18: "too much work ... i'm okay
with waiting for her to type, that can be only cut if its super long", Q58 "7s"). Content cuts unchanged
(DECISIONS #40, Q52). Per lecture: find_edit_points.py --min-silence 7 (previews reused); for 26 and 27 the silence
cuts inside her kept thinking waits are unticked again (Q52) and the page rebuilt with --report-only; *_v5_7s
copies; chapters remapped (--hms); verifier. Sequential, ~1-2 min per lecture. Repo root."""
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
for n in range(19, 28):
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    cuts = json.loads((d / "content_cuts.json").read_text(encoding="utf-8"))["cuts"]
    v4 = json.loads((d / "content_cuts_v4_4s.json").read_text(encoding="utf-8"))["cuts"]
    diff = [(a["start"], a["default"], b["default"]) for a, b in zip(cuts, v4) if a != b]
    expected = [(WAITS[n], False, True)] if n in WAITS else []
    if len(cuts) != len(v4) or diff != expected:
        raise ValueError(f"Das {n}: content cuts differ from the v4 plan beyond Q52: {diff}")
    run(["scripts/find_edit_points.py", "--output-dir", d, "--min-silence", "7"], d / "logs_replan7.txt")
    note = ""
    if n in WAITS:
        ep_path = d / "edit_points.json"
        data = json.loads(ep_path.read_text(encoding="utf-8"))
        (w,) = [c for c in data["cuts"] if c["source"] == "content" and c["requested"][0] == WAITS[n]]
        inside = [c for c in data["cuts"] if c["source"] == "silence" and c["start"] < w["end"] and c["end"] > w["start"]]
        for c in inside:
            c["default"] = False
            c["reason"] += " (inside her thinking invitation, kept: Q52)"
        ep_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        run(["scripts/find_edit_points.py", "--output-dir", d, "--report-only"], d / "logs_replan7_report.txt")
        note = f" | Q52: {len(inside)} silence(s) inside the wait unticked"
    shutil.copy2(d / "studio_cuts.txt", d / "studio_cuts_v5_7s.txt")
    run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
         "--from-cuts", "raw", "--to-cuts", "studio_cuts.txt", "--hms"], d / "logs_remap7.txt")
    ep = d / "edited_predicted"
    v = subprocess.run([sys.executable, str(VERIFY), str(ep / "timestamps.txt"), "--metadata", str(ep / "metadata.json"),
                        "--transcript", str(ep / "transcript.txt"), "--min-gap", "30"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (ep / "verify_report_7s.txt").write_text(v.stdout + v.stderr, encoding="utf-8")
    head = (d / "studio_cuts.txt").read_text(encoding="utf-8").splitlines()[1]
    cards = (d / "edit_review" / "studio.html").read_text(encoding="utf-8").count('class="cut"')
    print(f"{time.strftime('%H:%M')} Das {n}: {head[2:]} | {cards} cards | verifier "
          f"{'valid' if v.returncode == 0 else 'INVALID'}{note} | {time.time() - t0:.0f} s", flush=True)
print(f"all done in {time.time() - t_all:.0f} s", flush=True)
