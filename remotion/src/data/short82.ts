import type {ShortArt, ShortBeat, ShortData} from '../compositions/Short';
import {LINE_WINDOWS, SHORT82_CAPTIONS, SHORT82_TOTAL_SEC} from './short82_timing';

/**
 * SHORT #82 — "His confession was thrown out by the Supreme Court. He went back to prison anyway."
 * Episode PD-2026-001-miranda (Miranda v. Arizona, 384 U.S. 436 (1966)).
 *
 * ANGLE. EP01 already has short01 ("why police read you your rights / the 1966 line"). This cut
 * takes the ACT IV twist short01 never touches: the man whose name is on the warning lost anyway.
 *
 * FUNNEL. The short answers its OWN question - what happened to Miranda - so retention and the
 * loop hold. It leaves exactly one question for the long-form: *why did the rule survive when the
 * man did not?* The end-card carries the real long-form thumbnail (cQFql7tT1fE), which is PUBLIC.
 *
 * ACCURACY LOCKS (03_script/script.en.v001.md claim table):
 *  - The Court REVERSED his conviction and refused the confession [CLM-0001]; it did not free him.
 *  - 5-4, Chief Justice Warren for the majority, June 13 1966 [CLM-0002].
 *  - He was RETRIED and convicted again ON OTHER EVIDENCE [CLM-0006]. Never soften into "he got off".
 *  - No likeness of Ernesto Miranda anywhere: silhouettes, hands and objects only.
 *
 * ---- WHY THIS CUT IS NOT A SLIDESHOW (owner directive 2026-08-02) ----
 * Three sources, deliberately mixed, instead of stills-with-Ken-Burns everywhere:
 *   1. REAL FOOTAGE (`kind: 'video'`, 8 of 26 beats) - commercially licensed archive, centre-cropped
 *      and re-encoded to native 1080x1920 in `fx/`. Provenance for every clip is in `fx/RIGHTS.json`.
 *      Only ERA-NEUTRAL macro/silhouette shots are used: a typewriter, a hand signing, cuffs closing,
 *      police lights, a gavel, cell fronts, a corridor walk. Modern prison footage (orange jumpsuits,
 *      visible present-day faces) is deliberately excluded - it would date a 1963 story.
 *   2. NATIVE-VERTICAL AI STILLS (SD3.5 Large, commercial-OK) driven by real depth-map parallax.
 *      Regenerated at 1080x1920 because the episode's own library is 2048x1152, and a 9:16 centre
 *      crop of that keeps only 31.6% of the width - measured on v001, where the handcuffs, benches
 *      and bars all fell outside frame and the cut read as blue streaks.
 *   3. MOTION GRAPHICS (`votetally`) for the 5-4, which no photograph can carry.
 *
 * The archive shelf's filenames and keywords are both unreliable - "bars" returned gold bullion,
 * "court" returned a cartoon judge, and one paper clip carried a fully readable "Lease Agreement".
 * Every clip below was picked off a labelled contact sheet by eye and then re-checked against its
 * LEDGER TITLE; two survived the picture and failed the title, and were dropped.
 */

const img = (n: number) => `shorts/short82/short82_${String(n).padStart(2, '0')}.png`;
const fx = (n: number) => `shorts/short82/fx/fx_${String(n).padStart(3, '0')}.mp4`;
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
  /** Share of the line's span. Default 1 = an equal slice. The funnel card needs more than a
   *  beat: at an even split it got 2.19 s, which is not long enough to read a thumbnail, a
   *  title and a destination pill. Measured conversion is 0.77 subs/1000 views on Shorts vs
   *  3.67 on long-form, so the card is the most valuable 4 seconds in the cut. */
  weight?: number;
};

