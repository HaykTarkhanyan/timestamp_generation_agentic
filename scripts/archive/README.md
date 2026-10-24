# archive

One-off scripts kept as a record of how something was done. Not expected to still run (paths, video ids
and the scratchpad layout of the session that wrote them are baked in), and never imported by live code.
They use `print`, not logging: promote one to `non_essential/` (and give it logging) before reusing it.

## info_theory_2026-10/ (Ashot Harutyunyan, Ինֆորմացիայի տեսություն, Դաս 4-8; moved 2026-10-24 from the session scratchpad)

| script | what it did | when you would look at it again |
| --- | --- | --- |
| `ashot_align.py` | First, coarse audio alignment: 1 s loudness envelopes of the 17 h recorder file and the camera, best correlation (Դաս 6: 201 s, Դաս 7: 230 s). | Superseded by `scripts/align_audio.py` (cross-correlation at 8 kHz, drift fit). Only for the streaming trick on a 17 h file. |
| `blank_video.py` | Black 640x360 1 fps video carrying a lecture's audio, uploaded private to get YouTube's auto-captions without uploading the 5 GB camera file. | The next course with raw files and no captions. Worth promoting to `non_essential/`. |
| `aligned_preview.py` | 360p studio.html preview for a lecture whose sound is a separate recorder: camera keyframes placed by the align JSON, black where the camera has no picture. | The next classroom recording with a separate recorder (edit-point review). Worth promoting. |
| `prproj_tracks.py` | Read a Premiere `.prproj` (gzipped XML): which media each track uses, mute / volume, Lumetri values. Used to copy Դաս 2-5's intro, outro, speed and audio choices (DECISIONS #28). | When a lecturer's earlier videos were cut in Premiere and the new ones must match. |
| `deck_titles.py`, `deck_pages_text.py` | Page titles of every slide deck and which pages each deck added; text of a page range plus the check that page numbers stay the same across the cumulative decks. | Mapping slides to lessons for another course with cumulative decks (`_knowledge/info_theory/slides_map.md`). |
| `codex_info_prompts.py`, `codex_info_run.sh` | Codex review of the chapter lists and titles: one prompt per lesson with the slides and the transcript inline, `codex exec -s read-only`, ~55-62 s per lesson. | Pattern for the next independent review (see `_learnings/2026-10-24-2041_codex-chapter-review-useful-but-check-each-claim.md`). |
| `stage_ashot_drive.py` | Copied the 4 final decks under their Drive names plus a README into `.playwright-mcp/drive_upload_ashot/` for the Playwright upload (DECISIONS #33). | Rebuilding the Drive folder. |
| `ashot_materials.py` | Put the 📚 block (page range, deck link, folder link) into the live descriptions of Դաս 0-5, 7, 8, checking local copies against live first. | Same change on another course. |
| `nest_info_chapters.py` | Nested the chapter lists of all 9 videos (4 spaces, one level, a parent has 2+ children) and wrote videos over an hour as H:MM:SS, from the live descriptions (DECISIONS #34). | Nesting another course's chapters. |
| `audit_info.py` | Read-only audit of the 9 videos: title format, date line, slide links and pages, chapters, `<` `>`, length, thumbnail, playlist. | Before making Դաս 4-8 public. |
| `build_info_overview.py`, `info_playlist_dump.py` | Built `_knowledge/info_theory/videos_overview.html` (all 9 videos at a glance, standalone) from the live data; dumped the playlist's titles and descriptions to JSON. | Refresh the overview page after a change. |
