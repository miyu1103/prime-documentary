import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT26_CAPTIONS, SHORT26_TOTAL_SEC} from './short26_timing';

/**
 * SHORT #24 — Raj Rajaratnam ("his own voice"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #24.
 * R2 / sensitive: convicted at a jury trial (stateable as fact; he did NOT plead — never "admitted
 * guilt"). "Longest sentence" is ATTRIBUTED to prosecutors/press, time-bound 2011 (kept out of flat
 * telops). Profit hedged → anchor to ~$54M forfeiture. The Goldman director (Gupta) is a SEPARATE case.
 * No verbatim wiretap dialogue, no real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short26/short26_${n}.png`;
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
  // L1 — hook: agents never opened the door, yet it was an illegal "search"
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NEVER OPENED\nTHE DOOR'},
  // L2 — LA 1965; a mic taped to the OUTSIDE of a glass phone booth; agents never entered
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A MIC ON\nTHE OUTSIDE'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'EVERY WORD\nRECORDED'},
  // L3 — the old ~40yr trespass rule: no physical entry, no search; but he shut the door to keep words private
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'NO TRESPASS —\nNO SEARCH?'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'HE SHUT\nTHE DOOR'},
  {line: 'L3', id: 'b2c', src: img('01'), kind: 'image', motion: 'pushin'},
  // L4 — 7-1 (1967); "protects people, not places"; fault = no warrant (not a ban); Harlan concurrence = the test
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'PEOPLE,\nNOT PLACES'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '7 – 1\n(1967)'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'A WARRANT —\nNOT A BAN'},
  {line: 'L4', id: 'c4', src: img('05'), kind: 'image', motion: 'kenburns', telop: "HARLAN'S TEST:\nPRIVACY"},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT26_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT26: ShortData = {
  shortId: 'short26',
  episodeId: 'PD-2026-026-katz',
  durationSec: SHORT26_TOTAL_SEC,
  narrationSrc: 'shorts/short26/audio/short26_final_mix_v002_en_us.mp3',
  captions: SHORT26_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
