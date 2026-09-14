import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT21_CAPTIONS, SHORT21_TOTAL_SEC} from './short21_timing';

/**
 * SHORT #21 — D.B. Cooper ("he vanished"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #21.
 * R2 / sensitive: unsolved hijacking. WORDING LOCKS — UNSOLVED; never assert anyone "was D.B. Cooper";
 * the FBI never confirmed any suspect; the bomb was a CLAIM; 2016 = SUSPENDED, not solved; jump time/place
 * kept broad. No real-person likeness, no face. Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short21/short21_${n}.png`;
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
  // L1 — hook: jumped with $200k, vanished forever
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HE\nVANISHED'},
  // L2 — Nov 24 1971; "Dan Cooper"; bomb CLAIM
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: '1971:\n"DAN COOPER"'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: 'A NOTE:\n"I HAVE A BOMB"'},
  // L3 — $200k + 4 chutes; released passengers; jumped over Washington
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: '$200K ·\n4 CHUTES'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'JUMPED INTO\nTHE NIGHT'},
  // L4 — 45 yrs, only unsolved US hijacking; 1980 boy found ~$5,800, serials matched; 2016 suspended not solved
  {line: 'L4', id: 'c1', src: img('07'), kind: 'image', motion: 'kenburns', telop: '45 YEARS\nUNSOLVED'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'pushin', telop: '1980: ~$5,800\nBY A RIVER'},
  {line: 'L4', id: 'c3', src: img('04'), kind: 'image', motion: 'parallax', telop: 'ONLY MONEY\nEVER FOUND'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'pushin', telop: 'SUSPENDED —\nNOT SOLVED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT21_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT21: ShortData = {
  shortId: 'short21',
  episodeId: 'PD-2026-021-dbcooper',
  durationSec: SHORT21_TOTAL_SEC,
  narrationSrc: 'shorts/short21/audio/short21_final_mix_v002_en_us.mp3',
  captions: SHORT21_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
