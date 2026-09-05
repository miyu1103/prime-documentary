import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../brand';
import {PdMonogram} from './Brand';
import {Grain} from './Grain';
import {Particles, Vignette} from './Motion';

/**
 * Reusable channel BOOKENDS — the SAME opening + ending every episode (brand consistency,
 * decisions/0002 §G). Only the opening's episode title/subtitle/seriesLabel changes; the
 * end-card is fixed (identical every episode). All Premium compositions import these as-is.
 *
 * 2026-06-28: owner-approved "派手" brush-up adopted as the canonical look (背景=宇宙の日の出 /
 * PDモノグラム / トラッキングイン / 単語スタッガー＋マスク切れ上がり＋Trail残像 / ゴールド線スパーク /
 * 着地の光の筋＆フラッシュ / ED登録CTAパルス)。署名(props)とOPENING_SEC/ENDCARD_SECは不変。
 */

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

export const OPENING_SEC = 3.5;
export const ENDCARD_SEC = 9;

/** Standard cinematic title opening: sunrise bg + PD monogram + series label / TITLE / subtitle.
 *
 * This is the `card` variant -- the full-screen 3.5 s opening every episode up to EP65 renders.
 * Nothing inside it changed when `variant` was added (2026-08-10): the component was renamed and
 * a dispatcher put in front of it, so EP62-65 keep an identical element tree and identical
 * numbers. Do not tune anything in here for EP66; the overlay form is a separate component. */
