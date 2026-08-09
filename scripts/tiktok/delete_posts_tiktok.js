// Delete posts from TikTok Studio by caption match, or every post with --all.
//
// Why deletion is the only route: a cover cannot be changed after a post exists. On a scheduled or
// published post every edit control in the Studio list is rendered with cursor:not-allowed - the
// pencil, the cover icon and the comment icon are all dead. The cover has to be set during upload,
// so a post that went up without one has to be replaced.
//
// Refuses to touch anything with views unless --force, so a video that actually found an audience
// is never thrown away for a cosmetic fix.

const fs = require('fs');
const puppeteer = require('puppeteer-core');

const args = process.argv.slice(2);
const ALL = args.includes('--all');
const SCHEDULED_ONLY = args.includes('--scheduled');
const FORCE = args.includes('--force');
const MATCH = args.filter(a => !a.startsWith('--'));
const LOG = 'C:/temp/studio_auto/tt_deleted.jsonl';
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  if (!ALL && !SCHEDULED_ONLY && !MATCH.length) {
    console.error('usage: node tt_delete.js "<caption substring>" [...]   |   node tt_delete.js --all');
    process.exit(2);
  }
  const b = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222', defaultViewport: null });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1500, height: 1200 });

  let deleted = 0;
  let guard = 0;
  while (guard++ < 400) {
    await pg.goto('https://www.tiktok.com/tiktokstudio/content', { waitUntil: 'networkidle2', timeout: 120000 });
    await sleep(9000);

    const target = await pg.evaluate(({ all, match, force, schedOnly }) => {
      const rows = [...document.querySelectorAll('div.css-153feq8')];
      for (const row of rows) {
        const txt = (row.textContent || '').replace(/\s+/g, ' ').trim();
        // a scheduled row carries its publish date as a chip; a published one does not
        const scheduled = /\d+月\d+日\s*午[前後]/.test(txt);
        if (schedOnly && !scheduled) continue;
        if (!all && !match.some(m => txt.includes(m))) continue;
        // views sit in their own cell; a post with an audience is not disposable
        const cells = [...row.children].map(c => (c.textContent || '').trim());
        const views = parseInt((cells.find(c => /^\d[\d,]*$/.test(c)) || '0').replace(/,/g, ''), 10);
        if (!force && views > 0) continue;
        const rr = row.getBoundingClientRect();
        const icons = [...document.querySelectorAll('div.edss2sz8')].filter(e => {
          const r = e.getBoundingClientRect();
          return r.y >= rr.y && r.y < rr.y + rr.height && r.x > 1200;
        });
        const last = icons[icons.length - 1];
        if (!last) continue;
        const r = last.getBoundingClientRect();
        return { x: Math.round(r.x + r.width / 2), y: Math.round(r.y + r.height / 2), txt: txt.slice(0, 70), views };
      }
      return null;
    }, { all: ALL, match: MATCH, force: FORCE, schedOnly: SCHEDULED_ONLY });

    if (!target) { console.log('nothing left to delete'); break; }

    await pg.mouse.click(target.x, target.y);
    await sleep(2500);
    const opened = await pg.evaluate(() => {
      const e = [...document.querySelectorAll('div,li,span,button')]
        .find(n => n.offsetParent && n.children.length === 0 && (n.textContent || '').trim() === '削除');
      if (!e) return false;
      e.click();
      return true;
    });
    if (!opened) { console.log('no 削除 in the row menu; stopping'); break; }
    await sleep(2500);
    // confirm dialog
    const confirmed = await pg.evaluate(() => {
      const b = [...document.querySelectorAll('button')]
        .filter(e => e.offsetParent).find(e => /削除|Delete/.test((e.textContent || '').trim()));
      if (!b) return false;
      b.setAttribute('data-pd-del', '1');
      return true;
    });
    if (confirmed) {
      const h = await pg.$('[data-pd-del="1"]');
      if (h) await h.click();
    }
    await sleep(4000);
    deleted++;
    fs.appendFileSync(LOG, JSON.stringify({ txt: target.txt, views: target.views, at: new Date().toISOString() }) + '\n');
    console.log(`  deleted (${target.views} views): ${target.txt}`);
  }
  console.log(`\n${deleted} deleted`);
  await pg.close();
  await b.disconnect();
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
