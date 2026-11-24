# YouTube's Armenian ASR writes `<unk>` where the question mark ՞ belongs

**Symptom.** The umath transcripts (sent as a zip on 2026-11-24, then rebuilt) were full of `&lt;un`, `&lt;un&gt;`,
`&lt;k&gt;`: 12,489 `&lt;` and 4,157 `&gt;` in 258 of 283 Armenian VTTs, from yt-dlp and the API alike. In words:
`ի&lt;unչ` 578 times, `հա&lt;un` 629, `չէ&lt;un` 452, `ո&lt;k&gt;նց` 79.

**Cause.** The recognizer has no ՞ in its output and emits an unknown token (`<unk>`) where the mark goes. The
per-word timing tags cut the token into pieces (`<un`, `<un>`, `<k>`, `<k`), and the VTT HTML-escapes the angle
brackets. `parse_vtt`/`vtt_cues` strip real `<...>` tags but never decoded entities, so the escaped pieces stayed in
the text. Every position is a classic ՞ spot: ի՞նչ, ո՞նց, հա՞, չէ՞, ինչպե՞ս, թե՞, ո՞վ, կա՞. In the most common
case the token also took the next letter (`ի<unչ` = ի՞նչ); a few lost another one (`կարո՞` = կարո՞ղ, `ինչպե՞` =
ինչպե՞ս, `ինչո՞` = ինչո՞ւ).

**Fix.** `fetch_channel_transcripts.clean_caption_text`: decode entities, `ի/ո + marker + չ/ց` -> `ի՞նչ`/`ո՞նց`,
every other marker -> ՞, drop leftover closers and YouTube's `>>` speaker marks, complete the four truncated words.
On all 269,025 segments: 4,643 changed, 0 leftover `<`, `>` or entities; top results ի՞նչ 1,354, հա՞ 1,120, չէ՞ 581.

**Consequences.**
- The first zip sent on 2026-11-24 (Telegram message 877566) had the raw `&lt;un` pieces; it was replaced.
- A vocabulary test ("which reading gives a known word") picked wrong letters (`հա<un` -> հատ), because հա and չէ
  almost never appear without the marker, so the clean vocabulary barely has them. Rules by position worked.
- Not fixed: `transcript.txt` from `fetch_subtitles.parse_vtt` (the chapter pipeline) has the same pieces. Harmless
  for picking chapter labels, but the same `clean_caption_text` would fix it.
