import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT46_CAPTIONS, SHORT46_TOTAL_SEC} from './short46_timing';

/**
 * SHORT #46 — Vega v. Tekoh (2022) / a Miranda warning that was never read. PREMIUM tier.
 * EP44 tekoh (PD-2026-044-tekoh). R2: Terence Tekoh & Carlos Vega are living private persons —
 * NO face/likeness of anyone; symbols only (hospital corridor, pen & page, empty table, jury box,
 * colonnade, a closing door). Images reuse EP44 tekoh SDXL stills (H:/pd-media/assets/ai/tekoh/S*).
 *
 * WORDING LOCKS (every telop / caption / label below obeys these — do NOT loosen):
 *  1. DO NOT overstate the reach. Only ONE door closed: suing an officer for civil-damages under
 *     Section 1983 for the Miranda violation *by itself*. NEVER write / imply "Miranda is dead",
 *     "no right to remain silent", "police need not read rights", "Miranda overturned/struck down".
 *  2. The exclusion remedy SURVIVES — an unwarned statement can still be kept out of a criminal
 *     trial (Miranda 1966 + Dickerson 2000 stand, untouched). Keep the "closed door" and the
 *     "still-open door" together: a RIGHT is not the same as a civil PAYOUT.
 *  3. Vote 6-3 is accurate (Alito majority / Kagan, Breyer, Sotomayor dissent) — badge/votetally only.
 *  4. The underlying allegation is NEVER named or shown; Tekoh is framed only as a private person
 *     who was accused and then cleared. No face, no body, no readable document.
 */

const img = (n: string) => `shorts/short46/short46_${n}.png`;
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
  // L1 — hook: questioned with no warning; your own words on trial; can you make him pay?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO WARNING\nWAS READ', art: {kind: 'lightrays'}},

  // L2 — that night: the warning never came; his own written words; a jury cleared him
  {line: 'L2', id: 'b1', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'THE WARNING\nNEVER CAME'},
  {line: 'L2', id: 'b2', src: img('02'), kind: 'image', motion: 'parallax', telop: 'HIS OWN\nWORDS'},
  {line: 'L2', id: 'b3', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'A JURY\nCLEARED HIM'},

  // L3 — the turn: he sued for damages; twice he lost; appeals court agreed; then the Supreme Court
  {line: 'L3', id: 'c1', src: img('05'), kind: 'image', motion: 'pushin', telop: 'HE SUED\nFOR DAMAGES'},
  {line: 'L3', id: 'c2', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'HIS WORDS,\nAS EVIDENCE'},
  {line: 'L3', id: 'c3', src: img('07'), kind: 'image', motion: 'parallax', telop: 'THEN THE\nSUPREME COURT'},

  // L4 — the doctrine: 6-3; the missing warning alone is no lawsuit; BUT exclusion survives; right != payout
  {line: 'L4', id: 'd1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 6, dissent: 3, label: 'VEGA v. TEKOH · 2022'}},
  {line: 'L4', id: 'd2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.2, label: 'NO MIRANDA WARNING'}, {x: 0.28, y: 0.8, label: 'KEPT OUT OF TRIAL · STILL YOURS'}, {x: 0.72, y: 0.8, label: 'SUE FOR MONEY · CLOSED'}],
     edges: [{from: 0, to: 1, weight: 3}, {from: 0, to: 2, weight: 3}]}},
  {line: 'L4', id: 'd3', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'A RIGHT ≠\nA PAYOUT'},

  // L5 — CTA (return to the hospital corridor)
  {line: 'L5', id: 'cta', src: img('01'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'NO WARNING\nWAS READ'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT46_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT46: ShortData = {
  shortId: 'short46',
  episodeId: 'PD-2026-044-tekoh',
  durationSec: SHORT46_TOTAL_SEC,
  narrationSrc: 'shorts/short46/audio/short46_final_mix_v002_en_us.mp3',
  captions: SHORT46_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
