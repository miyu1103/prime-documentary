import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT29_CAPTIONS, SHORT29_TOTAL_SEC} from './short29_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short29/short29_${n}.png`;
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
  // L1 — hook: 30 years, planned execution of an innocent man
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THIRTY YEARS\nINNOCENT'},
  // L2 — whole case on one bullet "match" to an old revolver; no eyewitness/prints/confession
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'ONLY\nTHE BULLETS'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'NO WITNESS,\nNO PRINTS'},
  // L3 — lawyer's mistaken $1,000 belief (no real cap); one-eyed expert; convicted 1986 in about an hour
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'A $1,000\nMISTAKE'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'CONVICTED\nIN AN HOUR'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'pushin'},
  // L4 — EJI proved bullets matched nothing; 9-0 SCOTUS 2014; freed 2015 (152nd)
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'MATCHED\nNOTHING'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '9 – 0\n(2014)'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'FREED\n2015'},
  {line: 'L4', id: 'c4', src: img('06'), kind: 'image', motion: 'kenburns'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT29_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT29: ShortData = {
  shortId: 'short29',
  episodeId: 'PD-2026-029-hinton',
  durationSec: SHORT29_TOTAL_SEC,
  narrationSrc: 'shorts/short29/audio/short29_final_mix_v002_en_us.mp3',
  captions: SHORT29_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
