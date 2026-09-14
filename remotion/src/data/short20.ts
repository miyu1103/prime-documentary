import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT20_CAPTIONS, SHORT20_TOTAL_SEC} from './short20_timing';

/**
 * SHORT #20 — Gardner Heist ("still missing"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #20.
 * R2 / sensitive: unsolved crime, third parties. WORDING LOCKS — never name or imply anyone's guilt (the
 * FBI never named the thieves); "$500M" is an ESTIMATE; "biggest" is ATTRIBUTED ("it's called"); the guard
 * is never portrayed as complicit; no reproduction of the actual stolen works (symbolic voids only). No
 * real-person likeness. Same footage for YT and TikTok; CTA differs.
 */

const img = (n: string) => `shorts/short20/short20_${n}.png`;
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
  // L1 — hook: the empty frames still hang; still unsolved
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'STILL\nUNSOLVED'},
  // L2 — March 18 1990; fake police; ~81 minutes
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: '1990:\nFAKE COPS'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: '81 MINUTES\nINSIDE'},
  // L3 — 13 works cut from frames; ~$500M estimate; none found
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: '13 WORKS\nCUT OUT'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: '~$500M\n(ESTIMATE)'},
  {line: 'L3', id: 'b2c', src: img('01'), kind: 'image', motion: 'pushin', telop: 'NONE EVER\nFOUND'},
  // L4 — FBI believes it knows who, never named, now dead; time to charge ran out; $10M reward; frames hang
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'NEVER\nNAMED'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: '$10M\nREWARD'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'EMPTY FRAMES\nSTILL HANG'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT20_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT20: ShortData = {
  shortId: 'short20',
  episodeId: 'PD-2026-020-gardner',
  durationSec: SHORT20_TOTAL_SEC,
  narrationSrc: 'shorts/short20/audio/short20_final_mix_v002_en_us.mp3',
  captions: SHORT20_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
