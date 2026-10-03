#!/usr/bin/env python
"""Find edit points (cuts) in an unedited lecture recording and build a review page.

Two sources of cuts:
  1. Silence runs in the audio, >= --min-silence seconds (default 3.0). Each cut
     leaves --pad seconds of pause on both sides, so speech is never clipped.
  2. Content cuts picked from the transcript (<output-dir>/content_cuts.json,
     written by the LLM stage: dead air, "any questions?" + silence, logistics).
     Each edge is snapped outward to the nearest speech edge, minus the pad. An
     edge that lands on speech raises - fix the JSON, don't paper over it.

Writes, artifact of record first:
  <output-dir>/edit_points.json          every cut, its audio stats, the parameters
  <output-dir>/studio_cuts.txt           the pre-ticked cuts in whole frames, numbered as
                                         in Studio, listed last first for entry
  <output-dir>/edit_review/index.html    review page: spectrogram, "after the cut" and
                                         "what gets removed" clips per cut, tick/untick,
                                         copy the final list
  <output-dir>/edit_review/studio.html   the same clips per merged cut, numbered and timed
                                         exactly like Studio's Cut 1..N list
The frame rate comes from yt-dlp once and is kept in edit_points.json.
Clips and spectrograms (edit_review/media/) are regenerable and gitignored.

The audio is <output-dir>/audio/<id>_16k.wav. If it is missing it gets downloaded
(yt-dlp, audio only, ~80 MB for 1h45m) and converted (ffmpeg, mono 16 kHz).

Usage:
  python scripts/find_edit_points.py --output-dir output/<date>_<slug>_<id>
  python scripts/find_edit_points.py --output-dir ... --report-only   # page from JSON
  python scripts/find_edit_points.py --output-dir ... --speech-map 0:16:00 0:16:50
      # where the pauses are, to place content-cut edges (~10-25 s, reads the audio)

Runtime (ML48: 1h46m, 120 cuts, this laptop): 1.5-3.5 min wall, and it varied a
lot from run to run - the render loop took 80-137 s although an idle-machine probe
rendered a short cut in ~0.15 s and the 7-min chat cut in ~5 s. --report-only
re-renders the media too, so it costs about the same. Add ~1 min for the
download and conversion on the first run.
"""
import argparse
import hashlib
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
    sec = round(abs(sec), digits)          # round first, so 59.96 s can't print as ":60.0"
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
    """Put each edge at the speech edge next to it, leaving the pad of pause. Usually
    that widens the cut; an edge asked for within the pad of speech moves inward."""
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


def video_fps(data: dict, url: str) -> int:
    """Frame rate of the uploaded video. Studio's time boxes are H:MM:SS:FF, so cut
    times have to be whole frames. Asked from yt-dlp once, then kept in the JSON."""
    if "fps" not in data:
        out = subprocess.run(["yt-dlp", "--skip-download", "--print", "%(fps)s", url],
                             check=True, capture_output=True, text=True).stdout.strip()
        try:
            data["fps"] = float(out.splitlines()[-1])
        except (ValueError, IndexError):
            raise ValueError(f"yt-dlp gave no frame rate for {url}: {out!r}")
        log.info(f"Video frame rate: {data['fps']:g} fps")
    if data["fps"] != int(data["fps"]):
        raise NotImplementedError(f"{data['fps']} fps: Studio frame numbering for fractional rates is unverified")
    return int(data["fps"])


def studio_cuts(data: dict, fps: int) -> list[dict]:
    """The pre-ticked cuts as Studio lists them: merged, rounded inward to whole frames,
    numbered Cut 1..N by start time (Studio sorts its list that way)."""
    def tc(frame):
        s, ff = divmod(frame, fps)
        h, rem = divmod(s, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}:{ff:02d}"
    ticked = [c for c in data["cuts"] if c["default"]]
    out = []
    for n, (s, e) in enumerate(union([[c["start"], c["end"]] for c in ticked]), 1):
        fs, fe = math.ceil(s * fps - 1e-6), math.floor(e * fps + 1e-6)
        out.append({
            "id": f"studio{n:02d}", "n": n, "start": fs / fps, "end": fe / fps,
            "start_tc": tc(fs), "end_tc": tc(fe),
            "sources": [c["id"] for c in ticked if c["start"] < e and c["end"] > s],
        })
    return out


