import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT42_CAPTIONS, SHORT42_TOTAL_SEC} from './short42_timing';

/**
 * SHORT #42 — Lech v. Jackson / police destroyed a family's house; no compensation. PREMIUM tier.
 * R2. No real-person likeness (the family, the child shown as silhouette only, officers). Spec:
 * episodes/_planning/_short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-040-lech ledger C01–C31.
 * WORDING LOCKS: An ARMED stranger fleeing police (Robert Seacat) broke into the family's house AT RANDOM —
 * NO connection to them. (Do NOT frame the trigger as "a shoplifter"; the locked script frames him as an
 * armed man they tried to arrest.) The 9-year-old got out SAFELY. A ~19-hour standoff; police used gas, a
 * BearCat armored vehicle and explosives; the order on record: "take as much of the building as needed
 * without making the roof fall in." House destroyed. City offered $5,000 for temporary lodging; homeowner's
 * insurance EXCLUDED intentional acts by government; he borrowed $250,000 to rebuild. Courts ruled it was
 * POLICE POWER, not eminent domain = NO taking, NO compensation; the 10th Circuit (2019) quote is VERBATIM;
 * SCOTUS DECLINED review (2020) — a denial decides nothing, asserts no vote. Grade-A numbers: $5,000,
 * $250,000, 19 HOURS. SCOTUS has NOT ruled on the merits; do not assert an outcome.
 */

const img = (n: string) => `shorts/short42/short42_${n}.png`;
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
  // L1 — hook: an innocent family's house, gone in 19 hours
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'GONE IN\n19 HOURS', art: {kind: 'lightrays'}},

  // L2 — the night: a random address, breached and gassed under a chilling order
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A RANDOM\nADDRESS'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'BREACHED\nAND GASSED'},

  // L3 — the bill: $5k offered, insurance excluded government acts, $250k borrowed to rebuild
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 5000, prefix: '$', topLabel: 'THE CITY OFFERED', label: 'for temporary lodging'}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'INSURANCE:\nEXCLUDED'},
  {line: 'L3', id: 'b2c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 250000, prefix: '$', topLabel: 'TO REBUILD, HE BORROWED', label: 'a quarter of a million dollars'}},

  // L4 — the ruling: police power, not a taking; SCOTUS declined; it depends on your city
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote', quote: 'The innocence of the property owner does not factor into the determination.', attribution: 'U.S. Court of Appeals, 10th Circuit, 2019'}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'POLICE POWER,\nNOT A TAKING'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'NOTHING\nOWED'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'GONE IN\n19 HOURS'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT42_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT42: ShortData = {
  shortId: 'short42',
  episodeId: 'PD-2026-040-lech',
  durationSec: SHORT42_TOTAL_SEC,
  narrationSrc: 'shorts/short42/audio/short42_final_mix_v002_en_us.mp3',
  captions: SHORT42_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
