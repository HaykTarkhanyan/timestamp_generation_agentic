"""Q76 (the user, 2026-10-26: "Renumber Vahagn's to 44/45"): DECISIONS.md had two #39 and two #40 (this session's
Tserunyan entries and the Vahagn session's). Vahagn's #39 (batch pages) -> #44, #40 (webcam) -> #45, both moved to the
top so the file stays newest first, and every citation of them renumbered. Each replacement must match exactly once.
~1 s. Repo root."""
from pathlib import Path

REPO = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic")


def edit(rel, pairs):
    p = REPO / rel
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if t.count(old) != 1:
            raise ValueError(f"{rel}: expected one {old[:70]!r}, found {t.count(old)}")
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
    print(f"{rel}: {len(pairs)} change(s)")


# DECISIONS.md: cut the two Vahagn blocks out, renumber, put them on top (45 above 44)
p = REPO / "DECISIONS.md"
t = p.read_text(encoding="utf-8")
h40, h39, h38 = "## 40. While the lecturer's webcam", "## 39. Vahagn's remaining pieces", "## 38. Vahagn's 25 pieces"
for h in (h40, h39, h38):
    if t.count(h) != 1:
        raise ValueError(f"DECISIONS.md: heading {h!r} found {t.count(h)} times")
b40 = t[t.index(h40):t.index(h39)]
b39 = t[t.index(h39):t.index(h38)]
t = t.replace(b40, "").replace(b39, "")
b45 = b40.replace("## 40. ", "## 45. ", 1)
b44 = b39.replace("## 39. ", "## 44. ", 1)
top = "## 43. Tserunyan 22-27"
if t.count(top) != 1:
    raise ValueError("DECISIONS.md: #43 heading not found once")
note = ("- **Number:** was #40 until 2026-10-26; renumbered because this session and the Tserunyan session both used\n"
        "  #39 and #40 (the user's Q76).\n")
b45 = b45.rstrip("\n") + "\n" + note + "\n"
b44 = b44.rstrip("\n") + "\n" + note.replace("#40", "#39") + "\n"
t = t.replace(top, b45 + b44 + top)
p.write_text(t, encoding="utf-8")
print("DECISIONS.md: Vahagn #40 -> #45, #39 -> #44, moved to the top")

edit(".claude/skills/lecture-edit-points/SKILL.md", [
    ("**Lecturer's webcam on screen: cuts are suggestions only** (DECISIONS #40)",
     "**Lecturer's webcam on screen: cuts are suggestions only** (DECISIONS #45)"),
    ("for Vahagn's short pieces, DECISIONS #39)", "for Vahagn's short pieces, DECISIONS #44)")])
edit("scripts/cut_list.py", [("every cut a suggestion and none taken, DECISIONS #40)",
                              "every cut a suggestion and none taken, DECISIONS #45)")])
edit("scripts/find_edit_points.py", [("(a lecturer on camera,\n    DECISIONS #40)", "(a lecturer on camera,\n    DECISIONS #45)")])
edit("scripts/map_transcript_to_edit.py", [("e.g. a lecturer on camera, DECISIONS #40)", "e.g. a lecturer on camera, DECISIONS #45)")])
edit("scripts/remap_chapters.py", [("e.g. a lecturer on camera, DECISIONS #40)", "e.g. a lecturer on camera, DECISIONS #45)")])
edit("_learnings/2026-10-26-0120_studio-list-id-must-include-the-video.md", [("(DECISIONS #40)", "(DECISIONS #45)")])
edit("_work_sessions/2026-10-25-1700_vahagn-linalg-drafts-21-28.toml", [
    ("vahagn_batch_review.py build/split, DECISIONS #39;", "vahagn_batch_review.py build/split, DECISIONS #44;"),
    ("Webcam rule (DECISIONS #40)", "Webcam rule (DECISIONS #45)"),
    ("DECISIONS.md #35-#40, PLANNER.md", "DECISIONS.md #35-#38, #44, #45 (were #39, #40), PLANNER.md")])
edit("_knowledge/vahagn_linalg/status.md", [("**Batch review (DECISIONS #39, 2026-10-25):**", "**Batch review (DECISIONS #44, 2026-10-25):**"),
                                            ("**Webcam (DECISIONS #40, 2026-10-26):**", "**Webcam (DECISIONS #45, 2026-10-26):**")])
edit("scripts/non_essential/README.md", [("Several Vahagn pieces on one studio.html (DECISIONS #39)",
                                          "Several Vahagn pieces on one studio.html (DECISIONS #44)"),
                                         ("an unticked suggestion (DECISIONS #40)", "an unticked suggestion (DECISIONS #45)")])