const BrandOpeningCard: React.FC<{seriesLabel: string; title: string; subtitle?: string}> = ({
  seriesLabel,
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const bgZoom = interpolate(frame, [0, durationInFrames], [1.28, 1.06], {easing: Easing.out(Easing.cubic)});
  const bgRise = interpolate(frame, [0, durationInFrames], [34, -6], {easing: Easing.out(Easing.cubic)});
  const bloomGrow = spring({frame: frame - f(0.1), fps, config: {damping: 60, stiffness: 30}});
  const bloomPulse = 0.82 + 0.18 * Math.sin(frame * 0.12);

  const fadeIn = interpolate(frame, [0, f(0.35)], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - f(0.5), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});

  const monoS = spring({frame: frame - f(0.15), fps, config: {stiffness: 70, damping: 11, mass: 1}});
  const wordS = spring({frame: frame - f(0.5), fps, config: {damping: 18, stiffness: 110}});
  const track = interpolate(wordS, [0, 1], [46, 10]);
  const ruleS = spring({frame: frame - f(0.85), fps, config: {damping: 15, stiffness: 90}});
  const ruleW = interpolate(ruleS, [0, 1], [0, 560]);
  const subS = spring({frame: frame - f(2.0), fps, config: {damping: 20, stiffness: 110}});

  const words = title.split(' ');
  const wordStaggerF = Math.max(1, f(0.06));
  const titleHit = f(1.1);

  const streakP = interpolate(frame, [titleHit - 2, titleHit + f(0.7)], [-130, 130], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const streakO = interpolate(frame, [titleHit - 2, titleHit + f(0.2), titleHit + f(0.7)], [0, 0.8, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const flash = interpolate(frame, [titleHit - 1, titleHit + 1, titleHit + f(0.3)], [0, 0.26, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: INK, opacity: Math.min(fadeIn, fadeOut)}}>
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Img
          src={staticFile('banner_sunrise.png')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: '50% 46%',
            transform: `translateY(${bgRise}px) scale(${bgZoom})`,
            transformOrigin: '50% 60%',
            filter: 'brightness(0.6) contrast(1.18) saturate(0.95)',
          }}
        />
      </AbsoluteFill>

      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 30% at 50% 70%, ${GOLD}aa 0%, ${GOLD}22 35%, transparent 66%)`,
          transform: `scale(${0.6 + bloomGrow * 0.7})`,
          transformOrigin: '50% 70%',
          opacity: bloomGrow * bloomPulse,
          mixBlendMode: 'screen',
        }}
      />

      <AbsoluteFill style={{background: `linear-gradient(to bottom, ${INK}C0 0%, ${INK}38 40%, ${INK}E0 100%)`}} />

      <Trail layers={7} lagInFrames={1.5} trailOpacity={0.42}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
          <div style={{transform: `translateY(${interpolate(monoS, [0, 1], [40, 0])}px) scale(${interpolate(monoS, [0, 1], [0.55, 1])})`, opacity: Math.min(1, monoS * 1.3)}}>
            <PdMonogram size={120} />
          </div>
          <div
            style={{
              marginTop: 6,
              fontFamily: BRAND.font.display,
              color: WHITE,
              fontSize: 40,
              fontWeight: 900,
              letterSpacing: track,
              textTransform: 'uppercase',
              textShadow: `0 0 30px ${GOLD}66`,
              opacity: wordS,
            }}
          >
            {seriesLabel}
          </div>

          <div style={{position: 'relative', width: 560, height: 2, margin: '20px 0 22px'}}>
            <div style={{width: ruleW, height: 2, background: GOLD, boxShadow: `0 0 16px 3px ${GOLD}99`}} />
            <div style={{position: 'absolute', top: '50%', left: ruleW, width: 16, height: 16, marginTop: -8, marginLeft: -8, borderRadius: 8, background: WHITE, boxShadow: `0 0 22px 8px ${GOLD}`, opacity: ruleS > 0.02 && ruleS < 0.98 ? 1 : 0}} />
          </div>

          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              justifyContent: 'center',
              gap: '0 0.24em',
              maxWidth: 1600,
              fontFamily: BRAND.font.display,
              color: WHITE,
              fontSize: 96,
              lineHeight: 0.95,
              textTransform: 'uppercase',
              textAlign: 'center',
              textShadow: `0 0 50px ${GOLD}55, 0 4px 28px #000`,
            }}
          >
            {words.map((w, i) => {
              const ws = spring({frame: frame - titleHit - i * wordStaggerF, fps, config: {damping: 10, stiffness: 120, mass: 1}});
              const y = interpolate(ws, [0, 1], [120, 0]);
              const sc = interpolate(ws, [0, 1], [1.18, 1]);
              const o = interpolate(ws, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
              return (
                <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}>
                  <span style={{display: 'inline-block', transform: `translateY(${y}%) scale(${sc})`, opacity: o}}>{w}</span>
                </span>
              );
            })}
          </div>

          {subtitle ? (
            <div
              style={{
                fontFamily: BRAND.font.body,
                color: GOLD,
                fontSize: 30,
                fontWeight: 700,
                marginTop: 16,
                transform: `translateY(${interpolate(subS, [0, 1], [16, 0])}px)`,
                opacity: subS,
              }}
            >
              {subtitle}
            </div>
          ) : null}
        </AbsoluteFill>
      </Trail>

      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
        <div
          style={{
            position: 'absolute',
            top: '54%',
            width: '70%',
            height: 200,
            background: `linear-gradient(100deg, transparent 0%, ${WHITE}cc 48%, ${GOLD}aa 54%, transparent 70%)`,
            transform: `translateX(${streakP}%) rotate(-8deg)`,
            opacity: streakO,
            mixBlendMode: 'screen',
            filter: 'blur(2px)',
          }}
        />
      </AbsoluteFill>

      <Particles count={26} seed="brand-opening-bold" color={GOLD} />
      <Vignette strength={1} />
      <Grain opacity={0.06} />

      <AbsoluteFill style={{background: WHITE, opacity: flash, mixBlendMode: 'screen', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};

/**
 * OVERLAY form of the SAME brand opening (EP66 PACKAGING v001 sections 4 and 7).
 *
 * Why it exists: from EP66 the hook is voiced from frame 0 (SPEC v2 row 9), so the film declares
 * `leadSeconds: 0` and there is no silent gap in front of the body to hold a full-screen card.
 * Under the card layout the opening simply would not render at all. This form puts the brand
 * furniture in a band across the bottom of the frame while the picture and the narration keep
 * running underneath -- nothing cuts away and nothing pauses.
 *
 * TIMELINE (PACKAGING section 7.2). The component is mounted for OPENING_SEC; `frame` below is
 * relative to its own start, which for EP66 is 0:20.5 so this table is 20.50-24.00 on the film.
 *
 *   in    0.000-0.400 s   F 0-12    scrim band + monogram rise from below the frame edge
 *   in    0.133-0.600 s   F 4-18    series label mask-reveals            (+4F stagger)
 *   in    0.267-0.800 s   F 8-24    episode title mask-reveals           (+8F stagger)
 *   hold  0.800-2.600 s   F 24-78   still; the cut and the voice underneath do not stop
 *   out   2.600-3.500 s   F 78-105  the three elements drop out, -6F reverse stagger
 *
 * MOTION DISCIPLINE (owner's opening manual, carried by PD_ONE_PASS_PRODUCTION_SPEC.v2 row 14):
 *   - every movement is eased: spring() on the two rises, Easing.out(Easing.cubic) on the two
 *     mask reveals, Easing.in(Easing.cubic) on the exit. No constant-linear tween anywhere.
 *   - no element animates opacity alone. Scrim and monogram pair it with translateY (+ scale on
 *     the monogram); the two text lines never fade at all on entry -- they are revealed by an
 *     overflow:hidden mask -- and on exit their fade is paired with translateY.
 *   - the entrance is staggered +4F per element and the exit -6F per element; nothing moves
 *     together.
 *   - Trail (@remotion/motion-blur) is applied while anything is moving and dropped during the
 *     hold, where it would cost render time and change no pixel.
 * All timings are SECONDS and every frame is Math.round(sec * fps) -- no frame literals. The F
 * column above is what those seconds resolve to at the PD long-form 30 fps.
 */
const OVERLAY = {
  /** layer 2 of section 7.4: the band is the bottom 22% of the frame (238 px at 1080) */
  bandHeightRatio: 0.22,
  bandTopFadePx: 12,
  scrimAlpha: 0.82,
  scrimRisePx: 72,
  monoRisePx: 40,
  monoScaleFrom: 0.94,
  monoSize: 64,
  seriesDelaySec: 0.133,
  seriesRevealSec: 0.467,
  seriesSize: 28,
  titleDelaySec: 0.267,
  titleRevealSec: 0.533,
  titleSize: 46,
  outStartSec: 2.6,
  outStaggerSec: 0.2,
  outSec: 0.5,
  outDropPx: 64,
  trailLayers: 6,
  trailLagInFrames: 1.2,
  trailOpacity: 0.34,
} as const;

const BrandOpeningOverlay: React.FC<{seriesLabel: string; title: string}> = ({seriesLabel, title}) => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const bandH = Math.round(height * OVERLAY.bandHeightRatio);
  const outStart = f(OVERLAY.outStartSec);
  const outLen = f(OVERLAY.outSec);
  const outStagger = f(OVERLAY.outStaggerSec);

  // Exit, reverse-staggered: title leaves first (order 0, F 78), then the series label
  // (F 84), then the scrim and monogram together (F 90). translateY paired with the fade.
  const exit = (order: number) => {
    const from = outStart + order * outStagger;
    const p = interpolate(frame, [from, from + outLen], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.in(Easing.cubic),
    });
    return {y: p * OVERLAY.outDropPx, o: 1 - p};
  };
  const exTitle = exit(0);
  const exSeries = exit(1);
  const exBase = exit(2);

  const scrimS = spring({frame, fps, config: {damping: 20, mass: 0.6}});
  const monoS = spring({frame, fps, config: {damping: 18, mass: 0.5}});

  // Mask reveals: the line sits at +100% of its own height inside an overflow:hidden parent and
  // eases up to 0. Opacity is a constant 1 -- the mask is what makes it appear.
  const maskUp = (delaySec: number, revealSec: number) =>
    interpolate(frame, [f(delaySec), f(delaySec) + f(revealSec)], [100, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.cubic),
    });
  const seriesY = maskUp(OVERLAY.seriesDelaySec, OVERLAY.seriesRevealSec);
  const titleY = maskUp(OVERLAY.titleDelaySec, OVERLAY.titleRevealSec);

  const enterEnd = f(OVERLAY.titleDelaySec) + f(OVERLAY.titleRevealSec);
  const moving = frame < enterEnd || frame >= outStart;

  const band = (
    <AbsoluteFill>
      {/* layer 2 -- scrim band, with the brand gold hairline riding on its top edge */}
      <AbsoluteFill
        style={{
          background:
            `linear-gradient(to bottom, rgba(8,10,14,0) 0px, ` +
            `rgba(8,10,14,${OVERLAY.scrimAlpha}) ${OVERLAY.bandTopFadePx}px, ` +
            `rgba(8,10,14,${OVERLAY.scrimAlpha}) 100%)`,
          transform: `translateY(${(1 - scrimS) * OVERLAY.scrimRisePx + exBase.y}px)`,
          opacity: Math.max(0, scrimS * exBase.o),
        }}
      >
        <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 2, background: GOLD, boxShadow: `0 0 14px 2px ${GOLD}88`}} />
      </AbsoluteFill>

      <AbsoluteFill style={{flexDirection: 'row', alignItems: 'center', padding: '0 96px', gap: 28}}>
        {/* layer 3 -- monogram */}
        <div
          style={{
            flex: '0 0 auto',
            transform:
              `translateY(${(1 - monoS) * OVERLAY.monoRisePx + exBase.y}px) ` +
              `scale(${OVERLAY.monoScaleFrom + monoS * (1 - OVERLAY.monoScaleFrom)})`,
            opacity: Math.min(1, Math.max(0, monoS * 1.25)) * exBase.o,
          }}
        >
          <PdMonogram size={OVERLAY.monoSize} />
        </div>

        {/* layer 4 -- the two text lines, each in its own overflow:hidden mask */}
        <div style={{display: 'flex', flexDirection: 'column', minWidth: 0}}>
          <div style={{overflow: 'hidden', paddingBottom: '0.06em', transform: `translateY(${exSeries.y}px)`, opacity: exSeries.o}}>
            <div
              style={{
                transform: `translateY(${seriesY}%)`,
                fontFamily: BRAND.font.display,
                color: WHITE,
                fontSize: OVERLAY.seriesSize,
                fontWeight: 900,
                letterSpacing: 6,
                textTransform: 'uppercase',
                textShadow: `0 0 18px ${GOLD}66`,
              }}
            >
              {seriesLabel}
            </div>
          </div>
          <div style={{overflow: 'hidden', paddingBottom: '0.06em', transform: `translateY(${exTitle.y}px)`, opacity: exTitle.o}}>
            <div
              style={{
                transform: `translateY(${titleY}%)`,
                fontFamily: BRAND.font.display,
                color: WHITE,
                fontSize: OVERLAY.titleSize,
                fontWeight: 900,
                lineHeight: 1.06,
                textTransform: 'uppercase',
                textShadow: `0 3px 22px #000, 0 0 40px ${GOLD}44`,
              }}
            >
              {title}
            </div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* The band clips its own contents, so the elements rise in from below the frame edge and
          drop back out of it. Nothing above the band is touched: the cut keeps playing. */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: bandH, overflow: 'hidden'}}>
        {moving ? (
          <Trail layers={OVERLAY.trailLayers} lagInFrames={OVERLAY.trailLagInFrames} trailOpacity={OVERLAY.trailOpacity}>
            {band}
          </Trail>
        ) : (
          band
        )}
      </div>
    </AbsoluteFill>
  );
};

