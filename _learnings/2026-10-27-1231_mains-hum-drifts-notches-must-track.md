# A mains hum drifts within one lecture, so notches fitted once miss it

**Symptom**
After the first dehum of Vahagn 23.3.b (notches fitted on one pure-buzz sample at 3:01), the user: "in 7th minute i
still hear some, but not much". A stronger denoise (30 dB instead of 20) barely helped (-57.2 -> -59.0 dB vs speech in
that minute), while the minute holding the sample came out at -68.7.

**Cause**
The hum's fundamental moves: 73.6 Hz at 3:01, 76.2 Hz at 7:18 (73.5-76.7 Hz over the piece). A Q 20 notch at the
4th harmonic sat 11 Hz off (294 vs 305 Hz). In minute 7 the ladder (76, 152, 229, 305, 381 Hz...) stood as high over
its surroundings after processing as before (+47 vs +46 dB). afftdn does not fix it: it models noise in broad bands,
too coarse for a narrow ladder. Also the hum frequency differs between lectures (24.1: 48.8 Hz, 28.3.a: 48.39 Hz,
23.3.b: ~75 Hz), plus a second source at 90 / 113.8 / 138.3 Hz.

**Consequences**
Re-fit the notches every 30 s on that stretch's steadiest pure-buzz 2 s and cross-fade the chunks (1 s overlaps):
23.3.b went to -67.9 dB vs speech (minute 7: -68.3, no ladder left). Measure the residual as peak height over the
neighbouring spectrum, not as band energy alone: band energy dropped 5-8 dB while the peaks were untouched.
Scripts: `scripts/non_essential/vahagn_dehum.py` (`tracking_notches`), probes in `scripts/archive/vahagn_2026-10/`.
