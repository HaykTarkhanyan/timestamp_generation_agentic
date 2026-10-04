# ML49 correctness review

Sources: `ml/12_cnn/50_cnn_architectures.tex` (slide text and its source notes),
`fig/most_cited_top20.pdf`, both caption passes (raw and edited timeline; times below
are on the edited video), web search for the news items. Reviewed 2026-10-05.

## Clear mistakes (in the draft corrections)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:17:02 | Fei-Fei Li was at MIT at the time ("if I'm not mistaken") | ImageNet was built at Princeton (Deng et al., CVPR 2009); she moved to Stanford in 2009 | Deng et al. 2009 affiliations |
| 0:52:27 | CoCa reached 81% with no ImageNet training | 86% (86.3% zero-shot); 91% top-1 fine-tuned | slide "ImageNet today", source note: CoCa, arXiv 2205.01917. Both caption passes say 81% |

## Minor (left out by default)

| When | Note |
|---|---|
| 0:17:05 | World Labs "was bought 2-3 weeks ago": AMD agreed to buy it on 2026-09-28 (six days before the lecture), closing expected end of 2026 (slide source note) |
| 0:49:59 | "The 2001 paper has 199,000 citations": the top 2001 entry (real-time PCR) shows 159k on the chart; random forests (2001) 95k. Both caption passes say 199,000 |
| 0:35:13 | "12x fewer parameters than AlexNet - I was wrong, it's 7M": both are right; the GoogLeNet paper says 12x fewer (about 5M), later counts give 6.8M |

## Maybe ASR (never in the corrections unless confirmed)

| When | Caption | Correct |
|---|---|---|
| 0:29:23 | three 3x3 layers at 64 channels: "11000" (raw) / "1100" (edited) | 110,592 vs 200,704 for one 7x7; "about 2x fewer" was said and is right (45% fewer) |

## Checked and correct

ILSVRC top-5 errors 28.2 / 25.8 / 16.4 / 11.7 / 6.7 / 3.57% and the 5.1% human; ImageNet
14M images, about 22,000 categories, CVPR 2009, Mechanical Turk; 1.2M training images,
1000 classes; AlexNet 60M weights with about 58M in the dense layers, two GTX 580 3 GB,
5-6 days, about 90 epochs, ReLU 6x faster than tanh to 25% training error, dropout and
augmentation, own CUDA code, 8th most-cited paper of the 21st century; ZFNet 7x7 first
layer and smaller stride; VGG 7.3%, 138M weights with 124M in the dense layers, Karen
Simonyan and Andrew Zisserman, Simonyan at DeepMind; receptive field of stacked 3x3;
ResNet 152 layers, 8x deeper than VGG with fewer operations, most-cited paper of the 21st
century (174k), CVPR 2016; CoCa 91% top-1; Dario Amodei's September 2026 essay asking labs
to slow down ([Euronews](https://www.euronews.com/2026/09/12/anthropic-ceo-dario-amodei-calls-on-ai-companies-to-slow-down-ai-development-amid-superint),
[Forbes](https://www.forbes.com/sites/jonmarkman/2026/09/15/dario-amodei-calls-for-ai-slowdown-as-anthropic-opens-up-to-auditors/)).
