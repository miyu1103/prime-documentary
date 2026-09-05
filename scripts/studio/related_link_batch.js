// Set the "related video" on every Short in the worklist, and prove each one landed.
//
// Why this exists: the related video is the only official route YouTube gives a Short for sending
// a viewer to a long-form, and it exists ONLY in the Studio web UI. There is no Data API field and
// no Analytics API field for it. So it is set the way a human would set it, in a real signed-in
// Chrome, one video at a time.
//
// What it will not do, by construction:
//   * it will not touch a video that is not in the worklist. The worklist is the allowlist, and a
//     video id that is not in it is refused before any page is opened.
//   * it will not touch privacy, publish date, title or description. It reads all four from the
//     Data API before and after the run and fails the run if any of them moved. A past-dated
//     publishAt publishes immediately, so this guard is not decoration.
//   * it will not record a success it has not seen. Every save is followed by a full page reload
//     and a read-back of the control. "Save was clicked" is not evidence; the reloaded label is.
//   * it will not guess. If the picker shows no card matching the intended long-form, it closes
//     the dialog and records NO_MATCH.
//
// Resumability: every outcome is appended to runs/related_link/ledger.jsonl as it happens. A short
// whose most recent ledger entry is VERIFIED (or ALREADY_SET) for the same target is skipped on a
// re-run, so an interrupted batch resumes where it stopped.
//
// Usage (see scripts/studio/README.md for the one-time login):
//   node scripts/studio/related_link_batch.js --verify-only     # read-back only, changes nothing
//   node scripts/studio/related_link_batch.js --dry-run         # says what it would set
//   node scripts/studio/related_link_batch.js                   # sets what is missing
//   node scripts/studio/related_link_batch.js --only <shortId>  # one video, must be in worklist
//
// Exit codes: 0 all targeted rows verified · 2 no debug Chrome · 3 not signed in ·
//             4 metadata guard tripped · 5 one or more rows not verified.

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const DEFAULT_WORKLIST = path.join(ROOT, 'runs', '_cache', 'related_link_worklist.json');
const STATE_DIR = path.join(ROOT, 'runs', 'related_link');
const LEDGER = path.join(STATE_DIR, 'ledger.jsonl');
const GUARD = path.join(STATE_DIR, 'metadata_guard.json');
const SHOTS = path.join(STATE_DIR, 'shots');
const BROWSER_URL = 'http://127.0.0.1:9222';

// Studio renders in the account language. Both label sets are matched so a language switch is a
// visible failure rather than a silent one.
const L = {
  showAll: ['すべて表示', 'Show more', 'SHOW MORE'],
  save: ['保存', 'Save', 'SAVE'],
  searchPlaceholder: ['自分の動画', 'your videos', 'Search'],
  close: ['閉じる', 'Close', 'Cancel', 'キャンセル'],
};

function puppeteer() {
  try {
    return require('puppeteer-core');
  } catch {
    // The original one-off scripts installed the dependency outside the repo. Fall back to it so a
    // machine that has not run `npm install` in scripts/studio still works.
    return require('C:/temp/studio_auto/node_modules/puppeteer-core');
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const norm = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();

function args() {
  const a = process.argv.slice(2);
  const get = (flag) => {
    const i = a.indexOf(flag);
    return i >= 0 ? a[i + 1] : null;
  };
  return {
    verifyOnly: a.includes('--verify-only'),
    dryRun: a.includes('--dry-run'),
    only: get('--only'),
    limit: get('--limit') ? parseInt(get('--limit'), 10) : null,
    worklist: get('--worklist') || DEFAULT_WORKLIST,
  };
}

// ---------------------------------------------------------------- worklist / ledger

function loadWorklist(file) {
  const parsed = JSON.parse(fs.readFileSync(file, 'utf8'));
  // v001 is a flat array; v002 (built by build_related_link_worklist.py) nests the settable rows
  // under "eligible" alongside the rows that are waiting or unresolved.
  const raw = Array.isArray(parsed) ? parsed : (parsed.eligible || []);
  const eligible = raw.filter((r) => r.longform_video_id);
  const seen = new Set();
  for (const r of eligible) {
    if (!/^[A-Za-z0-9_-]{11}$/.test(r.short_video_id)) throw new Error(`bad short id: ${r.short_video_id}`);
    if (!/^[A-Za-z0-9_-]{11}$/.test(r.longform_video_id)) throw new Error(`bad longform id: ${r.longform_video_id}`);
    if (seen.has(r.short_video_id)) throw new Error(`duplicate short id in worklist: ${r.short_video_id}`);
    seen.add(r.short_video_id);
  }
  return { rows: eligible, total: raw.length, allow: seen };
}

function loadLedger() {
  const latest = new Map();
  if (!fs.existsSync(LEDGER)) return latest;
  for (const line of fs.readFileSync(LEDGER, 'utf8').split('\n')) {
    if (!line.trim()) continue;
    try {
      const r = JSON.parse(line);
      latest.set(r.short_video_id, r);
    } catch {
      /* a truncated final line from a killed run is not fatal */
    }
  }
  return latest;
}

function record(entry) {
  fs.mkdirSync(STATE_DIR, { recursive: true });
  fs.appendFileSync(LEDGER, JSON.stringify(entry) + '\n', 'utf8');
}

// ---------------------------------------------------------------- Data API guard

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
  const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', body });
  if (!r.ok) throw new Error(`token refresh failed: HTTP ${r.status}`);
  return (await r.json()).access_token;
}

// Snapshot exactly the fields this tool must never move. The description is reduced to its length
// rather than stored, so the state file cannot become a place long text or secrets accumulate.
async function snapshot(ids) {
  const tok = await accessToken();
  const out = {};
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const u = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id=' + chunk.join(',');
    const r = await fetch(u, { headers: { Authorization: `Bearer ${tok}` } });
    if (!r.ok) throw new Error(`videos.list failed: HTTP ${r.status}`);
    for (const v of (await r.json()).items || []) {
      out[v.id] = {
        title: v.snippet.title,
        descLen: (v.snippet.description || '').length,
        privacyStatus: v.status.privacyStatus,
        publishAt: v.status.publishAt || null,
      };
    }
  }
  return out;
}

