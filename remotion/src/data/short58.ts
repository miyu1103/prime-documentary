import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT58_CAPTIONS, SHORT58_TOTAL_SEC} from './short58_timing';

/**
 * SHORT #58 — Curtis Flowers / six trials by the same prosecutor (Mississippi, 1996-2020).
 * PREMIUM tier. Episode PD-2026-054-flowers. Sensitivity: Flowers is LIVING and fully cleared
 * (dismissed WITH PREJUDICE + statutory-max compensation) — innocence stated as fact. The four
 * victims are honored as absence (lamp-points image); "shot" stated once, flatly, no re-creation.
 * Evans is LIVING: every characterization traces to SCOTUS wording or record events; the absence
 * of punishment stated as plain fact. The informant appears only as "a jailhouse informant" with
 * his verified recantation. NO alternative suspect hinted. No faces anywhere (verified by eye).
 * Facts + ACCURACY LOCKS from episodes/_planning/EP54_flowers_FACTS_LEDGER.v001.md:
 *  - SIX trials (F22). Retrial after reversal/hung jury is LAWFUL — never claim double jeopardy
 *    was violated (F42). Four convictions thrown out + two hung juries (F15-F22).
 *  - Only direct evidence = a jailhouse informant; VERBATIM recantation "That was a lie." (F23/F26).
 *  - VERBATIM SCOTUS (F31/F32): Flowers v. Mississippi, June 21, 2019, 7-2, Kavanaugh — vote card
 *    uses exactly 7-2; "relentless, determined effort" is his verified wording; struck 41 of the 42
 *    Black prospective jurors it could have struck.
 *  - Sept 4, 2020: charges dropped, dismissed with prejudice (F35). "NEARLY 23 years", "most of
 *    them on death row" — keep both hedges (F08, never a hard death-row year count).
 *  - Murders officially unsolved (F41). Evans never charged, never disciplined, kept his pension
 *    (F39). The 2025 license petition is UNRESOLVED — never implied here (F40).
 * On-screen safe: "TRIED 6 TIMES", "41 OF 42", 7-2 card. Lane accent dust-gold #D2B15E.
 */

const ACCENT = '#D2B15E';
const img = (n: string) => `shorts/short58/short58_${n}.png`;
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
  // L1 — hook: six carved strokes of dust-gold light; six trials, same prosecutor
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'TRIED\n6 TIMES', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — Winona 1996: the store, the four lives, the man police fixed on
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'WINONA,\nMISSISSIPPI. 1996.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'SIXTEEN.\nA NEW HIRE.'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'GOSPEL SINGER.\nNO RECORD.'},

  // L3 — the only direct evidence recants; the trials that never stood
  {line: 'L3', id: 'b2', src: img('05'), kind: 'image', motion: 'kenburns', telop: '"THAT WAS\nA LIE"'},
  {line: 'L3', id: 'b2b', src: img('06'), kind: 'image', motion: 'parallax', telop: 'SIX TRIALS.\nNONE STOOD.'},

  // L4 — the jury arithmetic and the Supreme Court's answer
  {line: 'L4', id: 'c1', src: img('07'), kind: 'image', motion: 'pushin', telop: '41 OF 42\nSTRUCK'},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 7, dissent: 2, label: 'FLOWERS v. MISSISSIPPI · 2019'}},
  {line: 'L4', id: 'c3', src: img('08'), kind: 'image', motion: 'kenburns', telop: '"RELENTLESS,\nDETERMINED EFFORT"'},

  // L5 — CTA over the courthouse at the end of the empty night road
  {line: 'L5', id: 'cta', src: img('09'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — the six strokes return, now cracked (plan loop_design echo of beat 1) (rule 5).
  {line: 'L5', id: 'loop', src: img('10'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'TRIED\n6 TIMES'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT58_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT58: ShortData = {
  shortId: 'short58',
  episodeId: 'PD-2026-054-flowers',
  durationSec: SHORT58_TOTAL_SEC,
  narrationSrc: 'shorts/short58/audio/short58_final_mix_v002_en_us.mp3',
  captions: SHORT58_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
