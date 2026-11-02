import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT31_CAPTIONS, SHORT31_TOTAL_SEC} from './short31_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short31/short31_${n}.png`;
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
  // L1 — hook: they can take your face and thumb; your mind may be the one lock they can't force
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'UNLOCK\nIT'},
  // L2 — phone = your whole life; Riley (2014) needs a warrant to search; but the fight is forcing you to open it
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A WARRANT\nTO SEARCH'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'BUT CAN THEY\nMAKE YOU OPEN IT?'},
  // L3 — 5th shields the mind (passcode may be protected); face/thumb are on the body (treated like a print)
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'MIND\nVS BODY'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'FACE & THUMB:\nNO THOUGHT'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'pushin'},
  // L4 — 2024 a court allowed the thumb; 2025 another forbade it; states split; SCOTUS won't settle it
  {line: 'L4', id: 'c1', src: img('05'), kind: 'image', motion: 'kenburns', telop: '2024:\nTHUMB ALLOWED'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '2025: SAME ACT\nFORBIDDEN'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax', telop: "SCOTUS\nWON'T SETTLE"},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT31_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT31: ShortData = {
  shortId: 'short31',
  episodeId: 'PD-2026-031-unlock',
  durationSec: SHORT31_TOTAL_SEC,
  narrationSrc: 'shorts/short31/audio/short31_final_mix_v002_en_us.mp3',
  captions: SHORT31_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
