import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT05_CAPTIONS, SHORT05_TOTAL_SEC} from './short05_timing';

/**
 * SHORT #5 — Madoff ("Steady returns, zero trades").
 * US-market English. Source: episodes/_planning/SHORTS_EP1-8.md SHORT #5.
 * R3 / sensitive: real Ponzi operator (deceased 2021). Never named, never depicted; no human figure in
 * any still. Collapse and 150-year sentence stated as fact. No real-person likeness, no legible real text.
 * Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short05/short05_${n}.png`;
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
  // L1 — hook: steady profits, barely investing
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'STEADY RETURNS\nZERO TRADES'},
  // L2 — most trusted name, smooth returns year after year
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: "WALL ST'S\nSAFEST NAME"},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — almost no real trades
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'NO REAL\nTRADES',
   art: {kind: 'citation', label: 'Ponzi scheme', source: '150-year sentence'}},
  // L4 — new money paid old; collapsed 2008; 150 years
  {line: 'L4', id: 'c0', src: img('05'), kind: 'image', motion: 'pushin', telop: 'NEW MONEY\nPAID OLD'},
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'COLLAPSE\n2008'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'parallax', telop: '150\nYEARS'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT05_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT05: ShortData = {
  shortId: 'short05',
  episodeId: 'PD-2026-005-madoff',
  durationSec: SHORT05_TOTAL_SEC,
  narrationSrc: 'shorts/short05/audio/short05_final_mix_v002_en_us.mp3',
  captions: SHORT05_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
