# On PSU Kaltura, the small 720p flavor is the Zoom original; download that one

**Symptom**

`yt-dlp -F` on a PSU Kaltura lecture (Papikian's Algebra and Number Theory, `psu.mediaspace.kaltura.com`) lists two 1280x720 mp4 files of very different size, for example Lecture 16 (`1_ih9bifgs`):

```
mp4-282 mp4 1280x720    25 | ≈187.38MiB 282k http  | avc1    unknown mp42
mp4-493 mp4 1280x720    25 | ≈327.56MiB 493k http  | avc1    unknown isom
```

Same resolution, 75% more bytes. The obvious guess, "bigger is better", is wrong here.

**Cause**

The small one (`mp42`) is the Zoom recording as uploaded. The big one (`isom`) is Kaltura's ffmpeg re-encode of it for streaming. We downloaded both for Lecture 16 and compared them (2026-10-20):

| | small `mp4-282` | big `mp4-493` |
|---|---|---|
| size | 196,477,839 bytes | 343,473,174 bytes |
| encoder tag | `AVC Coding` | `Lavf58.76.100` (ffmpeg 4.4) |
| track handlers | `H.264/AVC video`, `AAC audio`, plus a `Text` data track | `VideoHandler`, `SoundHandler` (ffmpeg defaults) |
| audio | AAC 32 kHz mono | AAC 44.1 kHz mono (resampled) |
| video | High profile, 154 kbps | Main profile, 360 kbps |
| keyframe spacing | ~30 s (23 keyframes in the first 10 min) | exactly 2.0 s (301 in the first 10 min) |
| duration | 5571.8 s | 5571.8 s |

The ffmpeg tag, ffmpeg's default handler names and the resampled audio mark the big file as made from another file. The small file has none of them.

Neither file has an `x264 - core` tag in its first 8 MB, so that check, which we tried first, decides nothing on Kaltura.

Picture match on three 20 s stretches (600 s, 2400 s, 4200 s), small vs big:

```
600-620 s:   SSIM 0.997623, PSNR 50.80 dB
2400-2420 s: SSIM 0.997322, PSNR 50.04 dB
4200-4220 s: SSIM 0.997564, PSNR 50.56 dB
```

2x nearest-neighbor crops of the handwritten formulas and the webcam face showed no visible difference. The extra bitrate in the big file goes mostly to the forced 2 s keyframes, which help a streaming player seek; it adds no detail.

**Consequences**

- For these Kaltura recordings, pick the 1280x720 `mp42` entry from `yt-dlp -F`. Its format ID differs per lecture (`mp4-282`, `mp4-320`, `mp4-319`, `mp4-317`, `mp4-289`, `mp4-305` for lectures 16, 17, 19-23), so read the listing each time instead of reusing an ID.
- The `≈` sizes in the listing are bitrate times duration, not real byte counts. For Lecture 16 the estimate was 187.38 MiB and the real file was 187.38 MiB (196,477,839 bytes), so it was accurate here.
- No audio-only flavor exists; getting the audio means downloading the video.
- The same logic probably holds for other Kaltura sites (the original upload plus fixed-bitrate transcodes), but this was checked on one PSU lecture only.
