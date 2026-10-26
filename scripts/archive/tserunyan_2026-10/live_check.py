"""Live check of Tserunyan 15-27 as a viewer sees them (yt-dlp, no API quota): title = edited/titles.txt line 1,
chapters YouTube parsed = our chapter lines (nested ones included), first chapter label, and the served thumbnail
against our PNG (64x36 grey, mean abs difference: same image ~<12, a video frame ~>40). Read-only. ~6 s per video."""
import io
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")


def small(img):
    return img.convert("L").resize((64, 36))


bad = 0
for n in range(15, 28):
    t0 = time.time()
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    vid = d.name.split("_", 2)[2]
    r = subprocess.run(["yt-dlp", "-J", "--skip-download", f"https://www.youtube.com/watch?v={vid}"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        raise RuntimeError(f"Das {n}: yt-dlp failed\n{r.stderr[-800:]}")
    info = json.loads(r.stdout)
    title = (d / "edited" / "titles.txt").read_text(encoding="utf-8").splitlines()[0].strip()
    ours = [l for l in (d / "edited" / "timestamps.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    chaps = info.get("chapters") or []
    url = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    served = Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=20).read()))
    local = Image.open(REPO / "thumbnails" / "umath" / f"metric_{n}.png")
    diff = ImageStat.Stat(ImageChops.difference(small(served), small(local))).mean[0]
    ok = (info["title"] == title, len(chaps) == len(ours), diff < 12)
    bad += not all(ok)
    first = chaps[0]["title"] if chaps else "-"
    print(f"Das {n}: title {'OK' if ok[0] else 'DIFF'} | chapters parsed {len(chaps)} of {len(ours)} "
          f"{'OK' if ok[1] else 'DIFF'} | thumbnail diff {diff:.1f} {'OK' if ok[2] else 'NOT OURS YET'} | "
          f"{info.get('availability')} | {time.time() - t0:.0f} s", flush=True)
print(f"{13 - bad} of 13 all OK", flush=True)
