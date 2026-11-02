import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT33_CAPTIONS, SHORT33_TOTAL_SEC} from './short33_timing';

/**
 * SHORT #33 — Tyler v. Hennepin County (home-equity theft). PREMIUM tier.
 * Spec: episodes/_planning/_short_spec_33_PREMIUM.md · facts: PD-2026-033-tyler §1 FACTS LOCKED.
 * WORDING LOCKS: Tyler v. Hennepin County, 598 U.S. 631 (2023), NINE to ZERO, Roberts wrote it.
 * Debt ~$15,000 (principal ~$2,300); condo SOLD for $40,000; county KEPT the whole $40,000; surplus
 * ~$25,000 taken. Holding = keeping the surplus is a TAKING w/o just compensation (5th Amendment); the
 * Court did NOT decide the 8th Amendment. Roberts quote verbatim (comma). "most states already required
 * return" — do NOT burn the number "36". "home equity theft" = critics' term. No real-person likeness.
 *
 * PREMIUM build: every still gets real DPT depth parallax (Root registers depth:true); the money/vote/
 * quote/year beats are motionkit SCENE arts (opaque, they replace the still for that beat).
 */

const img = (n: string) => `shorts/short33/short33_${n}.png`;
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
  // L1 — hook: the county kept ALL of it (seized home)
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THEY KEPT\nALL OF IT'},

  // L2 — the event: owed ~$15k, condo sold for $40k, county kept the entire amount incl. ~$25k surplus
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: '$15,000\nOWED'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 40000, prefix: '$', topLabel: 'THE COUNTY SOLD HER CONDO', label: 'and kept every dollar'}},
  {line: 'L2', id: 'b1c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.28, label: 'HOME · $40K'}, {x: 0.27, y: 0.60, label: 'DEBT · $15K'}, {x: 0.75, y: 0.60, label: 'KEPT · $25K'}],
     edges: [{from: 0, to: 1, weight: 2}, {from: 0, to: 2, weight: 3}]}},

  // L3 — the Constitution: 5th Amendment (take it → pay for it); the surplus was hers
  {line: 'L3', id: 'b2a', src: img('05'), kind: 'image', motion: 'parallax', telop: 'TAKE IT →\nPAY FOR IT'},
  {line: 'L3', id: 'b2b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'stack', title: 'THE $40,000 SALE',
     parts: [{label: 'THE TAX DEBT', value: 15}, {label: 'HER SURPLUS — KEPT', value: 25}]}},

  // L4 — the ruling: 2023, 9–0, Roberts, now the rule everywhere
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 2020, to: 2023, label: 'All the way to the Supreme Court'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 9, dissent: 0, label: 'TYLER v. HENNEPIN COUNTY'}},
  {line: 'L4', id: 'c3', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'quote', quote: "render unto Caesar what is Caesar's, but no more.", attribution: 'Chief Justice Roberts, 2023'}},
  {line: 'L4', id: 'c4', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'THE RULE\nEVERYWHERE'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT33_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT33: ShortData = {
  shortId: 'short33',
  episodeId: 'PD-2026-033-tyler',
  durationSec: SHORT33_TOTAL_SEC,
  narrationSrc: 'shorts/short33/audio/short33_final_mix_v002_en_us.mp3',
  captions: SHORT33_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
