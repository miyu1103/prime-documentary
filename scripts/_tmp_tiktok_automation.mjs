import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { execFile as execFileNative } from 'node:child_process';
import { promisify } from 'node:util';
import { setTimeout as waitMs } from 'timers/promises';
import { openUploadTab, uploadAndPrepare, schedulePrepared } from 'file:///C:/Users/aab15/Documents/prime-documentary/scripts/tiktok_browser_helpers.mjs';

const ROOT = 'C:/Users/aab15/Documents/prime-documentary';
const QUEUE_PATH = path.join(ROOT, 'episodes/_planning/measurements/TIKTOK_SCHEDULE_QUEUE.v001.json');
const RECEIPTS_PATH = path.join(ROOT, 'episodes/_planning/measurements/TIKTOK_PUBLISH_RECEIPTS.v001.jsonl');
const RECORD_SCRIPT = path.join(ROOT, 'scripts/record_tiktok_receipt.py');
const HOURS = [9, 13, 17, 21];
const HORIZON_DAYS = 10;
const execFile = promisify(execFileNative);

function pad2(v) {
  return String(v).padStart(2, '0');
}

function formatSlotKey(date) {
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())} ${pad2(date.getHours())}:00`;
}

function toLocalIso(date) {
  const tz = -date.getTimezoneOffset();
  const sign = tz >= 0 ? '+' : '-';
  const abs = Math.abs(tz);
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}T${pad2(date.getHours())}:${pad2(date.getMinutes())}:00${sign}${pad2(Math.floor(abs / 60))}:${pad2(abs % 60)}`;
}

function parseReceiptDate(value) {
  if (!value) return null;
  const parsed = new Date(value);
  if (!Number.isNaN(parsed.getTime())) return parsed;

  const m = String(value).match(/^(\d{4})-(\d{1,2})-(\d{1,2})(?:[T\s](\d{1,2}):(\d{2}))/);
  if (!m) return null;
  return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]), Number(m[4]), Number(m[5]), Number(m[6] || 0), 0);
}

