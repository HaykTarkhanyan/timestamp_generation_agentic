# Find mains buzz in the quiet moments below 600 Hz, not in the high band and not in stitched pauses

**Symptom**
Three detectors failed before one worked on the Vahagn recordings (2026-10-26/27):
1. pause background in 3-7.5 kHz per 10 s window: flagged "episodes" in 12 pieces; the user found the noise was
   constant, and its spectrum showed almost nothing above 2 kHz. Wrong band.
2. harmonic ladder over a spectrum of thousands of stitched 10 ms pause snippets: every piece scored 0.4-2 dB, the
   noisiest included; the stitching smeared away the sharp peaks.
3. long-term average spectrum of the whole piece: clean 24.1 showed the same 49 Hz spike as noisy 28.3.a; speech
   covers 150-600 Hz when averaged.

**What works**
The 150-600 Hz band in the quietest 10% of 128 ms frames of each minute (or 10 s window), minus the speech level (90th
percentile, full band). No pause detector needed. Buzz -37..-48 dB, clean -73..-77: a 30 dB gap, constant within a
piece where the buzz is constant (28.3.a -42.5 median, -40.4 max). `scripts/archive/vahagn_2026-10/buzz_band.py`,
results `_knowledge/vahagn_linalg/buzz_band.json`.

**Also**
- One labelled example from the user (a 3.4 s mark of pure noise) beat all the detectors: its spectrum named the
  problem (a 48.4 Hz ladder + a 90/114/138 Hz source) in one plot. Ask for a sample early.
- find_edit_points' sound mask uses one threshold per piece; in a piece with buzz in part of it, the buzz counts as
  sound and its stretches show no pauses (24.1). Pick noise samples by steadiness (frame std 2 dB or less) instead.
