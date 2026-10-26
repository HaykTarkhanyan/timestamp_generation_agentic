"""Q52 (2026-10-25, "Keep words and wait, as suggestions"): Դաս 26 0:58:01.6 ('Any ideas?' + 21 s) and Դաս 27
1:01:51.6 ('shall we think about it?' + 10 s). Unticks that content cut, re-runs the 4 s plan, then unticks the
silence cuts inside it too (otherwise the pause rule still cuts the wait) in edit_points.json and rebuilds the
page and studio_cuts.txt from it (--report-only; previews reused); remaps the chapters (--hms) and runs the verifier.
A later full find_edit_points run would re-tick those silences: rerun this. ~3 min for both. Repo root."""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
VERIFY = REPO / ".claude/skills/youtube-timestamps/scripts/verify_timestamps.py"
WAITS = {26: "0:58:01.6", 27: "1:01:51.6"}
NOTE = " [suggestion since 2026-10-25: her thinking invitation and its wait are kept (Q52); the silences inside are unticked too]"


def run(cmd, log):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    log.write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"failed ({r.returncode}): {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-2000:]}")
    return r.stdout + r.stderr


for n, start in WAITS.items():
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    cc = d / "content_cuts.json"
    if cc.read_text(encoding="utf-8") != (d / "content_cuts_v4_4s.json").read_text(encoding="utf-8"):
        raise ValueError(f"Das {n}: content_cuts.json is not the v4_4s plan; stop and look")
    text = cc.read_text(encoding="utf-8")
    cuts = json.loads(text)["cuts"]
    (c,) = [c for c in cuts if c["start"] == start]
    if not c["default"]:
        raise ValueError(f"Das {n} {start}: already unticked")
    # edit the file in place (keeps its one-cut-per-two-lines layout): the cut's default and the end of its reason
    old_head = f'"start": "{start}", "end": "{c["end"]}", "kind": "{c["kind"]}", "default": true'
    old_reason = json.dumps(c["reason"], ensure_ascii=False)
    if text.count(old_head) != 1 or text.count(old_reason) != 1:
        raise ValueError(f"Das {n}: layout not found for {start}")
    text = text.replace(old_head, old_head.replace('"default": true', '"default": false'))
    text = text.replace(old_reason, json.dumps(c["reason"] + NOTE, ensure_ascii=False))
    cc.write_text(text, encoding="utf-8")
    json.loads(cc.read_text(encoding="utf-8"))
    run(["scripts/find_edit_points.py", "--output-dir", d, "--min-silence", "4"], d / "logs_keep_waits.txt")
    ep_path = d / "edit_points.json"
    data = json.loads(ep_path.read_text(encoding="utf-8"))
    (cc_snapped,) = [x for x in data["cuts"] if x["source"] == "content" and x["requested"][0] == start]
    a, b = cc_snapped["start"], cc_snapped["end"]
    inside = [x for x in data["cuts"] if x["source"] == "silence" and x["start"] < b and x["end"] > a]
    for x in inside:
        x["default"] = False
        x["reason"] += " (inside her thinking invitation, kept: Q52)"
    ep_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    run(["scripts/find_edit_points.py", "--output-dir", d, "--report-only"], d / "logs_keep_waits_report.txt")
    run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
         "--from-cuts", "raw", "--to-cuts", "studio_cuts.txt", "--hms"], d / "logs_remap_keep_waits.txt")
    ep = d / "edited_predicted"
    v = subprocess.run([sys.executable, str(VERIFY), str(ep / "timestamps.txt"), "--metadata", str(ep / "metadata.json"),
                        "--transcript", str(ep / "transcript.txt"), "--min-gap", "30"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (ep / "verify_report_4s.txt").write_text(v.stdout + v.stderr, encoding="utf-8")
    head = (d / "studio_cuts.txt").read_text(encoding="utf-8").splitlines()[1]
    starts = ", ".join(f"{x['start']:.1f}" for x in inside)
    print(f"Das {n}: wait {a:.1f}-{b:.1f} s kept, {len(inside)} silence cut(s) inside unticked ({starts}) | {head[2:]} | "
          f"verifier {'valid' if v.returncode == 0 else 'INVALID'} | {time.time() - t0:.0f} s", flush=True)
