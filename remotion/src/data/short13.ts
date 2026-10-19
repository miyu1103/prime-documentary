import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT13_CAPTIONS, SHORT13_TOTAL_SEC} from './short13_timing';

/**
 * SHORT #13 — Arrest DNA collection ("get arrested, even by mistake, and they keep your DNA").
 * US-market English. Source: episodes/_planning/SHORTS_EP9-15.md — Maryland v. King (2013, 5-4).
 * Neutral. Narration-driven cuts. Same footage for YouTube and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short13/short13_${n}.png`;
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
  // L1 — hook: get arrested, even by mistake, and police take and keep your DNA
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'ARRESTED?\nDNA TAKEN'},
  // L2 — 2009 assault arrest; cheek swab at booking
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'SWABBED AT\nBOOKING'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — that sample matched an unsolved case from years earlier
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'MATCHED TO\nAN OLD CASE'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 2013 SCOTUS 5-4 legal; four justices, left and right, dissented
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2013: LEGAL', art: {kind: 'vote', yes: 5, no: 4}},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Maryland v. King', source: '2013'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'BUT 4\nDISSENTED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('03'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT13_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT13: ShortData = {
  shortId: 'short13',
  episodeId: 'PD-2026-013-king',
  durationSec: SHORT13_TOTAL_SEC,
  narrationSrc: 'shorts/short13/audio/short13_final_mix_v002_en_us.mp3',
  captions: SHORT13_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
