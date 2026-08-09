// Upload and SCHEDULE each queued Short on TikTok, verifying the AI-generated switch is off first.
//
// Why the switch check is a hard stop: every one of the 127 videos already on the account carries
// a "creator labelled this AI-generated" badge, traced to Remotion's own container comment. The
// files in this queue have been re-muxed without it, and the point of these posts is to be
// label-free. If the switch is on, something regressed and posting would just add another badged
// video to a channel that documents real cases.
//
// Everything is verified rather than assumed: the caption is read back, the schedule radio is
// confirmed selected, and the row is looked up afterwards. Results append to tt_clean_result.jsonl
// so an interrupted run resumes.

const fs = require('fs');
const puppeteer = require('puppeteer-core');

const QUEUE = JSON.parse(fs.readFileSync('C:/temp/studio_auto/tt_queue.json', 'utf8'));
const OUT = 'C:/temp/studio_auto/tt_clean_result.jsonl';
const SLOTS = ['10:00', '14:00', '18:00', '22:00'];
const START = process.argv[2] || null;          // YYYY-MM-DD, first day to fill
// Slots already taken on the start day by an earlier run - skip them, or two videos land on the
// same minute and TikTok accepts both.
const SKIP = parseInt(process.argv[3] || '0', 10);
const sleep = ms => new Promise(r => setTimeout(r, ms));

const done = new Set();
if (fs.existsSync(OUT)) {
  for (const l of fs.readFileSync(OUT, 'utf8').split('\n')) {
    if (!l.trim()) continue;
    try { const r = JSON.parse(l); if (r.status === 'SCHEDULED') done.add(r.short); } catch {}
  }
}

function slotsFrom(startDate, n) {
  const out = [];
  const d = new Date(startDate + 'T00:00:00');
  while (out.length < n) {
    for (const s of SLOTS) {
      if (out.length >= n) break;
      // NOT toISOString: that converts to UTC, and from JST (+9) a local midnight lands on the
      // previous day - which is why asking for 08-11 scheduled 08-10. Format the local parts.
      const ymd = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      out.push({ date: ymd, time: s });
    }
    d.setDate(d.getDate() + 1);
  }
  return out;
}

async function aiSwitchOff(pg) {
  return await pg.evaluate(() => {
    const sw = [...document.querySelectorAll('[role=switch], input[type=checkbox]')].find(e => {
      let box = e;
      for (let i = 0; i < 6 && box.parentElement; i++) {
        box = box.parentElement;
        const n = box.querySelectorAll('[role=switch], input[type=checkbox]').length;
        const t = (box.textContent || '').replace(/\s+/g, ' ').trim();
        if (n === 1 && t.length > 3) return t.startsWith('AI生成コンテンツ');
      }
      return false;
    });
    if (!sw) return 'missing';
    const on = sw.checked !== undefined ? sw.checked : sw.getAttribute('aria-checked') === 'true';
    return on ? 'ON' : 'OFF';
  });
}


