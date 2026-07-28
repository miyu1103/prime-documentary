import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT30_CAPTIONS, SHORT30_TOTAL_SEC} from './short30_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short30/short30_${n}.png`;
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
  // L1 — hook: a certain survivor was honestly, completely wrong
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'SO SURE —\nSO WRONG'},
  // L2 — 1984 attack; memorized the face; chose Cotton in photo then live lineup
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MEMORIZED\nHIS FACE'},
  {line: 'L2', id: 'b1b', src: img('01'), kind: 'image', motion: 'pushin', telop: 'BOTH TIMES\nSHE CHOSE HIM'},
  // L3 — only man in both lineups; may have recalled the photo; reassurance hardened guess into certainty
  {line: 'L3', id: 'b2a', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'THE ONLY MAN\nIN BOTH LINEUPS'},
  {line: 'L3', id: 'b2b', src: img('04'), kind: 'image', motion: 'parallax', telop: 'A GUESS →\nCERTAINTY'},
  {line: 'L3', id: 'b2c', src: img('03'), kind: 'image', motion: 'pushin'},
  // L4 — decade served; 1995 DNA cleared Cotton, matched Poole; then accuser & accused became friends
  {line: 'L4', id: 'c1', src: img('05'), kind: 'image', motion: 'kenburns', telop: '1995: DNA\nCLEARED HIM'},
  {line: 'L4', id: 'c2', src: img('05'), kind: 'image', motion: 'pushin', telop: 'THE RIGHT\nMAN MATCHED'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax', telop: 'THEN THEY\nBECAME FRIENDS'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT30_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT30: ShortData = {
  shortId: 'short30',
  episodeId: 'PD-2026-030-cotton',
  durationSec: SHORT30_TOTAL_SEC,
  narrationSrc: 'shorts/short30/audio/short30_final_mix_v002_en_us.mp3',
  captions: SHORT30_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
