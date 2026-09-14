import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT32_CAPTIONS, SHORT32_TOTAL_SEC} from './short32_timing';

/**
 * SHORT #32 — "Can the police search your car?" (Carroll 1925 automobile exception + Collins v. Virginia 2018).
 * Source: episodes/PD-2026-032-carsearch (script.en.v001, claims.v001).
 * WORDING LOCKS: automobile exception since 1925 (Carroll); car ≠ house → probable cause, no warrant, on the
 * spot. Probable cause is NOT a hunch; being pulled over is NOT permission. Scope = wherever the object could
 * fit. Collins v. Virginia = 2018, EIGHT to ONE (not 7-1); the driveway pressed against the home = "curtilage"
 * = part of the home. "extends no further than the automobile itself" ATTRIBUTED to the Court (Sotomayor).
 * No real-person likeness. Same footage for YT/TT; CTA differs.
 */

const img = (n: string) => `shorts/short32/short32_${n}.png`;
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
  // L1 — hook: they can search your car without a warrant, but one place they can't follow it
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'SEARCH\nYOUR CAR'},
  // L2 — 1925 Carroll: agents tore the seats, 68 bottles; a car isn't a house → probable cause, no warrant
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NO WARRANT\nSINCE 1925'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'pushin', telop: '68 BOTTLES\nBEHIND THE SEAT'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'parallax', telop: 'A CAR ≠\nA HOUSE'},
  // L3 — probable cause is the catch: a stop isn't permission, a hunch isn't enough, scope = where it could fit
  {line: 'L3', id: 'b2a', src: img('01'), kind: 'image', motion: 'kenburns', telop: 'A STOP ≠\nPERMISSION'},
  {line: 'L3', id: 'b2b', src: img('04'), kind: 'image', motion: 'pushin', telop: 'NOT A HUNCH —\nA REAL REASON'},
  {line: 'L3', id: 'b2c', src: img('05'), kind: 'image', motion: 'parallax', telop: 'ONLY WHERE\nIT COULD FIT'},
  // L4 — Collins v. Virginia: tarp on a driveway; 8-1 (2018); curtilage = the home; no further than the car
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'LIFTED\nTHE TARP'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: '8 – 1\n(2018)'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'CURTILAGE =\nYOUR HOME'},
  {line: 'L4', id: 'c4', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'NO FURTHER\nTHAN THE CAR'},
  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT32_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT32: ShortData = {
  shortId: 'short32',
  episodeId: 'PD-2026-032-carsearch',
  durationSec: SHORT32_TOTAL_SEC,
  narrationSrc: 'shorts/short32/audio/short32_final_mix_v002_en_us.mp3',
  captions: SHORT32_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
