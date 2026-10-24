"""Stage Ashot's 4 final slide decks (DECISIONS #33) plus a README.txt for the math-team Drive folder.
Copies into .playwright-mcp/drive_upload_ashot/ (git-ignored, inside the Playwright upload root). ~2 s. Repo root."""
import shutil
from pathlib import Path

SRC = Path(r"C:\Users\hayk_\OneDrive\Desktop\misc\YSU OpenCourseWare\info\slides\Lecture Slides")
DST = Path(".playwright-mcp/drive_upload_ashot")
PLAYLIST = "https://www.youtube.com/playlist?list=PLz3NrXxHz_CBt8cN2KKhwNqm_SmoyDDPy"
PREFIX = "InformationTheory-ASDS-2026-"

plan = {
    "Intro-L-1-extended.pdf": "Դաս 0-1 - Ներածություն, հավանականության հիշեցում.pdf",
    "L-5-posted.pdf": "Դաս 1-4 - Ինֆորմացիայի չափեր.pdf",
    "L-11-posted.pdf": "Դաս 5-8 - Տվյալների սեղմում.pdf",
    "ChannelCapacity-L-13-end-posted.pdf": "Կապուղու թողունակություն (տեսագրություն չկա).pdf",
}

DST.mkdir(parents=True, exist_ok=True)
for src, name in plan.items():
    if any(c in name for c in '<>:"/\\|?*'):
        raise ValueError(f"character not allowed in a Windows file name: {name!r}")
    shutil.copy2(SRC / (PREFIX + src), DST / name)

readme = f"""Ինֆորմացիայի տեսություն - Աշոտ Հարությունյան
ԵՊՀ Մաթեմատիկայի և մեխանիկայի ֆակուլտետ, Կիրառական վիճակագրություն և տվյալների գիտություն
(մագիստրատուրա), գարուն 2026

Դասախոսությունների տեսագրությունները՝
{PLAYLIST}

Ո՞ր դասին որ էջերն են՝
Դաս 0 - «Դաս 0-1 - Ներածություն...», էջ 1-15
Դաս 1 - «Դաս 0-1 - Ներածություն...», էջ 16-36, և «Դաս 1-4 - Ինֆորմացիայի չափեր», էջ 2-7
Դաս 2 - «Դաս 1-4 - Ինֆորմացիայի չափեր», էջ 8-27
Դաս 3 - «Դաս 1-4 - Ինֆորմացիայի չափեր», էջ 28-54
Դաս 4 - «Դաս 1-4 - Ինֆորմացիայի չափեր», էջ 55-82
Դաս 5 - «Դաս 5-8 - Տվյալների սեղմում», էջ 1-21
Դաս 6 - «Դաս 5-8 - Տվյալների սեղմում», էջ 22-39
Դաս 7 - «Դաս 5-8 - Տվյալների սեղմում», էջ 40-71
Դաս 8 - «Դաս 5-8 - Տվյալների սեղմում», էջ 72-96 (97-100՝ ամփոփում)

«Կապուղու թողունակություն» մասի դասախոսությունները տեսագրված չեն։
"""
(DST / "README.txt").write_text(readme, encoding="utf-8")
total = sum(f.stat().st_size for f in DST.iterdir())
for f in sorted(DST.iterdir()):
    print(f"{f.stat().st_size / 1e6:6.1f} MB  {f.name}")
print(f"{len(list(DST.iterdir()))} files, {total / 1e6:.1f} MB")
