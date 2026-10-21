# Ինֆորմացիայի տեսություն (spring 2026): what was recorded, and where it is

Ashot Harutyunyan's course for the YSU ASDS master's, Fridays, room 243. Rebuilt on 2026-10-20 from
three Telegram chats (the filming group, a student who filmed, the lecturer), the Drive folder
screenshot `2026-10-20_drive_info_folders.png`, and the YouTube API. People other than the
lecturer are given as roles; the chats themselves stay out of this public repo.

Drive folder `info_NN` holds Friday NN of the course, so YouTube `Դաս N` is `info_(N+1)`.

| Fri | Lecture | Recording | Drive | YouTube |
|---|---|---|---|---|
| 6 Feb | intro | filmed; camera placed badly, low quality. Lecturer: "only a small part usable" | info_01 (in `Done`?) | Դաս 0, public. Lecturer's cut 48:35-49:56 (exam talk) made |
| 13 Feb | entropy | filmed; lecturer's hand often on the pocket with the phone, quiet voice | info_02 (in `Done`?) | Դաս 1, public |
| 20 Feb | conditional entropy, MI | filmed with the new tripod; projector glitch at 38:30 and 40:30 cut | info_03_feb_20 | Դաս 2, public, 1x speed |
| 27 Feb | KL divergence | filmed; mic rustle | info_04_feb_27 | Դաս 3, public, 1.25x. Lecturer approved cutting 14:10-14:38 |
| 6 Mar | Fano, cross-entropy | filmed; **video starts ~1 min after the audio** (filmer stepped out); dark | info_05_mar_06 | Դաս 4, **unlisted, title "ToDo"**, date blank |
| 13 Mar | AEP, typical set | filmed | info_06_mar_13 | Դաս 5, **unlisted, title "ToDo"**, date blank |
| 20 Mar | **substitute lecturer** (sound processing and AI applications) | **not filmed, by agreement**: the lecturer was unavailable, the substitute preferred not to be filmed, and the topic is not core | info_07_mar_20 (made in advance on 14 Feb; probably empty) | none, correctly |
| 27 Mar | ? | filmed on a classmate's phone; **last ~10 min of video missing** (recording stopped); audio complete (the recorder ran ~18 h). Plan: show the slides over the audio for the gap | info_08_mar_27 | **not uploaded** |
| 3 Apr | - | **no class** | - | - |
| 10 Apr | ? | **no mention in any chat, no Drive folder** | - | - |
| 17 Apr | ? | filmed (the team nearly forgot; the lecturer was late) | info_09_apr_17 | **not uploaded** |
| 24 Apr | - | no mention, no folder; Remembrance Day, a public holiday | - | - |
| 1 May | - | no mention, no folder; Labour Day, a public holiday | - | - |
| 8 May | ? | filmed; equipment left with the lecturer afterwards | info_may_08 | **not uploaded** |
| 15 May | ? | **no mention, no folder** | - | - |
| 22 May | channel capacity (planned) | **not filmed**: "almost the whole class was absent" (lecturer, 26 May). He would like 1-2 lectures filled in later | - | - |

## Agreements with the lecturer that still apply

