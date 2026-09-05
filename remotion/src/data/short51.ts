import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT51_CAPTIONS, SHORT51_TOTAL_SEC} from './short51_timing';

/**
 * SHORT #51 — Utah v. Strieff / an illegal stop, a warrant, and attenuation. PREMIUM tier.
 * Episode PD-2026-049-strieff. R2 subject: Edward Strieff is a living person convicted of a drug
 * offense after this case — no face, no likeness; symbols only (parking lot, ID/radio, chain,
 * handcuffs, columns). Drug reference kept minimal and clinical.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP49_strieff_script.en.v001.md (事実対応表 S00–S19):
 *  - The stop WAS ILLEGAL. Utah CONCEDED there was no reasonable suspicion; the Court agreed. NEVER
 *    say the stop was legal. (BLOCKER 1)
 *  - Evidence is admissible ONLY because the pre-existing warrant ATTENUATED the chain — the
 *    exclusionary rule normally suppresses; attenuation is the exception. Three factors: time /
 *    intervening warrant / flagrancy. Do NOT say the exclusionary rule was abolished. (BLOCKER 2)
 *  - 5-3, Scalia's seat vacant. Thomas majority; Sotomayor + Kagan dissents. Sotomayor "carceral
 *    state" line quoted VERBATIM, attributed to the DISSENT. Never use "we are all harmed". (BLOCKER 3/4)
 * On-screen safe: 5-3, "UTAH v. STRIEFF · 2016". Lane accent plum #9C6BAA.
 */

const ACCENT = '#9C6BAA';
const img = (n: string) => `shorts/short51/short51_${n}.png`;
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
  // L1 — hook: a stop with no reason, a name run, an old warrant, a search; can it all be used?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO REASON\nTO STOP', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the exclusionary rule: illegal search → evidence normally tossed; Utah conceded the stop was illegal
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'AN ILLEGAL\nSTOP'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'cititle', title: 'THE EXCLUSIONARY\nRULE', subtitle: 'illegal search. evidence tossed.'}},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'ARRESTED\nANYWAY'},

  // L3 — attenuation: the warrant found mid-stop; three-factor test (time / warrant / flagrancy)
  {line: 'L3', id: 'b2', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'ONE\nTHINNED LINK'},
  {line: 'L3', id: 'b2b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'diagram', steps: ['TIME', 'THE WARRANT', 'FLAGRANCY']}},
  {line: 'L3', id: 'b2c', src: img('05'), kind: 'image', motion: 'pushin', telop: 'BREAK THE\nCHAIN?'},

  // L4 — the payoff: 5-3, evidence stays, stop STILL illegal; Sotomayor "carceral state" dissent
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 5, dissent: 3, label: 'UTAH v. STRIEFF · 2016'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote',
     quote: 'You are not a citizen of a democracy but the subject of a carceral state, just waiting to be cataloged.',
     attribution: 'Justice Sotomayor, dissenting'}},
  {line: 'L4', id: 'c3', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'STILL AN\nILLEGAL STOP'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('06'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO REASON\nTO STOP'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT51_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT51: ShortData = {
  shortId: 'short51',
  episodeId: 'PD-2026-049-strieff',
  durationSec: SHORT51_TOTAL_SEC,
  narrationSrc: 'shorts/short51/audio/short51_final_mix_v002_en_us.mp3',
  captions: SHORT51_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
