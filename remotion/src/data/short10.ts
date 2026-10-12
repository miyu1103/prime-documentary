import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT10_CAPTIONS, SHORT10_TOTAL_SEC} from './short10_timing';

/**
 * SHORT #10 — Kelo v. City of New London ("They can take your home for a private developer").
 * US-market English. Source of truth: episodes/_planning/SHORTS_EP9-15.md — Vote 5-4 / 2005.
 * Narration-driven cuts (short10_timing.ts). Same footage for YouTube and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short10/short10_${n}.png`;
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
  // L1 — hook: the government can take your home and hand the land to a private developer
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'YOUR HOME —\nFOR A COMPANY?'},
  // L2 — the little pink house was perfectly fine; she didn't want to sell
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'THE LITTLE\nPINK HOUSE'},
  // L3 — the city wanted offices & a hotel; is that "public use"?
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'OFFICES &\nA HOTEL'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin', telop: "IS THIS\n'PUBLIC USE'?"},
  // L4 — climax: 2005 SCOTUS 5-4, torn down, never built, land sat empty
  {line: 'L4', id: 'c1', src: img('03'), kind: 'image', motion: 'kenburns',
   telop: '2005: 5-4', art: {kind: 'vote', yes: 5, no: 4}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Kelo v. City of New London', source: '2005'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'NEVER BUILT'},
  // L5 — CTA (platform-specific endcard text swapped at export)
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT10_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT10: ShortData = {
  shortId: 'short10',
  episodeId: 'PD-2026-010-kelo',
  durationSec: SHORT10_TOTAL_SEC,
  narrationSrc: 'shorts/short10/audio/short10_final_mix_v002_en_us.mp3',
  captions: SHORT10_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
