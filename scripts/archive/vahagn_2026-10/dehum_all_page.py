"""One page with all 18 dehum files under each other, to check them before uploading (the user, 2026-10-27: "all the 18
vids under each other with the spectograms so i can quickly check all for any problems before uploading").

    python scripts/archive/vahagn_2026-10/dehum_all_page.py      # ~5 min, one piece at a time
    -> output/vahagn_linalg_overview/audio/dehum_all.html

Per piece: the dehum video itself (played from disk, so the page works on this laptop only), the whole piece's
spectrogram after and before (log frequency 30 Hz - 8 kHz, 16 kHz audio, mean power per column; the hum lines live
under 600 Hz), a playhead that follows the video, click to seek, and the measured buzz per minute from
_knowledge/vahagn_linalg/dehum_check.json. The spectrograms are embedded as JPEG."""
import base64
import html
import io
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

import numpy as np
from matplotlib import colormaps
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
RAW = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
FF = r"C:\Users\hayk_\tools\ffmpeg-9\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
OUT = REPO / "output/vahagn_linalg_overview/audio/dehum_all.html"
SR, N, HOP = 16000, 2048, 1024
W, H, FMIN, FMAX, RANGE_DB = 1400, 200, 30.0, 8000.0, 75.0
TICKS = [50, 100, 200, 500, 1000, 2000, 5000]
CMAP = colormaps["magma"]


