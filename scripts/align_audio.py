"""Find where a camera recording sits inside a separate audio recording (a lecturer's voice recorder, a
phone's mp3), to the millisecond, and whether the two clocks drift apart.

Run:  python scripts/align_audio.py --camera <video.MOV> --audio <recorder.mp3> --approx <seconds>
      [--points 7] [--window 30] [--search 3] [-o align.json]
Expected wall-clock: ~20-40 s (decodes 7 x ~36 s of audio from each file at 8 kHz; one CPU core).

--approx is the rough offset (camera t=0 is at --approx seconds in the audio file), e.g. from a 1 s
loudness-envelope match. At each of --points camera times the script cross-correlates --window seconds of
camera sound against the audio file within +-search seconds of the rough offset, then fits
offset(t) = offset0 + drift * t. Output: JSON with every point (offset, correlation peak, and its z-score
against all other lags in the search range) and the fit. Two different microphones correlate weakly
(normalised peaks of 0.13-0.30 on Դաս 7, all at the same offset), so a match is judged by how far its
peak stands out: z < MIN_Z is reported and left out of the fit; fewer than 3 good points is an error,
since a fit through 2 points cannot be checked.

How exact it is: Դաս 7 (camera near the front) fits a straight line to within 3 ms. Դաս 6 (a classmate's
phone in the room, the recorder near the lecturer) scatters +-33 ms around the line whatever the window
(30 s or 60 s, 7 or 15 points): the camera hears the lecturer distance / 343 m/s late, and that changes
as he walks between the board and the screen. Both are inside lip-sync tolerance (~45 ms audio early).
"""
import argparse
import json
import logging
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stdout),
                              logging.FileHandler("logs/align_audio.log", encoding="utf-8")])
log = logging.getLogger(__name__)

SR = 8000
MIN_Z = 8.0


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True, check=True).stdout
    return float(out)


def pcm(path: Path, start: float, length: float) -> np.ndarray:
    """Mono float32 samples at SR from the first audio stream, [start, start + length), by input seeking,
    as render_lecture.py reads the files. Decoding Դաս 6's 17 h recorder mp3 from its start instead gave the
    same offsets to 0.1 ms at all 7 points (2026-10-24; its +-33 ms scatter is room acoustics, see above)
    and took 88 s instead of 34 s."""
    res = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", str(path), "-t", f"{length:.3f}",
                          "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True)
    x = np.frombuffer(res.stdout, dtype=np.float32)
    if len(x) < SR * length * 0.95:
        raise RuntimeError(f"{path}: got {len(x) / SR:.1f} s of audio at {start:.1f} s, wanted {length:.1f} s")
    return x - x.mean()


def best_lag(cam: np.ndarray, rec: np.ndarray) -> tuple[int, float, float]:
    """Lag (in samples) of cam inside rec with the highest normalised correlation, that correlation, and
    its z-score against the correlation at all lags."""
    n = len(rec) + len(cam)
    nfft = 1 << (n - 1).bit_length()
    corr = np.fft.irfft(np.fft.rfft(rec, nfft) * np.conj(np.fft.rfft(cam, nfft)), nfft)[:len(rec) - len(cam) + 1]
    # Energy of each rec window of len(cam) samples, for the normalisation
    c = np.concatenate([[0.0], np.cumsum(rec.astype(np.float64) ** 2)])
    win = np.sqrt(c[len(cam):] - c[:-len(cam)]) * np.sqrt(np.sum(cam.astype(np.float64) ** 2))
    norm = corr / np.maximum(win, 1e-9)
    k = int(np.argmax(norm))
    return k, float(norm[k]), float((norm[k] - norm.mean()) / norm.std())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--camera", type=Path, required=True)
    ap.add_argument("--audio", type=Path, required=True)
    ap.add_argument("--approx", type=float, required=True, help="rough offset: camera t=0 in the audio file, s")
    ap.add_argument("--points", type=int, default=7)
    ap.add_argument("--window", type=float, default=30.0)
    ap.add_argument("--search", type=float, default=3.0)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args()

    t0 = time.time()
    cam_len, rec_len = duration(args.camera), duration(args.audio)
    usable_end = min(cam_len, rec_len - args.approx) - args.window - args.search - 5
    times = np.linspace(30, usable_end, args.points)
    points = []
    for i, t in enumerate(times, 1):
        cam = pcm(args.camera, t, args.window)
        rec_start = max(0.0, t + args.approx - args.search)
        rec = pcm(args.audio, rec_start, args.window + 2 * args.search)
        k, peak, z = best_lag(cam, rec)
        offset = rec_start + k / SR - t
        points.append({"camera_s": round(float(t), 2), "offset_s": round(offset, 4), "peak": round(peak, 3),
                       "z": round(z, 1)})
        log.info(f"{i}/{len(times)} camera {t:7.1f} s: offset {offset:.4f} s, peak {peak:.2f}, z {z:.0f} "
                 f"({time.time() - t0:.0f} s elapsed)")

    good = [p for p in points if p["z"] >= MIN_Z]
    for p in points:
        if p["z"] < MIN_Z:
            log.warning(f"weak match at camera {p['camera_s']} s (z {p['z']}), left out of the fit")
    if len(good) < 3:
        log.error(f"only {len(good)} points with z >= {MIN_Z}; no trustworthy fit")
        raise SystemExit(1)
    t = np.array([p["camera_s"] for p in good])
    o = np.array([p["offset_s"] for p in good])
    drift, offset0 = np.polyfit(t, o, 1)
    resid_ms = (o - (offset0 + drift * t)) * 1000
    result = {"camera": args.camera.name, "audio": args.audio.name, "points": points,
              "offset0_s": round(float(offset0), 4), "drift_ppm": round(float(drift) * 1e6, 2),
              "drift_over_camera_ms": round(float(drift) * cam_len * 1000, 1),
              "max_residual_ms": round(float(np.abs(resid_ms).max()), 1)}
    log.info(f"offset at camera 0: {offset0:.4f} s; drift {drift * 1e6:.1f} ppm = "
             f"{drift * cam_len * 1000:.0f} ms over the {cam_len / 60:.1f} min camera file; "
             f"max residual {np.abs(resid_ms).max():.1f} ms; done in {time.time() - t0:.0f} s")
    if args.output:
        args.output.write_text(json.dumps(result, indent=1), encoding="utf-8")
        log.info(f"wrote {args.output}")


if __name__ == "__main__":
    main()
