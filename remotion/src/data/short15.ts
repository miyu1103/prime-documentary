import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT15_CAPTIONS, SHORT15_TOTAL_SEC} from './short15_timing';

/**
 * SHORT #15 — Theranos ("when does a bold promise become a crime?").
 * US-market English. Source: episodes/_planning/SHORTS_EP9-15.md.
 * R3 (real, litigated): neutral; fraud finding attributed to the 2022 jury verdict; no real-person
 * likeness, no legible real names/logos in art. Same footage for YT and TikTok; only CTA differs.
 */

const img = (n: string) => `shorts/short15/short15_${n}.png`;
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
  // L1 — hook: one drop of blood, a $9B company, but the machine didn't work
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'A PROMISE\nOR A CRIME?'},
  // L2 — hailed as the next Steve Jobs; whistleblowers said it didn't work as advertised
  {line: 'L2', id: 'b1', src: img('03'), kind: 'image', motion: 'kenburns', telop: "IT DIDN'T\nWORK"},
  {line: 'L2', id: 'b1b', src: img('02'), kind: 'image', motion: 'parallax'},
  // L3 — tests secretly run on other machines; finger-prick unreliable; investors poured in
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'OTHER FIRMS’\nMACHINES'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin'},
  // L4 — climax: 2022 jury convicted of investor fraud; intent is the line
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2022:\nFRAUD', art: {kind: 'citation', label: 'Federal fraud trial', source: '2022 verdict'}},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin'},
  {line: 'L4', id: 'c3', src: img('01'), kind: 'image', motion: 'parallax', telop: 'INTENT IS\nTHE LINE'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT15_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT15: ShortData = {
  shortId: 'short15',
  episodeId: 'PD-2026-015-theranos',
  durationSec: SHORT15_TOTAL_SEC,
  narrationSrc: 'shorts/short15/audio/short15_final_mix_v002_en_us.mp3',
  captions: SHORT15_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