def decode(p: Path) -> np.ndarray:
    r = subprocess.run([FF, "-v", "error", "-nostats", "-i", str(p), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le",
                        "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)


def rows_map() -> list[np.ndarray]:
    """For each image row (top = FMAX), the FFT bins in its log-spaced band (the nearest bin when the band has none)."""
    f = np.fft.rfftfreq(N, 1 / SR)
    edges = np.geomspace(FMIN, FMAX, H + 1)[::-1]
    out = []
    for hi, lo in zip(edges[:-1], edges[1:]):
        idx = np.flatnonzero((f >= lo) & (f < hi))
        out.append(idx if len(idx) else np.array([int(np.argmin(np.abs(f - np.sqrt(lo * hi))))]))
    return out


ROWS = rows_map()


def spectrogram(x: np.ndarray) -> np.ndarray:
    """W columns of mean power, H log-frequency rows, in dB."""
    nf = (len(x) - N) // HOP
    col = (np.arange(nf) * W // nf).astype(np.int64)
    starts = np.searchsorted(col, np.arange(W))
    acc = np.zeros((W, N // 2 + 1))
    win = np.hanning(N).astype(np.float32)
    for b0 in range(0, nf, 4000):
        b1 = min(nf, b0 + 4000)
        p = np.abs(np.fft.rfft(x[np.arange(N)[None, :] + HOP * np.arange(b0, b1)[:, None]] * win, axis=1)) ** 2
        np.add.at(acc, col[b0:b1], p)
    acc /= np.maximum(np.diff(np.r_[starts, nf]), 1)[:, None]
    return np.stack([10 * np.log10(acc[:, idx].max(axis=1) + 1e-20) for idx in ROWS])     # (H, W)


def jpeg(db: np.ndarray) -> str:
    top = np.percentile(db, 99.5)
    rgb = (CMAP(np.clip((db - (top - RANGE_DB)) / RANGE_DB, 0, 1))[:, :, :3] * 255).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(rgb).save(buf, "JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()


def strip(after: list[float], inside: list[int]) -> str:
    cells = []
    for m, v in enumerate(after):
        c = "#0033A0" if v <= -68 else "#F2A800" if v <= -62 else "#D90012"
        tip = f"min {m}: {v:.1f} dB vs speech" + ("" if m in inside else " (outside the buzz: the light chain)")
        cells.append(f"<span class='m' style='background:{c};opacity:{1 if m in inside else .35}' title='{tip}'></span>")
    return "<div class='strip'>" + "".join(cells) + "</div>"


def main() -> None:
    t0 = time.time()
    res = json.loads((REPO / "_knowledge/vahagn_linalg/dehum.json").read_text(encoding="utf-8"))
    chk = json.loads((REPO / "_knowledge/vahagn_linalg/dehum_check.json").read_text(encoding="utf-8"))
    order = lambda s: [int(p) if p.isdigit() else p for p in s.split(".")]
    secs = sorted((s for s, v in res.items() if " " not in s and v.get("regions")), key=order)
    if len(secs) != 18:
        raise ValueError(f"{len(secs)} pieces with a dehum file, expected 18: {secs}")
    parts = []
    for k, s in enumerate(secs, 1):
        dest = Path(res[s]["output"])
        raw = next(iter(RAW.glob(f"Videos Part */VidSection {s}.mp4")))
        y = decode(dest)
        dur = len(y) / SR
        a = jpeg(spectrogram(y))
        del y
        b = jpeg(spectrogram(decode(raw)))
        c = chk[s]
        worst = max(c["after_per_min"][m] for m in c["inside_minutes"])
        regions = "everywhere" if res[s]["whole"] else ", ".join(f"{int(r0 // 60)}:{int(r0 % 60):02d}-{int(r1 // 60)}:"
                                                                  f"{int(r1 % 60):02d}" for r0, r1 in res[s]["regions"])
        sid = "p" + s.replace(".", "_")
        src = "file:///" + quote(dest.as_posix(), safe="/:")
        parts.append((sid, s, worst, f"""
<details open id="{sid}"><summary>{s} <span class="note">buzz {regions}; worst minute {worst:.1f} dB vs speech
({res[s]['buzz_before_db']} before)</span></summary>
<video controls preload="metadata" src="{src}" data-dur="{dur:.3f}"></video>
<div class="lbl">After (the file you upload)</div>
<div class="spec" data-dur="{dur:.3f}"><img src="data:image/jpeg;base64,{a}"><div class="ph"></div><div class="ax"></div></div>
<div class="lbl">Buzz per minute after (blue -68 or better, orange to -62, red worse; faded = outside the buzz)</div>
{strip(c['after_per_min'], c['inside_minutes'])}
<div class="lbl">Before (raw)</div>
<div class="spec" data-dur="{dur:.3f}"><img src="data:image/jpeg;base64,{b}"><div class="ph"></div><div class="ax"></div></div>
</details>"""))
        el = time.time() - t0
        print(f"{k}/{len(secs)} {s}: {dur / 60:.1f} min, {el:.0f} s elapsed, ~{el / k * (len(secs) - k):.0f} s left",
              flush=True)

    ypos = {f: 100 * np.log(FMAX / f) / np.log(FMAX / FMIN) for f in TICKS}
    yt = "".join(f"<span class='yt' style='top:{p:.2f}%'>{f if f < 1000 else f'{f // 1000}k'}</span>" for f, p in ypos.items())
    toc = "".join(f"<li><a href='#{sid}'>{s}</a> <span class='note'>worst {w:.1f}</span></li>" for sid, s, w, _ in parts)
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn dehum: all 18</title><style>
body{{font-family:system-ui,sans-serif;max-width:1440px;margin:20px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.15em;font-weight:600;cursor:pointer}} details{{margin:14px 0 26px;border-top:1px solid #ddd;padding-top:8px}}
.note{{font-weight:400;color:#555;font-size:.85em}} video{{width:480px;max-width:100%;display:block;margin:8px 0}}
.spec{{position:relative;cursor:crosshair;line-height:0}} .spec img{{width:100%;height:160px;display:block}}
.ph{{position:absolute;top:0;bottom:0;width:2px;background:#0ff;left:0;pointer-events:none}}
.ax{{position:absolute;inset:0;pointer-events:none}} .yt,.xt{{position:absolute;font:10px system-ui;color:#fff;
text-shadow:0 0 2px #000;line-height:1}} .yt{{left:3px;transform:translateY(-50%)}} .xt{{bottom:2px;transform:translateX(-50%)}}
.lbl{{font-size:.8em;color:#444;margin:6px 0 2px}} .strip{{display:flex;height:12px;gap:1px}} .m{{flex:1}}
ul.toc{{columns:4;font-size:.9em}}
</style></head><body>
<h1>Vahagn: the 18 buzz-free files, before uploading</h1>
<nav><b>Contents</b><ul class="toc"><li><a href="#how">How to read this</a></li>{toc}</ul></nav>
<details open id="how"><summary>How to read this</summary>
<p>Each piece: its dehum video (the file itself, from disk), then the whole piece's spectrogram after and before. Height is
frequency on a log scale (50 Hz at the bottom labels, 5k near the top); the mains hum is the horizontal lines under
~600 Hz in "Before", which should be gone in "After". Click a spectrogram to jump the video there; the cyan line follows
the video. Things to look for: lines still there in "After", gaps or dark columns (a dropout), a sudden change in the
background at a boundary of the buzz map (where the two chains are joined), speckles that "Before" does not have.
The strip is the measured buzz per minute (the same numbers as the check you listened to). Times = the uncut file.</p>
</details>
{''.join(p for _, _, _, p in parts)}
<script>
const YT = `{yt}`;
document.querySelectorAll('details[id^="p"]').forEach(sec => {{
  const v = sec.querySelector('video');
  const specs = [...sec.querySelectorAll('.spec')];
  const dur = parseFloat(v.dataset.dur);
  specs.forEach(sp => {{
    const ax = sp.querySelector('.ax');
    let s = YT;
    const step = dur > 1200 ? 300 : 120;
    for (let t = step; t < dur; t += step)
      s += `<span class="xt" style="left:${{100 * t / dur}}%">${{Math.floor(t / 60)}}:00</span>`;
    ax.innerHTML = s;
    sp.addEventListener('click', e => {{
      const r = sp.getBoundingClientRect();
      v.currentTime = Math.max(0, Math.min(dur, (e.clientX - r.left) / r.width * dur));
      v.play();
    }});
  }});
  v.addEventListener('timeupdate', () => specs.forEach(sp =>
    sp.querySelector('.ph').style.left = `${{100 * v.currentTime / dur}}%`));
  v.addEventListener('play', () => document.querySelectorAll('video').forEach(o => {{ if (o !== v) o.pause(); }}));
}});
</script>
</body></html>"""
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT} {OUT.stat().st_size / 1e6:.1f} MB, {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