export type BrandOpeningVariant = 'card' | 'overlay';

/**
 * The channel opening. `variant` is OPT-IN and defaults to the historical full-screen card, so a
 * caller that does not pass it renders exactly what it rendered before this prop existed.
 *
 *   'card'    full-screen 3.5 s title (every episode up to EP65)
 *   'overlay' 3.5 s lower band over running picture and narration (EP66 onward, row 9 layout)
 *
 * `subtitle` is used by the card only; the band is 238 px tall and carries the series label and
 * the title, which is what PACKAGING section 7.4 lists as its text layer.
 */
export const BrandOpening: React.FC<{
  seriesLabel: string;
  title: string;
  subtitle?: string;
  variant?: BrandOpeningVariant;
}> = ({seriesLabel, title, subtitle, variant = 'card'}) =>
  variant === 'overlay' ? (
    <BrandOpeningOverlay seriesLabel={seriesLabel} title={title} />
  ) : (
    <BrandOpeningCard seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
  );

/** Standard channel END-CARD — IDENTICAL every episode (brand sign-off + subscribe). */
export const BrandEndcard: React.FC<{
  channel?: string;
  ctaLine?: string;
  cadenceLine?: string;
}> = ({
  channel = 'PRIME DOCUMENTARY',
  ctaLine = '▶ SUBSCRIBE — LANDMARK RIGHTS CASES',
  cadenceLine = 'New episodes every week',
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const bgZoom = interpolate(frame, [0, durationInFrames], [1.12, 1.26], {easing: Easing.inOut(Easing.sin)});
  const bgRise = interpolate(frame, [0, durationInFrames], [10, -18]);
  const bloom = 0.7 + 0.22 * Math.sin(frame * 0.08);

  const fadeIn = interpolate(frame, [0, f(0.4)], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - f(0.5), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic)});

  const monoS = spring({frame: frame - f(0.2), fps, config: {stiffness: 70, damping: 11, mass: 1}});
  const wordS = spring({frame: frame - f(0.55), fps, config: {damping: 18, stiffness: 110}});
  const track = interpolate(wordS, [0, 1], [44, 8]);
  const ruleS = spring({frame: frame - f(0.95), fps, config: {damping: 15, stiffness: 90}});
  const ruleW = interpolate(ruleS, [0, 1], [0, 560]);
  const ctaS = spring({frame: frame - f(1.6), fps, config: {damping: 20, stiffness: 110}});
  const ctaPulse = ctaS > 0.6 ? 1 + 0.04 * Math.sin((frame - f(1.6)) * 0.2) : 1;
  const ctaGlow = 0.5 + 0.5 * (0.5 + 0.5 * Math.sin((frame - f(1.6)) * 0.2));
  const cadS = spring({frame: frame - f(2.2), fps, config: {damping: 20, stiffness: 110}});
  const baseLineW = interpolate(spring({frame: frame - f(1.2), fps, config: {damping: 18, stiffness: 80}}), [0, 1], [0, 1]);

  const brandHit = f(1.0);
  const streakP = interpolate(frame, [brandHit - 2, brandHit + f(0.7)], [-130, 130], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const streakO = interpolate(frame, [brandHit - 2, brandHit + f(0.2), brandHit + f(0.7)], [0, 0.75, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const flash = interpolate(frame, [brandHit - 1, brandHit + 1, brandHit + f(0.3)], [0, 0.22, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: INK, opacity: Math.min(fadeIn, fadeOut)}}>
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Img
          src={staticFile('banner_sunrise.png')}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: '50% 44%',
            transform: `translateY(${bgRise}px) scale(${bgZoom})`,
            transformOrigin: '50% 58%',
            filter: 'brightness(0.5) contrast(1.16) saturate(0.92)',
          }}
        />
      </AbsoluteFill>

      <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 42%, ${NAVY}cc 0%, ${INK}f2 82%)`}} />

      <AbsoluteFill
        style={{
          background: `radial-gradient(42% 30% at 50% 66%, ${GOLD}aa 0%, ${GOLD}22 36%, transparent 66%)`,
          opacity: bloom,
          mixBlendMode: 'screen',
        }}
      />

      <Trail layers={6} lagInFrames={1.4} trailOpacity={0.4}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
          <div style={{transform: `translateY(${interpolate(monoS, [0, 1], [44, 0])}px) scale(${interpolate(monoS, [0, 1], [0.55, 1])})`, opacity: Math.min(1, monoS * 1.3)}}>
            <PdMonogram size={150} />
          </div>
          <div
            style={{
              marginTop: 12,
              fontFamily: BRAND.font.display,
              color: WHITE,
              fontSize: 56,
              fontWeight: 900,
              letterSpacing: track,
              textTransform: 'uppercase',
              textShadow: `0 0 36px ${GOLD}66`,
              opacity: wordS,
            }}
          >
            {channel}
          </div>

          <div style={{position: 'relative', width: 560, height: 2, margin: '18px 0 24px'}}>
            <div style={{width: ruleW, height: 2, background: GOLD, boxShadow: `0 0 16px 3px ${GOLD}99`}} />
            <div style={{position: 'absolute', top: '50%', left: ruleW, width: 16, height: 16, marginTop: -8, marginLeft: -8, borderRadius: 8, background: WHITE, boxShadow: `0 0 22px 8px ${GOLD}`, opacity: ruleS > 0.02 && ruleS < 0.98 ? 1 : 0}} />
          </div>

          <div
            style={{
              fontFamily: BRAND.font.body,
              color: GOLD,
              fontSize: 34,
              fontWeight: 800,
              letterSpacing: 1,
              transform: `translateY(${interpolate(ctaS, [0, 1], [20, 0])}px) scale(${ctaPulse})`,
              opacity: ctaS,
              textShadow: `0 0 ${10 + ctaGlow * 26}px ${GOLD}cc`,
            }}
          >
            {ctaLine}
          </div>

          <div
            style={{
              fontFamily: BRAND.font.body,
              color: SILVER,
              fontSize: 27,
              marginTop: 12,
              transform: `translateY(${interpolate(cadS, [0, 1], [14, 0])}px)`,
              opacity: cadS,
            }}
          >
            {cadenceLine}
          </div>
        </AbsoluteFill>
      </Trail>

      <div style={{position: 'absolute', left: '50%', bottom: '22%', width: `${baseLineW * 70}%`, height: 3, background: GOLD, opacity: 0.85, boxShadow: `0 0 16px 3px ${GOLD}77`, transform: 'translateX(-50%)'}} />

      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
        <div
          style={{
            position: 'absolute',
            top: '46%',
            width: '70%',
            height: 200,
            background: `linear-gradient(100deg, transparent 0%, ${WHITE}cc 48%, ${GOLD}aa 54%, transparent 70%)`,
            transform: `translateX(${streakP}%) rotate(-8deg)`,
            opacity: streakO,
            mixBlendMode: 'screen',
            filter: 'blur(2px)',
          }}
        />
      </AbsoluteFill>

      <Particles count={24} seed="brand-ending-bold" color={GOLD} />
      <Vignette strength={1} />
      <Grain opacity={0.06} />

      <AbsoluteFill style={{background: WHITE, opacity: flash, mixBlendMode: 'screen', pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
