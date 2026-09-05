import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT66_CAPTIONS, SHORT66_TOTAL_SEC} from './short66_timing';

/**
 * SHORT #66 — "A jail doctor put police torture in writing in 1982. The letter was buried."
 * Episode PD-2026-055-burge (Jon Burge / Area 2, Chicago). Format lane F-C, "they knew, and
 * nothing happened". Slate: episodes/_planning/SHORTS_SLATE_EP53-56.v001.md §4.
 *
 * Sensitivity: torture is described clinically and never staged or depicted. No identifiable
 * person anywhere — coats, hands, backs, silhouettes and objects only; the one face plate (F003)
 * is an illustrative, non-real stand-in.
 * ACCURACY LOCKS carried from EP55_burge_FACTS_LEDGER.v001:
 *  - Burge is DEAD and stands convicted of PERJURY + OBSTRUCTION ONLY. He was NEVER CHARGED WITH
 *    TORTURE. The closing beat carries that as an on-screen lock telop and the CTA line says it
 *    aloud — nothing in this cut may blur the two.
 *  - The 1982 letter, the chain of command and the silence are the documented spine of the cold
 *    open; the 2010 federal trial is where that same page returned as an exhibit.
 *  - Claimants other than the four 2003 pardonees carry the official torture FINDING, not blanket
 *    innocence — this cut makes no innocence claim about anyone.
 * On-screen safe: "FEBRUARY 1982", "NO ANSWER", "2010", "NEVER CHARGED WITH TORTURE".
 * Lane accent Chicago amber #C98E3F (same lane as short59).
 *
 * Audio is hybrid and unusually cheap: L1–L4 are ALL cut from the episode's own vc_master_v001.mp3
 * (the long-form cold open already opens on a person + an irreversible event inside 8 s, so it is
 * its own hook), and only the CTA is re-recorded. L4 drops VC-0224 so the payoff lands on
 * "The letter." — see episodes/PD-2026-055-burge/09_package/short66_lines.v001.json.
 */

const ACCENT = '#C98E3F';
const img = (n: string) => `shorts/short66/short66_${n}.png`;
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

// 24 cuts over 52.1 s => ~2.1 s per beat (METHOD rule 6). 23 distinct plates — only the hook plate
// repeats, and only as the loop tail.
const CUTS: Cut[] = [
  // L1 — hook: the doctor, the night, the injuries he could not explain away.
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'FEBRUARY 1982', art: {kind: 'lightrays', color: ACCENT}},
  {line: 'L1', id: 'hook_b', src: img('02'), kind: 'image', motion: 'parallax', fast: true},
  {line: 'L1', id: 'hook_c', src: img('03'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'INJURIES HE\nCOULD NOT EXPLAIN'},
  {line: 'L1', id: 'hook_d', src: img('04'), kind: 'image', motion: 'kenburns'},

  // L2 — he does the one thing a doctor is supposed to do: he writes it down.
  {line: 'L2', id: 'b1', src: img('05'), kind: 'image', motion: 'parallax'},
  {line: 'L2', id: 'b1b', src: img('06'), kind: 'image', motion: 'pushin', telop: 'HE WROTE IT\nDOWN'},
  {line: 'L2', id: 'b1c', src: img('07'), kind: 'image', motion: 'kenburns'},
  {line: 'L2', id: 'b1d', src: img('08'), kind: 'image', motion: 'pushin'},
  {line: 'L2', id: 'b1e', src: img('09'), kind: 'image', motion: 'parallax'},
  {line: 'L2', id: 'b1f', src: img('10'), kind: 'image', motion: 'kenburns', telop: 'UP THE\nCHAIN'},

  // L3 — the burial: it lands on the desk of a powerful man and dies there.
  {line: 'L3', id: 'b2', src: img('11'), kind: 'image', motion: 'pushin'},
  {line: 'L3', id: 'b2b', src: img('12'), kind: 'image', motion: 'kenburns'},
  {line: 'L3', id: 'b2c', src: img('13'), kind: 'image', motion: 'parallax', telop: 'IT LANDED\nON HIS DESK'},
  {line: 'L3', id: 'b2d', src: img('14'), kind: 'image', motion: 'pushin', telop: 'NO ANSWER'},
  {line: 'L3', id: 'b2e', src: img('15'), kind: 'image', motion: 'pushin'},
  {line: 'L3', id: 'b2f', src: img('16'), kind: 'image', motion: 'kenburns', telop: 'NOTHING'},

  // L4 — payoff: twenty-eight years later the same page is carried in as an exhibit.
  {line: 'L4', id: 'c1', src: img('17'), kind: 'image', motion: 'parallax', telop: '2010'},
  {line: 'L4', id: 'c1b', src: img('18'), kind: 'image', motion: 'pushin'},
  {line: 'L4', id: 'c1c', src: img('19'), kind: 'image', motion: 'kenburns', telop: 'THE MEDICAL\nRECORDS'},
  {line: 'L4', id: 'c1d', src: img('20'), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c1e', src: img('21'), kind: 'image', motion: 'pushin', fast: true, telop: 'THE LETTER'},

  // L5 — the legal lock, then the CTA. No citation art on the lock beat (the short19 defect).
  {line: 'L5', id: 'c2', src: img('22'), kind: 'image', motion: 'kenburns',
   telop: 'NEVER CHARGED\nWITH TORTURE'},
  {line: 'L5', id: 'cta', src: img('23'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — back to the coat on the infirmary door (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'FEBRUARY 1982'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT66_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT66: ShortData = {
  shortId: 'short66',
  episodeId: 'PD-2026-055-burge',
  durationSec: SHORT66_TOTAL_SEC,
  narrationSrc: 'shorts/short66/audio/short66_final_mix_v002_en_us.mp3',
  captions: SHORT66_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  ctaLongThumbSrc: 'shorts/short66/short66_ctathumb.png',
  ctaLongTitle: 'They Buried the Letter',
  ctaHeadline: 'FULL CASE',
  beats: buildBeats(),
};
