# Zero-phase (forward-backward) notch filters made an audible echo; forward-only ones did not

**Symptom**
After switching the Vahagn dehum notches (12-23 IIR notches, Q 30, at a drifting mains-hum ladder) to
`scipy.signal.sosfiltfilt`, the user: "i now hear kind of an echo which makes it worse".

**Cause**
Forward-backward filtering cancels the phase shift, but it runs each sharp notch's ringing in both directions, so
every sound gets a faint smear *before* it as well as after it. A pre-echo is far more noticeable than the usual
after-ring of a forward filter, and a dozen-plus sharp notches add up.

**Evidence**
23.3.b 6:50-7:30 in six variants, one suspect switched off at a time
(`output/vahagn_linalg_overview/audio/echo_test.html`, `scripts/non_essential/vahagn_dehum.py` switches):

| variant | notches | denoise | buzz left (dB vs speech) | echo (the user) |
|---|---|---|---|---|
| A | zero-phase, Q 30 | learning + re-learn per minute | -67.6 | yes |
| B | forward only | learning + re-learn | -67.8 | no |
| C | zero-phase | learning | -67.6 | yes |
| D | forward only | learning | -67.9 | no |
| E | forward only, Q 20 | learning | -67.7 | no |
| F | forward only, Q 20 | plain light | -57.7 | no |

The user: "only a and C have it".

**Consequences**
- Use forward-only notches (`sosfilt`), started 2 s early so the filters have settled where the output begins.
  They cost nothing in buzz removal here.
- Re-learning the noise once a minute changed nothing measurable (A vs C, B vs D) and was dropped.
- When a processing change makes things "worse" in a way the user can hear, render one variant per suspect over
  the same short excerpt and let the user name the bad ones: one round settled it.
