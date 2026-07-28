import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT23_CAPTIONS, SHORT23_TOTAL_SEC} from './short23_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short23/short23_${n}.png`;
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
  // L1 — hook: JSTOR (the party) didn't even want him charged
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE VICTIM\nSAID NO'},
  // L2 — prodigy: RSS + Creative Commons; believed public knowledge should be public
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A CODING\nPRODIGY'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'KNOWLEDGE\nFOR ALL'},
  // L3 — ~4.8M JSTOR articles; JSTOR settled & didn't want prosecution; MIT neutral; charged anyway 4 -> 13
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: '4.8M\nARTICLES'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'JSTOR: NO\nPROSECUTION'},
  {line: 'L3', id: 'b2c', src: img('01'), kind: 'image', motion: 'pushin', telop: 'CHARGED\nANYWAY'},
  // L4 — 35yr theoretical max PAIRED w/ ~6-month plea signal + scholars; death stated once; causation attributed to family
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: '35 YEARS?\nON PAPER'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: 'PLEA SIGNAL:\n~6 MONTHS'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'parallax', telop: 'HIS FAMILY\nSPOKE OUT'},
  // L5 — CTA (988 Suicide & Crisis Lifeline shown; quiet, respectful)
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT23_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT23: ShortData = {
  shortId: 'short23',
  episodeId: 'PD-2026-023-swartz',
  durationSec: SHORT23_TOTAL_SEC,
  narrationSrc: 'shorts/short23/audio/short23_final_mix_v002_en_us.mp3',
  captions: SHORT23_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Call or text 988',
  ctaTextTT: 'Call or text 988',
  beats: buildBeats(),
};
