import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT57_CAPTIONS, SHORT57_TOTAL_SEC} from './short57_timing';

/**
 * SHORT #57 — The Norfolk Four / four false confessions to one man's crime (Virginia, 1997).
 * PREMIUM tier. Episode PD-2026-053-norfolk. Sensitivity: all four exonerees are LIVING with
 * ABSOLUTE PARDONS — innocence stated as fact. No identifiable person anywhere: caps, objects and
 * back-views only (verified by eye). Michelle Moore-Bosko named once in narration, with dignity;
 * her apartment appears only as exterior absence; no wound detail, no assault language beyond
 * "murdered". The Moore family is not depicted or referenced.
 * Facts + ACCURACY LOCKS from the EP53 FACTS_LEDGER (all H-grade):
 *  - Norfolk, VA, 1997 (NF-01/02). Within hours police land on a sailor from her building (NF-07).
 *  - Eleven hours of overnight interrogation + a false polygraph claim before the first confession
 *    (NF-08/11, "eleven hours" per Frontline's 11+).
 *  - Forensics said ONE attacker; every DNA test excluded all the accused (NF-06/18/38).
 *  - The real killer's prison letter quoted ONLY as rendered in the 4th Cir. record (Tice v.
 *    Johnson): "guess who did that. Me. Ha, ha." His DNA is the only match; he said he acted alone
 *    (NF-21/22).
 *  - More than FORTY years combined before relief (NF-31). VERBATIM (quoted, attributed): federal
 *    judge Gibney — "no sane human being could find them guilty" (NF-39, actual-innocence ruling).
 *  - Detective Ford: federal prison for extortion/false statements in UNRELATED cases — NEVER imply
 *    he was punished for this one (NF-44). NO vote card exists for this case — none used.
 * On-screen safe: "4 CONFESSIONS. 0 KILLERS.", "ACTUALLY INNOCENT". Lane accent harbor
 * steel-blue #7E93A8.
 */

const ACCENT = '#7E93A8';
const img = (n: string) => `shorts/short57/short57_${n}.png`;
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
  // L1 — hook: four sailor caps on a dark steel table
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '4 CONFESSIONS.\n0 KILLERS.', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the harbor, the fast focus, the overnight room
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NORFOLK,\nVIRGINIA. 1997.'},
  {line: 'L2', id: 'b1b', src: img('04'), kind: 'image', motion: 'parallax', telop: 'WITHIN\nHOURS'},
  {line: 'L2', id: 'b1c', src: img('05'), kind: 'image', motion: 'pushin', telop: 'ELEVEN HOURS\nOVERNIGHT'},

  // L3 — the domino: sailor after sailor, and the science saying no every time
  {line: 'L3', id: 'b2', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'ANOTHER.\nTHEN ANOTHER.'},
  {line: 'L3', id: 'b2b', src: img('07'), kind: 'image', motion: 'parallax', telop: 'EVERY DNA\nTEST: NO'},

  // L4 — the real killer's letter, then the ruling that ends it
  {line: 'L4', id: 'c1', src: img('08'), kind: 'image', motion: 'pushin', telop: 'HIS DNA\nMATCHES EVERYTHING'},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote',
     quote: 'No sane human being could find them guilty.',
     attribution: 'Judge John Gibney, U.S. District Court'}},
  {line: 'L4', id: 'c3', src: img('01'), kind: 'image', motion: 'kenburns', telop: 'ACTUALLY\nINNOCENT'},

  // L5 — CTA over the lone cap on the wet pier
  {line: 'L5', id: 'cta', src: img('09'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook caps (last frame cuts back to first) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: '4 CONFESSIONS.\n0 KILLERS.'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT57_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT57: ShortData = {
  shortId: 'short57',
  episodeId: 'PD-2026-053-norfolk',
  durationSec: SHORT57_TOTAL_SEC,
  narrationSrc: 'shorts/short57/audio/short57_final_mix_v002_en_us.mp3',
  captions: SHORT57_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
