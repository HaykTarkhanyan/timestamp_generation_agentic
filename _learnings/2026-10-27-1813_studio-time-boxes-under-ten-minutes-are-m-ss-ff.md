# Under ten minutes Studio's time boxes are M:SS:FF, so typing MM:SS:FF gets truncated

**Symptom**
Vahagn 23.3.b (`3kfEyTsqq-s`, 9:37), 2026-10-27: the entry batch stopped on cut 1, "typed 00:00:00 into the playhead
box, it reads "00:00:0" after 3 tries". The box showed "0:00:00" before typing; the trim markers read
"Start trim marker 0:00:00" / "End trim marker 9:36:14", one minute digit.

**Cause**
The box's `maxlength` is 7 on a video under ten minutes (M:SS:FF) and 8 from ten minutes up (MM:SS:FF; measured on
the 7 other open editors, 10:21 and longer). The template typed MM:SS:FF for every video under an hour, so the last
character was dropped, and its `full()` turned the 3-part marker "0:00:00" into "0:0:00:00", which no planned time
equals. No video under ten minutes had been cut before (the ML, Tserunyan, Papikian and Arnak lectures are all longer).

**Fix (scripts/studio_enter_cuts.js)**
- `full()` pads the minutes of a 3-part time to two digits ("0:00:00" -> "0:00:00:00").
- `underTen` = the playhead box's `maxlength` is 7; `typed()` then drops the leading minute zero ("0:09:30:00" ->
  "9:30:00"). The box's value is no guide: at the start of a fresh 23.3.b tab it did not read "0:00:00".
- Videos of ten minutes and longer type exactly as before.
23.3.b (3 cuts) and 28.3.b (5:13, 2 cuts) then went in identical, as did 28.2.b (9:41).

**Also**
The Playwright session was on Metric when this work started (another session had used it), although the editor link
of a umath video opened: the account chip said "Metric - Python, ... You're a manager". Switched through the chip
(Switch account > @hamalsaranakan_matematika) before any cut, as `2026-10-27-0359_studio-session-channel-...` says.
