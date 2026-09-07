import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT07_CAPTIONS, SHORT07_TOTAL_SEC} from './short07_timing';

/**
 * SHORT #7 — Riley v. California ("Police need a warrant for your phone").
 * Source of truth: episodes/_planning/SHORTS_EP1-8.md + SHORTS_MOTION_DESIGN.md §3 #7.
 * Meaning animation: phone exception hook / legacy search flow / life-in-phone reveal / 9-0 vote + citation.
 */

const img = (n: string) => `shorts/short07/short07_${n}.png`;
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
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'YOUR PHONE\nIS DIFFERENT', art: {kind: 'bignum', top: 'NO', bottom: 'PHONE SEARCH'}},
  {line: 'L2', id: 'b1a', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'OLD RULE:\nSEARCH YOUR STUFF'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax',
   art: {kind: 'diagram', steps: ['Arrest', 'Search your pockets', 'Two-century rule']}},
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'A PHONE HOLDS\nYOUR LIFE'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'pushin',
   art: {kind: 'doors', title: 'Inside your phone', items: ['Messages', 'Photos', 'Location', 'Your life']}},
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns',
   telop: '2014: 9-0\nGET A WARRANT', art: {kind: 'vote', yes: 9, no: 0}},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Riley v. California', source: '2014'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'PHONES ARE DIFFERENT'},
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT07_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT07: ShortData = {
  shortId: 'short07',
  episodeId: 'PD-2026-007-riley',
  durationSec: SHORT07_TOTAL_SEC,
  narrationSrc: 'shorts/short07/audio/short07_final_mix_v002_en_us.mp3',
  captions: SHORT07_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
