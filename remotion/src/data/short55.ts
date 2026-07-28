import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT55_CAPTIONS, SHORT55_TOTAL_SEC} from './short55_timing';

/**
 * SHORT #55 — Cameron Todd Willingham / the fire that may never have been a crime (Texas, 2004).
 * PREMIUM tier. Episode PD-2026-051-willingham. Sensitivity: Willingham was EXECUTED in 2004 —
 * respectful treatment throughout. Children are NEVER depicted (house/yard exteriors only, per the
 * script restraint rule). Human figures are anonymous back-views only, no faces (verified by eye).
 * The execution is shown only as an EMPTY gurney chamber, no person.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP51_willingham_script.en.v001.md + FACTS_LEDGER:
 *  - Dec 1991, Corsicana TX; he ran out screaming his three girls were inside; neighbors held him
 *    back (COLD OPEN L10, ACT I L20-22).
 *  - Investigators cited pour patterns / crazed glass / roughly TWENTY indicators of arson —
 *    always framed as what THEY said the ashes proved (ACT I L26, ACT II L40-42).
 *  - Plea offered (plead guilty, live); he REFUSED (ACT II L50). Jailhouse informant claim (L46-48).
 *  - Hurst report warned the state IN WRITING before the execution (ACT III L64-76). Executed
 *    anyway, Feb 17, 2004, Huntsville (L78-80).
 *  - VERBATIM (quoted, attributed): Beyler 2009 — "a finding of arson could not be sustained"
 *    (L86-88). Five experts: none of the science was valid (L92).
 *  - HARD FRAME: NEVER claim exoneration. Payoff hedged exactly — the fire MAY never have been a
 *    crime at all (COLD OPEN L10, ENDING L102-104). Hook stays a question: "NO CRIME?"
 * Lane accent ember-orange #D9884A.
 */

const ACCENT = '#D9884A';
const img = (n: string) => `shorts/short55/short55_${n}.png`;
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
  // L1 — hook: the burning house at night; Texas decided he set the fire
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO\nCRIME?', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the yard, the ashes, the indicators the state said it could read
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NEIGHBORS HELD\nHIM BACK'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'THEY READ\nTHE ASHES'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'CRAZED GLASS.\nPOUR PATTERNS.'},

  // L3 — the informant, and the deal he would not take
  {line: 'L3', id: 'b2', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'AN INFORMANT\nSWEARS'},
  {line: 'L3', id: 'b2b', src: img('06'), kind: 'image', motion: 'parallax', telop: 'HE\nREFUSES'},

  // L4 — the written warning, the execution, the verdict on the science
  {line: 'L4', id: 'c1', src: img('07'), kind: 'image', motion: 'pushin', telop: 'WARNED.\nIN WRITING.'},
  {line: 'L4', id: 'c2', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'EXECUTED\nANYWAY'},
  {line: 'L4', id: 'c3', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote',
     quote: 'A finding of arson could not be sustained.',
     attribution: 'Craig Beyler, the state-hired fire expert, 2009'}},

  // L5 — the quiet dawn yard; the hedged payoff + CTA play over this
  {line: 'L5', id: 'cta', src: img('10'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook house (last frame cuts back to first) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO\nCRIME?'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT55_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT55: ShortData = {
  shortId: 'short55',
  episodeId: 'PD-2026-051-willingham',
  durationSec: SHORT55_TOTAL_SEC,
  narrationSrc: 'shorts/short55/audio/short55_final_mix_v002_en_us.mp3',
  captions: SHORT55_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