def studio_lines(scuts):
    """Cut list for YouTube Studio: Studio's numbering, listed last first for entry."""
    return [f"Cut {c['n']:>2}   {c['start_tc']}  ->  {c['end_tc']}   ({c['end'] - c['start']:.2f} s)"
            for c in reversed(scuts)]


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
const KEY = 'edit-points-' + DATA.video_id + '-' + DATA.signature;   // a changed cut list starts from the defaults
const byId = Object.fromEntries(DATA.cuts.map(c => [c.id, c]));
let ticked = new Set(DATA.cuts.filter(c => c.default).map(c => c.id));
try { const saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) ticked = new Set(saved); } catch (e) {}
const minSel = document.getElementById('minsil');
function fmt(sec, d=1) { sec = Math.round(sec * 10**d) / 10**d; const h=Math.floor(sec/3600), m=Math.floor(sec%3600/60), s=sec%60;
  return h + ':' + String(m).padStart(2,'0') + ':' + s.toFixed(d).padStart(d ? 3+d : 2, '0'); }
function active(c) { return ticked.has(c.id) && (c.source !== 'silence' || c.run_len >= +minSel.value); }
function union(iv) { const out=[]; iv.sort((a,b)=>a[0]-b[0]);
  for (const [s,e] of iv) { if (out.length && s <= out[out.length-1][1]+0.05) out[out.length-1][1]=Math.max(out[out.length-1][1],e); else out.push([s,e]); }
  return out; }
function tc(f) { const F = DATA.fps, s = Math.floor(f / F);
  return Math.floor(s/3600) + ':' + String(Math.floor(s%3600/60)).padStart(2,'0') + ':' +
         String(s%60).padStart(2,'0') + ':' + String(f%F).padStart(2,'0'); }
function studio(iv) {   // Studio's Cut 1..N (by start), whole frames rounded inward, listed last first
  const F = DATA.fps;
  const rows = iv.map(([s,e], i) => [i+1, Math.ceil(s*F - 1e-6), Math.floor(e*F + 1e-6)]);
  return rows.reverse().map(([n,fs,fe]) => 'Cut ' + String(n).padStart(2) + '   ' + tc(fs) + '  ->  ' + tc(fe) +
                                         '   (' + ((fe-fs)/F).toFixed(2) + ' s)'); }
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
  document.getElementById('n-cuts').textContent = iv.length;
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
  <li>In Studio: Editor &rarr; Trim &amp; cut &rarr; New Cut for each line of the list in the last section. It uses Studio's own numbering (Cut 1..N by start time) and its <code>H:MM:SS:FF</code> frame times, the same as <code>studio.html</code>, listed last first. Studio keeps the original timeline while you edit, so the times stay valid.</li>
  <li>Times are rounded inward to whole frames, so a cut never eats into speech.</li>
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
    sig = hashlib.sha1(json.dumps([[c["id"], c["start"], c["end"]] for c in data["cuts"]]).encode()).hexdigest()[:12]
    blob = json.dumps({**data, "signature": sig}, ensure_ascii=False).replace("</", "<\\/")
    page.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Edit points {html.escape(data['video_id'])}</title>
<style>{PAGE_CSS}</style></head>
<body><main>
<h1>Edit points: {html.escape(data['title'])}</h1>
<p class="sub">{fmt_t(data['duration'], 0)} raw recording, https://youtu.be/{html.escape(data['video_id'])}</p>
<div class="stats">
  <span>Studio cuts <b id="n-cuts"></b></span>
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

STUDIO_CSS = """
.specwrap { position: relative; cursor: ew-resize; touch-action: none; user-select: none; margin-top: 6px; }
.specwrap img { display: block; width: 100%; height: auto; border-radius: 6px; pointer-events: none; }
.bar { position: absolute; top: -3px; bottom: -3px; width: 3px; margin-left: -1px; background: #fff;
       box-shadow: 0 0 0 1px #000; border-radius: 2px; pointer-events: none; }
.axis { display: flex; justify-content: space-between; font-size: 12px; color: var(--muted);
        font-variant-numeric: tabular-nums; }
.ctl { display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: center; margin: 8px 0 4px; }
.ctl .now { font-variant-numeric: tabular-nums; font-weight: 650; min-width: 90px; }
.play { min-width: 74px; }
.flag button { font-size: 12px; padding: 0 6px; margin-left: 6px; }
.err { color: var(--red); }
nav ol { columns: 2; font-variant-numeric: tabular-nums; }
summary { font-variant-numeric: tabular-nums; }
"""