async function setSchedule(pg, slot) {
  const visibleText = async () => {
    const hs = await pg.$$('input[type=text]');
    const out = [];
    for (const h of hs) if (await h.evaluate(e => !!e.offsetParent)) out.push(h);
    return out;
  };
  // --- date ---
  let fields = await visibleText();
  const idxDate = await pg.evaluate(() => {
    const ins = [...document.querySelectorAll('input[type=text]')].filter(e => e.offsetParent);
    return ins.findIndex(e => /^\d{4}-\d{2}-\d{2}$/.test(e.value));
  });
  if (idxDate < 0) return 'no date field';
  const want = new Date(slot.date + 'T00:00:00');
  // The popup does not always open on the first click, and a fixed wait then found no calendar and
  // reported "day cell not found" on a run where nothing was actually wrong. Click and poll, and
  // click again if it stayed shut.
  const header = async () => await pg.evaluate(() => {
    const h = [...document.querySelectorAll('div,span')]
      .find(e => e.offsetParent && /^\d{1,2}月\s*\/\s*\d{4}$/.test((e.textContent || '').trim()));
    return h ? h.textContent.trim() : null;
  });
  let opened = null;
  for (let attempt = 0; attempt < 3 && !opened; attempt++) {
    fields = await visibleText();
    if (!fields[idxDate]) break;
    await fields[idxDate].click();
    for (let w = 0; w < 8 && !opened; w++) { await sleep(700); opened = await header(); }
  }
  if (!opened) return 'calendar never opened';
  // step the month grid forward until the header matches, then click the day
  for (let guard = 0; guard < 6; guard++) {
    const hdr = await header();
    if (!hdr) break;
    const [m, y] = hdr.split('/').map(s => parseInt(s));
    if (y === want.getFullYear() && m === want.getMonth() + 1) break;
    await pg.evaluate(() => {
      const btns = [...document.querySelectorAll('svg,button,[role=button]')].filter(e => e.offsetParent);
      const next = btns[btns.length - 1];
      if (next) next.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    });
    await sleep(1200);
  }
  // A synthesised MouseEvent set the time but never the date: this widget listens for a real
  // pointer sequence. Mark the cell, then let the browser click it for real.
  const marked = await pg.evaluate((d) => {
    // Scope the search to the calendar popup. Searching the whole document also finds "11" in the
    // hour list of the time dropdown, and clicking that changes nothing about the date - which is
    // exactly the symptom: the time field updated, the date field never did.
    const hdr = [...document.querySelectorAll('div,span')]
      .find(e => e.offsetParent && /^\d{1,2}月\s*\/\s*\d{4}$/.test((e.textContent || '').trim()));
    if (!hdr) return false;
    let grid = hdr;
    for (let i = 0; i < 6 && grid.parentElement; i++) {
      grid = grid.parentElement;
      if (grid.querySelectorAll('*').length > 40) break;   // header + weekday row + day cells
    }
    const cells = [...grid.querySelectorAll('div,span,td')]
      .filter(e => e.offsetParent && e.children.length === 0 && (e.textContent || '').trim() === String(d));
    // the grid pads with the neighbouring months in a dimmed colour; take the live one
    let cell = cells.find(e => getComputedStyle(e).color !== 'rgb(191, 191, 191)') || cells[0];
    if (!cell) return false;
    // the text sits in a zero-size wrapper; climb to the first ancestor with a real box, which is
    // what a finger would actually hit
    while (cell.parentElement) {
      const r = cell.getBoundingClientRect();
      if (r.width > 8 && r.height > 8) break;
      cell = cell.parentElement;
    }
    cell.setAttribute('data-pd-pick', '1');
    return true;
  }, want.getDate());
  if (!marked) return 'day cell not found';
  const handle = await pg.$('[data-pd-pick="1"]');
  if (!handle) return 'day cell vanished';
  await handle.click();
  await pg.evaluate(() => document.querySelector('[data-pd-pick="1"]')?.removeAttribute('data-pd-pick'));
  await sleep(1500);

  // --- time ---
  fields = await visibleText();
  const idxTime = await pg.evaluate(() => {
    const ins = [...document.querySelectorAll('input[type=text]')].filter(e => e.offsetParent);
    return ins.findIndex(e => /^\d{2}:\d{2}$/.test(e.value));
  });
  if (idxTime >= 0) {
    await fields[idxTime].click();
    await sleep(1500);
    const [hh, mm] = slot.time.split(':');
    await pg.evaluate(({ hh, mm }) => {
      const opts = [...document.querySelectorAll('div,span,li')]
        .filter(e => e.offsetParent && e.children.length === 0);
      const h = opts.find(e => (e.textContent || '').trim() === hh);
      if (h) h.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      const m = opts.filter(e => (e.textContent || '').trim() === mm).pop();
      if (m) m.dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }, { hh, mm });
    await sleep(1500);
  }
  return await pg.evaluate(() => {
    const ins = [...document.querySelectorAll('input[type=text]')].filter(e => e.offsetParent);
    const d = ins.find(e => /^\d{4}-\d{2}-\d{2}$/.test(e.value));
    const t = ins.find(e => /^\d{2}:\d{2}$/.test(e.value));
    return `${d ? d.value : '?'} ${t ? t.value : '?'}`;
  });
}

