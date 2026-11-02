import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT40m_CAPTIONS, SHORT40m_TOTAL_SEC} from './short40m_timing';

/**
 * SHORT #40m — "Kids for Cash" — SHORTS_METHOD v001 REFERENCE IMPLEMENTATION.
 * Rebuilt from short40 to the 12-rule spec (episodes/_planning/SHORTS_METHOD.v001.md):
 *  1s hook (open mid-action on "$2.8M to send kids to jail"), packaging-first cover, open-loop
 *  ("how is that even legal / did he get caught?") -> payoff (caught, 28 years, thousands vacated),
 *  25-40s target, loop tail = hook, pattern-interrupt <=2.5s, illustrative NON-REAL judge face at
 *  hook + payoff + loop (CTR_PLAYBOOK §4A, 2-stage Juggernaut->DreamShaper 0.55 painterly), a faceless
 *  child figure for the victims, persona mark + kinetic center-safe captions + spoken/on-screen CTA +
 *  short->long funnel. Facts ledger-locked (EP38_kidsforcash_fact_recheck.v001): $2.8M, Ciavarella 28y /
 *  Conahan 17.5y, ~50% vs ~8% statewide, THOUSANDS vacated. No real-person likeness; child's death kept out.
 * NOTE: this is a NEW composition (short40m); the scheduled short40 files are never touched.
 */

const img = (n: string) => `shorts/short40/short40_${n}.png`;
const JUDGE = 'shorts/short40m/short40m_judge.png';
const CHILD = 'shorts/short40m/short40m_child.png';
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
  // ---- L1 HOOK (0-1s land): the cover = judge face + "$2.8 MILLION / TO JAIL KIDS"; open the loop.
  {line: 'L1', id: 'hook', src: JUDGE, kind: 'image', motion: 'pushin', fast: true,
   telop: '$2.8 MILLION\nTO JAIL KIDS', art: {kind: 'lightrays'}},
  {line: 'L1', id: 'h2', src: CHILD, kind: 'image', motion: 'parallax', fast: true,
   telop: 'REAL KIDS.\nA CELL.'},
  {line: 'L1', id: 'h3', src: JUDGE, kind: 'image', motion: 'pushin',
   telop: 'HOW IS THIS\nLEGAL?'},

  // ---- L2 the case: a joke webpage -> 3 months after a 90-second hearing.
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A JOKE\nWEB PAGE'},
  {line: 'L2', id: 'b2', src: img('01'), kind: 'image', motion: 'parallax', telop: 'SHE EXPECTED\nDETENTION'},
  {line: 'L2', id: 'b3', src: img('05'), kind: 'image', motion: 'kenburns', telop: '3 MONTHS'},
  {line: 'L2', id: 'b4', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 90, suffix: ' SEC', topLabel: 'HER HEARING LASTED', label: "a child's whole case"}},

  // ---- L3 follow the money: starved the public jail, guaranteed a for-profit lockup a supply of kids.
  {line: 'L3', id: 'c1', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'STARVED THE\nPUBLIC JAIL'},
  {line: 'L3', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 2800000, prefix: '$', topLabel: 'TWO JUDGES TOOK', label: 'disguised as a finder’s fee'}},
  {line: 'L3', id: 'c3', src: img('03'), kind: 'image', motion: 'parallax', telop: 'A PRIVATE\nJAIL, PAID'},
  {line: 'L3', id: 'c4', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.16, label: 'A CHILD'}, {x: 0.5, y: 0.44, label: 'THE JUDGE'}, {x: 0.5, y: 0.72, label: 'A CELL'}, {x: 0.5, y: 0.94, label: 'A PAYMENT'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 1, to: 2, weight: 3}, {from: 2, to: 3, weight: 3}]}},
  {line: 'L3', id: 'c5', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'CASH FOR\nEVERY CHILD'},

  // ---- L4 PAYOFF: caught -> thousands vacated -> 28 years.
  {line: 'L4', id: 'd1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'DID HE GET\nCAUGHT?'},
  {line: 'L4', id: 'd2', src: img('06'), kind: 'image', motion: 'parallax', telop: 'FILES BLEW\nIT OPEN'},
  {line: 'L4', id: 'd3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'THOUSANDS\nVACATED'},
  {line: 'L4', id: 'd4', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 28, suffix: ' YEARS', topLabel: 'THE JUDGE GOT', label: 'the other got 17½'}},

  // ---- L5 CTA + funnel, then the LOOP TAIL (judge face + hook telop == first frame).
  {line: 'L5', id: 'cta', src: JUDGE, kind: 'image', motion: 'kenburns'},
  {line: 'L5', id: 'loop', src: JUDGE, kind: 'image', motion: 'pushin', fast: true,
   telop: '$2.8 MILLION\nTO JAIL KIDS'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT40m_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT40M: ShortData = {
  shortId: 'short40m',
  episodeId: 'PD-2026-038-kidsforcash',
  durationSec: SHORT40m_TOTAL_SEC,
  narrationSrc: 'shorts/short40m/audio/short40m_final_mix_v002_en_us.mp3',
  captions: SHORT40m_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
