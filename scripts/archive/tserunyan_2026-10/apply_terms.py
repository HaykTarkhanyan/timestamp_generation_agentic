"""Q84 A + Q85 A (2026-10-27): 'Գեներիկ էրգոդիկություն' -> 'Էրգոդիկություն ըստ Բեռի' (Դաս 16, 17),
'Պրոֆինիտ տոպոլոգիա' -> 'Թվաբանական պրոգրեսիաների տոպոլոգիա' (Դաս 19). Active files only (masters, the snapped
edited/timestamps.txt, the draft description and titles); the *_v1/_v2/_before_* history copies stay as they were.
Raises if a pair is not found anywhere or an old word is left in an active file. ~1 s."""
import re
import sys
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")
FILES = ["edited_predicted/titles.txt", "edited_predicted/timestamps_raw.txt", "edited_predicted/timestamps_raw_flat.txt",
         "edited_predicted/timestamps.txt", "edited_predicted/description.txt", "edited/timestamps.txt"]
PAIRS = {
    16: [("Լիովին կարգավորում։ Գեներիկ էրգոդիկություն", "Լիովին կարգավորում։ Էրգոդիկություն ըստ Բեռի"),
         ("Բորելյան գրաֆներ և գեներիկ էրգոդիկություն", "Բորելյան գրաֆներ և էրգոդիկություն ըստ Բեռի"),
         ("Կիրառություններ․ գեներիկ էրգոդիկություն և բորելյան գրաֆներ",
          "Կիրառություններ․ էրգոդիկություն ըստ Բեռի և բորելյան գրաֆներ"),
         ("Գեներիկ էրգոդիկություն (generically ergodic)", "Էրգոդիկություն ըստ Բեռի (generically ergodic)")],
    17: [("Գեներիկ էրգոդիկություն։ Գրաֆների ներկում", "Էրգոդիկություն ըստ Բեռի։ Գրաֆների ներկում"),
         ("ուղեծրեր, գեներիկ էրգոդիկություն", "ուղեծրեր, էրգոդիկություն ըստ Բեռի"),
         ("պտույտները գեներիկ էրգոդիկ են", "պտույտները էրգոդիկ են ըստ Բեռի"),
         ("Գեներիկ էրգոդիկության իմաստը", "Ըստ Բեռի էրգոդիկության իմաստը"),
         ("T_2α-ն էլ է գեներիկ էրգոդիկ", "T_2α-ն էլ է էրգոդիկ ըստ Բեռի")],
    19: [("Պրոֆինիտ տոպոլոգիա ℤ-ի վրա (profinite)", "Թվաբանական պրոգրեսիաների տոպոլոգիա ℤ-ի վրա (profinite)"),
         ("Պրոֆինիտ տոպոլոգիան հաուսդորֆյան է և մետրիզացվող", "Այս տոպոլոգիան հաուսդորֆյան է և մետրիզացվող"),
         ("Հարաբերական տոպոլոգիա։ Պրոֆինիտ տոպոլոգիա |", "Հարաբերական տոպոլոգիա։ Թվաբանական պրոգրեսիաների տոպոլոգիա |")],
}
OLD = re.compile("գեներիկ|պրոֆինիտ", re.IGNORECASE)

dry = "--dry" in sys.argv
for n, pairs in PAIRS.items():
    (d,) = [p for p in (REPO / "output").glob(f"2026-10-21_Das-{n}-Metric*") if p.is_dir()]
    texts = {f: (d / f).read_text(encoding="utf-8") for f in FILES}
    for old, new in pairs:
        hits = {f: t.count(old) for f, t in texts.items() if old in t}
        if not hits:
            raise ValueError(f"Das {n}: not found anywhere: {old}")
        for f in hits:
            texts[f] = texts[f].replace(old, new)
        print(f"Das {n}: {old!r} -> {new!r}: {hits}")
    for f, t in texts.items():
        left = [l for l in t.splitlines() if OLD.search(l)]
        if left:
            raise ValueError(f"Das {n} {f}: old word left: {left}")
        if not dry:
            (d / f).write_text(t, encoding="utf-8")
print("dry run, nothing written" if dry else "written")
