// Change ONLY the video element of an existing end screen in YouTube Studio from JOB.from ("Best for viewer" when absent,
// else the title prefix of the video it points at now) to a specific video (JOB.next). Stops unless the end screen is
// exactly Subscribe + that Video + Playlist, or if Studio runs as another channel than JOB.channel. Keeps every
// element's times; checks Subscribe, Playlist and all times are unchanged and the video is JOB.next, then saves (the
// owner's OK, 2026-10-27).
async (page) => {
  const JOB = __JOB__;   // {id, lesson, channel, next: {prefix, query}, from?}
  const FROM = JOB.from || 'Best for viewer';
  const t0 = Date.now();
  const step = s => { JOB.step = s; };
  const fail = m => { throw new Error(JSON.stringify({ video: JOB.lesson, step: JOB.step, error: m })); };
  const wait = ms => page.waitForTimeout(ms);
  const norm = s => s.replace(/\s+/g, ' ').trim();   // innerText collapses the double spaces some titles have
  const times = () => page.locator('ytve-endscreen-editor-options-panel input:visible');
  // click a point where nothing outside the end-screen overlay is on top: a Subscribe element in the middle of the
  // player has the player's rewind icon over its center (2026-10-28, Հավանականություն Դաս 4)
  const select = async cls => {
    const r = await page.evaluate(c => { const e = [...document.querySelectorAll(c)].find(x => x.getBoundingClientRect().width > 0);
      if (!e) return null; const b = e.getBoundingClientRect();
      const ov = e.closest('ytve-endscreen-editor-preview-overlay'), item = e.closest('ytve-endscreen-editor-preview-overlay-item');
      for (const [fx, fy] of [[0.5, 0.5], [0.3, 0.3], [0.7, 0.7], [0.3, 0.7], [0.7, 0.3], [0.5, 0.2], [0.5, 0.8]]) {
        const x = b.x + b.width * fx, y = b.y + b.height * fy, h = document.elementFromPoint(x, y);
        const other = h && h.closest('ytve-endscreen-editor-preview-overlay-item');
        if (h && ov && ov.contains(h) && (!other || other === item)) return { x, y }; }
      return { covered: true }; }, cls);
    if (!r) fail('no ' + cls);
    if (r.covered) fail(`every point of ${cls} is covered by something outside the end-screen overlay`);
    await page.mouse.click(r.x, r.y); await wait(1500); };
  const radio = label => page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: label }).first();
  const what = () => page.evaluate(() => { const t = (document.querySelector('ytve-endscreen-editor-options-panel') || {}).innerText || '';
    const m = t.match(/(Subscribe|Playlist|Video): [^\n]+/); return m ? m[0] : t.slice(0, 80); });
  const ELS = [['subscribe', '.ytp-ce-element.ytp-ce-channel'], ['playlist', '.ytp-ce-element.ytp-ce-playlist'], ['video', '.ytp-ce-element.ytp-ce-video']];
  const read = async () => { const got = {};
    for (const [k, cls] of ELS) { await select(cls);
      got[k] = { times: (await times().evaluateAll(xs => xs.map(x => x.value))).join('-'),
                 what: k === 'video' && await radio('Best for viewer').getAttribute('aria-checked') === 'true' ? 'Best for viewer' : await what() }; }
    return got; };

  step('open editor');
  await page.goto(`https://studio.youtube.com/video/${JOB.id}/editor`, { waitUntil: 'domcontentloaded' });
  await page.bringToFront();
  // usually ready in ~9 s, sometimes far later, so wait for the End screen entry
  const loaded = await page.waitForFunction(() => /End screen/.test(document.body.innerText), null, { timeout: 40000 }).then(() => true, () => false);
  if (!loaded) fail('the editor did not show its End screen entry within 40 s');
  await wait(3000);
  const session = await page.evaluate(() => window.ytcfg && ytcfg.get('CHANNEL_ID'));
  if (session !== JOB.channel) fail(`Studio runs as channel ${session}, not ${JOB.channel}: switch account first`);
  const listed = await page.evaluate(() => document.body.innerText.match(/(Subscribe|Playlist|Video|Channel|Link): [^\n]*/g) || []);
  // a batch retry after a Save that did go through finds the target already set: skip, nothing touched
  if (listed.some(e => norm(e).startsWith(norm('Video: ' + JOB.next.prefix)))) fail('ALREADY: the video element already points at the target');
  if (listed.length !== 3 || !listed.some(e => norm(e).startsWith(norm('Video: ' + FROM))))
    fail(`end screen is not Subscribe + Video: ${FROM} + Playlist: ` + listed.join(' | '));

  step('open end screen');
  // by link name: a video with Info cards has a second Edit button in the entry panel (2026-10-28, Հավանականություն Դաս 4)
  await page.getByRole('link', { name: 'End screen Edit' }).click({ timeout: 15000 }); await wait(4000);
  const before = await read();
  if (!norm(before.video.what).startsWith(norm(FROM === 'Best for viewer' ? FROM : 'Video: ' + FROM))) fail('video element is ' + before.video.what);

  step('video');
  await select('.ytp-ce-element.ytp-ce-video');
  // the third radio opens the video picker: labelled "Choose specific video", or "Video: <title>" once one is chosen
  await radio(FROM === 'Best for viewer' ? 'Choose specific video' : 'Video: ').click({ timeout: 15000 });
  await wait(3500);
  // the search box can refuse keyboard focus, so set its value and press Enter from inside the page
  const searched = await page.evaluate(q => {
    const i = document.querySelector('tp-yt-paper-dialog #search-yours'); if (!i) return false;
    i.value = q; i.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
    for (const type of ['keydown', 'keypress', 'keyup'])
      i.dispatchEvent(new KeyboardEvent(type, { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, composed: true }));
    return true;
  }, JOB.next.query);
  if (!searched) fail('no #search-yours input in the video dialog');
  // results can take 10 s to arrive, so poll
  const cards = page.locator('tp-yt-paper-dialog:visible ytcp-entity-card');
  let hit = -1, n = 0;
  for (let tries = 0; tries < 10 && hit < 0; tries++) {
    await wait(2000);
    n = await cards.count();
    for (let i = 0; i < n; i++) if (norm(await cards.nth(i).innerText()).startsWith(norm(JOB.next.prefix))) { if (hit >= 0) fail('two cards start with ' + JOB.next.prefix); hit = i; }
  }
  if (hit < 0) fail(`no search result starts with "${JOB.next.prefix}" (${n} results after 20 s)`);
  await cards.nth(hit).click({ timeout: 15000 }); await wait(3000);

  step('verify');
  const after = await read();
  for (const k of ['subscribe', 'playlist']) if (after[k].what !== before[k].what) fail(`${k} changed: ${before[k].what} -> ${after[k].what}`);
  for (const [k] of ELS) if (after[k].times !== before[k].times) fail(`${k} times changed: ${before[k].times} -> ${after[k].times}`);
  if (!norm(after.video.what).startsWith(norm('Video: ' + JOB.next.prefix))) fail('video: ' + after.video.what);

  step('save');
  const save = page.locator('ytcp-button, button').filter({ hasText: /^\s*Save\s*$/ }).first();
  if (await save.getAttribute('aria-disabled') === 'true') fail('Save is disabled: ' + await page.evaluate(() => document.body.innerText.match(/Please [^\n]+/)?.[0]));
  await save.click({ timeout: 15000 });
  // Save can take well over 7 s, so poll
  const saved = await page.waitForFunction(v => { const t = document.body.innerText.replace(/\s+/g, ' '); return /End screen Edit/.test(t) && t.includes(v); },
    norm('Video: ' + JOB.next.prefix), { timeout: 30000 }).then(() => true, () => false);
  if (!saved) fail('30 s after Save the editor does not show the new video element');
  return { video: JOB.lesson, times: after.video.times, was: before.video.what, now: after.video.what, playlist: after.playlist.what,
           seconds: Math.round((Date.now() - t0) / 1000) };
}
