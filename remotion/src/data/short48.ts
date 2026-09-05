import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT48_CAPTIONS, SHORT48_TOTAL_SEC} from './short48_timing';

/**
 * SHORT #48 — New Jersey v. T.L.O. / the schoolhouse Fourth Amendment. PREMIUM tier.
 * Episode PD-2026-046-tlo. R2 subject: T.L.O. is a MINOR — no face, no likeness, no name beyond
 * the public initials; symbols only (purse, desk, lockers, gate, columns). Drugs clinical/minimal.
 * Facts + WORDING LOCKS from episodes/_planning/EP46_tlo_script.en.v001.md (事実対応表 F01–F17):
 *  - HOLDING(1): the Fourth Amendment DOES apply to public-school officials — students do NOT lose
 *    it at the door. NEVER "students have no rights" / "schools can search anything". (BLOCKER)
 *  - HOLDING(2): the standard is LOWERED, not eliminated — no warrant, no probable cause, just
 *    REASONABLE SUSPICION, plus a two-part test (justified at inception + reasonably related in scope).
 *  - 6-3, White majority / Brennan, Marshall, Stevens partial dissent. Neutral attribution.
 *  - When POLICE run the search a higher standard can return (footnote 7) — not overclaimed here.
 * On-screen safe: 6-3, "NEW JERSEY v. T.L.O. · 1985", the two-prong test. Lane accent green #3F8F5F.
 */

const ACCENT = '#3F8F5F';
const img = (n: string) => `shorts/short48/short48_${n}.png`;
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
  // L1 — hook: a purse dumped on the desk; does the 4th Amendment follow you into school?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'INSIDE\nSCHOOL?', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the search: she denied it, the bag opened anyway, one object pointed to the next
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'SHE SAID\nSHE DIDN’T'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'diagram', steps: ['CIGARETTES', 'ROLLING PAPERS', 'THEN: DEALING']}},
  {line: 'L2', id: 'b1c', src: img('03'), kind: 'image', motion: 'parallax', telop: 'THROW IT\nOUT'},

  // L3 — the turn: two easy answers refused; the 4th Amendment DOES follow you in
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'pushin', telop: 'STOPS AT\nTHE DOOR?'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'NO — IT\nFOLLOWS YOU'},

  // L4 — the catch: lowered bar (reasonable suspicion, in proportion); 6-3
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'diagram', steps: ['REASONABLE SUSPICION', 'NOT PROBABLE CAUSE', 'KEPT IN PROPORTION']}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 6, dissent: 3, label: 'NEW JERSEY v. T.L.O. · 1985'}},
  {line: 'L4', id: 'c3', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'A LOWER\nBAR'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('06'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'INSIDE\nSCHOOL?'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT48_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT48: ShortData = {
  shortId: 'short48',
  episodeId: 'PD-2026-046-tlo',
  durationSec: SHORT48_TOTAL_SEC,
  narrationSrc: 'shorts/short48/audio/short48_final_mix_v002_en_us.mp3',
  captions: SHORT48_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
