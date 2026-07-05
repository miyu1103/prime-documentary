import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {AmbientMotion} from './AmbientMotion';
import {StatCounter, Timeline, BarChart} from './Figures';
// carsearch/motionkit "moving diagram" tier — wired here so film_data.figures can render them.
import {BrightLine} from './carsearch/BrightLine';
import {CarCutaway} from './carsearch/CarCutaway';
import {ProbableCauseMeter} from './carsearch/ProbableCauseMeter';
import {CurtilageShield} from './carsearch/CurtilageShield';
import {StateMap} from './carsearch/StateMap';
import {CaseTimeline} from './carsearch/CaseTimeline';
import {CarKeyLock} from './carsearch/CarKeyLock';
import {NumberTicker} from './motionkit/NumberTicker';
import {VoteTally} from './motionkit/VoteTally';
import {QuoteCard} from './motionkit/QuoteCard';

/**
 * FigureBeats — the §5.6 "Figures tier": data beats rendered as full-screen ANIMATED figures
 * (StatCounter counts up, Timeline draws L->R, BarChart grows) instead of flat kinetic text.
 * Data-driven from film_data.figures; each figure covers its own span (opaque backdrop) so the
 * footage gives way to a dynamic data-viz moment. Captions still render on top. This is the
 * single biggest "画面が生きる" upgrade — numbers/timeline come alive.
 */
export type FigureSpec =
  | {start: number; end: number; kind: 'stat'; value: number; prefix?: string; suffix?: string; decimals?: number; label: string; topLabel?: string}
  | {start: number; end: number; kind: 'timeline'; events: {year: string; text: string}[]}
  | {start: number; end: number; kind: 'bar'; data: {label: string; value: number}[]}
  // --- carsearch / motionkit "moving diagram" tier (real components rendered full-screen) ---
  | {start: number; end: number; kind: 'brightline'; mode?: 'draw' | 'hold' | 'slam'}
  | {start: number; end: number; kind: 'carcutaway'; mode?: 'all' | 'big' | 'small'; zones?: string[]}
  | {start: number; end: number; kind: 'probablecause'; outcome?: 'stall' | 'cross'}
  | {start: number; end: number; kind: 'curtilage'}
  | {start: number; end: number; kind: 'statemap'; label?: string}
  // distinct from the existing flat 'timeline' — this is the carsearch CaseTimeline component
  | {start: number; end: number; kind: 'casetimeline_c'; events: {year: string; text: string}[]}
  | {start: number; end: number; kind: 'carkeylock'}
  | {start: number; end: number; kind: 'numberticker'; value: number; prefix?: string; suffix?: string; decimals?: number; label?: string; topLabel?: string}
  | {start: number; end: number; kind: 'votetally'; majority: number; dissent: number; label?: string}
  | {start: number; end: number; kind: 'quote'; quote: string; attribution: string};

/** SceneBed — the DESIGNED scene bed behind every figure.
 *
 * CRITICAL (freezedetect fix): this bed is NO LONGER an opaque fill. In CaseFilm the Body renders
 * the photo/footage cuts CONTINUOUSLY underneath FigureBeats (Ken-Burns pan/zoom + depth parallax +
 * footage — those cut frames already PASS freezedetect). The old opaque navy ground hid that moving
 * cut, so during a figure the whole frame was static except the small central diagram → the freeze
 * detector flagged ~7s figure stretches as near-still no matter how much the figure itself drifted.
 *
 * The fix: the DOMINANT background is now the moving cut, seen through a SEMI-TRANSPARENT dark scrim.
 * A large peripheral portion of every frame therefore keeps changing (the cut moves), so per-frame
 * pixel difference over a big area stays well above the freeze noise floor across the whole hold.
 * Legibility is preserved by a STRONGER LOCAL panel behind the figure's text/number region only.
 *
 * Layer order (bottom→top), all deterministic / frame-driven / eased:
 *  1. Base scrim: semi-transparent dark, alpha ~0.46–0.55 → ~45–54% of the moving cut shows through
 *     across the whole frame (the reliable carrier of full-frame motion). A `backdropFilter` blur is
 *     ALSO applied so the underlying cut reads as a soft moving bokeh field — but the semi-transparent
 *     gradient alone already carries the motion, so we never depend on backdrop-filter rendering.
 *  2. Local center panel: a stronger dark radial (center only, fades to transparent by ~74% radius)
 *     that seats the figure so its text/number stays crisp and high-contrast, while the periphery
 *     keeps showing the moving cut. This is effectively an INVERSE vignette (dark center, clear edges).
 *  3. Two large soft glows on slow lissajous drifts, `screen`-blended (additive light only — never
 *     darkens the figure) — extra ambient motion + volume.
 *  4. A FAINT corner vignette only (soft, low alpha) so it barely trims the moving cut at the edges. */
