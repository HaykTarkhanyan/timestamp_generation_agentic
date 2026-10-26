"""One Codex review prompt per Vahagn linear algebra piece: series rules, title candidates, chapters (raw
timeline) and the full raw transcript, all inline (Codex runs read-only and reads no files). ~1 s.

    python -X utf8 make_prompts.py            # every piece with a draft
"""
import json
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
OUT = Path(__file__).parent
pieces = json.loads((REPO / "_knowledge/vahagn_linalg/pieces.json").read_text(encoding="utf-8"))["pieces"]
uploads = {u["section"]: u["id"] for u in json.loads((REPO / "_knowledge/vahagn_linalg/uploads.json").read_text(encoding="utf-8"))}

RULES = """# Series style (the 72 published pieces 1.1-20.3 look like this)
- Title: `Դաս <section> | <topic in Armenian> | Գծային հանրահաշիվ`, the topic one or two parts joined by `։`,
  the whole title under 100 characters (aim for a topic under ~55). Notation in titles like `R^2`, `F^n`, `Ax=b`.
- Chapter labels: short Armenian, with prefixes and the Armenian `․` : `Օրինակ․ ...`, `Ապացույց․ ...`, `Թեորեմ․ ...`,
  `Լեմմա․ ...`, `Հետևանք․ ...`, `Հիշեցում․ ...`, `Սահմանում․ ...`, `Հարց․ ...`. Notation: ker(T), rank(A), nullity(A),
  R^5 → R^3, P_3, E_λ, [T], A^(-1), Q^T, ⇔, ⇒. ASCII `<` and `>` are FORBIDDEN (YouTube rejects them): `＜` `＞` stay.
- One level of nesting is allowed (4 spaces before the time), a parent needs 2+ children; chapters 30 s+ apart.
- Terms: the lecturer's own words where he uses them (e.g. դիագոնալիզացիա, դիագոնալիզացվող, դեֆեկտ, երկրաչափական
  / հանրահաշվական պատիկություն, Գրամ-Շմիդտի պրոցես, օրթոգոնալիզացիա), otherwise the course glossary: միջուկ
  (kernel), պատկեր (image), ռանգ, ինյեկտիվ / սյուրյեկտիվ / բիյեկտիվ, պրոյեկցիա, պտույտ, արտացոլում (reflection),
  համադրույթ (composition), իզոմորֆիզմ, սեփական արժեք / վեկտոր / ենթատարածություն, բնութագրիչ բազմանդամ, նման
  մատրիցներ, անկյունագծային մատրից, սկալյար արտադրյալ, օրթոգոնալ / օրթոնորմալ բազիս, օրթոգոնալ մատրից, սիմետրիկ
  մատրից, սպեկտրալ թեորեմ, որոշիչ (determinant). Do not replace these with synonyms.
- No correction notes are published for this channel: if the lecturer slips, the label simply states the correct
  thing (and you mention the slip in your report)."""


def chapters(sec):
    d = next(iter(REPO.glob(f"output/*_{uploads[sec]}")))
    return d, (d / "edited_predicted/timestamps_raw.txt").read_text(encoding="utf-8").rstrip()


for p in pieces:
    if not p["titles"]:
        continue
    d, chap = chapters(p["section"])
    transcript = (d / "transcript.txt").read_text(encoding="utf-8").replace("&lt;", "<").replace("&gt;", ">")
    titles = "\n".join(f"{i}. Դաս {p['label']} | {t} | Գծային հանրահաշիվ" for i, t in enumerate(p["titles"], 1))
    prompt = f"""You are reviewing a YouTube chapter list and title candidates for one piece of a university lecture
in Armenian. Do NOT run shell commands or read files: everything you need is below. Reply with the report only.

# Context
Piece {p['label']} (book section {p['section']}) of prof. Vahagn Mikaelian's course «Բարձրագույն հանրահաշիվ», linear
algebra part, Yerevan State University, recorded online on {p['date']}. He lectures in Armenian from his own English
textbook (a PDF he annotates on screen). The recording has only his microphone: students' answers are mostly NOT in the
transcript; he usually repeats them. All times are on the raw recording's timeline (the transcript's timeline).

The transcript is YouTube's automatic Armenian captions: noisy, no punctuation, terms often garbled ("ինեկտիվ" for
ինյեկտիվ, "դիագանալիզացիա" for դիագոնալիզացիա, "գրամշմիթ" for Գրամ-Շմիդտ, "քեռ"/"քերտ" for ker T, "նալիթի" for
nullity). Infer the mathematics from context.

{RULES}

# What to check
1. Each label: is it what he actually covers there, and is the mathematics correct and complete (hypotheses such as
   dim V = n, c ≠ 0, A invertible, real field; direction of implications; formulas)? Is the Armenian correct and
   natural (spelling, grammar, question mark `՞` placement)?
2. Each boundary: does the chapter start where he turns to / names the new topic? Propose a move only with the
   transcript line that proves it (quote its time and words), and never so that a turn sentence ("Հիմա ...",
   "Նայեք ...", "Լավ, ...", "Ահա ...") ends up in the previous chapter. Keep 30 s+ between chapters.
3. Coverage: something covered at length with no chapter, or a chapter for something trivial.
4. Titles: which candidate is best, or a better one (it must name what this piece is actually about; under 100 chars).
5. Any slip by the lecturer worth knowing (a wrong statement he does not correct).

Report format: one-line verdict (good / needs fixes); then a table: time | current label | problem | proposed label or
move | evidence (transcript time + words). Then the title verdict, then slips (if any). Under ~50 lines, no praise.

# Title candidates (1 = current recommendation)
{titles}

# Chapters (raw timeline)
{chap}

# Transcript (raw timeline)
{transcript}
"""
    (OUT / f"prompt_{p['section']}.md").write_text(prompt, encoding="utf-8")
    print(p["section"], len(prompt), "chars")