- **Send every video to him before it goes public** (25 Jan). He replies within hours.
- **Speed: 1.25x from Դաս 3 on** (26 Feb, after he asked for 2x twice). Speech rate in the YouTube
  captions, words per minute: Դաս 0: 84, 1: 91, 2: 84, **3: 98, 4: 106**, **5: 85**. So 3 and 4
  are sped up and Դաս 5 most likely is not. His last message on it was ambiguous ("if the
  original sounds fine to you, keep the original"). The user decided on 2026-10-20 not to
  pursue the speed question.
- **Slides:** he uploads them to the ASDS Drive after each lecture; we offered to link them from
  the descriptions (17 Feb, agreed). All six descriptions still say "[կավելացվի շուտով]".
- His wording fixes are in: "Կոլմոգորով" (Դաս 0), "խմբավորում" for clustering (Դաս 2).
- He asked on 16 Mar whether Դաս 4's sound is audible; it sounded fine to us, but it was never
  measured.

## Slides (the user's zip `InformationTheory_ASDS_Lecture Slides.zip`, 2026-10-20)

The lecturer numbers lectures by count, and each deck is cumulative ("Lectures 6-10" = the part-3
deck as of lecture 10). The deck posted for each Friday:

| Deck | Posted | Friday | Lesson |
|---|---|---|---|
| Intro-L-1 (14 p) | 6 Feb | 6 Feb | Դաս 0 |
| Intro-L-1-extended (36 p) | 13 Feb | 13 Feb | Դաս 1 |
| L-3, "Lectures 2-3" (28 p) | 20 Feb | 20 Feb | Դաս 2 |
| L-4, "2-4" (53 p) | 27 Feb | 27 Feb | Դաս 3 |
| L-5, "2-5" (82 p) | 9 Mar | 6 Mar | Դաս 4 |
| L-6, "Lecture 6" (21 p) | 13 Mar | 13 Mar | Դաս 5 |
| (no L-7) | | 20 Mar | substitute lecture |
| L-8, "6-8" (39 p) | 27 Mar | 27 Mar | Դաս 6 (has the slides for the missing last 10 min) |
| **(no L-9)** | | **10 Apr?** | **probably held, not filmed** |
| L-10, "6-10" (71 p) | 17 Apr | 17 Apr | Դաս 7 |
| L-11, "6-11" (100 p) | 8 May | 8 May | Դաս 8 |
| **(no L-12)** | | **15 May?** | **probably held, not filmed** |
| ChannelCapacity-L-13-end, "Lectures 13-" (78 p) | 22 May | 22 May | not filmed (class absent) |

Lecture 7 counts the substitute's Friday (lecture 8 is 27 Mar). 3 Apr had no class, and 24 Apr and
1 May were holidays, so with one lecture per Friday, L-9 = 10 Apr and L-12 = 15 May. No Drive folder,
no chat message and no deck exists for either. Not confirmed; the first minutes of the 17 Apr and
8 May recordings ("last time we...") or the students would settle it. The lecturer wrote on 26 May
that "1-2 lectures" are worth filling in later.

## Local files (checked 2026-10-20)

- `Desktop\misc\YSU OpenCourseWare\info\` holds only Premiere projects for Դաս 0-5 (`done\info_01`
  to `info_04`, then `info_04_0_indexed` = Դաս 4 and `info_05_0_indexed` = Դաս 5: the project names
  switched to 0-based numbering at Դաս 4). Their raw `.MOV` / `.mp3` sources are gone; the projects
  point at the old path `Desktop\YSU OpenCourseWare\info\`. The intro and outro clips are one level up.
- `Downloads\info_09_apr_17.mp3`: the 17 Apr audio, 72.8 min, 192 kbps.
- No Premiere project and no media for 27 Mar, 17 Apr (video) or 8 May.

## Open

1. Check the Drive folders: is info_07 empty, what is in `Done`, and do 08 / 09 / may_08 have both
   video and audio?
2. Was there a lecture on 10 Apr or 15 May? Nothing in the chats either way.
3. DONE 2026-10-20: Դաս 4 and 5 thumbnails set (see Thumbnails below). (Titles, dates and chapters in the Դաս 0-3 style were pushed on
   2026-10-20; both still unlisted. No editing needed: 16 and 28 silences of 3 s+, longest 5.4 s
   and 7 s; nothing in the transcripts worth cutting.)
4. Դաս 6 (27 Mar), 7 (17 Apr), 8 (8 May): edit, upload, send to the lecturer.
5. Playlist order (now 3, 2, 1, 0, 4, 5); publish; slide links.

## Terms in titles: his own words (checked 2026-10-20)

The slides are in English; the Armenian titles use what he says in class. Դաս 4: "Ֆանոյի
անհավասարությունը" (38:29), "խաչաձև էնթրոպիան" (59:09; titles keep the standard spelling
էնտրոպիա). Դաս 5: "հավասար բաժանումների սկզբունք" (6:19, 15:45), "տվյալների սեղմում",
"տիպական / ոչ տիպական". Same rule as Arnak's course (DECISIONS #14).

## Thumbnails (2026-10-20)

Դաս 4 and 5 made in the Canva copy `DAHYkiiz7hc` from the Win95 Դաս 0 page; the joke texts in
its two buttons ("© Շենոն", "ծիծիկ") were replaced with "< Back" / "Finish", as on the published
Դաս 0, 2, 3. The text is ArmSCII in a legacy font: in the browser editor "և" (0xA2) is drawn as
"§", but Canva's PNG export renders it correctly. Files: `thumbnails/umath/info_theory_04.png`,
`info_theory_05.png` (1280x720, Canva export).
