import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT36_CAPTIONS, SHORT36_TOTAL_SEC} from './short36_timing';

/**
 * SHORT #36 — Riley v. California (2014). Loop-designed (last line echoes the hook).
 * Facts: search of a cell phone seized during an arrest requires a warrant; decision was unanimous (9-0).
 * WORDING LOCKS: no warrant to scroll the phone; more private data than a full house search; David Riley's
 * phone searched after a traffic stop; 2014 Supreme Court unanimous; searching a phone needs a warrant.
 * No real-person likeness; no invented quotes.
 */

const img = (n: string) => `shorts/short36/short36_${n}.png`;
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

// NOTE on length: this short is ~33s, deliberately shorter than the 55-62s premium band.
// Rationale (retention data 2026-07-13): the winning short (short08, 41s) was watched ~2.5x
// on loop; short, tight, loop-closed shorts out-retain longer ones. Cut density is kept high
// (~2-3s per beat) so nothing sits still. This is an explicit, documented deviation.
const CUTS: Cut[] = [
  // L1 — hook: stopped for expired tags, hours later they scroll your whole phone, no warrant
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'YOUR PHONE.\nNO WARRANT.', art: {kind: 'lightrays'}},
  {line: 'L1', id: 'h2', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'EVERYTHING\nON IT'},

  // L2 — photos, texts, location: more private than a house search, in your pocket
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'parallax', telop: 'PHOTOS.\nMESSAGES.'},
  {line: 'L2', id: 'b2', src: img('08'), kind: 'image', motion: 'pushin', telop: 'YOUR\nFINGERPRINT'},
  {line: 'L2', id: 'b3', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'IN YOUR\nPOCKET'},

  // L3 — David Riley: arrested, a detective searched his phone, tied him to a shooting
  {line: 'L3', id: 'c1', src: img('04'), kind: 'image', motion: 'pushin', telop: 'ARRESTED'},
  {line: 'L3', id: 'c2', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'THEY\nSEARCHED IT'},

  // L4 — the turn: 2014, unanimous 9-0, phone needs a warrant
  {line: 'L4', id: 'd1', src: img('05'), kind: 'image', motion: 'kenburns', telop: '2014'},
  {line: 'L4', id: 'd2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 9, dissent: 0, label: 'THE SUPREME COURT'}},
  {line: 'L4', id: 'd3', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'WARRANT\nNEEDED'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT36_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT36: ShortData = {
  shortId: 'short36',
  episodeId: 'PD-2026-007-riley',
  durationSec: SHORT36_TOTAL_SEC,
  narrationSrc: 'shorts/short36/audio/short36_final_mix_v002_en_us.mp3',
  captions: SHORT36_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
