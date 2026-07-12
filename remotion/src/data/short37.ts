import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT37_CAPTIONS, SHORT37_TOTAL_SEC} from './short37_timing';

/**
 * SHORT #37 — Mapp v. Ohio (1961). Loop-designed (last line echoes the hook).
 * Facts: evidence from an illegal search is inadmissible in state courts (exclusionary rule applied to states).
 * WORDING LOCKS: officers entered Dollree Mapp's home claiming a warrant; before this, illegally seized
 * evidence could still convict; 1961 Supreme Court, decision 6-3; illegal-search evidence can't be used in
 * any state. No real-person likeness; no invented quotes.
 */

const img = (n: string) => `shorts/short37/short37_${n}.png`;
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

// NOTE on length: ~35s, deliberately shorter than the 55-62s premium band. Rationale
// (retention data 2026-07-13): loop-closed shorts around 40s out-retain longer ones (the
// winning short08 was watched ~2.5x). Cut density kept high so nothing sits still. Documented deviation.
const CUTS: Cut[] = [
  // L1 — hook: forced in with a warrant that didn't exist, searched everything
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'A WARRANT\nTHAT DIDN’T EXIST', art: {kind: 'lightrays'}},
  {line: 'L1', id: 'h2', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'SEARCHED\nEVERYTHING'},

  // L2 — for most of history, illegal evidence still convicted you
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'parallax', telop: 'ILLEGAL\nSEARCH'},
  {line: 'L2', id: 'b2', src: img('03'), kind: 'image', motion: 'pushin', telop: 'STILL\nCOUNTED'},

  // L3 — they pushed into Mapp's home waving a fake paper, searched the house
  {line: 'L3', id: 'c1', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'THEY\nBROKE IN'},
  {line: 'L3', id: 'c2', src: img('04'), kind: 'image', motion: 'pushin', telop: 'A FAKE\nPAPER'},

  // L4 — the turn: 1961, 6-3, illegal-search evidence can't be used in any state
  {line: 'L4', id: 'd1', src: img('05'), kind: 'image', motion: 'kenburns', telop: '1961'},
  {line: 'L4', id: 'd2', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 6, dissent: 3, label: 'THE SUPREME COURT'}},
  {line: 'L4', id: 'd3', src: img('08'), kind: 'image', motion: 'kenburns', telop: 'IN ANY\nSTATE'},
  {line: 'L4', id: 'd4', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'THROWN\nOUT'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT37_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT37: ShortData = {
  shortId: 'short37',
  episodeId: 'PD-2026-003-mapp',
  durationSec: SHORT37_TOTAL_SEC,
  narrationSrc: 'shorts/short37/audio/short37_final_mix_v002_en_us.mp3',
  captions: SHORT37_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
