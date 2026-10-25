"""Build the studio.html video previews for some Tserunyan lectures, one after another, and check after
each that the page's cut list is still the active 5 s plan (the Cut lines of studio_cuts.txt equal
studio_cuts_v3_5s.txt). Two of these run in parallel (the user's pick). ~25-40 min per lecture then.

    python preview_queue.py 17 19 21 ...     (from the repo root)
"""
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")


def cut_lines(p: Path) -> list:
    return [l for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("Cut")]


t_all = time.time()
for n in sys.argv[1:]:
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    r = subprocess.run([sys.executable, "scripts/find_edit_points.py", "--output-dir", str(d), "--report-only",
                        "--video-preview"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    (d / "logs_preview.txt").write_text(r.stdout + r.stderr, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"Das {n}: find_edit_points failed ({r.returncode}), see {d / 'logs_preview.txt'}")
    same = cut_lines(d / "studio_cuts.txt") == cut_lines(d / "studio_cuts_v3_5s.txt")
    mp4 = next((d / "video").glob("*_360p.mp4"), None)
    size = f"{mp4.stat().st_size / 1e6:.0f} MB" if mp4 else "NO MP4"
    print(f"{time.strftime('%H:%M')} Das {n}: preview {size}, cut list {'unchanged' if same else 'CHANGED'}, "
          f"{(time.time() - t0) / 60:.0f} min", flush=True)
    if not same:
        raise SystemExit(f"Das {n}: studio_cuts.txt differs from studio_cuts_v3_5s.txt after the rebuild")
print(f"queue done in {(time.time() - t_all) / 60:.0f} min")
