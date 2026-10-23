// Probe the vote.nz voting-place finder (map.vote.nz) with headless Chromium and record the data endpoints it calls.
// Usage: NODE_PATH=/opt/node22/lib/node_modules node tools/howtovote_map_probe.js <url> <outdir>
// Writes <outdir>/requests.log (url, status, content-type, bytes) and saves JSON/CSV/GeoJSON responses as files.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [url, outdir] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const log = [];
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', locale: 'en-NZ', viewport: { width: 1366, height: 900 } });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  const page = await ctx.newPage();
  let n = 0;
  page.on('response', async (resp) => {
    try {
      const ct = (resp.headers()['content-type'] || '').toLowerCase();
      const u = resp.url();
      let body = null;
      if (/json|csv|geo|octet|text\/plain/.test(ct) && !/\.(js|css|png|jpg|woff2?)(\?|$)/.test(u)) {
        body = await resp.body().catch(() => null);
      }
      log.push(`${resp.status()} ${ct} ${body ? body.length : '-'} ${u}`);
      if (body && body.length > 200) {
        const ext = /json/.test(ct) ? 'json' : /csv/.test(ct) ? 'csv' : 'txt';
        fs.writeFileSync(path.join(outdir, `resp-${String(++n).padStart(3, '0')}.${ext}`), body);
        fs.appendFileSync(path.join(outdir, 'index.txt'), `resp-${String(n).padStart(3, '0')}.${ext} ${u}\n`);
      }
    } catch (e) { /* ignore */ }
  });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }).catch(e => console.error('ERR', e.message));
  for (let i = 0; i < 12; i++) { const t = await page.title(); if (!/just a moment|attention required/i.test(t)) break; await page.waitForTimeout(2500); }
  await page.waitForTimeout(8000);
  console.error('TITLE', await page.title(), 'URL', page.url());
  fs.writeFileSync(path.join(outdir, 'page.html'), await page.content());
  // try typing an address into any search box to trigger the search API
  const box = await page.$('input[type="search"], input[type="text"], input[placeholder*="address" i], input[placeholder*="search" i]');
  if (box) {
    await box.fill('Wellington');
    await page.waitForTimeout(4000);
    await box.press('Enter').catch(() => {});
    await page.waitForTimeout(6000);
  }
  fs.writeFileSync(path.join(outdir, 'requests.log'), log.join('\n'));
  await browser.close();
})();
