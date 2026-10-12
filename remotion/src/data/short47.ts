import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT47_CAPTIONS, SHORT47_TOTAL_SEC} from './short47_timing';

/**
 * SHORT #47 — Bearden v. Georgia (1983) / jailed for being too poor. PREMIUM tier.
 * EP45 cleveland (PD-2026-045-cleveland). R2: Harriet Cleveland is a living private person —
 * NO face/body/likeness; symbols only (citation stack, face-down license, intake door, signed
 * order & gavel, booking clock, a for-profit invoice, colonnade, institutional corridor). No
 * poverty-porn. Images reuse EP45 cleveland SDXL stills (H:/pd-media/assets/ai/cleveland/S*).
 *
 * WORDING LOCKS (every telop / caption / label below obeys these — do NOT loosen):
 *  1. NEVER say the practice was "legal" / "lawful". The theme is: jailing someone only because
 *     they are too poor has been UNCONSTITUTIONAL since 1983 (Bearden) — yet it continued. It is an
 *     ENFORCEMENT failure, not a legal one. Keep "the rule held; enforcing it is what failed".
 *  2. Cleveland's relief was a LOWER-COURT 2014 SETTLEMENT — NOT the Supreme Court. NEVER say
 *     "the Supreme Court saved her" / "the Supreme Court freed Cleveland". Bearden is the SCOTUS
 *     line (1983); Cleveland's remedy is the 2014 settlement in her own case.
 *  3. Bearden's holding is bounded: a court may not jail for nonpayment without first asking whether
 *     the person could pay (and weighing alternatives). It did NOT abolish fines. Don't overstate.
 *  4. $1,554-or-31-days and the $200/$40 split are FFJC-attributed (medium confidence) — shown on
 *     cards as figures, framed as the order she faced; narration keeps them plain ("fifteen hundred").
 */

const img = (n: string) => `shorts/short47/short47_${n}.png`;
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
  // L1 — hook: job, car, license gone; then a court took her freedom over tickets; jail you for being broke?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'JAILED FOR\nBEING POOR', art: {kind: 'lightrays'}},
  {line: 'L1', id: 'hook2', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'JOB, CAR,\nLICENSE — GONE'},

  // L2 — the order: fines grew; pay $1,554 or 31 days; no one asked if she could pay; the door closed
  {line: 'L2', id: 'b1', src: img('04'), kind: 'image', motion: 'pushin', telop: 'PAY OR\nGO TO JAIL'},
  {line: 'L2', id: 'b2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 1554, prefix: '$', topLabel: 'THE ORDER', label: 'or thirty-one days in jail'}},
  {line: 'L2', id: 'b3', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'NO ONE ASKED:\nCOULD SHE PAY?'},

  // L3 — the machine: for-profit probation; $40 of every payment; her ruin was revenue; already forbidden
  {line: 'L3', id: 'c1', src: img('06'), kind: 'image', motion: 'parallax', telop: 'A PRIVATE\nCOMPANY'},
  {line: 'L3', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 40, prefix: '$', topLabel: 'EVERY MONTH TO THE COMPANY', label: 'skimmed before a cent of her fine'}},
  {line: 'L3', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'ALREADY\nFORBIDDEN'},

  // L4 — Bearden: too poor is not jailable; the law was on her side; freed by a settlement, not SCOTUS
  {line: 'L4', id: 'd1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 1983, to: 2014, label: 'UNCONSTITUTIONAL SINCE 1983'}},
  {line: 'L4', id: 'd2', src: img('08'), kind: 'image', motion: 'pushin', telop: 'FREED BY A\nSETTLEMENT'},
  {line: 'L4', id: 'd3', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'THE RULE HELD.\nENFORCING IT FAILED'},

  // L5 — CTA (return to the citation stack)
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'JAILED FOR\nBEING POOR'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT47_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT47: ShortData = {
  shortId: 'short47',
  episodeId: 'PD-2026-045-cleveland',
  durationSec: SHORT47_TOTAL_SEC,
  narrationSrc: 'shorts/short47/audio/short47_final_mix_v002_en_us.mp3',
  captions: SHORT47_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
