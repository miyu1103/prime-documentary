import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT49_CAPTIONS, SHORT49_TOTAL_SEC} from './short49_timing';

/**
 * SHORT #49 — Atwater v. City of Lago Vista / a custodial arrest for a fine-only offense. PREMIUM tier.
 * Episode PD-2026-047-atwater. R2 subject: Gail Atwater is a living private person, non-convicted —
 * no face, no likeness; symbols only (road, seatbelt, handcuffs, cell, columns). Children symbolic /
 * non-sensational (empty child seats), never lingered on.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP47_atwater_script.en.v001.md (事実対応表 A01–A19):
 *  - HOLDING: the Court UPHELD the arrest, 5-4 (2001). A full custodial arrest for a fine-only
 *    offense is CONSTITUTIONAL. "The police COULD do this." NEVER "illegal" / "unconstitutional" /
 *    "struck down". The provocation is that it was ALLOWED. (BLOCKER)
 *  - Souter majority called it a "pointless indignity" yet permitted it; the fix is LEGISLATIVE.
 *  - O'Connor wrote the dissent (joined by three); her line is quoted verbatim, attributed to the
 *    DISSENT. Vote 5-4, neutral attribution. No invented quotes.
 * On-screen safe: $50 (max fine), 5-4, "ATWATER v. LAGO VISTA · 2001". Lane accent violet #7A5CD0.
 */

const ACCENT = '#7A5CD0';
const img = (n: string) => `shorts/short49/short49_${n}.png`;
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
  // L1 — hook: a Texas road, an unbuckled seatbelt; jail over a $50 fine?
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'OVER A\nSEATBELT?', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the arrest: not a ticket, handcuffs; kids left at the road; $50 was the whole penalty; booked
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'NOT A TICKET.\nCUFFS.'},
  {line: 'L2', id: 'b1b', src: img('04'), kind: 'image', motion: 'parallax', telop: 'KIDS LEFT\nAT THE ROAD'},
  {line: 'L2', id: 'b1c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 50, prefix: '$', topLabel: 'THE ENTIRE PENALTY', label: 'a fine-only offense · no jail'}},
  {line: 'L2', id: 'b1d', src: img('03'), kind: 'image', motion: 'pushin', telop: 'BOOKED\nAND CAGED'},

  // L3 — the suit: probable cause was undisputed; is that alone enough for a cell?
  {line: 'L3', id: 'b2a', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'IS CAUSE\nENOUGH?'},

  // L4 — the payoff: 5-4 UPHELD, constitutional, police could do this; O'Connor dissent
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 5, dissent: 4, label: 'ATWATER v. LAGO VISTA · 2001'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote',
     quote: 'It cloaks the pointless indignity that Gail Atwater suffered with the mantle of reasonableness.',
     attribution: 'Justice O’Connor, dissenting'}},
  {line: 'L4', id: 'c3', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'THE POLICE\nCAN DO THIS'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('06'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'OVER A\nSEATBELT?'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT49_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT49: ShortData = {
  shortId: 'short49',
  episodeId: 'PD-2026-047-atwater',
  durationSec: SHORT49_TOTAL_SEC,
  narrationSrc: 'shorts/short49/audio/short49_final_mix_v002_en_us.mp3',
  captions: SHORT49_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