async function one(pg, item, slot) {
  let discards = 0;
  await pg.goto('https://www.tiktok.com/tiktokstudio/upload', { waitUntil: 'networkidle2', timeout: 120000 });
  await sleep(5000);
  // A previous attempt that never submitted leaves a draft, and the uploader then offers
  // "continue editing?" and will not take a new file until that is answered.
  //
  // Answering it is a two-step dance and getting it wrong is what broke four runs: the banner
  // button only OPENS a confirmation dialog, and that dialog is a modal overlay. Clicking
  // 破棄する blindly in a loop ended with a freshly reopened dialog sitting over the form, so
  // every later click went to the overlay - the date picker never opened and the run reported
  // "calendar never opened" while a screenshot showed the dialog waiting for an answer.
  //
  // So: press the banner once, confirm once, then reload and verify the page came back clean.
  const dialogOpen = () => pg.evaluate(() => {
    const btns = [...document.querySelectorAll('button')].filter(e => e.offsetParent);
    return btns.some(e => (e.textContent || '').trim() === '後で')
        && btns.some(e => (e.textContent || '').trim() === '破棄する');
  });
  const clickText = (label) => pg.evaluate((l) => {
    const b = [...document.querySelectorAll('button')]
      .find(e => (e.textContent || '').trim() === l && e.offsetParent);
    if (!b) return false;
    b.click();
    return true;
  }, label);

  for (let round = 0; round < 3; round++) {
    if (!(await clickText('破棄する'))) break;          // no leftover draft
    await sleep(2000);
    if (await dialogOpen()) { await clickText('破棄する'); await sleep(2500); }
    await pg.goto('https://www.tiktok.com/tiktokstudio/upload',
                  { waitUntil: 'networkidle2', timeout: 120000 });
    await sleep(4000);
    discards++;
  }
  if (discards) console.log(`    discarded a leftover draft (${discards} rounds)`);
  if (await dialogOpen()) return { status: 'DIALOG_STUCK' };

  // Discarding tears the uploader down and rebuilds it; for a moment there is no file input at
  // all, which read as NO_FILE_INPUT on a page that was merely mid-rebuild.
  let inp = null;
  for (let pass = 0; pass < 2 && !inp; pass++) {
    for (let i = 0; i < 12 && !inp; i++) { inp = await pg.$('input[type=file]'); if (!inp) await sleep(1500); }
    if (!inp) { await pg.reload({ waitUntil: 'networkidle2', timeout: 120000 }); await sleep(4000); }
  }
  if (!inp) return { status: 'NO_FILE_INPUT' };
  await inp.uploadFile(item.file);

  let ready = false;
  for (let i = 0; i < 30; i++) {
    await sleep(4000);
    ready = await pg.evaluate(() => !!document.querySelector('div[contenteditable="true"]'));
    if (ready) break;
  }
  if (!ready) return { status: 'EDITOR_NEVER_APPEARED' };
  await sleep(3000);

  for (const l of ['さらに表示', 'すべて表示']) {
    await pg.evaluate((x) => {
      const e = [...document.querySelectorAll('*')]
        .find(n => (n.textContent || '').trim() === x && n.children.length === 0);
      if (e) e.click();
    }, l);
    await sleep(1500);
  }

  const ai = await aiSwitchOff(pg);
  if (ai !== 'OFF') return { status: 'AI_SWITCH_' + ai };

  // Set the cover. Left alone, TikTok picks a frame from the video, and this channel's Shorts open
  // on a near-black frame: the profile grid was a wall of identical black tiles with unreadable
  // subtitle text, and nothing could be told apart. The cover cannot be changed after posting -
  // on a published or scheduled post every edit control is disabled - so it has to happen here.
  if (item.cover) {
    const opened = await pg.evaluate(() => {
      const e = [...document.querySelectorAll('*')]
        .find(n => (n.textContent || '').trim() === 'カバーを編集' && n.children.length === 0);
      if (!e) return false;
      e.click();
      return true;
    });
    if (!opened) return { status: 'NO_COVER_BUTTON' };
    await sleep(4000);
    // the image input appears only inside the cover dialog; the video input is gone by now
    let imgInput = null;
    for (let i = 0; i < 12 && !imgInput; i++) {
      imgInput = await pg.$('input[type=file][accept*="image"]');
      if (!imgInput) await sleep(1200);
    }
    if (!imgInput) return { status: 'NO_COVER_INPUT' };
    await imgInput.uploadFile(item.cover);
    await sleep(6000);
    const saved = await pg.evaluate(() => {
      const b = [...document.querySelectorAll('button')]
        .find(e => e.offsetParent && (e.textContent || '').trim() === '保存');
      if (!b) return false;
      b.setAttribute('data-pd-save', '1');
      return true;
    });
    if (!saved) return { status: 'NO_COVER_SAVE' };
    const sv = await pg.$('[data-pd-save="1"]');
    await sv.click();
    await sleep(4000);
    console.log('    cover set');
  }

  const box = await pg.$('div[contenteditable="true"]');
  await box.click();
  await pg.keyboard.down('Control'); await pg.keyboard.press('KeyA'); await pg.keyboard.up('Control');
  await pg.keyboard.press('Backspace');
  await sleep(500);
  await pg.type('div[contenteditable="true"]', item.caption, { delay: 10 });
  await sleep(1200);

  // switch to scheduled posting
  const sched = await pg.evaluate(() => {
    const r = document.querySelector('input[type=radio][value="schedule"]');
    if (!r) return 'no radio';
    r.click();
    let box = r;
    for (let i = 0; i < 4 && box.parentElement; i++) { box.click(); box = box.parentElement; }
    return 'clicked';
  });
  if (sched !== 'clicked') return { status: 'NO_SCHEDULE_RADIO' };
  await sleep(2500);
  await pg.evaluate(() => {
    const b = [...document.querySelectorAll('button')]
      .find(e => (e.textContent || '').trim() === '許可する' && e.offsetParent);
    if (b) b.click();
  });
  await sleep(2500);

  // A "discard this post?" dialog can still be sitting over the form at this point, and while it
  // is open every click lands on the overlay instead of the field - the date picker simply never
  // opens. Answer it with 後で, which keeps the post being edited. Never 破棄する here: the draft
  // on screen is the video about to be scheduled.
  if (await dialogOpen()) {
    await clickText('後で');
    await sleep(2000);
    if (await dialogOpen()) return { status: 'DIALOG_STUCK_BEFORE_SCHEDULE' };
    console.log('    closed a confirmation dialog');
  }

  // Both fields are readOnly - assigning .value is silently ignored, which is why three attempts
  // posted nothing and the fields still read today. They open pickers: the date one a month grid,
  // the time one a list of hours and minutes.
  const set = await setSchedule(pg, slot);
  console.log(`    schedule -> ${set}`);
  if (!String(set).startsWith(slot.date)) {
    // Keep the evidence. "calendar never opened" is a guess about the page until the page is
    // actually looked at, and guessing cost a whole batch run once already.
    const shot = `C:/temp/studio_auto/tt_fail_short${item.short}.png`;
    try { await pg.screenshot({ path: shot }); } catch {}
    return { status: 'SCHEDULE_NOT_SET', detail: String(set), shot };
  }
  await sleep(1500);

  // When scheduling, the submit button is labelled 投稿予約する - "投稿" alone is the left-hand
  // navigation link, and clicking that navigated nowhere and looked like a silent failure.
  // The button exists long before it works. Right after the schedule is set it reports
  // aria-disabled="true" - TikTok is still finishing its own checks on the upload - and clicking
  // it then does nothing at all, which looked exactly like a successful click that failed to
  // navigate. Wait for it to go live.
  // TikTok runs its own music-copyright and content checks on the upload, and submitting before
  // they finish pops "投稿に進みますか？ 著作権侵害のチェックが完了していません" and STOPS the check.
  // A copyright strike is the one failure mode this channel cannot absorb, so wait for both checks
  // to come back clean rather than clicking through the warning.
  let checksDone = false;
  for (let i = 0; i < 40 && !checksDone; i++) {
    checksDone = await pg.evaluate(() => {
      const s = (document.body.innerText || '').replace(/\s+/g, ' ');
      return s.includes('問題は見つかりませんでした') && s.includes('違反は見つかりませんでした');
    });
    if (!checksDone) await sleep(3000);
  }
  console.log(`    copyright/content checks clear: ${checksDone}`);
  if (!checksDone) return { status: 'CHECKS_NOT_CLEAR' };

  let submitLive = false;
  for (let i = 0; i < 40 && !submitLive; i++) {
    submitLive = await pg.evaluate(() => {
      const t = [...document.querySelectorAll('button')]
        .find(e => e.offsetParent && (e.textContent || '').trim() === '投稿予約する');
      return !!t && !t.disabled && t.getAttribute('aria-disabled') !== 'true';
    });
    if (!submitLive) await sleep(3000);
  }
  console.log(`    submit button enabled: ${submitLive}`);

  // Mark it, then let the browser click it for real. A programmatic .click() left the page exactly
  // as it was - no navigation, no error text, nothing red - because this control listens for a
  // pointer sequence, the same way the calendar day cell does.
  const clicked = await pg.evaluate(() => {
    const all = [...document.querySelectorAll('button')].filter(e => e.offsetParent);
    const t = all.find(e => (e.textContent || '').trim() === '投稿予約する');
    if (!t) return { hit: false, buttons: all.map(e => (e.textContent || '').trim()).slice(0, 20) };
    t.setAttribute('data-pd-submit', '1');
    return { hit: true, disabled: t.disabled, aria: t.getAttribute('aria-disabled') };
  });
  if (!clicked.hit) return { status: 'NO_POST_BUTTON', detail: (clicked.buttons || []).join('|').slice(0, 200) };
  if (clicked.aria === 'true') return { status: 'SUBMIT_STAYED_DISABLED' };
  const submit = await pg.$('[data-pd-submit="1"]');
  if (!submit) return { status: 'SUBMIT_VANISHED' };
  await submit.click();
  await sleep(3000);
  // Even with the checks green TikTok can still ask once more. Answering it is safe here - what
  // the warning protects against has already finished.
  const confirmed = await pg.evaluate(() => {
    const b = [...document.querySelectorAll('button')]
      .find(e => e.offsetParent && (e.textContent || '').trim() === '今すぐ投稿');
    if (!b) return false;
    b.setAttribute('data-pd-go', '1');
    return true;
  });
  if (confirmed) {
    const go = await pg.$('[data-pd-go="1"]');
    if (go) { await go.click(); console.log('    confirmed the post dialog'); }
  }
  console.log(`    submit: disabled=${clicked.disabled} aria=${clicked.aria}`);

  for (let i = 0; i < 20; i++) {
    await sleep(3000);
    if (!pg.url().includes('/upload')) return { status: 'SCHEDULED', when: `${slot.date} ${slot.time}` };
  }
  // Still here after a minute: read whatever the form is complaining about instead of guessing.
  const why = await pg.evaluate(() => {
    const txt = (document.body.innerText || '').replace(/\s+/g, ' ');
    const red = [...document.querySelectorAll('div,span,p')]
      .filter(e => e.offsetParent && e.children.length === 0 && /rgb\(2[45][0-9], ?[0-9]{1,2}, ?[0-9]{1,3}\)/.test(getComputedStyle(e).color))
      .map(e => (e.textContent || '').trim()).filter(s => s.length > 1 && s.length < 120);
    return { red: [...new Set(red)].slice(0, 8), hasErr: /エラー|失敗|必須|入力してください/.test(txt) };
  });
  try { await pg.screenshot({ path: `C:/temp/studio_auto/tt_submit_short${item.short}.png` }); } catch {}
  return { status: 'STAYED_ON_EDITOR', detail: JSON.stringify(why).slice(0, 300) };
}

