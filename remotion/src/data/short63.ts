import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT63_CAPTIONS, SHORT63_TOTAL_SEC} from './short63_timing';

/**
 * SHORT #63 — "He voted not guilty. They handcuffed him in the jury box."
 * Episode PD-2026-054-flowers (Curtis Flowers, tried six times). Format lane F-B, "the number that
 * convicted him". Slate: episodes/_planning/SHORTS_SLATE_EP53-56.v001.md §3.
 *
 * FIRST SHORT IN THE SERIES WITH REAL MOTION: the hook and the loop tail are Wan-i2v clips
 * (kind:'video'), not a still under a zoom — the standing "animation feels thin" complaint.
 * Sensitivity: no identifiable person anywhere — backs, hands, silhouettes and objects only.
 * NO FACE PLATE. EP54's F07 ("lone holdout juror") is an illustrative white woman; James Bibbs is
 * a Black man, so putting that face on the beat that names him would have read as a portrait of
 * him. It was pulled after eyes-on QC and the beat now carries hands on the courtroom rail (10).
 * METHOD rule 7 is met here by real motion (the i2v hook and loop), not by a face.
 * ACCURACY LOCKS carried from EP54_flowers_FACTS_LEDGER.v001:
 *  - James Bibbs was charged with perjury and the charge was DROPPED — he was NEVER CONVICTED.
 *    The final content beat carries "CHARGE DROPPED / NEVER CONVICTED" as an on-screen lock telop
 *    and nothing in this cut may read as him having been punished.
 *  - Doug Evans is LIVING and was NEVER criminally charged or disciplined. He is named only as the
 *    prosecutor who pursued the case, which is what the record says.
 *  - Curtis Flowers is LIVING and FULLY CLEARED. The murders remain UNSOLVED — no alternative
 *    suspect is named or hinted anywhere in this cut.
 *  - Victim dignity: Bertha Tardy, Carmen Rigby, Robert Golden and Derrick "Bobo" Stewart are not
 *    depicted and the killings are not staged.
 * On-screen safe: "HE VOTED NOT GUILTY", "MISTRIAL", "CHARGED WITH PERJURY",
 * "CHARGE DROPPED / NEVER CONVICTED", "TRIED SIX TIMES".
 * Lane accent Mississippi gold #D2B15E (same lane as short58).
 *
 * Audio is hybrid: L3–L4 are cut from the episode's own vc_master_v001.mp3; L1, the L2 bridge (the
 * master's version of that beat leans on the running trial count, which this cut does not set up)
 * and L5 are re-recorded — episodes/PD-2026-054-flowers/09_package/short63_lines.v001.json.
 */

const ACCENT = '#D2B15E';
const img = (n: string) => `shorts/short63/short63_${n}.png`;
const clip = (n: string) => `shorts/short63/short63_${n}.mp4`;
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

// 23 cuts over 51.5 s => ~2.2 s per beat (METHOD rule 6), two of them real video. 20 distinct
// plates + 2 clips; only the hook clip repeats, and only as the loop tail.
const CUTS: Cut[] = [
  // L1 — hook: motion from frame 0. A juror's chair in a cold spotlight, a deputy's shadow entering.
  {line: 'L1', id: 'hook', src: clip('v01'), kind: 'video', motion: 'video',
   telop: 'HE VOTED\nNOT GUILTY', art: {kind: 'lightrays', color: ACCENT}},
  {line: 'L1', id: 'hook_b', src: img('01'), kind: 'image', motion: 'pushin', fast: true},
  {line: 'L1', id: 'hook_c', src: img('02'), kind: 'image', motion: 'parallax', fast: true},

  // L2 — trial five, 2008: the jury hangs on one holdout.
  {line: 'L2', id: 'b1', src: img('03'), kind: 'image', motion: 'parallax', telop: 'TRIAL FIVE.\n2008.'},
  {line: 'L2', id: 'b1b', src: clip('v02'), kind: 'video', motion: 'video'},
  {line: 'L2', id: 'b1c', src: img('21'), kind: 'image', motion: 'kenburns'},
  {line: 'L2', id: 'b1d', src: img('05'), kind: 'image', motion: 'pushin'},
  {line: 'L2', id: 'b1e', src: img('06'), kind: 'image', motion: 'parallax', telop: 'ONE HOLDOUT'},

  // L3 — the mistrial, and what the state did to the citizen it had summoned.
  {line: 'L3', id: 'b2', src: img('07'), kind: 'image', motion: 'parallax', telop: 'MISTRIAL'},
  {line: 'L3', id: 'b2b', src: img('08'), kind: 'image', motion: 'pushin'},
  {line: 'L3', id: 'b2c', src: img('09'), kind: 'image', motion: 'kenburns'},
  {line: 'L3', id: 'b2d', src: img('10'), kind: 'image', motion: 'pushin', telop: 'HANDCUFFED\nIN COURT'},
  {line: 'L3', id: 'b2e', src: img('11'), kind: 'image', motion: 'kenburns'},
  {line: 'L3', id: 'b2f', src: img('12'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'CHARGED WITH\nPERJURY'},

  // L4 — the attorney general takes it away and drops it; the message had already been broadcast.
  {line: 'L4', id: 'c1', src: img('13'), kind: 'image', motion: 'parallax', telop: 'THE STATE AG\nSTEPPED IN'},
  {line: 'L4', id: 'c1b', src: img('14'), kind: 'image', motion: 'pushin'},
  {line: 'L4', id: 'c1c', src: img('15'), kind: 'image', motion: 'kenburns', telop: 'TOOK THE CASE\nAWAY'},
  {line: 'L4', id: 'c1d', src: img('16'), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c1e', src: img('17'), kind: 'image', motion: 'kenburns'},
  // MANDATORY legal-lock telop. No citation art on this beat (the short19 defect: a telop covered
  // the middle of a legal disclaimer and inverted its meaning).
  {line: 'L4', id: 'c1f', src: img('18'), kind: 'image', motion: 'pushin',
   telop: 'CHARGE DROPPED\nNEVER CONVICTED'},

  // L5 — payoff + CTA.
  {line: 'L5', id: 'c2', src: img('19'), kind: 'image', motion: 'pushin', telop: 'TRIED\nSIX TIMES'},
  {line: 'L5', id: 'cta', src: img('20'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — back to the hook clip and hook telop (rule 5).
  {line: 'L5', id: 'loop', src: clip('v01'), kind: 'video', motion: 'video',
   telop: 'HE VOTED\nNOT GUILTY'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT63_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT63: ShortData = {
  shortId: 'short63',
  episodeId: 'PD-2026-054-flowers',
  durationSec: SHORT63_TOTAL_SEC,
  narrationSrc: 'shorts/short63/audio/short63_final_mix_v002_en_us.mp3',
  captions: SHORT63_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  ctaLongThumbSrc: 'shorts/short63/short63_ctathumb.png',
  ctaLongTitle: 'Tried Six Times for One Crime',
  ctaHeadline: 'FULL CASE',
  beats: buildBeats(),
};
