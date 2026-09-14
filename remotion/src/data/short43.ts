import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT43_CAPTIONS, SHORT43_TOTAL_SEC} from './short43_timing';

/**
 * SHORT #43 — Connick v. Thompson / prosecutors hid exculpatory blood evidence. PREMIUM tier.
 * R2. No real-person likeness (John Thompson, prosecutors, justices) — silhouette / symbolic only.
 * Spec: episodes/_planning/_short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-041-thompson ledger.
 * WORDING LOCKS: John Thompson was on death row for a New Orleans murder. Prosecutors also had him for a
 * robbery, and the robber's blood was TYPE B; Thompson's blood is TYPE O — it was NEVER his. The crime lab
 * report existed and sat in a file; it was HIDDEN for FOURTEEN years and never given to the defense (a Brady
 * violation). 14 years on DEATH ROW, 18 years behind bars in all. A dying prosecutor (Deegan) admitted he
 * buried the blood evidence; an investigator found the report weeks before the execution. 2003 RETRIAL =
 * NOT GUILTY (minutes). He sued the Orleans Parish DA's office (failure-to-train) and a jury awarded
 * $14 MILLION. Connick v. Thompson, 563 U.S. 51 (2011): decided March 29, 2011, FIVE TO FOUR, the Supreme
 * Court REVERSED — every dollar gone, he was paid NOTHING. Thomas wrote the majority; Ginsburg dissented.
 * Grade-A on-screen: $14 MILLION, 5–4, TYPE B / TYPE O, 14 YEARS. Founded Resurrection After Exoneration; died 2017.
 */

const img = (n: string) => `shorts/short43/short43_${n}.png`;
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
  // L1 — hook: one hidden page proved the blood was not his
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HIDDEN FOR\n14 YEARS', art: {kind: 'lightrays'}},

  // L2 — the secret: death row for a murder; blood type B vs his O; the lab knew, defense never told
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'DEATH ROW\nFOR A LIE'},
  {line: 'L2', id: 'b1b', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.2, label: 'THE BLOOD · TYPE B'}, {x: 0.5, y: 0.52, label: 'THOMPSON · TYPE O'}, {x: 0.5, y: 0.84, label: 'NOT HIS'}],
     edges: [{from: 0, to: 2, weight: 3}, {from: 1, to: 2, weight: 3}]}},
  {line: 'L2', id: 'b1c', src: img('03'), kind: 'image', motion: 'parallax', telop: 'THE LAB\nKNEW'},

  // L3 — the wait: 14 years on death row; a dying confession; retrial = not guilty
  {line: 'L3', id: 'b2a', src: img('04'), kind: 'image', motion: 'kenburns', telop: 'FOURTEEN\nYEARS'},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'parallax', telop: 'RETRIAL:\nNOT GUILTY'},

  // L4 — the verdict: $14M won, then 5-4 reversed, paid nothing
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 14000000, prefix: '$', topLabel: 'A JURY AWARDED HIM', label: 'for eighteen stolen years'}},
  {line: 'L4', id: 'c2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 5, dissent: 4, label: 'CONNICK v. THOMPSON · REVERSED'}},
  {line: 'L4', id: 'c3', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'PAID\nNOTHING'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HIDDEN FOR\n14 YEARS'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT43_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT43: ShortData = {
  shortId: 'short43',
  episodeId: 'PD-2026-041-thompson',
  durationSec: SHORT43_TOTAL_SEC,
  narrationSrc: 'shorts/short43/audio/short43_final_mix_v002_en_us.mp3',
  captions: SHORT43_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
