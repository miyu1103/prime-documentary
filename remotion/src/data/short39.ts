import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT39_CAPTIONS, SHORT39_TOTAL_SEC} from './short39_timing';

/**
 * SHORT #39 — Florence v. Board of Chosen Freeholders (strip-search after a minor offense). PREMIUM tier.
 * R2. No real-person likeness (Albert Florence, officers). Spec: episodes/_planning/_short_spec_33_PREMIUM.md
 * (§0/§4/§5/§10 shared) · facts PD-2026-037-florence §claim-link map.
 * WORDING LOCKS: Florence carried PROOF the fine was already PAID (settled within ~a week); a statewide
 * database never cleared the warrant, so he was arrested anyway — for a debt that no longer existed.
 * At the county jail he was strip-searched at intake; moved to a SECOND jail and searched again (squat and
 * cough). ONE stop, TWO jails, SIX days. Released, no charges, no apology. He sued on principle; won in the
 * district court (2009), reversed by the 3rd Circuit (2010). SCOTUS, APRIL 2, 2012, FIVE TO FOUR, held the
 * searches did NOT violate the Fourth Amendment (the jail won). Kennedy wrote the majority; Breyer dissented.
 * Ruling is NEVER called "wrong" — legitimate competing reasoning. Race framing is ACLU-attributed (keep it
 * out of a 50s Short). Kennedy quote is VERBATIM. Do not assert the specific 1998 charge; "an old case."
 */

const img = (n: string) => `shorts/short39/short39_${n}.png`;
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
  // L1 — hook: he had the receipt, and was arrested and stripped anyway
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HE PAID.\nARRESTED ANYWAY.', art: {kind: 'lightrays'}},

  // L2 — the stop: family night out, a stale warrant for a fine already paid
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A NIGHT OUT\nWITH FAMILY'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'ONE STALE\nWARRANT'},
  {line: 'L2', id: 'b1c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 2005, to: 2012, label: 'A paid fine, all the way to the Supreme Court'}},

  // L3 — the two doors: strip-searched at intake, again at a second jail, six days
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'STRIPPED\nAT INTAKE'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'TWO JAILS.\nSIX DAYS.'},
  {line: 'L3', id: 'b2c', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'NO CHARGES.\nNO APOLOGY.'},

  // L4 — the ruling: he sued on principle; 5-4 the searches were constitutional
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote', quote: 'The seriousness of an offense is a poor predictor of who has contraband.', attribution: 'Justice Kennedy, 2012'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 5, dissent: 4, label: 'FLORENCE v. BD. OF CHOSEN FREEHOLDERS'}},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'ANY OFFENSE.\nNO SUSPICION.'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HE PAID.\nARRESTED ANYWAY.'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT39_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT39: ShortData = {
  shortId: 'short39',
  episodeId: 'PD-2026-037-florence',
  durationSec: SHORT39_TOTAL_SEC,
  narrationSrc: 'shorts/short39/audio/short39_final_mix_v002_en_us.mp3',
  captions: SHORT39_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
