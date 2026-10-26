// Enters one batch of cuts in YouTube Studio's editor (Trim & cut). Template: the batch files are made by
//     python scripts/cut_list.py entry-js --output-dir output/<dir>
// which fills in JOB below and writes .playwright-mcp/studio_entry_<id>_NNofMM.js, one per batch, plus a
// read-only _dryrun.js.
// Run a batch with the Playwright MCP tool browser_run_code_unsafe(filename=<that file>) in the user's
// signed-in Studio tab, with the Trim & cut panel open. Never presses Save and never navigates the tab.
//
// Per cut (the order measured on ML48/ML49): playhead to the cut's start (the time box outside the panel),
// New Cut, end box, the start box only if it doesn't already read the cut's start (since 2026-10-25), the
// panel's Cut button, then wait until the cut is among Studio's trim markers. The result carries msPerCut.
// Cuts already in Studio are skipped, so a batch that stopped halfway can simply be run again.
// Any surprise throws, with the cuts done so far in the message. Per cut: ~6 s on an empty timeline (ML51),
// 8-15 s with 0-42 cuts in (Tserunyan Դաս 16, the old loop). A call over ~120 s moves to the background; fine.
async (page) => {
  const JOB = __JOB__;  // {video, overOneHour, batch, batches, dryRun, cuts: [[n, 'H:MM:SS:FF', 'H:MM:SS:FF'], ...]}
  const t0 = Date.now();
  const done = [];
  let already = [];
  const fail = (msg, extra = {}) => { throw new Error(JSON.stringify({ error: msg, done, already, ...extra })); };

  if (!page.url().includes(`/video/${JOB.video}/editor`)) fail(`not on the editor of ${JOB.video}: ${page.url()}`);
  // A window behind other windows stops drawing frames, and a click then hangs after it took effect
  // (lesson 12, 2026-10-21: New Cut opened cut 3's row, the click timed out, the screenshot too)
  await page.bringToFront();
  // With ~90+ cuts on the timeline Studio takes over 5 s to take a click (Papikian Դաս 16, 2026-10-22:
  // the clicks on cuts 73, 92 and 93 timed out after they took effect), so allow 30 s
  const CLICK_MS = 30000;
  const editRow = page.locator('#panel-container input:visible');
  const openRow = async n => { if (await editRow.count() !== 0)
    fail(`${n ? `cut ${n}: ` : ''}a cut's editing row is already open (a half-made cut): finish it (end, start, Cut) or cancel it first`); };
  // Studio types and labels times without the hour field on videos under an hour (MM:SS:FF)
  const full = tc => (tc.split(':').length === 4 ? tc : `0:${tc}`);
  // On some uploads Studio stores every cut one frame later than typed (Papikian Դաս 20, 2026-10-22:
  // typed 0:00:24:05-0:00:28:01, stored 0:00:24:06-0:00:28:02), so cut_list.py entry-js --type-shift -1
  // types each time that many frames off; the checks below still use the planned times
  const shifted = tc => {
    if (!JOB.typeShift) return tc;
    const [h, m, s, f] = full(tc).split(':').map(Number);
    let n = ((h * 60 + m) * 60 + s) * JOB.fps + f + JOB.typeShift;
    const ff = n % JOB.fps; n = (n - ff) / JOB.fps;
    const ss = n % 60; n = (n - ss) / 60;
    const p2 = x => String(x).padStart(2, '0');
    return `${(n - n % 60) / 60}:${p2(n % 60)}:${p2(ss)}:${p2(ff)}`;
  };
  const typed = tc => { const t = shifted(tc); return JOB.overOneHour ? t : t.replace(/^0:/, ''); };
  const cutsInStudio = async () => {
    const m = (await page.evaluate(() => [...document.querySelectorAll(
      '[aria-label^="Start trim marker"], [aria-label^="End trim marker"]')]
      .map(e => e.getAttribute('aria-label').replace(/^(Start|End) trim marker /, '')))).map(full);
    const pairs = [];
    for (let i = 2; i < m.length; i += 2) pairs.push(`${m[i]}-${m[i + 1]}`);   // pair 0 is the whole-video trim
    return pairs;
  };
  // One insertText instead of a keystroke per character (2026-10-25, tested on Tserunyan Դաս 16 cut 99: the box
  // read back exactly). With 100+ cuts in, Studio takes 2-4 s to answer any event, so fewer events matter more
  const typeIn = async (loc, tc, slow = false) => {
    await loc.click({ timeout: CLICK_MS });
    await page.keyboard.press('Control+A');
    if (slow) await page.keyboard.type(typed(tc), { delay: 40 }); else await page.keyboard.insertText(typed(tc));
    await page.keyboard.press('Tab');
    await page.waitForTimeout(300);
  };
  // With ~75 cuts on the timeline the page lags enough to drop or reorder keystrokes (Papikian Դաս 17,
  // 2026-10-22: the playhead box read "1:0117:55:" for cut 76, New Cut stayed disabled), so the playhead
  // time is typed slower and read back, and retyped up to 3 times before giving up
  const typePlayhead = async (n, tc) => {
    for (let attempt = 1; ; attempt++) {
      await typeIn(playhead, tc, attempt > 1);   // insertText first, then the slow keystrokes
      await page.waitForTimeout(300 * (attempt - 1));
      const got = (await playhead.inputValue()).trim();
      if (got === typed(tc)) return;
      if (attempt === 3) fail(`cut ${n}: typed ${typed(tc)} into the playhead box, it reads "${got}" after 3 tries`);
    }
  };
  const playhead = page.locator('input[aria-label*="frame"]:visible:not(#panel-container input)');
  const nph = await playhead.count();
  if (nph !== 1) fail(`${nph} playhead time boxes outside the panel, expected 1`);
  const label = await playhead.getAttribute('aria-label');
  if (/hour/.test(label) !== JOB.overOneHour) fail(`playhead label "${label}" does not fit overOneHour=${JOB.overOneHour}`);
  if (await page.getByRole('button', { name: 'New Cut' }).count() !== 1) fail('no single New Cut button: is the Trim & cut panel open?');
  await openRow(0);

  const before = await cutsInStudio();
  already = JOB.cuts.filter(([, s, e]) => before.includes(`${s}-${e}`)).map(([n]) => n);
  const todo = JOB.cuts.filter(([n]) => !already.includes(n));
  if (JOB.dryRun) return { dryRun: true, playheadLabel: label, cutsInStudio: before.length, alreadyInStudio: already.length, toEnter: todo.length };

  // Poll for a state instead of sleeping a fixed time (until 2026-10-25: 700 ms after New Cut, 800 ms after Cut)
  const until = async (cond, what) => {
    const t1 = Date.now();
    while (!(await cond())) {
      if (Date.now() - t1 > CLICK_MS) fail(what);
      await page.waitForTimeout(100);
    }
  };
  const ms = { playhead: 0, newCut: 0, end: 0, start: 0, cut: 0 };   // where the time goes, summed over the batch
  let lapT = Date.now(), startsTyped = 0;
  const startSeen = [];   // what the start box read when it was not the cut's start (first 3)
  // " 1 hour 8 minutes 11 seconds 23 frames" -> "1:08:11:23" (no hour part under an hour; "1 hour", "2 hours")
  const labelTc = lbl => {
    const g = k => Number((lbl.match(new RegExp(`(\\d+) ${k}`)) || [0, 0])[1]);
    const p2 = x => String(x).padStart(2, '0');
    return `${g('hour')}:${p2(g('minute'))}:${p2(g('second'))}:${p2(g('frame'))}`;
  };
  const lap = k => { const now = Date.now(); ms[k] += now - lapT; lapT = now; };

  for (const [n, s, e] of todo) {
    if (await playhead.count() !== 1) fail(`cut ${n}: playhead time box not unique`);
    await openRow(n);
    lapT = Date.now();
    await typePlayhead(n, s); lap('playhead');
    await page.getByRole('button', { name: 'New Cut' }).click({ timeout: CLICK_MS });
    await until(async () => (await editRow.count()) === 2, `cut ${n}: the editing row did not open with 2 inputs`); lap('newCut');
    await typeIn(editRow.nth(1), e);
    if ((await editRow.nth(1).inputValue()).trim() !== typed(e)) await typeIn(editRow.nth(1), e, true);
    lap('end');
    // New Cut starts the cut at the playhead, which is already on the cut's start: type the start only if the
    // box says otherwise (the user, 2026-10-25: "i think you have a redundant step"). The box's value stays
    // empty until typed into; its aria-label carries the time (" 1 hour 8 minutes 11 seconds 23 frames",
    // Tserunyan Դաս 16 cut 85), so that is what is compared
    const startLabel = (await editRow.nth(0).getAttribute('aria-label')) || '';
    if (labelTc(startLabel) !== full(shifted(s))) {
      if (startSeen.length < 3) startSeen.push({ n, label: startLabel, want: full(shifted(s)) });
      await typeIn(editRow.nth(0), s); startsTyped++;
    }
    lap('start');
    await page.locator('#panel-container').getByRole('button', { name: 'Cut', exact: true }).click({ timeout: CLICK_MS });
    await until(async () => (await cutsInStudio()).includes(`${s}-${e}`), `cut ${n} (${s}-${e}) not in Studio after Cut`); lap('cut');
    done.push(n);
  }
  const per = Object.fromEntries(Object.entries(ms).map(([k, v]) => [k, done.length ? Math.round(v / done.length) : 0]));
  return { batch: `${JOB.batch} of ${JOB.batches}`, done, already, cutsInStudio: (await cutsInStudio()).length,
           seconds: Math.round((Date.now() - t0) / 1000), msPerCut: per, startsTyped, startSeen };
}