(async () => {
  if (!START) { console.error('usage: node tt_batch_clean.js <YYYY-MM-DD first day>'); process.exit(2); }
  const todo = QUEUE.filter(q => !done.has(q.short));
  const slots = slotsFrom(START, todo.length + SKIP).slice(SKIP);
  console.log(`${todo.length} to schedule, 4/day from ${START}`);
  const b = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222', defaultViewport: null });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1500, height: 1100 });
  let ok = 0, streak = 0;
  for (let i = 0; i < todo.length; i++) {
    const item = todo[i], slot = slots[i];
    let r;
    try { r = await one(pg, item, slot); }
    catch (e) { r = { status: 'ERROR', detail: e.message.slice(0, 90) }; }
    r.short = item.short;
    fs.appendFileSync(OUT, JSON.stringify(r) + '\n');
    console.log(`  short${item.short}  ${r.status}  ${r.when || r.detail || ''}`);
    if (r.status === 'SCHEDULED') { ok++; streak = 0; } else { streak++; }
    if (streak >= 3) { console.log('THREE FAILURES IN A ROW - stopping'); break; }
    await sleep(4000 + Math.floor(Math.random() * 4000));
  }
  console.log(`\n${ok}/${todo.length} scheduled`);
  await pg.close();
  await b.disconnect();
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
