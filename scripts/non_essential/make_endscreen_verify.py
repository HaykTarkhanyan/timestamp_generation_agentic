"""Read-only check that the saved end screens match their job files: one Playwright file that opens each video's editor
and compares the listed elements with the job (Subscribe, Playlist: <playlist>, Video: <next title> or Best for viewer).

    python scripts/non_essential/make_endscreen_verify.py .playwright-mcp/endscreen_verify_ml.js .playwright-mcp/endscreen_ml_*.js   # ~1 s

Run the output with browser_run_code_unsafe(filename=...): ~10 s per video, nothing is clicked or saved. It returns the
count that match and one line per video that does not (no end screen, wrong video, wrong playlist, extra elements).
With --times (first argument) it also opens each end screen's edit view, reads the first element's start-end and
returns one row per video with the elements and that span (~18 s per video; still nothing changed or saved).
"""
import json
import logging
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
JOB_LINE = re.compile(r"^  const JOB = (\{.*\});   //", re.M)

(REPO / "logs").mkdir(exist_ok=True)
log = logging.getLogger("make_endscreen_verify")
log.setLevel(logging.INFO)
for h in (logging.StreamHandler(), logging.FileHandler(REPO / "logs" / "make_endscreen_verify.log", encoding="utf-8")):
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    log.addHandler(h)

args = sys.argv[1:]
with_times = args[:1] == ["--times"]
out, *job_files = args[1:] if with_times else args
jobs = []
for f in job_files:
    m = JOB_LINE.findall(Path(f).read_text(encoding="utf-8"))
    if len(m) != 1:
        raise ValueError(f"{f}: expected one 'const JOB = ...' line, found {len(m)}")
    j = json.loads(m[0])
    jobs.append({"id": j["id"], "lesson": j["lesson"], "channel": j["channel"], "playlist": j["playlist"],
                 "video": j["next"]["prefix"] if j["next"] else "Best for viewer",
                 "subscribe": j.get("layout") != "video+playlist"})   # portrait videos: Video + Playlist only
body = f"""// Read-only end-screen check of {len(jobs)} videos, made by make_endscreen_verify.py.
async (page) => {{
  const JOBS = {json.dumps(jobs, ensure_ascii=False)};
  const TIMES = {"true" if with_times else "false"};
  const norm = s => s.replace(/\\s+/g, ' ').trim();
  const ok = [], problems = [], rows = [];
  for (const J of JOBS) {{
    // a page that does not open is one problem line, not the end of the check (2026-10-28: a network blip lost 20 results)
    const nav = await page.goto(`https://studio.youtube.com/video/${{J.id}}/editor`, {{ waitUntil: 'domcontentloaded', timeout: 60000 }})
      .then(() => null, e => String(e.message || e).split('\\n')[0].slice(0, 80));
    if (nav) {{ problems.push(`${{J.lesson}}: editor did not open (${{nav}})`); continue; }}
    const loaded = await page.waitForFunction(() => /End screen/.test(document.body.innerText), null, {{ timeout: 40000 }}).then(() => true, () => false);
    if (!loaded) {{ problems.push(`${{J.lesson}}: editor did not load in 40 s`); continue; }}
    await page.waitForTimeout(2500);
    // the element titles show as "Video: ..." / "Playlist: ..." for a few seconds after load (2026-10-27: 5 of 56)
    await page.waitForFunction(() => !(document.body.innerText.match(/(Subscribe|Playlist|Video): [^\\n]*/g) || []).some(e => /: \\.\\.\\.$/.test(e.trim())),
      null, {{ timeout: 30000 }}).catch(() => {{}});
    const r = await page.evaluate(() => ({{ ch: ytcfg.get('CHANNEL_ID'), el: document.body.innerText.match(/(Subscribe|Playlist|Video|Channel|Link): [^\\n]*/g) || [] }}));
    if (r.ch !== J.channel) {{ problems.push(`${{J.lesson}}: Studio runs as ${{r.ch}}, stopped`); break; }}
    const el = r.el.map(norm);
    const want = [...(J.subscribe ? ['Subscribe: '] : []), 'Playlist: ' + norm(J.playlist), 'Video: ' + norm(J.video)];
    const miss = want.filter(w => !el.some(e => e.startsWith(w)));
    if (el.length !== want.length || miss.length) problems.push(`${{J.lesson}}: has [${{el.join(' | ').slice(0, 220)}}], missing [${{miss.join(' | ')}}]`);
    else ok.push(J.lesson.slice(0, 2));
    if (TIMES) {{
      // the edit view selects the first element and shows its start and end; leaving it unchanged asks nothing
      let span = null;
      if (el.length) {{
        await page.getByRole('link', {{ name: 'End screen Edit' }}).click({{ timeout: 15000 }}).catch(() => {{}});
        await page.waitForTimeout(4000);
        const tt = await page.locator('ytve-endscreen-editor-options-panel input:visible').evaluateAll(xs => xs.map(x => x.value)).catch(() => []);
        const secs = tc => {{ const p = tc.split(':').map(Number); const [h, m, s] = p.length === 4 ? p : [0, ...p]; return h * 3600 + m * 60 + s; }};
        span = tt.length >= 2 && tt[1] ? {{ start: tt[0], end: tt[1], seconds: secs(tt[1]) - secs(tt[0]) }} : {{ error: 'no times shown' }};
      }}
      rows.push({{ lesson: J.lesson, matches_job: el.length === want.length && !miss.length, elements: el.map(e => e.slice(0, 70)), span }});
    }}
  }}
  return {{ ok: ok.length, of: JOBS.length, problems: TIMES ? problems.length : problems, rows }};
}}
"""
Path(out).write_text(body, encoding="utf-8")
log.info(f"{out}: {len(jobs)} videos to check")
