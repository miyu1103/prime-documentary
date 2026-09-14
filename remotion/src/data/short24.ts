import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT24_CAPTIONS, SHORT24_TOTAL_SEC} from './short24_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short24/short24_${n}.png`;
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
  // L1 — hook: FBI used wiretaps (the mob's tool) on Wall Street
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WIRETAPS ON\nWALL STREET'},
  // L2 — Galleon ~$7B; inside sources (Intel/McKinsey/IBM), each charged separately
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: '$7B\nHEDGE FUND'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'INSIDERS AT\nTHE TOP'},
  // L3 — first big case on court-authorized wiretaps; his own calls; May 11 2011 convicted on all 14
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'HIS OWN\nVOICE'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'CONVICTED ON\nALL 14 COUNTS'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'pushin'},
  // L4 — 11 years; ~$54M forfeit; 2013 wiretaps upheld; separate trial convicted a Goldman director
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: '11\nYEARS'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: '~$54M\nFORFEITED'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax', telop: 'WIRETAPS\nUPHELD (2013)'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'SECRETS FROM\nTHE TOP'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT24_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT24: ShortData = {
  shortId: 'short24',
  episodeId: 'PD-2026-024-rajaratnam',
  durationSec: SHORT24_TOTAL_SEC,
  narrationSrc: 'shorts/short24/audio/short24_final_mix_v002_en_us.mp3',
  captions: SHORT24_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
