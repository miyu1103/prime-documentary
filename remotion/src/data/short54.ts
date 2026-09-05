import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT54_CAPTIONS, SHORT54_TOTAL_SEC} from './short54_timing';

/**
 * SHORT #54 — The Central Park Five / five false confessions (New York, 1989). PREMIUM tier.
 * Episode PD-2026-050-centralpark. R2 subject: the Exonerated Five are LIVING men and the case is
 * race-charged — ALL frames are empty rooms / empty chairs / abstract forensic light; zero human
 * figures, zero faces (verified by eye; the "five" are five empty chairs). The victim is never
 * depicted; the crime is never depicted; Reyes is described only as "a convicted murderer already
 * serving life" per the script's own framing — his name is NOT used in this short.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP50_centralpark_script.en.v001.md:
 *  - Ages 14/14/15/15/16 (ACT1 L45). Interrogated "for hours" — NO hard hour total on screen
 *    (DO-NOT-STATE list L17).
 *  - No physical evidence connecting any of them; no eyewitness placing them (ACT1 L53 / ACT2 L69).
 *  - Camera switched on only at the END — confessions recorded, never how they were made (L59/L91).
 *  - DNA from the scene matched NONE of the five; convicted anyway, 1990 trials (L63/L85/L107/L117).
 *  - 2002: the real attacker ("It was me. And I did it alone.") — DNA matched; ALL five convictions
 *    vacated Dec 19, 2002 (ACT5 L155-167, ACT6 L181). Telop quote kept to the verbatim "IT WAS ME."
 * On-screen safe: ages, "CONVICTED ANYWAY", "EVERY CONVICTION VACATED". Lane accent
 * interrogation-cyan #5FB8C9.
 */

const ACCENT = '#5FB8C9';
const img = (n: string) => `shorts/short54/short54_${n}.png`;
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
  // L1 — hook: one empty chair under harsh cyan light; five children confessed, none did it
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THEY ALL\nCONFESSED', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the roundup and the room: teenagers, nothing tying them, camera dark
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'parallax', telop: 'FOURTEEN.\nFIFTEEN. SIXTEEN.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'NO PHYSICAL\nEVIDENCE'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'THE CAMERA\nSTAYS OFF'},

  // L3 — the science said no; the verdict said yes
  {line: 'L3', id: 'b2', src: img('05'), kind: 'image', motion: 'parallax', telop: 'DNA MATCHED\nNONE OF THEM'},
  {line: 'L3', id: 'b2b', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'CONVICTED\nANYWAY'},

  // L4 — thirteen years later: the real confession, and every conviction falls
  {line: 'L4', id: 'c1', src: img('07'), kind: 'image', motion: 'pushin', telop: '"IT WAS\nME."'},
  {line: 'L4', id: 'c2', src: img('08'), kind: 'image', motion: 'parallax', telop: 'EVERY CONVICTION\nVACATED'},

  // L5 — payoff question + CTA over the quiet chair by the window
  {line: 'L5', id: 'cta', src: img('09'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook chair (last frame cuts back to first) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THEY ALL\nCONFESSED'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT54_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT54: ShortData = {
  shortId: 'short54',
  episodeId: 'PD-2026-050-centralpark',
  durationSec: SHORT54_TOTAL_SEC,
  narrationSrc: 'shorts/short54/audio/short54_final_mix_v002_en_us.mp3',
  captions: SHORT54_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
