import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT56_CAPTIONS, SHORT56_TOTAL_SEC} from './short56_timing';

/**
 * SHORT #56 — Michael Morton / the prosecutor who hid the file (Texas, 1987-2013). PREMIUM tier.
 * Episode PD-2026-052-morton. Sensitivity: Morton is LIVING and fully EXONERATED — his innocence
 * is statable as fact. The child witness is handled via the crayon-drawing motif only: no attack
 * re-creation, no child face (hand only in S001, verified by eye). Christine Morton named once in
 * narration, with dignity; no violence depicted. Anderson facts are strictly of record.
 * Facts + ACCURACY LOCKS from the EP52 FACTS_LEDGER (all H-grade):
 *  - The boy told his grandmother a "monster" attacked his mom and daddy wasn't home.
 *  - Neighbors reported a green van behind the house; a bloody bandana was found near the scene
 *    (distance soft-cited — NOT stated).
 *  - Anderson deliberately suppressed all of it (verbatim of record: "the other side can't have
 *    access to those reports"). Morton convicted Feb 17, 1987 — LIFE.
 *  - Served NEARLY twenty-five years (keep the hedge — never a bare "25 years").
 *  - Bandana DNA named Mark Norwood, who murdered another woman while Morton was imprisoned.
 *  - Released Oct 4, 2011; exonerated Dec 19, 2011. Anderson: Nov 8, 2013 contempt — TEN DAYS in
 *    jail, law license surrendered. Never overstate his punishment beyond the record.
 * On-screen safe: "NEARLY 25 YEARS", "TEN DAYS IN JAIL". Lane accent evidence-blue #6B9BD1.
 */

const ACCENT = '#6B9BD1';
const img = (n: string) => `shorts/short56/short56_${n}.png`;
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
  // L1 — hook: the crayon monster under evidence-blue light; not his dad
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE MONSTER\nWAS REAL', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the truth already in the file: the van, the bandana
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'A GREEN VAN\nOUT BACK'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'A BLOODY\nBANDANA'},

  // L3 — the drawer slides shut; Morton gets life
  {line: 'L3', id: 'b2', src: img('04'), kind: 'image', motion: 'pushin', telop: 'HE HID\nALL OF IT'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'LIFE\nSENTENCE'},

  // L4 — the years, the DNA, the gate opening
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'parallax', telop: 'NEARLY 25\nYEARS'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'pushin', telop: 'DNA NAMED\nTHE KILLER'},
  {line: 'L4', id: 'c3', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'MORTON\nWALKED OUT'},

  // L5 — the prosecutor's ten days, then CTA over the drawer reopening on the drawing
  {line: 'L5', id: 'd1', src: img('09'), kind: 'image', motion: 'parallax', telop: 'TEN DAYS\nIN JAIL'},
  {line: 'L5', id: 'cta', src: img('10'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook drawing (last frame cuts back to first) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE MONSTER\nWAS REAL'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT56_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT56: ShortData = {
  shortId: 'short56',
  episodeId: 'PD-2026-052-morton',
  durationSec: SHORT56_TOTAL_SEC,
  narrationSrc: 'shorts/short56/audio/short56_final_mix_v002_en_us.mp3',
  captions: SHORT56_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
