# Finishing a umath course: the playbook (from Papikian 16-23, for Tserunyan 15-27 next)

Written 2026-10-22 after Papikian's «Հանրահաշիվ և թվերի տեսություն» (7 new lectures, 21 videos in all)
went from raw Zoom files to public, linked, reviewed and announced. Next: Anush Tserunyan's «Մետրիկական
տարածություններ և տոպոլոգիա», 13 new lectures (15-27), already uploaded unlisted with content-only cut
plans (`_knowledge/umath_todo.md`, `_knowledge/tserunyan_metric/standard.md`). Each point says what
happened and what to do differently.

## 0. Set up before touching videos

- **Read the series standard first** (`_knowledge/<course>/standard.md`): title, description layout,
  dates, homework rule, chapter notation. Papikian's standard grew notation rules during the review
  (disc(K), H(K), N(I) vs Nr(α), state hypotheses like I ≠ 0); write such rules in the standard as soon
  as they are decided, so lectures processed later do not drift.
- **Keep one working file per run** (Papikian: `_knowledge/papikian_ant/finish_16-23.md`): tasks with
  status, the video table, open decisions. It survives context compaction; read it first after one.
- **Snapshot the lecturer's site into the repo** (`_knowledge/papikian_site/`): notes, homework, dates,
  and the contact email were all needed later. Tserunyan's course page is the McGill site.

## 1. Cuts: calibrate on one lecture before planning all of them

