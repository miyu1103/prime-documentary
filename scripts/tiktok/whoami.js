// Print the handle TikTok Studio is actually operating, and nothing else.
//
// This exists because on 2026-08-16 three videos were scheduled onto the wrong account. The same
// browser was signed into two: www.tiktok.com acted as prime.documentary1 (its profile could be
// edited and the bio saved), while TikTok Studio - the surface that uploads - was operating
// prime.documentary8. Checking the profile page proved nothing about where a post would land.
//
// Usage:  node scripts/tiktok/whoami.js          -> prints e.g. prime.documentary1
// Exit 1 if no handle can be read at all.
const puppeteer = require('puppeteer-core');
(async () => {
  const b = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
  const p = await b.newPage();
  await p.setViewport({ width: 1400, height: 900 });
  await p.goto('https://www.tiktok.com/tiktokstudio', { waitUntil: 'domcontentloaded', timeout: 120000 });
  await new Promise(r => setTimeout(r, 9000));
  // Not a regex over the whole HTML: the first "prime..." in the page is the YouTube handle
  // sitting inside the bio text, so that version read "primedocumentarystudio" and would have
  // refused a correct account. The handle is the line directly under the sidebar entry
  // "TikTokに戻る" in the Studio header block.
  const handle = await p.evaluate(() => {
    const lines = (document.body.innerText || '').split('\n').map(s => s.trim()).filter(Boolean);
    const i = lines.findIndex(l => l === 'TikTokに戻る' || l === 'Back to TikTok');
    return i >= 0 ? (lines[i + 1] || '') : '';
  });
  try { await p.close(); } catch (e) {}
  await b.disconnect();
  if (!handle) { console.error('could not read the Studio account handle'); process.exit(1); }
  console.log(handle);
})();
