# Բազմաչափ վիճակագրություն (Arnak Dalalyan, spring 2026): state of the videos

YSU ASDS master's, Tuesdays. Lecture 1 in person (3 Feb), the rest on Zoom. Playlist
`PLz3NrXxHz_CB0PhhZrFvhE4gbd6dotQFI` on Համալսարանական մաթեմատիկա. Checked 2026-10-20 through
the YouTube API, the email thread with the lecturer, the filming team's chat and the local files.

| Lesson | Date | Video | Visibility | State |
|---|---|---|---|---|
| 1 | Tue 3 Feb | 7j53RC1y6i8 | public | done |
| 2 | Tue 10 Feb | cb3evNQOa2g | public | done |
| 3 | Tue 17 Feb | QMvIy2auywg | public | done |
| 4 | Tue 24 Feb | _P_HhQhJalQ | public | done (iPad bar in the raw: "Mardi 24 février") |
| 5 | Tue 10 Mar | oP0QPwjYegM | public | done ("Mardi 10 mars"). No lecture on 3 Mar |
| 6 | ? | 1SbwkELkTpg | unlisted | "[to review] ... ToDo". **The recording shows "Mercredi 12 mars": a Wednesday, so 12 Mar 2025, last year's course** |
| 7 | Tue 24 Mar | uFJ53ry9FXc | unlisted | "[to review] ... ToDo" (Zoom clock 2026-03-24 15:43) |
| 8 | Tue 7 Apr | mwdDFKOw2Vw | unlisted | "[to review] ... ToDo" (Zoom clock 2026-04-07 17:02); chapter times off after a later cut, says a note in the description |
| 9 | Tue 14 Apr | v0TamNWWzHs | unlisted | "[to review] ... ToDo" (Zoom clock 2026-04-14 16:46) |
| 10 | Tue 21 Apr | Hv7Jux-KYBk | new upload | 20 min (part 2 only), the start was not recorded. Asked the lecturer on 3 May which option he prefers (publish the 20 min / wait for a previous year's recording / other): **no reply**. The "2025" file is not lesson 10, see below |
| 11 | Tue 28 Apr | WFMoX0xRU6I | new upload | replaces bJy5XvxZ2B8 (deleted 2026-10-20) |
| 12 | Tue 5 May | Bz6aVzkrqbM | new upload | 2026-10-20 |
| 13 | Tue 19 May | syeGoSopVM0 | new upload | 2026-10-20 |

- **Review of lessons 6-9 (2026-10-20, a separate agent, local files only):** new chapters (25, 23,
  19, 26), titles and descriptions in `output/2026-10-20_to-review-Das-{6..9}-ToDo-Bazmachap_*`.
  None needs cuts (pauses of 3 s+: 5, 8, 3, 16; longest 4.8 s; intro and outro present). Lesson 6's
  raw file has the internal timestamp 2025-03-12T16:19:07Z (files 04, 05, 07, 08 match their 2026
  dates), so it is last year's recording; the date line is left as TODO. Lesson 7 shows the
  lecturer's browser tab strip (two mail tabs, one tab title with his address) at about
  0:31-2:41 of the YouTube version; no mailbox content seen in the raw frames. Blur, not cut.
- **Pushed 2026-10-20:** titles and descriptions of lessons 6-9 (still unlisted); lesson 6 dated
  "12 մարտ, 2025" (the user said either date is fine). A visual pass (low-res copies, ffmpeg
  black/freeze detection, one frame per minute) found no black frames in any lesson; lesson 7's
  browser tab strip is on screen at **0:00-0:05, 0:35-2:40 and 7:00-12:20** (blur 0:00-12:20).
- **The lecturer's Drive folder (two zips, unzipped to `misc\YSU OpenCourseWare\arnak\drive_lecture_slides\`):**
  Zoom recordings for lessons 2-13 and PDFs for 1-9, 10a/10b, 11, 12a/12b (none for 13).
  - Internal dates confirm 2026 for every lesson except **6 (2025-03-12)** and **10**, which has
    two files: a full 82-min **2025** lecture (2025-05-07) and this year's last 20 min (2026-04-21,
    "2rd-mas"). It looked like his answer to the 3 May email (last year's recording for the missing
    part), and he says so at the start of part 2, but the 2025 file is a different lecture (below).
  - **The course has 13 lectures.** Not on YouTube yet: 10, 12 (2026-05-05, 69 min),
    13 (2026-05-19, 65 min). Lesson 11 on YouTube is the raw 73-min recording, unedited.
