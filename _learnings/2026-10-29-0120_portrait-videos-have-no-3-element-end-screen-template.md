# Portrait and square videos get no 3-element end-screen template

**Symptom:** Arnak's Դաս 3 (2026-10-28) failed 3 times in a row: the template card
`[aria-label="1 video, 1 playlist, 1 subscribe"]` never appeared after "Apply template".

**Cause:** the video is portrait (1760x1920). For portrait and square videos Studio lists only 2-element templates,
so "1 video, 1 playlist, 1 subscribe" does not exist there. yt-dlp sizes of the 14 Arnak lessons: 9 portrait or square
(e.g. 1440x1662, 1760x1920), 5 landscape.

**Consequences:**
- Those lessons got "1 video, 1 playlist" (no Subscribe), the user's Q31 (DECISIONS #52).
  `endscreen_template.js` takes `JOB.layout: "video+playlist"` for them, and the verifier knows the 2-element shape.
- Check the frame size first (YouTube API `fileDetails` for our own uploads, yt-dlp `width`/`height` otherwise) and
  pick the layout in the job generator, instead of letting a batch find out by failing.
- The template check after deleting old elements matches only `1 video, 1 playlist`, the part both template
  names share.
