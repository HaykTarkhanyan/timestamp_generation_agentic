"""Audio-only upload for YouTube captions: a black 640x360 video at 1 fps carrying the audio (AAC 128 kbps),
optionally a slice of the source (start, duration in seconds). Light: the video is almost free to encode;
~1-2 min per hour of audio. Prints the output size and duration.

    python blank_video.py <source> <out.mp4> [start_s duration_s]
"""
import subprocess
import sys
import time
from pathlib import Path

t0 = time.time()
src, out = sys.argv[1], Path(sys.argv[2])
cut = ["-ss", sys.argv[3], "-t", sys.argv[4]] if len(sys.argv) > 4 else []
out.parent.mkdir(parents=True, exist_ok=True)
cmd = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=black:s=640x360:r=1",
       *cut, "-i", src, "-map", "0:v", "-map", "1:a:0", "-c:v", "libx264", "-tune", "stillimage", "-preset", "veryfast",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ac", "1", "-shortest", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                           capture_output=True, text=True, check=True).stdout)
print(f"{out.name}: {out.stat().st_size / 1e6:.0f} MB, {dur / 60:.1f} min, made in {time.time() - t0:.0f} s")
