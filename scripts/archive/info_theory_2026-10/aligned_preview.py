"""studio.html preview for a lecture whose sound is a separate recorder: 360p, 15 fps, black where the camera
has no picture (before it starts, after it stops), the camera's keyframes (~1/s, -skip_frame nokey) placed
on the recorder's timeline by align_audio.py's offset and drift, and the WAV's own source as the sound.
Writes <out_dir>/video/<id>_360p.mp4 and the .source.txt that find_edit_points.existing_video_proxy checks.
~8-9 min for a 70-min HEVC 10-bit camera file (Դաս 8's keyframe preview: 501 s).

    python aligned_preview.py <out_dir> <camera.MOV> <align.json>
"""
import json
import subprocess
import sys
import time
from pathlib import Path

t0 = time.time()
out_dir, cam, align = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
meta = json.loads((out_dir / "metadata.json").read_text(encoding="utf-8"))
vid = meta["id"]
audio_src = (out_dir / "audio" / f"{vid}_16k.source.txt").read_text(encoding="utf-8").strip()
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            str(out_dir / "audio" / f"{vid}_16k.wav")], capture_output=True, text=True,
                           check=True).stdout)
al = json.loads(align.read_text(encoding="utf-8"))
if al["camera"] != cam.name:
    raise ValueError(f"{align} is for {al['camera']}, not {cam.name}")
k, off = 1 + al["drift_ppm"] / 1e6, al["offset0_s"]
dest = out_dir / "video" / f"{vid}_360p.mp4"
part = dest.with_suffix(".part.mp4")
dest.parent.mkdir(exist_ok=True)
graph = (f"[0:v]scale=640:360,setpts=PTS*{k:.9f}+{off:.6f}/TB[cam];"
         f"color=c=black:s=640x360:r=15:d={dur:.3f}[bg];"
         "[bg][cam]overlay=eof_action=pass:repeatlast=0,format=nv12[v]")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-skip_frame", "nokey", "-i", str(cam),
       "-i", audio_src, "-filter_complex", graph, "-map", "[v]", "-map", "1:a:0", "-t", f"{dur:.3f}",
       "-c:v", "h264_qsv", "-preset", "veryfast", "-global_quality", "30", "-g", "30",
       "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-movflags", "+faststart", str(part)]
print(f"encoding {dest.name}: {dur / 60:.1f} min, camera at {off:.3f} s, drift {al['drift_ppm']} ppm", flush=True)
subprocess.run(cmd, check=True)
got = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            str(part)], capture_output=True, text=True, check=True).stdout)
if abs(got - dur) > 1.0:
    raise RuntimeError(f"{part}: {got:.1f} s, the WAV is {dur:.1f} s; left as .part")
part.replace(dest)
dest.with_suffix(".source.txt").write_text(f"{cam} keyframes, aligned by {align.name}\naudio: {audio_src}\n",
                                           encoding="utf-8")
print(f"wrote {dest} ({dest.stat().st_size / 1e6:.0f} MB, {got / 60:.1f} min) in {time.time() - t0:.0f} s")
