"""Put the slides block (DECISIONS #33) into Ashot's descriptions: page range, deck link, folder link.
Reads the live descriptions from info_playlist_dump.json (run info_playlist_dump.py first). Local repo copies
(Դաս 4, 5, 7, 8) must equal live before the change and are rewritten with it; Դաս 0-3 get a header-less
file in scratchpad/ashot_desc/. Prints the push commands' file list. ~1 s, no API calls.
"""
import json
import re
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
S = Path(__file__).parent
ids = json.loads((REPO / "_knowledge/info_theory/drive_folder_ids.json").read_text(encoding="utf-8"))
F = {name.split(" - ")[0]: f"https://drive.google.com/file/d/{v['id']}/view" for name, v in ids["files"].items()}
FOLDER = f"https://drive.google.com/drive/folders/{ids['folder']['id']}"
INTRO, MEAS, COMP = F["Դաս 0-1"], F["Դաս 1-4"], F["Դաս 5-8"]

# lesson -> (video id, local folder or None, [(pages, url)])
LESSONS = {
    0: ("U3BbIALq4aM", None, [("1-15", INTRO)]),
    1: ("4IO6iU7rRTA", None, [("16-36", INTRO), ("2-7", MEAS)]),
    2: ("N3LL6k55sao", None, [("8-27", MEAS)]),
    3: ("bHyOK-SSawI", None, [("28-54", MEAS)]),
    4: ("fHPN7fJEusA", "2026-10-20_Das-4-ToDo-Informaciayi-tesutyun_fHPN7fJEusA", [("55-82", MEAS)]),
    5: ("0WSFqm9E-Pc", "2026-10-20_Das-5-ToDo-Informaciayi-tesutyun_0WSFqm9E-Pc", [("1-21", COMP)]),
    7: ("S8vcM74HZVE", "2026-10-24_das7-final-1080p_S8vcM74HZVE", [("40-71", COMP)]),
    8: ("LOHGyVgaIuI", "2026-10-24_das8-final-1080p_LOHGyVgaIuI", [("72-96", COMP)]),
}
OLD_BLOCK = re.compile(r"📚 Դասախոսության ֆայլը՝[^\n]*\n[^\n]+\n")


def block(parts):
    if len(parts) == 1:
        pages, url = parts[0]
        head = f"📚 Դասախոսության ֆայլը՝ սլայդներ {pages}\n{url}\n"
    else:
        head = "📚 Դասախոսության ֆայլերը՝\n" + "".join(f"սլայդներ {p}՝ {u}\n" for p, u in parts)
    return head + f"📁 Բոլոր սլայդները՝\n{FOLDER}\n"


live = {v["id"]: v for v in json.loads((S / "info_playlist_dump.json").read_text(encoding="utf-8"))}
out = S / "ashot_desc"
out.mkdir(exist_ok=True)
for n, (vid, folder, parts) in LESSONS.items():
    desc = live[vid]["description"]
    if len(OLD_BLOCK.findall(desc)) != 1:
        raise ValueError(f"Դաս {n}: expected one 📚 block, found {len(OLD_BLOCK.findall(desc))}")
    new = OLD_BLOCK.sub(lambda m: block(parts), desc)
    if "<" in new or ">" in new:
        raise ValueError(f"Դաս {n}: ASCII angle bracket")
    if folder:
        p = REPO / "output" / folder / "description.txt"
        text = p.read_text(encoding="utf-8")
        head, body = text.split("──────────────────────────────", 1)
        if body.strip() != desc.strip():
            raise ValueError(f"Դաս {n}: local description.txt differs from live; sync first")
        p.write_text(head + "──────────────────────────────\n\n" + new.strip() + "\n", encoding="utf-8")
        print(n, vid, p)
    else:
        p = out / f"das{n}.txt"
        p.write_text(new.strip() + "\n", encoding="utf-8")
        print(n, vid, p)
print("\nexample (Դաս 1):\n" + block(LESSONS[1][2]))
