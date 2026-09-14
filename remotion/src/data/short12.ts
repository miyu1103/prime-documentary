import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT12_CAPTIONS, SHORT12_TOTAL_SEC} from './short12_timing';

/**
 * SHORT #12 — Forced arbitration ("'I agree' can waive your right to sue").
 * US-market English. Source: episodes/_planning/SHORTS_EP9-15.md — Concepcion (2011, 5-4) + Epic (2018).
 * Neutral. Narration-driven cuts. Same footage for YouTube and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short12/short12_${n}.png`;
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
  // L1 — hook: you gave up your right to sue when you tapped "I agree"
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'YOU GAVE UP\nYOUR RIGHT TO SUE'},
  // L2 — one clause in the fine print: arbitration, no court, no class action
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NO COURT.\nNO CLASS ACTION.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax'},
  // L3 — it started at ~$30 on a "free" phone; small harms need joining together
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'IT STARTED\nAT $30'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 2011 SCOTUS 5-4 enforce; 2018 reached the workplace
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2011: 5-4', art: {kind: 'vote', yes: 5, no: 4}},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'AT&T Mobility v. Concepcion', source: '2011'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'THEN YOUR\nJOB, 2018'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT12_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT12: ShortData = {
  shortId: 'short12',
  episodeId: 'PD-2026-012-arbitration',
  durationSec: SHORT12_TOTAL_SEC,
  narrationSrc: 'shorts/short12/audio/short12_final_mix_v002_en_us.mp3',
  captions: SHORT12_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
