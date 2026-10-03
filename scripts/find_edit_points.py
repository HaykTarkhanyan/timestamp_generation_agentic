#!/usr/bin/env python
"""Find edit points (cuts) in an unedited lecture recording and build a review page.

Two sources of cuts:
  1. Silence runs in the audio, >= --min-silence seconds (default 2.0). Each cut
     leaves --pad seconds of pause on both sides, so speech is never clipped.
  2. Content cuts picked from the transcript (<output-dir>/content_cuts.json,
     written by the LLM stage: dead air, "any questions?" + silence, logistics).
     Each edge is snapped outward to the nearest speech edge, minus the pad. An
     edge that lands on speech raises - fix the JSON, don't paper over it.

Writes, artifact of record first:
  <output-dir>/edit_points.json          every cut, its audio stats, the parameters
  <output-dir>/studio_cuts.txt           the pre-ticked cuts, last first, for YouTube Studio
  <output-dir>/edit_review/index.html    review page: spectrogram, "after the cut" and
                                         "what gets removed" clips per cut, tick/untick,
                                         copy the final list
Clips and spectrograms (edit_review/media/) are regenerable and gitignored.

The audio is <output-dir>/audio/<id>_16k.wav. If it is missing it gets downloaded
(yt-dlp, audio only, ~80 MB for 1h45m) and converted (ffmpeg, mono 16 kHz).

Usage:
  python scripts/find_edit_points.py --output-dir output/<date>_<slug>_<id>
  python scripts/find_edit_points.py --output-dir ... --report-only   # page from JSON

Runtime (ML48: 1h46m, 120 cuts, this laptop): 1.5-3.5 min wall, and it varied a
lot from run to run - the render loop took 80-137 s although an idle-machine probe
rendered a short cut in ~0.15 s and the 7-min chat cut in ~5 s. --report-only
re-renders the media too, so it costs about the same. Add ~1 min for the
download and conversion on the first run.
"""
import argparse
import html
import json
import logging
import math
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
from matplotlib import colormaps
from PIL import Image
from scipy.signal import butter, sosfilt, spectrogram
from tqdm import tqdm

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LOG_DIR = Path("logs")
SR = 16000
HOP = SR // 100            # 10 ms frames
BLIP_FRAMES = 20           # sounds shorter than 0.2 s inside silence are clicks, not speech
FAINT_FLAG_DB = -50.0      # a filled blip louder than this gets flagged "listen"
CONTEXT_S = 4.0            # seconds of audio either side in the "after the cut" clip
REMOVED_CAP_S = 30.0       # longer removed parts are previewed as first 15 s + last 15 s
SPEC_W, SPEC_H = 960, 130  # spectrogram image size, px
MAGMA = colormaps["magma"]

log = logging.getLogger("find_edit_points")


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "find_edit_points.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def parse_t(text: str) -> float:
    parts = [float(p) for p in text.strip().split(":")]
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def fmt_t(sec: float, digits: int = 1) -> str:
    sign = "-" if sec < 0 else ""
    sec = abs(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    width = 3 + digits if digits else 2
    return f"{sign}{int(h)}:{int(m):02d}:{s:0{width}.{digits}f}"


# ---------------------------------------------------------------- audio

def ensure_wav(out_dir: Path, meta: dict) -> Path:
    audio_dir = out_dir / "audio"
    wav = audio_dir / f"{meta['id']}_16k.wav"
    if wav.exists():
        return wav
    audio_dir.mkdir(exist_ok=True)
    src = sorted(p for p in audio_dir.glob(f"{meta['id']}.*") if p.suffix in (".webm", ".m4a", ".opus", ".mp3"))
    if not src:
        log.info(f"Downloading audio for {meta['id']} (yt-dlp, audio only)")
        subprocess.run(["yt-dlp", "-f", "bestaudio", "-o", str(audio_dir / "%(id)s.%(ext)s"), meta["url"]], check=True)
        src = sorted(p for p in audio_dir.glob(f"{meta['id']}.*") if p.suffix in (".webm", ".m4a", ".opus", ".mp3"))
        if not src:
            raise FileNotFoundError(f"yt-dlp finished but no audio file appeared in {audio_dir}")
    log.info(f"Converting {src[0].name} -> {wav.name} (mono 16 kHz)")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(src[0]),
                    "-ac", "1", "-ar", str(SR), str(wav)], check=True)
    return wav


