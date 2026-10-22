"""Cut-list tools for the Studio step, between the user's review on studio.html and the cuts in Studio.

  check     the list the user pasted from studio.html (studio_cuts_edited.txt) against the plan it
            came from (edit_points.json): every planned cut accounted for once (unchanged, CHANGED,
            or REMOVED), numbering, lengths, gaps and overlaps, cuts too short to mean anything
  to-enter  studio_cuts_edited.txt -> studio_cuts_to_enter.txt: drop cuts under MIN_CUT_S (shrunk
            to nothing on a page without a delete button), merge cuts that overlap or leave at most
            one frame between them, optionally end the last cut on Studio's own End trim marker,
            renumber by start; then verify frame by frame that it removes what the paste removes
  entry-js  studio_cuts_to_enter.txt -> .playwright-mcp/studio_entry_<id>_NNofMM.js, batches of the entry
            loop in scripts/studio_enter_cuts.js (plus _dryrun.js, read-only), for the Playwright MCP's
            browser_run_code_unsafe(filename=...) in the signed-in Studio tab
  diff      the cuts in Studio (trim markers saved from Playwright) against studio_cuts_to_enter.txt

    python scripts/cut_list.py check    --output-dir output/<dir>
    python scripts/cut_list.py to-enter --output-dir output/<dir> [--studio-end 1:38:59:15]
    python scripts/cut_list.py entry-js --output-dir output/<dir> [--batch-size 14]
    python scripts/cut_list.py diff     --output-dir output/<dir> --markers .playwright-mcp/<name>.json
    # each ~1 s; exits 1 on any problem

Times are Studio's H:MM:SS:FF at the frame rate in edit_points.json; a cut covers frames [start, end).
Saving the markers: browser_evaluate of the [aria-label^="Start trim marker"], [aria-label^="End trim
marker"] labels with filename=.playwright-mcp/<name>.json (a list, or {"markers": [...]}).
Until 2026-10-17 these lived as throwaway scripts (ML50-ML52).
"""
import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/cut_list.log", encoding="utf-8")])
log = logging.getLogger(__name__)

MIN_CUT_S = 0.5
EDITED, TO_ENTER = "studio_cuts_edited.txt", "studio_cuts_to_enter.txt"
REPO = Path(__file__).resolve().parent.parent
ENTRY_TEMPLATE, ENTRY_DIR = REPO / "scripts" / "studio_enter_cuts.js", REPO / ".playwright-mcp"
CUT = re.compile(r"Cut\s+(\d+)\s+(\S+)\s+->\s+(\S+)\s+\(([\d.]+) s\)\s*(.*)$")
REMOVED = re.compile(r"# REMOVED, was (\S+) -> (\S+)$")


class Frames:
    def __init__(self, fps: float):
        if fps != int(fps):
            raise NotImplementedError(f"{fps} fps: Studio frame numbering for fractional rates is unverified")
        self.fps = int(fps)

    def __call__(self, tc: str) -> int:
        h, m, s, f = map(int, tc.split(":"))
        if f >= self.fps:
            raise ValueError(f"{tc}: frame {f} at {self.fps} fps")
        return ((h * 60 + m) * 60 + s) * self.fps + f

    def tc(self, n: int) -> str:
        fps = self.fps
        return f"{n // (3600 * fps)}:{n // (60 * fps) % 60:02d}:{n // fps % 60:02d}:{n % fps:02d}"

    def hms(self, n: int) -> str:
        s = round(n / self.fps)
        return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"


def load(d: Path):
    data = json.loads((d / "edit_points.json").read_text(encoding="utf-8"))
    return data, Frames(float(data["fps"]))


def read_cuts(path: Path, fr: Frames) -> list[tuple[int, int, int, str]]:
    """(n, start frame, end frame, note) of every 'Cut N ...' line."""
    if not path.exists():
        raise FileNotFoundError(path)
    cuts = [(int(m[1]), fr(m[2]), fr(m[3]), m[5].strip())
            for line in path.read_text(encoding="utf-8").splitlines() if (m := CUT.match(line))]
    if not cuts:
        raise ValueError(f"no 'Cut N  start  ->  end  (d s)' lines in {path}")
    return cuts


