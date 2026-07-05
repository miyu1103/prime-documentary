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

/** SceneBed — a DESIGNED scene bed behind every figure so it never reads as text floating on flat
 * black. Layers a deep-navy radial ground + two large soft glows that slowly drift (deterministic,
 * frame-driven) + a faint vignette. All extra light is `screen`-blended (it only ADDS light, so it
 * can never wash out or lower contrast on the figure), and the vignette darkens the EDGES only,
 * seating the central figure. The figure itself renders on top (inside <Drift>) and is untouched. */
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
      {/* deep navy radial ground */}
      <AbsoluteFill
        style={{background: `radial-gradient(125% 108% at 50% 40%, ${BRAND.color.navy} 0%, #071019 58%, #05070d 100%)`}}
      />
      {/* large soft drifting glows (screen = additive light only, never darkens the figure) */}
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
      {/* faint vignette — darkens edges only, seats the central figure */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `radial-gradient(120% 100% at 50% 46%, transparent 55%, #04060baa 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};

/** Continuous micro-drift so a figure that has finished counting still MOVES (a held stat is
 * otherwise flagged near-still by animation_density). Slow parallax pan + breathing scale. */
const Drift: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const p = interpolate(f, [0, d], [0, 1], {extrapolateRight: 'clamp'});
  const x = Math.sin(p * Math.PI * 2) * 14;
  const y = Math.cos(p * Math.PI * 2) * 9;
  const s = 1.015 + 0.02 * p; // gentle continuous push-in
  return (
    <AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${s})`}}>{children}</AbsoluteFill>
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
            <AbsoluteFill>
              <SceneBed />
              <AmbientMotion count={18} intensity={1.05} />
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
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </>
  );
};