def frame_levels(x: np.ndarray) -> np.ndarray:
    """Speech-band (100-4000 Hz) power per 10 ms frame, in dB."""
    sos = butter(4, [100, 4000], btype="band", fs=SR, output="sos")
    y = sosfilt(sos, x).astype(np.float32)
    n = len(y) // HOP
    return 10 * np.log10((y[: n * HOP].reshape(n, HOP) ** 2).mean(axis=1) + 1e-12)


def runs(mask: np.ndarray):
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    return np.flatnonzero(d == 1), np.flatnonzero(d == -1)


def sound_mask(db: np.ndarray, thr: float) -> np.ndarray:
    """True where something is audible; blips shorter than 0.2 s count as silence."""
    sound = db > thr
    a, b = runs(sound)
    for s, e in zip(a, b):
        if e - s < BLIP_FRAMES:
            sound[s:e] = False
    return sound


def blip_flags(db: np.ndarray, thr: float, i0: int, i1: int) -> list[str]:
    """Short sounds (filled as silence) inside frames i0..i1 that are loud enough to check."""
    a, b = runs(db[i0:i1] > thr)
    out = []
    for s, e in zip(a, b):
        peak = db[i0 + s: i0 + e].max()
        if peak > FAINT_FLAG_DB:
            out.append(f"short sound at {fmt_t((i0 + s) / 100)} ({peak:.0f} dB) - listen")
    return out


# ---------------------------------------------------------------- cuts

def silence_cuts(db, sound, thr, min_len, pad):
    a, b = runs(~sound)
    cuts = []
    for s, e in zip(a, b):
        run_len = (e - s) / 100
        if run_len < min_len:
            continue
        start, end = s / 100 + pad, e / 100 - pad
        if s == 0:                       # silence at the very start: nothing to keep before it
            start = 0.0
        if e == len(sound):
            end = len(sound) / 100
        cuts.append({
            "source": "silence", "kind": "safe", "default": True,
            "start": round(start, 2), "end": round(end, 2),
            "run_len": round(run_len, 2),
            "reason": f"{run_len:.1f} s of silence",
            "flags": blip_flags(db, thr, s, e),
        })
    return cuts


def snap_content(cut: dict, sound: np.ndarray, duration: float, pad_default: float) -> dict:
    """Move each edge outward to the speech edge next to it, leaving the pad of pause."""
    pad = float(cut.get("pad", pad_default))
    n = len(sound)
    s_req = parse_t(cut["start"])
    e_req = duration if cut["end"] == "end" else parse_t(cut["end"])
    if e_req <= s_req:
        raise ValueError(f"Content cut ends before it starts: {cut}")
    i, j = int(round(s_req * 100)), min(int(round(e_req * 100)), n)
    bad = []
    if i < n and sound[i]:
        bad.append(f"start {cut['start']} is on speech")
    if cut["end"] != "end" and j < n and sound[j]:
        bad.append(f"end {cut['end']} is on speech")
    if bad:
        raise ValueError(f"Content cut edge on speech ({'; '.join(bad)}): {cut['reason']!r}. "
                         f"Move the edge into a pause and rerun.")
    before = np.flatnonzero(sound[:i])
    if len(before):
        last_end = (before[-1] + 1) / 100
        nxt = np.flatnonzero(sound[i:])
        gap = ((i + nxt[0]) / 100 if len(nxt) else duration) - last_end
        start = last_end + min(pad, gap / 2)
    else:
        start = 0.0
    if cut["end"] == "end":
        end = duration
    else:
        after = np.flatnonzero(sound[j:])
        if len(after):
            next_start = (j + after[0]) / 100
            prev = np.flatnonzero(sound[:j])
            gap = next_start - ((prev[-1] + 1) / 100 if len(prev) else 0.0)
            end = next_start - min(pad, gap / 2)
        else:
            end = duration
    return {
        "source": "content", "kind": cut["kind"], "default": bool(cut["default"]),
        "start": round(start, 2), "end": round(end, 2),
        "requested": [cut["start"], cut["end"]],
        "reason": cut["reason"], "flags": [],
    }


