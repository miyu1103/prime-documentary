import type {ShortArt, ShortBeat, ShortData, ShortLayer} from '../compositions/Short';
import {LINE_WINDOWS, SHORT06_CAPTIONS, SHORT06_TOTAL_SEC} from './short06_timing';

/**
 * SHORT #6 — Terry v. Ohio ("Stopped & frisked without an arrest"). US-market English.
 * Source of truth: episodes/_planning/SHORTS_EP1-8.md (SHORT #6) + SHORTS_MOTION_DESIGN.md.
 *
 * SHARPNESS RULE: heroes are the 4K SDXL stills (shorts/short06/short06_01..07.png) so every focal
 * frame is crisp. Factory clips (all 1080p landscape) are used ONLY as screen-blended LIGHT overlays
 * (police strobe / light leak / dust / smoke) — diffuse light where upscaling softness is invisible —
 * never as full-frame heroes (that was the source of the soft/blurry footage). Pexels License.
 *
 * NARRATION-DRIVEN: cuts laid against the real EN narration windows (short06_timing.ts). Audio = the
 * en_us 4-layer mix. Same footage for YouTube and TikTok; only the CTA differs. Neutral; no real
 * person (faces in shadow/symbolic). Terry was 8–1.
 */

const img = (n: string) => `shorts/short06/short06_${n}.png`;
const fac = (f: string) => `shorts/short06/factory/${f}`;
const r3 = (n: number) => Math.round(n * 1000) / 1000;

// factory LIGHT overlays only (diffuse; sharpness-independent)
const F = {
  strobe: 'AF-LIGHT-3004__police_strobe_red_and_blue.mp4',
  leak: 'AF-LIGHT-0057__light_leak_overlay.mp4',
  leak2: 'AF-LIGHT-0058__light_leak_overlay.mp4',
  dust: 'AF-PART-0049__dust_particles_floating.mp4',
  smoke: 'AF-VFX-0056__smoke_on_black_background.mp4',
} as const;

const strobe = (opacity = 0.3): ShortLayer => ({src: fac(F.strobe), blend: 'screen', opacity});
const leak = (opacity = 0.36): ShortLayer => ({src: fac(F.leak), blend: 'screen', opacity});
const leakB = (opacity = 0.34): ShortLayer => ({src: fac(F.leak2), blend: 'screen', opacity});
const dust = (opacity = 0.3): ShortLayer => ({src: fac(F.dust), blend: 'screen', opacity});
const smoke = (opacity = 0.46): ShortLayer => ({src: fac(F.smoke), blend: 'screen', opacity});

type Cut = {
  line: string;
  id: string;
  src: string | null;
  kind: 'image' | 'video' | 'card';
  motion: ShortBeat['motion'];
  telop?: string;
  fast?: boolean;
  art?: ShortArt;
  overlays?: ShortLayer[];
};

// Visual cuts grouped by narration line (L1..L5). Within a line they split the time evenly.
const CUTS: Cut[] = [
  // L1 — hook: "police can stop you and pat you down without arresting you"
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'STOPPED &\nFRISKED?', overlays: [strobe(0.36), leak(0.3)]},
  {line: 'L1', id: 'h2', src: img('05'), kind: 'image', motion: 'pushin', fast: true,
   overlays: [strobe(0.26)]},

  // L2 — "no warrant, no proof; just reasonable suspicion, a bit more than a hunch"
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns',
   telop: 'NO WARRANT\nNEEDED', overlays: [leak(0.34)]},
  {line: 'L2', id: 'b2', src: img('03'), kind: 'image', motion: 'pushin',
   telop: 'JUST "REASONABLE\nSUSPICION"',
   art: {kind: 'diagram', steps: ['A hunch', 'Reasonable suspicion', 'Real proof']}},

  // L3 — 1968 story: two men casing a store -> frisk -> a gun
  {line: 'L3', id: 's1', src: img('05'), kind: 'image', motion: 'kenburns',
   telop: '1968', overlays: [dust(0.28)]},
  {line: 'L3', id: 's2', src: img('04'), kind: 'image', motion: 'pushin',
   telop: 'CASING\nA STORE'},
  {line: 'L3', id: 's3', src: img('06'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'HE FOUND\nA GUN', overlays: [smoke(0.5)]},

  // L4 — the ruling: allowed 8–1; a lower standard is born
  {line: 'L4', id: 'c1', src: img('05'), kind: 'image', motion: 'kenburns',
   telop: 'THE COURT\nALLOWED IT', overlays: [leakB(0.3)]},
  {line: 'L4', id: 'c2', src: img('07'), kind: 'image', motion: 'kenburns',
   telop: '8 — 1', art: {kind: 'vote', yes: 8, no: 1}},
  {line: 'L4', id: 'c3', src: img('03'), kind: 'image', motion: 'pushin',
   art: {kind: 'citation', label: 'Terry v. Ohio', source: '1968'}},
  {line: 'L4', id: 'c4', src: img('01'), kind: 'image', motion: 'pushin',
   telop: 'A LOWER\nSTANDARD IS BORN', overlays: [strobe(0.24)]},

  // L5 — CTA (platform-specific endcard text swapped at export)
  {line: 'L5', id: 'cta', src: img('05'), kind: 'image', motion: 'kenburns', overlays: [leak(0.28)]},
];

/** Lay each line's cuts continuously across [line.start, nextLine.start) (last -> total). */
const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT06_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT06: ShortData = {
  shortId: 'short06',
  episodeId: 'PD-2026-006-terry',
  durationSec: SHORT06_TOTAL_SEC,
  narrationSrc: 'shorts/short06/audio/short06_final_mix_v002_en_us.mp3', // en_us 4-layer mix
  captions: SHORT06_CAPTIONS,
  bgmSrc: null, // BGM/ambience/SFX already inside the mix
  ctaTextYT: 'Watch on YouTube',
  ctaTextTT: 'Full episode on our profile',
  beats: buildBeats(),
};
