"""Build one Codex review prompt per Ashot info theory lesson: title, chapters, that lesson's slide text and the
full transcript, all inline (Codex's sandbox cannot read files). Writes scratchpad/codex_info/prompt_<N>.md. ~2 s.

    python -X utf8 codex_info_prompts.py 4 5        # existing (published) lists
    python -X utf8 codex_info_prompts.py 7 8        # drafts
"""
import re
import sys
from pathlib import Path

import fitz

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
SLIDES = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\info\slides\Lecture Slides")
OUT = Path(__file__).parent / "codex_info"
OUT.mkdir(exist_ok=True)

# lesson -> (output folder, deck key, first page, last page, date, status)
LESSONS = {
    4: ("2026-10-20_Das-4-ToDo-Informaciayi-tesutyun_fHPN7fJEusA", "L-5", 54, 82, "6 March 2026", "published (unlisted)"),
    5: ("2026-10-20_Das-5-ToDo-Informaciayi-tesutyun_0WSFqm9E-Pc", "L-6", 1, 21, "13 March 2026", "published (unlisted)"),
    6: ("2026-10-24_Das-6-Tvyalneri-seghmum-Koderi_LRQ6r_DaAVU", "L-8", 22, 39, "27 March 2026", "draft"),
    7: ("2026-10-24_das7-final-1080p_S8vcM74HZVE", "L-10", 38, 71, "17 April 2026", "draft"),
    8: ("2026-10-24_das8-final-1080p_LOHGyVgaIuI", "L-11", 66, 100, "8 May 2026", "draft"),
}


def deck_text(key: str, a: int, b: int) -> str:
    pdf = next(p for p in SLIDES.glob("*.pdf")
               if p.stem.replace("InformationTheory-ASDS-2026-", "").replace("-posted", "") == key)
    doc = fitz.open(pdf)
    out = []
    for i in range(a - 1, min(b, len(doc))):
        lines = [ln.strip() for ln in doc[i].get_text().splitlines() if ln.strip()]
        out.append(f"--- page {i + 1}\n" + "\n".join(lines[:14]))
    return "\n".join(out)


def chapters_and_title(folder: Path) -> tuple[str, str]:
    desc = (folder / "description.txt").read_text(encoding="utf-8")
    title = desc.splitlines()[0].split("՝", 1)[1].strip()
    chap = desc.split("⏳ Թեմաներ", 1)[1].split("\n\n\n", 1)[0]
    chap = "\n".join(ln for ln in chap.splitlines()[1:] if re.match(r"^\s*\d", ln))
    return title, chap


for n in map(int, sys.argv[1:]):
    name, deck, a, b, date, status = LESSONS[n]
    folder = REPO / "output" / name
    title, chapters = chapters_and_title(folder)
    transcript = (folder / "transcript.txt").read_text(encoding="utf-8").replace("&lt;", "<").replace("&gt;", ">")
    prompt = f"""You are reviewing a YouTube chapter list and title for a university lecture in Armenian.
Do NOT run shell commands or read files: everything you need is below. Reply with the report only.

# Context
Lesson {n} (Դաս {n}) of Ashot Harutyunyan's course "Information Theory" (Yerevan State University, master's programme
in applied statistics and data science), recorded in a classroom on {date}. He lectures in Armenian from English slides
(Cover & Thomas based). All times below are on the published video's timeline.
Status of this list: {status}. You are an independent reviewer of the chapters and the title.

The transcript is YouTube's automatic Armenian captions: noisy, no punctuation, terms often garbled ("Huffman" comes out
as "հաղթման", "հատման", "հավման"; "Kraft" as "գրաֆթ"). Use the slides below to understand what is being taught.

# Series style (lessons 0-5 are already published this way)
- Title: `Դաս N | <topic in Armenian> | Ինֆորմացիայի տեսություն`, the topic usually two parts joined by `։`.
- Chapter labels: short Armenian labels, often with a prefix and the Armenian `․` : `Հիշեցում․ ...`, `Օրինակ․ ...`,
  `Ապացույց․ ...`, `Թեորեմ․ ...`, `Հետևանք․ ...`, `Հարց․ ...` (a student's question). Formulas inline in Unicode
  (H(X), D(P‖Q), 2^(-nH), ≤). Times as MM:SS, or HH:MM:SS past an hour, first chapter 00:00.
- Terms: the lecturer's own Armenian terms where he uses them (ակնթարթային կոդ, միարժեք ապակոդավորվող կոդ,
  Կրաֆտի անհավասարություն, օպտիմալ կոդ, Շենոնի կոդ, Ֆանոյի կոդ, Հաֆմանի կոդ), standard Armenian math terms otherwise.

# What to check
1. Each label: is it what he actually covers at that point, and is the statement correct (formulas, direction of
   inequalities, hypotheses)? Is the Armenian correct and natural (spelling, grammar, question marks `՞`)?
2. Each boundary: does the chapter start where he turns to / names the new topic? Propose a move only with the
   transcript line that proves it (quote its time and words). Do not move a boundary so that a turn sentence
   ("Հիմա ...", "Շատ լավ ...", "Լավ, ...") falls into the previous chapter.
3. Coverage: an important topic or slide covered at length with no chapter, or a chapter for something trivial.
4. The title: does it name what this lesson is actually about? Suggest a better one if it does not.

Report format: a short verdict (good / needs fixes), then a table: time | current label | problem | proposed fix |
evidence (transcript time + words or slide page). Then the title verdict. Keep it under ~60 lines; no praise padding.

# Title
{title}

# Chapters
{chapters}

# Slides covered in this lesson ({deck} deck, pages {a}-{b}; first lines of each page)
{deck_text(deck, a, b)}

# Transcript (published video timeline)
{transcript}
"""
    (OUT / f"prompt_{n}.md").write_text(prompt, encoding="utf-8")
    print(n, len(prompt), "chars", title)
