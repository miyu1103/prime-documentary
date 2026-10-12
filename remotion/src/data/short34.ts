import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT34_CAPTIONS, SHORT34_TOTAL_SEC} from './short34_timing';

/**
 * SHORT #34 — Rolin / Brown v. TSA (airport cash civil forfeiture). PREMIUM tier. R2.
 * Spec: episodes/_planning/_short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-034-rolin §1.
 * WORDING LOCKS: amount hedged ("about eighty-two thousand"); domestic-flight cash is legal (no limit, no
 * reporting — reporting only international >$10,000); no one charged; civil forfeiture = money is the
 * defendant, owner must prove it innocent; IJ sued (Brown v. TSA); 2022 settlement; DEA ended airport cash
 * program by 2025; government returned Rolin's savings. No named officials. No real-person likeness.
 * Only on-screen number = $10,000 (the international reporting threshold, grade-A) — NOT the seized amount.
 */

const img = (n: string) => `shorts/short34/short34_${n}.png`;
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
  // L1 — hook: legal to fly with cash, yet taken at the gate
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'TAKEN AT\nTHE GATE', art: {kind: 'lightrays'}},

  // L2 — Rolin: ~$82k life savings seized at the airport, no crime
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'SEIZED —\nNO CRIME'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.24, label: 'HIS CASH'}, {x: 0.5, y: 0.52, label: 'THE GATE'}, {x: 0.5, y: 0.8, label: 'HELD'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 1, to: 2, weight: 3}]}},

  // L3 — the law: domestic cash has no limit; the only limit is $10k INTERNATIONAL; civil forfeiture flips the burden
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 10000, prefix: '$', topLabel: 'THE ONLY CASH LIMIT', label: 'and only when flying internationally'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'GUILTY UNTIL\nYOU PROVE IT'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'THE MONEY\nIS ON TRIAL'},

  // L4 — the fight: IJ sued (Brown v. TSA); 2022 settlement; DEA ended the program by 2025; his savings returned
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 2020, to: 2025, label: 'From lawsuit to shutdown'}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'kenburns', telop: '2022:\nSETTLED'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'HE GOT IT\nBACK'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT34_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT34: ShortData = {
  shortId: 'short34',
  episodeId: 'PD-2026-034-rolin',
  durationSec: SHORT34_TOTAL_SEC,
  narrationSrc: 'shorts/short34/audio/short34_final_mix_v002_en_us.mp3',
  captions: SHORT34_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
