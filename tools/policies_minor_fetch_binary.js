// Usage: node tools/policies_minor_fetch_binary.js <warmup-url> <file-url> <outfile>
// Visits warmup-url in headless Chromium (to pass bot checks such as Incapsula), then downloads file-url
// with the same browser context (cookies) and saves it to outfile.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [warm, url, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', locale: 'en-NZ', acceptDownloads: true });
  const page = await ctx.newPage();
  await page.goto(warm, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(e => console.error('ERR', e.message));
  await page.waitForTimeout(4000);
  let body = null;
  const p2 = await ctx.newPage();
  try {
    const [dl] = await Promise.all([p2.waitForEvent('download', { timeout: 60000 }), p2.goto(url).catch(() => {})]);
    await dl.saveAs(out); console.error('DOWNLOADED via download event');
  } catch (e) {
    const resp = await ctx.request.get(url, { timeout: 60000 });
    body = await resp.body();
    console.error('STATUS', resp.status(), resp.headers()['content-type'], body.length);
    fs.writeFileSync(out, body);
  }
  await browser.close();
})();
