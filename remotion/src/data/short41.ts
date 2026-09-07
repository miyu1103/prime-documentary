import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT41_CAPTIONS, SHORT41_TOTAL_SEC} from './short41_timing';

/**
 * SHORT #41 — Frazier v. Cupp / police deception in interrogation -> false confession. PREMIUM tier.
 * R2 (+R3 adjacent). No real-person likeness (Barry Laughman, officers, victim). Symbolic only.
 * Spec: episodes/_planning/_short_spec_33_PREMIUM.md (§0/§4/§5/§10 shared) · facts PD-2026-039-frazier ledger.
 * WORDING LOCKS: An officer told Barry Laughman his FINGERPRINTS were at the scene — there were NO
 * fingerprints, NO match; it was INVENTED, and it was LEGAL. Barry was 24 with the comprehension of a
 * ten-year-old (IQ 70). Blood exclusion: victim was an A secretor, Barry a B secretor, the swab carried
 * A-type material with NO B antigen — the strongest exclusion available before DNA. He was convicted and
 * sentenced to LIFE. Frazier v. Cupp, 394 U.S. 731 (1969): a police lie about the evidence, standing ALONE,
 * does not make an otherwise voluntary confession inadmissible (totality of the circumstances). Y-STR DNA
 * cleared him in 2003; ~16 years served. For ADULTS, lying about evidence is STILL LEGAL (some states now
 * bar it only for minors). Do NOT assert a Frazier vote count (not in the ledger). Do not depict the assault.
 */

const img = (n: string) => `shorts/short41/short41_${n}.png`;
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
  // L1 — hook: the prints were invented, and the lie was legal
  {line: 'L1', id: 'hook', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE PRINTS\nDID NOT EXIST', art: {kind: 'lightrays'}},

  // L2 — the room: 24, mind of a 10-year-old, told his prints were there, confessed
  {line: 'L2', id: 'b1', src: img('02'), kind: 'image', motion: 'kenburns', telop: 'MIND OF A\n10-YEAR-OLD'},
  {line: 'L2', id: 'b1b', src: img('03'), kind: 'image', motion: 'parallax', telop: 'SO HE\nCONFESSED'},

  // L3 — the science: A vs B blood, no B antigen -> strongest pre-DNA exclusion, ignored; life
  {line: 'L3', id: 'b2a', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'money',
     nodes: [{x: 0.5, y: 0.2, label: 'VICTIM · TYPE A'}, {x: 0.5, y: 0.5, label: 'BARRY · TYPE B'}, {x: 0.5, y: 0.82, label: 'NO MATCH'}],
     edges: [{from: 0, to: 2, weight: 3}, {from: 1, to: 2, weight: 3}]}},
  {line: 'L3', id: 'b2b', src: img('05'), kind: 'image', motion: 'kenburns', telop: 'THE BLOOD\nCLEARED HIM'},
  {line: 'L3', id: 'b2c', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'ticker', value: 16, suffix: ' YEARS', topLabel: 'DNA FREED HIM AFTER', label: 'the confession was legal'}},

  // L4 — the rule: 1969, a lie about the evidence alone is not enough; still legal for adults
  {line: 'L4', id: 'c1', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'yearsweep', from: 1969, to: 2004, label: 'The rule the Supreme Court left standing'}},
  {line: 'L4', id: 'c2', src: img('06'), kind: 'image', motion: 'kenburns', telop: 'THE LIE\nWAS LEGAL'},
  {line: 'L4', id: 'c3', src: img('07'), kind: 'image', motion: 'kenburns', telop: 'STILL LEGAL\nTODAY'},

  // L5 — CTA
  {line: 'L5', id: 'cta', src: img('07'), kind: 'image', motion: 'kenburns'},

  // L5 loop tail — mirrors the hook (last frame == first frame) for a seamless loop (rule 5).
  {line: 'L5', id: 'loop', src: img('01'), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THE PRINTS\nDID NOT EXIST'},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT41_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const each = (spanEnd - spanStart) / Math.max(1, cuts.length);
    cuts.forEach((cut, k) => {
      const {line: _line, ...rest} = cut;
      beats.push({...rest, startSec: r3(spanStart + k * each), durSec: r3(each)});
    });
  });
  return beats;
};

export const SHORT41: ShortData = {
  shortId: 'short41',
  episodeId: 'PD-2026-039-frazier',
  durationSec: SHORT41_TOTAL_SEC,
  narrationSrc: 'shorts/short41/audio/short41_final_mix_v002_en_us.mp3',
  captions: SHORT41_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full story on the channel',
  ctaTextTT: 'Full story on our profile',
  beats: buildBeats(),
};
