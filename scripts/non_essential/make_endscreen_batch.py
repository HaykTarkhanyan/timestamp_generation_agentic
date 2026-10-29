"""Bundle several end-screen job files into one Playwright file that runs them in order. It skips a video that already
has an end screen (an "ALREADY:" error, raised before anything is touched), retries any other failure twice after
60 s, then stops.

    python scripts/non_essential/make_endscreen_batch.py endscreen_template.js .playwright-mcp/endscreen_batch_ml_1.js \
        .playwright-mcp/endscreen_ml_54_*.js .playwright-mcp/endscreen_ml_53_*.js ...      # ~1 s

The first argument is the template the job files were made from (endscreen_template.js or endscreen_edit_template.js,
next to this file); the JOB of each job file is read back from its "const JOB = {...};" line. One job file per
browser_run_code_unsafe call prints the whole template every time; a batch prints it once and returns one line per video.
Run the batch with browser_run_code_unsafe(filename=...): ~1 min per video, the call moves to the background after 2 min.
"""
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOB_LINE = re.compile(r"^  const JOB = (\{.*\});   //", re.M)
HEAD = "async (page) => {\n  const JOB = __JOB__;"

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_batch")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_batch.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

template, out, *job_files = sys.argv[1:]
tpl = (Path(__file__).parent / template).read_text(encoding="utf-8")
if tpl.count(HEAD) != 1:
    raise ValueError(f"{template} does not start its function with {HEAD!r}")
one = tpl[tpl.index(HEAD):].replace(HEAD, "async function one(page, JOB) {", 1).rstrip()
jobs = []
for f in job_files:
    m = JOB_LINE.findall(Path(f).read_text(encoding="utf-8"))
    if len(m) != 1:
        raise ValueError(f"{f}: expected one 'const JOB = ...' line, found {len(m)}")
    jobs.append(json.loads(m[0]))
# An "ALREADY:" error (the video has an end screen; raised before anything is touched) skips the video. Any other error
# is retried twice after 60 s (2026-10-27: Wi-Fi drops made Studio drop a Save, "your recent edits were not saved"):
# safe, because a retry of a video whose earlier attempt did save stops at ALREADY. Every retry is listed in the result.
# The dialog handler accepts the "leave page?" prompt, which discards the failed attempt's unsaved edits.
body = (f"// Batch of {len(jobs)} jobs from {template}, made by make_endscreen_batch.py. Skips videos that already have an\n"
        "// end screen, retries any other failure twice after 60 s, then stops.\n"
        f"async (page) => {{\n{one}\n  const JOBS = {json.dumps(jobs, ensure_ascii=False)};\n"
        "  const done = [], skipped = [], retried = [];\n"
        "  const onDialog = d => d.accept().catch(() => {});\n  page.on('dialog', onDialog);\n  try {\n"
        "    for (const [k, JOB] of JOBS.entries()) {\n      let last = null;\n"
        "      for (let attempt = 1; attempt <= 3; attempt++) {\n"
        "        try { done.push(await one(page, JOB)); last = null; break; }\n"
        "        catch (e) {\n          last = String(e.message || e);\n          if (last.includes('ALREADY:')) break;\n"
        "          retried.push(`${JOB.lesson} attempt ${attempt}: ${last.slice(0, 200)}`);\n"
        "          if (attempt < 3) await page.waitForTimeout(60000);\n        }\n      }\n"
        "      if (last && last.includes('ALREADY:')) { skipped.push(`${JOB.lesson}: ${(last.match(/ALREADY:[^\"]*/) || [''])[0].slice(0, 160)}`); continue; }\n"
        "      if (last) return { done, skipped, retried, failed: JOB.lesson, error: last, not_run: JOBS.length - k - 1 };\n"
        "    }\n  } finally { page.off('dialog', onDialog); }\n  return { done, skipped, retried };\n}\n")
Path(out).write_text(body, encoding="utf-8")
log.info(f"{out}: {len(jobs)} jobs, first {jobs[0]['lesson']!r}, last {jobs[-1]['lesson']!r}")
