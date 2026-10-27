"""A/B samples of fixes for the mains buzz (the user's pure-noise sample: 28.3.a 20:47.6-20:51.0).
usage: dehum_samples.py <f0 Hz> <start s> <len s>    -> output/vahagn_linalg_overview/audio/dehum_samples.html
Versions: raw / the current upload (its own audio) / dehum notches + light chain / + denoise with the user's sample
as the noise profile (nr 20, nr 30). 3-5 matched to the current upload's loudness. Standalone page."""
import base64
import html
import re
import subprocess
import sys
from pathlib import Path

RAWDIR = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
SRC = RAWDIR / "Videos Part 9" / "VidSection 28.3.a.mp4"
FIXED = RAWDIR / "audio_fixed" / "VidSection 28.3.a fixed.mp4"
OUT = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\output\vahagn_linalg_overview\audio")
NOISE_AT, NOISE_LEN = 1247.6, 3.4                       # the user's mark, 28.3.a 20:47.6-20:51.0
f0, start, length = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
LIGHT = "highpass=f=80,afftdn=nr=12:nf=-50:tn=1"
# the 48.39 Hz ladder, plus a second source the fit found off it (f0_fit.py: 90.0, 113.8, 138.3, 900, 1080 Hz)
EXTRA = [90.0, 113.8, 138.3, 900.0, 1080.0]
NOTCH = ",".join(f"bandreject=f={fq:.2f}:width_type=q:w=20"
                 for fq in sorted([k * f0 for k in range(1, 23) if k * f0 < 1100] + EXTRA))
LIMIT = "alimiter=limit=0.891:level=0"


def lufs(path: Path) -> float:
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8")
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def render(name: str, chain: str | None, with_profile: bool = False) -> Path:
    out = OUT / f"dehum_{name}.m4a"
    if chain is None:                                    # the current upload: its own sound, untouched
        cmd = ["-ss", str(start), "-t", str(length), "-i", str(FIXED), "-vn", "-c:a", "aac", "-b:a", "128k"]
    elif with_profile:
        # put the noise sample in front, let afftdn learn it there (sample_noise start/stop), then drop it
        learn = f"asendcmd=c='0.2 afftdn sn start;{NOISE_LEN - 0.2:.1f} afftdn sn stop',afftdn="
        sampled = chain.replace("afftdn=", learn)
        fc = (f"[0:a]atrim=start={NOISE_AT}:duration={NOISE_LEN},asetpts=PTS-STARTPTS[n];"
              f"[0:a]atrim=start={start}:duration={length},asetpts=PTS-STARTPTS[s];"
              f"[n][s]concat=n=2:v=0:a=1,{sampled},atrim=start={NOISE_LEN},asetpts=PTS-STARTPTS[a]")
        cmd = ["-i", str(SRC), "-filter_complex", fc, "-map", "[a]", "-c:a", "aac", "-b:a", "128k"]
    else:
        cmd = ["-ss", str(start), "-t", str(length), "-i", str(SRC), "-vn", "-af", chain, "-c:a", "aac", "-b:a", "128k"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", *cmd, "-ar", "48000", "-ac", "1", str(out)], check=True)
    return out


target = lufs(render("2_current", None))
rows = [("1_raw", "Raw recording, untouched", render("1_raw", "anull"))]
rows.append(("2_current", "What is on YouTube now: 80 Hz low cut + light denoise, -16 LUFS", OUT / "dehum_2_current.m4a"))
versions = [("3_notches", "Notches: the 48.4 Hz hum ladder + the 90/114/138 Hz peaks (Q 20, up to 1.1 kHz) + the light chain",
             f"{NOTCH},{LIGHT}", False),
            ("4_profile", "Denoise that learns the noise from your sample (20 dB), no notches",
             "highpass=f=80,afftdn=nr=20:nf=-50:tn=0", True),
            ("5_both", "Notches + the denoise that learns from your sample (20 dB)",
             f"{NOTCH},highpass=f=80,afftdn=nr=20:nf=-50:tn=0", True),
            ("6_both_strong", "Notches + the denoise that learns from your sample, stronger (30 dB)",
             f"{NOTCH},highpass=f=80,afftdn=nr=30:nf=-50:tn=0", True)]
for name, label, chain, prof in versions:
    tmp = render(name + "_tmp", chain, prof)
    gain = target - lufs(tmp)
    out = OUT / f"dehum_{name}.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", f"volume={gain:.2f}dB,{LIMIT}", "-c:a", "aac",
                    "-b:a", "128k", str(out)], check=True)
    tmp.unlink()                                          # this run's own intermediate, by its literal name
    rows.append((name, label, out))
for name, label, p in rows:
    print(f"{name}: {lufs(p):.1f} LUFS")


def player(name, label, p):
    return (f"<div class='s'><h3>{html.escape(label)}</h3><audio controls preload='auto' "
            f"src='data:audio/mp4;base64,{base64.b64encode(p.read_bytes()).decode()}'></audio></div>")


mmss = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vahagn dehum samples</title><style>
body{{font-family:system-ui,sans-serif;max-width:860px;margin:24px auto;padding:0 16px;background:#fff;color:#111}}
summary{{font-size:1.2em;font-weight:600;cursor:pointer}} details{{margin:18px 0}}
.s{{border:1px solid #ddd;border-radius:8px;padding:10px 14px;margin:12px 0}} h3{{margin:4px 0;font-size:1em}}
audio{{width:100%}} code{{font-size:.85em}} p{{color:#444}}
</style></head><body>
<h1>Vahagn: fixing the mains buzz</h1>
<nav><b>Contents</b><ul><li><a href="#how">What this is</a></li><li><a href="#samples">Samples</a></li></ul></nav>
<details open id="how"><summary>What this is</summary>
<p>28.3.a {mmss(start)}-{mmss(start + length)} (your pure-noise mark is at 20:47.6-20:51.0). The buzz is the mains hum,
{f0:.1f} Hz, and its harmonics up to ~600 Hz. 3-5 are matched to the loudness of 2, so volume does not decide.
Listen to the pauses (the buzz) and to his voice (does it get thin, watery or metallic?).</p></details>
<details open id="samples"><summary>Samples</summary>{''.join(player(*r) for r in rows)}</details>
</body></html>"""
dest = OUT / "dehum_samples.html"
dest.write_text(page, encoding="utf-8")
print(dest)
