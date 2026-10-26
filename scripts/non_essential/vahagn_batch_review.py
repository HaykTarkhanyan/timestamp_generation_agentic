"""Review several Vahagn pieces on ONE studio.html and download ONE cut list (the user, 2026-10-25: "since here
the vids are short i dont want to do one by one and keep on downloading many txts").

    python scripts/non_essential/vahagn_batch_review.py plan                       # batches by lecture day
    python scripts/non_essential/vahagn_batch_review.py build b0504 22.1 22.2 22.3 23.1.a
    python scripts/non_essential/vahagn_batch_review.py split b0504 [--file <downloaded list>]

build: joins the pieces' analysis WAVs, 360p previews (stream copy), transcripts and captions onto one timeline
(each piece starts on a whole frame), shifts every piece's own planned cuts onto it unchanged, and builds the page
with find_edit_points --report-only in output/vahagn_<name>/. Each piece's analysis audio is scaled so its noise
floor lands on the batch's lowest one, so the page's one silence threshold means each piece's own threshold
(floor + margin); the sound you hear comes from the previews, untouched. ~1-2 min per batch.

split: reads the batch list (output/vahagn_<name>/studio_cuts_edited.txt, or --file) and writes each piece's own
studio_cuts_edited.txt in studio.html's format (Studio numbering, CHANGED / NEW / REMOVED against that piece's
plan), splitting any cut that crosses a boundary; then per piece cut_list.py check + to-enter, and
vahagn_build_drafts.py + vahagn_review_page.py. Times within one frame of a planned cut count as that cut (the
batch rounds the shifted times again). An existing studio_cuts_edited.txt is kept as studio_cuts_edited.before_<time>.txt.
"""
import argparse
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import cut_list  # noqa: E402

SR = 16000
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_batch_review.log", encoding="utf-8")])
log = logging.getLogger(__name__)
TIME = re.compile(r"\d\d:\d\d:\d\d\.\d\d\d")
FLAG_T = re.compile(r"at (\d+:\d\d:\d\d(?:\.\d)?)")


def piece_dirs() -> dict:
    uploads = json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))
    return {u["section"]: next(iter(REPO.glob(f"output/*_{u['id']}"))) for u in uploads}


def hms(t: float, decimals: int = 0) -> str:
    """H:MM:SS (whole seconds floored, as the transcripts have them) or H:MM:SS.s"""
    if decimals == 0:
        t = int(t)
        return f"{t // 3600}:{t // 60 % 60:02d}:{t % 60:02d}"
    h, rem = divmod(round(t, decimals), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:0{3 + decimals}.{decimals}f}"


def shift_vtt_time(t: str, off: float) -> str:
    h, m, s = t.split(":")
    v = int(h) * 3600 + int(m) * 60 + float(s) + off
    h, rem = divmod(v, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def sync_lag(proxy: Path, x: np.ndarray, t: float, win: float = 20.0, maxlag: float = 0.5) -> float:
    """Seconds the preview's sound is late against the analysis audio x around t (1 ms steps). Both high-passed at
    150 Hz, since the hum pieces' analysis audio is (vahagn_plan_queue.py --highpass)."""
    a = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t - maxlag:.3f}", "-t", f"{win + 2 * maxlag:.3f}", "-i",
                        str(proxy), "-vn", "-af", "highpass=f=150", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True).stdout
    p = np.frombuffer(a, np.float32)
    w = x[int(t * SR):int((t + win) * SR)]
    w = w - np.convolve(w, np.ones(53) / 53, mode="same")   # crude 300 Hz high-pass, enough to drop any hum
    best, lag = -1.0, 0.0
    for k in range(0, len(p) - len(w), 16):
        seg = p[k:k + len(w)]
        c = float(np.dot(seg, w) / (np.linalg.norm(seg) * np.linalg.norm(w) + 1e-12))
        if c > best:
            best, lag = c, k / SR - maxlag
    if best < 0.5:
        raise ValueError(f"sync check at {t:.0f} s: best correlation only {best:.2f}, can't tell the lag")
    return lag


