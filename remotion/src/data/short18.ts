import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT18_CAPTIONS, SHORT18_TOTAL_SEC} from './short18_timing';

/**
 * SHORT #18 — Flash Crash ("$1 trillion gone in 36 minutes, then back").
 * US-market English. Source: episodes/_planning/SHORTS_EP16-18.md.
 * R3 / sensitive: living person who pleaded guilty. CAUSATION LOCK — never says he caused the crash;
 * only "part of the imbalance / not for the crash / not one man alone." Guilty plea (spoofing + wire
 * fraud) is fact. No real-person likeness, no nameable firm. Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short18/short18_${n}.png`;
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
  // L1 — hook: ~$1T vanished in 36 minutes, then came back
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '$1T GONE\nIN 36 MIN'},
  // L2 — May 6, 2010; ~1000 pts down; penny prints
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MAY 6,\n2010'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — London bedroom trader; flash orders meant to cancel; "spoofing"
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'SPOOFING:\nFAKE ORDERS'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: pleaded guilty (spoofing+wire fraud) but NOT to causing the crash; not one man alone
  {line: 'L4', id: 'c1', src: img('07'), kind: 'image', motion: 'kenburns',
   telop: 'GUILTY — NOT\nFOR THE CRASH', art: {kind: 'citation', label: 'Pleaded guilty: spoofing', source: 'not the crash'}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax', telop: 'NOT ONE\nMAN ALONE'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT18_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT18: ShortData = {
  shortId: 'short18',
  episodeId: 'PD-2026-018-flashcrash',
  durationSec: SHORT18_TOTAL_SEC,
  narrationSrc: 'shorts/short18/audio/short18_final_mix_v002_en_us.mp3',
  captions: SHORT18_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
