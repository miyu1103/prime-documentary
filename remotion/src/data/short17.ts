import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT17_CAPTIONS, SHORT17_TOTAL_SEC} from './short17_timing';

/**
 * SHORT #17 — OneCoin ("she sold a cryptocurrency that, prosecutors say, never existed").
 * US-market English. Source: episodes/_planning/SHORTS_EP16-18.md.
 * R3 / HIGH sensitivity: living, CHARGED-BUT-NOT-CONVICTED fugitive. No real-person likeness
 * (wanted poster is a blank silhouette). Fraud/"no blockchain" attributed to prosecutors + the
 * co-founder's guilty plea; on-screen caveat "Charged, not convicted." Same footage for YT and TikTok.
 */

const img = (n: string) => `shorts/short17/short17_${n}.png`;
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
  // L1 — hook: a cryptocurrency that, prosecutors say, never existed
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO COIN.\nNO BLOCKCHAIN'},
  // L2 — 2014 Bulgaria; buy token packages; get paid to recruit
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'BUY IN,\nRECRUIT MORE'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — prosecutors + co-founder's guilty plea: no real blockchain; price typed in
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'PRICE SET\nBY TYPING'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — €4B+ in sales (per prosecutors); charged 2017; vanished; charged-not-convicted-still-missing
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: '4B EUROS,\nTHEN GONE'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Charged, not convicted', source: 'still missing'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'STILL\nMISSING'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT17_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT17: ShortData = {
  shortId: 'short17',
  episodeId: 'PD-2026-017-onecoin',
  durationSec: SHORT17_TOTAL_SEC,
  narrationSrc: 'shorts/short17/audio/short17_final_mix_v002_en_us.mp3',
  captions: SHORT17_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
