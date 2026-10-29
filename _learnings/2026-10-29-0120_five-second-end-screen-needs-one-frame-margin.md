# A 5 s end screen needs one frame more than 5 s

**Symptom:** Մաթ. անալիզ 3 (ԿՎՏԳ) Դաս 23 (2026-10-28): elements at 43:38:13-43:43:13, exactly 5 s, made Studio show
"Element must be visible for at least 5 seconds" and disabled Save. 43:38:12 (one frame earlier) saved.

**Cause:** 5 s is Studio's minimum, and an exact 5 s can count as slightly less (frame rounding).

**Fix in `endscreen_template.js`:** `back(tc, secs, frame=true)` starts 5 s end screens one more frame back. Frame 0
borrows a second and takes frame 23, which is a valid frame at 24, 25 and 30 fps and still over 5 s.

**Consequences:** YSU's ~5.5 s outro (measured white from 5.4-5.6 s before the end on 6 videos) leaves almost no
slack: 5 s plus one frame fits, 6 s would cover the last of the lecture (DECISIONS #54).
