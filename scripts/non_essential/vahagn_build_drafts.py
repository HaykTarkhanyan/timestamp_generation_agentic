"""Assemble the local drafts of the Vahagn linear algebra pieces (DECISIONS #35): titles, description, chapters
mapped through the current cut list, verifier and glossary results, thumbnail. Nothing is pushed.

Inputs: _knowledge/vahagn_linalg/pieces.json (titles, date, thumbnail text) and, per piece,
<output dir>/edited_predicted/timestamps_raw.txt (chapters on the raw timeline) plus the cut list:
studio_cuts_to_enter.txt once the user has reviewed the piece, else the 4 s plan studio_cuts.txt.

    python scripts/non_essential/vahagn_build_drafts.py              # every piece with a draft
    python scripts/non_essential/vahagn_build_drafts.py 22.1 23.2    # some
Expected: ~3 s per piece (~1.5 min for 24). Writes, per piece, edited_predicted/{titles.txt, description.txt,
timestamps.txt, transcript.txt, metadata.json, verify_report.json, glossary_check.txt}, the thumbnail
thumbnails/umath/linalg_<section>.png, and the summary _knowledge/vahagn_linalg/drafts_status.json.
"""
import argparse
import json
import logging
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / ".claude/skills/youtube-timestamps/scripts"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_build_drafts.log", encoding="utf-8")])
log = logging.getLogger(__name__)

SUFFIX = " | Գծային հանրահաշիվ"
DIVIDER = "──────────────────────────────"
INTRO = ("ԵՊՀ Ինֆորմատիկայի և կիրառական մաթեմատիկայի ֆակուլտետի դասախոս պրոֆ․ Վահագն Միքայելյանի դասախոսությունը "
         "«Բարձրագույն հանրահաշիվ» առարկայից՝ գծային հանրահաշվի վերաբերյալ։")
PLAYLIST = "https://www.youtube.com/playlist?list=PLz3NrXxHz_CCqlI0X_XZvf4YOVuF2n_FM"


