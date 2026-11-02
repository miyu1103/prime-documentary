import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT14_CAPTIONS, SHORT14_TOTAL_SEC} from './short14_timing';

/**
 * SHORT #14 — Hot-pursuit home entry ("can a cop chase you into your home?").
 * US-market English. Source: episodes/_planning/SHORTS_EP9-15.md — Lange v. California (2021, 9-0).
 * Neutral. Narration-driven cuts. Same footage for YouTube and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short14/short14_${n}.png`;
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
  // L1 — hook: a cop chases you over something minor; you step inside; can he follow?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'CHASED INTO\nYOUR HOME?'},
  // L2 — music too loud; lights flip on; man pulls into his own garage
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MINOR STOP →\nHIS GARAGE'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — officer sticks foot under closing garage door and walks in
  {line: 'L3', id: 'b2a', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'FOOT UNDER\nTHE DOOR'},
  {line: 'L3', id: 'b2b', src: img('04'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 2021 SCOTUS, minor-offense pursuit alone is no automatic entry; warrant or emergency
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2021: NO\nAUTO ENTRY', art: {kind: 'vote', yes: 9, no: 0}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Lange v. California', source: '2021'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'YOUR HOME\nHOLDS'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT14_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT14: ShortData = {
  shortId: 'short14',
  episodeId: 'PD-2026-014-lange',
  durationSec: SHORT14_TOTAL_SEC,
  narrationSrc: 'shorts/short14/audio/short14_final_mix_v002_en_us.mp3',
  captions: SHORT14_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
