// Usage: node tools/fetch_page.js <url> [outfile.html]
// Fetches a page with headless Chromium and waits out bot-check interstitials.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [url, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: process.env.HEADFUL ? false : true,
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', locale: 'en-NZ', viewport: { width: 1366, height: 900 } });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(e => console.error('ERR', e.message));
  for (let i = 0; i < 12; i++) { const t = await page.title(); if (!/just a moment|attention required/i.test(t)) break; await page.waitForTimeout(2500); }
  await page.waitForTimeout(1500);
  console.error('TITLE', await page.title(), 'URL', page.url());
  const html = await page.content();
  if (out) fs.writeFileSync(out, html); else process.stdout.write(html);
  await browser.close();
})();
