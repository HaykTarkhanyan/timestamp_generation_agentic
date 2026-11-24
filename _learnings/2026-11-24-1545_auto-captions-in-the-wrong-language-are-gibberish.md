# YouTube auto-captions in the wrong language: noise, or fluent-looking gibberish

**Symptom.** Fetching umath transcripts (pilot, 2026-11-24), some videos' only auto-caption track was not
Armenian although the speech is. yt-dlp names the speech-recognition track `<lang>-orig` (the plain `<lang>`
entries are machine translations of it), and for these it was `ro-orig` or `en-orig`:

| video | audio language set | track | chars/min | sample |
|---|---|---|---|---|
| BfuZCh83Sp4 (Դաս 12, Ֆունկցիոնալ անալիզ) | en-US | ro | 38 | `[Muzică] asun cea ț Dar ați factor f faktor fak normal [Aplauze]` |
| f3qOK-kTZi8 (private, via API) | none | ro | 40 | `[Muzică] or [Muzică] G ek Yet f alf h` |
| 53J-ao36SpE | none | en | 11 | `[Music] [Laughter] [Music] um um [Applause] me foreign` |
| 9pTflZVOzLc | en-US | en | 3 | `is foreign [Music] foreign [Music] m foreign um` |
| pcvuCY6IUag (Armenian Public TV) | hy | en | 713 | `para decir la Ossa gardener Nahor decision menachem including` |
| VKVbUbRioDk (Armenian Public TV) | hy | en | 678 | `perrantes irelia Hartnett I saw men Cosumnes en cualquier otra` |
| real Armenian, 3 videos | hy | hy | 537-615 | `Ուրեմն, հարգելի ուսանողներ, հիմա մենք...` |

**Cause (partly a guess).** The track language does not simply follow the current audio-language setting: the TV
videos are set to `hy` and still have an English track, BfuZCh83Sp4 is set to en-US and has a Romanian one. Most
likely the tracks were generated once, with the setting or auto-detection of that time (perhaps before YouTube
recognized Armenian), and never redone. Not tested: whether setting the audio language to `hy` now makes YouTube
regenerate the track.

**The test that works: the share of Armenian letters in the text.** On all 367 umath transcripts (full run,
2026-11-24) every wrong-language track (30 ro, 16 en, 13 tr) has a share of 0.0 and every real one 0.65-1.0 (the
lowest are Tserunyan's topology lectures, full of Latin math). Two simpler tests failed:
- the track's language label: kAhHrwS_-Kk is labelled `de` (the video's metadata language is German) and is 99%
  Armenian;
- characters per minute: the TV gibberish runs to 713, a real but quiet solution video (mJdFeWleKPQ) has 110.

**Consequences.**
- `fetch_channel_transcripts.py` marks a transcript usable if at least half its letters are Armenian; the rest keep
  their text with `usable: false`.
- Some videos have no auto-caption track at all (1 unlisted umath lesson, 4 of 6 TV lessons). yt-dlp exits 0 and
  writes nothing; the API's `captions.list` returns `[]` for the same videos (2 of 2 checked), so asking the API
  after yt-dlp found no track only spends 50 units.
- yt-dlp and the API return the same track: VQKqS7JvWmM gave 483 of 483 identical segments, text and timings.
