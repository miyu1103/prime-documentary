import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT60_CAPTIONS, SHORT60_TOTAL_SEC} from './short60_timing';

/**
 * SHORT #60 — "His confession didn't match the murder. So they fixed the confession."
 * Episode PD-2026-053-norfolk (The Norfolk Four). Format lane F-A, "the machine that manufactures
 * agreement". Slate: episodes/_planning/SHORTS_SLATE_EP53-56.v001.md §2.
 *
 * Sensitivity: all four exonerees are LIVING with ABSOLUTE PARDONS — innocence is stated as fact.
 * No identifiable person anywhere: backs, hands, silhouettes and objects only. Michelle Moore-Bosko
 * is named twice in the L3 narration (cut from the long-form master) and is never depicted; her
 * death is referred to only as "how Michelle died" — no wound detail, no assault language, and her
 * family is neither depicted nor referenced.
 * ACCURACY LOCKS carried from EP53_norfolk_FACTS_LEDGER.v001 (all H-grade):
 *  - The polygraph "failure" he was told about was FALSE, and telling it was LEGAL (NF-08/11).
 *    The hook states the rule; the body states the instance. Neither says he passed a test he
 *    was never truthfully scored on — only that what he was told was false.
 *  - His account did not match the crime; the statement was re-taken until it agreed with the
 *    crime scene (NF-11). This is the whole short.
 *  - Every DNA test excluded all the accused (NF-06/18/38) — the CTA line, not a visual claim.
 *  - Detective Ford is NOT mentioned: his federal sentence was for UNRELATED extortion and false
 *    statements, and nothing here may read as punishment for this case (NF-44).
 * On-screen safe: "POLICE MAY LIE TO YOU", "CONFESSION NUMBER ONE", "EVERY DNA TEST SAID NO".
 * Lane accent harbor steel-blue #7E93A8 (same lane as short57).
 *
 * Audio is hybrid: L2–L4 are cut from the episode's own vc_master_v001.mp3, L1 and L5 re-recorded.
 * L2 stops at a measured pause (277.10 s) because the rest of that chunk is the L1 hook verbatim —
 * see episodes/PD-2026-053-norfolk/09_package/short60_lines.v001.json.
 */

const ACCENT = '#7E93A8';
const img = (n: string) => `shorts/short60/short60_${n}.png`;
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

// 23 cuts over 50.2 s => ~2.1 s per beat, so a pattern interrupt lands inside every 2 s window
// (METHOD rule 6). 18 distinct plates; only the polygraph needle (hook/callback/loop), the machine
// and the file drawer repeat, each on a different motion and never in adjacent beats.
// Plates were chosen off a rendered contact sheet, not off the CODEX_A prompt list: three plates
// whose file numbers did not match their prompt (an abstract card, a cup-and-ashtray, an empty
// floor) were swapped for what is actually on disk — 07 folder+page, 16 DNA gel, 18 four tallies.
const CUTS: Cut[] = [
  // L1 — hook: the rule itself. Needle mid-swing from frame 0.
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'POLICE MAY\nLIE TO YOU', art: {kind: 'lightrays', color: ACCENT}},
  {line: 'L1', id: 'hook_b', src: img('02'), kind: 'image', motion: 'parallax', fast: true},
  {line: 'L1', id: 'hook_c', src: img('03'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THAT WAS\nA LIE'},

  // L2 — the overnight room: the lie is told, and it is legal.
  {line: 'L2', id: 'b1', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'MIDDLE OF\nTHE NIGHT'},
  {line: 'L2', id: 'b1b', src: img('05'), kind: 'image', motion: 'parallax'},
  {line: 'L2', id: 'b1c', src: img('06'), kind: 'image', motion: 'pushin'},
  {line: 'L2', id: 'b1d', src: img('13'), kind: 'image', motion: 'kenburns'},
  {line: 'L2', id: 'b1e', src: img('08'), kind: 'image', motion: 'parallax', telop: 'PERFECTLY\nLEGAL'},

  // L3 — the detail that should have ended it: he got the murder wrong.
  {line: 'L3', id: 'b2', src: img('09'), kind: 'image', motion: 'pushin', telop: 'HE GOT IT\nWRONG'},
  {line: 'L3', id: 'b2b', src: img('10'), kind: 'image', motion: 'parallax'},
  {line: 'L3', id: 'b2c', src: img('21'), kind: 'image', motion: 'kenburns'},
  {line: 'L3', id: 'b2d', src: img('07'), kind: 'image', motion: 'pushin'},
  {line: 'L3', id: 'b2e', src: img('12'), kind: 'image', motion: 'parallax'},
  {line: 'L3', id: 'b2f', src: img('01'), kind: 'image', motion: 'kenburns', telop: 'THE DETAILS\nWERE WRONG'},

  // L4 — the repair: taken again, and again, until it agreed with the crime scene.
  {line: 'L4', id: 'c1', src: img('11'), kind: 'image', motion: 'pushin', telop: 'SO THEY FIXED\nTHE CONFESSION'},
  {line: 'L4', id: 'c1b', src: img('03'), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c1c', src: img('14'), kind: 'image', motion: 'kenburns'},
  {line: 'L4', id: 'c1d', src: img('02'), kind: 'image', motion: 'pushin'},
  {line: 'L4', id: 'c1e', src: img('21'), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c1f', src: img('15'), kind: 'image', motion: 'pushin', telop: 'CONFESSION\nNUMBER ONE'},

  // L5 — payoff + CTA. No citation art on these beats (the short19 defect).
  {line: 'L5', id: 'c2', src: img('16'), kind: 'image', motion: 'kenburns', telop: 'EVERY DNA TEST\nSAID NO'},
  {line: 'L5', id: 'cta', src: img('18'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — back to the hook plate and hook telop so the last frame cuts to the first (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'POLICE MAY\nLIE TO YOU'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT60_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT60: ShortData = {
  shortId: 'short60',
  episodeId: 'PD-2026-053-norfolk',
  durationSec: SHORT60_TOTAL_SEC,
  narrationSrc: 'shorts/short60/audio/short60_final_mix_v002_en_us.mp3',
  captions: SHORT60_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  ctaLongThumbSrc: 'shorts/short60/short60_ctathumb.png',
  ctaLongTitle: 'Four Sailors. Four Confessions.',
  ctaHeadline: 'FULL CASE',
  beats: buildBeats(),
};
