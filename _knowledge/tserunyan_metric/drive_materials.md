# Tserunyan's course files on the math-team Drive (2026-10-23)

The user, asked whether to put her files on the math-team Drive "as for Arnak and Papikian": "yes
upload". Same pattern as Papikian (`_knowledge/papikian_ant/drive_materials.md`).

- **Folder:** "Մետրիկական տարածություններ և տոպոլոգիա - Անուշ Ծերունյան - ASOF 2023 - նյութեր" in
  **Մաթ Թիմ** (the math-team Google account),
  https://drive.google.com/drive/folders/1HcmQLDevenreXek6CpK22JORez5F7Jdm. Anyone with the link can
  view; checked from a signed-out browser context (the folder lists its files, `Տնային 12` opens
  without a sign-in).
- **Made with** the Playwright browser signed in at `drive/u/2`: New -> New folder; New -> File upload
  from `.playwright-mcp/drive_upload_metric/` (40 files, 287 MB, uploaded in ~3.5 min); right-click ->
  Share -> Share -> General access "Anyone with the link" (Viewer). Staged by scratchpad
  `metric_drive_stage.py` from `_knowledge/tserunyan_site/`.
- **IDs:** `drive_folder_ids.json` (name -> Drive ID). The folder view loads only ~26 rows; the rest
  were read from Drive search (`<word> parent:<folder id>`).
- **Contents (41 files):**
  - `NN <topic>.pdf`, her notes of lecture NN; the topic is that lesson's YouTube title. Lectures 1
    and 7 were never recorded: `01 Մետրիկական տարածության սահմանումը (տեսագրված չէ).pdf` and
    `07 Լրիվացում (տեսագրված չէ).pdf`, topics from her notes. YouTube "Դաս 1-2" is lecture 2.
  - `Տնային N - <topics>.pdf`, homework 1-12, named by their problems (the user: "name the homeworks
    semantically ... just say Tnayin 1 - topics").
  - `README.txt`: course, playlist, her page as the original source, the numbering.
  - `00 Դասընթացի նկարագիր.pdf`, her course info sheet (`Metric_and_Top.2023S.pdf`) with the TA's
    personal email redacted (the user: "just obfuscate the email and upload"): PyMuPDF true redaction,
    "[email removed]" in its place, the address gone from the text layer and the file bytes; her McGill
    address stays (the sheet tells students to write to it). Scratchpad `redact_ta_email.py`.

## Descriptions

Local `edited_predicted/description.txt` of 15-27 (not on YouTube yet), by scratchpad
`metric_desc_materials.py`: the 📚 block is now this lesson's notes in the folder, the homework copy
(series rule; Դաս 27 links hw12, the user's "link last"), the folder, her course page as a backup,
the textbooks. Backups of the old files: scratchpad `desc_before_drive/`.

The published 1-14 (Դաս 1-2, 3-6, 8-14): the user said yes (Q13), to go with the other pushes after the
09:00 quota reset. Scratchpad `metric_1_14_drive.py` (`plan` / `push` / `check`) reads the live text and
replaces only the 📚 block, keeping each video's homework number; the backup goes to
`descriptions_before_drive_2026-10-23.json`. Dry run from yt-dlp text: all 12 parse. None of the 12 is in
the pending audit batch 2.