function diffSnapshots(before, after) {
  const diffs = [];
  for (const id of Object.keys(before)) {
    const b = before[id];
    const a = after[id];
    if (!a) {
      diffs.push({ id, field: 'video', before: 'present', after: 'MISSING' });
      continue;
    }
    for (const k of ['title', 'descLen', 'privacyStatus', 'publishAt']) {
      if (String(b[k]) !== String(a[k])) diffs.push({ id, field: k, before: b[k], after: a[k] });
    }
  }
  return diffs;
}

// ---------------------------------------------------------------- Studio page work

async function expandDetails(pg) {
  await pg.evaluate((labels) => {
    const b = [...document.querySelectorAll('ytcp-button, button, tp-yt-paper-button')]
      .find((e) => labels.includes((e.textContent || '').trim()));
    if (b) b.click();
  }, L.showAll);
  await sleep(1800);
}

// A modal left open by a failed row swallows every click on the next one, which is how one
// failure became three. Escape first, then the labelled close button, then check it is gone.
async function dismissDialog(pg) {
  await pg.keyboard.press('Escape').catch(() => {});
  await sleep(600);
  await pg.evaluate((labels) => {
    const x = [...document.querySelectorAll('ytcp-button, button')]
      .find((e) => labels.some((l) => (e.getAttribute('aria-label') || '').includes(l)));
    if (x) x.click();
  }, L.close);
  await sleep(900);
}

async function openEdit(pg, videoId) {
  await dismissDialog(pg);
  await pg.goto(`https://studio.youtube.com/video/${videoId}/edit`,
                { waitUntil: 'networkidle2', timeout: 120000 });
  await sleep(3500);
}

// Poll instead of sleeping. The picker dialog loads its thumbnail grid over the network, and on a
// busy machine the search input can appear well after the 3s the first version of this waited.
// Three videos in a row failed NO_SEARCH_BOX on 2026-08-09 for exactly that reason, and the
// failure screenshot showed the dialog open with the search box plainly visible.
async function waitFor(pg, fn, arg, timeoutMs = 20000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    if (await pg.evaluate(fn, arg)) return true;
    if (Date.now() > deadline) return false;
    await sleep(500);
  }
}

// offsetParent is part of the test on purpose: the input is in the DOM before it is laid out,
// and the typing step needs a VISIBLE one. When the wait accepted an invisible input the very
// next step reported NO_SEARCH_BOX on a box the screenshot showed plainly. Wait for the same
// thing you are about to use.
const SEARCH_BOX_PRESENT = (placeholders) => [...document.querySelectorAll("input")]
  .some((e) => e.offsetParent && placeholders.some((p) => (e.placeholder || "").includes(p)));

async function readLabel(pg) {
  return pg.evaluate(() => {
    const t = document.querySelector('#linked-video-editor-link');
    return t ? (t.textContent || '').replace(/\s+/g, ' ').trim() : '';
  });
}

async function signedIn(pg) {
  return pg.evaluate(() => !!document.querySelector('ytcp-video-metadata-editor, ytcp-app'));
}