// 26 cuts over 43.1 s => ~1.66 s per beat (METHOD rule 6: a visual change every 1-2 s).
const CUTS: Cut[] = [
  // L1 — hook. Real motion lands on beat 2 so the first second is not a static plate.
  {line: 'L1', id: 'hook', src: img(1), kind: 'image', motion: 'pushin', fast: true,
   telop: 'THROWN OUT'},
  {line: 'L1', id: 'hook_b', src: fx(35), kind: 'video', motion: 'video'},     // cuffs closing
  {line: 'L1', id: 'hook_c', src: img(2), kind: 'image', motion: 'parallax', fast: true},
  {line: 'L1', id: 'hook_d', src: fx(7), kind: 'video', motion: 'video',       // cell fronts
   telop: 'BACK TO\nPRISON'},

  // L2 — Phoenix, 1963. The room does its work.
  // fx_046 ("strobe lights of a police car") was here and failed the eye test: centre-cropped to
  // 9:16 it reads as an abstract stripe, not a patrol car, under a "PHOENIX 1963" telop. Swapped
  // for the plate shot tight on the beacon; the real-motion beats in this line are the typewriter
  // and the signing hand below.
  {line: 'L2', id: 'b1', src: img(5), kind: 'image', motion: 'pushin', telop: 'PHOENIX 1963'},
  {line: 'L2', id: 'b1b', src: fx(47), kind: 'video', motion: 'video'},
  {line: 'L2', id: 'b1c', src: img(7), kind: 'image', motion: 'kenburns'},
  {line: 'L2', id: 'b1d', src: img(8), kind: 'image', motion: 'pushin'},
  {line: 'L2', id: 'b1e', src: fx(51), kind: 'video', motion: 'video'},        // typewriter
  {line: 'L2', id: 'b1f', src: fx(52), kind: 'video', motion: 'video',         // signing
   telop: 'HE CONFESSED'},
  {line: 'L2', id: 'b1g', src: img(11), kind: 'image', motion: 'kenburns',
   telop: 'NOBODY TOLD HIM\nHE COULD STOP'},

  // L3 — it climbs, and the Court agrees. The vote is the beat.
  {line: 'L3', id: 'b2', src: img(12), kind: 'image', motion: 'pushin'},
  {line: 'L3', id: 'b2b', src: img(13), kind: 'image', motion: 'parallax', telop: '1966'},
  {line: 'L3', id: 'b2c', src: img(14), kind: 'image', motion: 'kenburns'},
  {line: 'L3', id: 'b2d', src: null, kind: 'card', motion: 'pushin',
   art: {kind: 'votetally', majority: 5, dissent: 4, label: 'MIRANDA v. ARIZONA'}},
  {line: 'L3', id: 'b2e', src: fx(28), kind: 'video', motion: 'video',         // gavel struck
   telop: 'IT SHOULD NEVER\nHAVE COUNTED'},

  // L4 — the payoff: tried again, convicted again.
  {line: 'L4', id: 'c1', src: img(16), kind: 'image', motion: 'kenburns'},
  {line: 'L4', id: 'c1b', src: img(17), kind: 'image', motion: 'parallax'},
  {line: 'L4', id: 'c1c', src: img(18), kind: 'image', motion: 'pushin', telop: 'TRIED AGAIN'},
  {line: 'L4', id: 'c1d', src: img(19), kind: 'image', motion: 'kenburns'},
  {line: 'L4', id: 'c1e', src: fx(9), kind: 'video', motion: 'video', telop: 'GUILTY'},
  {line: 'L4', id: 'c1f', src: fx(20), kind: 'video', motion: 'video'},        // corridor walk

  // L5 — what outlived him, then the funnel card, then the loop tail.
  {line: 'L5', id: 'c2', src: img(22), kind: 'image', motion: 'kenburns', weight: 0.7},
  {line: 'L5', id: 'c2b', src: img(23), kind: 'image', motion: 'pushin', weight: 0.7,
   telop: 'THE RULE\nOUTLIVED HIM'},
  // The funnel card is the most valuable real estate in the cut: measured conversion is
  // 0.77 subs / 1000 views on Shorts against 3.67 on long-form. At an equal share it got
  // 2.40 s, and the headline / title / pill were still animating in at 0.3 s. 4 s lets the
  // whole card land and be read.
  // Owner 2026-08-02: the card used to disappear 1.4 s before the end because a loop-tail
  // beat followed it. METHOD rule 5 wants the last frame to cut cleanly back to the first, but
  // the destination is worth more than the seam here: Shorts loops on its own, and conversion is
  // the measured bottleneck (0.77 subs/1000 on Shorts vs 3.67 on long-form). The card now holds
  // to the final frame.
  {line: 'L5', id: 'cta', src: img(13), kind: 'image', motion: 'kenburns', weight: 2.55},
];

const buildBeats = (): ShortBeat[] => {
  const beats: ShortBeat[] = [];
  LINE_WINDOWS.forEach((win, i) => {
    const spanStart = win.start;
    const spanEnd = i + 1 < LINE_WINDOWS.length ? LINE_WINDOWS[i + 1].start : SHORT82_TOTAL_SEC;
    const cuts = CUTS.filter((c) => c.line === win.id);
    const total = cuts.reduce((s, c) => s + (c.weight ?? 1), 0) || 1;
    const unit = (spanEnd - spanStart) / total;
    let cursor = spanStart;
    cuts.forEach((cut) => {
      const {line: _line, weight, ...rest} = cut;
      const dur = unit * (weight ?? 1);
      beats.push({...rest, startSec: r3(cursor), durSec: r3(dur)});
      cursor += dur;
    });
  });
  return beats;
};

export const SHORT82: ShortData = {
  shortId: 'short82',
  episodeId: 'PD-2026-001-miranda',
  durationSec: SHORT82_TOTAL_SEC,
  narrationSrc: 'shorts/short82/audio/short82_final_mix_v002_en_us.mp3',
  captions: SHORT82_CAPTIONS,
  bgmSrc: null,
  ctaTextYT: 'Watch the full case on the channel',
  ctaTextTT: 'Full case on our profile',
  ctaLongThumbSrc: 'shorts/short82/short82_ctathumb.jpg',
  ctaLongTitle: 'Read Rights or It’s Out',
  ctaHeadline: 'FULL CASE',
  // METHOD's default band puts captions at 52-69% of the frame - dead centre, across the
  // subject. Dropped to the lower third: y1270+250 ends at 1520, above the Shorts bottom
  // overlay, and leaves the picture unobstructed.
  // Measured 2026-08-02 by drawing the real Shorts furniture over a rendered frame: the
  // related-video link band lands at ~y1450 and the channel/title block at ~y1580. At 1380 the
  // caption was completely buried under the link band. 1210+250 ends at 1460... so 1210+220 ends
  // at 1430, which clears it. This is the LOWEST captions can go - below it is YouTube's own text.
  captionTop: 1210,
  beats: buildBeats(),
};
