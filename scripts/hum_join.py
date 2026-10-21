"""The hum rule (DECISIONS #17): two planned cuts separated only by a short sound with no real caption
word become one cut, so a hum ("ըըը") between two cut pauses goes with them. Arnak's hums are as loud
as speech, so they can't be found by level; the captions tell them apart (a hum has no real word).

    python scripts/hum_join.py --output-dir output/<dir> [--cuts studio_cuts.txt] [--write]
    # ~1 s; then rerun find_edit_points.py (the full analysis, not --report-only) so the joins take effect

Reads the plan's pre-ticked cuts (--cuts, relative to --output-dir) and the .hy.vtt there, and logs
each join. --write adds them to content_cuts.json as safe, pre-ticked content cuts, after copying it to
content_cuts_before_hum_join_<YYYYmmdd-HHMMSS>.json; nothing is deleted. It raises if a join is already
in content_cuts.json (the analysis was not rerun since the last --write).
Until 2026-10-21 this was a throwaway script (Arnak lessons 12, 13 and the 2025 recording).
"""
import argparse
import json
import logging
import re
import shutil
import sys
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/hum_join.log", encoding="utf-8")])
log = logging.getLogger(__name__)

# the hum test, shared with studio.html's timeline: longest hum (lesson 11: 0 conflicts), the filler words
from find_edit_points import FILLER, HUM_MAX_SOUND_S as MAX_SOUND_S, caption_words  # noqa: E402

PAD_S = 0.35        # the pause find_edit_points.py leaves on each side of a cut (its --pad default)
CUT = re.compile(r"Cut\s+\d+\s+(\S+)\s+->\s+(\S+)")


def fmt(t: float) -> str:
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def find_joins(d: Path, cuts_name: str) -> list[tuple[float, float, float]]:
    fps = float(json.loads((d / "edit_points.json").read_text(encoding="utf-8"))["fps"])
    tc = lambda s: (lambda h, m, sec, f: ((h * 60 + m) * 60 + sec) + f / fps)(*map(int, s.split(":")))
    cuts = sorted((tc(m[1]), tc(m[2])) for line in (d / cuts_name).read_text(encoding="utf-8").splitlines()
                  if (m := CUT.match(line)))
    if not cuts:
        raise ValueError(f"no 'Cut N  start  ->  end' lines in {d / cuts_name}")
    vtts = sorted(d.glob("*.hy.vtt"))
    if len(vtts) != 1:
        raise FileNotFoundError(f"expected one .hy.vtt in {d}, found {[v.name for v in vtts]}")
    words = caption_words(vtts[0].read_text(encoding="utf-8"))
    real = lambda a, b: [w for t, w in words if a - 0.2 <= t <= b + 0.2 and w and not FILLER.match(w)]
    joins = []
    for (s0, e0), (s1, e1) in zip(cuts, cuts[1:]):
        sound = (s1 - e0) - 2 * PAD_S          # the gap between the cuts minus the pause each cut leaves
        if 0 < sound < MAX_SOUND_S and not real(e0, s1):
            joins.append((e0 - 0.05, s1 + 0.05, sound))
    log.info(f"{d.name}: {len(cuts)} cuts in {cuts_name}, {len(joins)} hum joins")
    for a, b, snd in joins:
        log.info(f"   join {fmt(a)} - {fmt(b)} (sound {snd:.2f} s)")
    return joins


def write_joins(d: Path, joins: list[tuple[float, float, float]]) -> None:
    cc_file = d / "content_cuts.json"
    cc = json.loads(cc_file.read_text(encoding="utf-8"))
    present = {(c["start"], c["end"]) for c in cc["cuts"]}
    dupes = [(fmt(a), fmt(b)) for a, b, _ in joins if (fmt(a), fmt(b)) in present]
    if dupes:
        raise ValueError(f"already in {cc_file.name}: {dupes}; rerun find_edit_points.py before joining again")
    backup = d / f"content_cuts_before_hum_join_{time.strftime('%Y%m%d-%H%M%S')}.json"
    if backup.exists():
        raise FileExistsError(f"{backup} exists; refusing to overwrite a backup")
    shutil.copy2(cc_file, backup)
    for a, b, snd in joins:
        cc["cuts"].append({"start": fmt(a), "end": fmt(b), "kind": "safe", "default": True,
                           "reason": f"Hum between two cut pauses ({snd:.1f} s of sound, no real caption word): "
                                     "joins them, owner's lesson 11 rule"})
    parse = lambda t: float("inf") if t == "end" else sum(float(p) * 60 ** i for i, p in enumerate(reversed(t.split(":"))))
    cc["cuts"].sort(key=lambda c: parse(c["start"]))
    cc_file.write_text("{\"cuts\": [\n" + ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in cc["cuts"]) + "\n]}\n",
                       encoding="utf-8")
    log.info(f"wrote {len(joins)} joins to {cc_file.name}; backup {backup.name}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--cuts", default="studio_cuts.txt", help="the plan's pre-ticked cuts (default: %(default)s)")
    ap.add_argument("--write", action="store_true", help="add the joins to content_cuts.json (backed up first)")
    a = ap.parse_args()
    t0 = time.time()
    joins = find_joins(a.output_dir, a.cuts)
    if a.write and joins:
        write_joins(a.output_dir, joins)
    log.info(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
