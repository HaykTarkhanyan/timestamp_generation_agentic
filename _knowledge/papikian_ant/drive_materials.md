# Papikian ANT course files on the math-team Drive (2026-10-22)

The user: "for all the files and extra materials pls create a folder in google drive like we did with
arnak and place them there and add links to it from here". Same pattern as Arnak
(`_knowledge/arnak_multivariate/status.md`, "Lecture PDFs moved to one folder").

- **Folder:** "Հանրահաշիվ և թվերի տեսություն - Միհրան Պապիկյան - ASOF 2024 - նյութեր" in
  **Մաթ Թիմ** (the math-team Google account), https://drive.google.com/drive/folders/1b8yBCAiiZgftMziYFeVQlvv8sf4Qqi04.
  Anyone with the link can view; checked from a signed-out browser context (folder lists all files,
  files open without a sign-in).
- **Made with:** the Playwright browser, where the math-team account is signed in at `drive/u/2` (the Drive
  connector of this setup is the user's personal account and cannot write there). New -> New folder;
  New -> File upload, then `browser_file_upload` with paths under `.playwright-mcp/` (the only folder
  the upload tool accepts); right-click -> Share -> Share; General access "Restricted" ->
  `menuitemradio` "Anyone with the link" (Viewer); file IDs from the rows' `data-id` attributes.
- **Contents (30 files, 220 MB),** from the site snapshot `_knowledge/papikian_site/algebra_number_theory_2024/`:
  - `NN <topic from the live YouTube title>.pdf` for the lecture notes, NN = the YouTube lesson:
    lecture 12's notes are `11-12 ...`, lecture 19's are `18-19 ...` (no lectures 11 and 18).
  - `14 ... - խնդիրներ.pdf` (lecture 14 problems).
  - `Տնային աշխատանք 1-5.pdf`, `Միջանկյալ քննություն - լուծումներ.pdf`, `Նախագիծ.pdf`.
  - `README.txt`: course, playlist link, the lecturer's site as the original source, the 11-12 / 18-19
    numbering, and the loose first page of the 18-19 notes.
- **File IDs:** `drive_folder_ids.json` (name -> Drive ID).

## Descriptions (all 21 videos of the playlist, pushed 18:40, read back: all match)

Only the 📚 block changed, 6 lines per video:
- the lecture-notes link: the lecturer's site page (`#h.gej4b75dpiyv`; Դաս 1 `#h.ctef3p3rdmzk`; Դաս 4 his
  Drive file `1qmLW6ji_...`) -> this lesson's notes in the folder;
- the homework / project / problems link: his Drive file -> our copy;
- new lines `Դասընթացի բոլոր նյութերը՝` + the folder link, before the textbooks line.

Everything before the change: `descriptions_before_drive_2026-10-22.json` (title and full description
of all 21, for a rollback). His original Drive files, as a second backup: Homework 1
`1Opo3KlF63nzEjy2VS3UmdS5A2hbGmcl0`, 2 `1D1ucEJU4kLAb542IHctwzwwIfMtdx0Nc`, 3
`1gKG6tAF23v4z3_a4Z4tBPLKdOXZVnyhD`, 4 `1GY_gmd4l6LTli-ltxf_H0MG9ikx3sNC4`, 5
`1uKmNo0ZS8Wvz-s3tPHG16SQ9LuWmV6bA`, project `1WYj9pcjeAPmoYUHCYxrrUYTC5lwyE4RF`, lecture 14
problems `1ajRB_5oOlgxD6EvIQIHiLD55C1GkQpz0` (each as https://drive.google.com/file/d/<id>).

**Site kept as a backup (20:41, user: "point both to site and to folder so there is backup"):** two more
lines after the folder link, `Դասախոսի կայքը՝` + the site link each video had before (Դաս 1
`#h.ctef3p3rdmzk`, all others `#h.gej4b75dpiyv`; Դաս 4, which linked his Drive file, got the common
one). All 21 pushed, read back: all match. The block now reads: notes file, homework copy, folder,
lecturer's site, textbooks.

The local `edited/description.txt` of 16-23 carry the same block. Later the same evening the user had
all 21 made public (16-23 were unlisted until then;
see `finish_16-23.md`).

**Midterm and project links (20:49, user: "when next is midterm or proj or exam put the material link
of that to description as well"):** Դաս 10 got `Միջանկյալ քննություն (լուծումներ)՝` + the midterm
solutions file, Դաս 11-12 got `Նախագիծ՝` + the project file (both after the homework lines). Read back:
match. No final-exam file exists for this course.
