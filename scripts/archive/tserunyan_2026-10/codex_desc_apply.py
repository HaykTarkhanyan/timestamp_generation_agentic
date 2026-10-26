"""Apply the taken findings of _knowledge/tserunyan_metric/codex_desc_review_2026-10-26.json: replace each label once in
the chapter master (edited_predicted/timestamps_raw.txt) and its flat copy (plus edited/timestamps_flat.txt where it
exists), then regenerate: remap --hms, and where the edited captions exist snap --hms, verifier, metric_assemble,
glossary. Proves that only the labels changed (same times, same line count). Backups in scratchpad
before_codex_desc/. ~5 s per lecture. Repo root."""
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
SK = REPO / ".claude/skills/youtube-timestamps/scripts"
BACK = Path(__file__).parent / "before_codex_desc"
review = json.loads((REPO / "_knowledge/tserunyan_metric/codex_desc_review_2026-10-26.json").read_text(encoding="utf-8"))
todo = defaultdict(list)
for f in review["findings"]:
    if f["verdict"].startswith("take"):
        todo[f["n"]].append((f["label"], f["new"]))


def run(cmd, ok=(0,)):
    r = subprocess.run([sys.executable, *map(str, cmd)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode not in ok:
        raise RuntimeError(f"exit {r.returncode}: {' '.join(map(str, cmd))}\n{(r.stdout + r.stderr)[-1500:]}")
    return r.returncode, r.stdout + r.stderr


def lines(p):
    return [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


for n, changes in sorted(todo.items()):
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ep, ed = d / "edited_predicted", d / "edited"
    final = (ed / "description.txt").exists()
    outs = [ep / "timestamps.txt", ep / "description.txt"] + ([ed / "timestamps.txt", ed / "description.txt"] if final else [])
    (BACK / str(n)).mkdir(parents=True, exist_ok=True)
    before = {}
    for p in outs + [ep / "timestamps_raw.txt", ep / "timestamps_raw_flat.txt"] + ([ed / "timestamps_flat.txt"] if (ed / "timestamps_flat.txt").exists() else []):
        shutil.copy2(p, BACK / str(n) / f"{p.parent.name}__{p.name}")
        before[p] = lines(p)
    for p in [ep / "timestamps_raw.txt", ep / "timestamps_raw_flat.txt"] + ([ed / "timestamps_flat.txt"] if (ed / "timestamps_flat.txt").exists() else []):
        text = p.read_text(encoding="utf-8")
        for old, new in changes:
            hits = sum(1 for l in text.splitlines() if l.strip().split(" ", 1)[-1] == old)
            if hits != 1:
                raise ValueError(f"Das {n} {p.name}: label found {hits} times: {old}")
            text = "\n".join((l.replace(old, new) if l.strip().split(" ", 1)[-1] == old else l) for l in text.split("\n"))
        p.write_text(text, encoding="utf-8")
    run(["scripts/remap_chapters.py", "--output-dir", d, "--from", "edited_predicted/timestamps_raw.txt",
         "--from-cuts", "raw", "--to-cuts", "studio_cuts_to_enter.txt", "--hms"])
    if final:
        run(["scripts/non_essential/snap_chapters_to_captions.py", d, "--hms"])
        code, ver = run([SK / "verify_timestamps.py", ed / "timestamps.txt", "--metadata", ed / "metadata.json",
                         "--transcript", ed / "transcript.txt", "--min-gap", "30"], ok=(0, 1))
        (ed / "verify_report_final.txt").write_text(ver, encoding="utf-8")
        if code:
            raise RuntimeError(f"Das {n}: verifier INVALID")
        run(["scripts/non_essential/metric_assemble.py", n])
        gcode, glo = run([SK / "glossary_check.py", ed / "timestamps.txt", ed / "description.txt"], ok=(0, 1))
        if gcode:
            raise RuntimeError(f"Das {n}: glossary DENY\n{glo[-800:]}")
    # only the changed labels may differ
    news = {new for _, new in changes}
    for p in outs:
        a, b = before[p], lines(p)
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        if len(a) != len(b) or len(diff) != len(changes) or any(y.strip().split(" ", 1)[-1] not in news or
                                                                 x.strip().split(" ", 1)[0] != y.strip().split(" ", 1)[0]
                                                                 for x, y in diff):
            raise ValueError(f"Das {n} {p}: unexpected changes {diff[:4]} ({len(a)} -> {len(b)} lines)")
    print(f"Das {n}: {len(changes)} label(s) changed in {len(outs)} files, times unchanged"
          f"{', verifier valid, glossary clean' if final else ' (draft: no edited captions yet)'}", flush=True)
