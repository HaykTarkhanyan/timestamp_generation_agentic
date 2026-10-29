# ML52 correctness review

Sources: the practical's solution notebook `ml/12_cnn/52_gesture_snake/52_gesture_snake_solution.ipynb`
(its printed outputs), the raw-upload caption pass mapped through the 41 cuts
(`edited_predicted/transcript.txt`), and YouTube's regenerated captions of the edited video
(`edited/transcript.txt`, a second recognizer pass): both passes agree on both clear mistakes.
Times below are on the edited video. Reviewed 2026-10-17. **Published 2026-10-17: the two clear
mistakes are in the description; the optional fine-tuning update is not.**

Note: the notebook was re-run at 22:52 on 2026-10-16, after the lecture, and gained Part 8b
(fine-tuning). It is seeded, so the numbers shown in class should match; the timings
(machine-dependent) do not.

## Clear mistakes (draft corrections)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:18:43 | The first conv layer's weights: "16 x 3 x 3 = 16 x 9, plus the biases" | 16 x 3 x 3 x **3** + 16 = 448: each 3x3 filter spans all 3 input channels (RGB) | notebook cell 24, `Conv2d (16, 64, 64) 448`; cell 26 `conv_weights(k, cin, cout) = k*k*cin*cout + cout` |
| 0:49:29 | "Hammerhead is the hammer's head" | ImageNet's `hammerhead` is the hammerhead **shark**; the hammer is a separate class (`hammer`, the 3% second guess) | notebook cell 111: `right: hammerhead 87% \| hammer 3% \| gar 1%`; ImageNet class 4, between tiger shark and electric ray |

## Update worth telling viewers (optional)

| When | Said | Now |
|---|---|---|
| 0:54:42 | "I forgot to fine-tune (unfreeze the last layer); I'll add it to the file before the video is up" | Done: Part 8b retrains ResNet-18's last conv (2.36M weights). Val accuracy 64% -> 76% (LP-FT, best 78%), 82.8% with a random head (best 84.4%) |
| 0:57:02 | `gesture_model.pt2` is the big CNN with augmentation | After the re-run, `gesture_model.pt2` is the fine-tuned ResNet (76% val); the big CNN is `gesture_model_bigcnn.pt2` |

## Maybe ASR (never in the corrections unless confirmed)

| When | Caption | Correct |
|---|---|---|
| 0:27:48 | the flattened crop has "1228 pixels" | 12,288 (64 x 64 x 3) |

## Minor (left out by default)

| When | Note |
|---|---|
| 0:37:05 | "bottom-left corner 95%": 94.4% train (22.0% val) |
| 1:12:00 | the 2x2 average pool "is basically a Gaussian blur": it is a box (uniform) blur plus downsampling |
| 0:22:12 | batches "0 to 32, then 33 to 64": slices 0-31, then 32-63 |
| 0:56:06 | other people's photos: CLIP zero-shot 41.1% and the ResNet-18 probe 44.4% are "much better" than our CNNs (17.8-23.3%), but those photos have only 3 classes, and "always nothing" already scores 33.3% |

## Not checked

Training times "30, 60, 120 s" and ResNet-18 "48 ms vs 4 ms per frame": machine-dependent; the
re-run printed 17/40/52 s and 59.6 vs 8.3 ms under a different load.

## Checked and correct

500 crops, 100 per class, 2 sessions split 250/250 by burst; small CNN 44,293 weights with
20,485 (almost half) in the head; BatchNorm 2 parameters per channel; MLP 3,179,525 weights,
72x the small CNN, ~50% val; bigger CNN 525,445 ("half a million"), 42% last epoch; train loss to
0 and train accuracy 100% while val loss rises (overfitting); average colour + logistic
regression 86.4% / 30.4%; nearest neighbour of every "left" crop is a "nothing" crop; mirror
augmentation swaps left and right; bigger CNN + augmentation best 90%, last 66% ("from 42 to
66"); 1-NN random split 100% vs burst split 43.2%; Minkowski = Euclidean (p = 2); ResNet-18 11.7M
weights, 47 MB; ImageNet guesses plunger (then electric and acoustic guitar), basketball, cello,
harp; ResNet-18 probe 64% val, 100% train; CLIP ViT-B/32 image 87M / text 63M weights, probe
47.6%, zero-shot about random on our crops (27.6%); other people's photos: big CNN 17.8%;
AdamW fixes Adam's weight-decay coupling; ImageNet normalization and eval mode for the frozen
trunk; Claude Opus 5.5.
