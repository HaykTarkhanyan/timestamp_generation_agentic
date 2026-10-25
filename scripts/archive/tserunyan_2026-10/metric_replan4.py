"""Tserunyan 17-27 re-plan from the user's Դաս 16 edit (DECISIONS #40, the user's Q44-Q50 on 2026-10-25):
silences of 4 s or more pre-ticked; her math/talk content cuts (thinking aloud, false starts, room talk,
tangents) become unticked suggestions; practical cuts and "any questions?" prompts stay ticked; the end cut
of 17 and 18 keeps her "next time" line (22's whole wrap-up cut becomes a suggestion); Դաս 27's goodbyes kept.
Backs up content_cuts.json (content_cuts_v3_5s.json is the plan it came from), runs
find_edit_points.py --min-silence 4 (the existing video previews are reused), keeps *_v4_4s copies, remaps the
nested chapter masters with --hms and runs the verifier. Sequential, ~40 s per lecture. Repo root.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
VERIFY = REPO / ".claude/skills/youtube-timestamps/scripts/verify_timestamps.py"
NOTE = " [suggestion since 2026-10-25: her math or talk, kept by default (Q45)]"

UNTICK = {17: ["1:31:41.5"], 18: ["0:21:05.8", "0:21:38.5"], 19: ["0:15:38.5"], 21: ["1:26:39.0"],
          22: ["0:20:46.9"], 23: ["0:13:47.0", "0:28:20.6", "0:59:46.9"], 24: ["0:52:04.5", "1:26:28.8"],
          26: ["0:42:26.0", "1:00:24.6"]}
KEEP_END = {22: (["1:28:04.5"], " [suggestion since 2026-10-25: holds her 'examples next time ... digest this' line (Q48)]"),
            27: (["1:37:24.0", "1:39:23.45"], " [suggestion since 2026-10-25: the course farewell is kept (Q50)]")}


def edit_17(cuts):
    i = next(k for k, c in enumerate(cuts) if c["start"] == "1:48:43.95")
    c = cuts[i]
    if c["end"] != "1:49:25.0" or not c["default"]:
        raise ValueError("Das 17: end cut not as planned")
    # her next-time line runs on from the chatter with no pause (speech map: sound 1:48:44.1-1:49:03.4), so it
    # cannot be kept alone: the chatter + line become one suggestion, the ticked end cut starts after the line
    a = dict(c, end="1:49:03.9", kind="judgment", default=False,
             reason="End, part 1, unticked since 2026-10-25 (Q48 keeps her next-time line, and no pause separates it): "
                    "'OK, that's it; Aram probably wants to kill me, and my husband too', homework soon, 'just swamped, "
                    "sorry', then the line 'from the Tuesday after next we'll start [topological] spaces' (1:48:59.8-1:49:03.4)")
    b = dict(c, start="1:49:03.9", reason="End, part 2: 'goodbye, any questions?' and the goodbyes, up to the outro")
    cuts[i:i + 1] = [a, b]


def edit_18(cuts):
    c = next(c for c in cuts if c["start"] == "1:24:30.6")
    if c["end"] != "1:25:37.5" or not c["default"]:
        raise ValueError("Das 18: end cut not as planned")
    c["start"] = "1:24:43.4"  # the 1:24:43.2-43.8 gap after "կշարունակենք" (speech map)
    c["reason"] = ("End after her next-time line (kept, Q48: 'I have to run... I wanted to define what first countable "
                   "means, but we'll continue next week'): 'questions on the abstract definitions?', rescheduling the "
                   "next class, goodbyes, up to the outro")


def write_cuts(path, cuts):
    lines = []
    for c in cuts:
        head = ", ".join(f"{json.dumps(k)}: {json.dumps(c[k], ensure_ascii=False)}" for k in ("start", "end", "kind", "default"))
        rest = ", ".join(f"{json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in c.items()
                         if k not in ("start", "end", "kind", "default"))
        lines.append(f"  {{{head},\n   {rest}}}")
    path.write_text('{"cuts": [\n' + ",\n".join(lines) + "\n]}\n", encoding="utf-8")


def run(cmd, log):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    log.write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"failed ({r.returncode}): {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-2000:]}")
    return r.stdout + r.stderr


t_all = time.time()
for n in range(17, 28):
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    cc = d / "content_cuts.json"
    if cc.read_text(encoding="utf-8") != (d / "content_cuts_v3_5s.json").read_text(encoding="utf-8"):
        raise ValueError(f"Das {n}: content_cuts.json is not the v3_5s plan; stop and look")
    shutil.copy2(cc, d / "content_cuts_before_v4.json")
    cuts = json.loads(cc.read_text(encoding="utf-8"))["cuts"]
    for start in UNTICK.get(n, []):
        (c,) = [c for c in cuts if c["start"] == start]
        if not c["default"] or c["kind"] != "judgment":
            raise ValueError(f"Das {n} {start}: expected a ticked judgment cut")
        c["default"], c["reason"] = False, c["reason"] + NOTE
    if n in KEEP_END:
        starts, note = KEEP_END[n]
        for start in starts:
            (c,) = [c for c in cuts if c["start"] == start]
            if not c["default"]:
                raise ValueError(f"Das {n} {start}: already unticked")
            c["default"], c["reason"] = False, c["reason"] + note
    if n == 17:
        edit_17(cuts)
    if n == 18:
        edit_18(cuts)
    write_cuts(cc, cuts)
    json.loads(cc.read_text(encoding="utf-8"))  # still valid JSON
    run(["scripts/find_edit_points.py", "--output-dir", d, "--min-silence", "4"], d / "logs_replan4.txt")
    shutil.copy2(d / "studio_cuts.txt", d / "studio_cuts_v4_4s.txt")
    shutil.copy2(cc, d / "content_cuts_v4_4s.json")
    rm = run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
              "--from-cuts", "raw", "--to-cuts", "studio_cuts.txt", "--hms"], d / "logs_remap4.txt")
    ep = d / "edited_predicted"
    v = subprocess.run([sys.executable, str(VERIFY), str(ep / "timestamps.txt"), "--metadata", str(ep / "metadata.json"),
                        "--transcript", str(ep / "transcript.txt"), "--min-gap", "30"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (ep / "verify_report_4s.txt").write_text(v.stdout + v.stderr, encoding="utf-8")
    head = (d / "studio_cuts.txt").read_text(encoding="utf-8").splitlines()[1]
    moved = sum(1 for l in rm.splitlines() if "moved to the end of cut" in l)
    preview = "video preview" if "plays the video preview" in (d / "logs_replan4.txt").read_text(encoding="utf-8") else "NO VIDEO"
    print(f"Das {n}: {head[2:]} | chapters moved out of cuts: {moved} | verifier "
          f"{'valid' if v.returncode == 0 else 'INVALID'} | {preview} | {time.time() - t0:.0f} s", flush=True)
print(f"all done in {time.time() - t_all:.0f} s", flush=True)
