// Enters one batch of cuts in YouTube Studio's editor (Trim & cut). Template: the batch files are made by
//     python scripts/cut_list.py entry-js --output-dir output/<dir>
// which fills in JOB below and writes .playwright-mcp/studio_entry_<id>_NNofMM.js, one per batch, plus a
// read-only _dryrun.js.
// Run a batch with the Playwright MCP tool browser_run_code_unsafe(filename=<that file>) in the user's
// signed-in Studio tab, with the Trim & cut panel open. Never presses Save and never navigates the tab.
//
// Per cut (the order measured on ML48/ML49): playhead to the cut's start (the time box outside the panel),
// New Cut, end box, start box, the panel's Cut button, then check the cut is among Studio's trim markers.
// Cuts already in Studio are skipped, so a batch that stopped halfway can simply be run again.
// Any surprise throws, with the cuts done so far in the message. ~6 s per cut (ML51: 15 cuts in 87 s);
// keep a batch under ~100 s, the MCP moves calls over ~120 s to the background.
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
  const editRow = page.locator('#panel-container input:visible');
  const openRow = async n => { if (await editRow.count() !== 0)
    fail(`${n ? `cut ${n}: ` : ''}a cut's editing row is already open (a half-made cut): finish it (end, start, Cut) or cancel it first`); };
  // Studio types and labels times without the hour field on videos under an hour (MM:SS:FF)
  const typed = tc => (JOB.overOneHour ? tc : tc.replace(/^0:/, ''));
  const full = tc => (tc.split(':').length === 4 ? tc : `0:${tc}`);
  const cutsInStudio = async () => {
    const m = (await page.evaluate(() => [...document.querySelectorAll(
      '[aria-label^="Start trim marker"], [aria-label^="End trim marker"]')]
      .map(e => e.getAttribute('aria-label').replace(/^(Start|End) trim marker /, '')))).map(full);
    const pairs = [];
    for (let i = 2; i < m.length; i += 2) pairs.push(`${m[i]}-${m[i + 1]}`);   // pair 0 is the whole-video trim
    return pairs;
  };
  const typeIn = async (loc, tc) => {
    await loc.click({ timeout: 5000 });
    await page.keyboard.press('Control+A');
    await page.keyboard.type(typed(tc));
    await page.keyboard.press('Tab');
    await page.waitForTimeout(300);
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

  for (const [n, s, e] of todo) {
    if (await playhead.count() !== 1) fail(`cut ${n}: playhead time box not unique`);
    await openRow(n);
    await typeIn(playhead, s);
    await page.getByRole('button', { name: 'New Cut' }).click({ timeout: 5000 });
    await page.waitForTimeout(700);
    const nr = await editRow.count();
    if (nr !== 2) fail(`cut ${n}: the editing row has ${nr} inputs, expected 2`);
    await typeIn(editRow.nth(1), e);
    await typeIn(editRow.nth(0), s);
    await page.locator('#panel-container').getByRole('button', { name: 'Cut', exact: true }).click({ timeout: 5000 });
    await page.waitForTimeout(800);
    if (!(await cutsInStudio()).includes(`${s}-${e}`)) fail(`cut ${n} (${s}-${e}) not in Studio after Cut`);
    done.push(n);
  }
  return { batch: `${JOB.batch} of ${JOB.batches}`, done, already, cutsInStudio: (await cutsInStudio()).length,
           seconds: Math.round((Date.now() - t0) / 1000) };
}
