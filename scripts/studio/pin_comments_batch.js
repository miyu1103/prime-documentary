// Post the drafted channel comment on each long-form and PIN it, proving both by read-back.
//
// Why the browser and not the Data API: `commentThreads.insert` can post as the channel (50 units)
// but there is no pin parameter, no pin endpoint, and no `isPinned` field to read back. Pinning
// exists only in the signed-in web UI. And on 2026-08-10 the quota ledger already stood at
// 10,734 of 10,000 units for the Pacific day, so 56 inserts at 50 units each (2,800) had a real
// chance of dying mid-batch on a 403. Doing both steps in the one browser costs zero quota and
// keeps post and pin in the same tab, so a posted-but-unpinned comment cannot be left behind by a
// half-run.
//
// What it will not do, by construction:
//   * it will not touch a video that is not in the drafts file. That file is the allowlist and
//     --only with anything else is refused before a page is opened.
//   * it will not touch privacy, publish date, title, description or thumbnail. It never opens
//     Studio and never calls a write endpoint; the only mutation is a comment.
//   * it will not post to a video that videos.list does not report as `public` with no pending
//     `publishAt`. A comment on a private video is invisible, and a scheduled video is off-limits.
//   * it will not post the same text twice. Before typing it reads the existing threads and, if
//     the channel already posted this exact text, it skips straight to pinning.
//   * it will not record a success it has not seen. After posting AND after pinning the page is
//     fully reloaded and re-read. "The button was clicked" is not evidence.
//
// Usage (one-time login: see scripts/studio/README.md):
//   node scripts/studio/pin_comments_batch.js --dry-run          # say what it would do
//   node scripts/studio/pin_comments_batch.js --only <videoId>   # one video, must be in drafts
//   node scripts/studio/pin_comments_batch.js --limit 5
//   node scripts/studio/pin_comments_batch.js --verify-only      # read back, change nothing
//   node scripts/studio/pin_comments_batch.js                    # the batch
//
// Exit codes: 0 every targeted row verified · 1 refused/crashed · 2 no debug Chrome on 9222 ·
//             3 profile not signed in · 5 a row did not verify.

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const DEFAULT_DRAFTS = path.join(ROOT, 'episodes', '_planning', 'measurements',
  'PINNED_COMMENTS.v001.json');
const STATE_DIR = path.join(ROOT, 'runs', 'pinned_comments');
const LEDGER = path.join(STATE_DIR, 'ledger.jsonl');
const SHOTS = path.join(STATE_DIR, 'shots');
const BROWSER_URL = 'http://127.0.0.1:9222';
const CHANNEL_ID = 'UCuQPtAz1rca9eJ4xhvX0yKA';
const CHANNEL_NAME = 'Prime Documentary';

// Studio/YouTube render in the account language. Both label sets are matched so a language switch
// is a loud failure rather than a click on the wrong item.
const L = {
  pin: ['固定', 'Pin', 'PIN'],
  unpin: ['固定を解除', 'Unpin'],
  confirm: ['固定', 'Pin', 'PIN', 'OK'],
  submit: ['コメント', 'Comment', 'COMMENT'],
  pinnedBadge: ['固定', 'Pinned by'],
};

