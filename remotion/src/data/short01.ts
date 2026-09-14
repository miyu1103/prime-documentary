import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT01_CAPTIONS, SHORT01_TOTAL_SEC} from './short01_timing';

/**
 * SHORT #1 — Miranda v. Arizona ("Why do police read you your rights?").
 * US-market English. Source: episodes/_planning/SHORTS_EP1-8.md SHORT #1.
 * R1 / not sensitive (1966 case). No real-person likeness, no logo, no legible real text.
 * Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short01/short01_${n}.png`;
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
  // L1 — hook: rights warning isn't politeness
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WHY READ\nYOUR RIGHTS?'},
  // L2 — decades ago: questioned alone for hours, no warning
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NO WARNING.\nNO LAWYER.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — false confessions; 1966 the Court drew a line
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'FALSE\nCONFESSIONS',
   art: {kind: 'citation', label: 'Miranda v. Arizona', source: '1966'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: structural fix; no warning = confession thrown out
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'NO WARNING =\nTHROWN OUT'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'parallax', telop: 'EVERY ARREST\nCHANGED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT01_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT01: ShortData = {
  shortId: 'short01',
  episodeId: 'PD-2026-001-miranda',
  durationSec: SHORT01_TOTAL_SEC,
  narrationSrc: 'shorts/short01/audio/short01_final_mix_v002_en_us.mp3',
  captions: SHORT01_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