def cmd_plan() -> None:
    pieces = json.loads((REPO / "_knowledge/vahagn_linalg/pieces.json").read_text(encoding="utf-8"))["pieces"]
    dirs = piece_dirs()
    by_date: dict[str, list] = {}
    for p in pieces:
        by_date.setdefault(p["date"], []).append(p["section"])
    for date, secs in by_date.items():
        mins = sum(json.loads((dirs[s] / "edit_points.json").read_text(encoding="utf-8"))["duration"] for s in secs) / 60
        done = [s for s in secs if (dirs[s] / "studio_cuts_to_enter.txt").exists()]
        log.info(f"{date:18s} {' '.join(secs):32s} {mins:5.1f} min" + (f"   reviewed: {' '.join(done)}" if done else ""))


def cmd_build(name: str, secs: list[str]) -> None:
    t0 = time.time()
    dirs = piece_dirs()
    pieces = {p["section"]: p for p in
              json.loads((REPO / "_knowledge/vahagn_linalg/pieces.json").read_text(encoding="utf-8"))["pieces"]}
    out = REPO / "output" / f"vahagn_{name}"
    bid = f"vahagn_{name}"
    (out / "audio").mkdir(parents=True, exist_ok=True)
    (out / "video").mkdir(exist_ok=True)
    datas = [json.loads((dirs[s] / "edit_points.json").read_text(encoding="utf-8")) for s in secs]
    fps = {d["fps"] for d in datas}
    if len(fps) != 1:
        raise ValueError(f"mixed frame rates {fps}")
    fps = int(fps.pop())
    margins = {round(d["params"]["threshold_db"] - d["params"]["floor_db"], 3) for d in datas}
    if len(margins) != 1:
        raise ValueError(f"pieces use different silence margins {margins}: one page threshold can't serve them")
    margin = margins.pop()
    floor = min(d["params"]["floor_db"] for d in datas)
    frames = [round(d["duration"] * fps) for d in datas]
    offs = [sum(frames[:i]) for i in range(len(frames))]
    total = sum(frames) / fps

    # audio: each piece on its frame-exact slot, scaled so its floor sits on the batch floor (all gains <= 0)
    x = np.zeros(round(total * SR), dtype=np.float32)
    for s, d, o, n in zip(secs, datas, offs, frames):
        y, sr = sf.read(dirs[s] / "audio" / f"{d['video_id']}_16k.wav", dtype="float32")
        if sr != SR:
            raise ValueError(f"{s}: {sr} Hz")
        a, length = round(o / fps * SR), round(n / fps * SR)
        y = y[:length] * 10 ** ((floor - d["params"]["floor_db"]) / 20)
        x[a:a + len(y)] = y
    wav = out / "audio" / f"{bid}_16k.wav"
    sf.write(wav, x, SR)
    wav.with_suffix(".source.txt").write_text(str(wav.resolve()), encoding="utf-8")

    # video: the previews' pictures joined without re-encoding ('duration' fixes where the next piece starts);
    # their sound decoded, fitted to each slot and encoded once. Joining the sound by stream copy put it 32 ms late
    # everywhere (b0504; a piece's own preview: 0 ms): AAC's 1024-sample start-up delay at the previews' 32 kHz,
    # which each file's own header skips and the join loses.
    probes, proxies = set(), []
    lst = out / "video" / "concat.txt"
    lines = []
    for s, d, n in zip(secs, datas, frames):
        p = dirs[s] / "video" / f"{d['video_id']}_360p.mp4"
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,"
                            "sample_rate,channels", "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
        probes.add(r.stdout.strip())
        proxies.append(p)
        lines += [f"file '{p.as_posix()}'", f"outpoint {n / fps:.3f}", f"duration {n / fps:.3f}"]
    if len(probes) != 1:
        raise ValueError(f"previews differ, can't join their pictures without re-encoding: {probes}")
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    pictures = out / "video" / "pictures.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-map", "0:v",
                    "-c", "copy", str(pictures)], check=True)
    fit = ";".join(f"[{k + 1}:a]atrim=0:{n / fps:.6f},apad=whole_dur={n / fps:.6f},asetpts=PTS-STARTPTS[a{k}]"
                   for k, n in enumerate(frames))
    joined = "".join(f"[a{k}]" for k in range(len(frames))) + f"concat=n={len(frames)}:v=0:a=1[a]"
    proxy = out / "video" / f"{bid}_360p.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pictures), *[a for p in proxies for a in ("-i", str(p))],
                    "-filter_complex", f"{fit};{joined}", "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    # the fast coder: 5.2 s vs 18.1 s for 5 min of a preview's sound (28.3.b), plenty for reviewing
                    "-c:a", "aac", "-aac_coder", "fast", "-b:a", "64k", "-ac", "1", "-movflags", "+faststart",
                    str(proxy)], check=True)
    pictures.unlink()   # this run's own intermediate, by its literal name
    vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                 str(proxy)], capture_output=True, text=True, check=True).stdout)
    if abs(vdur - total) > 0.5:
        raise ValueError(f"joined preview {vdur:.2f} s vs {total:.2f} s")
    lags = [sync_lag(proxy, x, (o + n / 2) / fps) for o, n in zip(offs, frames)]
    log.info("preview sound vs analysis audio, middle of each piece: " +
             ", ".join(f"{s} {l * 1000:+.0f} ms" for s, l in zip(secs, lags)))
    if max(abs(l) for l in lags) > 0.010:
        raise ValueError(f"the joined preview is out of sync with the analysis audio: {lags}")
    proxy.with_suffix(".source.txt").write_text(f"{lst}\naudio: {wav.resolve()}\n", encoding="utf-8")

    # cuts, transcript, captions shifted onto the batch timeline
    cuts, rows, vtt = [], [], ["WEBVTT", ""]
    for k, (s, d, o) in enumerate(zip(secs, datas, offs), 1):
        off = o / fps
        for c in d["cuts"]:
            c = dict(c)
            c["id"] = f"p{k}{c['id']}"
            c["start"], c["end"] = round(c["start"] + off, 3), round(c["end"] + off, 3)
            for key in ("requested", "spec_window"):   # requested: content_cuts.json's own text ("0:04:13.5", "end")
                if key in c:
                    c[key] = [round((d["duration"] if v == "end" else v if isinstance(v, (int, float)) else
                                     sum(float(p) * 60 ** i for i, p in enumerate(reversed(v.split(":"))))) + off, 3)
                              for v in c[key]]
            c["flags"] = [FLAG_T.sub(lambda m: f"at {hms(sum(float(p) * 60 ** i for i, p in enumerate(reversed(m[1].split(':')))) + off, 1)}", f)
                          for f in c["flags"]]
            if c["source"] == "content":
                c["reason"] = f"[{s}] {c['reason']}"
            cuts.append(c)
        rows.append(f"{hms(off)}  ===== Դաս {pieces[s]['label']} ({s}) =====")
        for ln in (dirs[s] / "transcript.txt").read_text(encoding="utf-8").splitlines():
            m = re.match(r"^(\d+:\d\d(?::\d\d)?)\s+(.*)$", ln)
            if m:
                t = sum(float(p) * 60 ** i for i, p in enumerate(reversed(m[1].split(":"))))
                rows.append(f"{hms(t + off)}  {m[2]}")
        src_vtt = (dirs[s] / f"{d['video_id']}.hy.vtt").read_text(encoding="utf-8")
        body = src_vtt.split("\n\n", 1)[1] if src_vtt.startswith("WEBVTT") else src_vtt
        vtt.append(TIME.sub(lambda m: shift_vtt_time(m[0], off), body))
    (out / "transcript.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (out / f"{bid}.hy.vtt").write_text("\n".join(vtt), encoding="utf-8")
    meta = {"id": bid, "title": f"Vahagn {name}: {', '.join(secs)}", "duration": total, "fps": fps,
            "url": "", "silence_margin_db": margin}
    (out / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    data = {"video_id": bid, "title": meta["title"], "duration": total, "fps": fps,
            "params": {"min_silence": datas[0]["params"]["min_silence"], "pad": datas[0]["params"]["pad"],
                       "floor_db": floor, "audio_source": str(wav.resolve()), "threshold_db": floor + margin,
                       "blip_s": datas[0]["params"]["blip_s"]},
            "cuts": cuts,
            "marks": [[round(o / fps, 3), f"Դաս {pieces[s]['label']}"] for s, o in zip(secs, offs)],
            "batch": [{"section": s, "video_id": d["video_id"], "output_dir": str(dirs[s].relative_to(REPO)),
                       "offset_frames": o, "frames": n, "floor_db": d["params"]["floor_db"]}
                      for s, d, o, n in zip(secs, datas, offs, frames)]}
    (out / "edit_points.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([sys.executable, "scripts/find_edit_points.py", "--output-dir", str(out), "--report-only"],
                       cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"find_edit_points failed:\n{r.stderr[-2000:]}")
    planned = sum(len(d["studio_cuts"]) for d in datas)
    got = len(json.loads((out / "edit_points.json").read_text(encoding="utf-8"))["studio_cuts"])
    log.info(f"{name}: {len(secs)} pieces, {total / 60:.1f} min, {got} cuts on the page ({planned} in the pieces' plans; "
             f"fewer = a tail cut and the next piece's opening cut joined at a boundary), {time.time() - t0:.0f} s")
    log.info(f"page: {out / 'edit_review' / 'studio.html'}")


def cmd_split(name: str, file: Path | None, dry_run: bool = False) -> None:
    out = REPO / "output" / f"vahagn_{name}"
    data, fr = cut_list.load(out)
    src = file or out / cut_list.EDITED
    if file and not dry_run:
        (out / cut_list.EDITED).write_text(file.read_text(encoding="utf-8"), encoding="utf-8")
    entries = []   # (kind, current (s, e) or None, was (s, e) or None)
    for line in src.read_text(encoding="utf-8").splitlines():
        if rm := cut_list.REMOVED.match(line):
            entries.append(("removed", None, (fr(rm[1]), fr(rm[2]))))
        elif m := cut_list.CUT.match(line):
            cur, note = (fr(m[2]), fr(m[3])), m[5].strip()
            if not note:
                entries.append(("unchanged", cur, cur))
            elif w := re.match(r"CHANGED, was (\S+) -> (\S+)$", note):
                entries.append(("changed", cur, (fr(w[1]), fr(w[2]))))
            elif note == "NEW":
                entries.append(("new", cur, None))
            else:
                raise ValueError(f"unknown note {note!r} in {line!r}")
    if not entries and not re.search(r"^# 0 cuts\b", src.read_text(encoding="utf-8"), flags=re.M):
        raise ValueError(f"no cut lines in {src}")   # a page where every cut stayed a suggestion says "# 0 cuts"
    batch = data["batch"]
    plans = {}
    for b in batch:
        pd, pfr = cut_list.load(REPO / b["output_dir"])
        plans[b["section"]] = {(pfr(c["start_tc"]), pfr(c["end_tc"])) for c in pd["studio_cuts"]}

    def parts(rng):
        """{section: (start, end) in that piece's frames} for every piece the range overlaps by more than 2 frames."""
        res = {}
        for b in batch:
            o, n = b["offset_frames"], b["frames"]
            s, e = max(rng[0], o), min(rng[1], o + n)
            if e - s > 2:
                res[b["section"]] = (s - o, e - o)
            elif e - s > 0:
                log.info(f"{b['section']}: dropped a {e - s}-frame sliver of {fr.tc(rng[0])} -> {fr.tc(rng[1])} at a boundary")
        return res

    def snap(sec, p, must=False):
        for q in plans[sec]:
            if abs(q[0] - p[0]) <= 1 and abs(q[1] - p[1]) <= 1:
                return q
        if must:
            raise ValueError(f"{sec}: {p} is within one frame of no planned cut (a list from an older batch page?)")
        return p

    per = {b["section"]: {"cuts": [], "removed": []} for b in batch}
    crossing = 0
    for kind, cur, was in entries:
        pc = parts(cur) if cur else {}
        pw = {s: snap(s, p, must=True) for s, p in parts(was).items()} if was else {}
        crossing += len(pc) > 1 or len(pw) > 1
        for s, p in pc.items():
            p = snap(s, p) if s in pw else p
            if s not in pw:
                per[s]["cuts"].append((p, "NEW"))
            elif p == pw[s]:
                per[s]["cuts"].append((p, ""))
            else:
                per[s]["cuts"].append((p, f"CHANGED, was {fr.tc(pw[s][0])} -> {fr.tc(pw[s][1])}"))
        for s, w in pw.items():
            if s not in pc:
                per[s]["removed"].append(w)
    log.info(f"{len(entries)} entries in the batch list, {crossing} crossing a boundary (split)")

    stamp = time.strftime("%Y%m%d-%H%M")
    for b in batch:
        s, d = b["section"], REPO / b["output_dir"]
        cuts = sorted(per[s]["cuts"])
        kinds = {"changed": sum(n.startswith("CHANGED") for _, n in cuts), "new": sum(n == "NEW" for _, n in cuts),
                 "removed": len(per[s]["removed"])}
        lines = [f"# studio_cuts_edited_{b['video_id']}.txt | split from batch {name} ({stamp})",
                 f"# {len(cuts)} cuts ({kinds['changed']} changed, {kinds['new']} new, {kinds['removed']} removed), "
                 f"numbered as in Studio, listed last first for entry"]
        for n, ((a, e), note) in reversed(list(enumerate(cuts, 1))):
            lines.append(f"Cut {n:>2}   {fr.tc(a)}  ->  {fr.tc(e)}   ({(e - a) / fr.fps:.2f} s)" + (f"   {note}" if note else ""))
        lines += [f"# REMOVED, was {fr.tc(a)} -> {fr.tc(e)}" for a, e in sorted(per[s]["removed"])]
        if dry_run:   # check against a copy of the piece's plan; the piece folder is not touched
            d2 = out / "split_check" / s
            d2.mkdir(parents=True, exist_ok=True)
            (d2 / "edit_points.json").write_text((d / "edit_points.json").read_text(encoding="utf-8"), encoding="utf-8")
            d = d2
        dest = d / cut_list.EDITED
        if dest.exists() and not dry_run:
            dest.rename(d / f"studio_cuts_edited.before_{stamp}.txt")
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        for sub in (("check",) if dry_run else ("check", "to-enter")):
            r = subprocess.run([sys.executable, "scripts/cut_list.py", sub, "--output-dir", str(d)], cwd=REPO,
                               capture_output=True, text=True, encoding="utf-8")
            summary = [ln.split("INFO ")[-1] for ln in (r.stdout + r.stderr).splitlines()
                       if "cuts in the paste" in ln or "removes" in ln or "ERROR" in ln]
            if r.returncode != 0:
                raise RuntimeError(f"{s}: cut_list.py {sub} failed:\n{(r.stdout + r.stderr)[-1500:]}")
            if sub == "check":
                log.info(f"{s}: {' | '.join(summary)}")
    secs = [b["section"] for b in batch]
    if dry_run:
        log.info(f"dry run: lists and checks in {out / 'split_check'}; no piece folder changed")
        return
    for script in (["scripts/non_essential/vahagn_build_drafts.py", *secs], ["scripts/non_essential/vahagn_review_page.py"]):
        r = subprocess.run([sys.executable, *script], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise RuntimeError(f"{script[0]} failed:\n{(r.stdout + r.stderr)[-1500:]}")
    log.info(f"split {name} into {len(secs)} pieces; chapters remapped, review page rebuilt")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    b = sub.add_parser("build")
    b.add_argument("name")
    b.add_argument("sections", nargs="+")
    s = sub.add_parser("split")
    s.add_argument("name")
    s.add_argument("--file", type=Path)
    s.add_argument("--dry-run", action="store_true", help="write and check the per-piece lists in "
                   "output/vahagn_<name>/split_check/ only; no piece folder, chapter or page changes")
    args = ap.parse_args()
    if args.cmd == "plan":
        cmd_plan()
    elif args.cmd == "build":
        cmd_build(args.name, args.sections)
    else:
        cmd_split(args.name, args.file, args.dry_run)


if __name__ == "__main__":
    main()
