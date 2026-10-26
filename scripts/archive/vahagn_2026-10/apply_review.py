"""Merge Codex verdicts into _knowledge/vahagn_linalg/codex_review.json and optional title changes into pieces.json.

    python -X utf8 apply_review.py verdicts_<batch>.json
The input: {"ledger": {"<section>": {"findings": [...], "title": "..."}}, "titles": {"<section>": ["t1", "t2", "t3"]}}
"""
import json
import sys
from pathlib import Path

K = Path(r"C:\Users\hayk_\OneDrive\Desktop\timestamp_generation_agentic\_knowledge\vahagn_linalg")
inp = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
led_p = K / "codex_review.json"
led = json.loads(led_p.read_text(encoding="utf-8"))
led.update(inp.get("ledger", {}))
led_p.write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding="utf-8")
pc_p = K / "pieces.json"
pc = json.loads(pc_p.read_text(encoding="utf-8"))
for p in pc["pieces"]:
    if p["section"] in inp.get("titles", {}):
        p["titles"] = inp["titles"][p["section"]]
        print(p["section"], "title ->", p["titles"][0])
pc_p.write_text(json.dumps(pc, ensure_ascii=False, indent=1), encoding="utf-8")
print("ledger sections:", sorted(k for k in led if not k.startswith("_")))
