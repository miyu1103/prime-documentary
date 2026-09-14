import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT28_CAPTIONS, SHORT28_TOTAL_SEC} from './short28_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short28/short28_${n}.png`;
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
  // L1 — hook: house seized because the house "did" it, not the family
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE HOUSE\nON TRIAL'},
  // L2 — painter's earned home; son's ~$40 heroin sale to an informant
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: "A PAINTER'S\nHOME"},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'A $40\nSALE'},
  // L3 — city moves against the house; civil forfeiture; property is the defendant; owners must prove it innocent
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'SEIZE\nAND SEAL'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'THE HOUSE =\nDEFENDANT'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'PROVE IT\nINNOCENT'},
  // L4 — 2002-2014 aggregates (locked numbers); class action; 2018 city AGREED to dismantle (not a court ruling)
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: '1,200+\nHOMES'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '$50M+\nIN CASH'},
  {line: 'L4', id: 'c3', src: img('05'), kind: 'image', motion: 'parallax', telop: '~$178\nTYPICAL'},
  {line: 'L4', id: 'c4', src: img('06'), kind: 'image', motion: 'kenburns', telop: '2018: CITY\nAGREED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT28_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT28: ShortData = {
  shortId: 'short28',
  episodeId: 'PD-2026-028-forfeiture',
  durationSec: SHORT28_TOTAL_SEC,
  narrationSrc: 'shorts/short28/audio/short28_final_mix_v002_en_us.mp3',
  captions: SHORT28_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