// Returns {status, label, matchedBy}
async function setOne(pg, row, opts) {
  const want = row.longform_title;
  await openEdit(pg, row.short_video_id);
  if (!(await signedIn(pg))) return { status: 'NOT_SIGNED_IN' };
  await expandDetails(pg);

  const current = await readLabel(pg);
  if (!current) return { status: 'NO_CONTROL', label: '' };
  if (norm(current).includes(norm(want).slice(0, 25))) {
    return { status: 'ALREADY_SET', label: current.slice(0, 140) };
  }
  if (opts.verifyOnly || opts.dryRun) {
    return { status: opts.verifyOnly ? 'NOT_SET' : 'WOULD_SET', label: current.slice(0, 140) };
  }

  const opened = await pg.evaluate(() => {
    const t = document.querySelector('#linked-video-editor-link');
    if (!t) return false;
    (t.querySelector('[role="button"]') || t).click();
    return true;
  });
  if (!opened) return { status: 'NO_CONTROL' };
  if (!(await waitFor(pg, SEARCH_BOX_PRESENT, L.searchPlaceholder))) {
    await dismissDialog(pg);
    return { status: 'NO_PICKER_INPUT' };
  }

  // Search by the long-form video ID first: it is unique, so a single returned card is an
  // id-exact selection. Only if the id yields nothing do we fall back to the title.
  let matchedBy = 'id';
  let picked = await typeAndPick(pg, row.longform_video_id, want);
  if (!picked.ok) {
    matchedBy = 'title';
    picked = await typeAndPick(pg, want.slice(0, 40), want);
  }
  if (!picked.ok) {
    await dismissDialog(pg);
    return { status: picked.reason || 'NO_MATCH',
             label: `searched ${matchedBy}; ${picked.cards ?? 0} card(s): ${(picked.sample || []).join(' | ')}` };
  }
  await sleep(2000);

  await pg.evaluate((labels) => {
    const s = [...document.querySelectorAll('ytcp-button, button, tp-yt-paper-button')]
      .find((e) => labels.includes((e.textContent || '').trim()) && e.offsetParent);
    if (s) s.click();
  }, L.save);
  await sleep(5000);

  // Read-back after a full reload. This, and only this, is what a VERIFIED row means.
  await openEdit(pg, row.short_video_id);
  await expandDetails(pg);
  const label = await readLabel(pg);
  const ok = norm(label).includes(norm(want).slice(0, 25));
  return { status: ok ? 'VERIFIED' : 'NOT_VERIFIED', label: label.slice(0, 140), matchedBy };
}

async function typeAndPick(pg, query, wantTitle) {
  const typed = await pg.evaluate((q, placeholders) => {
    const inp = [...document.querySelectorAll('input')]
      .find((e) => e.offsetParent && placeholders.some((p) => (e.placeholder || '').includes(p)));
    if (!inp) return false;
    const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    setter.call(inp, '');
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    setter.call(inp, q);
    inp.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  }, query, L.searchPlaceholder);
  if (!typed) return { ok: false, reason: 'NO_SEARCH_BOX' };
  // Wait for the filtered grid rather than guessing at 3.5s.
  await waitFor(pg, () => document.querySelectorAll(
    'ytcp-video-picker-card, ytcp-entity-card, .video-card, [role="option"]').length > 0, null, 15000);
  await sleep(1200);

  return pg.evaluate((want) => {
    const n = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    const w = n(want).slice(0, 28);
    const cards = [...document.querySelectorAll(
      'ytcp-video-picker-card, ytcp-entity-card, .video-card, [role="option"]')];
    const hit = cards.find((c) => n(c.textContent).includes(w));
    if (!hit) return { ok: false, reason: 'NO_MATCH', cards: cards.length,
                       sample: cards.slice(0, 3).map((c) => n(c.textContent).slice(0, 40)) };
    hit.click();
    return { ok: true, cards: cards.length };
  }, wantTitle);
}

// ---------------------------------------------------------------- main

