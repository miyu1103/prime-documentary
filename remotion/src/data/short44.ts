import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT44_CAPTIONS, SHORT44_TOTAL_SEC} from './short44_timing';

/**
 * SHORT #44 — Anjanette Young / wrong-address police raid + Hudson v. Michigan. PREMIUM tier.
 * R2 (Young = living private person). Spec: episodes/_planning/_short_spec_33_PREMIUM.md (shared).
 * Facts + WORDING LOCKS derived from the LOCKED long-form: episodes/_planning/EP42_young_script.en.v001.md
 * (事実対応表, 6 accuracy constraints). Images reuse EP42 young stills S01..S85 (not on disk yet — built later).
 *
 * WORDING LOCKS (every telop / caption / label below obeys these — do NOT loosen):
 *  1. SETTLEMENT ≠ LIABILITY FINDING. The city PAID / a City Council APPROVED it (reported 48-0). NEVER
 *     "court ruled", "found liable", "found guilty". Say "No court found anyone broke the law / No officer
 *     was declared liable". The $2.9M is a settlement, NOT a verdict.
 *  2. NEVER the word "no-knock" — anywhere (telop, caption, label, prompt). The warrant was a REAL, valid
 *     search warrant signed by a judge; the wrong was the ADDRESS.
 *  3. REFORM WAS REJECTED. The Anjanette Young Ordinance was VOTED DOWN (10-4, Nov 2022) — never "she
 *     changed the law" / "the law changed". Say "voted down" / "rejected".
 *  4. HUDSON REACH NOT COMPRESSED. Knock-and-announce is STILL a command of the 4th Amendment; only the
 *     exclusion remedy was denied. Say "still a command — with almost nothing behind it". Never "the rule
 *     was struck down / abolished". (Part IV was a 4-vote plurality; Kennedy did not join — not dramatized here.)
 *  5. BOOKER HUDSON NOT DRAMATIZED — he is not named or depicted in this Short at all.
 *  6. YOUNG'S UNDRESSED STATE = NON-GRAPHIC, SYMBOLIC ONLY ("changing after a shift / before she can cover
 *     herself"). No face, no body, no likeness — objects only (door, handcuff, body cam, clock, check).
 * R2/R1: no identifiable real person, no readable document/check amount burned into any still.
 */

const img = (n: string) => `shorts/short44/short44_${n}.png`;
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
  // L1 — hook: armed police, wrong house, she is right, it is all on camera, does the law owe you anything
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE WRONG\nHOUSE', art: {kind: 'lightrays'}},

  // L2 — the raid: twelve officers, cuffed in her home, a REAL warrant but the wrong address, "wrong house"
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'parallax', telop: 'TWELVE\nOFFICERS'},
  {line: 'L2', id: 'b2', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'CUFFED IN\nHER HOME'},
  {line: 'L2', id: 'b3', src: img('04'), kind: 'image', motion: 'pushin', telop: 'A REAL WARRANT\nWRONG DOOR'},
  {line: 'L2', id: 'b4', src: img('01'), kind: 'image', motion: 'kenburns', telop: '"THE WRONG\nHOUSE"'},

  // L3 — the tape: it was all on camera, buried for years, the country heard her, ~100 ALLEGED violations
  {line: 'L3', id: 'c1', src: img('05'), kind: 'image', motion: 'pushin', telop: 'IT WAS ALL\nON CAMERA'},
  {line: 'L3', id: 'c2', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'BURIED FOR\nTWO YEARS'},
  {line: 'L3', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'THE COUNTRY\nHEARD HER'},
  {line: 'L3', id: 'c4', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 100, prefix: '~', topLabel: 'A WATCHDOG FLAGGED', label: 'alleged violations — not a court finding'}},

  // L4 — the payoff: $2.9M settlement, no court found fault, no one liable, reform voted down, still a command
  {line: 'L4', id: 'd1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 2.9, prefix: '$', suffix: 'M', decimals: 1, topLabel: 'THE CITY PAID HER', label: 'a settlement — not a verdict'}},
  {line: 'L4', id: 'd2', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'PAID TO MAKE\nIT GO AWAY'},
  {line: 'L4', id: 'd3', src: img('09'), kind: 'image', motion: 'pushin', telop: 'NO COURT\nFOUND FAULT'},
  {line: 'L4', id: 'd4', src: img('10'), kind: 'image', motion: 'parallax', telop: 'REFORM\nVOTED DOWN'},
  {line: 'L4', id: 'd5', src: img('11'), kind: 'image', motion: 'pushin', telop: 'STILL A\nCOMMAND'},

  // L5 — CTA (return to the same closed door)
  {line: 'L5', id: 'cta', src: img('12'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT44_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT44: ShortData = {
  shortId: 'short44',
  episodeId: 'PD-2026-042-young',
  durationSec: SHORT44_TOTAL_SEC,
  narrationSrc: 'shorts/short44/audio/short44_final_mix_v001_en_us.mp3',
  captions: SHORT44_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