def check(d: Path) -> int:
    data, fr = load(d)
    plan = [(fr(c["start_tc"]), fr(c["end_tc"])) for c in data["studio_cuts"]]
    used = {p: 0 for p in plan}
    problems, notes, kinds = [], [], {"unchanged": 0, "changed": 0, "new": 0, "removed": 0}

    def account(pair, where):
        if pair not in used:
            problems.append(f"{where}: {fr.tc(pair[0])} -> {fr.tc(pair[1])} is not a planned cut "
                            "(a list from an older studio.html tab?)")
        else:
            used[pair] += 1

    cuts = []
    for line in (d / EDITED).read_text(encoding="utf-8").splitlines():
        if rm := REMOVED.match(line):
            kinds["removed"] += 1
            account((fr(rm[1]), fr(rm[2])), "REMOVED")
            continue
        m = CUT.match(line)
        if not m:
            continue
        n, s, e, page_len, note = int(m[1]), fr(m[2]), fr(m[3]), float(m[4]), m[5].strip()
        cuts.append((s, e, n))
        if e <= s:
            problems.append(f"Cut {n} ends before it starts")
        if abs((e - s) / fr.fps - page_len) > 0.005:
            problems.append(f"Cut {n}: {m[2]} -> {m[3]} is {(e - s) / fr.fps:.2f} s, the line says {page_len:.2f} s")
        if not note:
            kinds["unchanged"] += 1
            account((s, e), f"Cut {n} (unchanged)")
        elif w := re.match(r"CHANGED, was (\S+) -> (\S+)$", note):
            kinds["changed"] += 1
            account((fr(w[1]), fr(w[2])), f"Cut {n} (was)")
        elif note == "NEW":
            kinds["new"] += 1
        else:
            problems.append(f"Cut {n}: unknown note {note!r}")
    cuts.sort()
    missing = [p for p, k in used.items() if k == 0]
    twice = [p for p, k in used.items() if k > 1]
    problems += [f"planned cut {fr.tc(s)} -> {fr.tc(e)} is in the paste {'twice' if p in twice else 'nowhere'}"
                 for p in missing + twice for s, e in [p]]
    if [n for _, _, n in cuts] != list(range(1, len(cuts) + 1)):
        problems.append("the Cut numbers do not follow Studio's order (1..N by start)")
    for (s0, e0, n0), (s1, e1, n1) in zip(cuts, cuts[1:]):
        gap = s1 - e0
        if gap < 0:
            notes.append(f"Cut {n0} and Cut {n1} overlap by {-gap} frame(s): to-enter merges them" if gap >= -1 * fr.fps
                         else f"Cut {n0} and Cut {n1} overlap by {-gap / fr.fps:.2f} s")
        elif gap <= 1:
            notes.append(f"Cut {n0} -> Cut {n1}: {gap} frame(s) between them: to-enter merges them")
    tiny = [n for s, e, n in cuts if (e - s) / fr.fps < MIN_CUT_S]
    if tiny:
        notes.append(f"cuts under {MIN_CUT_S} s (shrunk to nothing; to-enter drops them): {tiny}")
    end = round(data["duration"] * fr.fps)
    removed, last = 0, -1
    for s, e, _ in cuts:                                         # union, so overlaps count once
        removed += max(0, e - max(s, last)); last = max(last, e)
    log.info(f"{len(cuts)} cuts in the paste ({', '.join(f'{v} {k}' for k, v in kinds.items())}); "
             f"planned cuts accounted for: {len(plan) - len(missing)} of {len(plan)}")
    log.info(f"removes {removed / fr.fps / 60:.1f} min: {fr.hms(end)} -> {fr.hms(end - removed)}")
    for n in notes:
        log.info(f"note: {n}")
    for p in problems:
        log.error(p)
    log.info("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def to_enter(d: Path, studio_end: str | None) -> int:
    data, fr = load(d)
    paste = read_cuts(d / EDITED, fr)
    keep = sorted((s, e, [n]) for n, s, e, _ in paste if (e - s) / fr.fps >= MIN_CUT_S)
    dropped = [(n, (e - s) / fr.fps) for n, s, e, _ in paste if (e - s) / fr.fps < MIN_CUT_S]
    merged = []
    for s, e, ns in keep:
        if merged and s - merged[-1][1] <= 1:
            ps, pe, pns = merged[-1]
            merged[-1] = (ps, max(pe, e), pns + ns)
        else:
            merged.append((s, e, ns))
    extended = 0
    if studio_end:
        se = fr(studio_end)
        s, e, ns = merged[-1]
        if abs(se - e) > 2:
            raise ValueError(f"the last cut ends at {fr.tc(e)}, {abs(se - e)} frames from Studio's end {studio_end}: "
                             "not the end trim, check the list")
        extended = se - e
        merged[-1] = (s, se, ns)
    header = [f"# From {EDITED}: {len(paste)} cuts -> {len(merged)}"]
    if dropped:
        header.append(f"# dropped (under {MIN_CUT_S} s): " + ", ".join(f"Cut {n} ({t:.2f} s)" for n, t in dropped))
    if any(len(ns) > 1 for _, _, ns in merged):
        header.append("# merged (overlapping or <= 1 frame apart): " + ", ".join("+".join(map(str, ns)) for _, _, ns in merged if len(ns) > 1))
    if studio_end:
        header.append(f"# last cut ends on Studio's End trim marker {studio_end} ({extended:+d} frame(s))")
    header.append("# Numbered as in Studio (by start), listed last first.")
    lines = [f"Cut {i:>2}   {fr.tc(s)}  ->  {fr.tc(e)}   ({(e - s) / fr.fps:.2f} s)"
             for i, (s, e, _) in reversed(list(enumerate(merged, 1)))]
    (d / TO_ENTER).write_text("\n".join(header + lines) + "\n", encoding="utf-8")
    # frame-level check against the paste
    frames = lambda cuts: set().union(*(range(s, e) for s, e in cuts))
    f_paste = frames((s, e) for _, s, e, _ in paste)
    f_enter = frames((s, e) for s, e, _ in merged)
    f_tiny = frames((s, e) for n, s, e, _ in paste if (e - s) / fr.fps < MIN_CUT_S)
    only_paste, only_enter = f_paste - f_enter, sorted(f_enter - f_paste)
    edges = {s for _, s, _, _ in paste} | {e for _, _, e, _ in paste} | ({fr(studio_end)} if studio_end else set())
    problems = []
    if not only_paste <= f_tiny:
        problems.append(f"{len(only_paste - f_tiny)} frame(s) cut in the paste are missing from the entry list")
    if len(only_enter) > sum(len(ns) - 1 for _, _, ns in merged) + max(extended, 0):
        problems.append(f"the entry list cuts {len(only_enter)} frame(s) the paste keeps: {[fr.tc(f) for f in only_enter][:10]}")
    if not all(s in edges and e in edges for s, e, _ in merged):
        problems.append("an entry edge is not an edge of the paste")
    removed = len(f_enter)
    end = round(data["duration"] * fr.fps)
    log.info(f"wrote {d / TO_ENTER}: {len(merged)} cuts, removing {removed / fr.fps / 60:.1f} min -> {fr.hms(end - removed)}")
    for h in header[1:-1]:
        log.info(h[2:])
    log.info(f"frames: paste {len(f_paste)}, entry {len(f_enter)}; only in the paste {len(only_paste)} "
             f"(all from dropped cuts: {only_paste <= f_tiny}); only in the entry list: {[fr.tc(f) for f in only_enter]}")
    print(json.dumps([[i, fr.tc(s), fr.tc(e)] for i, (s, e, _) in enumerate(merged, 1)]))   # for the Playwright loop
    for p in problems:
        log.error(p)
    log.info("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def entry_js(d: Path, batch_size: int, type_shift: int = 0) -> int:
    data, fr = load(d)
    cuts = sorted((s, e) for _, s, e, _ in read_cuts(d / TO_ENTER, fr))
    template = ENTRY_TEMPLATE.read_text(encoding="utf-8")
    if template.count("__JOB__") != 1:
        raise ValueError(f"{ENTRY_TEMPLATE}: expected exactly one __JOB__ placeholder")
    rows = [[i, fr.tc(s), fr.tc(e)] for i, (s, e) in enumerate(cuts, 1)]
    batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
    vid, over = data["video_id"], data["duration"] >= 3600   # Studio drops the hour field under an hour
    ENTRY_DIR.mkdir(exist_ok=True)
    jobs = [("dryrun", 0, rows, True)] + [(f"{k:02d}of{len(batches):02d}", k, b, False) for k, b in enumerate(batches, 1)]
    for tag, k, b, dry in jobs:
        job = {"video": vid, "overOneHour": over, "batch": k, "batches": len(batches), "dryRun": dry,
               "fps": fr.fps, "typeShift": type_shift, "cuts": b}
        path = ENTRY_DIR / f"studio_entry_{vid}_{tag}.js"
        path.write_text(template.replace("__JOB__", json.dumps(job)), encoding="utf-8")
        log.info(f"{path}: {'dry run, ' if dry else ''}cuts {b[0][0]}-{b[-1][0]}")
    log.info(f"{len(rows)} cuts from {d / TO_ENTER} in {len(batches)} batches of up to {batch_size} "
             f"(~{6 * batch_size} s each at ~6 s per cut); over an hour: {over}; typed times shifted by "
             f"{type_shift} frame(s)")
    return 0


def diff(d: Path, markers: Path) -> int:
    _, fr = load(d)
    text = markers.read_text(encoding="utf-8")
    obj = json.loads(text[min(i for i in (text.find("["), text.find("{")) if i >= 0):])
    labels = obj["markers"] if isinstance(obj, dict) else obj
    vals = [lab.split("marker ")[1] for lab in labels]
    vals = [v if v.count(":") == 3 else f"0:{v}" for v in vals]   # Studio's MM:SS:FF on videos under an hour
    if len(vals) % 2:
        raise ValueError(f"{markers}: {len(vals)} trim markers, expected start/end pairs")
    pairs = [(fr(a), fr(b)) for a, b in zip(vals[0::2], vals[1::2])]
    whole, studio = pairs[0], sorted(pairs[1:])
    want = sorted((s, e) for _, s, e, _ in read_cuts(d / TO_ENTER, fr))
    only_studio = [p for p in studio if p not in want]
    only_list = [p for p in want if p not in studio]
    log.info(f"whole video {fr.tc(whole[0])} - {fr.tc(whole[1])} | Studio {len(studio)} cuts | list {len(want)} cuts")
    for s, e in only_studio:
        log.error(f"only in Studio: {fr.tc(s)} -> {fr.tc(e)}")
    for s, e in only_list:
        log.error(f"only in the list: {fr.tc(s)} -> {fr.tc(e)}")
    if want and want[-1][1] != whole[1]:
        log.info(f"note: the last cut ends at {fr.tc(want[-1][1])}, the end trim is {fr.tc(whole[1])}")
    ok = not only_studio and not only_list
    log.info("OK, identical frame for frame" if ok else "MISMATCH")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("check", "to-enter", "entry-js", "diff"):
        p = sub.add_parser(name)
        p.add_argument("--output-dir", type=Path, required=True)
        if name == "to-enter":
            p.add_argument("--studio-end", help="Studio's End trim marker, if the last cut must end on it")
        if name == "entry-js":
            p.add_argument("--batch-size", type=int, default=14, help="cuts per batch (~6 s each; stay under ~100 s)")
            p.add_argument("--type-shift", type=int, default=0,
                           help="frames added to every typed time; -1 for an upload on which Studio stores each cut "
                                "one frame later than typed (Papikian Դաս 20); cuts are still checked at the planned times")
        if name == "diff":
            p.add_argument("--markers", type=Path, required=True)
    a = ap.parse_args()
    t0 = time.time()
    code = (check(a.output_dir) if a.cmd == "check" else
            to_enter(a.output_dir, a.studio_end) if a.cmd == "to-enter" else
            entry_js(a.output_dir, a.batch_size, a.type_shift) if a.cmd == "entry-js" else diff(a.output_dir, a.markers))
    log.info(f"done in {time.time() - t0:.1f} s")
    sys.exit(code)


if __name__ == "__main__":
    main()
