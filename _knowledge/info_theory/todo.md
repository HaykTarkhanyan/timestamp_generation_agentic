# Ashot - Ինֆորմացիայի տեսություն: todo for Դաս 6-8 and the course (set up 2026-10-23)

Facts behind this list: `recording_timeline.md` (same folder). Raw files: `Desktop\misc\YSU OpenCourseWare\info\<Drive folder>\`
(the QYSU VIDEOS Drive account: My Drive > 25-26 2 > Info). YouTube `Դաս N` = Drive `info_(N+2)`
from Դաս 6 on (20 Mar, the substitute's Friday, has no video).

| Դաս | Friday | Raw video | Separate audio | Known problem |
|---|---|---|---|---|
| 6 | 27 Mar | `info_08_mar_27\Info-27-03.MOV` (3.38 GB) | `27 Information Theory.mp3` (17 h recorder file, 1.37 GB) | video stops ~10 min before the end; audio complete |
| 7 | 17 Apr | `info_09_apr_17\info_09_apr_17.MOV` (4.34 GB) | `Downloads\info_09_apr_17.mp3` (72.8 min) | the team nearly forgot to film; lecturer was late |
| 8 | 8 May | `info_may_08\IMG_3880.MOV` (5.01 GB, 73.1 min, 1920x1080 29.97 fps) | none (the camera's own sound) | |

**Audio vs video (measured 2026-10-23, `scripts/archive/info_theory_2026-10/ashot_align.py`: 1 s loudness envelopes, best correlation):**
- Դաս 6: the camera starts **201 s** into the recorder file (corr 0.84) and ends at 3820 s (1:03:40); the
  recorder has speech until ~1:20 and goes quiet at ~1:21, so ~17 min (not 10) of the end has no video.
- Դաս 7: the camera starts **230 s** into the mp3 (corr 0.90) and ends at 4305 s; the mp3 runs to 4366 s.
- Դաս 8: camera sound only.

**Transcripts without uploading the 5 GB videos (the user's idea, 2026-10-23):** black 640x360 1 fps videos
carrying the audio (`scripts/archive/info_theory_2026-10/blank_video.py`), uploaded by the user, captions fetched from YouTube. Their
timelines: Դաս 6 = recorder 0:00-1:22:00 (video = recorder - 201 s); Դաս 7 = the whole mp3 (video = mp3 - 230 s);
Դաս 8 = the camera's own timeline. Files in `Desktop\misc\YSU OpenCourseWare\info\captions_upload\`.
- [x] Uploaded by the user to umath, 2026-10-23 23:18: Դաս 6 `P7nf8jFgm0o`, Դաս 7 `qv8yr8Ml7Yo`, Դաս 8 `rtueGKrucms`
- [x] Captions fetched 2026-10-24 00:20. The user uploaded the 3 as **private**, so yt-dlp can't read them; the
      API with the umath login can (`captions.list`, then `captions.download` tfmt=vtt: same auto-caption VTT
      with per-word tags; ~750 quota units for the 3). Cleaned with `fetch_subtitles.parse_vtt` into
      `transcripts/das6_P7nf8jFgm0o.txt` (1511 lines), `das7_qv8yr8Ml7Yo.txt` (1365), `das8_rtueGKrucms.txt` (1423),
      VTTs next to them. Timelines as above (Դաս 6, 7: the separate audio's; Դաս 8: the camera's).
- [ ] Decide later whether to delete the 3 temp videos.
- Clues so far: Դաս 6's lecture goes on after the camera stops (1:03:40 in the recorder: Kraft's inequality,
  code lengths, the minimisation problem, until ~1:20). Դաս 8 opens with "Հիշում եք որտեղ էինք կանգ առել երկու
  շաբաթվա..." ("remember where we stopped two weeks ago"), although 17 Apr is three weeks before 8 May.

## 0. Downloads

- [x] All four files (2026-10-23 22:31-23:02): Դաս 6 audio and Դաս 8, 7 video via Playwright; Դաս 6 video (3.63 GB, 60.3 min) by the user in Chrome (Playwright keeps two copies while saving, and C: was too full for that)
- [ ] Keep C: above 5 GB free (21 GB before the downloads, ~7-8 GB after). Delete each raw MOV only after its
      lecture is uploaded, processed and approved; the Drive keeps the originals.

## 1. Consistency with the published Դաս 0-5 (check before editing anything)

Checked 2026-10-24 from the Premiere projects (`info\*.prproj`, `done\`, `Adobe Premiere Pro Auto-Save\`;
gzipped XML, read with `scripts/archive/info_theory_2026-10/prproj_tracks.py`) and `yt-dlp -F`. Decisions in DECISIONS #28.
YouTube ids: Դաս 0 `U3BbIALq4aM`, 1 `4IO6iU7rRTA`, 2 `N3LL6k55sao`, 3 `bHyOK-SSawI` (in the playlist, missing
from the API's uploads list), 4 `fHPN7fJEusA`, 5 `0WSFqm9E-Pc`; playlist `PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy`.

- [x] Intro and outro: `intro-attemt-2.mp4` (6.46 s) and `outro-attempt-2.mp4` (5.78 s), 1080p 25 fps 48 kHz
      stereo, at 1x before and after the sped-up lecture (Դաս 2, 4, 5 projects).
- [x] Frame rate: Դաս 0, 2, 4, 5 are 1080p **25 fps** on YouTube (Premiere sequences at the intro's 25 fps),
      Դաս 3 is 30. Output 25 fps.
- [x] Audio: the **recorder** mp3 on the timeline, camera sound muted (Դաս 2, 4, 5). Same for Դաս 6 and 7;
      Դաս 8 has only the camera's.
- [x] Speed: `PlaybackSpeed` 1.25 in Դաս 3's and 4's projects, none in Դաս 5's: Դաս 5 really is 1x (matches
      the 85 words per minute). Still open: redo Դաս 5 at 1.25x? (Q38)
- [x] Picture: every project had Lumetri exposure -1.1 to -1.9 (Դաս 4 +1.0; it was dark). **The raw Դաս 6-8
      are iPhone HDR** (HEVC 10-bit, HLG, BT.2020): none is dark; read as SDR they look washed out (mean
      luma 177-191 vs 138-153 published). Tone map hable npl 200 -> 143-158, like Դաս 2-5. Contact sheets:
      scratchpad `frames/contact_sheet.jpg`, `tonemap2/npl_sheet.jpg`.
- [ ] Դաս 6's camera is a classmate's phone: tighter framing, the lecturer often half out of the frame on
      the right (seen in the contact sheet). Nothing to fix, just expected.
- [ ] Title format, description template (lecturer line, date line, the slides line, chapters header,
      hashtags), chapter style: copy Դաս 4 / 5, which were done on 2026-10-20.
- [ ] Thumbnail: the Win95 page in the Canva copy `DAHYkiiz7hc` (ArmSCII text, "< Back" / "Finish" buttons;
      the browser editor draws "և" as "§", the PNG export is right). Same for 6-8.
- [ ] Terms in titles: his own words from the recording, glossary otherwise (as for Դաս 4 / 5).

## 2. Per lecture (Դաս 6, 7, 8)

- [x] Sync the separate audio to the video: `scripts/align_audio.py` -> `render/align_das6.json` (offset
      200.869 s, drift -5.9 ppm, +-33 ms scatter from room acoustics), `render/align_das7.json` (230.047 s,
      -11.4 ppm, 3 ms). Checked through the render's own graph with `scripts/non_essential/render_sync_check.py`.
- [x] Render script: `scripts/render_lecture.py` (cuts, 1.25x, tone map, recorder audio, intro/outro, one
      pass). 12 s sample of Դաս 7 OK (scratchpad `render_test/d7_w12_qsv.mp4`, 2 Mbps). Not yet: a full
      render (ask first; ~1-1.3 h per lecture, all cores, a guess), Դաս 6's slides-over-audio tail.
- [x] Դաս 6's slides over the sound (2026-10-24): `render/tail_slides_das6.txt` (slide 38 from the camera's end,
      slide 39 from 1:05:47.8 to the end), images in `info\slides\png\`, `render_lecture.py --tail-slides
      ... --slides-dir ...`. Straight cut from the camera (on the room screen: slide 38) to the full-screen
      slide; samples `output/2026-10-24_info_theory_samples/video/das6_camera_to_slides.mp4`,
      `das6_slide38_to_39.mp4`. The user: straight cut (Q43), keep 39 to the end (Q45); every picture jump
      dips to black (DECISIONS #30, samples `das6_camera_to_slides_dip.mp4`, `das8_cut_dip.mp4`).
- [ ] Դաս 6 description: say that the recording stopped ~13 min before the end (after 1.25x), so that part
      shows his slides with the sound.
- [ ] (was) Դաս 6: the last 16 min 45 s (recorder 1:03:40-1:20:25) have audio only: show his slides over the audio
      (deck L-8, "Lectures 6-8": prefix codes, Kraft's condition, minimising the expected length). The lecture ends at
      1:20:25; the rest of the recorder is chatter.
- [ ] Edit points: content cuts only, borderline pauses as unticked suggestions, no silence rule (DECISIONS
      #29: a fixed camera makes every cut a visible jump). Plan, review on studio.html, then the render.
      Դաս 8 first (2026-10-24): `output/2026-10-24_Das-8-Informaciayi-tesutyun_rtueGKrucms/` (metadata.json
      carries fps 30 and `silence_margin_db` 8: the camera mic's floor is -57.8 dB and +20 marked 97% as
      silent), 2 ticked cuts + 1 suggestion, keyframes-only 360p preview. Render with `--gain-db 13`.
      Դաս 7: `output/2026-10-24_Das-7-Informaciayi-tesutyun_qv8yr8Ml7Yo/` (audio = the mp3, master time;
      margin 10 dB): 0:00-5:23 (quiz talk, mic) and after 1:11:42 ticked, 2 suggestions; -6.5 min.
      Դաս 6: `output/2026-10-24_Das-6-Informaciayi-tesutyun_P7nf8jFgm0o/` (audio = the caption upload, the
      recorder's first 82 min; margin 12 dB): 0:00-3:18 setup, 3:18-7:39 logistics (Davit's session, the
      quiz), after 1:20:37 ticked (check the end by ear), 2 suggestions; -9.0 min. 1:03:40-1:20:25 is
      sound only: pauses could be cut freely there (no picture to jump).
      Their previews: `scripts/archive/info_theory_2026-10/aligned_preview.py` (black where the camera has no picture, keyframes
      placed by the align JSON, the WAV's own source as sound); worth moving to scripts/non_essential.
- Sample answers (2026-10-24): picture (hable npl 200) good; +10 dB better, "add a bit more" -> +13;
  1.25x fine.
- Reviewed cut lists (2026-10-24), saved as `studio_cuts_edited.txt` in each folder, `cut_list.py check` OK:
  Դաս 6 2 cuts (to 7:55.8; from 1:20:09.2, kept although 0.1 s into a sound), -9.8 min; Դաս 7 2 cuts
  (to 5:25.9; from 1:11:42), -6.5 min; Դաս 8 4 cuts (to 0:14.8; 7:13.7-7:15.0; 7:20.3-7:31.6; from 1:13:00.4),
  -0.5 min. Denoise "light" (`--denoise`) for 7 and 8 (the user), 6 too (same recorder type).
- Դաս 8 sound, final (DECISIONS #32): **no gain, light denoise** (the user, after +13 / +16 had been judged on a
  player set low). -28.9 LUFS on 7:05-7:45. The 144p check copy still has +13 (only the volume differs).
  Final renders with ffmpeg 9 (DECISIONS #31).
- Check renders first (the user: 144p of the whole video, then 1080p): `--check` = 256x144, camera keyframes
  only, everything else final; into each folder's `video/`.
- [x] Speed-up 1.25x, intro and outro, 1080p renders: Դաս 8 752 MB, Դաս 7 888 MB, Դաս 6 564 MB (57:59, A/V
      both 3478.92 s, 58.7 min to render), all with ffmpeg 9 in the background (one reaped, restarted by the user).
- [x] Uploaded unlisted and finished (2026-10-24): Դաս 6 `LRQ6r_DaAVU`, 7 `S8vcM74HZVE`, 8 `LOHGyVgaIuI`.
      Chapters from each video's own captions, Codex-reviewed (`scripts/archive/info_theory_2026-10/codex_info_prompts.py`,
      originals in `timestamps_before_codex.txt`), titles (Q44, Q63), descriptions in the Դաս 4/5 template with
      the slides block, Դաս 6's note about the slides at the end (shortened by the user in Studio), thumbnails
      from the user's Canva export (`thumbnails/umath/info_theory_05..08.png`, 5-8 re-exported once). Read back.
- [x] Դաս 4/5 quality check (Codex + transcript): boundaries and titles fine; 10 imprecise labels fixed and
      pushed (Դաս 5 05:02 "analogue" -> "consequence of the weak LLN", Դաս 4 45:20 "խիստ" -> "cannot be improved").
- [x] All 9 chapter lists nested like Metric Academy, H:MM:SS over an hour (DECISIONS #34), pushed, read back.
- [x] Final audit of all 9 (`scripts/archive/info_theory_2026-10/audit_info.py`): every check passes except Դաս 3's
      27 s gap (10:57 -> 11:24), an old public list, YouTube's floor is 10 s. Overview page:
      `videos_overview.html` (standalone, all 9 at a glance).
- [ ] **Waiting on Ashot:** the user sends him the message (Telegram, Armenian, links + titles of Դաս 4-8, slides
      folder, 1.25x except Դաս 5, Դաս 6's lost picture). Public only after his OK (agreement of 25 Jan); then
      make 4-8 public with their own status fields, read back.

## 3. Course-wide

- [x] 10 Apr: the written quiz, not a lecture (transcripts, 2026-10-24; `recording_timeline.md`). 17 Apr -> 8 May:
      no missing lecture, Huffman's construction most likely in the TA's session.
- [ ] 15 May: still unknown; ask him.
- [x] Slides found and mapped to lessons (2026-10-24): `slides_map.md` (the zip was on the Desktop; extracted
      to `info\slides\Lecture Slides\`). Draft titles for Դաս 6-8 there too.
- [x] Slides (2026-10-24, DECISIONS #33): folder "Ինֆորմացիայի տեսություն - Աշոտ Հարությունյան - ԵՊՀ ԿՎՏԳ
      2026 - սլայդներ" on the math-team Drive (IDs in `drive_folder_ids.json`), 4 final decks + README,
      anyone with the link can view (checked signed out). The 📚 block of Դաս 0-5, 7, 8 now has the page
      range, the deck link and the folder link; pushed and read back (`descriptions_after_slides_2026-10-24.json`;
      before: `descriptions_before_2026-10-24.json`). Դաս 6 (`LRQ6r_DaAVU`): pages 22-39, with its chapters.
- [ ] Դաս 4-8 are unlisted: public together after his OK (the user's word, then the API).
- [x] Playlist into lesson order (2026-10-24): `sort-playlist --by lesson --apply` moved 5 of 9 (it was
      already Manual), read back Դաս 0-8 in order.
- [ ] Message him: drafted 2026-10-24, the user sends it. Still to ask: 15 May (Q36), the 1-2 lectures he wanted to add.
- [ ] Delete the 3 private audio-only caption uploads (`P7nf8jFgm0o`, `qv8yr8Ml7Yo`, `rtueGKrucms`) in Studio (the user).
- [ ] End screens (Q46), Դաս 5 at 1.25x (Q38): open, the user's call.
