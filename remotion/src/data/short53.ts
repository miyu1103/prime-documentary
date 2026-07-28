import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT53_CAPTIONS, SHORT53_TOTAL_SEC} from './short53_timing';

/**
 * SHORT #53 — Caniglia v. Strom / the "community caretaking" home entry (2021). PREMIUM tier.
 * Episode PD-2026-043-caniglia. R2 subject: Mr. Caniglia is a LIVING private person — no face,
 * no likeness; objects and empty spaces carry the story. The "shoot me" remark is NEVER quoted
 * (script sensitivity lock); the awful night is symbolized by the handgun on the table only.
 * Facts + ACCURACY LOCKS from episodes/PD-2026-043-caniglia/03_script/script.en.v001.md:
 *  - Cranston, RI, 2015. Wife stayed at a hotel; called the NON-EMERGENCY line for a welfare check.
 *  - He was found alive/calm on his porch; agreed to a psych evaluation on the condition (HE SAYS —
 *    keep the hedge) that his guns be left alone. Officers entered after the ambulance left:
 *    NO warrant, NO emergency; took two handguns. Their label: "community caretaking".
 *  - HOLDING (2021): 9–0 — community caretaking does NOT justify warrantless HOME entry. State it
 *    narrowly: the caretaking EXCUSE is dead at the front door. NEVER say "police can never enter
 *    a home" (real emergencies/exigency still allow entry).
 * On-screen safe: "9–0", "CANIGLIA v. STROM · 2021". Lane accent porch-amber #C9A05B.
 */

const ACCENT = '#C9A05B';
const img = (n: string) => `shorts/short53/short53_${n}.png`;
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
  // L1 — hook: a welfare check that ends with the guns leaving the house
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'JUST A\nWELFARE CHECK', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the awful night and the morning after
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'SHE LEFT\nTHAT NIGHT'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'NO ANSWER\nBY MORNING'},

  // L3 — found alive, calm, on his own porch; one condition
  {line: 'L3', id: 'b2', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'ALIVE.\nCALM.'},

  // L4 — the entry: no warrant, no emergency; "caretaking"
  {line: 'L4', id: 'c1', src: img('05'), kind: 'image', motion: 'pushin', telop: 'NO WARRANT.\nNO EMERGENCY.'},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'parallax', telop: 'THEY CALLED IT\nCARETAKING'},

  // L5 — the 9-0 payoff + CTA
  {line: 'L5', id: 'c3', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 9, dissent: 0, label: 'CANIGLIA v. STROM · 2021'}},
  {line: 'L5', id: 'cta', src: img('08'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — the bare table with the faint mark mirrors the hook's gun-on-table (rule 5).
  {line: 'L5', id: 'loop', src: img('09'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'JUST A\nWELFARE CHECK'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT53_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT53: ShortData = {
  shortId: 'short53',
  episodeId: 'PD-2026-043-caniglia',
  durationSec: SHORT53_TOTAL_SEC,
  narrationSrc: 'shorts/short53/audio/short53_final_mix_v002_en_us.mp3',
  captions: SHORT53_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
