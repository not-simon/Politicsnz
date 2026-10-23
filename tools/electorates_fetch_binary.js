// Usage: node tools/electorates_fetch_binary.js <landing-url> <file-url> <outfile>
// Visits landing page with headless Chromium (passes bot check), then downloads file-url with same cookies.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [landing, url, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', locale: 'en-NZ' });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  const page = await ctx.newPage();
  await page.goto(landing, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(e => console.error('ERR', e.message));
  await page.waitForTimeout(3000);
  const r = await ctx.request.get(url, { timeout: 60000 });
  console.error('STATUS', r.status(), r.headers()['content-type']);
  fs.writeFileSync(out, await r.body());
  await browser.close();
})();
