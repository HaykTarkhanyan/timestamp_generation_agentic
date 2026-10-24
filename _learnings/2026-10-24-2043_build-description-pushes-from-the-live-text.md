# Build every description push from the live text: the user edits descriptions in Studio

**Symptom:** while nesting the chapters of Ashot's 9 videos (2026-10-24), the script stopped on Դաս 6:
the local `description.txt`, read back identical to YouTube one hour earlier, no longer matched live.

```
-ℹ️ ... 45-րդ րոպեից մինչև վերջ ցուցադրվում են դասախոսի սլայդները՝ դասախոսության ձայնով։
+ℹ️ ... 45-րդ րոպեից մինչև վերջ ցուցադրվում են դասախոսի սլայդները։
```

**Cause:** the user had shortened the note in Studio ("i had deleted a line, thats on me, i want it that way").

**Consequences:**
- A push built from the local copy would have silently undone their edit. Fetch the live description,
  change only the part being changed, and write the result back to the local copy as well.
- Keep the comparison step: when local and live differ, stop and show the diff instead of picking one.
  `scripts/archive/info_theory_2026-10/nest_info_chapters.py` and `ashot_materials.py` do this.
- Same rule as the umath playbook's "keep the repo copies in sync with every live fix", seen from the other
  side: live can also move without Claude.
