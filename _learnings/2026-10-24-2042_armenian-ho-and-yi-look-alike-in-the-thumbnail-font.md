# In the Win95 thumbnail font, Armenian Հ and Յ look almost the same: don't call a typo from pixels

**Symptom:** checking the user's Canva export of Ashot's Դաս 5 thumbnail (2026-10-24), the first letter of
"Հավասար" looked like Յ next to the clearly different Հ of "Հաֆմանի" on Դաս 8. I reported it as a typo
("Յավասար") on both the new and the live thumbnail.

**Cause:** it was Հ. The user: "das 5 is actually with h, they are just very similar". The two glyphs in that
font differ by a stroke that a 1280x720 export barely shows, and the two text boxes need not use the same font.

**Consequences:**
- Check thumbnail text against the title string the user typed, not by eye letter by letter. Flag only what a
  reader would notice (wrong word, missing word, wrong lesson number) and phrase a glyph-level doubt as a
  question, not as a finding.
- Related: in the Canva editor the ArmSCII "և" shows as "§" while the export is right
  (`_knowledge/info_theory/recording_timeline.md`, Thumbnails).