- Papikian's cut rule changed four times: content only, then pauses from 4 s, then back to content only
  ("match the style of older papikian videos"), then, after the user hand-edited Դաս 16 (128 cuts, 16 min:
  "mihran is awful at this i had to add cuts"), pauses from 6 s + hum joins (DECISIONS #22, #23). Each
  change meant replanning and remapping every lecture.
- **For Tserunyan: the user reviews and edits ONE lecture in Studio first** (Դաս 15), then the rule is
  fixed (content only as now, or 6 s / 4 s pauses on top) and only then the other 12 are applied. Her
  plans already keep both versions (`*_v1_content_only` active, `*_v2_4s`).
- Studio entry: JS loop through Playwright in batches (DECISIONS #18). After the first cut of each video,
  read back what Studio stored: on some uploads it stores every cut one frame late; then use
  `--type-shift -1` (`_learnings/2026-10-22-1640_...`). Never navigate away from an editor with unsaved
  cuts; cancelling a Playwright call does not stop code already running in the page.
- No cut touches the ASOF intro (0:00-0:08.55) or the outro (last 7.51 s).
- Tserunyan-specific: blur checks are open (Դաս 15 name tag, Դաս 22 students' names, start cuts of
  20 / 26 / 27 hide an email address and her bedroom if unticked).
- **Keep privacy flags in proportion** (the user, 2026-10-23): raw unlisted uploads may stay in the playlist
  while they wait for their cuts ("16-27 no its fine"), and an address the lecturer already publishes on her
  own site is not a big deal ("don't make such big of a deal out of it"). Mention such things once, in one
  line; keep the real checks (a stranger's face or name on screen) for the review.

## 2. Chapters after the cuts are saved

- Fetch the edited video's own captions (`fetch_subtitles.py`); if yt-dlp is bot-blocked, catch the
  player's timedtext request in Playwright (`_learnings/2026-10-22-0338_...`).
- The predicted remap was right to +-1 s on all 7 (`edited_predicted/` -> `edited/`).
  `scripts/non_essential/snap_chapters_to_captions.py` then moved 46 of 181 chapters by 1-3 s onto the
  first word of the topic. Keep that order: remap, snap, verify.
- Run `glossary_check.py` (stage 3 of the skill) and the verifier on every list. The denylist catches
  terms already corrected once (չօրինակ -> հակաօրինակ, ինչու՞ -> ինչո՞ւ, ...).
- **Nest and format like Metric Academy** (Ashot's course, 2026-10-24, DECISIONS #34): sub-chapters 4 spaces
  in, one level, 2+ children per parent; a video over an hour writes every time as `0:00:00`. Ask whether
  the other umath courses should follow before their next push.
- Make a description line start with a word, never a time ("ℹ️ ... 45-րդ րոպեից ..."), so it cannot be
  taken for a chapter.

## 3. Review: two independent readers, then reconcile against the transcript

- One Claude agent (report only) + Codex (`codex exec`, read-only, material inline; 7 runs took 652 s).
  Then every claim checked against the transcript and per-word caption times before anything changes:
  67 of 181 chapters changed, titles of 4 of 7 changed.
- Codex was strongest on missing hypotheses; Claude (which also had the notes and word times) on
  boundaries and cross-lecture consistency. 10 of Codex's 12 plain boundary moves were wrong: they would
  have pushed the "Լավ, հիմա..." turn sentence into the previous chapter. Do not apply boundary moves
  without the word times.
- Neither reviewer caught "Չօրինակ"; the glossary check now does. A final read just before the push
  still caught Դաս 20 "Cl(K)" against the agreed "H(K)": always do one last read.
- **Cost:** ask before any fan-out. Tserunyan's drafts already took 4 agents and 2.01M tokens; 13
  lectures through two reviewers is roughly twice Papikian's review.
- Lecture mistakes (Papikian 16 Carlitz, 21, 23 (m+1)^n; Tserunyan 17, 18 "Egorov" for Lusin, 19, 24,
  27): **no correction notes on umath** (DECISIONS #25, the user 2026-10-23: corrections are only for
  their own Metric Academy videos). A slip only shapes the chapter label; keep the finding unpublished.

## 4. Materials

- The user wanted the course files in a public folder on the math-team Drive (Arnak, then Papikian),
  each video's 📚 block linking that lesson's notes and homework copy, the folder, and the lecturer's
  site as a backup ("point both to site and to folder so there is backup"), plus the midterm / project
  file on the lecture right before it. Expect the same for Tserunyan; ask first.
- The folder is made through Playwright where the math-team account is signed in (`drive/u/2`); the Drive
  connector here is the personal account and cannot write there. Uploads must come from
  `.playwright-mcp/`. Check the sharing from a signed-out context (`drive_materials.md`).
- Slides instead of notes (Ashot, DECISIONS #33): his decks only grow within a part, so the folder holds the
  final deck of each part and every 📚 block says "սլայդներ N-M" + the deck + the folder. Page ranges per
  lesson: `_knowledge/info_theory/slides_map.md`.
- To change a file already linked from descriptions, replace it in place: right-click, File information,
  Manage versions, Upload new version. The file id and every link stay the same (Ashot's README, 2026-10-24).

## 5. Thumbnails, review page, push

- `scripts/make_umath_thumbnails.py --series <s> --lesson N --topic "..."`; long topics need a shorter
  thumbnail text so it fits in 2 lines.
- One standalone HTML page with titles, chapters, descriptions and thumbnails for the user's review
  before anything is pushed (`review_16-23.html`).
- Push with `yt_publish.py --channel umath` (the token is per channel), read back every video.
- Build each push from the **live** description, not the local copy: the user edits descriptions in Studio
  (`_learnings/2026-10-24-2043_build-description-pushes-from-the-live-text.md`).
- **API quota: 10,000 units a day; every videos.update and thumbnails.set costs 50.** A course push of
  13 videos (title, description, thumbnail) is ~2,000 units and fine on its own, but on 2026-10-22 the
  Papikian pushes, the Drive relinks, a visibility change and an 80-video audit together ran it out
  (403 quotaExceeded, then reads too). The quota resets at 09:00 Munich time. Plan big batches on a
  fresh day, and make push scripts skip videos that already match, so a rerun after a stop is safe.
- Visibility only on the user's word; when changing it, send the video's own status fields back and
  change only privacyStatus.
- Playlist order: `sort-playlist --by lesson`; the playlist must be set to Manual in Studio first
  (`_learnings/2026-10-20-2221_...`). Missing lecture numbers go into the next label ("Դաս 11-12",
  "Դաս 18-19"; Tserunyan: "Դաս 1-2"; DECISIONS #24).

## 6. After the push

- **Keep the repo copies in sync with every live fix** (`edited/description.txt`, `final/`): a later
  push from a stale file silently undoes the fix. The audit found 26 local files behind live.
- Rescan both channels: `scripts/non_essential/glossary_scan_channels.py` (0 DENY expected).
- **Email the lecturer.** Search Gmail first: there was no Papikian thread in this mailbox (the
  contact had gone through Hayk Aprikyan), so it was a new draft to the address on his own site, in
  Armenian, Aprikyan in cc, links as short text («այս playlist-ում», «այս Drive թղթապանակում») rather
  than bare URLs: playlist, materials folder, thanks, offer of help. Draft only; the user sends it.
  Since Tserunyan (2026-10-27, the user: "put the urls as well"): the full URL on its own line after each
  short text.
