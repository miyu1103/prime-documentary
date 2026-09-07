import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT03_CAPTIONS, SHORT03_TOTAL_SEC} from './short03_timing';

/**
 * SHORT #3 — Mapp v. Ohio ("Can evidence from an illegal search be used?").
 * US-market English. Source: episodes/_planning/SHORTS_EP1-8.md SHORT #3.
 * R1 / not sensitive (1961 case). No real-person likeness, no logo, no legible real text.
 * Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short03/short03_${n}.png`;
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
  // L1 — hook: illegal search, can they use it?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'ILLEGAL\nSEARCH?'},
  // L2 — 1957: forced in without a valid warrant
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NO VALID\nWARRANT'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — wrong suspect; found books; charged with another crime
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'WRONG MAN.\nNEW CHARGE.',
   art: {kind: 'citation', label: 'Mapp v. Ohio', source: '1961'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: evidence excluded in any state; guilty may go free
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'EVIDENCE\nTHROWN OUT'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'parallax', telop: 'POLICE KEPT\nHONEST'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT03_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT03: ShortData = {
  shortId: 'short03',
  episodeId: 'PD-2026-003-mapp',
  durationSec: SHORT03_TOTAL_SEC,
  narrationSrc: 'shorts/short03/audio/short03_final_mix_v002_en_us.mp3',
  captions: SHORT03_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