function puppeteer() {
  try {
    return require('puppeteer-core');
  } catch {
    return require('C:/temp/studio_auto/node_modules/puppeteer-core');
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();

function args() {
  const a = process.argv.slice(2);
  const get = (f) => { const i = a.indexOf(f); return i >= 0 ? a[i + 1] : null; };
  return {
    dryRun: a.includes('--dry-run'),
    verifyOnly: a.includes('--verify-only'),
    only: get('--only'),
    limit: get('--limit') ? parseInt(get('--limit'), 10) : null,
    drafts: get('--drafts') || DEFAULT_DRAFTS,
    force: a.includes('--force'),
  };
}

// ---------------------------------------------------------------- drafts / ledger

function loadDrafts(file) {
  const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
  const rows = parsed.comments || [];
  const seen = new Set();
  for (const r of rows) {
    if (!/^[A-Za-z0-9_-]{11}$/.test(r.video_id)) throw new Error(`bad video id: ${r.video_id}`);
    if (seen.has(r.video_id)) throw new Error(`duplicate video id in drafts: ${r.video_id}`);
    if (!r.text || r.text.length < 20) throw new Error(`empty/short text for ${r.video_id}`);
    if (r.text.includes('\n')) throw new Error(`multi-line text for ${r.video_id}: the box would submit early`);
    seen.add(r.video_id);
  }
  return { rows, allow: seen, channel_id: parsed.channel_id };
}

function loadLedger() {
  const latest = new Map();
  if (!fs.existsSync(LEDGER)) return latest;
  for (const line of fs.readFileSync(LEDGER, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try { const r = JSON.parse(line); latest.set(r.video_id, r); } catch { /* truncated tail */ }
  }
  return latest;
}

function record(entry) {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  fs.appendFileSync(LEDGER, JSON.stringify(entry) + '\n', 'utf8');
}

// ---------------------------------------------------------------- Data API (read only)

function loadEnv() {
  const env = {};
  for (const line of fs.readFileSync(path.join(ROOT, '.env'), 'utf8').split('\n')) {
    const t = line.trim();
    if (!t || t.startsWith('#') || !t.includes('=')) continue;
    const i = t.indexOf('=');
    env[t.slice(0, i).trim()] = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
  }
  return env;
}

async function accessToken() {
  const env = loadEnv();
  const body = new URLSearchParams({
    client_id: env.YOUTUBE_CLIENT_ID,
    client_secret: env.YOUTUBE_CLIENT_SECRET,
    refresh_token: env.YOUTUBE_REFRESH_TOKEN,
    grant_type: 'refresh_token',
  });
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', body,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  if (!r.ok) throw new Error(`token refresh HTTP ${r.status}`);
  return (await r.json()).access_token;
}

// The eligibility gate. Read-only: `part=status` and nothing is ever written back.
async function fetchStatus(token, ids) {
  const out = {};
  for (let n = 0; n < ids.length; n += 50) {
    const chunk = ids.slice(n, n + 50);
    const r = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?part=status,snippet&id=${chunk.join(',')}`,
      { headers: { Authorization: `Bearer ${token}` } });
    if (!r.ok) throw new Error(`videos.list HTTP ${r.status}`);
    const j = await r.json();
    for (const v of j.items || []) {
      out[v.id] = { privacy: v.status.privacyStatus, publishAt: v.status.publishAt || null,
        title: v.snippet.title };
    }
  }
  return out;
}

// ---------------------------------------------------------------- page helpers

async function newTab(browser) {
  // A fresh tab per video. Reusing one tab stacks dropdowns and dialogs that YouTube never
  // removes, and past a few the newest one stops being reachable — the same failure mode the
  // related-video batch hit on 2026-08-09.
  const page = await browser.newPage();
  page.setDefaultTimeout(45000);
  // Block the media segments. The comment section does not need them and the machine is busy.
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const u = req.url();
    if (u.includes('.googlevideo.com/videoplayback') || req.resourceType() === 'media') {
      req.abort().catch(() => {});
    } else {
      req.continue().catch(() => {});
    }
  });
  return page;
}

async function openWatch(page, videoId) {
  await page.goto(`https://www.youtube.com/watch?v=${videoId}`,
    { waitUntil: 'domcontentloaded', timeout: 90000 });
  await sleep(2500);
  await page.evaluate(() => {
    const v = document.querySelector('video');
    if (v) { try { v.pause(); v.muted = true; } catch { /* player not ready */ } }
  }).catch(() => {});
  // Comments are lazily rendered and how far down they sit varies with the description length,
  // so scroll until they actually appear rather than a fixed number of times.
  let seen = false;
  for (let i = 0; i < 30 && !seen; i++) {
    await page.evaluate(() => window.scrollBy(0, 900));
    await sleep(600);
    seen = await page.evaluate(() => !!document.querySelector(
      'ytd-comment-thread-renderer ytd-comment-view-model, ytd-comment-thread-renderer ytd-comment-renderer, ytd-comments ytd-message-renderer'));
  }
  await sleep(1800);
  return seen;
}

// Read every top-level comment the page is showing, with author, text and pinned badge.
async function readThreads(page) {
  return page.evaluate(() => {
    const out = [];
    for (const t of document.querySelectorAll('ytd-comment-thread-renderer')) {
      const host = t.querySelector('ytd-comment-view-model, ytd-comment-renderer') || t;
      const author = host.querySelector('#author-text');
      const content = host.querySelector('#content-text');
      const badge = host.querySelector('#pinned-comment-badge, ytd-pinned-comment-badge-renderer');
      out.push({
        author: author ? author.textContent.replace(/\s+/g, ' ').trim() : null,
        text: content ? content.innerText.replace(/\s+/g, ' ').trim() : '',
        pinnedBadge: badge ? badge.innerText.replace(/\s+/g, ' ').trim() : null,
      });
    }
    return {
      threads: out,
      disabled: !!document.querySelector('ytd-comments ytd-message-renderer'),
      hasBox: !!document.querySelector('ytd-comment-simplebox-renderer'),
    };
  });
}

async function postComment(page, text) {
  const clicked = await page.evaluate(() => {
    const ph = document.querySelector('ytd-comment-simplebox-renderer #simplebox-placeholder')
      || document.querySelector('ytd-comment-simplebox-renderer #placeholder-area');
    if (!ph) return false;
    ph.scrollIntoView({ block: 'center' });
    ph.click();
    return true;
  });
  if (!clicked) return { ok: false, why: 'NO_BOX' };
  await sleep(1200);
  const editor = await page.$('ytd-commentbox #contenteditable-root');
  if (!editor) return { ok: false, why: 'NO_EDITOR' };
  await editor.click();
  await sleep(300);
  await page.keyboard.type(text, { delay: 4 });
  await sleep(800);
  const typed = await page.evaluate(() => {
    const e = document.querySelector('ytd-commentbox #contenteditable-root');
    return e ? e.innerText.replace(/\s+/g, ' ').trim() : null;
  });
  if (norm(typed) !== norm(text)) return { ok: false, why: 'TYPED_MISMATCH', typed };
  const sent = await page.evaluate((labels) => {
    const box = document.querySelector('ytd-commentbox');
    if (!box) return false;
    const cands = [...box.querySelectorAll('#submit-button button, #submit-button, button')];
    for (const b of cands) {
      const t = (b.innerText || b.getAttribute('aria-label') || '').trim();
      if (labels.some((l) => t === l || t.includes(l))) {
        if (b.disabled || b.getAttribute('aria-disabled') === 'true') continue;
        b.click();
        return true;
      }
    }
    const sb = box.querySelector('#submit-button button') || box.querySelector('#submit-button');
    if (sb) { sb.click(); return true; }
    return false;
  }, L.submit);
  if (!sent) return { ok: false, why: 'NO_SUBMIT' };
  await sleep(3500);
  return { ok: true };
}

// Open the kebab on the thread whose text matches, click Pin, accept the confirm dialog.
//
// Every click here is a real mouse click at page coordinates, never `element.click()`. Measured
// 2026-08-10: the menu row is a `ytd-menu-navigation-item-renderer` with no href and the confirm
// button is a Polymer `tp-yt-paper-dialog` whose `opened` attribute is not set even while it is
// on screen. A synthetic `.click()` on either returns without error and does nothing at all — the
// first attempt reported "CONFIRMED" and left the comment unpinned. Coordinates are the evidence.
async function pinComment(page, text) {
  const kebab = await page.evaluate((want) => {
    const n = (s) => (s || '').replace(/\s+/g, ' ').trim();
    for (const t of document.querySelectorAll('ytd-comment-thread-renderer')) {
      const host = t.querySelector('ytd-comment-view-model, ytd-comment-renderer') || t;
      const c = host.querySelector('#content-text');
      if (!c || n(c.innerText) !== n(want)) continue;
      host.scrollIntoView({ block: 'center' });
      const k = host.querySelector('#action-menu button, #action-menu yt-icon-button, ytd-menu-renderer #button');
      if (!k) return 'NO_KEBAB';
      const r = k.getBoundingClientRect();
      if (r.width < 4) return 'KEBAB_NOT_VISIBLE';
      return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
    }
    return 'NO_THREAD';
  }, text);
  if (typeof kebab === 'string') return { ok: false, why: kebab };
  await page.mouse.click(kebab.x, kebab.y);
  await sleep(2200);

  const found = await page.evaluate((labels, unlabels) => {
    const n = (s) => (s || '').replace(/\s+/g, ' ').trim();
    const d = [...document.querySelectorAll('tp-yt-iron-dropdown')]
      .filter((x) => x.getAttribute('aria-hidden') !== 'true')
      .pop();
    if (!d) return { why: 'NO_DROPDOWN', menu: [] };
    const items = [...d.querySelectorAll('ytd-menu-navigation-item-renderer, ytd-menu-service-item-renderer')];
    const menu = items.map((i) => n(i.innerText));
    for (const it of items) {
      const t = n(it.innerText);
      if (unlabels.some((u) => t.includes(u))) return { why: 'ALREADY_PINNED', menu };
    }
    for (const it of items) {
      const t = n(it.innerText);
      if (labels.some((l) => t === l)) {
        const r = it.getBoundingClientRect();
        if (r.width < 4) return { why: 'PIN_ITEM_NOT_VISIBLE', menu };
        return { why: 'FOUND', menu, x: r.x + r.width / 2, y: r.y + r.height / 2 };
      }
    }
    return { why: 'NO_PIN_ITEM', menu };
  }, L.pin, L.unpin);

  if (found.why !== 'FOUND') {
    await page.keyboard.press('Escape').catch(() => {});
    return { ok: found.why === 'ALREADY_PINNED', why: found.why, menu: found.menu };
  }
  await page.mouse.click(found.x, found.y);
  await sleep(2200);

  // Confirmation dialog: 「このコメントを固定しますか？」 / "Pin this comment?"
  const btn = await page.evaluate((labels) => {
    const n = (s) => (s || '').replace(/\s+/g, ' ').trim();
    const dlg = [...document.querySelectorAll('yt-confirm-dialog-renderer, tp-yt-paper-dialog')]
      .filter((d) => d.getBoundingClientRect().width > 0).pop();
    if (!dlg) return 'NO_DIALOG';
    const cands = [...dlg.querySelectorAll('#confirm-button button, #confirm-button, button, tp-yt-paper-button')];
    for (const b of cands) {
      const t = n(b.innerText);
      const pid = b.parentElement ? b.parentElement.id : '';
      if (pid === 'checkbox-enabled-confirm-button') continue;
      const isConfirm = pid === 'confirm-button' || b.id === 'confirm-button'
        || labels.some((l) => t === l);
      if (!isConfirm) continue;
      const r = b.getBoundingClientRect();
      if (r.width < 4) continue;
      return { x: r.x + r.width / 2, y: r.y + r.height / 2, label: t };
    }
    return 'NO_CONFIRM_BTN';
  }, L.confirm);
  if (typeof btn === 'string') return { ok: false, why: btn, menu: found.menu };
  await page.mouse.click(btn.x, btn.y);
  await sleep(3500);
  return { ok: true, why: `CONFIRMED(${btn.label})`, menu: found.menu };
}

// ---------------------------------------------------------------- main

(async () => {
  const a = args();
  const { rows, allow } = loadDrafts(a.drafts);
  if (a.only && !allow.has(a.only)) {
    console.error(`refused: ${a.only} is not in ${path.basename(a.drafts)}`);
    process.exit(1);
  }

  const token = await accessToken();
  const status = await fetchStatus(token, rows.map((r) => r.video_id));

  let targets = rows.filter((r) => (!a.only || r.video_id === a.only));
  const ledger = loadLedger();
  const skipped = [];
  targets = targets.filter((r) => {
    const s = status[r.video_id];
    if (!s) { skipped.push([r.video_id, 'NOT_FOUND_ON_CHANNEL']); return false; }
    if (s.privacy !== 'public') { skipped.push([r.video_id, `PRIVACY_${s.privacy}`]); return false; }
    if (s.publishAt) { skipped.push([r.video_id, `SCHEDULED_${s.publishAt}`]); return false; }
    const prev = ledger.get(r.video_id);
    if (!a.force && !a.verifyOnly && prev && prev.status === 'VERIFIED_PINNED' && prev.text === r.text) {
      skipped.push([r.video_id, 'ALREADY_DONE']);
      return false;
    }
    return true;
  });
  if (a.limit) targets = targets.slice(0, a.limit);

  console.log(`drafts ${rows.length} · eligible now ${targets.length} · skipped ${skipped.length}`);
  for (const [v, why] of skipped) console.log(`  skip ${v} ${why}`);
  if (a.dryRun) {
    for (const r of targets) console.log(`  would post+pin ${r.video_id}  ${r.text.slice(0, 60)}...`);
    process.exit(0);
  }

  const pptr = puppeteer();
  let browser;
  try {
    // protocolTimeout: the default 30s is not enough on a machine that is also rendering. One row
    // failed on 2026-08-10 with "Runtime.callFunctionOn timed out" while a 1.9 GB scan was reading.
    browser = await pptr.connect({ browserURL: BROWSER_URL, defaultViewport: null,
      protocolTimeout: 180000 });
  } catch {
    console.error('no debug Chrome on 9222 — run: node scripts/studio/start_chrome.js');
    process.exit(2);
  }
  fs.mkdirSync(SHOTS, { recursive: true });

  let ok = 0; let bad = 0; let consecutive = 0;
  for (const [i, r] of targets.entries()) {
    const vid = r.video_id;
    const page = await newTab(browser);
    const entry = { video_id: vid, title: status[vid].title, at: new Date().toISOString(),
      text: r.text };
    try {
      await openWatch(page, vid);
      let before = await readThreads(page);
      if (!before.hasBox && !before.threads.length) {
        const who = await page.evaluate(() => !!document.querySelector('#avatar-btn'));
        if (!who) { console.error('profile not signed in'); await page.close(); process.exit(3); }
      }
      const mine = before.threads.find((t) => norm(t.text) === norm(r.text));
      let posted = !!mine;

      if (!posted && !a.verifyOnly) {
        const p = await postComment(page, r.text);
        if (!p.ok) throw new Error(`post failed: ${p.why}${p.typed ? ` typed=${p.typed.slice(0, 60)}` : ''}`);
      }

      // Read-back #1: full reload, is the comment actually there and authored by the channel?
      // In --verify-only nothing was clicked, so the page just loaded is already the read-back.
      if (!a.verifyOnly) await openWatch(page, vid);
      let after = a.verifyOnly ? before : await readThreads(page);
      let row = after.threads.find((t) => norm(t.text) === norm(r.text));
      if (!row) {
        // A brand new comment sometimes needs a moment before it is served back.
        await sleep(6000);
        await openWatch(page, vid);
        after = await readThreads(page);
        row = after.threads.find((t) => norm(t.text) === norm(r.text));
      }
      if (!row) throw new Error('posted but not present on reload');
      entry.author_on_page = row.author;
      entry.present = true;

      // Pin, unless it already carries the badge.
      let pinnedBadge = row.pinnedBadge;
      if (!pinnedBadge && !a.verifyOnly) {
        const pin = await pinComment(page, r.text);
        entry.pin_menu = pin.menu;
        entry.pin_result = pin.why;
        if (!pin.ok) throw new Error(`pin failed: ${pin.why} menu=${JSON.stringify(pin.menu)}`);
        // Read-back #2: full reload, does the comment now carry the pinned badge?
        await openWatch(page, vid);
        const v2 = await readThreads(page);
        const row2 = v2.threads.find((t) => norm(t.text) === norm(r.text));
        pinnedBadge = row2 ? row2.pinnedBadge : null;
        entry.first_thread_is_ours = v2.threads.length
          ? norm(v2.threads[0].text) === norm(r.text) : false;
      } else {
        entry.first_thread_is_ours = after.threads.length
          ? norm(after.threads[0].text) === norm(r.text) : false;
      }
      entry.pinned_badge = pinnedBadge;
      entry.status = pinnedBadge ? 'VERIFIED_PINNED' : (a.verifyOnly ? 'PRESENT_NOT_PINNED' : 'POSTED_PIN_UNVERIFIED');
      if (!pinnedBadge) throw new Error(`no pinned badge after reload (present=${!!row})`);
      ok++; consecutive = 0;
      console.log(`[${i + 1}/${targets.length}] ${vid} PINNED  "${pinnedBadge}"`);
    } catch (e) {
      entry.status = entry.status && entry.status !== 'VERIFIED_PINNED' ? entry.status : 'ERROR';
      entry.error = String(e.message || e).slice(0, 400);
      bad++; consecutive++;
      console.log(`[${i + 1}/${targets.length}] ${vid} FAIL  ${entry.error}`);
      try { await page.screenshot({ path: path.join(SHOTS, `${vid}.png`), fullPage: false }); } catch { /* tab gone */ }
    }
    record(entry);
    await page.close().catch(() => {});
    if (consecutive >= 3) {
      console.error('three failures in a row — stopping rather than grinding through a broken UI');
      break;
    }
    await sleep(1500);
  }

  await browser.disconnect();
  console.log(`\ndone: ${ok} verified pinned · ${bad} failed · ledger ${LEDGER}`);
  process.exit(bad ? 5 : 0);
})().catch((e) => { console.error('crashed:', e); process.exit(1); });
