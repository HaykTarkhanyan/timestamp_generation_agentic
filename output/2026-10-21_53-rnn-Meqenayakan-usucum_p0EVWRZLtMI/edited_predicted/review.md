# ML53 correctness review

Sources: the raw-upload caption pass mapped through the 50 entered cuts
(`edited_predicted/transcript.txt`), the deck outline `ml/13_rnns/53_rnn_foundations_OUTLINE.md`
and the figures in `ml/13_rnns/fig/`. Times are on the edited video. Reviewed 2026-10-21, before
YouTube's second caption pass exists. **Published 2026-10-21 22:00 without corrections (none
found). Checked 2026-10-24 on the second caption pass: 5 chapters moved back 1 s, re-pushed; both passes hear "casual" at 0:41:27.**

## Clear mistakes

None found.

## Maybe a slip or ASR (check on the second caption pass)

| When | Caption | Correct |
|---|---|---|
| 0:41:27 | "casual language modeling" | causal language modeling (left to right only). Both caption passes hear "casual", so it was probably said: a slip, not ASR |

## Minor (left out by default)

| When | Note |
|---|---|
| 0:52:03 | "largest eigenvalue under 1, everything goes to 0; over 1, everything explodes": under 1 (with tanh, the largest singular value) is enough for vanishing; over 1 is only necessary for exploding, the activation's derivatives can still shrink it (Pascanu, Mikolov, Bengio 2013) |
| 0:56:54 | "that's why nobody uses LSTMs now": an overstatement; LSTMs are still used for some time series and on-device speech, just not for language models |
| 0:20:29 | RNN ideas "from the 90s": Jordan 1986 and Elman 1990; BPTT is Werbos 1990 |
| 0:32:30 | GPT-2's vocabulary, 50257 tokens = 50,000 BPE merges + 256 bytes + 1 end-of-text token; padded to 50304 in nanoGPT (a multiple of 64) and faster despite the extra rows. What he said matches; the caption garbles the sum |

## Checked and correct

Sigmoid derivative at most 1/4 (so at best a 4x shrink per step); ReLU derivative 0 or 1; tanh as
the default between the two; one-hot vectors all sqrt(2) apart; W 3x2 for a 3-word vocabulary and
a 2-dim state, V 2x2; the one-hot times embedding matrix picks one row; zero padding still changes
the state (V z3 + 0 is not z3), hence masking; AlexNet-style CNN about 60M weights with only about
2M in the convolutions; 0.8^29 = 0.0015 and 1.25^29 = 646 (fig/vanish_curve.pdf); D_t is diagonal;
gradient clipping rescales to the threshold (norm 40, threshold 4: divide by 10); clipping is from
Pascanu, Mikolov and Bengio; bidirectional RNNs cheat at next-word prediction but suit translation;
GPT-style decoders look left only, masked LMs both ways; image captioning is one-to-many,
translation many-to-many with an encoder and a decoder, POS tagging synchronized many-to-many.
