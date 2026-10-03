# ML48 correctness review

Sources: `ml/12_cnn/L16_cnn_foundations.tex` (slide text), the regenerated captions of
the edited video (times below are on the edited timeline), web search for news items.
Reviewed 2026-10-03.

## Clear mistakes (in the draft comment)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:14:57 | Hubel and Wiesel got the Nobel for looking at a **mouse** brain | Their recordings were in a **cat's** visual cortex (1959-62, Nobel 1981) | slide "Nature had the same two wishes" |
| 0:35:27 | A 100x100x3 image connected to one output needs **300,000** weights | 100 x 100 x 3 = **30,000** weights per output; the slide's 300 million is for a full 100x100 output | slide "Parameter sharing"; both caption passes (raw and edited) say 300 thousand |

## Minor (left out of the comment by default)

| When | Note |
|---|---|
| 0:15:20-0:15:43 | Puts the ZIP-code reader in 1998 with LeNet-5. The ZIP-code network was LeCun's 1989 version; LeNet-5 (1998, LeCun, Bottou, Bengio, Haffner) read bank checks and came with MNIST. |
| 0:13:27 | "Translation equivariance" is explained as "the same person here or there is the same", which is invariance. Convolution is equivariant (the feature map shifts with the input); pooling and the head add the invariance. |
| 1:13:12 | Models "storing information in a useless pixel as memory" is the Vision Transformer registers finding (Darcet et al. 2023), not a CNN result; it comes up while showing ResNet-18 layers. |

## Was caption noise, not a mistake

The raw captions had pixel values "0 to 285"; the regenerated captions say 255, which is right.

## Checked and correct

150,528 inputs x 1000 hidden = about 150M weights vs GPT-2 small 124M; IEEE Computer
Society stopped accepting papers with the Lena image after 2024-04-01
([Slashdot](https://tech.slashdot.org/story/24/03/29/2233208/playboy-image-from-1972-gets-ban-from-ieee-computer-journals));
Gaussian kernel 1-2-1/2-4-2/1-2-1 over 16; 9 x 4 = 36 dense connections vs 4 shared
weights; 5 x 5 x 3 = 75; 3 x 3 x 3 x 16 + 16 = 448; 28 - 5 + 1 = 24; 16 x 26 for sixteen
5x5 kernels; 24x24 -> 12x12 after 2x2 pooling; MLP 784-128-64-10 = 109k weights; Canny
1986, Hough 1962/1972, Harris 1988, HOG 2005; PyTorch's conv2d computes
cross-correlation.
