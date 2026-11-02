import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT04_CAPTIONS, SHORT04_TOTAL_SEC} from './short04_timing';

/**
 * SHORT #4 — FTX ("Where did $8 billion go?").
 * US-market English. Source: episodes/_planning/SHORTS_EP1-8.md SHORT #4.
 * R3 / sensitive: living person convicted of fraud (2023). Founder never named, never depicted; no human
 * figure in any still. Jury verdict stated as fact. No real-person likeness, no legible real text.
 * Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short04/short04_${n}.png`;
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
  // L1 — hook: ~$8B missing
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '$8 BILLION\nGONE?'},
  // L2 — biggest exchange, most trusted face
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MOST TRUSTED\nIN CRYPTO'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — secret exception in the code; deposits pulled almost without limit
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'A SECRET\nIN THE CODE',
   art: {kind: 'citation', label: 'Federal fraud trial', source: '2023 verdict'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: vault empty; jury found founder guilty 2023
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'THE VAULT\nWAS EMPTY'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'parallax', telop: 'GUILTY:\n2023'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT04_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT04: ShortData = {
  shortId: 'short04',
  episodeId: 'PD-2026-004-ftx',
  durationSec: SHORT04_TOTAL_SEC,
  narrationSrc: 'shorts/short04/audio/short04_final_mix_v002_en_us.mp3',
  captions: SHORT04_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
