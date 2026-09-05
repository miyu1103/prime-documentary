import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT11_CAPTIONS, SHORT11_TOTAL_SEC} from './short11_timing';

/**
 * SHORT #11 — Mahanoy Area SD v. B.L. ("Can your school punish an off-campus post?").
 * US-market English. Source: episodes/_planning/SHORTS_EP9-15.md — Vote 8-1 / 2021. No minor's likeness.
 * Narration-driven cuts (short11_timing.ts). Same footage for YouTube and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short11/short11_${n}.png`;
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
  // L1 — hook: can your school punish a weekend post made from home?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'PUNISHED FOR A\nWEEKEND POST?'},
  // L2 — didn't make the team; vented on a post meant to disappear
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: "DIDN'T MAKE\nTHE TEAM"},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'MEANT TO\nDISAPPEAR'},
  // L3 — screenshots don't vanish; reached the coach; suspended a year
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: "SCREENSHOTS\nDON'T VANISH"},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 2021 SCOTUS 8-1, schools usually can't punish off-campus speech
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2021: 8-1', art: {kind: 'vote', yes: 8, no: 1}},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Mahanoy Area SD v. B.L.', source: '2021'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'OFF-CAMPUS\nSPEECH'},
  // L5 — CTA (platform-specific endcard text swapped at export)
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT11_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT11: ShortData = {
  shortId: 'short11',
  episodeId: 'PD-2026-011-mahanoy',
  durationSec: SHORT11_TOTAL_SEC,
  narrationSrc: 'shorts/short11/audio/short11_final_mix_v002_en_us.mp3',
  captions: SHORT11_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