STUDIO_JS = """
const A = document.getElementById('audio');
const FPS = +document.body.dataset.fps;
let cur = null, raf = null;
function tc(t) { const f = Math.floor(t * FPS + 1e-6), s = Math.floor(f / FPS);
  return Math.floor(s / 3600) + ':' + String(Math.floor(s % 3600 / 60)).padStart(2, '0') + ':' +
         String(s % 60).padStart(2, '0') + ':' + String(f % FPS).padStart(2, '0'); }
const num = (el, k) => parseFloat(el.dataset[k]);
function show(el, t) {
  const w0 = num(el, 'w0'), w1 = num(el, 'w1');
  t = Math.min(w1, Math.max(w0, t));
  el.querySelector('.bar').style.left = (100 * (t - w0) / (w1 - w0)) + '%';
  el.querySelector('.now').textContent = tc(t);
  el.dataset.pos = t;
  return t;
}
function tick() {
  if (!cur) return;
  let t = A.currentTime;
  if (cur.querySelector('.skip').checked && t >= num(cur, 's') && t < num(cur, 'e')) { A.currentTime = num(cur, 'e'); t = num(cur, 'e'); }
  if (t >= num(cur, 'w1')) A.pause();
  show(cur, t);
  if (!A.paused) raf = requestAnimationFrame(tick);
}
function label(el, playing) { el.querySelector('.play').textContent = playing ? 'Pause' : 'Play'; }
function play(el) {
  if (cur && cur !== el) { A.pause(); label(cur, false); }
  cur = el;
  let t = num(el, 'pos');
  if (t >= num(el, 'w1') - 0.05) t = show(el, num(el, 'w0'));
  A.currentTime = t;
  A.play().then(() => { label(el, true); cancelAnimationFrame(raf); raf = requestAnimationFrame(tick); })
          .catch(err => { if (err.name !== 'AbortError') el.querySelector('.err').textContent = 'Could not play: ' + err.message; });  // AbortError = paused before playback began
}
A.addEventListener('pause', () => { if (cur) label(cur, false); cancelAnimationFrame(raf); });
A.addEventListener('error', () => document.querySelectorAll('.err').forEach(e => e.textContent = 'Audio failed to load: ' + A.src));
document.querySelectorAll('details.cut').forEach(el => {
  show(el, num(el, 'w0'));
  el.querySelector('.play').addEventListener('click', () => (cur === el && !A.paused) ? A.pause() : play(el));
  const wrap = el.querySelector('.specwrap');
  const seek = ev => { const r = wrap.getBoundingClientRect();
    const t = show(el, num(el, 'w0') + (ev.clientX - r.left) / r.width * (num(el, 'w1') - num(el, 'w0')));
    if (cur === el && !A.paused) A.currentTime = t; };
  let drag = false;
  wrap.addEventListener('pointerdown', ev => { drag = true; wrap.setPointerCapture(ev.pointerId); seek(ev); });
  wrap.addEventListener('pointermove', ev => { if (drag) seek(ev); });
  wrap.addEventListener('pointerup', () => { drag = false; });
  el.querySelectorAll('.jump').forEach(b => b.addEventListener('click', () => { show(el, parseFloat(b.dataset.t)); play(el); }));
});
document.addEventListener('keydown', ev => {
  if (ev.code === 'Space' && cur && !['INPUT', 'BUTTON'].includes(document.activeElement.tagName)) {
    ev.preventDefault(); A.paused ? play(cur) : A.pause(); } });
"""


