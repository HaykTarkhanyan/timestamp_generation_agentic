# A term the lecturer says in English gets spelled in Armenian letters when no Armenian word exists

**Symptom**
Tserunyan's titles and chapters said "Գեներիկ էրգոդիկություն" (Դաս 16, 17) and "Պրոֆինիտ տոպոլոգիա" (Դաս 19). The
user, reading the review page: "in armenian generic sounds weird". Both had passed the agents' drafts, the inline
review, the Codex review and the glossary check, and were already pushed.

**Cause**
The series rule is "Armenian term + (English term)". When she says a term only in English and Armenian has no
established word for it, the drafting step wrote the English word in Armenian letters instead of flagging the gap.
The transcripts show she never said either form:

```
16 "generic ergodicity" / "generically ergodic" in English: 0:35:42, 0:36:13, 1:20:32; "գեներիկ": 0 times
17 "generic ergodicity": 0:39:40, 0:48:13; "generically ergodic": 0:45:25
19 "profinite": 1:16:30 "էդ տոպոլոգիան կոչվում ա պրոֆայնայթ"; "պրոֆինիտ": 0 times
```

Her own words gave the fix: at Դաս 16 1:20:32, "generic բառը նշանակում է որպես Բեռի կատեգորիայի" -> "Էրգոդիկություն ըստ
Բեռի (generic ergodicity)", next to the series' "Ըստ Բեռի չափելի (Baire measurable)". A web search (8 queries,
Armenian and Russian) found no Armenian term for either word (DECISIONS #49).

**The check that would have caught it (cheap, no agents)**
For each label word in Armenian letters that looks like a loanword, count it in that lecture's transcript:

```
grep -c -i -E '<armenian form>' edited/transcript.txt     # how she says it in Armenian
grep -c -i -E '<english form>' edited/transcript.txt      # how often she says it in English
```

0 Armenian + many English = we coined it: describe it in Armenian (from her explanation if she gives one) and keep the
English in parentheses. A loanword she says herself is fine: "ինտերվալ" 34 times in Դաս 17, "box" 10 times in Դաս 20.
Not every Armenian-letters word is a coinage: "չնչին / կոչնչին" (she says "միգր" ~60 times a lecture) came from the
published Դաս 1-14 and stays for consistency.

**Consequences**
- A term reaches further than the titles: thumbnails, chapter masters and their derived copies, the lecture-note PDF
  names on the math-team Drive (named after the titles) and our own homework names ("Տնային 8 - ..., գեներիկ
  էրգոդիկություն, ..."). Search the Drive folder too (`<word> parent:<folder id>` at `drive/u/2`).
- `glossary_denylist.csv` now blocks "գեներիկ" and "պրոֆինիտ", but only those two words; the transcript count above
  is the general check. Run it on new titles before the review page, not after the push.
