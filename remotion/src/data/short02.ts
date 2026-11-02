import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT02_CAPTIONS, SHORT02_TOTAL_SEC} from './short02_timing';

/**
 * SHORT #2 — Gideon v. Wainwright ("A pencil letter that changed every court").
 * US-market English. Source: episodes/_planning/SHORTS_EP1-8.md SHORT #2.
 * R1 / not sensitive (1963 case). No real-person likeness, no logo, no legible real text.
 * Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short02/short02_${n}.png`;
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
  // L1 — hook: can't afford a lawyer?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: "CAN'T AFFORD\nA LAWYER?"},
  // L2 — denied a lawyer, convicted
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'DENIED.\nCONVICTED.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — from his cell, with a pencil, a petition
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'A PENCIL.\nA PETITION.',
   art: {kind: 'citation', label: 'Gideon v. Wainwright', source: '1963'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 9-0, one letter changed courtrooms
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'NINE TO\nZERO'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'parallax', telop: 'ONE LETTER\nCHANGED IT'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT02_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT02: ShortData = {
  shortId: 'short02',
  episodeId: 'PD-2026-002-gideon',
  durationSec: SHORT02_TOTAL_SEC,
  narrationSrc: 'shorts/short02/audio/short02_final_mix_v002_en_us.mp3',
  captions: SHORT02_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
