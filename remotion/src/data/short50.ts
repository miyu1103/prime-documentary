import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT50_CAPTIONS, SHORT50_TOTAL_SEC} from './short50_timing';

/**
 * SHORT #50 — Kansas v. Glover / a traffic stop on a license-plate check. PREMIUM tier.
 * Episode PD-2026-048-glover. R2 subject: Charles Glover Jr. is a living person convicted of driving
 * on a revoked license — no face, no likeness; symbols only (road, plate/laptop, silhouette in the cab,
 * light bar, columns). The story is the STOP and YOUR car, never glorifying him.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP48_glover_script.en.v001.md (事実対応表 G01–G19):
 *  - HOLDING: the Court UPHELD the stop, 8-1 (2020). It does NOT violate the Fourth Amendment. NEVER
 *    call it illegal / unconstitutional / "struck down". (BLOCKER 1)
 *  - Standard = REASONABLE SUSPICION for a brief investigative stop, NOT probable cause. (BLOCKER 3)
 *  - The inference (owner = driver) is reasonable ONLY absent contrary info; it DISSOLVES the moment
 *    the officer can see the driver is plainly not the owner. State the limit. (BLOCKER 2/6)
 *  - Do NOT overclaim "police can stop any car" — the short explicitly negates it. (BLOCKER 6)
 *  - 8-1: Thomas majority; Sotomayor the LONE dissent, quoted attributed to the DISSENT. (BLOCKER 4)
 * On-screen safe: 8-1, "KANSAS v. GLOVER · 2020". Lane accent patrol-blue #5B8DB8.
 */

const ACCENT = '#5B8DB8';
const img = (n: string) => `shorts/short50/short50_${n}.png`;
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
  // L1 — hook: a random plate, "REVOKED", never saw the driver; can they stop your car?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WHO OWNS\nYOUR CAR?', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the case: driver really was the owner; lawyers fought the STOP, not the facts; stopped on a guess
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'LICENSE\nREVOKED'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'NEVER SAW\nHIS FACE'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'STOPPED ON\nA GUESS'},

  // L3 — the standard: reasonable suspicion, not proof, not probable cause; common sense vs stereotype
  {line: 'L3', id: 'b2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'cititle', title: 'REASONABLE\nSUSPICION', subtitle: 'not proof. not probable cause.'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'A HUNCH?\nOR A FACT?'},

  // L4 — the payoff: 8-1 UPHELD; narrow — dissolves if he can see the driver; Sotomayor lone dissent
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 8, dissent: 1, label: 'KANSAS v. GLOVER · 2020'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote',
     quote: 'The majority has paved the road to finding reasonable suspicion based on nothing more than a demographic profile.',
     attribution: 'Justice Sotomayor, dissenting'}},
  {line: 'L4', id: 'c3', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'IT DISSOLVES\nIF HE LOOKS'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('06'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WHO OWNS\nYOUR CAR?'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT50_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT50: ShortData = {
  shortId: 'short50',
  episodeId: 'PD-2026-048-glover',
  durationSec: SHORT50_TOTAL_SEC,
  narrationSrc: 'shorts/short50/audio/short50_final_mix_v002_en_us.mp3',
  captions: SHORT50_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
