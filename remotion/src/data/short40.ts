import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT40_CAPTIONS, SHORT40_TOTAL_SEC} from './short40_timing';

/**
 * SHORT #40 — "Kids for Cash" / Luzerne County judges paid to jail children. PREMIUM tier.
 * R2. No real-person likeness (children, judges, families). Spec: episodes/_planning/_short_spec_33_PREMIUM.md
 * (§0/§4/§5/§10 shared) · facts EP38_kidsforcash_fact_recheck.v001 (ledger-locked).
 * WORDING LOCKS: Two judges — one ran the juvenile court (Ciavarella), one held the county checkbook
 * (Conahan). Conahan DEFUNDED the public detention center and signed an agreement GUARANTEEING a private,
 * for-profit jail a steady stream of children. A developer BUILT it, an attorney RAN it; over ~3 years they
 * passed ABOUT $2.8 MILLION to the judges, disguised as a "finder's fee." KICKBACKS. Half the kids who gave
 * up their lawyer were locked up (vs ~8% statewide). The state Supreme Court VACATED thousands of cases.
 * Conahan pleaded guilty to racketeering — 17.5 years; Ciavarella convicted — 28 years; later ordered to
 * repay $200M+. Grade-A on-screen numbers only: $2.8M, 28 YEARS, ~8%, THOUSANDS VACATED. Do NOT depict the
 * child's death (handled in the long-form, kept out of a 50s Short). Judges TOOK kickbacks — never softened.
 */

const img = (n: string) => `shorts/short40/short40_${n}.png`;
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
  // L1 — hook: a joke web page -> 3 months, a 90-second hearing
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '90 SECONDS.\n3 MONTHS.', art: {kind: 'lightrays'}},

  // L2 — the pattern: half locked up here vs ~8% statewide; the money starts one floor up
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'HALF WERE\nLOCKED UP'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'stack', title: 'CHILDREN LOCKED UP',
     parts: [{label: 'THIS COUNTY', value: 50}, {label: 'REST OF STATE — ~8%', value: 8}]}},
  {line: 'L2', id: 'b1c', src: img('03'), kind: 'image', motion: 'parallax', telop: 'A PRIVATE\nJAIL, PAID'},

  // L3 — follow the money: ~$2.8M to two judges; child in -> cell -> payment
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 2800000, prefix: '$', topLabel: 'TWO JUDGES TOOK', label: 'disguised as a finder’s fee'}},
  {line: 'L3', id: 'b2b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.16, label: 'A CHILD'}, {x: 0.5, y: 0.44, label: 'THE JUDGE'}, {x: 0.5, y: 0.72, label: 'A CELL'}, {x: 0.5, y: 0.94, label: 'A PAYMENT'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 1, to: 2, weight: 3}, {from: 2, to: 3, weight: 3}]}},
  {line: 'L3', id: 'b2c', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'CASH FOR\nEVERY CHILD'},

  // L4 — exposed: thousands vacated; 28 years (the other got 17.5)
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'THOUSANDS\nVACATED'},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 28, suffix: ' YEARS', topLabel: 'THE JUVENILE JUDGE GOT', label: 'the other got 17½'}},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'JUDGES TOOK\nKICKBACKS'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT40_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT40: ShortData = {
  shortId: 'short40',
  episodeId: 'PD-2026-038-kidsforcash',
  durationSec: SHORT40_TOTAL_SEC,
  narrationSrc: 'shorts/short40/audio/short40_final_mix_v002_en_us.mp3',
  captions: SHORT40_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
