import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT16_CAPTIONS, SHORT16_TOTAL_SEC} from './short16_timing';

/**
 * SHORT #16 — Titan / OceanGate ("a four-day countdown for people already gone").
 * US-market English. Source: episodes/_planning/SHORTS_EP16-18.md.
 * R2 / sensitive (real, deceased people; ongoing litigation): elegiac, non-sensational. All imagery
 * symbolic & disclosed — no likeness, no remains, no implosion. "Preventable"/cause attributed to the
 * 2025 U.S. Coast Guard finding, not the narrator. Same footage for YT and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short16/short16_${n}.png`;
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
  // L1 — hook: the world watched a four-day countdown; they were already gone
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '4-DAY COUNTDOWN\nALREADY GONE'},
  // L2 — June 2023, five aboard the experimental sub Titan, dove toward the Titanic
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'JUNE 2023:\nTO THE TITANIC'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — they had been warned: hull flagged, design called catastrophic, game-controller steering
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'WARNED:\n“CATASTROPHIC”'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — "All good here," then silence; imploded that first day; 2025 Coast Guard: preventable
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: '“ALL GOOD HERE.”\nTHEN SILENCE'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'U.S. Coast Guard', source: '2025: preventable'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'RULED\nPREVENTABLE'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT16_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT16: ShortData = {
  shortId: 'short16',
  episodeId: 'PD-2026-016-titan',
  durationSec: SHORT16_TOTAL_SEC,
  narrationSrc: 'shorts/short16/audio/short16_final_mix_v002_en_us.mp3',
  captions: SHORT16_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