const SceneBed: React.FC = () => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const p = interpolate(f, [0, d], [0, 1], {extrapolateRight: 'clamp'});
  // two large soft glows on slow lissajous drifts — volumetric, always-moving bed
  const g1x = 34 + 11 * Math.sin(p * Math.PI * 2);
  const g1y = 32 + 9 * Math.cos(p * Math.PI * 2);
  const g2x = 68 + 12 * Math.cos(p * Math.PI * 2 + 1.5);
  const g2y = 64 + 10 * Math.sin(p * Math.PI * 2 + 1.5);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      {/* 1. SEMI-TRANSPARENT base scrim — the moving cut underneath shows through (~45–54% visible).
             backdropFilter blurs that moving cut into a soft bokeh field; if the Remotion/Chromium
             pipeline ignores backdrop-filter, the semi-transparent gradient below still carries the
             full-frame motion, so the freeze fix does NOT rely on backdrop-filter alone. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          backdropFilter: 'blur(9px)',
          WebkitBackdropFilter: 'blur(9px)',
          background:
            'linear-gradient(180deg, rgba(5,8,14,0.55) 0%, rgba(6,12,20,0.46) 55%, rgba(4,6,11,0.52) 100%)',
        } as React.CSSProperties}
      />
      {/* 2. LOCAL center panel — stronger dark radial behind the figure's text/number only, fading to
             transparent by ~74% radius so the periphery keeps showing the moving cut. Seats the figure
             (crisp, high-contrast) without turning the whole frame static. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background:
            'radial-gradient(60% 64% at 50% 48%, rgba(3,5,10,0.74) 0%, rgba(3,5,10,0.5) 40%, transparent 74%)',
        }}
      />
      {/* 3. large soft drifting glows (screen = additive light only, never darkens the figure) */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: `radial-gradient(42% 48% at ${g1x}% ${g1y}%, ${BRAND.color.electric}22 0%, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: `radial-gradient(48% 54% at ${g2x}% ${g2y}%, ${BRAND.color.navy}66 0%, transparent 72%)`,
        }}
      />
      {/* 4. faint corner vignette — soft & low-alpha so it barely trims the moving cut at the edges */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `radial-gradient(122% 104% at 50% 46%, transparent 72%, #04060b47 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

/** FigureScene — wraps the ENTIRE figure scene (SceneBed + AmbientMotion + figure) in a MONOTONIC,
 * constant-velocity Ken-Burns. This is the primary freezedetect fix: a monotonic zoom+pan (unlike a
 * sinusoid, which has zero velocity at its extremes) means EVERY frame differs from the previous one
 * across the WHOLE frame — the scrim, glows, particles and figure all shift together, so the per-frame
 * pixel delta over a huge area never drops to the freeze noise floor, even on a long hold over a dark
 * low-detail cut.
 *
 * Safety / legibility: the ramp is applied over the figure's own dur (frame-driven), scale only ever
 * grows (1.00 → 1.16, always >= 1.0 → never shrinks below full frame → no black reveal at the edges),
 * and the linear pan is small (x: +46 → -46px, y: -30 → +30px) so centered content stays centered and
 * legible and never leaves frame (the 1.16 zoom leaves ~153px/86px of horizontal/vertical margin, far
 * more than the ±46/±30px pan). Reveals are untouched — this is layered ON TOP of each figure's own
 * animation, exactly like the inner Drift.
 *
 * FOREGROUND LIGHT SWEEPS (critical): several figure components (BrightLine, CarCutaway, ...) paint
 * their OWN near-black full-frame background, which OCCLUDES the SceneBed behind them — so a monotonic
 * zoom over that near-black diagram still yields sub-threshold luma deltas and freezedetect flags it.
 * The reliable fix is to move a bright element ABOVE the figure: two soft, wide, screen-blended (purely
 * additive → only brightens, never darkens/hides the figure) light bands that travel across the full
 * frame on INCOMMENSURATE periods (2.7s L→R, 3.3s R→L) in opposite directions, so at least one bright
 * band is always raking a large mid-frame area and physically repaints many pixels every single frame,
 * regardless of what the figure draws underneath. Peak alpha is kept modest (0.22 / 0.18) so it reads
 * as a premium "raking light" pass and leaves the figure fully legible (screen over white text stays
 * white; over the dark bed it lifts to a soft sheen). Each band re-enters from off-frame at its wrap so
 * the reset is invisible. This is the layer that guarantees dark/opaque diagram figures clear the gate. */
const FigureScene: React.FC<{dur: number; children: React.ReactNode}> = ({dur, children}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = interpolate(f, [0, Math.max(1, dur - 1)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const scale = 1.0 + 0.16 * p; // 1.00 -> 1.16 linear, monotonic, always >= 1.0
  const x = interpolate(p, [0, 1], [46, -46]); // linear pan across, px
  const y = interpolate(p, [0, 1], [-30, 30]);
  // foreground raking-light sweeps — continuous, constant-velocity, incommensurate periods, opposite
  // directions (see note above). Time-based so velocity is constant on a long hold.
  const t = f / fps;
  const sweepA = interpolate((t % 2.7) / 2.7, [0, 1], [-24, 124]); // % pos, L->R
  const sweepB = interpolate((t % 3.3) / 3.3, [0, 1], [124, -24]); // % pos, R->L
  return (
    <AbsoluteFill
      style={{transformOrigin: '50% 50%', transform: `translate(${x}px, ${y}px) scale(${scale})`}}
    >
      {children}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: `linear-gradient(100deg,
            transparent ${sweepA - 26}%,
            rgba(150,196,255,0.09) ${sweepA - 10}%,
            rgba(206,228,255,0.22) ${sweepA}%,
            rgba(150,196,255,0.09) ${sweepA + 10}%,
            transparent ${sweepA + 26}%)`,
        }}
      />
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: `linear-gradient(80deg,
            transparent ${sweepB - 24}%,
            rgba(140,180,240,0.08) ${sweepB - 9}%,
            rgba(190,214,250,0.18) ${sweepB}%,
            rgba(140,180,240,0.08) ${sweepB + 9}%,
            transparent ${sweepB + 24}%)`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Continuous micro-drift so a figure that has finished counting/revealing still MOVES for its
 * ENTIRE on-screen span (a held stat/quote/tally is otherwise flagged near-still by the freeze
 * detector). This is a perpetual, eased Ken-Burns applied to the figure container (parent of the
 * diagram), layered ON TOP of the figure's own reveal so reveals are untouched.
 *
 * Why it never freezes, even on a 7s hold:
 *  - Motion is TIME-based (t = frame/fps), NOT normalized to the clip duration, so a long hold does
 *    not slow the motion down — velocity is identical on second 1 and second 7.
 *  - Each axis is a SUM of sinusoids at DISTINCT, incommensurate periods (pan x: 7.3s+2.9s,
 *    pan y: 6.1s+2.3s, scale: 9.0s). A single sinusoid has zero velocity at its extremes; summing
 *    incommensurate periods means the three axes are never simultaneously at an extreme, so the
 *    composited frame is always changing. The short ~2-3s micro terms keep per-frame pixel velocity
 *    comfortably above the freezedetect floor across the whole hold.
 *  - Sinusoids are inherently eased (smooth accel/decel) — no linear ramps, no rotation.
 *
 * Legibility / safety: scale stays >= 1.0 (only ever pushes IN, never shrinks -> no black reveal),
 * amplitude is small (x <= +/-17px, y <= +/-11px, scale 1.001..1.035) so centered content stays
 * centered and never leaves frame; the un-drifted SceneBed behind covers any sub-pixel edge. */
const TAU = Math.PI * 2;
const Drift: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps; // seconds — continuous, independent of clip length -> never stops on a hold
  // pan: slow primary sway + faster small micro-term (the micro-term guarantees per-frame velocity)
  const x = 13 * Math.sin((TAU * t) / 7.3) + 4 * Math.sin((TAU * t) / 2.9 + 1.1);
  const y = 8 * Math.cos((TAU * t) / 6.1) + 3 * Math.sin((TAU * t) / 2.3 + 0.6);
  // breathing scale: 1.001 .. 1.035 (always >= 1.0 so the figure never shrinks below full frame)
  const s = 1.018 + 0.017 * Math.sin((TAU * t) / 9.0);
  return (
    <AbsoluteFill style={{transformOrigin: '50% 50%', transform: `translate(${x}px, ${y}px) scale(${s})`}}>
      {children}
    </AbsoluteFill>
  );
};

export const FigureBeats: React.FC<{beats: FigureSpec[]}> = ({beats}) => {
  const {fps} = useVideoConfig();
  const accent = BRAND.color.gold;
  return (
    <>
      {beats.map((b, i) => {
        const dur = Math.max(1, Math.round((b.end - b.start) * fps));
        return (
          <Sequence key={i} from={Math.round(b.start * fps)} durationInFrames={dur} name={`figure-${i}`}>
            <FigureScene dur={dur}>
              <SceneBed />
              <AmbientMotion count={22} intensity={1.12} />
              <Drift>
                {b.kind === 'stat' && (
                  <StatCounter
                    accent={accent}
                    value={b.value}
                    prefix={b.prefix}
                    suffix={b.suffix}
                    decimals={b.decimals ?? 0}
                    label={b.label}
                    topLabel={b.topLabel}
                    dur={dur}
                  />
                )}
                {b.kind === 'timeline' && <Timeline accent={accent} events={b.events} dur={dur} />}
                {b.kind === 'bar' && <BarChart accent={accent} data={b.data} dur={dur} />}
                {/* carsearch / motionkit components: each self-contained full-screen scene, dur in frames */}
                {b.kind === 'brightline' && <BrightLine mode={b.mode} dur={dur} />}
                {b.kind === 'carcutaway' && <CarCutaway mode={b.mode} zones={b.zones} dur={dur} />}
                {b.kind === 'probablecause' && <ProbableCauseMeter outcome={b.outcome} dur={dur} />}
                {b.kind === 'curtilage' && <CurtilageShield dur={dur} />}
                {b.kind === 'statemap' && <StateMap label={b.label} dur={dur} />}
                {b.kind === 'casetimeline_c' && <CaseTimeline events={b.events} dur={dur} />}
                {b.kind === 'carkeylock' && <CarKeyLock dur={dur} />}
                {b.kind === 'numberticker' && (
                  <NumberTicker
                    value={b.value}
                    prefix={b.prefix}
                    suffix={b.suffix}
                    decimals={b.decimals}
                    label={b.label}
                    topLabel={b.topLabel}
                    dur={dur}
                  />
                )}
                {b.kind === 'votetally' && (
                  <VoteTally majority={b.majority} dissent={b.dissent} label={b.label} dur={dur} />
                )}
                {b.kind === 'quote' && <QuoteCard quote={b.quote} attribution={b.attribution} dur={dur} />}
              </Drift>
            </FigureScene>
          </Sequence>
        );
      })}
    </>
  );
};
