import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT35_CAPTIONS, SHORT35_TOTAL_SEC} from './short35_timing';

/**
 * SHORT #35 — Carole Hinders / IRS "structuring" seizure. PREMIUM tier. R2 (grade-A public core only).
 * Spec: episodes/_planning/_short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-035-hinders §1.
 * WORDING LOCKS: cash-only restaurant in Iowa (no town); deposited under $10,000; IRS seized her ENTIRE
 * account ~$33,000; "structuring" = splitting deposits to dodge the bank's $10,000 reporting rule; she
 * committed no other crime; civil forfeiture (take first, owner fights). NO false NYT→memo causation —
 * attribute policy change to "national attention"; money returned; Congress later passed a reform (unnamed).
 * No dates, no congressional-testimony claim, no McLellan/stats, no named officials, no real-person likeness.
 */

const img = (n: string) => `shorts/short35/short35_${n}.png`;
const r3 = (n: number) => Math.round(n * 1000) / 1000;

type Cut = {
  line: string;
  id: string;
  src: string | null;
  kind: 'image' | 'video' | 'card';
  motion: ShortBeat['motion'];
  telop?: string;
  fast?: boolean;
  art?: ShortArt;
};

const CUTS: Cut[] = [
  // L1 — hook: followed the rules, account emptied, no crime
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO CRIME.\nACCOUNT GONE.', art: {kind: 'lightrays'}},

  // L2 — Hinders: cash restaurant, deposits under $10k, IRS seized the whole ~$33k account
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'DEPOSITS\nUNDER $10K'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 33000, prefix: '$', topLabel: 'THE IRS SEIZED IT ALL', label: 'her entire bank account'}},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'parallax', telop: 'ACCOUNT\nFROZEN'},

  // L3 — the law: "structuring" (dodge the $10k report), yet no other crime; civil forfeiture flips the burden
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 10000, prefix: '$', topLabel: 'BANKS REPORT CASH OVER', label: 'so staying under it can look suspicious'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'SHE BROKE\nNO OTHER LAW'},
  {line: 'L3', id: 'b2c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.24, label: 'HER DEPOSITS'}, {x: 0.5, y: 0.52, label: 'THE BANK'}, {x: 0.5, y: 0.8, label: 'SEIZED'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 1, to: 2, weight: 3}]}},

  // L4 — the turn: national attention, IRS stops seizing from the innocent, money returned, reform passed
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'NATIONAL\nATTENTION'},
  {line: 'L4', id: 'c2', src: img('03'), kind: 'image', motion: 'parallax', telop: 'POLICY\nCHANGED'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'SHE GOT IT\nBACK'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT35_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT35: ShortData = {
  shortId: 'short35',
  episodeId: 'PD-2026-035-hinders',
  durationSec: SHORT35_TOTAL_SEC,
  narrationSrc: 'shorts/short35/audio/short35_final_mix_v002_en_us.mp3',
  captions: SHORT35_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
