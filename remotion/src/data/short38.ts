import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT38_CAPTIONS, SHORT38_TOTAL_SEC} from './short38_timing';

/**
 * SHORT #38 — Robert Williams / Detroit face-recognition wrongful arrest. PREMIUM tier.
 * R2 (living private person) + invariant 11: NO real-person face/likeness — Williams, his family and
 * all officers are anonymous (silhouette / from behind / hands-only). Spec: episodes/_planning/
 * _short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-036-williams §claims.v001.
 * WORDING LOCKS: arrested because SOFTWARE MATCHED HIS FACE (a computer, not a witness) from a blurry
 * store-camera frame vs millions of driver's-license photos; a match is only a LEAD, never proof; the
 * computer's pick was dropped into a lineup shown to someone who had only watched the same video =
 * "probable cause"; ~30 hours in a cell (grade-A, may burn); charges dropped. A government lab (NIST)
 * found these systems misidentify Black and Asian faces FAR MORE OFTEN — but ALWAYS paired with the
 * training-data counter-finding (the gap all but vanishes on systems built in Asia); NEVER an unqualified
 * "racist" verdict. He SUED, the city SETTLED, and it can no longer arrest on a face-match alone.
 * NEVER burn grade-B figures on screen: theft ~$3,800, settlement ~$300,000, "more than a dozen"
 * wrongful arrests — keep hedged in VO only. "First publicly reported," never "first ever."
 */

const img = (n: string) => `shorts/short38/short38_${n}.png`;
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
  // L1 — hook: a computer's guess put an innocent man in a cell
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'A COMPUTER\nPICKED YOU', art: {kind: 'lightrays'}},

  // L2 — the arrest: cuffed on his lawn, ~30 hours, "a computer did"
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'CUFFED ON\nHIS LAWN'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 30, suffix: ' HOURS', topLabel: 'JAILED ON A GUESS', label: 'for a crime he never saw'}},
  {line: 'L2', id: 'b1c', src: img('03'), kind: 'image', motion: 'parallax', telop: 'HE SAID:\nNOT ME'},

  // L3 — the machine: one blurry frame -> a look-alike -> a lineup called "probable cause"
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.14, label: 'BLURRY PHOTO'}, {x: 0.5, y: 0.4, label: 'SOFTWARE'}, {x: 0.5, y: 0.66, label: 'LINEUP'}, {x: 0.5, y: 0.9, label: 'ARREST'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 1, to: 2, weight: 3}, {from: 2, to: 3, weight: 3}]}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'A LEAD —\nNOT PROOF'},
  {line: 'L3', id: 'b2c', src: img('04'), kind: 'image', motion: 'parallax', telop: 'YOUR FACE\nIS IN IT'},

  // L4 — the pattern + the outcome: measured bias (w/ counter-finding in VO), settled, rule rewritten
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'WRONG FACE,\nSAME PATTERN'},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 2020, to: 2024, label: 'From arrest to settlement'}},
  {line: 'L4', id: 'c3', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NO ARREST ON\nA MATCH ALONE'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('02'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'A COMPUTER\nPICKED YOU'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT38_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT38: ShortData = {
  shortId: 'short38',
  episodeId: 'PD-2026-036-williams',
  durationSec: SHORT38_TOTAL_SEC,
  narrationSrc: 'shorts/short38/audio/short38_final_mix_v002_en_us.mp3',
  captions: SHORT38_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
