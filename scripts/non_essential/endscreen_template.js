// One video's end screen in YouTube Studio (template "1 video, 1 playlist, 1 subscribe"), each element in the
// last 10 s; the video element is a specific video (JOB.next) or "Best for viewer". Stops if the video already
// has an end screen. Verifies the three elements, then saves (the owner's OK, 2026-10-21).
async (page) => {
  const JOB = __JOB__;   // {id, lesson, next: {prefix, query} | null, playlist}
  const t0 = Date.now();
  const step = s => { JOB.step = s; };
  const fail = m => { throw new Error(JSON.stringify({ video: JOB.lesson, step: JOB.step, error: m })); };
  const wait = ms => page.waitForTimeout(ms);
  const typeIn = async (loc, tc) => { await loc.click({ timeout: 15000 }); await page.keyboard.press('Control+A'); await page.keyboard.type(tc); await page.keyboard.press('Tab'); await wait(700); };
  const minus10 = tc => {                                   // H:MM:SS:FF, or M:SS:FF under an hour
    const p = tc.split(':').map(Number), hasH = p.length === 4, [h, m, s, f] = hasH ? p : [0, ...p];
    const t = h * 3600 + m * 60 + s - 10, pad = n => String(n).padStart(2, '0');
    return hasH ? `${Math.floor(t / 3600)}:${pad(Math.floor(t % 3600 / 60))}:${pad(t % 60)}:${pad(f)}` : `${Math.floor(t / 60)}:${pad(t % 60)}:${pad(f)}`;
  };
  const times = () => page.locator('ytve-endscreen-editor-options-panel input:visible');
  const select = async cls => { const r = await page.locator(cls).first().boundingBox(); if (!r) fail('no ' + cls);
    await page.mouse.click(r.x + r.width / 2, r.y + r.height / 2); await wait(1500); };
  const what = () => page.evaluate(() => { const t = (document.querySelector('ytve-endscreen-editor-options-panel') || {}).innerText || '';
    const m = t.match(/(Subscribe|Playlist|Video): [^\n]+/); return m ? m[0] : (/Best for viewer[^\n]*\n[^\n]*\n?/.test(t) ? 'best-for-viewer?' : t.slice(0, 80)); });

  step('open editor');
  await page.goto(`https://studio.youtube.com/video/${JOB.id}/editor`, { waitUntil: 'domcontentloaded' });
  await page.bringToFront();
  await wait(9000);
  const add = page.getByRole('button', { name: 'Add end screens' });
  if (await add.count() !== 1) fail('no single "Add end screens" button (an end screen already there, or the editor did not load)');
  const already = await page.evaluate(() => /Subscribe: |Playlist: |Video: /.test(document.body.innerText));
  if (already) fail('end screen elements already present');

  step('apply template');
  await add.click({ timeout: 15000 }); await wait(2500);
  await page.locator('tp-yt-paper-item, [role="menuitem"], [role="option"]').filter({ hasText: 'Apply template' }).first().click({ timeout: 15000 });
  await wait(3000);
  await page.locator('[aria-label="1 video, 1 playlist, 1 subscribe"].card').first().click({ timeout: 15000 });
  await wait(5000);

  step('subscribe');
  await select('.ytp-ce-element.ytp-ce-channel');
  const end = (await times().evaluateAll(xs => xs.map(x => x.value)))[1];
  if (!end) fail('no end time');
  const start = minus10(end);
  await typeIn(times().nth(0), start);

  step('playlist');
  await select('.ytp-ce-element.ytp-ce-playlist');
  await page.locator('ytve-endscreen-editor-options-panel').getByText('Playlist: ...').first().click({ timeout: 15000 });
  await wait(3000);
  await page.locator('tp-yt-paper-dialog:visible').getByText(JOB.playlist, { exact: true }).first().click({ timeout: 15000 });
  await wait(2500);
  await typeIn(times().nth(0), start);

  step('video');
  await select('.ytp-ce-element.ytp-ce-video');
  if (JOB.next) {
    await page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Choose specific video' }).first().click({ timeout: 15000 });
    await wait(3500);
    await page.locator('tp-yt-paper-dialog:visible input[placeholder="Search your videos"]').first().click({ timeout: 15000 });
    await page.keyboard.type(JOB.next.query); await page.keyboard.press('Enter'); await wait(4000);
    const cards = page.locator('tp-yt-paper-dialog:visible ytcp-entity-card');
    const n = await cards.count();
    let hit = -1;
    for (let i = 0; i < n; i++) if ((await cards.nth(i).innerText()).trim().startsWith(JOB.next.prefix)) { if (hit >= 0) fail('two cards start with ' + JOB.next.prefix); hit = i; }
    if (hit < 0) fail(`no search result starts with "${JOB.next.prefix}" (${n} results)`);
    await cards.nth(hit).click({ timeout: 15000 }); await wait(3000);
  } else {
    const r = page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Best for viewer' }).first();
    if (await r.getAttribute('aria-checked') !== 'true') { await r.click({ timeout: 15000 }); await wait(1500); }
  }
  await typeIn(times().nth(0), start);

  step('verify');
  const got = {};
  for (const [k, cls] of [['subscribe', '.ytp-ce-element.ytp-ce-channel'], ['playlist', '.ytp-ce-element.ytp-ce-playlist'], ['video', '.ytp-ce-element.ytp-ce-video']]) {
    await select(cls);
    got[k] = { times: await times().evaluateAll(xs => xs.map(x => x.value)), what: await what() };
    if (got[k].times[0] !== start || got[k].times[1] !== end) fail(`${k} times ${got[k].times} != ${start}-${end}`);
  }
  if (!got.subscribe.what.startsWith('Subscribe: ')) fail('subscribe: ' + got.subscribe.what);
  if (got.playlist.what !== 'Playlist: ' + JOB.playlist) fail('playlist: ' + got.playlist.what);
  if (JOB.next && !got.video.what.startsWith('Video: ' + JOB.next.prefix)) fail('video: ' + got.video.what);
  if (!JOB.next) {
    const best = await page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Best for viewer' }).first().getAttribute('aria-checked');
    if (best !== 'true') fail('video element is not Best for viewer');
    got.video.what = 'Best for viewer';
  }

  step('save');
  const save = page.locator('ytcp-button, button').filter({ hasText: /^\s*Save\s*$/ }).first();
  if (await save.getAttribute('aria-disabled') === 'true') fail('Save is disabled: ' + await page.evaluate(() => document.body.innerText.match(/Please [^\n]+/)?.[0]));
  await save.click({ timeout: 15000 });
  await wait(7000);
  const after = await page.evaluate(() => document.body.innerText);
  const saved = /End screen\s+Edit/.test(after) && after.includes('Playlist: ');
  if (!saved) fail('after Save the editor does not show the end screen elements');
  return { video: JOB.lesson, start, end, ...Object.fromEntries(Object.entries(got).map(([k, v]) => [k, v.what])), seconds: Math.round((Date.now() - t0) / 1000) };
}