- **The "2025" file in the lesson 10 folder is NOT the missing part of lesson 10 (checked
  2026-10-20 from frames and the PDFs).** Its iPad header says "Բազմաչափ վիճակագրություն, Դաս 12",
  "Mercredi 7 mai" (2025): correlation circle, PCA in R (`fviz_eig` scree plot, `corrplot`), then
  sparse PCA as an SDP for the last ~30 min. What each 2026 lesson holds:
  - 10 (21 Apr): first part = R practical on linear regression, Auto-MPG data (10a.pdf, 10 slides),
    **never recorded**; part 2 (20 min, iPad) = population PCA definition and its properties.
    10b.pdf is the 2025 handwritten version of that part (dated 23/04/25).
  - 11 (28 Apr, 11.pdf): PCA as an optimization (max v'Σv, best projection), then sample PCA.
  - 12 (5 May, 12a/12b): sample PCA, correlation circle, PCA in R (FactoMineR, decathlon2). The
    same scree-plot and corrplot slides as the 2025 video, so the 2025 video's first ~50 min
    duplicate 2026 lesson 12.
  - 13 (19 May): a new chapter, canonical correlation analysis (CCA).
  - Sparse PCA shows up in no 2026 frame sampled (lessons 11-13, 5 frames each), so it may be the
    only part of the 2025 video that 2026 lacks. Not checked against full transcripts yet.
- **Plans prepared 2026-10-20 evening (nothing applied or pushed):** per video, `content_cuts.json`,
  `studio_cuts.txt`, `edit_review.md`, and on the predicted edited timeline
  `edited_predicted/{timestamps,titles,description}.txt`. Analysis ran with `--min-silence 150`, so
  no automatic pause cuts: every cut is a listed content cut. Silences of 15 s+ were checked with a
  frame at each end; writing on the iPad stays.
  - 10 part 2: 2 cuts (0:58), 11 chapters. 12: 3 cuts (1:43) + 1 unticked, 37 chapters.
    13: 3 cuts (3:03, incl. the 2-min dead iPad), 30 chapters; Chrome tab strip with mail tabs
    visible from raw 0:55:29 to the end (optional blur, like lesson 7).
  - 11 (by an agent): 2 cuts (3:50: 2.6 min of waiting and screen-share setup at the start, the
    goodbyes at the end), 32 chapters, all 8 silences of 15 s+ are writing. When a student speaks,
    a small Zoom tile with their display name shows bottom right (seen at raw 13:28, 22:17, 25:50):
    optional blur, like lesson 6's names column.
  - At the end of 11 a student asks for the previous lesson's recording; he answers it is on a
    computer in his Paris office and he will upload it at the end of the week. Nothing there says
    which file he meant.
  - 2025 recording (by an agent): 5 cuts (2:10; two are the silent screen switches iPad -> laptop
    at raw 0:23:27 and back at 0:45:58, ticked as judgment because private frames sit inside them),
    35 chapters. Parts on the edited timeline: correlation circle 00:00-22:57, PCA in R
    22:57-42:23, sparse PCA 42:23-end (a sparse-only video would start at raw 0:43:32, ~37 min).
    **Private on screen in the raw upload:** at raw 0:24:03-0:24:10 Chrome with a Google Drive
    folder URL (folder id visible), a window picker showing his Outlook inbox with his work address
    in a window title, Acrobat tabs; at ~0:46:03 the iPad home screen. Students' full names in the
    Zoom strip for the whole video (blur, like lesson 6).
  - Lesson 6 after the blur: 58:57 (3537 s, unchanged), captions serving, so its chapters stand.
- **Titles redone from his notes' section headers (2026-10-20, DECISIONS #14), local only:**
  6 "Էմպիրիկ միջին և կովարիացիոն մատրից։ Բազմաչափ գծային ռեգրեսիա", 7 "Նվազագույն քառակուսիների
  մեթոդ", 8 "ՆՔ-ի վիճակագրական հատկությունները։ Կանխատեսում", 9 "Գծային կապի վարկածի ստուգում։
  Հիմնական բաղադրիչներ", 10 "Տեսական հիմնական բաղադրիչների վերլուծություն", 11 "Տեսական և
  էմպիրիկ հիմնական բաղադրիչների վերլուծություն", 12 "Հիմնական բաղադրիչների գրաֆիկական
  ներկայացում", 13 "Կանոնիկ կորելյացիաների վերլուծություն". Chapters and descriptions switched to
  his terms (հիմնական, կանոնիկ, կորելյացիա). 6-9 on YouTube still carry the old titles.
  Section map: Ch. I (Gaussian) 1-6, Ch. II (linear regression) 1) intro 2) least squares
  3) statistical properties 4) prediction 5) linear hypothesis test, Ch. III (PCA) 1) intro
  2) theoretical 3) empirical 4) graphical, Ch. V CCA.