function parseDateFromText(text) {
  if (!text) return null;
  const norm = String(text).replace(/\u00a0/g, ' ').replace(/\u3000/g, ' ').replace(/\s+/g, ' ').trim();
  const m1 = norm.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  const m2 = norm.match(/(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日/);
  const t = norm.match(/(\d{1,2})[:：](\d{2})/);
  const dMatch = m1 || m2;
  if (!dMatch || !t) return null;
  const y = Number(dMatch[1]);
  const mo = Number(dMatch[2]);
  const d = Number(dMatch[3]);
  const h = Number(t[1]);
  const mi = Number(t[2]);
  return new Date(y, mo - 1, d, h, mi, 0, 0);
}

function normalizeText(value) {
  return String(value || "")
    .replace(/\u00a0/g, ' ')
    .replace(/\r?\n/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/[\u2010-\u2015]/g, '-');
}

async function loadJson(filePath) {
  return JSON.parse(await readFile(filePath, 'utf-8'));
}

async function loadReceipts() {
  const text = await readFile(RECEIPTS_PATH, 'utf-8');
  const lines = text.split(/\r?\n/).filter(Boolean);
  const rows = [];
  const map = new Map();
  for (const line of lines) {
    const obj = JSON.parse(line);
    rows.push(obj);
    map.set(obj.short_id, obj);
  }
  return { rows, map };
}

async function scrapeContentRows(tab) {
  await tab.goto('https://www.tiktok.com/tiktokstudio/content', {
    timeoutMs: 90000,
    waitUntil: "domcontentloaded",
  });
  await tab.playwright.waitForLoadState('domcontentloaded', { timeout: 20000 }).catch(() => {});
  const byUrl = new Map();
  let emptyPasses = 0;

  for (let pass = 0; pass < 12; pass += 1) {
    const rows = await tab.playwright.evaluate(() => {
      const out = [];
      const anchors = Array.from(document.querySelectorAll('a[href*="/video/"]'));
      for (const a of anchors) {
        let node = a;
        for (let i = 0; i < 6 && node && node.parentElement; i += 1) {
          node = node.parentElement;
        }
        const text = `${a.textContent || ''} ${(node ? node.innerText : '')} ${a.href || ''}`.replace(/\s+/g, ' ').trim();
        if (!text) continue;
        out.push({
          url: a.href || '',
          text,
        });
      }
      return out;
    });

    if (!rows.length) {
      emptyPasses += 1;
      if (emptyPasses <= 5) {
        await waitMs(900);
        continue;
      }
    }

    let changed = false;
    for (const row of rows) {
      if (!byUrl.has(row.url)) {
        byUrl.set(row.url, row);
        changed = true;
      }
    }

    if (!changed && pass >= 5) break;
    await tab.playwright.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await waitMs(900);
  }

  const slots = new Set();
  for (const row of byUrl.values()) {
    const dt = parseDateFromText(row.text);
    if (dt) slots.add(formatSlotKey(dt));
  }
  return { rows: Array.from(byUrl.values()), slots };
}

function isWindow(dt, now) {
  const max = now.getTime() + HORIZON_DAYS * 24 * 60 * 60 * 1000;
  return dt.getTime() > now.getTime() && dt.getTime() <= max;
}

function buildSlots(now, used) {
  const base = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
  const out = [];
  for (let d = 0; d <= HORIZON_DAYS; d += 1) {
    const day = new Date(base.getFullYear(), base.getMonth(), base.getDate() + d, 0, 0, 0, 0);
    for (const hour of HOURS) {
      const dt = new Date(day.getFullYear(), day.getMonth(), day.getDate(), hour, 0, 0, 0);
      if (!isWindow(dt, now)) continue;
      const key = formatSlotKey(dt);
      if (!used.has(key)) out.push({ datetime: dt, key, hour });
    }
  }
  return out;
}

async function recordReceipt(shortId, url, when, caption) {
  const args = [RECORD_SCRIPT, shortId, 'scheduled', '--url', url, '--scheduled-for', when, '--caption', caption];
  const result = await execFile('python', args, { cwd: ROOT, encoding: 'utf-8', maxBuffer: 1024 * 1024 });
  return JSON.parse(result.stdout || '{}');
}

async function processItem(item, slot, contentRows, browser) {
  let tab = null;
  try {
    if (!item.video_exists || !item.video_file) {
      return { short_id: item.short_id, status: 'failed', reason: 'video missing' };
    }

    tab = await openUploadTab(browser);
    const openSnapshot = await tab.playwright.domSnapshot();
    if (!openSnapshot.includes('動画を選択')) {
      throw new Error('upload control missing on /upload page');
    }

    await uploadAndPrepare(tab, {
      shortId: item.short_id,
      videoPath: item.video_file,
      caption: item.caption,
    });

    const preparedSnapshot = await tab.playwright.domSnapshot();
    const requires = ['誰でも', '高画質', 'コンテンツ再利用', 'ブランド開示', 'AI生成コンテンツ'];
    for (const needle of requires) {
      if (!preparedSnapshot.includes(needle)) {
        throw new Error(`required setting control not detected: ${needle}`);
      }
    }

    const schedule = await schedulePrepared(tab, {
      day: slot.datetime.getDate(),
      targetHour: slot.hour,
      caption: item.caption,
    });

    if (!schedule.url) throw new Error('scheduled row URL is missing from content list');
    const captionPrefix = item.caption.slice(0, 72);
    const rowText = String(schedule.rowText || schedule.text || '');
    if (!rowText.includes(captionPrefix)) {
      throw new Error('caption mismatch in content list row');
    }
    if (!rowText.includes('誰でも')) {
      throw new Error('visibility mismatch in content list row');
    }
    const duplicate = contentRows.rows.filter((row) => row.text.includes(captionPrefix));
    if (duplicate.length >= 2) {
      throw new Error('duplicate caption in content list');
    }

    const postedDate =
      parseDateFromText(`${schedule.displayedSchedule} ${rowText}`) ||
      parseDateFromText(rowText) ||
      parseDateFromText(schedule.displayedSchedule);
    const scheduledAt = postedDate ? toLocalIso(postedDate) : slotToIso(slot.datetime);

    const rec = await recordReceipt(item.short_id, schedule.url, scheduledAt, item.caption);

    contentRows.rows.push({ url: schedule.url, text: `${item.caption} ${scheduledAt}` });

    return {
      short_id: item.short_id,
      status: rec.result || 'recorded',
      url: schedule.url,
      scheduled_for: scheduledAt,
    };
  } finally {
    if (tab) {
      try {
        await tab.close();
      } catch {}
    }
  }
}

function slotToIso(dt) {
  return toLocalIso(dt);
}

export async function runQueueAutomation(browser = globalThis.chrome) {
  if (!browser) {
    throw new Error("chrome/browser runtime is required");
  }

  const queue = await loadJson(QUEUE_PATH);
  const receiptState = await loadReceipts();

  const maxReceived = receiptState.rows
    .map((r) => Number(String(r.short_id).replace(/^short/, '')))
    .filter((n) => Number.isFinite(n))
    .reduce((m, n) => Math.max(m, n), 0);

  const now = new Date();

  const contentTab = await browser.tabs.new();
  const contentRows = await scrapeContentRows(contentTab);
  await contentTab.close();
  if (!contentRows.rows.length) {
    return {
      result: 'blocked',
      reason: 'content list is empty or not readable',
      details: 'no rows found on TikTok Studio content page',
    };
  }

  const usedSlots = new Set(contentRows.slots);
  for (const rec of receiptState.rows) {
    if (rec.status === 'scheduled' && rec.scheduled_for) {
      const dt = parseReceiptDate(rec.scheduled_for);
      if (dt) usedSlots.add(formatSlotKey(dt));
    }
  }

  const mismatch = receiptState.rows.filter((rec) => {
    if (rec.status !== 'scheduled') return false;
    const p = normalizeText(rec.caption || '').slice(0, 120);
    if (!p) return false;

    const byUrl = rec.url ? contentRows.rows.some((row) => row.url === rec.url) : false;
    if (byUrl) return false;

    return !contentRows.rows.some((row) => normalizeText(row.text).includes(p));
  });
  if (mismatch.length) {
    return {
      result: 'blocked',
      reason: 'receipt mismatch',
      missing_in_content_count: mismatch.length,
      missing_in_content: mismatch.map((m) => ({
        short_id: m.short_id,
        caption: m.caption,
      })),
    };
  }

  const candidates = (queue.items || [])
    .filter((item) => item.number >= maxReceived + 1)
    .filter((item) => item.status === 'pending')
    .filter((item) => item.video_exists)
    .sort((a, b) => a.number - b.number)
    .slice(0, 12);

  if (!candidates.length) {
    return { result: 'done', message: 'no pending targets found' };
  }

  const missingVideos = (queue.items || [])
    .filter((item) => item.number >= maxReceived + 1)
    .filter((item) => item.status === 'pending')
    .filter((item) => !item.video_exists)
    .sort((a, b) => a.number - b.number)
    .slice(0, 12);
  if (missingVideos.length) {
    return {
      result: 'blocked',
      reason: 'unrendered shorts in target window',
      missing_videos: missingVideos.map((item) => item.short_id),
    };
  }

  const slots = buildSlots(now, usedSlots);
  if (slots.length < candidates.length) {
    return { result: 'blocked', reason: 'schedule window full', available_slots: slots.length, required: candidates.length };
  }

  const results = [];
  for (let i = 0; i < candidates.length; i += 1) {
    const slot = slots[i];
    const plan = await processItem(candidates[i], slot, contentRows, browser);
    results.push(plan);
    if (plan.status === 'failed') {
      throw new Error(`${plan.short_id}: ${plan.reason}`);
    }
    usedSlots.add(slot.key);
  }

  return {
    result: 'done',
    count: results.length,
    first: candidates[0]?.short_id,
    last: candidates[candidates.length - 1]?.short_id,
    results,
  };
}
