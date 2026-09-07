import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT19_CAPTIONS, SHORT19_TOTAL_SEC} from './short19_timing';

/**
 * SHORT #19 — Varsity Blues ("the side door"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #19.
 * R3 / sensitive: living people who pleaded guilty. WORDING LOCKS — always "pleaded guilty," NEVER
 * "convicted at trial"; Loughlin pleaded guilty to fraud conspiracy only (money-laundering/bribery
 * DISMISSED); schools = victims, not suspects; no knowledge imputed to any child. No real-person
 * likeness, no nameable school/logo. Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short19/short19_${n}.png`;
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
  // L1 — hook: the secret "side door" into elite colleges
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE SIDE\nDOOR'},
  // L2 — March 2019, 50 arrested; Singer's "sham charity"
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MARCH 2019\n50 ARRESTED'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — ~$25M fake athletes / staged photos / SAT taken or fixed
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: '$25M FOR\nFAKE ATHLETES'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin', telop: 'SATs TAKEN\nOR FIXED'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'parallax'},
  // L4 — climax: pleaded guilty (never convicted at trial); schools = victims; almost all pleaded
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'PLEADED\nGUILTY'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: 'SCHOOLS =\nVICTIMS'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'ALMOST ALL\nPLEADED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT19_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT19: ShortData = {
  shortId: 'short19',
  episodeId: 'PD-2026-019-varsityblues',
  durationSec: SHORT19_TOTAL_SEC,
  narrationSrc: 'shorts/short19/audio/short19_final_mix_v002_en_us.mp3',
  captions: SHORT19_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