def run(cmd: list, ok_codes=(0,)) -> subprocess.CompletedProcess:
    r = subprocess.run([str(c) for c in cmd], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if r.returncode not in ok_codes:
        raise RuntimeError(f"{' '.join(map(str, cmd[:3]))} ... failed ({r.returncode}):\n{r.stdout[-800:]}\n{r.stderr[-1500:]}")
    return r


def build(piece: dict, uploads: dict) -> dict:
    sec = piece["section"]
    vid = uploads[sec]
    out = next(iter(REPO.glob(f"output/*_{vid}")))
    ep = out / "edited_predicted"
    raw = (ep / "timestamps_raw.txt").read_text(encoding="utf-8").rstrip("\n").splitlines()
    cuts = "studio_cuts_to_enter.txt" if (out / "studio_cuts_to_enter.txt").exists() else "studio_cuts.txt"
    if not (out / cuts).exists() or not (out / "edit_points.json").exists():
        raise FileNotFoundError(f"{sec}: no {cuts} / edit_points.json in {out} (run vahagn_plan_queue.py first)")
    titles = [f"Դաս {piece['label']} | {t}{SUFFIX}" for t in piece["titles"]]
    for t in titles:
        if len(t) > 100:
            raise ValueError(f"{sec}: title over 100 characters ({len(t)}): {t}")
    (ep / "titles.txt").write_text("\n".join(titles) + "\n", encoding="utf-8")

    desc = [f"🎬 Վերնագիր՝ {titles[0]}", "", DIVIDER, "", INTRO, "", f"🗓️ Ամսաթիվ՝ {piece['date']}", "", "",
            "📚 Դասախոսությունների ֆայլը՝", "http://bit.ly/LinAlgebra", "Դասագրքեր և այլ նյութեր՝",
            "https://mathteam.notion.site/algebra", "", "", "⏳ Թեմաներ", *raw, "", "",
            "👇 Բոլոր դասախոսությունները՝", PLAYLIST]
    text = "\n".join(desc) + "\n"
    if "<" in text or ">" in text:
        raise ValueError(f"{sec}: ASCII < or > in the description (YouTube rejects it)")
    (ep / "description.txt").write_text(text, encoding="utf-8")

    run([sys.executable, "scripts/map_transcript_to_edit.py", "--output-dir", out, "--cuts", cuts])
    remap = run([sys.executable, "scripts/remap_chapters.py", "--output-dir", out, "--from-cuts", "raw",
                 "--from", "edited_predicted/timestamps_raw.txt", "--to-cuts", cuts])
    moved = [ln.split("INFO ")[-1] for ln in remap.stdout.splitlines() if "moved to the end of cut" in ln]
    short = [ln.split("WARNING ")[-1] for ln in remap.stdout.splitlines() if "WARNING" in ln]
    ver = run([sys.executable, SKILL / "verify_timestamps.py", ep / "timestamps.txt", "--metadata", ep / "metadata.json",
               "--transcript", ep / "transcript.txt", "--min-gap", "30"], ok_codes=(0, 1))
    report = json.loads((ep / "verify_report.json").read_text(encoding="utf-8"))
    glo = run([sys.executable, SKILL / "glossary_check.py", ep / "timestamps.txt", ep / "titles.txt", ep / "description.txt"],
              ok_codes=(0, 1))
    (ep / "glossary_check.txt").write_text(glo.stdout + glo.stderr, encoding="utf-8")
    kinds = re.findall(r"\b(DENY|NEAR|ENG)\b", glo.stdout)
    thumb = REPO / f"thumbnails/umath/linalg_{sec}.png"
    run([sys.executable, "scripts/make_umath_thumbnails.py", "--series", "linalg", "--lesson", piece["label"],
         "--topic", piece["thumb"], "-o", thumb])
    meta = json.loads((ep / "metadata.json").read_text(encoding="utf-8"))
    status = {"section": sec, "video_id": vid, "output_dir": str(out.relative_to(REPO)), "cut_list": cuts,
              "title": titles[0], "chapters": len(raw), "nested": sum(1 for l in raw if l.startswith("    ")),
              "predicted_length_s": meta.get("duration"), "verifier_valid": report.get("valid"),
              "verifier_issues": report.get("issues"), "moved_into_cut_ends": moved, "gaps_under_30s": short,
              "glossary": {k: kinds.count(k) for k in ("DENY", "NEAR", "ENG")}, "thumbnail": str(thumb.relative_to(REPO)),
              "description_chars": len("\n".join(desc[4:]))}
    level = logging.INFO if report.get("valid") and not status["glossary"]["DENY"] else logging.WARNING
    log.log(level, f"{sec}: {len(raw)} chapters ({status['nested']} nested), valid={report.get('valid')}, "
                   f"glossary {status['glossary']}, moved {len(moved)}, short gaps {len(short)}, {cuts}")
    return status


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*")
    args = ap.parse_args()
    pieces = json.loads((REPO / "_knowledge/vahagn_linalg/pieces.json").read_text(encoding="utf-8"))["pieces"]
    uploads = {u["section"]: u["id"] for u in json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json")
                                                          .read_text(encoding="utf-8"))}
    todo = [p for p in pieces if p["titles"] and (not args.sections or p["section"] in args.sections)]
    t0 = time.time()
    status_path = REPO / "_knowledge/vahagn_linalg/drafts_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    failed = []
    for i, p in enumerate(todo, 1):
        try:
            status[p["section"]] = build(p, uploads)
        except Exception as e:
            log.error(f"{p['section']}: {e}")
            failed.append(p["section"])
        log.info(f"{i}/{len(todo)} ({time.time() - t0:.0f} s elapsed)")
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=1), encoding="utf-8")
    log.info(f"done in {time.time() - t0:.0f} s; summary in {status_path.relative_to(REPO)}")
    if failed:
        raise SystemExit(f"FAILED: {failed}")


if __name__ == "__main__":
    main()