def build_studio_page(data, scuts, rows, page: Path, wav: Path):
    """One collapsible section per cut, numbered exactly like Studio's Cut 1..N list.
    One shared player streams the full lecture WAV; each cut's spectrogram has a
    draggable bar, and "skip the cut" plays the window as it will sound after the edit."""
    if not wav.exists():
        raise FileNotFoundError(f"The Studio page plays {wav}, which is missing")
    esc = html.escape
    by_id = {c["id"]: c for c in data["cuts"]}
    sections = []
    for sc in scuts:
        src = [by_id[i] for i in sc["sources"]]
        content = [c for c in src if c["source"] == "content"]
        sil = [c for c in src if c["source"] == "silence"]
        why = [f'<div class="reason"><span class="badge {c["kind"]}">{"safe" if c["kind"] == "safe" else "your call"}</span> '
               f'{esc(c["reason"])}</div>' for c in content]
        if sil and not content:
            why.append(f'<div class="reason">{esc(sil[0]["reason"]) if len(sil) == 1 else f"{len(sil)} silences"}</div>')
        flags = []
        for c in sil:
            for f in c["flags"]:
                m = re.search(r"at (\d+:\d\d:\d\d(?:\.\d)?)", f)
                jump = f'<button class="jump" data-t="{parse_t(m.group(1)) - 1.0:.2f}">play here</button>' if m else ""
                flags.append(f'<div class="flag">{esc(f)}{jump}</div>')
        tx = []
        for r in snippet(rows, sc["start"], sc["end"]):
            if r is None:
                tx.append('<div>...</div>')
                continue
            cls = "in" if sc["start"] - 1 <= r[0] <= sc["end"] else ""
            tx.append(f'<div class="{cls}"><span class="t">{esc(r[1])}</span>{esc(r[2])}</div>')
        w0, w1 = sc["spec_window"]
        title = f"Cut {sc['n']}   {sc['start_tc']} \u2192 {sc['end_tc']}   ({sc['end'] - sc['start']:.1f} s)"
        sections.append((f"cut-{sc['n']}", title, f"""
<details open class="cut" id="cut-{sc['n']}" data-w0="{w0}" data-w1="{w1}" data-s="{sc['start']}" data-e="{sc['end']}">
<summary>{esc(title)}</summary>
{''.join(why)}{''.join(flags)}
<div class="ctl"><button class="play">Play</button><span class="now"></span>
  <label><input type="checkbox" class="skip"> skip the cut (hear the result)</label><span class="err"></span></div>
<div class="specwrap"><img loading="lazy" src="media/{sc['id']}_spec.png" alt="spectrogram cut {sc['n']}"><div class="bar"></div></div>
<div class="axis"><span>{fmt_t(w0)}</span><span>cut part in red, 0-5 kHz; click or drag to move the bar</span><span>{fmt_t(w1)}</span></div>
<div class="tx">{''.join(tx)}</div>
</details>"""))
    removed = sum(c["end"] - c["start"] for c in scuts)
    toc = "".join(f'<li><a href="#{sid}">{esc(title)}</a></li>' for sid, title, _ in sections)
    rel_wav = Path("..") / wav.relative_to(page.parent.parent)
    page.write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Studio cuts {esc(data['video_id'])}</title>
