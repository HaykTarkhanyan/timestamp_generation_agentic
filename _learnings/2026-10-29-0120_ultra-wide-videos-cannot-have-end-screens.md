# Ultra-wide videos cannot have end screens

**Symptom:** umath Tier 3 (2026-10-28): on 6 short lessons Studio disabled "Add end screens" with "Your video has an
unsupported aspect ratio".

**Cause:** the videos are ~2.27:1 (1280x558-564, 1920x846-850, sizes from yt-dlp). Studio offers end screens only up to
some aspect ratio, and these are past it.

**Consequences:** nothing to fix. Skip them and record them as "cannot have one"
(`output/endscreens/umath_tier3_survey_2026-10-28.json`). Together with the portrait case (learning
2026-10-29-0120_portrait-videos-...), this means the frame size decides which end screen a video can get.