(async () => {
  const opts = args();
  const { rows, total, allow } = loadWorklist(opts.worklist);
  console.log(`worklist ${path.relative(ROOT, opts.worklist)}: ${total} rows, ${rows.length} eligible`);

  let queue = rows;
  if (opts.only) {
    if (!allow.has(opts.only)) {
      console.error(`REFUSED: ${opts.only} is not in the worklist. This tool only touches worklist rows.`);
      process.exit(1);
    }
    queue = rows.filter((r) => r.short_video_id === opts.only);
  }

  const ledger = loadLedger();
  const pending = queue.filter((r) => {
    const p = ledger.get(r.short_video_id);
    return !(p && ['VERIFIED', 'ALREADY_SET'].includes(p.status) && p.longform_video_id === r.longform_video_id);
  });
  const skipped = queue.length - pending.length;
  let work = pending;
  if (opts.limit) work = work.slice(0, opts.limit);
  const mode = opts.verifyOnly ? 'VERIFY-ONLY (no writes)' : opts.dryRun ? 'DRY-RUN (no writes)' : 'SET';
  console.log(`mode ${mode} | ${queue.length} targeted | ${skipped} already verified in ledger | ${work.length} to process`);
  if (!work.length) {
    console.log('nothing to do');
    process.exit(0);
  }

  const pup = puppeteer();
  let browser;
  try {
    browser = await pup.connect({ browserURL: BROWSER_URL, defaultViewport: null, protocolTimeout: 600000 });
  } catch (e) {
    console.error(`\nNo Chrome is listening on ${BROWSER_URL}.`);
    console.error('Start the dedicated profile first (it is signed in once, by hand):');
    console.error('    node scripts/studio/start_chrome.js');
    process.exit(2);
  }

  const ids = work.map((r) => r.short_video_id);
  const before = await snapshot(ids);
  console.log(`metadata guard: snapshot of ${Object.keys(before).length}/${ids.length} shorts taken`);

  fs.mkdirSync(SHOTS, { recursive: true });
  // A fresh tab per video. Studio stacks a new tp-yt-paper-dialog every time the picker is
  // opened and does not remove the old ones -- nine of them were counted in one tab on
  // 2026-08-09 -- and once that pile builds up the search input inside the newest dialog stops
  // being reachable. Three videos failed NO_SEARCH_BOX in a reused tab and every one of them
  // succeeded first try in a fresh one. Escape and the close button are not enough; a new tab is.
  const newTab = async () => {
    const p = await browser.newPage();
    await p.setViewport({ width: 1500, height: 1000 });
    return p;
  };

  const counts = {};
  let streak = 0;
  const runId = new Date().toISOString();
  for (const row of work) {
    if (!allow.has(row.short_video_id)) {          // defensive: cannot happen, must never happen
      console.error(`REFUSED (not in allowlist): ${row.short_video_id}`);
      continue;
    }
    let r;
    const pg = await newTab();
    try {
      r = await setOne(pg, row, opts);
    } catch (e) {
      r = { status: 'ERROR', label: String(e.message).slice(0, 120) };
    }
    if (r.status === 'NOT_SIGNED_IN') {
      console.error('\nThe dedicated profile is not signed in to YouTube Studio.');
      console.error('Sign in once by hand in that Chrome window, then re-run this command.');
      await pg.close();
      await browser.disconnect();
      process.exit(3);
    }
    const entry = {
      run: runId,
      at: new Date().toISOString(),
      short: row.short,
      short_video_id: row.short_video_id,
      longform_video_id: row.longform_video_id,
      longform_title: row.longform_title,
      status: r.status,
      matched_by: r.matchedBy || null,
      readback_label: r.label || '',
      mode,
    };
    record(entry);
    counts[r.status] = (counts[r.status] || 0) + 1;
    const bad = !['VERIFIED', 'ALREADY_SET', 'NOT_SET', 'WOULD_SET'].includes(r.status);
    if (bad) {
      streak++;
      try { await pg.screenshot({ path: path.join(SHOTS, `${row.short_video_id}.png`) }); } catch {}
    } else {
      streak = 0;
    }
    const tag = row.short == null ? '' : `short${row.short}`;   // newer Shorts have no local number
    console.log(`  ${tag.padEnd(9)} ${row.short_video_id}  ${r.status.padEnd(15)} ${(r.label || '').slice(0, 60)}`);
    await pg.close().catch(() => {});
    if (streak >= 3) {
      console.log('THREE FAILURES IN A ROW - stopping rather than grinding through a broken UI');
      break;
    }
    await sleep(2500 + Math.floor(Math.random() * 2500));
  }

  await browser.disconnect();

  const after = await snapshot(ids);
  const diffs = diffSnapshots(before, after);
  fs.writeFileSync(GUARD, JSON.stringify({ run: runId, before, after, diffs }, null, 2), 'utf8');
  console.log('\n' + Object.entries(counts).map(([k, v]) => `${k}=${v}`).join('  '));
  if (diffs.length) {
    console.error(`METADATA GUARD FAILED: ${diffs.length} field(s) changed that must not change`);
    for (const d of diffs.slice(0, 20)) console.error(`   ${d.id} ${d.field}: ${d.before} -> ${d.after}`);
    console.error(`   full detail: ${path.relative(ROOT, GUARD)}`);
    process.exit(4);
  }
  console.log('metadata guard: PASS - no title, description length, privacy or publishAt changed');
  console.log(`ledger: ${path.relative(ROOT, LEDGER)}`);

  const unresolved = Object.entries(counts)
    .filter(([k]) => !['VERIFIED', 'ALREADY_SET'].includes(k))
    .reduce((a, [, v]) => a + v, 0);
  process.exit(unresolved && !opts.verifyOnly && !opts.dryRun ? 5 : 0);
})().catch((e) => {
  console.error('FAILED:', e.message);
  process.exit(1);
});
