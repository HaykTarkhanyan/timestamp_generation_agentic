# ML47 correctness review

Sources: `ml/11_neural_networks/47_name_inventor_solution.ipynb` (printed outputs
and source), web search for the news items. Reviewed 2026-10-01.

## Clear mistakes (in the draft comment)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:01:57 | W&B "became CoreWeave" in the last few weeks | CoreWeave bought W&B in May 2025; the product keeps its name. New since 2026-09-30: sign-in through CoreWeave Forge | [CoreWeave](https://www.coreweave.com/news/coreweave-completes-acquisition-of-weights-biases-2), [W&B is now part of CoreWeave](https://www.coreweave.com/companies/weights-and-biases) |
| 0:28:38 | After «ն» the name does NOT end in 74% | Reversed: it ends in 74% (527 of 716), goes on in 26%. Also «ան»'s 17% is of its 638 occurrences, not of surnames | notebook cell 18 output |
| 0:31:34 | For K=2, 3.6% of the 422 contexts don't appear in validation | Reversed: 3.6% of validation windows have a context never seen in training | notebook cell 22 output |
| 0:33:27, 0:36:16 | One-hot of 39, embedding table 39 x 8 | Input side has 40 symbols (38 letters + "." + "^"): 40-dim one-hot, 40 x 8 table. Said correctly at 0:38:36 and 0:46:18 | notebook cells 6, 27, 38 |
| 1:21:20 | The .pt checkpoint holds Adam's first/second moments | It holds `state_dict`, `config`, `stoi` only - no optimizer state | notebook cell 96 source and output |

## Minor / framing (left out of the comment by default)

| When | Note |
|---|---|
| 0:55:44 | Started from the binary cross-entropy formula for a 39-class problem; landed on -log p correctly |
| 0:33:46, 0:46:55 vs 1:19:21 | One-hot called "not a good option"; in the comparison the plain one-hot MLP had the best val loss (1.646 vs 1.671, about 3.5x the 0.007 seed noise). The embedding's win is parameters (8,551 vs 20,519), not loss |
| 0:35:34 | CLIP dims "512 or 784": ViT-B/32 is 512, ViT-L/14 is 768; 784 is MNIST's 28x28 (hedged in the video) |

## Maybe ASR (never in the comment unless confirmed)

| When | Caption | Correct |
|---|---|---|
| 0:46:29 | "205000" parameters | 20,519 (fine if "20,500" was said) |
| 1:16:53 | "dropped by about 1" from the bigram | perplexity 7.0 -> 5.3 (1.7) |

## Checked and correct

Bengio 2003 (23 years); NVIDIA buying Hugging Face (agreement 2026-09-02, about
$12.9B, close expected H1 2027 - [TechCrunch](https://techcrunch.com/2026/09/03/nvidia-confirms-it-will-buy-hugging-face-for-12-9-billion/));
GPT-2's 50,257 tokens; 8,551 parameters; ln 39 = 3.66; loss 0.69 = perplexity 2;
temperature numbers; 945 of 1000 ending in -յան; best epoch 51.
