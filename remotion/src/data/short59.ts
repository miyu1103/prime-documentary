import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT59_CAPTIONS, SHORT59_TOTAL_SEC} from './short59_timing';

/**
 * SHORT #59 — Jon Burge / the torture Chicago now teaches in school (1972-2015). PREMIUM tier.
 * Episode PD-2026-055-burge. Sensitivity: survivors are LIVING — torture is NEVER depicted
 * anywhere: the device is inert and alone on a table (verified by eye), no restrained person, no
 * distress face; no screams in sound design (ad-safety MEDIUM ceiling). No individual detective
 * named. Race handled soberly; the family beat is an empty hallway, no persons. Officers
 * Fahey/O'Brien out of scope for 60s.
 * Facts + ACCURACY LOCKS from the EP55 FACTS_LEDGER (episodes/_planning/EP55_burge_FACTS_LEDGER.v001.md):
 *  - "More than one hundred Black men" — keep the ledger hedge on the count (BU-05/07).
 *  - Methods stated as a clinical list from survivor accounts: hand-cranked box, two wires,
 *    electric shock, suffocation, mock executions (BU-06).
 *  - 1982: jail doctor's letter demanded, IN WRITING, an investigation of the brutality; it was
 *    forwarded to the top and NOTHING happened — no motive speculation (BU-10). Complaints fell on
 *    deaf ears for decades (BU-15).
 *  - NEVER say Burge was convicted of or punished for torture: the statute of limitations expired
 *    (BU-19); he was convicted only of lying about it under oath — perjury/obstruction over 2003
 *    sworn denials (BU-25/26); FOUR AND A HALF years exact (BU-28); kept his pension via a 4-4
 *    board deadlock until he died in 2018 (BU-29/35) — the deadlock detail stays off screen.
 *  - 2015: America's FIRST MUNICIPAL reparations for police violence (Amnesty's safe phrasing) +
 *    the story entered Chicago's 8th/10th-grade curriculum from 2018 (BU-31/33). NO vote card,
 *    no court tally exists for this story — none used.
 * On-screen safe: "TAUGHT IN SCHOOLS", "HE KEPT HIS PENSION". Lane accent sodium-amber #C98E3F.
 */

const ACCENT = '#C98E3F';
const img = (n: string) => `shorts/short59/short59_${n}.png`;
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
  // L1 — hook: the open schoolbook in warm morning light; why do they teach this?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'TAUGHT IN\nSCHOOLS', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the commander, the crew, the inert machine
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'COMMANDER\nJON BURGE'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'MORE THAN 100\nBLACK MEN'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'A BOX.\nTWO WIRES.'},

  // L3 — the 1982 letter, and the silence that answered it
  {line: 'L3', id: 'b2', src: img('06'), kind: 'image', motion: 'kenburns', telop: '1982.\nIN WRITING.'},
  {line: 'L3', id: 'b2b', src: img('07'), kind: 'image', motion: 'parallax', telop: 'NOTHING\nHAPPENED'},

  // L4 — decades of deaf ears; the clock runs out; the only crime left
  {line: 'L4', id: 'c1', src: img('05'), kind: 'image', motion: 'pushin', telop: 'DEAF EARS.\nFOR DECADES.'},
  {line: 'L4', id: 'c2', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'THE CLOCK\nRAN OUT'},
  {line: 'L4', id: 'c3', src: img('09'), kind: 'image', motion: 'parallax', telop: 'HE KEPT\nHIS PENSION'},

  // L5 — reparations + the schoolbook payoff; CTA plays over this
  {line: 'L5', id: 'cta', src: img('10'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — the same schoolbook frame as the hook (last frame cuts back to first) (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'TAUGHT IN\nSCHOOLS'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT59_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT59: ShortData = {
  shortId: 'short59',
  episodeId: 'PD-2026-055-burge',
  durationSec: SHORT59_TOTAL_SEC,
  narrationSrc: 'shorts/short59/audio/short59_final_mix_v002_en_us.mp3',
  captions: SHORT59_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
