"""Remove the mains buzz from the Vahagn pieces where it is (the user picked "notches + the denoise that learns from
your sample" on output/vahagn_linalg_overview/audio/dehum_samples.html, 2026-10-27).

    python scripts/non_essential/vahagn_dehum.py 23.3.b            # one piece
    python scripts/non_essential/vahagn_dehum.py --all             # every piece whose buzz map is not empty

Per piece, from the raw recording:
1. buzz map: the 150-600 Hz band in the quietest 10% of 128 ms frames of each 10 s window, vs the speech level (90th
   pct): over -55 dB = buzz (buzz -37..-48, clean -73..-77, _knowledge/vahagn_linalg/buzz_band.json); gaps up to 20 s
   filled, runs under 20 s dropped.
2. noise sample: the quietest steady 3.4 s inside the buzz (2 s if no 3.4 s is steady) that holds the buzz (not a
   dropout), 15 dB+ under the speech level
   (by level, not by find_edit_points' pause mask, whose one threshold counts the buzz as sound in a piece with buzz in
   part of it).
3. notches (Q 30) at every narrow peak under 1.2 kHz standing 12 dB+ over its +-15 Hz surroundings, re-fitted per
   30 s on the nearest steady pure-buzz 2 s and moved to where the chunk's own quietest 1 s blocks have each line (the
   hum drifts: 23.3.b 73.6 Hz at 3:01, 76.2 Hz at 7:18), forward only
   (zero-phase rang before each sound: an echo the user heard), chunks cross-faded over 1 s overlaps.
4. two full-length tracks: buzz chain = notches + 80 Hz low cut + afftdn 20 dB learning the sample (the sample is put
   in front, sampled with afftdn's sample_noise, then trimmed off); clean chain = the uploaded light chain (80 Hz low
   cut + afftdn 12 dB tracking). The output takes the buzz track inside the buzz map, the clean one elsewhere, joined
   at the quietest moment within 10 s of each boundary with 50 ms crossfades.
5. -16 LUFS, peaks limited to -1 dBFS, 48 kHz AAC, picture copied; lengths and picture checked; the buzz measured
   again on the result.
Files: <raw folder>/audio_dehum/VidSection <section> dehum.mp4; results in _knowledge/vahagn_linalg/dehum.json.
Expected: ~3 min per 20 min piece (decode, two filter passes, AAC encode), ~1 h for the 18 with buzz. One process.
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
from scipy.ndimage import median_filter

REPO = Path(__file__).resolve().parents[2]
RAW =Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\vahagn_linalg")
OUT = RAW / "audio_dehum"
FFMPEG = r"C:\Users\hayk_\tools\ffmpeg-9\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"   # as vahagn_audio_fix.py
SR = 32000                                    # the recordings' own rate; 48 kHz only at the final encode
N, HOP = 4096, 2048                           # 128 ms frames at 32 kHz
WIN_S, BUZZ_DB, MIN_RUN_S = 10, -55.0, 20
CLEAN = "highpass=f=80,afftdn=nr=12:nf=-50:tn=1"
LIMIT = "alimiter=limit=0.891:level=0"
(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler(REPO / "logs/vahagn_dehum.log", encoding="utf-8")])
log = logging.getLogger("vahagn_dehum")


def ff(*args, capture=False):
    r = subprocess.run([FFMPEG, "-v", "error", "-nostats", *map(str, args)], capture_output=True,
                       text=not capture, encoding=None if capture else "utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {r.stderr[-1500:] if not capture else r.stderr.decode()[-1500:]}")
    return r.stdout


def decode(path: Path) -> np.ndarray:
    return np.frombuffer(ff("-i", path, "-vn", "-ac", "1", "-ar", SR, "-f", "f32le", "-", capture=True), np.float32)


def frames_db(x: np.ndarray, band: tuple[float, float] | None) -> np.ndarray:
    f = np.fft.rfftfreq(N, 1 / SR)
    sel = slice(None) if band is None else (f >= band[0]) & (f <= band[1])
    nf = (len(x) - N) // HOP
    out, win = np.empty(nf, np.float32), np.hanning(N).astype(np.float32)
    for b0 in range(0, nf, 3000):
        b1 = min(nf, b0 + 3000)
        s = np.abs(np.fft.rfft(x[np.arange(N)[None, :] + HOP * np.arange(b0, b1)[:, None]] * win, axis=1)) ** 2
        out[b0:b1] = 10 * np.log10(s[:, sel].sum(axis=1) + 1e-12)
    return out


FT = HOP / SR                                 # seconds per frame


def buzz_level(band: np.ndarray, full: np.ndarray) -> list[float]:
    """Per WIN_S window: the 150-600 Hz band of the quietest 10% of frames, minus the speech level (dB)."""
    speech, w = np.percentile(full, 90), int(WIN_S / FT)
    return [float(np.percentile(band[i:i + w], 10) - speech) for i in range(0, len(band), w)]


def runs(mask: np.ndarray) -> list[tuple[int, int]]:
    e = np.flatnonzero(np.diff(np.r_[0, mask.astype(np.int8), 0]))
    return list(zip(e[::2], e[1::2]))


def buzz_map(levels: list[float], duration: float) -> list[list[float]]:
    on = np.array(levels) > BUZZ_DB
    k = MIN_RUN_S // WIN_S
    for a, b in runs(~on):                                  # fill gaps of up to MIN_RUN_S between buzz
        if b - a <= k and a > 0 and b < len(on):
            on[a:b] = True
    for a, b in runs(on):                                   # then drop buzz shorter than MIN_RUN_S
        if b - a < k:
            on[a:b] = False
    return [[float(a * WIN_S), float(min(duration, b * WIN_S))] for a, b in runs(on)]


def quietest_moment(full: np.ndarray, t: float, reach: float = 10.0) -> float:
    """The quietest 0.4 s within +-reach s of t, for a join. By level, not by find_edit_points' pause mask: in a
    piece with buzz in part of it, that mask's one threshold counts the buzz as sound (24.1: no pause found in the
    buzz, 2026-10-27)."""
    lo, hi = max(0, int((t - reach) / FT)), min(len(full), int((t + reach) / FT))
    sm = np.convolve(full[lo:hi], np.ones(3) / 3, mode="same")
    return round((lo + int(np.argmin(sm))) * FT + N / 2 / SR, 2)


def noise_sample(regions, full: np.ndarray, band: np.ndarray, buzz_db: float,
                 lengths: tuple[float, ...] = (3.4, 2.0)) -> tuple[float, float]:
    """The quietest window inside the buzz, which must be pure buzz: steady (std of its 128 ms frame levels 2 dB
    or less; speech swings far more), 15 dB+ under the speech level, and holding the buzz (its 150-600 Hz level at
    most 6 dB under the piece's median buzz `buzz_db`, vs speech). Steadiness, not distance from speech, is the
    test: 23.3.b's buzz is so loud that its pure-buzz stretch is only 20.7 dB under speech, std 0.2 dB (the user's mark
    in 28.3.a: 34.8 dB under, std 1.0). The buzz test came after the batch of 2026-10-27: a dropout is steady and
    quiet too, so 28.3.a learned digital silence (band -163 dB vs a buzz at -42) and 28.1.a a stretch where the buzz is
    weak (-66 vs -42), and their worst minutes stayed at -45.5 and -51.2 dB. 3.4 s (the user's mark) first, then 2 s:
    24.4's pauses are short, so its steadiest 3.4 s had std 2.06 dB while 80 windows of 2 s passed (best 0.97 dB); a
    pure 2 s sample beats a 3.4 s one with a breath in it."""
    speech, first_best = np.percentile(full, 90), None
    for length in lengths:
        n = int(length / FT)
        mean = np.convolve(full, np.ones(n) / n, mode="valid")          # mean[i] = frames i .. i+n-1
        std = np.sqrt(np.maximum(np.convolve(full ** 2, np.ones(n) / n, mode="valid") - mean ** 2, 0))
        bmean = np.convolve(band, np.ones(n) / n, mode="valid")
        ok = np.zeros(len(mean), bool)
        for r0, r1 in regions:
            ok[int(r0 / FT):max(int(r0 / FT), int(r1 / FT) - n)] = True
        # the quietest among the STEADY windows: the quietest window overall can straddle a dropout (22.1: 41 dB under
        # speech but a frame std of 15.8 dB, 2026-10-27)
        quiet = ok & (mean <= speech - 15) & (bmean >= speech + buzz_db - 6)
        good = quiet & (std <= 2.0)
        if first_best is None:
            first_best = float(std[quiet].min()) if quiet.any() else float("nan")
        if good.any():
            if length != lengths[0]:
                log.warning(f"no steady {lengths[0]} s of pure buzz (steadiest std {first_best:.2f} dB), noise sample "
                            f"shortened to {length} s")
            i = int(np.argmin(np.where(good, mean, np.inf)))
            return round(i * FT, 2), length
    raise ValueError(f"no steady pure-buzz window of {' or '.join(map(str, lengths))} s inside the buzz map {regions} "
                     "(frame std 2 dB or less, 15 dB+ under speech, the buzz in it) to learn from")


def refresh_points(regions, full: np.ndarray, length: float = 2.0, every: float = 60.0) -> list[tuple[float, float]]:
    """One steady pure-buzz window per `every` s inside the buzz (same test as noise_sample), where the denoise
    re-learns the noise. The buzz drifts: with one sample (23.3.b at 3:01) the minute of the sample came out at -68.7 dB
    vs speech and the others at -56..-58 (the user still heard it in minute 7); at nr 30 still -57..-60."""
    n = int(length / FT)
    mean = np.convolve(full, np.ones(n) / n, mode="valid")
    sq = np.convolve(full ** 2, np.ones(n) / n, mode="valid")
    std = np.sqrt(np.maximum(sq - mean ** 2, 0))
    speech = np.percentile(full, 90)
    good = (std <= 2.0) & (mean <= speech - 15)
    out = []
    for r0, r1 in regions:
        t = r0
        while t < r1 - length:
            lo, hi = int(t / FT), min(len(mean), int(min(t + every, r1 - length) / FT))
            cand = np.flatnonzero(good[lo:hi])
            if len(cand):
                i = lo + cand[int(np.argmin(mean[lo + cand]))]
                out.append((round(i * FT, 2), length))
            t += every
    return out


def heights(s: np.ndarray, nfft: int) -> tuple[np.ndarray, np.ndarray]:
    """30-1200 Hz of a dB spectrum, as height over its +-15 Hz surroundings."""
    f = np.fft.rfftfreq(nfft, 1 / SR)
    keep = (f > 30) & (f < 1200)
    return f[keep], s[keep] - median_filter(s[keep], size=int(30 / (SR / nfft)) | 1)


def pick_peaks(fk: np.ndarray, h: np.ndarray) -> list[float]:
    """Every narrow peak standing 12 dB+ over its +-15 Hz surroundings, at least 6 Hz apart."""
    out = []
    for i in np.argsort(-h):
        if h[i] < 12:
            break
        if all(abs(fk[i] - o) > 6 for o in out):
            out.append(float(fk[i]))
    return sorted(round(v, 1) for v in out)


def notches(x: np.ndarray, start: float, length: float) -> list[float]:
    """The peaks of one pure-buzz sample."""
    seg = x[int(start * SR):int((start + length) * SR)]
    nfft = 2 ** 20
    return pick_peaks(*heights(10 * np.log10(np.abs(np.fft.rfft(seg * np.hanning(len(seg)), nfft)) ** 2 + 1e-20), nfft))


def quiet_heights(x: np.ndarray, a: int, b: int, block: int = 32768, share: float = 0.2):
    """heights() of the averaged spectrum of the quietest 1 s blocks of x[a:b] (at least 3). Needs no pause: speech in
    those blocks changes pitch and smears out in the average, while the hum lines stay where they are."""
    n = (b - a) // block
    if n < 3:
        raise ValueError(f"chunk {a / SR:.1f}-{b / SR:.1f} s is under 3 blocks of {block / SR:.2f} s")
    blocks = x[a:a + n * block].reshape(n, block).astype(np.float64)
    q = blocks[np.argsort((blocks ** 2).mean(axis=1))[:max(3, int(n * share))]]
    nfft = 2 ** 19                                                     # zero-padded: 0.06 Hz bins
    return heights(10 * np.log10((np.abs(np.fft.rfft(q * np.hanning(block), nfft, axis=1)) ** 2).mean(axis=0) + 1e-20), nfft)


def refine(template: list[float], fk: np.ndarray, h: np.ndarray, tol: float = 0.025) -> list[float]:
    """Each template line moved to where the chunk has it (the highest point within +-2.5%, at least +-1 Hz, if it
    stands 6 dB+ there), plus the chunk's own 12 dB+ lines the template lacks. Tested 2026-10-27 on 28.3.a, 28.1.a and
    23.3.b: the template alone (the nearest steady 2 s) missed where the hum had moved since the sample (28.3.a minute 3:
    49.2 Hz vs the sample's 48.2, 9 Hz off at the 9th harmonic, -45.5 dB vs speech); the chunk's quiet blocks alone found
    only 0-3 lines in some chunks, speech hiding the rest (28.1.a minute 4: 2 lines, -44.3 dB)."""
    out = []
    for p in template:
        sel = np.flatnonzero(np.abs(fk - p) <= max(1.0, tol * p))
        j = sel[int(np.argmax(h[sel]))] if len(sel) else None
        out.append(round(float(fk[j]), 1) if j is not None and h[j] >= 6 else p)
    out += [p for p in pick_peaks(fk, h) if all(abs(p - o) > 6 for o in out)]
    return sorted(set(out))


def tracking_notches(x: np.ndarray, full: np.ndarray, regions, chunk: float = 30.0, overlap: float = 1.0,
                     q: float = 30.0, zero_phase: bool = False):
    """Notches that follow the hum as it drifts: per `chunk` s, the peaks of the chunk's steadiest pure-buzz 2 s (else
    the nearest chunk's; refresh_points' test), each moved to where the chunk's own quiet blocks have it (refine),
    applied to that chunk only, chunks overlapping by `overlap` s and cross-faded.
    One set of notches from one sample missed: 23.3.b's hum moves from 73.6 Hz (3:01) to 76.2 Hz (7:18), so at the 4th
    harmonic the notch sat 11 Hz off and the peaks after processing stood as high as before (+47 vs +46 dB, 2026-10-27).
    Returns the notched signal and per chunk (start, sample used, peaks)."""
    from scipy.signal import iirnotch, sosfilt, sosfiltfilt, tf2sos
    pts = dict(refresh_points(regions, full, length=2.0, every=chunk))     # start -> length, one per chunk at most
    starts = sorted(pts)
    if not starts:
        raise ValueError("no steady pure-buzz moment anywhere in the buzz to fit the notches on")
    y, w_sum = np.zeros_like(x), np.zeros(len(x), np.float32)
    used, step, ov = [], int(chunk * SR), int(overlap * SR)
    for c0 in range(0, len(x), step):
        if c0 and len(x) - c0 < ov:     # the previous chunk already runs to the end (24.4: a 1.64 s tail, shorter than the ramp)
            break
        a, b = max(0, c0 - ov), min(len(x), c0 + step + ov)
        mid = (c0 + step / 2) / SR
        s = min(starts, key=lambda t: abs(t - mid))                       # this chunk's sample, else the nearest one
        # a tail chunk under 3 s is looked at over the last 3 s
        peaks = refine(notches(x, s, pts[s]), *quiet_heights(x, min(c0, max(0, len(x) - 3 * 32768)), min(len(x), c0 + step)))
        used.append((round(c0 / SR, 1), round(s, 1), peaks))
        seg = x[a:b].astype(np.float64)
        if peaks:
            sos = np.vstack([tf2sos(*iirnotch(p, q, SR)) for p in peaks if p < SR / 2])
            if zero_phase:   # forward-backward: no phase shift, but sharp notches then ring BEFORE each sound too
                seg = sosfiltfilt(sos, seg)
            else:            # forward only, started 2 s early so the filters have settled when the chunk begins
                w0 = max(0, a - 2 * SR)
                seg = sosfilt(sos, x[w0:b].astype(np.float64))[a - w0:]
        w = np.ones(b - a, np.float32)                                    # triangular ramps over the overlaps
        if a > 0:
            w[:2 * ov] = np.linspace(0, 1, 2 * ov)
        if b < len(x):
            w[-2 * ov:] = np.linspace(1, 0, 2 * ov)
        y[a:b] += (seg * w).astype(np.float32)
        w_sum[a:b] += w
    return y / np.maximum(w_sum, 1e-6), used


def lufs(path: Path) -> float:
    r = subprocess.run([FFMPEG, "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8")
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def dehum(sec: str, nr: int = 20, q: float = 30.0, zero_phase: bool = False, relearn: bool = False, tag: str = "",
          plain: bool = False) -> dict:
    t0 = time.time()
    log.info(f"{sec}: starting")
    raw = next(iter([*RAW.glob(f"Videos Part */VidSection {sec}.mp4"), *RAW.glob(f"already_on_youtube/VidSection {sec}.mp4")]))
    x = decode(raw)
    dur = len(x) / SR
    full, band = frames_db(x, None), frames_db(x, (150, 600))
    levels = buzz_level(band, full)
    regions = buzz_map(levels, dur)
    if not regions:
        log.info(f"{sec}: no buzz, nothing to do")
        return {"section": sec, "regions": []}
    whole = len(regions) == 1 and regions[0][0] == 0 and regions[0][1] >= dur - WIN_S
    if not whole:                                           # joins at the quietest moment near each boundary
        regions = [[0.0 if a == 0 else quietest_moment(full, a), dur if b >= dur - 1 else quietest_moment(full, b)]
                   for a, b in regions]
    inside_lv = [lv for i, lv in enumerate(levels) if any(r0 <= i * WIN_S < r1 for r0, r1 in regions)]
    ns, nl = noise_sample(regions, full, band, float(np.median(inside_lv)))
    del band
    xn, used = tracking_notches(x, full, regions, q=q, zero_phase=zero_phase)
    log.info(f"{sec}: buzz {'everywhere' if whole else regions}; noise sample {ns:.1f}+{nl:.1f} s; notches re-fitted "
             f"per 30 s on {len({s for _, s, _ in used})} samples, refined on each chunk, {min(len(p) for _, _, p in used)}-"
             f"{max(len(p) for _, _, p in used)} per chunk")
    OUT.mkdir(exist_ok=True)
    tmp_n, tmp_x, tmp_b, tmp_c, tmp_m = (OUT / f"_tmp_{sec}_{k}.wav" for k in ("noise", "notched", "buzz", "clean", "mix"))
    sf.write(tmp_x, xn, SR, subtype="FLOAT")
    sf.write(tmp_n, xn[int(ns * SR):int(ns * SR) + int(nl * SR)], SR, subtype="FLOAT")  # its own file: no buffering
    del xn
    refresh = refresh_points(regions, full) if relearn else []
    cmds = [f"0.2 afftdn sn start;{nl - 0.2:.2f} afftdn sn stop"] + \
           [f"{nl + s + 0.1:.2f} afftdn sn start;{nl + s + l - 0.1:.2f} afftdn sn stop" for s, l in refresh]
    learn = f"asendcmd=c='{';'.join(cmds)}'"
    den = "afftdn=nr=12:nf=-50:tn=1" if plain else f"{learn},afftdn=nr={nr}:nf=-50:tn=0"   # plain: the #38 light denoise
    log.info(f"{sec}: the denoise re-learns the noise at {len(refresh)} steady moments in the buzz")
    fc = (f"[0:a]asetpts=PTS-STARTPTS[n];[1:a]asetpts=PTS-STARTPTS[s];"
          f"[n][s]concat=n=2:v=0:a=1,highpass=f=80,{den},"
          f"atrim=start={nl},asetpts=PTS-STARTPTS[o]")
    ff("-y", "-i", tmp_n, "-i", tmp_x, "-filter_complex", fc, "-map", "[o]", "-ac", 1, "-c:a", "pcm_f32le", tmp_b)
    yb, _ = sf.read(tmp_b, dtype="float32")
    if whole:
        y = yb
    else:
        ff("-y", "-i", raw, "-vn", "-af", f"aresample={SR},{CLEAN}", "-ac", 1, "-c:a", "pcm_f32le", tmp_c)
        yc, _ = sf.read(tmp_c, dtype="float32")
        n = min(len(yb), len(yc))
        w = np.zeros(n, np.float32)
        ramp = int(0.05 * SR)
        for a, b in regions:
            i, j = int(a * SR), int(b * SR)
            w[i:j] = 1
            if i > 0:
                w[max(0, i - ramp // 2):i + ramp // 2] = np.linspace(0, 1, len(w[max(0, i - ramp // 2):i + ramp // 2]))
            if j < n:
                w[j - ramp // 2:min(n, j + ramp // 2)] = np.linspace(1, 0, len(w[j - ramp // 2:min(n, j + ramp // 2)]))
        y = w * yb[:n] + (1 - w) * yc[:n]
        del yc
    del yb
    sf.write(tmp_m, y, SR, subtype="FLOAT")
    gain = -16.0 - lufs(tmp_m)
    dest = OUT / f"VidSection {sec} dehum{' ' + tag if tag else ''}.mp4"
    ff("-y", "-i", raw, "-i", tmp_m, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", f"volume={gain:.2f}dB,{LIMIT}",
       "-ar", 48000, "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", dest)
    for p in (tmp_n, tmp_x, tmp_b, tmp_c, tmp_m):           # this run's own intermediates, by their literal names
        if p.exists():
            p.unlink()
    probe = lambda p: json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,"
                                                 "width,height,duration", "-of", "json", str(p)], capture_output=True,
                                                text=True, check=True).stdout)["streams"]
    a, b = {s["codec_type"]: s for s in probe(raw)}, {s["codec_type"]: s for s in probe(dest)}
    if (a["video"]["width"], a["video"]["height"]) != (b["video"]["width"], b["video"]["height"]) or \
            abs(float(a["video"]["duration"]) - float(b["video"]["duration"])) > 0.05 or \
            abs(float(a["audio"]["duration"]) - float(b["audio"]["duration"])) > 0.1:
        raise RuntimeError(f"{sec}: picture or length changed: {a} -> {b}")
    y_out = decode(dest)
    after = buzz_level(frames_db(y_out, (150, 600)), frames_db(y_out, None))
    del y_out
    inside = [i for i in range(len(levels)) if any(r0 <= i * WIN_S < r1 for r0, r1 in regions)]
    res = {"section": sec, "regions": regions, "whole": whole, "noise_sample": [ns, nl], "notches_per_chunk": used,
           "gain_db": round(gain, 2), "lufs_out": round(lufs(dest), 1),
           "buzz_before_db": round(float(np.median([levels[i] for i in inside])), 1),
           "buzz_after_db": round(float(np.median([after[i] for i in inside if i < len(after)])), 1),
           "output": str(dest), "seconds": round(time.time() - t0)}
    log.info(f"{sec}: buzz {res['buzz_before_db']} -> {res['buzz_after_db']} dB vs speech inside the buzz map, "
             f"{res['lufs_out']} LUFS, {res['seconds']} s -> {dest.name}")
    return res


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--nr", type=int, default=20, help="strength of the learning denoise in dB (the user picked 20)")
    ap.add_argument("--q", type=float, default=30.0, help="notch sharpness")
    ap.add_argument("--zero-phase", action="store_true", help="forward-backward notches (rang before sounds: the user heard an echo)")
    ap.add_argument("--relearn", action="store_true", help="the denoise re-learns the noise once a minute")
    ap.add_argument("--plain-denoise", action="store_true", help="after the notches, the #38 light denoise instead of the learning one")
    ap.add_argument("--tag", default="", help="suffix for the output file and the results key, for test variants")
    args = ap.parse_args()
    band = json.loads((REPO / "_knowledge/vahagn_linalg/buzz_band.json").read_text(encoding="utf-8"))
    secs = args.sections or [s for s, v in band.items() if any(m > BUZZ_DB for m in v["per_min"])]
    res_path = REPO / "_knowledge/vahagn_linalg/dehum.json"
    allres = json.loads(res_path.read_text(encoding="utf-8")) if res_path.exists() else {}
    t0 = time.time()
    for i, s in enumerate(secs, 1):
        allres[f"{s} {args.tag}" if args.tag else s] = dehum(s, args.nr, args.q, args.zero_phase, args.relearn, args.tag, args.plain_denoise)
        res_path.write_text(json.dumps(allres, ensure_ascii=False, indent=1), encoding="utf-8")
        el = time.time() - t0
        log.info(f"{i}/{len(secs)} done, {el / 60:.1f} min elapsed, ~{el / i * (len(secs) - i) / 60:.1f} min left")


if __name__ == "__main__":
    main()
