// One video's end screen in YouTube Studio (template "1 video, 1 playlist, 1 subscribe"), each element in the
// last JOB.seconds (default 10; 5 for videos ending in YSU's ~5.5 s outro, Studio's minimum); the video element is a specific video (JOB.next) or "Best for viewer". Stops if the video already
// has an end screen, or if Studio runs as another channel than JOB.channel. Verifies the three elements, then saves
// (the owner's OK, 2026-10-21). With JOB.rebuild (the element kinds the old end screen must have, e.g. ["Subscribe",
// "Video", "Video"]) it instead deletes that old end screen's elements and builds the standard one in the same Save.
// With JOB.layout "video+playlist" it uses the template "1 video, 1 playlist" (no Subscribe): Studio offers no
// 3-element template for portrait or square videos (2026-10-28, Arnak's 1440x1662 and 1760x1920 lessons).
// With JOB.rebuild + JOB.retimeFrom (seconds) it rebuilds only our own standard end screen of that length at
// JOB.seconds; any other end screen, or one already at JOB.seconds, is skipped untouched ("ALREADY:"). Rebuild works
// with either layout (2-element: JOB.rebuild ["Video", "Playlist"]).
async (page) => {
  const JOB = __JOB__;   // {id, lesson, channel, next: {prefix, query, id?} | null, playlist, rebuild?, layout?, seconds?, retimeFrom?}
  const SECS = JOB.seconds || 10;
  const t0 = Date.now();
  const step = s => { JOB.step = s; };
  const fail = m => { throw new Error(JSON.stringify({ video: JOB.lesson, step: JOB.step, error: m })); };
  const wait = ms => page.waitForTimeout(ms);
  const norm = s => s.replace(/\s+/g, ' ').trim();   // innerText collapses the double spaces some titles have
  const typeIn = async (loc, tc) => { await loc.click({ timeout: 15000 }); await page.keyboard.press('Control+A'); await page.keyboard.type(tc); await page.keyboard.press('Tab'); await wait(700); };
  // H:MM:SS:FF, or M:SS:FF / MM:SS:FF under an hour. The minutes take the width of the end time, which follows the
  // video's length: "09:40:14" on a 10:01 video, "7:35:18" on a 7:46 one (2026-10-28, Vahagn 4.2 and 6.1)
  // frame: one more frame back. At Studio's 5 s minimum an exact 5 s can count as less ("Element must be visible for at
  // least 5 seconds", Save disabled: 2026-10-28, Մաթ. անալիզ 3 (ԿՎՏԳ) Դաս 23, 43:38:13-43:43:13; 43:38:12 saved).
  // Frame 0 borrows a second and takes frame 23, valid at 24, 25 and 30 fps and still over 5 s
  const back = (tc, secs, frame = false) => {
    let p = tc.split(':').map(Number), hasH = p.length === 4, [h, m, s, f] = hasH ? p : [0, ...p];
    if (frame) { if (f > 0) f -= 1; else { s -= 1; f = 23; } }
    const t = h * 3600 + m * 60 + s - secs, pad = (n, w = 2) => String(n).padStart(w, '0');
    return hasH ? `${Math.floor(t / 3600)}:${pad(Math.floor(t % 3600 / 60))}:${pad(t % 60)}:${pad(f)}`
      : `${pad(Math.floor(t / 60), tc.split(':')[0].length)}:${pad(t % 60)}:${pad(f)}`;
  };
  const times = () => page.locator('ytve-endscreen-editor-options-panel input:visible');
  // the first element with a size: deleted ones stay in the page with none, and in edit mode the others are
  // visibility:hidden until the playhead reaches them, so :visible misses them (2026-10-27, rebuild)
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
  const what = () => page.evaluate(() => { const t = (document.querySelector('ytve-endscreen-editor-options-panel') || {}).innerText || '';
    const m = t.match(/(Subscribe|Playlist|Video): [^\n]+/); return m ? m[0] : (/Best for viewer[^\n]*\n[^\n]*\n?/.test(t) ? 'best-for-viewer?' : t.slice(0, 80)); });

  step('open editor');
  await page.goto(`https://studio.youtube.com/video/${JOB.id}/editor`, { waitUntil: 'domcontentloaded' });
  await page.bringToFront();
  // usually ready in ~9 s, sometimes far later (2026-10-27, ML [45]), so wait for the End screen entry
  const loaded = await page.waitForFunction(() => /End screen/.test(document.body.innerText), null, { timeout: 40000 }).then(() => true, () => false);
  if (!loaded) fail('the editor did not show its End screen entry within 40 s');
  await wait(3000);
  // Studio opens any managed channel's video under the channel used last; search and playlists would be that one's
  const session = await page.evaluate(() => window.ytcfg && ytcfg.get('CHANNEL_ID'));
  if (session !== JOB.channel) fail(`Studio runs as channel ${session}, not ${JOB.channel}: switch account first`);
  const twoEl = JOB.layout === 'video+playlist';
  const card = page.locator(`[aria-label="${twoEl ? '1 video, 1 playlist' : '1 video, 1 playlist, 1 subscribe'}"].card`).first();
  if (JOB.rebuild) {
    step('rebuild: check old');
    const listed = (await page.evaluate(() => document.body.innerText.match(/(Subscribe|Playlist|Video|Channel|Link): [^\n]*/g) || [])).map(norm);
    const standard = listed.length === (twoEl ? 2 : 3) && listed.some(e => e.startsWith(norm('Playlist: ' + JOB.playlist)))
        && listed.some(e => e.startsWith(norm('Video: ' + (JOB.next ? JOB.next.prefix : 'Best for viewer'))));
    // a batch retry after a Save that did go through finds the standard end screen: skip, nothing touched
    if (standard && !JOB.retimeFrom) fail('ALREADY: rebuilt before');
    if (JOB.retimeFrom && !standard) fail(`ALREADY: not ours: [${listed.join(' | ').slice(0, 150)}]`);
    const kinds = listed.map(e => e.split(':')[0]).sort();
    if (JSON.stringify(kinds) !== JSON.stringify([...JOB.rebuild].sort())) fail(`old end screen is [${listed.join(' | ')}], expected kinds [${JOB.rebuild}]`);
    await page.getByRole('link', { name: 'End screen Edit' }).click({ timeout: 15000 }); await wait(4000);
    if (JOB.retimeFrom) {
      // opening the editor selects the first element; ours have all three at the same times
      step('retime: check times');
      const tt = await times().evaluateAll(xs => xs.map(x => x.value));
      if (tt.length < 2 || !tt[1]) fail('no times shown for the selected element');
      if (tt[0] === back(tt[1], SECS) || tt[0] === back(tt[1], SECS, true)) fail(`ALREADY: at ${SECS} s`);
      // retimeFrom "any": any standard end screen not already at SECS (the user's Q44d: Խմբերի տեսություն at 9-10 s)
      if (JOB.retimeFrom !== 'any' && tt[0] !== back(tt[1], JOB.retimeFrom)) fail(`ALREADY: not ours: times ${tt.join('-')}`);
    }
    step('rebuild: delete');
    const panelText = () => page.evaluate(() => (document.querySelector('ytve-endscreen-editor-options-panel') || {}).innerText || '');
    // opening the editor selects the first element and deleting one selects the next, so only the panel's trash is
    // needed (2026-10-27: 8 videos done this way by hand after clicks on the hidden elements kept failing)
    for (let i = 0; i < JOB.rebuild.length; i++) {
      if (!/^\s*Element\s+(Subscribe|Video|Playlist|Channel|Link) element/.test(await panelText())) fail(`no element selected to delete (${i} deleted)`);
      await page.locator('ytve-endscreen-editor-options-panel ytcp-icon-button[aria-label="Delete element"]').first().click({ timeout: 10000 });
      await wait(2000);
    }
    // portrait videos list only 2-element templates, so match the part both template names share
    if (!/1 video, 1 playlist/.test(await panelText())) fail('the template list is not shown after deleting the old elements');
    step('rebuild: apply template');
    await card.click({ timeout: 15000 });
    await wait(5000);
  } else {
    const add = page.getByRole('button', { name: 'Add end screens' });
    // "ALREADY:" errors come before anything is touched, so a batch may skip the video and go on
    if (await add.count() !== 1) {
      const has = await page.evaluate(() => /End screen\s+Edit/.test(document.body.innerText));
      fail(has ? 'ALREADY: the video already has an end screen' : 'no single "Add end screens" button (the editor did not load?)');
    }
    const already = await page.evaluate(() => /Subscribe: |Playlist: |Video: /.test(document.body.innerText));
    if (already) fail('ALREADY: end screen elements already present');

    step('apply template');
    await add.click({ timeout: 15000 }); await wait(2500);
    await page.locator('tp-yt-paper-item, [role="menuitem"], [role="option"]').filter({ hasText: 'Apply template' }).first().click({ timeout: 15000 });
    await wait(3000);
    await card.click({ timeout: 15000 });
    await wait(5000);
  }

  // the first element handled reads the template's end time (the video's end); every element starts 10 s before it
  let end, start;
  const span = async () => {
    end = (await times().evaluateAll(xs => xs.map(x => x.value)))[1];
    if (!end) fail('no end time');
    start = back(end, SECS, SECS <= 5);
  };
  if (!twoEl) {
    step('subscribe');
    await select('.ytp-ce-element.ytp-ce-channel');
    await span();
    await typeIn(times().nth(0), start);
  }

  step('playlist');
  await select('.ytp-ce-element.ytp-ce-playlist');
  if (twoEl) await span();
  await page.locator('ytve-endscreen-editor-options-panel').getByText('Playlist: ...').first().click({ timeout: 15000 });
  await wait(3000);
  const plItem = page.locator('tp-yt-paper-dialog:visible').getByText(JOB.playlist, { exact: true }).first();
  // the picker lists only 20 of the channel's playlists (2026-10-28: "Մաթեմատիկական անալիզ 3 (տվյալագետների համար)" was
  // not among them); its "Any playlist on YouTube" box finds one by URL, but only with real typing (a value set from
  // the page searched nothing)
  if (!await plItem.count() && JOB.playlistId) {
    await page.locator('tp-yt-paper-dialog:visible #search-any').click({ timeout: 10000 });
    await page.keyboard.press('Control+A');
    await page.keyboard.insertText(`https://www.youtube.com/playlist?list=${JOB.playlistId}`);
    await page.keyboard.press('Enter');
    await plItem.waitFor({ timeout: 20000 }).catch(() => fail(`playlist ${JOB.playlistId} not found by URL in 20 s`));
  }
  await plItem.click({ timeout: 15000 });
  await wait(2500);
  await typeIn(times().nth(0), start);

  step('video');
  await select('.ytp-ce-element.ytp-ce-video');
  if (JOB.next) {
    await page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Choose specific video' }).first().click({ timeout: 15000 });
    await wait(3500);
    // the search box can refuse keyboard focus (2026-10-27: typed text went nowhere, the list stayed the 50 newest),
    // so set its value and press Enter from inside the page
    const searched = await page.evaluate(q => {
      const i = document.querySelector('tp-yt-paper-dialog #search-yours'); if (!i) return false;
      i.value = q; i.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
      for (const type of ['keydown', 'keypress', 'keyup'])
        i.dispatchEvent(new KeyboardEvent(type, { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true, composed: true }));
      return true;
    }, JOB.next.query);
    if (!searched) fail('no #search-yours input in the video dialog');
    // results can take 10 s to arrive (2026-10-27: 0 cards at 2 s and 6 s, the match at 10 s), so poll
    const cards = page.locator('tp-yt-paper-dialog:visible ytcp-entity-card');
    let hit = -1, n = 0;
    // an older upload can share the title (2026-10-28, Vahagn 22.1 and its replaced upload): with JOB.next.id only the
    // card whose thumbnail is that video's ("vi_webp/<id>/") counts
    const isNext = async c => !JOB.next.id || await c.evaluate((e, id) => e.outerHTML.includes(`/${id}/`), JOB.next.id);
    for (let tries = 0; tries < 10 && hit < 0; tries++) {
      await wait(2000);
      n = await cards.count();
      for (let i = 0; i < n; i++) if (norm(await cards.nth(i).innerText()).startsWith(norm(JOB.next.prefix)) && await isNext(cards.nth(i))) { if (hit >= 0) fail('two cards start with ' + JOB.next.prefix); hit = i; }
    }
    if (hit < 0) fail(`no search result starts with "${JOB.next.prefix}" (${n} results after 20 s)`);
    await cards.nth(hit).click({ timeout: 15000 }); await wait(3000);
  } else {
    const r = page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Best for viewer' }).first();
    if (await r.getAttribute('aria-checked') !== 'true') { await r.click({ timeout: 15000 }); await wait(1500); }
  }
  await typeIn(times().nth(0), start);

  step('verify');
  const got = {};
  const kinds = [['subscribe', '.ytp-ce-element.ytp-ce-channel'], ['playlist', '.ytp-ce-element.ytp-ce-playlist'], ['video', '.ytp-ce-element.ytp-ce-video']];
  for (const [k, cls] of twoEl ? kinds.slice(1) : kinds) {
    await select(cls);
    got[k] = { times: await times().evaluateAll(xs => xs.map(x => x.value)), what: await what() };
    if (got[k].times[0] !== start || got[k].times[1] !== end) fail(`${k} times ${got[k].times} != ${start}-${end}`);
  }
  if (!twoEl && !got.subscribe.what.startsWith('Subscribe: ')) fail('subscribe: ' + got.subscribe.what);
  if (norm(got.playlist.what) !== norm('Playlist: ' + JOB.playlist)) fail('playlist: ' + got.playlist.what);
  if (JOB.next && !norm(got.video.what).startsWith(norm('Video: ' + JOB.next.prefix))) fail('video: ' + got.video.what);
  if (JOB.next?.id && !await page.evaluate(id => [...document.querySelectorAll('.ytp-ce-element.ytp-ce-video')].some(e => e.outerHTML.includes(`/${id}/`)), JOB.next.id))
    fail(`the video element does not show ${JOB.next.id}'s thumbnail`);
  if (!JOB.next) {
    const best = await page.locator('ytve-endscreen-editor-options-panel tp-yt-paper-radio-button').filter({ hasText: 'Best for viewer' }).first().getAttribute('aria-checked');
    if (best !== 'true') fail('video element is not Best for viewer');
    got.video.what = 'Best for viewer';
  }

  step('save');
  const save = page.locator('ytcp-button, button').filter({ hasText: /^\s*Save\s*$/ }).first();
  if (await save.getAttribute('aria-disabled') === 'true') fail('Save is disabled: ' + await page.evaluate(() => document.body.innerText.match(/Please [^\n]+/)?.[0]));
  await save.click({ timeout: 15000 });
  // Save can take well over 7 s (2026-10-27, ML [12]: shown as saved only later, and it was), so poll
  const saved = await page.waitForFunction(() => { const t = document.body.innerText; return /End screen\s+Edit/.test(t) && t.includes('Playlist: '); },
    null, { timeout: 30000 }).then(() => true, () => false);
  if (!saved) fail('30 s after Save the editor does not show the end screen elements');
  return { video: JOB.lesson, start, end, ...Object.fromEntries(Object.entries(got).map(([k, v]) => [k, v.what])), seconds: Math.round((Date.now() - t0) / 1000) };
}
