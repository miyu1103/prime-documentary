// Print the first line of every caption currently on the account, one per line.
//
// Used to reconcile the local ledger against TikTok itself before posting. On 2026-08-17 the same
// video was uploaded twice: a run died mid-upload, the ledger never recorded the first copy, and
// the retry put a second one on the account for the same slot. Duplicate posting is a spam signal,
// so the account - not the ledger - decides what has already gone out.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
  const p = await b.newPage();
  await p.setViewport({ width: 1500, height: 1000 });
  await p.goto('https://www.tiktok.com/tiktokstudio/content', { waitUntil: 'domcontentloaded', timeout: 120000 });
  await new Promise(r => setTimeout(r, 10000));
  for (let i = 0; i < 15; i++) {
    await p.evaluate(() => window.scrollBy(0, 2500));
    await new Promise(r => setTimeout(r, 700));
  }
  const lines = await p.evaluate(() => {
    const txt = (document.body.innerText || '').split('\n').map(s => s.trim()).filter(Boolean);
    const out = [];
    for (let i = 0; i < txt.length; i++) {
      if (/^\d{2}:\d{2}$/.test(txt[i]) && txt[i + 1]) out.push(txt[i + 1]);
    }
    return out;
  });
  try {
    const pages = await b.pages();
    if (pages.length > 1) await p.close();
  } catch (e) {}
  await b.disconnect();
  lines.forEach(l => console.log(l));
})();
