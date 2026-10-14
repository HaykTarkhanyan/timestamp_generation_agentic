# ML51 correctness review

Sources: course deck `ml/12_cnn/52_vision_tasks.tex` (slide text and its source notes),
`results/detector_candidates.json` (the real detector run behind the slide), three caption
passes (raw [50], raw [51], edited [51]), web search. Times below are on the edited video.
Reviewed 2026-10-15. **Published 2026-10-15 in the description, above the chapters:** the U-Net
correction (the user approved it and declined the optional "pear" one).

## Clear mistakes (draft corrections)

| When | Said | Correct | Evidence |
|---|---|---|---|
| 0:33:20 | U-Net has "the skip connections that came from ResNet, so the in-between maps get added, the gradient flows better" | U-Net **concatenates** the early sharp maps onto the upsampled ones (ResNet adds); the point is to bring back the detail lost in the bottleneck. U-Net (May 2015) is also older than ResNet (Dec 2015), so its skips did not come from ResNet | the deck's U-Net frame ("concatenated"); Ronneberger et al., arXiv 1505.04597; He et al., arXiv 1512.03385 |

## Optional (minor)

| When | Said | Note |
|---|---|---|
| 0:07:54 | the detector "says apple and pear" (all three caption passes) | It said apple (6 boxes) and orange (1); COCO has no pear class. The slide on screen shows the right labels |
| 0:29:38 | "earlier Mask R-CNN or Faster R-CNN; now in '25 transformer-based SAM came out" | Faster R-CNN is a detector (Mask R-CNN = Faster R-CNN + a mask head). SAM came out in April 2023, SAM 2 in 2024, SAM 3 in Nov 2025 - "'25" fits SAM 3 only |
| 0:02:08 | localization is "detection with one class" | with one **object** (one box); maybe the recognizer |
| 0:08:41 | "divided into 120 cells, then crops of different sizes from them" | the slide: 120 crops in total, at 3 sizes |

## Not checked

0:27:52 "YOLOv3 has 43,000 citations": read off the screen live; the citation API was
rate-limited, so the count is not verified (it is plausible for 2026).

## Checked and correct

Four tasks (classification, localization, detection, segmentation); the label vector (box,
"is there an object", one-hot classes) and why "nothing here" must be an answer; the real
SSDlite run: 401 pairs above 5%, 45 above 0.4, NMS after that, COCO has no pomegranate;
R-CNN (2014) with about 2,000 region proposals; anchors; YOLO = You Only Look Once, and
`codex --yolo` is a real alias of `--dangerously-bypass-approvals-and-sandbox`
([Codex CLI reference](https://developers.openai.com/codex/cli/reference)); IoU (1 = same box,
0 = no overlap, 0.5 as "same object"); NMS with a 0.45 threshold; no true negatives in
detection, so precision, recall, AP and mAP; R-CNN, Fast, Faster R-CNN vs YOLO; YOLO's 7x7 grid,
the centre cell is responsible, the box may be bigger than the cell; YOLO v1 used squared
error for everything, including classes, with lambda weights; modern YOLO uses an IoU-based box
loss and log-loss for classes; Joseph Redmon: YOLO 2016, YOLO9000, YOLOv3 2018, Darknet, left
computer vision over military uses, v4 on by others; the YOLOv3 intro ("Twitter"); separable
convs about 20,000 vs 800 weights (slide: 19,200 vs 843), MobileNet on phones; U-Net down,
bottleneck, up with transposed convs; SAM click-to-mask and video tracking (SAM 2); 1D and 3D
convs (CT, MRI, video); style transfer; GAN faces, thispersondoesnotexist; SuperAnnotate (an
Armenian-founded annotation startup) and assisted labeling tools.
