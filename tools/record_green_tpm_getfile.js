// Usage: node tools/record_green_tpm_getfile.js <origin-page-url> <file-url> <outfile>
// Visits an origin page in headless Chromium (to pass bot checks), then downloads a file with the same cookies.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [origin, url, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36' });
  const page = await ctx.newPage();
  await page.goto(origin, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(e => console.error('ERR', e.message));
  await page.waitForTimeout(3000);
  const r = await ctx.request.get(url, { timeout: 60000 });
  console.error('STATUS', r.status(), r.headers()['content-type']);
  fs.writeFileSync(out, await r.body());
  await browser.close();
})();