def union(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1] + 0.05:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def studio_lines(intervals, duration):
    """Cut list for YouTube Studio, last first. Times rounded inward to 0.1 s."""
    lines = []
    for s, e in reversed(intervals):
        s_r, e_r = math.ceil(s * 10) / 10, math.floor(e * 10) / 10
        if e >= duration - 0.05:
            lines.append(f"TRIM END   keep until {fmt_t(s_r)}   (drops {duration - s:.1f} s)")
        elif s <= 0.05:
            lines.append(f"TRIM START keep from  {fmt_t(e_r)}   (drops {e:.1f} s)")
        else:
            lines.append(f"CUT  {fmt_t(s_r)}  ->  {fmt_t(e_r)}   ({e - s:.1f} s)")
    return lines


# ---------------------------------------------------------------- media

def write_clips(x, cut, media: Path):
    s, e = int(cut["start"] * SR), int(cut["end"] * SR)
    c = int(CONTEXT_S * SR)
    fade = int(0.02 * SR)
    a, b = x[max(0, s - c): s].copy(), x[e: e + c].copy()
    if len(a) > fade and len(b) > fade:
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        a[-fade:] *= ramp[::-1]
        b[:fade] *= ramp
    after = np.concatenate([a, b]) if len(a) + len(b) else np.zeros(SR // 2, np.float32)
    sf.write(media / f"{cut['id']}_after.wav", after, SR, subtype="PCM_16")
    removed = x[s:e]
    if len(removed) > REMOVED_CAP_S * SR:
        half = int(REMOVED_CAP_S / 2 * SR)
        removed = np.concatenate([removed[:half], np.zeros(int(0.4 * SR), np.float32), removed[-half:]])
    peak = float(np.abs(removed).max()) if len(removed) else 0.0
    gain = min(0.5 / peak, 30.0) if peak > 1e-5 else 1.0   # make faint sounds audible, max +30 dB
    sf.write(media / f"{cut['id']}_removed.wav", np.clip(removed * gain, -1, 1), SR, subtype="PCM_16")
    cut["removed_gain_db"] = round(20 * math.log10(gain), 1)


def draw_spectrogram(x, cut, duration, media: Path):
    """0-5 kHz spectrogram of the cut plus 3 s either side, cut shaded red. Drawn
    with numpy + PIL: matplotlib took ~2 s per image here, this takes ~0.05 s."""
    w0 = max(0.0, cut["start"] - 3.0)
    w1 = min(duration, cut["end"] + 3.0)
    seg = x[int(w0 * SR): int(w1 * SR)]
    nper = 512 if (w1 - w0) < 120 else 2048
    f, t, sxx = spectrogram(seg, fs=SR, nperseg=nper, noverlap=nper * 3 // 4)
    sdb = 10 * np.log10(sxx[f <= 5000] + 1e-12)
    vmax = np.percentile(sdb, 99.5)
    norm = np.clip((sdb - (vmax - 70)) / 70, 0, 1)[::-1]          # low frequencies at the bottom
    rgb = (MAGMA(norm)[..., :3] * 255).astype(np.uint8)
    img = np.asarray(Image.fromarray(rgb).resize((SPEC_W, SPEC_H), Image.BILINEAR)).copy()
    span = w1 - w0
    a = int(round((cut["start"] - w0) / span * SPEC_W))
    b = int(round((cut["end"] - w0) / span * SPEC_W))
    red = np.array([217, 0, 18], np.float32)
    img[:, a:b] = (img[:, a:b] * 0.6 + red * 0.4).astype(np.uint8)
    for col in (a, b - 1):
        img[:, max(0, min(SPEC_W - 2, col)): max(0, min(SPEC_W - 2, col)) + 2] = red.astype(np.uint8)
    Image.fromarray(img).save(media / f"{cut['id']}_spec.png", optimize=False)
    cut["spec_window"] = [round(w0, 2), round(w1, 2)]


# ---------------------------------------------------------------- transcript

def load_transcript(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\d+:\d\d(?::\d\d)?)\s+(.*)$", line)
        if m:
            rows.append((parse_t(m.group(1)), m.group(1), m.group(2)))
    return rows


def snippet(rows, s, e):
    inside = [r for r in rows if s - 6 <= r[0] <= e + 4]
    if len(inside) > 10:
        inside = inside[:5] + [None] + inside[-4:]
    return inside


# ---------------------------------------------------------------- page

PAGE_CSS = """
:root { --bg:#fbfaf7; --fg:#1d1d1f; --muted:#6b6b70; --card:#ffffff; --line:#e3e1dc;
        --red:#D90012; --blue:#0033A0; --orange:#F2A800; --absorbed:#f0efe9; }
@media (prefers-color-scheme: dark) {
  :root { --bg:#17171a; --fg:#ececef; --muted:#9a9aa2; --card:#202024; --line:#34343a; --absorbed:#26262b; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.45 system-ui, "Segoe UI", sans-serif; }
main { max-width: 1000px; margin: 0 auto; padding: 16px; }
h1 { font-size: 22px; margin: 8px 0 4px; }
.sub { color: var(--muted); margin: 0 0 12px; }
nav ol { margin: 6px 0 16px; padding-left: 22px; }
nav a { color: var(--blue); }
details { background: var(--card); border:1px solid var(--line); border-radius:10px; margin: 12px 0; padding: 4px 14px 12px; }
summary { cursor: pointer; font-weight: 650; font-size: 17px; padding: 8px 0; }
.stats { position: sticky; top: 0; z-index: 5; background: var(--bg); border-bottom: 2px solid var(--red);
         padding: 8px 0; display:flex; flex-wrap:wrap; gap: 6px 18px; align-items:center; }
.stats b { font-variant-numeric: tabular-nums; }
.card { border-top: 1px solid var(--line); padding: 12px 0; }
.card.off { opacity: .45; }
.card.absorbed { background: var(--absorbed); opacity:.55; }
.head { display:flex; flex-wrap:wrap; gap: 4px 12px; align-items: baseline; }
.head label { font-weight: 650; font-variant-numeric: tabular-nums; cursor:pointer; }
.badge { font-size: 12px; padding: 1px 7px; border-radius: 9px; color:#fff; }
.safe { background: var(--blue); } .judgment { background: var(--orange); color:#1d1d1f; }
.reason { flex-basis: 100%; }
.flag { color: var(--red); font-size: 13px; }
.note { color: var(--muted); font-size: 13px; }
img.spec { width: 100%; height: auto; border-radius: 6px; margin: 6px 0 2px; display:block; }
.players { display:flex; flex-wrap:wrap; gap: 4px 18px; font-size: 13px; color: var(--muted); }
.players audio { height: 32px; width: 290px; max-width: 100%; vertical-align: middle; }
.tx { font-size: 13px; color: var(--muted); margin-top: 6px; }
.tx .t { font-variant-numeric: tabular-nums; margin-right: 8px; }
.tx .in { color: var(--fg); }
textarea { width: 100%; min-height: 260px; font: 13px/1.4 Consolas, monospace; background: var(--card);
           color: var(--fg); border: 1px solid var(--line); border-radius: 6px; padding: 8px; }
button, select { font: inherit; padding: 4px 10px; border-radius: 6px; border: 1px solid var(--line);
                 background: var(--card); color: var(--fg); cursor: pointer; }
ul.how li { margin: 4px 0; }
"""

PAGE_JS = """
const DATA = JSON.parse(document.getElementById('data').textContent);
const KEY = 'edit-points-' + DATA.video_id;
const byId = Object.fromEntries(DATA.cuts.map(c => [c.id, c]));
let ticked = new Set(DATA.cuts.filter(c => c.default).map(c => c.id));
try { const saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) ticked = new Set(saved); } catch (e) {}
const minSel = document.getElementById('minsil');
function fmt(sec, d=1) { const h=Math.floor(sec/3600), m=Math.floor(sec%3600/60), s=sec%60;
  return h + ':' + String(m).padStart(2,'0') + ':' + s.toFixed(d).padStart(d ? 3+d : 2, '0'); }
function active(c) { return ticked.has(c.id) && (c.source !== 'silence' || c.run_len >= +minSel.value); }
function union(iv) { const out=[]; iv.sort((a,b)=>a[0]-b[0]);
  for (const [s,e] of iv) { if (out.length && s <= out[out.length-1][1]+0.05) out[out.length-1][1]=Math.max(out[out.length-1][1],e); else out.push([s,e]); }
  return out; }
function studio(iv) { const D=DATA.duration, L=[];
  for (const [s,e] of [...iv].reverse()) { const sr=Math.ceil(s*10)/10, er=Math.floor(e*10)/10;
    if (e >= D-0.05) L.push('TRIM END   keep until ' + fmt(sr) + '   (drops ' + (D-s).toFixed(1) + ' s)');
    else if (s <= 0.05) L.push('TRIM START keep from  ' + fmt(er) + '   (drops ' + e.toFixed(1) + ' s)');
    else L.push('CUT  ' + fmt(sr) + '  ->  ' + fmt(er) + '   (' + (e-s).toFixed(1) + ' s)'); }
  return L; }
function refresh() {
  const on = DATA.cuts.filter(active);
  const content = on.filter(c => c.source === 'content');
  for (const c of DATA.cuts) {
    const el = document.getElementById('card-' + c.id); if (!el) continue;
    const hidden = c.source === 'silence' && c.run_len < +minSel.value;
    el.style.display = hidden ? 'none' : '';
    el.classList.toggle('off', !ticked.has(c.id));
    const host = c.source === 'silence' && content.find(k => k.start <= c.start && k.end >= c.end);
    el.classList.toggle('absorbed', !!host);
    const n = el.querySelector('.absorbed-note'); if (n) n.textContent = host ? 'inside ' + host.id + ', which is ticked' : '';
    el.querySelector('input').checked = ticked.has(c.id);
  }
  const iv = union(on.map(c => [c.start, c.end]));
  const removed = iv.reduce((a,[s,e]) => a + e - s, 0);
  const cuts = iv.filter(([s,e]) => s > 0.05 && e < DATA.duration - 0.05).length;
  document.getElementById('n-cuts').textContent = cuts;
  document.getElementById('n-trims').textContent = iv.length - cuts;
  document.getElementById('t-removed').textContent = fmt(removed, 0);
  document.getElementById('t-new').textContent = fmt(DATA.duration - removed, 0);
  document.getElementById('export').value = studio(iv).join('\\n');
  try { localStorage.setItem(KEY, JSON.stringify([...ticked])); } catch (e) {}
}
document.querySelectorAll('.card input').forEach(cb => cb.addEventListener('change', e => {
  const id = e.target.dataset.id; if (e.target.checked) ticked.add(id); else ticked.delete(id); refresh(); }));
minSel.addEventListener('change', refresh);
document.getElementById('reset').addEventListener('click', () => {
  ticked = new Set(DATA.cuts.filter(c => c.default).map(c => c.id)); refresh(); });
document.getElementById('copy').addEventListener('click', async () => {
  const ta = document.getElementById('export');
  try { await navigator.clipboard.writeText(ta.value); } catch (e) { ta.select(); document.execCommand('copy'); }
  document.getElementById('copy').textContent = 'Copied'; setTimeout(() => document.getElementById('copy').textContent = 'Copy list', 1500); });
refresh();
"""


def card_html(c, rows):
    esc = html.escape
    badge = f'<span class="badge {c["kind"]}">{"safe" if c["kind"] == "safe" else "your call"}</span>'
    flags = "".join(f'<div class="flag">{esc(f)}</div>' for f in c["flags"])
    tx = []
    for r in snippet(rows, c["start"], c["end"]):
        if r is None:
            tx.append('<div>...</div>')
            continue
        cls = "in" if c["start"] - 1 <= r[0] <= c["end"] else ""
        tx.append(f'<div class="{cls}"><span class="t">{esc(r[1])}</span>{esc(r[2])}</div>')
    gain = c.get("removed_gain_db", 0)
    gain_note = f" (boosted +{gain:.0f} dB)" if gain >= 1 else ""
    capped = " - first 15 s + last 15 s" if c["end"] - c["start"] > REMOVED_CAP_S else ""
    return f"""
<div class="card" id="card-{c['id']}">
  <div class="head">
    <label><input type="checkbox" data-id="{c['id']}"> {c['id']} &nbsp; {fmt_t(c['start'])} &rarr; {fmt_t(c['end'])}</label>
    <span>{c['end'] - c['start']:.1f} s</span> {badge} <span class="note absorbed-note"></span>
    <div class="reason">{esc(c['reason'])}</div>
  </div>
  {flags}
  <img class="spec" loading="lazy" src="media/{c['id']}_spec.png" alt="spectrogram {c['id']}">
  <div class="note">spectrogram 0-5 kHz, {fmt_t(c['spec_window'][0], 0)} to {fmt_t(c['spec_window'][1], 0)}, cut part in red</div>
  <div class="players">
    <span>after the cut <audio controls preload="none" src="media/{c['id']}_after.wav"></audio></span>
    <span>what gets removed{gain_note}{capped} <audio controls preload="none" src="media/{c['id']}_removed.wav"></audio></span>
  </div>
  <div class="tx">{''.join(tx)}</div>
</div>"""


def build_page(data, rows, page: Path):
    content = [c for c in data["cuts"] if c["source"] == "content"]
    sil_long = [c for c in data["cuts"] if c["source"] == "silence" and c["run_len"] >= 5]
    sil_short = [c for c in data["cuts"] if c["source"] == "silence" and c["run_len"] < 5]
    p = data["params"]
    opts = "".join(f'<option value="{v:g}"{" selected" if v == p["min_silence"] else ""}>{v:g} s</option>'
                   for v in sorted({p["min_silence"], 2.0, 3.0, 4.0, 5.0, 8.0}) if v >= p["min_silence"])
    sections = [
        ("how", "How to apply this in YouTube Studio", f"""
<ul class="how">
  <li>Listen to <b>after the cut</b> first: it is {CONTEXT_S:g} s before the cut joined to {CONTEXT_S:g} s after, so you hear exactly how the edit will sound. <b>What gets removed</b> is the cut part itself, boosted so faint sounds are audible.</li>
  <li>Untick anything you want to keep. Ticks are remembered in this browser. The minimum-silence menu at the top hides the shorter silence cuts.</li>
  <li>In Studio: Editor &rarr; Trim &amp; cut. Do the <b>end trim first</b>, then the cuts <b>from the last one to the first</b>, then the start trim. The list in the last section is already in that order. Working backwards means an earlier time never moves, whether or not Studio re-times the timeline after each cut.</li>
  <li>Times are rounded inward to 0.1 s, so a rounded cut never eats into speech. If Studio's boxes only take whole seconds, round the start up and the end down.</li>
  <li>Studio edits can't be undone after saving. Keep your original recording.</li>
  <li>Chapters come after the edit: every cut shifts the times after it.</li>
</ul>
<p class="note">Silence = speech-band level below {p['threshold_db']:.0f} dB (noise floor {p['floor_db']:.0f} dB + 20) for at least {p['min_silence']:g} s; clicks under 0.2 s count as silence. Each silence cut leaves {p['pad']:g} s of pause on both sides. Content cuts come from the transcript, with edges snapped to the speech edge.</p>"""),
        ("content", f"Content cuts ({len(content)})", "".join(card_html(c, rows) for c in content)),
        ("sil-long", f"Silence cuts, 5 s and longer ({len(sil_long)})", "".join(card_html(c, rows) for c in sil_long)),
        ("sil-short", f"Silence cuts, under 5 s ({len(sil_short)})", "".join(card_html(c, rows) for c in sil_short)),
        ("export", "Final cut list for Studio (last first)", """
<p><button id="copy">Copy list</button> <button id="reset">Reset to my picks</button></p>
<textarea id="export" readonly></textarea>"""),
    ]
    toc = "".join(f'<li><a href="#{sid}">{html.escape(title)}</a></li>' for sid, title, _ in sections)
    body = "".join(f'<details open id="{sid}"><summary>{html.escape(title)}</summary>{inner}</details>'
                   for sid, title, inner in sections)
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edit points {html.escape(data['video_id'])}</title>
<style>{PAGE_CSS}</style></head>
<body><main>
<h1>Edit points: {html.escape(data['title'])}</h1>
<p class="sub">{fmt_t(data['duration'], 0)} raw recording, https://youtu.be/{html.escape(data['video_id'])}</p>
<div class="stats">
  <span>cuts <b id="n-cuts"></b> + trims <b id="n-trims"></b></span>
  <span>removed <b id="t-removed"></b></span>
  <span>new length <b id="t-new"></b></span>
  <span>min silence <select id="minsil">{opts}</select></span>
</div>
<nav><ol>{toc}</ol></nav>
{body}
</main>
<script id="data" type="application/json">{blob}</script>
<script>{PAGE_JS}</script>
</body></html>
""", encoding="utf-8")


# ---------------------------------------------------------------- main

def analyse(out_dir: Path, min_silence: float, pad: float) -> dict:
    meta = json.loads((out_dir / "metadata.json").read_text(encoding="utf-8"))
    wav = ensure_wav(out_dir, meta)
    log.info(f"Reading {wav.name} and measuring levels")
    x, sr = sf.read(wav, dtype="float32")
    if sr != SR:
        raise ValueError(f"{wav} is {sr} Hz, expected {SR}")
    duration = len(x) / SR
    db = frame_levels(x)
    floor = float(np.percentile(db, 5))
    thr = floor + 20
    sound = sound_mask(db, thr)
    log.info(f"{duration / 60:.1f} min audio, noise floor {floor:.1f} dB, silence threshold {thr:.1f} dB, "
             f"{100 * (~sound).mean():.0f}% of frames silent")

    cuts = silence_cuts(db, sound, thr, min_silence, pad)
    log.info(f"{len(cuts)} silences >= {min_silence:g} s ({sum(c['run_len'] for c in cuts) / 60:.1f} min raw)")
    cc_path = out_dir / "content_cuts.json"
    if cc_path.exists():
        spec = json.loads(cc_path.read_text(encoding="utf-8"))
        content = [snap_content(c, sound, duration, pad) for c in spec["cuts"]]
        log.info(f"{len(content)} content cuts from {cc_path.name}")
    else:
        log.warning(f"No {cc_path} - silence cuts only. Write it in the LLM stage for content cuts.")
        content = []
    for k, c in enumerate(content, 1):
        c["id"] = f"C{k:02d}"
    for k, c in enumerate(sorted(cuts, key=lambda c: c["start"]), 1):
        c["id"] = f"S{k:03d}"
    all_cuts = content + sorted(cuts, key=lambda c: c["start"])
    return {
        "video_id": meta["id"], "title": meta["title"], "duration": round(duration, 2),
        "params": {"min_silence": min_silence, "pad": pad, "floor_db": round(floor, 1),
                   "threshold_db": round(thr, 1), "blip_s": BLIP_FRAMES / 100},
        "cuts": all_cuts,
    }


def main():
    ap = argparse.ArgumentParser(description="Find cut points in an unedited lecture and build a review page.")
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--min-silence", type=float, default=2.0, help="shortest silence to cut, seconds (default 2.0)")
    ap.add_argument("--pad", type=float, default=0.35, help="pause left on each side of a cut, seconds (default 0.35)")
    ap.add_argument("--report-only", action="store_true", help="rebuild the page and clips from edit_points.json")
    args = ap.parse_args()
    setup_logging()
    t0 = time.time()
    out_dir = args.output_dir
    jpath = out_dir / "edit_points.json"

    if args.report_only:
        data = json.loads(jpath.read_text(encoding="utf-8"))
    else:
        data = analyse(out_dir, args.min_silence, args.pad)
        jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    default_iv = union([[c["start"], c["end"]] for c in data["cuts"] if c["default"]])
    removed = sum(e - s for s, e in default_iv)
    (out_dir / "studio_cuts.txt").write_text(
        f"# {data['title']} - pre-ticked cuts, last first (end trim, cuts, start trim)\n"
        f"# {len(default_iv)} edits, removes {fmt_t(removed, 0)}, new length {fmt_t(data['duration'] - removed, 0)}\n"
        + "\n".join(studio_lines(default_iv, data["duration"])) + "\n", encoding="utf-8")

    review = out_dir / "edit_review"
    media = review / "media"
    media.mkdir(parents=True, exist_ok=True)
    x, _ = sf.read(out_dir / "audio" / f"{data['video_id']}_16k.wav", dtype="float32")
    for c in tqdm(data["cuts"], desc="clips + spectrograms"):
        write_clips(x, c, media)
        draw_spectrogram(x, c, data["duration"], media)
    jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    rows = load_transcript(out_dir / "transcript.txt")
    build_page(data, rows, review / "index.html")
    log.info(f"Pre-ticked: {len(default_iv)} edits removing {removed / 60:.1f} min "
             f"({fmt_t(data['duration'], 0)} -> {fmt_t(data['duration'] - removed, 0)})")
    log.info(f"Wrote {jpath}, {out_dir / 'studio_cuts.txt'}, {review / 'index.html'} in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
