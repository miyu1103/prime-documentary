import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT52_CAPTIONS, SHORT52_TOTAL_SEC} from './short52_timing';

/**
 * SHORT #52 — Anjanette Young / the wrong-house raid (Chicago, 2019). PREMIUM tier.
 * Episode PD-2026-042-young. R2 subject: Ms. Young is a LIVING private person and the case is
 * race-charged — NO faces, NO bodies anywhere; symbols and cast shadows only (all stills verified
 * by eye). Never depict her state of undress; that fact is narrated with dignity, not shown.
 * Facts + ACCURACY LOCKS from episodes/_planning/EP42_young_script.en.v001.md (claims C11–C20):
 *  - The warrant was REAL (judge-signed); the TIP behind it was wrong. Never say "fake warrant".
 *  - The man sought lived elsewhere with a court-ordered ANKLE MONITOR — location known. (C15/C16)
 *  - The city FOUGHT release of the bodycam video; a CBS station aired it (Dec 2020). (C17)
 *  - Settlement $2.9M — but NO court ever ruled an officer violated her rights; the money admitted
 *    NOTHING. Never say "found liable" / "court ruled against the city". (C19/C20)
 * On-screen safe: "$2.9 MILLION", "WRONG HOUSE". Lane accent cold police-cyan #6FA8C9.
 */

const ACCENT = '#6FA8C9';
const img = (n: string) => `shorts/short52/short52_${n}.png`;
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
  // L1 — hook: twelve rifles, the wrong door, being right won't save her
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WRONG\nHOUSE', art: {kind: 'lightrays', color: ACCENT}},

  // L2 — the raid fills her home; she repeats the truth and it changes nothing
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'parallax', telop: 'SHIFT OVER.\nDOOR GONE.'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'kenburns', telop: 'RIFLES IN\nHER HOME'},
  {line: 'L2', id: 'b1c', src: img('04'), kind: 'image', motion: 'pushin', telop: 'AGAIN AND\nAGAIN: WRONG'},

  // L3 — the tip was wrong and the truth was on a screen the whole time
  {line: 'L3', id: 'b2', src: img('05'), kind: 'image', motion: 'parallax', telop: 'HE WAS ON\nA SCREEN'},

  // L4 — the camera saw it all; the city hid the tape; then paid
  {line: 'L4', id: 'c1', src: img('06'), kind: 'image', motion: 'pushin', telop: 'ALL ON\nCAMERA'},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'THEY HID\nTHE TAPE'},
  {line: 'L4', id: 'c3', src: img('08'), kind: 'image', motion: 'parallax', telop: '$2.9\nMILLION'},

  // L5 — payoff + CTA over the quiet door
  {line: 'L5', id: 'cta', src: img('09'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook door (last frame cuts back to first) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'WRONG\nHOUSE'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT52_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT52: ShortData = {
  shortId: 'short52',
  episodeId: 'PD-2026-042-young',
  durationSec: SHORT52_TOTAL_SEC,
  narrationSrc: 'shorts/short52/audio/short52_final_mix_v002_en_us.mp3',
  captions: SHORT52_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  beats: buildBeats(),
};
