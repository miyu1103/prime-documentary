// =====================================================================
// EP35 "hinders" — shared theme & primitives for the bespoke FigureBeats
// (Following the Rule / IRS structuring — civil forfeiture).
//
// Extends the motion3d prototype grammar (prototypes/motion3d/Figures.tsx)
// but obeys the EP35 ANIMATION manifest §5 discipline:
//   - NO sine "breathing" loops, NO orbiting faint light, NO blink.  Motion is
//     ONLY reveal-driven (one-directional eased) or event-driven.
//   - All easing required (spring or Easing.out(cubic)); linear motion banned.
//   - opacity-only reveals banned (always paired with translateY / scale).
//   - Deterministic RNG only (mulberry32); Math.random is banned so Codex can
//     reproduce every frame (manifest §SH.0).
//
// The 3 lanes keep Iowa / Federal / NC strictly separated (manifest §6) so the
// episode never reuses EP33/34 palette.
// =====================================================================
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

// ---- ink / neutrals (shared across lanes) ---------------------------
export const INK = '#ffffff';
export const INK2 = '#c8d2e6';
export const MUTED = '#6b7688';
export const BG = '#06080f';

// ---- 3 narrative lanes (manifest §6 — never mix, never reuse EP33/34) --
export type HinderLane = 'iowa' | 'federal' | 'nc';

export interface LaneTokens {
  /** human label */
  readonly name: string;
  /** primary accent */
  readonly accent: string;
  /** brighter highlight (glows / rims / count-ups) */
  readonly accentHi: string;
  /** desaturated backdrop tint for this lane */
  readonly tint: string;
}

export const LANES: Record<HinderLane, LaneTokens> = {
  // Iowa — Carole's warm amber (the small-town diner / register)
  iowa: {name: 'IOWA', accent: '#f0a830', accentHi: '#ffc862', tint: '#3a2a10'},
  // Federal — cold steel-blue (the government / the statute)
  federal: {name: 'FEDERAL', accent: '#5a86b0', accentHi: '#8fb8de', tint: '#101c2a'},
  // North Carolina — cold green (McLellan / the convenience store)
  nc: {name: 'NORTH CAROLINA', accent: '#2f9f74', accentHi: '#5fd1a0', tint: '#0e2a20'},
};

/** Resolve a lane -> accent, tolerant of a raw accent string being passed. */
export const laneAccent = (laneOrAccent: HinderLane | string): string =>
  (LANES as Record<string, LaneTokens>)[laneOrAccent]?.accent ?? laneOrAccent;

// ---- helpers --------------------------------------------------------
/** seconds -> frames (manifest: never hard-code frame counts) */
export const sec = (fps: number, s: number): number => Math.round(fps * s);

/** deterministic PRNG — manifest §SH.0 (Math.random is banned). */
export const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** per-frame film grain (feTurbulence, seed = frame % N, overlay). */
export const grain = (frame: number, opacity: number): React.CSSProperties => {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>` +
    `<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 131}'/>` +
    `<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>`;
  return {
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svg)}")`,
    backgroundSize: '200px 200px',
    mixBlendMode: 'overlay',
    opacity,
    pointerEvents: 'none',
  };
};

/** scene in/out — opacity paired with translateY (opacity-only is banned). */
export const sceneFade = (frame: number, dur: number): {opacity: number; y: number} => {
  const opacity = interpolate(frame, [0, 10, dur - 12, dur], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame, [0, 10], [16, 0], {extrapolateRight: 'clamp'});
  return {opacity, y};
};

/**
 * A tail-end structural drift the figure can apply AFTER its primary reveal so
 * no ROI ever freezes for >0.67s (manifest §7.2 freeze integrity). One
 * direction, eased — never a sine loop.  Returns px offset for the whole plate.
 */
export const tailDrift = (frame: number, dur: number, amp = 18): number =>
  interpolate(frame, [0, dur], [0, amp], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

// ---- shared backdrop (reveal-driven, NO breathing loop) -------------
export const HinderBackdrop: React.FC<{accent: string; tint?: string}> = ({accent, tint = '#0e1424'}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  // one-directional eased grid drift — replaces the prototype's banned sine drift.
  const drift = interpolate(frame, [0, durationInFrames], [0, 34], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  return (
    <>
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 120% at 50% 30%, ${tint} 0%, #080b14 52%, ${BG} 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.14,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 72px),
            repeating-linear-gradient(90deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 72px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
        }}
      />
      <AbsoluteFill
        style={{
          background: 'radial-gradient(120% 100% at 50% 45%, transparent 45%, rgba(0,0,0,0.66) 100%)',
        }}
      />
    </>
  );
};

// ---- mask-reveal headline (overflow:hidden + translateY, 1-char stagger) ----
export const MaskTitle: React.FC<{
  text: string;
  start?: number; // seconds
  size: number;
  weight?: number;
  serif?: boolean;
  color?: string;
  /** per-char stagger in seconds (default ≈0.045s per manifest OP spec) */
  stagger?: number;
}> = ({text, start = 0, size, weight = 700, serif, color = INK, stagger = 0.045}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const chars = Array.from(text);
  const st = Math.max(1, sec(fps, stagger));
  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        fontFamily: serif ? "'Times New Roman', Georgia, serif" : 'Inter, system-ui, sans-serif',
        fontWeight: weight,
        fontSize: size,
        letterSpacing: serif ? 1 : -0.5,
        color,
        lineHeight: 1.05,
      }}
    >
      {chars.map((ch, i) => {
        const cs = spring({
          frame: frame - sec(fps, start) - i * st,
          fps,
          config: {damping: 16, mass: 1},
        });
        const y = interpolate(cs, [0, 1], [110, 0]);
        const o = interpolate(cs, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}>
            <span style={{display: 'inline-block', transform: `translateY(${y}%)`, opacity: o, whiteSpace: 'pre'}}>
              {ch}
            </span>
          </span>
        );
      })}
    </div>
  );
};

// ---- vignette + grain wrapper an FX layer can drop on top -------------
export const FigureFX: React.FC<{grainOpacity?: number}> = ({grainOpacity = 0.07}) => {
  const frame = useCurrentFrame();
  return (
    <>
      <AbsoluteFill
        style={{background: 'radial-gradient(120% 100% at 50% 45%, transparent 55%, rgba(0,0,0,0.55) 100%)', pointerEvents: 'none'}}
      />
      <AbsoluteFill style={grain(frame, grainOpacity)} />
    </>
  );
};

/**
 * Shared prop contract every FigureBeat accepts.  `lane` selects the palette;
 * `accent` may override it directly.  `dur` is the cut length in frames.
 */
export interface FigureProps {
  lane?: HinderLane;
  accent?: string;
  dur: number;
}

/** Resolve the accent a FigureBeat should paint with. */
export const resolveAccent = (p: {lane?: HinderLane; accent?: string}): string =>
  p.accent ?? (p.lane ? LANES[p.lane].accent : LANES.federal.accent);

export const resolveTokens = (p: {lane?: HinderLane}): LaneTokens =>
  p.lane ? LANES[p.lane] : LANES.federal;
