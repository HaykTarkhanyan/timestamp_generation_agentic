"""Loudness samples for the Vahagn audio-only fix (Q82): the same 40 s at several target levels, after Ashot's
chain (80 Hz low cut + light afftdn). The gain comes from the WHOLE piece's loudness after the chain, as the batch
will compute it, so each clip sounds like the final file. Plus 23.3.b untouched (the hum) and published 20.3 as
YouTube serves it (the neighbouring videos). Standalone HTML, clips embedded. ~1.5 min, one core."""
import base64
import html
import re
import subprocess
import time
from pathlib import Path

RAW = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
OUT = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\output\vahagn_linalg_overview\audio")
REF = Path(r"C:\Users\hayk_\AppData\Local\Temp\claude\C--Users-hayk--OneDrive-Desktop-timestamp-generation-agentic"
           r"\5791a543-07ae-454f-84b0-13fbb91d0e60\scratchpad\calib\yt_pCzP2OJnUns.wav")
OUT.mkdir(parents=True, exist_ok=True)
CHAIN = "highpass=f=80,afftdn=nr=12:nf=-50:tn=1"
LIMIT = "alimiter=limit=0.891:level=0"   # peaks at -1 dBFS, no auto-gain of its own (render_lecture.py)
TARGETS = [None, -20.0, -16.0, -14.0]    # None = the recording's own level, after the chain
PIECES = [("21.1", RAW / "Videos Part 7/VidSection 21.1.mp4", 51.0, "clean recording (noise floor about -80 dB)"),
          ("23.3.b", RAW / "Videos Part 8/VidSection 23.3.b.mp4", 55.0,
           "the worst hum recording (70 Hz mains hum, noise floor -47.6 dB)")]
LEN = 40.0


def measure(args: list[str], af: str) -> tuple[float, float]:
    """Integrated loudness (LUFS) and sample peak (dBFS) of the input after af."""
    r = subprocess.run(["ffmpeg", "-nostats", *args, "-vn", "-af", f"{af},ebur128=peak=sample", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return (float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1]),
            float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1]))


def clip(src: Path, start: float, af: str, name: str) -> dict:
    out = OUT / f"{name}.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(LEN), "-i", str(src), "-vn",
                    "-af", af, "-ac", "1", "-ar", "48000", "-c:a", "aac", "-b:a", "96k", str(out)], check=True)
    i, pk = measure(["-i", str(out)], "anull")
    return {"name": name, "af": af, "clip_lufs": i, "clip_peak": pk, "path": out}


t0 = time.time()
sections = []
for sec, src, start, what in PIECES:
    if not src.exists():
        raise FileNotFoundError(src)
    whole, whole_pk = measure(["-i", str(src)], CHAIN)
    print(f"{sec}: whole piece after the chain {whole:.1f} LUFS, peak {whole_pk:.1f} dBFS ({time.time() - t0:.0f} s)")
    rows = []
    if sec == "23.3.b":
        r = clip(src, start, "anull", f"{sec}_0_untouched")
        r["label"], r["whole"] = "Untouched: no cleanup, no gain (what the raw upload sounds like)", None
        rows.append(r)
    for n, tgt in enumerate(TARGETS, 1):
        if tgt is None:
            r = clip(src, start, CHAIN, f"{sec}_{n}_own")
            r["label"], r["whole"] = f"Cleanup, own level (whole piece {whole:.1f} LUFS, gain 0 dB)", whole
        else:
            g = tgt - whole
            r = clip(src, start, f"{CHAIN},volume={g:.2f}dB,{LIMIT}", f"{sec}_{n}_{int(-tgt)}")
            r["label"], r["whole"] = f"Cleanup, raised to {tgt:.0f} LUFS (gain {g:+.1f} dB, peaks limited to -1 dBFS)", tgt
        rows.append(r)
        print(f"  {r['name']}: clip {r['clip_lufs']:.1f} LUFS, peak {r['clip_peak']:.1f} dBFS")
    sections.append((sec, start, what, whole, rows))

ref_whole, _ = measure(["-i", str(REF)], "anull")
ref = clip(REF, 60.0, "anull", "ref_20.3_published")
ref["label"] = f"Published Դաս 20.3 as YouTube serves it (whole video {ref_whole:.1f} LUFS)"
print(f"reference: whole {ref_whole:.1f} LUFS, clip {ref['clip_lufs']:.1f} ({time.time() - t0:.0f} s)")


def player(r: dict) -> str:
    b64 = base64.b64encode(r["path"].read_bytes()).decode()
    return (f"<div class='s'><h3>{html.escape(r['label'])}</h3>"
            f"<p class='m'>this clip: {r['clip_lufs']:.1f} LUFS, peak {r['clip_peak']:.1f} dBFS</p>"
            f"<audio controls preload='auto' src='data:audio/mp4;base64,{b64}'></audio>"
            f"<p class='m'><code>{html.escape(r['af'])}</code></p></div>")


def fmt(s: float) -> str:
    return f"{int(s // 60)}:{s % 60:04.1f}"


toc = ["<li><a href='#how'>How to listen</a></li>", "<li><a href='#ref'>Reference: published 20.3</a></li>"]
body = [f"""<details open id="how"><summary>How to listen</summary>
<p>Set the volume once on the reference clip (or on any ordinary YouTube video) and don't touch it again while
comparing. YouTube turns videos louder than about -14 LUFS down, but never turns quiet ones up (our raw 21.1 upload
stayed at -24.2 LUFS, the file is -24.1), so what you hear here is what viewers will get.</p>
<p>The gain for each level is computed from the whole piece, so the clip's own loudness differs a little from the
target. Every cleaned clip uses Ashot's chain: <code>{CHAIN}</code>.</p></details>""",
        f"<details open id='ref'><summary>Reference: published Դաս 20.3 (the neighbouring videos)</summary>"
        f"<p>1:00-1:40 of the YouTube copy. The previous editor's pieces are about 3 dB under their raw files.</p>"
        f"{player(ref)}</details>"]
for sec, start, what, whole, rows in sections:
    sid = "s" + sec.replace(".", "-")
    toc.append(f"<li><a href='#{sid}'>Դաս {sec}: {html.escape(what)}</a></li>")
    body.append(f"<details open id='{sid}'><summary>Դաս {sec}: {html.escape(what)}</summary>"
                f"<p>{fmt(start)}-{fmt(start + LEN)} of the raw file. Whole piece after the cleanup: {whole:.1f} LUFS.</p>"
                + "".join(player(r) for r in rows) + "</details>")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn loudness samples</title><style>
body{{font-family:system-ui,sans-serif;max-width:860px;margin:24px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.2em;font-weight:600;cursor:pointer}} details{{margin:18px 0}}
.s{{border:1px solid #ddd;border-radius:8px;padding:10px 14px;margin:12px 0}}
h3{{margin:4px 0;font-size:1em}} .m{{color:#555;font-size:.9em;margin:4px 0}} audio{{width:100%}} code{{font-size:.85em}}
</style></head><body>
<h1>Vahagn linear algebra: loudness samples</h1>
<nav><b>Contents</b><ul>{''.join(toc)}</ul></nav>
{''.join(body)}
</body></html>"""
dest = OUT / "loudness_samples.html"
dest.write_text(page, encoding="utf-8")
print(f"page: {dest} ({dest.stat().st_size / 1e6:.1f} MB) in {time.time() - t0:.0f} s")
