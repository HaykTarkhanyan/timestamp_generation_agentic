// Runs one Playwright file from .playwright-mcp/ (an end-screen job, batch or verify file: `async (page) => {...}`) in a
// headless Chrome with the login exported from the Playwright MCP browser, so a second batch can run beside the
// visible one (a background tab in the same browser is throttled and its clicks do not land, 2026-10-28).
//
//   node scripts/non_essential/run_endscreen_headless.js <playwright-core dir> <storage state .json> <file.js> [result.json] [--ua "<user agent>"]
//
// playwright-core: the MCP's own copy (npm-cache/_npx/<hash>/node_modules/playwright-core), channel "chrome" = the
// installed Google Chrome, as the MCP uses. Storage state: `page.context().storageState({ path })` from the MCP browser,
// kept in the gitignored scripts/.secrets/; only Google and YouTube cookies are loaded. Prints a line per page opened
// (time and URL, for an ETA), then the file's result as JSON. Same time per video as the visible browser.
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const uaAt = args.indexOf('--ua');
const userAgent = uaAt >= 0 ? args.splice(uaAt, 2)[1] : undefined;
const [pwDir, statePath, file, outPath] = args;
if (!pwDir || !statePath || !file) { console.error('usage: <playwright-core dir> <storage state .json> <file.js> [result.json] [--ua "..."]'); process.exit(2); }
const { chromium } = require(path.resolve(pwDir));

(async () => {
  const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  const keep = d => /(^|\.)(google\.[a-z.]+|youtube\.com)$/.test(d.replace(/^\./, ''));
  state.cookies = state.cookies.filter(c => keep(c.domain));
  state.origins = state.origins.filter(o => keep(new URL(o.origin).hostname));
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const context = await browser.newContext({ storageState: state, viewport: { width: 1280, height: 576 }, userAgent });
  const page = await context.newPage();
  const t0 = Date.now();
  page.on('framenavigated', f => { if (f === page.mainFrame()) console.log(`${Math.round((Date.now() - t0) / 1000)}s ${f.url()}`); });
  const fn = eval(fs.readFileSync(file, 'utf8'));
  let result, code = 0;
  try { result = await fn(page); } catch (e) { result = { error: String((e && e.message) || e) }; code = 1; }
  console.log(JSON.stringify(result));
  if (outPath) fs.writeFileSync(outPath, JSON.stringify(result, null, 1));
  await browser.close();
  process.exit(code);
})();