<style>{PAGE_CSS}{STUDIO_CSS}</style></head>
<body data-fps="{data['fps']:g}"><main>
<h1>Studio cuts: {esc(data['title'])}</h1>
<p class="sub">{len(scuts)} cuts, numbered and timed exactly as in YouTube Studio's Trim &amp; cut list
({data['fps']:g} fps, H:MM:SS:FF). Removes {fmt_t(removed, 0)}: {fmt_t(data['duration'], 0)} &rarr; {fmt_t(data['duration'] - removed, 0)}.
Each cut plays its whole segment plus 3 s either side; space bar pauses. To drop one, delete that Cut N in Studio before saving.</p>
<audio id="audio" preload="metadata" src="{rel_wav.as_posix()}"></audio>
<nav><ol>{toc}</ol></nav>
{''.join(inner for _, _, inner in sections)}
</main>
<script>{STUDIO_JS}</script>
</body></html>
""", encoding="utf-8")


def levels(out_dir: Path):
    """Audio, 10 ms speech-band levels, the silence threshold (noise floor + 20 dB)
    and the sound mask - shared by the analysis and --speech-map."""
    meta = json.loads((out_dir / "metadata.json").read_text(encoding="utf-8"))
    wav = ensure_wav(out_dir, meta)
    log.info(f"Reading {wav.name} and measuring levels")
    x, sr = sf.read(wav, dtype="float32")
    if sr != SR:
        raise ValueError(f"{wav} is {sr} Hz, expected {SR}")
    db = frame_levels(x)
    floor = float(np.percentile(db, 5))
    thr = floor + 20
    sound = sound_mask(db, thr)
    log.info(f"{len(x) / SR / 60:.1f} min audio, noise floor {floor:.1f} dB, silence threshold {thr:.1f} dB, "
             f"{100 * (~sound).mean():.0f}% of frames silent")
    return meta, x, db, floor, thr, sound


def speech_map(out_dir: Path, start: str, end: str) -> None:
    """Print where the speech and the pauses are, 0.1 s per character, so a content
    cut's edges can be put inside a pause. '#' sound, '.' a click or short sound
    (under 0.2 s, counts as silence), '_' silence. One line per 10 s."""
    _, _, db, _, thr, sound = levels(out_dir)
    i0, i1 = int(parse_t(start) * 100), min(int(parse_t(end) * 100), len(sound))
    if i1 <= i0:
        raise ValueError(f"--speech-map end {end} is not after start {start}")
    for row in range(i0 - i0 % 1000, i1, 1000):
        chars = []
        for k in range(row, min(row + 1000, i1), 10):
            if k < i0:
                chars.append(" ")
            elif sound[k:k + 10].any():
                chars.append("#")
            elif (db[k:k + 10] > thr).any():
                chars.append(".")
            else:
                chars.append("_")
        line = "".join(chars)
        print(f"{fmt_t(row / 100, 0)}  " + "|".join(line[j:j + 10] for j in range(0, len(line), 10)))


def analyse(out_dir: Path, min_silence: float, pad: float) -> dict:
    meta, x, db, floor, thr, sound = levels(out_dir)
    duration = len(x) / SR

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
    ap.add_argument("--min-silence", type=float, help="shortest silence to cut, seconds (default 3.0)")
    ap.add_argument("--pad", type=float, help="pause left on each side of a cut, seconds (default 0.35)")
    ap.add_argument("--report-only", action="store_true", help="rebuild the page and clips from edit_points.json")
    ap.add_argument("--speech-map", nargs=2, metavar=("START", "END"),
                    help="print speech/pause map between two times (H:MM:SS) and exit")
    args = ap.parse_args()
    if args.speech_map:
        setup_logging()
        speech_map(args.output_dir, *args.speech_map)
        return
    if args.report_only and (args.min_silence is not None or args.pad is not None):
        ap.error("--min-silence/--pad only apply to a fresh analysis; --report-only reuses edit_points.json as is")
    args.min_silence = 3.0 if args.min_silence is None else args.min_silence   # the user's pick, ML48
    args.pad = 0.35 if args.pad is None else args.pad
    setup_logging()
    t0 = time.time()
    out_dir = args.output_dir
    jpath = out_dir / "edit_points.json"

    if args.report_only:
        data = json.loads(jpath.read_text(encoding="utf-8"))
    else:
        data = analyse(out_dir, args.min_silence, args.pad)
        jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    fps = video_fps(data, f"https://youtu.be/{data['video_id']}")
    scuts = studio_cuts(data, fps)
    removed = sum(c["end"] - c["start"] for c in scuts)
    (out_dir / "studio_cuts.txt").write_text(
        f"# {data['title']} - pre-ticked cuts, numbered as in Studio, listed last first for entry\n"
        f"# {len(scuts)} cuts at {fps} fps, removes {fmt_t(removed, 0)}, new length {fmt_t(data['duration'] - removed, 0)}\n"
        + "\n".join(studio_lines(scuts)) + "\n", encoding="utf-8")

    review = out_dir / "edit_review"
    media = review / "media"
    media.mkdir(parents=True, exist_ok=True)
    x, _ = sf.read(out_dir / "audio" / f"{data['video_id']}_16k.wav", dtype="float32")
    for c in tqdm(data["cuts"], desc="clips + spectrograms"):
        write_clips(x, c, media)
        draw_spectrogram(x, c, data["duration"], media)
    for c in scuts:                       # the Studio page plays the full WAV, so no clips
        draw_spectrogram(x, c, data["duration"], media)
    data["studio_cuts"] = scuts
    jpath.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    rows = load_transcript(out_dir / "transcript.txt")
    build_page(data, rows, review / "index.html")
    build_studio_page(data, scuts, rows, review / "studio.html", out_dir / "audio" / f"{data['video_id']}_16k.wav")
    log.info(f"Pre-ticked: {len(scuts)} Studio cuts removing {removed / 60:.1f} min "
             f"({fmt_t(data['duration'], 0)} -> {fmt_t(data['duration'] - removed, 0)})")
    log.info(f"Wrote {jpath}, {out_dir / 'studio_cuts.txt'}, {review / 'index.html'}, "
             f"{review / 'studio.html'} in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
