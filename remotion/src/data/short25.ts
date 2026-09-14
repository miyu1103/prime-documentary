import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT25_CAPTIONS, SHORT25_TOTAL_SEC} from './short25_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short25/short25_${n}.png`;
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
  // L1 — hook: agent never entered, yet it was a "search" of the home
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NEVER\nENTERED'},
  // L2 — Jan 1992, agent on a public street points a thermal imager at Kyllo's home
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'THERMAL\nSCAN'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'FROM A\nPUBLIC STREET'},
  // L3 — roof/wall glow -> warrant -> plants; device only read heat drifting into open air (never through walls)
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'HEAT\nLEAKS OUT'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'NEVER SAW\nTHROUGH WALLS'},
  {line: 'L3', id: 'b2c', src: img('01'), kind: 'image', motion: 'pushin'},
  // L4 — 5-4 (2001); Scalia: device not in general public use = a search needing a warrant; dissent attributed; firm & bright line
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'A SEARCH —\nGET A WARRANT'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '5 – 4\n(2001)'},
  {line: 'L4', id: 'c3', src: img('05'), kind: 'image', motion: 'parallax', telop: 'DISSENT: JUST\nHEAT OUTSIDE'},
  {line: 'L4', id: 'c4', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'FIRM &\nBRIGHT LINE'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT25_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT25: ShortData = {
  shortId: 'short25',
  episodeId: 'PD-2026-025-kyllo',
  durationSec: SHORT25_TOTAL_SEC,
  narrationSrc: 'shorts/short25/audio/short25_final_mix_v002_en_us.mp3',
  captions: SHORT25_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
