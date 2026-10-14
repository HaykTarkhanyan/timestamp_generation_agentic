# ML50 correctness review

Sources: course deck `ml/12_cnn/51_transfer_learning.tex` (slide text and its source notes),
three caption passes (raw upload of [50], raw upload of [51] - same recording - and the
edited [50]), a PyTorch check, web search. Times below are on the edited video. Reviewed
2026-10-15. **Published 2026-10-15 in the description, above the chapters:** the frozen-layer
correction and the optional GPT paper-title one (the user approved both).

## Clear mistakes (draft corrections)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:27:36 | If a middle layer is frozen, "the chain probably breaks, not sure how implementations do it"; before that, "we can set this piece's gradient to zero ... if it goes times zero" | Freezing only stops that layer's own weights from updating. The gradient still flows *through* it (chain rule, its weights used as constants), so the layers before it train normally | PyTorch run (scratchpad `frozen_middle.py`): three linear layers, middle one `requires_grad=False`; after `backward()` the first layer's grad is non-zero (abs sum 0.031), the middle's is None |

## Optional (hedged by the speaker, or minor)

| When | Said | Note |
|---|---|---|
| 0:16:59 | GPT's paper was "Language models are zero shot learners, or something like that" | The idea described (next-word training, then zero-shot translation and summaries) is GPT-2's: "Language Models are Unsupervised Multitask Learners" (2019). GPT-3: "Language Models are Few-Shot Learners" (2020). The exact title "...Are Zero-Shot Learners" is Google's FLAN (Wei et al., 2021), which someone searching would land on |
| 0:04:26 | "ResNet-101, or the 150-layer one" | ResNet-152 |
| 0:33:15 | the last layer "is 512 filters of 7x7" | 512 feature maps of 7x7 (the slide says maps); the filters are 3x3 |

## Maybe ASR (never in the corrections unless confirmed)

| When | Caption | Note |
|---|---|---|
| 0:04:36, 0:04:42 | "117 million parameters" (all three caption passes) | ResNet-18 has 11.7M. 0:04:57 says 11.7M in the edited pass (117M in both raw passes), 0:08:50 says 11.7M in all three, and the slide shows 11.7M. If "117" was said, it was corrected on screen within seconds |

## Checked and correct

ResNet-18 11.7M weights; its layout (224x224x3 in, blocks of two 3x3 convs, 512 maps of 7x7,
global average pooling to 512, fc to 1000 classes); the new head 512 x 3 + 3; ImageNet 1000
classes and 1.2M images; freeze = take the published weights and keep training from them;
DeepSeekMath started from their code model (DeepSeek-Coder-Base-v1.5) and trained all of it on
120B math tokens ([arXiv 2402.03300](https://arxiv.org/abs/2402.03300)); small learning rate,
augmentation, early stopping, freeze first; BatchNorm keeps updating its running statistics
in train() mode even with requires_grad=False, and eval() does not turn gradients off;
unfreezing continues from the current weights, not from random; domain mismatch
(spectrograms), cv2 reads BGR; DINOv3 on 1.7B unlabeled images, trained by matching a small
and a large crop; CLIP on 400M image-text pairs (2021); Clever Hans read the questioners'
reactions; Grad-CAM (ICCV 2017): gradient per map, weighted sum, ReLU, 7x7 heatmap, upsampled
to 224 with no model involved; ImageNet has a pomegranate class; cat vs dog maps for the same
photo.