- **Thumbnails (2026-10-20):** made in the Canva design `DAHYkiiz7hc` ("Copy of thumbnails -
  մաթեմ", the user's trimmed copy): Arnak 6-13 from the lesson 5 page (topic font 38-49.5 to fit
  beside the Gaussian), and Ashot Դաս 5 from the Win95 Դաս 0 page (ArmSCII text). Exported by
  the user from Canva (1280x720) into `thumbnails/umath/bazmachap_06..13.png`.
- **Lecture PDFs moved to one folder (2026-10-20 23:40, user's request):** the math team's Drive
  folder "Բազմաչափ վիճակագրություն 1 - Առնակ Դալալյան - ԵՊՀ ԿՎՏԳ 2026 - դասախոսություններ"
  (https://drive.google.com/drive/folders/1vtvPDxKoD12JZXXuWqGRFRA4m6GcbX3J, anyone with the link
  can view; checked from a signed-out browser). Files `NN <topic from the title>.pdf` for 1-12
  (10 = 10a + 10b, 12 = 12a + 12b merged), plus README.txt with the backup link to the lecturer's
  own folder (https://drive.google.com/drive/folders/1w3IqwiA7HIdGsD_iZ-iSEXuIGeZBlqjK). Lesson 13
  has no PDF: its 📚 line is dropped. The 2025 recording links file 12.
  - Descriptions of 1-10 now link the new files (pushed, read back: all match). 11, 12 and the
    2025 recording have the links locally; they go up with the rest after their cuts are saved.
  - Old links, as a backup (lecturer's Drive): 1 1wsuQs2XnSCwi4UB7ygM4nnxz6Aggck6n,
    2 1J5C3Eej8plP6walAa8UbIo995CU9UF16, 3 1SSgZwlyHLB4I8EBUimMUX5alvt-zCXmq,
    4 1uogfioOSC-8wdgYzdl9zMm5kmQbCdKO4, 5 142i-BoWW49aoHuYnpLr4IZo4wCBZgD4_,
    6 1vgqjaeaeTK36bqj0s6zLqLpQfT8KqyVh, 7 1D-XrKhepX8YgyKVvxul6QlzkGgju_gYZ,
    8 1tdPx_ygccYp2OEJOTSjc9QTWlQb2tOG_, 9 1kb4Ap1UrfBIkgZ9PUYeBCC-_AWYi5J89
    (each as https://drive.google.com/file/d/<id>).
  - Lesson 10 is edited in Studio (the user's 13 cuts + 2 they added after the 8 s review): 996 s,
    chapters checked against its new captions; its description is pushed.
- **Pushed 2026-10-20 22:02-22:07 (user: "go"), all still unlisted:** titles of 6-13 (read back:
  all 8 match), thumbnails of 6-13, descriptions of 6 and 9 (only the term swap; 7 and 8 had no
  diff; read back: match). Not pushed: descriptions of 10-13 (chapters assume the planned cuts;
  push after the cuts are saved in Studio and the chapters are rechecked).
- Uploads of 2026-10-20 (user): kJMKNFHYlFU (the 2025 file), WFMoX0xRU6I (11), Bz6aVzkrqbM (12),
  syeGoSopVM0 (13), Hv7Jux-KYBk (10 part 2). Old private bJy5XvxZ2B8 deleted (it was not lesson
  11's raw). Local files match the uploads to within 1 s.
- Lessons 1-5: template thumbnail (title, "Դաս N", topic, 3D Gaussian), chapters with "․"
  separators. Lessons 6-9: a Zoom frame as thumbnail, chapters with " - " separators and English
  in parentheses (a first draft), day missing from the date line.
- Every lesson already links its lecture PDF. The lecturer's materials for lectures 1-8:
  his Drive folder from the 11 Apr email.
- Playlist order on 2026-10-20: 5, 4, 9, 8, 7, 6, 3, 2, 1, 11. Publish-date sort would give
  1, 2, 3, 6, 7, 8, 9, 4, 5, 11, so it has to be ordered by the lesson number in the title.
- Local raw files: `Desktop\misc\YSU OpenCourseWare\arnak\todo\arnak-04..08.mp4` (= lessons 4-8,
  46-76 min each); Premiere projects for lessons 1-3 only.
- The lecturer's position (10 Feb): "no comments; if already published, leave it". In April he
  asked for the remaining lectures to be published. Promised on 25 Apr: chapters fixed, title and
  thumbnail added, then public.
- **2026-10-21 00:10, cut plans after the owner's lesson 11 review (DECISIONS #17):**
  11: the owner's 48 cuts (`studio_cuts_to_enter.txt`, 1:02:08) + `proposed_additions_4s.txt`
  (24 proposals); 12: 45 cuts, 1:01:19; 13: 14 cuts, 1:01:27; 2025 recording: 43 cuts, 1:15:02.
  Chapters of all four moved and verified. None entered in Studio yet.
- **2026-10-21 01:00, lesson 11 list final:** the 48 were never entered in Studio, so the owner's
  review of the 18 extra proposals (22 cuts back) was merged in: 70 cuts, 12.9 min, -> 1:00:12
  (`studio_cuts_to_enter.txt`). Chapters remapped (32, smallest gap 38 s). Not entered yet.
- **2026-10-21 ~01:30, lesson 11 entered in Studio:** 70 cuts via the batch files, diff identical
  frame for frame. Waiting for the owner's Save; then description push after processing.
- **2026-10-21 02:15, lesson 11 done:** saved (59:59, the owner's 2 extra edits at raw 44:32 and
  47:24), chapters on the real captions, description pushed and read back. Pages of 12, 13 and 2025
  rebuilt with the timeline view (cut lists unchanged).
- **2026-10-21 (afternoon): lessons 12, 13 and the 2025 recording edited, published to their
  descriptions.** Cuts entered in Studio with the batch files (12: 66, 13: 34, 2025: 73), each
  `cut_list.py diff` identical, saved by the user; YouTube's new lengths matched the predictions
  (3625, 3625, 4385 s) and the new captions matched the predicted timelines to 0 ± 1 s. Chapters
  moved onto the real timeline and nudged onto the first word of their topic (12: 7, 13: 6,
  2025: 2, 1 s each); descriptions pushed and read back (37, 30, 35 chapters). 2025: "Sparse PCA"
  became his own "Նոսր ՀԲՎ" (his notes' header "Նոսր ՀԲՎ (Sparse PCA)", 2025 frame at 46:30) in
  the title (keeping "(Sparse PCA)"), 3 chapters and the note; thumbnail from the user's Canva
  export (`thumbnails/umath/bazmachap_12_2025.png`). Blurs: 2025 names strip and lesson 7 done by
  the user; 11 (student tile) and 13 (Chrome tabs) not needed, the user's call.
- **2026-10-21 16:35: all 14 videos public** (6-13 and the 2025 recording were unlisted; user: "pls set
  all arnak videos to public"). Through `videos.update(part=status)` with each video's current
  embeddable/license/publicStatsViewable/selfDeclaredMadeForKids sent back, read back: all public,
  madeForKids false, embeddable, standard licence. Playlist sorted by lesson (Manual ordering set in
  Studio), PDF folder link in its description. Overview page: `output/arnak_overview/overview.html`.
  End screens: lesson 1 done, the rest parked (DEFERRED_TODO).
- **2026-10-21 16:45: course DONE.** The user sent the closing email in the "Դասախոսությունների
  տեսագրություններ" thread (all 13 public with timestamps, descriptions and PDF links; one PDF folder,
  also in the playlist description; pauses and technical parts cut; lesson 10 as its recorded ~17 min;
  the 2025 recording as an extra after lesson 12 for its sparse PCA part; asked for lesson 13's notes).
  His earlier position: 10 Feb "no comments, leave it published"; 11 Apr "great work". Open: end
  screens for 2-13 + 2025 (parked, DEFERRED_TODO); his reply about lesson 13's notes.
