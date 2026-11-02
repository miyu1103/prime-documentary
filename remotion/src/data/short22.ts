import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT22_CAPTIONS, SHORT22_TOTAL_SEC} from './short22_timing';

/**
 * SHORT #22 — Michael Milken ("98 charges, 6 pleas"). US-market English.
 * Source: episodes/_planning/SHORTS_EP19-24.md SHORT #22.
 * R3 / sensitive: living, pardoned. WORDING LOCKS — "pleaded guilty to six," NEVER "convicted" (not of
 * insider trading / racketeering / RICO / at trial); CHARGED (98) ≠ PLEADED (6); ~$600M = $200M fine +
 * $400M restitution; pardon = clemency NOT innocence, the plea STANDS, the SEC lifetime ban was NOT
 * lifted; genius-vs-greed stays attributed. No real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short22/short22_${n}.png`;
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
  // L1 — hook: 98 counts charged, pleaded guilty to 6
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '98 CHARGED →\n6 PLEADED'},
  // L2 — built the junk-bond market; ~$550M 1987 pay
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'BUILT THE\n"JUNK" MARKET'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: '$550M PAY\nIN 1987'},
  // L3 — 1989 indictment, 98 counts incl. RICO; accusations only; never went to trial
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: '98 COUNTS\n+ RICO'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'NEVER WENT\nTO TRIAL'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'pushin'},
  // L4 — pleaded to 6, RICO+92 dropped; ~$600M; lifetime ban; 2020 pardon forgives punishment, not the plea/ban
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'PLEADED TO 6\n— NOT CONVICTED'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: 'PARDON ≠\nINNOCENCE'},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'parallax', telop: 'GUILTY PLEA\nSTILL STANDS'},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'LIFETIME BAN\nNOT LIFTED'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT22_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT22: ShortData = {
  shortId: 'short22',
  episodeId: 'PD-2026-022-milken',
  durationSec: SHORT22_TOTAL_SEC,
  narrationSrc: 'shorts/short22/audio/short22_final_mix_v002_en_us.mp3',
  captions: SHORT22_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
