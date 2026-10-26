"""One Codex prompt for the user's Q70 ask ("ask codex for feedback on titles and descriptions"): all 13 Tserunyan
titles and assembled descriptions (15 as published, 16-27 from edited/) inline, series rules stated so Codex does not
propose what they forbid. Writes scratchpad/codex_desc/prompt.md. ~1 s."""
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
OUT = Path(__file__).parent / "codex_desc"
OUT.mkdir(exist_ok=True)

blocks = []
for n in range(15, 28):
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    ed = d / "edited"
    if not (ed / "description.txt").exists():   # 24, 26, 27: no edited captions yet, same labels, times +-2 s
        ed = d / "edited_predicted"
        print(f"Das {n}: using edited_predicted/")
    titles = (ed / "titles.txt").read_text(encoding="utf-8").splitlines()
    desc = (ed / "description.txt").read_text(encoding="utf-8").strip()
    alt = "\n".join(f"  - {t}" for t in titles[1:] if t.strip())
    blocks.append(f"## Դաս {n}\nPublished title (line 1): {titles[0]}\nAlternative titles considered:\n{alt}\n\n"
                  f"Description:\n```\n{desc}\n```\n")

prompt = f"""You are reviewing the YouTube titles and descriptions of 13 university lectures in Armenian.
Do NOT run shell commands or read files: everything you need is below. Reply with the report only, in English;
write any proposed Armenian text in Armenian.

# Context
Lectures 15-27 (Դաս 15-27) of Anush Tserunyan's (McGill University) course "Metric spaces and topology"
(Մետրիկական տարածություններ և տոպոլոգիա), taught in Yerevan in spring 2023 for the ASOF foundation, in Armenian.
Topics: descriptive set theory flavour (Baire category, Kuratowski-Ulam, Borel graphs), then general topology
(separation and countability axioms, products, compactness, Tychonoff, nets). Lectures 1-14 are already published
in the same format. The videos were cut before publishing, and the chapter times are on the cut video.
The chapter lists were already reviewed once against the transcripts, by Claude and by you (Codex), on 2026-10-23,
and the titles of 19, 24 and 27 were changed then and approved by the channel owner.

# Fixed rules: do not propose anything against these
- Title format: `Դաս N | <topic> | Մետրիկական տարածություններ և տոպոլոգիա`, at most 100 characters in total.
  The topic is usually two parts joined by the Armenian full stop `։`.
- The description template is fixed: title line, lecturer line, date, the 📚 links block, ⏳Թեմաներ chapters,
  playlist, music. The links themselves cannot be checked here; only flag a label in front of a link that is wrong.
- Chapters: H:MM:SS, first one 0:00:00, at least 30 s apart, nested sub-chapters indented by 4 spaces (one level
  only, a parent has 2 or more children). Do not propose moving times: you have no transcript of the cut videos.
- ASCII `<` and `>` are forbidden anywhere in a description (YouTube rejects them); the fullwidth `＜` `＞` are used on
  purpose. Unicode math (ℝ, ⇒, ∈, ↦, ^, _) is on purpose.
- English terms in parentheses after the Armenian term are on purpose (the first time a term appears).
- Glossary terms are fixed. In particular `լիովին կարգավորում` / `լիովին կարգավորված` = well-ordering / well-ordered
  (not "total order"); `մասնակի սահման` = subsequential limit. If you think a term is wrong, flag it as a question,
  do not just replace it.
- No correction notes are added to these videos, even where the lecturer misspoke.
- A reworded label that is only longer or only different in taste is not wanted. Propose a change only for an
  error: wrong math or a missing hypothesis, an Armenian spelling or grammar error (question marks `՞`, `ու`/`վ`,
  case endings), an inconsistency between lectures (the same thing named differently), or a title that does not
  say what the lecture is about.

# What to check
1. Titles: correct Armenian, accurate for the chapter list below it, consistent style across the 13, within 100
   characters. Prefer the published title; suggest one of the alternatives or a new one only with a reason.
2. Descriptions: Armenian spelling and grammar in every chapter label, math statements in labels (hypotheses,
   quantifiers, direction of implications), consistent naming of the same notion across lectures, and anything in
   the description that contradicts its own chapter list or title. (The date lines are checked separately.)
3. Cross-course: the same theorem or notion named two ways in different lectures; a topic that appears to be
   repeated or missing in the sequence.

Report format: one short overall verdict, then per lecture a table: where (title / date / chapter time) | current
text | problem | proposed fix | how sure you are (high / medium / low). Lectures with nothing to fix: one line "Դաս N:
no issues". Then a short cross-course section. Keep it under ~150 lines; no praise padding.

# The 13 lectures
{chr(10).join(blocks)}
"""
(OUT / "prompt.md").write_text(prompt, encoding="utf-8")
print(len(prompt), "chars")
