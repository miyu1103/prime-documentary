// =====================================================================
// EP35 "hinders" — bespoke FigureBeats (non-hero 19 + 3 hero OffthreadVideo
// wrappers).  "Following the Rule" / IRS structuring — civil forfeiture.
//
// Discipline (manifest EP35_hinders_ANIMATION_ASSETS.v001 §5 / §7):
//   - No new full-scratch re-implementation of an existing capability: every
//     non-hero figure THIN-WRAPS the nearest MOTIONKIT component with data
//     props (CLAUDE invariant 14 / no double-implementation).  Only the 3 truly
//     new concepts (StructuringExplainer, BurdenShiftScale, McLellanStore) and
//     the 3 hero 2D fallbacks are hand-built here.
//   - All motion is eased (spring or Easing.out(cubic)); linear motion banned.
//   - opacity-only reveals banned (always paired with translateY / scaleX).
//   - Multiple elements are staggered; fast moves get @remotion/motion-blur Trail.
//   - freeze integrity: after the primary reveal each figure keeps a *different*
//     structural motion running to the cut end (tailDrift parallax / left→right
//     rule draw) so no ROI ever freezes for >0.67s.
//   - NO sine breathing on OUR layers, NO orbiting faint light, NO blink.
//   - Deterministic RNG only (mulberry32); Math.random banned.
//   - 3 lanes (Iowa amber / Federal steel / NC green) never mixed (LANES).
//
// Facts placed here are VERBATIM (never altered):
//   $32,820.56  → F5 FrozenAccount label + F6 CaseCaptionNameplate caption
//   $107,702.66 → F14c McLellanStore seized label
//   231 cases / $17.1M → F15b LegalSourceBars
//   2014 / 2019 RESPECT Act → F19 RESPECTActNode
// (278 / 91% / 301 / ~$2M live in the Blender/three heroes F15 / F14b, built by
//  the other thread — not in this file.)
// =====================================================================
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  OffthreadVideo,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';

import {
  ComparisonBars,
  EvidenceCard,
  HeadlineStack,
  MechanismReveal,
  NumberTicker,
  ProcessSteps,
  QuoteCard,
  RadialGauge,
  StampReveal,
  YearSweep,
} from '../motionkit';

import {
  FigureFX,
  FigureProps,
  HinderBackdrop,
  HinderLane,
  INK,
  INK2,
  LANES,
  MaskTitle,
  MUTED,
  mulberry32,
  resolveAccent,
  resolveTokens,
  sec,
  tailDrift,
} from './theme';

// Shared easing handle (banned: linear).
const EO = Easing.out(Easing.cubic);

// ---------------------------------------------------------------------
// Hero Blender/3D renders (built by the separate 3D thread).  Until those
// mp4s exist under remotion/public/hinders/, this flag stays FALSE so that
// tsc + a still-render never try to load a missing OffthreadVideo src — the
// 2D fallback below is ALWAYS laid down as the base layer.  Flip to true (or
// gate per-key) once the encodes land.
// ---------------------------------------------------------------------
export const HERO_VIDEO_READY = false;

export const HERO_MP4 = {
  bsa: 'hinders/hero_bsa_flow.mp4',
  frozen: 'hinders/hero_frozen_account.mp4',
  carole: 'hinders/hero_carole_after.mp4',
} as const;

const HeroVideo: React.FC<{srcKey: string}> = ({srcKey}) =>
  HERO_VIDEO_READY ? (
    <AbsoluteFill>
      <OffthreadVideo
        src={staticFile(srcKey)}
        muted
        style={{width: '100%', height: '100%', objectFit: 'cover'}}
      />
    </AbsoluteFill>
  ) : null;

// =====================================================================
// Shared chrome for the MOTIONKIT thin-wraps: adds lane identity + an extra
// independent sustained-motion pair (chip drift + bottom rule draw) ON TOP of
// the MOTIONKIT scene, guaranteeing lane color + freeze integrity without
// forking the component.
// =====================================================================
const LaneChrome: React.FC<{lane?: HinderLane; accent?: string; dur: number; label: string}> = ({
  lane,
  accent,
  dur,
  label,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tok = resolveTokens({lane});
  const ac = accent ?? tok.accent;

  const chip = spring({frame: frame - sec(fps, 0.1), fps, config: {damping: 16, mass: 1}});
  const chipY = interpolate(chip, [0, 1], [120, 0]);
  const chipO = interpolate(chip, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  const drift = tailDrift(frame, dur, 12);
  const rule = interpolate(frame, [sec(fps, 0.3), Math.max(sec(fps, 0.5), dur - sec(fps, 0.2))], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <>
      {/* lane chip (mask-reveal + continuous drift) */}
      <div
        style={{
          position: 'absolute',
          left: 64,
          top: 54,
          transform: `translateY(${drift * 0.35}px)`,
          overflow: 'hidden',
          paddingBottom: '0.24em',
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            transform: `translateY(${chipY}%)`,
            opacity: chipO,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 700,
            fontSize: 22,
            letterSpacing: 4,
            color: ac,
            textTransform: 'uppercase',
            whiteSpace: 'nowrap',
          }}
        >
          {tok.name} · {label}
        </div>
      </div>
      {/* bottom lane rule — draws left→right then keeps drifting to cut end */}
      <div
        style={{
          position: 'absolute',
          left: 64,
          right: 64,
          bottom: 60,
          height: 4,
          transform: `translateX(${drift}px)`,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            height: '100%',
            borderRadius: 2,
            background: ac,
            transformOrigin: 'left center',
            transform: `scaleX(${rule})`,
            boxShadow: `0 0 18px ${ac}aa`,
          }}
        />
      </div>
    </>
  );
};

/** Thin wrap: MOTIONKIT scene + lane chrome + grain/vignette. */
const Wrapped: React.FC<{
  lane?: HinderLane;
  accent?: string;
  dur: number;
  label: string;
  children: React.ReactNode;
}> = ({lane, accent, dur, label, children}) => (
  <AbsoluteFill style={{backgroundColor: '#06080f'}}>
    {children}
    <LaneChrome lane={lane} accent={accent} dur={dur} label={label} />
    <FigureFX />
  </AbsoluteFill>
);

// =====================================================================
// Small hand-built helpers (deterministic, eased) for the 3 new figures
// + the 3 hero 2D fallbacks.
// =====================================================================

/** mask-reveal single line used inside hand-built SVG figures */
const Line: React.FC<{
  text: string;
  start: number; // seconds
  size: number;
  weight?: number;
  color?: string;
  ls?: number;
  serif?: boolean;
}> = ({text, start, size, weight = 700, color = INK, ls = 1, serif}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cs = spring({frame: frame - sec(fps, start), fps, config: {damping: 16, mass: 1}});
  const y = interpolate(cs, [0, 1], [118, 0]);
  const o = interpolate(cs, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <div style={{overflow: 'hidden', paddingBottom: '0.16em'}}>
      <div
        style={{
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: serif ? "'Times New Roman', Georgia, serif" : 'Inter, system-ui, sans-serif',
          fontWeight: weight,
          fontSize: size,
          letterSpacing: ls,
          color,
          whiteSpace: 'pre',
          lineHeight: 1.08,
        }}
      >
        {text}
      </div>
    </div>
  );
};

// =====================================================================
// HERO WRAPPERS (F2 / F5 / F20) — OffthreadVideo over an always-on 2D fallback
// =====================================================================

/** F2 BSAOriginFlow ★ — 1970 BSA money-tracking origin drips into a small store. */
export const BSAOriginFlow: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ac = resolveAccent(p);
  const hi = resolveTokens(p).accentHi;

  // main stream draw (one-directional eased)
  const draw = interpolate(frame, [sec(fps, 0.1), sec(fps, 0.8)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = tailDrift(frame, p.dur, 24);
  const nodePulse = interpolate(frame, [sec(fps, 0.8), sec(fps, 1.4)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 3 droplets travel down the branch, staggered, fast → Trail λ0.9
  const droplets = [0, 1, 2].map((i) => {
    const t = interpolate(frame, [sec(fps, 0.35 + i * 0.16), sec(fps, 0.35 + i * 0.16 + 0.6)], [0, 1], {
      easing: EO,
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return {t, y: 300 + t * 470, x: 960 + Math.sin(t * Math.PI) * 40};
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={resolveTokens(p).tint} />
      <AbsoluteFill style={{transform: `translateY(${-drift * 0.3}px)`}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {/* upstream reservoir → small store: main stream path */}
          <path
            d="M960 190 C 700 340, 1220 520, 960 700"
            fill="none"
            stroke={ac}
            strokeWidth={10}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray="1"
            strokeDashoffset={1 - draw}
            opacity={0.85}
          />
          {/* branch that drips off toward the store node */}
          <path
            d="M960 700 C 940 780, 980 820, 960 900"
            fill="none"
            stroke={hi}
            strokeWidth={6}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray="1"
            strokeDashoffset={1 - Math.max(0, (draw - 0.55) / 0.45)}
            opacity={0.7}
          />
          {/* store node (single decay pulse, no breathing loop) */}
          <circle cx={960} cy={930} r={40 + nodePulse * 10} fill="none" stroke={hi} strokeWidth={4} opacity={0.5 * (1 - nodePulse) + 0.35} />
          <circle cx={960} cy={930} r={22} fill={ac} opacity={0.9} />
        </svg>
      </AbsoluteFill>

      {/* fast droplets with motion blur */}
      <AbsoluteFill>
        <Trail layers={6} lagInFrames={1} trailOpacity={0.42}>
          <AbsoluteFill>
            <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
              {droplets.map((d, i) =>
                d.t > 0 && d.t < 1 ? (
                  <circle key={i} cx={d.x} cy={d.y - drift * 0.3} r={10} fill={hi} opacity={0.9} />
                ) : null,
              )}
            </svg>
          </AbsoluteFill>
        </Trail>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '92px 96px', justifyContent: 'flex-start'}}>
        <Line text="1970 · BANK SECRECY ACT" start={0.1} size={30} color={INK2} ls={3} />
        <Line text="Built to track organized-crime money" start={0.28} size={40} color={INK} weight={800} />
        <div style={{marginTop: 8}}>
          <Line text="CLM-0015 · it reached a small-town till" start={0.46} size={24} color={MUTED} ls={2} />
        </div>
      </AbsoluteFill>

      <HeroVideo srcKey={HERO_MP4.bsa} />
      <FigureFX />
    </AbsoluteFill>
  );
};

/** F5 FrozenAccount ★ — account frozen; ice cracks propagate. Seized $32,820.56. */
export const FrozenAccount: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tok = resolveTokens(p);
  const ac = tok.accent;
  const hi = tok.accentHi;

  const cx = 960;
  const cy = 470;
  const cracks = [-140, -75, -10, 55, 120, 180].map((deg, i) => {
    const rad = (deg * Math.PI) / 180;
    const len = 300 + (i % 3) * 90;
    const t = interpolate(frame, [sec(fps, 0.08 + i * 0.05), sec(fps, 0.08 + i * 0.05 + 0.55)], [0, 1], {
      easing: EO,
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return {x2: cx + Math.cos(rad) * len, y2: cy + Math.sin(rad) * len, t};
  });

  const ring = interpolate(frame, [sec(fps, 0.06), sec(fps, 0.5)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = tailDrift(frame, p.dur, 26);

  // deterministic frost drift (one-directional, no sine loop)
  const rnd = mulberry32(3282056);
  const frost = Array.from({length: 16}, () => ({x: rnd() * 1920, y: rnd() * 1080, s: 0.4 + rnd() * 1.4}));

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={tok.tint} />

      {/* near passbook plate — parallax to cut end */}
      <AbsoluteFill style={{transform: `translate(${drift}px, ${-drift * 0.4}px)`}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          <rect x={640} y={300} width={640} height={360} rx={14} fill="#0c1220" stroke={ac} strokeWidth={2} opacity={0.9} />
          <rect x={640} y={300} width={640} height={70} rx={14} fill={ac} opacity={0.16} />
        </svg>
      </AbsoluteFill>

      {/* frost particles (slow one-directional fall) */}
      <AbsoluteFill>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {frost.map((f, i) => {
            const dy = interpolate(frame, [0, p.dur], [0, 26 + f.s * 34], {easing: EO, extrapolateRight: 'clamp'});
            return <circle key={i} cx={f.x} cy={(f.y + dy) % 1080} r={f.s * 1.6} fill={hi} opacity={0.16} />;
          })}
        </svg>
      </AbsoluteFill>

      {/* cracks propagate — fast → Trail λ0.75 */}
      <AbsoluteFill>
        <Trail layers={5} lagInFrames={1} trailOpacity={0.4}>
          <AbsoluteFill>
            <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
              {cracks.map((c, i) => (
                <line
                  key={i}
                  x1={cx}
                  y1={cy}
                  x2={cx + (c.x2 - cx) * c.t}
                  y2={cy + (c.y2 - cy) * c.t}
                  stroke={hi}
                  strokeWidth={3}
                  strokeLinecap="round"
                  opacity={0.85}
                />
              ))}
              <circle cx={cx} cy={cy} r={20 + ring * 90} fill="none" stroke={ac} strokeWidth={3} opacity={0.5 * (1 - ring)} />
            </svg>
          </AbsoluteFill>
        </Trail>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '0 96px', justifyContent: 'flex-end', paddingBottom: 150}}>
        <Line text="ACCOUNT FROZEN · CLM-0002" start={0.14} size={26} color={INK2} ls={3} />
        <Line text="$32,820.56 seized" start={0.34} size={72} color={INK} weight={800} />
      </AbsoluteFill>

      <HeroVideo srcKey={HERO_MP4.frozen} />
      <FigureFX />
    </AbsoluteFill>
  );
};

/** F20 CaroleAfterCard ★ — the emptied store, back→front dolly, "SOLD" placard. */
export const CaroleAfterCard: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tok = resolveTokens(p);
  const ac = tok.accent;

  // dolly-in (nested perspective frames scale up over the whole cut)
  const dolly = interpolate(frame, [0, p.dur], [1, 1.16], {easing: EO, extrapolateRight: 'clamp'});
  const drift = tailDrift(frame, p.dur, 30);

  // "SOLD" placard drop — fast → Trail λ0.75
  const drop = spring({frame: frame - sec(fps, 0.4), fps, config: {damping: 12, mass: 1}});
  const placardY = interpolate(drop, [0, 1], [-260, 0]);
  const placardRot = interpolate(drop, [0, 1], [-8, -3]);

  const rnd = mulberry32(19850);
  const dust = Array.from({length: 18}, () => ({x: rnd() * 1920, y: rnd() * 1080, s: 0.5 + rnd() * 1.6}));

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={tok.tint} />

      <AbsoluteFill style={{transform: `scale(${dolly}) translateX(${drift * 0.4}px)`, transformOrigin: '50% 60%'}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {/* receding interior planes (parallax depth) */}
          {[0, 1, 2, 3].map((i) => {
            const inset = 120 + i * 150;
            const px = drift * (0.12 + i * 0.06);
            return (
              <rect
                key={i}
                x={inset + px}
                y={inset * 0.5}
                width={1920 - inset * 2}
                height={1080 - inset}
                rx={10}
                fill="none"
                stroke={ac}
                strokeWidth={2}
                opacity={0.1 + i * 0.06}
              />
            );
          })}
        </svg>
      </AbsoluteFill>

      {/* dust motes drifting one direction */}
      <AbsoluteFill>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {dust.map((d, i) => {
            const dx = interpolate(frame, [0, p.dur], [0, 30 + d.s * 26], {easing: EO, extrapolateRight: 'clamp'});
            return <circle key={i} cx={(d.x + dx) % 1920} cy={d.y} r={d.s * 1.4} fill={tok.accentHi} opacity={0.12} />;
          })}
        </svg>
      </AbsoluteFill>

      {/* SOLD placard */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.45}>
          <div
            style={{
              transform: `translateY(${placardY}px) rotate(${placardRot}deg)`,
              padding: '22px 56px',
              background: '#0c1220',
              border: `6px solid ${ac}`,
              borderRadius: 8,
              color: ac,
              fontFamily: 'Inter, system-ui, sans-serif',
              fontWeight: 900,
              fontSize: 120,
              letterSpacing: 10,
              boxShadow: `0 0 40px ${ac}55`,
            }}
          >
            SOLD
          </div>
        </Trail>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '0 96px', justifyContent: 'flex-end', paddingBottom: 120}}>
        <Line text="MRS. LADY'S · CLOSED" start={0.2} size={26} color={INK2} ls={3} />
        <Line text="She sold the restaurant to fight back" start={0.42} size={40} color={INK} weight={800} />
      </AbsoluteFill>

      <HeroVideo srcKey={HERO_MP4.carole} />
      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// NEW SELF-BUILT (F2b / F5b / F14c)
// =====================================================================

/** F2b StructuringExplainer — deposits kept under $10,000 = a crime (§5324). */
export const StructuringExplainer: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tok = resolveTokens(p);
  const ac = tok.accent;
  const hi = tok.accentHi;

  const thresholdY = 360;
  // illustrative sub-threshold deposits (structuring pattern; $10k line is the fact)
  const deposits = [9700, 9500, 9800, 9400, 9600];
  const baseY = 760;
  const drawLine = interpolate(frame, [sec(fps, 0.15), sec(fps, 0.7)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fill = interpolate(frame, [sec(fps, 1.1), Math.max(sec(fps, 1.6), p.dur - sec(fps, 0.3))], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = tailDrift(frame, p.dur, 16);

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={tok.tint} />

      <AbsoluteFill style={{transform: `translateY(${-drift * 0.2}px)`}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {/* $10,000 reporting threshold line (draws left→right) */}
          <line
            x1={300}
            y1={thresholdY}
            x2={300 + 1320 * drawLine}
            y2={thresholdY}
            stroke={hi}
            strokeWidth={4}
            strokeDasharray="14 10"
            opacity={0.9}
          />
          {/* deposit bars, staggered, each just under the line — fast → Trail */}
          {deposits.map((amt, i) => {
            const cs = spring({frame: frame - sec(fps, 0.4 + i * 0.12), fps, config: {damping: 17, mass: 1}});
            const h = interpolate(cs, [0, 1], [0, baseY - thresholdY - 30]);
            const x = 420 + i * 230;
            return (
              <g key={i}>
                <rect x={x} y={baseY - h} width={150} height={h} rx={6} fill={ac} opacity={0.85} />
                <text x={x + 75} y={baseY - h - 16} fill={INK2} fontSize={26} fontFamily="Inter, sans-serif" textAnchor="middle">
                  {`$${amt.toLocaleString()}`}
                </text>
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '92px 96px', justifyContent: 'flex-start'}}>
        <Line text="THE $10,000 REPORTING THRESHOLD" start={0.12} size={30} color={hi} ls={3} />
        <Line text="Keep every deposit just under it…" start={0.3} size={46} color={INK} weight={800} />
      </AbsoluteFill>

      {/* filling "= a crime" label sweep (bottom) */}
      <div style={{position: 'absolute', left: 96, right: 96, bottom: 150, transform: `translateX(${drift}px)`}}>
        <div style={{position: 'relative', height: 62, borderRadius: 8, overflow: 'hidden', border: `2px solid ${ac}66`}}>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: `linear-gradient(90deg, ${ac}dd, ${hi})`,
              transformOrigin: 'left center',
              transform: `scaleX(${fill})`,
            }}
          />
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              paddingLeft: 26,
              color: INK,
              fontFamily: 'Inter, sans-serif',
              fontWeight: 800,
              fontSize: 32,
              letterSpacing: 2,
            }}
          >
            …AND THAT ITSELF IS A CRIME — 31 U.S.C. §5324
          </div>
        </div>
      </div>

      <FigureFX />
    </AbsoluteFill>
  );
};

/** F5b BurdenShiftScale — burden of proof flips onto the owner. */
export const BurdenShiftScale: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tok = resolveTokens(p);
  const ac = tok.accent;
  const hi = tok.accentHi;

  // beam rotates: level → tipped so the OWNER pan drops (burden lands on owner)
  const rot = spring({frame: frame - sec(fps, 0.35), fps, config: {damping: 14, mass: 1.1}});
  const beamDeg = interpolate(rot, [0, 1], [-9, 12]); // gov side up → owner side down
  const cx = 960;
  const cy = 430;
  const arm = 320;
  const leftY = cy + Math.sin((beamDeg * Math.PI) / 180) * -arm * 0.0; // computed in group rotate
  void leftY;

  // burden weight drops onto owner pan — fast → Trail
  const drop = spring({frame: frame - sec(fps, 0.6), fps, config: {damping: 12, mass: 1}});
  const weightY = interpolate(drop, [0, 1], [-320, 0]);

  const fill = interpolate(frame, [sec(fps, 1.0), Math.max(sec(fps, 1.5), p.dur - sec(fps, 0.3))], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = tailDrift(frame, p.dur, 14);
  const fulcrumGlow = interpolate(frame, [sec(fps, 0.35), sec(fps, 0.9)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={tok.tint} />

      <AbsoluteFill style={{transform: `translateY(${-drift * 0.2}px)`}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {/* fulcrum + single decay glow */}
          <polygon points={`${cx - 40},${cy + 140} ${cx + 40},${cy + 140} ${cx},${cy}`} fill="#0c1220" stroke={ac} strokeWidth={3} />
          <circle cx={cx} cy={cy} r={16 + fulcrumGlow * 8} fill={hi} opacity={0.5 * (1 - fulcrumGlow) + 0.4} />

          {/* rotating beam + two pans */}
          <g transform={`rotate(${beamDeg} ${cx} ${cy})`}>
            <line x1={cx - arm} y1={cy} x2={cx + arm} y2={cy} stroke={ac} strokeWidth={10} strokeLinecap="round" />
            {/* government pan (left) */}
            <line x1={cx - arm} y1={cy} x2={cx - arm} y2={cy + 90} stroke={ac} strokeWidth={3} />
            <path d={`M ${cx - arm - 70} ${cy + 90} A 70 40 0 0 0 ${cx - arm + 70} ${cy + 90} Z`} fill={ac} opacity={0.25} stroke={ac} strokeWidth={2} />
            <text x={cx - arm} y={cy + 74} fill={INK} fontSize={24} fontFamily="Inter, sans-serif" fontWeight={700} textAnchor="middle">
              GOVERNMENT
            </text>
            {/* owner pan (right) */}
            <line x1={cx + arm} y1={cy} x2={cx + arm} y2={cy + 90} stroke={hi} strokeWidth={3} />
            <path d={`M ${cx + arm - 70} ${cy + 90} A 70 40 0 0 0 ${cx + arm + 70} ${cy + 90} Z`} fill={hi} opacity={0.3} stroke={hi} strokeWidth={2} />
            <text x={cx + arm} y={cy + 74} fill={INK} fontSize={24} fontFamily="Inter, sans-serif" fontWeight={700} textAnchor="middle">
              OWNER
            </text>
          </g>
        </svg>
      </AbsoluteFill>

      {/* burden weight dropping onto the owner side */}
      <AbsoluteFill>
        <Trail layers={5} lagInFrames={1} trailOpacity={0.4}>
          <AbsoluteFill>
            <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
              <rect x={cx + arm - 46} y={cy + 20 + weightY} width={92} height={64} rx={8} fill={hi} opacity={0.92} />
            </svg>
          </AbsoluteFill>
        </Trail>
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '92px 96px', justifyContent: 'flex-start'}}>
        <Line text="CIVIL FORFEITURE" start={0.12} size={30} color={INK2} ls={3} />
        <Line text="The burden of proof flips" start={0.3} size={46} color={INK} weight={800} />
      </AbsoluteFill>

      <div style={{position: 'absolute', left: 96, right: 96, bottom: 150, transform: `translateX(${drift}px)`}}>
        <div style={{position: 'relative', height: 62, borderRadius: 8, overflow: 'hidden', border: `2px solid ${hi}66`}}>
          <div style={{position: 'absolute', inset: 0, background: `linear-gradient(90deg, ${ac}dd, ${hi})`, transformOrigin: 'left center', transform: `scaleX(${fill})`}} />
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', paddingLeft: 26, color: INK, fontFamily: 'Inter, sans-serif', fontWeight: 800, fontSize: 32, letterSpacing: 3}}>
            NOW YOU MUST PROVE IT INNOCENT
          </div>
        </div>
      </div>

      <FigureFX />
    </AbsoluteFill>
  );
};

/** F14c McLellanStore — rural NC convenience store; small tender lights up. Seized $107,702.66. */
export const McLellanStore: React.FC<FigureProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // NC lane by nature, but honor an explicit lane/accent override.
  const tok = p.lane || p.accent ? resolveTokens(p) : LANES.nc;
  const ac = p.accent ?? tok.accent;
  const hi = tok.accentHi;

  const dolly = interpolate(frame, [0, p.dur], [1, 1.14], {easing: EO, extrapolateRight: 'clamp'});
  const drift = tailDrift(frame, p.dur, 24);
  const registerGlow = interpolate(frame, [sec(fps, 0.5), sec(fps, 1.0)], [0, 1], {
    easing: EO,
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const tender = [
    {label: 'GAS', amt: '$18.40'},
    {label: 'CIGARETTES', amt: '$6.25'},
    {label: 'LOTTERY', amt: '$2.00'},
  ];

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <HinderBackdrop accent={ac} tint={tok.tint} />

      {/* interior dolly-in with parallax shelves */}
      <AbsoluteFill style={{transform: `scale(${dolly}) translateX(${drift * 0.3}px)`, transformOrigin: '50% 58%'}}>
        <svg width="100%" height="100%" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice">
          {[0, 1, 2].map((i) => {
            const inset = 160 + i * 170;
            const px = drift * (0.14 + i * 0.08);
            return (
              <rect key={i} x={inset + px} y={inset * 0.5} width={1920 - inset * 2} height={1000 - inset} rx={8} fill="none" stroke={ac} strokeWidth={2} opacity={0.12 + i * 0.07} />
            );
          })}
          {/* register / counter */}
          <rect x={760} y={640} width={400} height={150} rx={10} fill="#0c1220" stroke={ac} strokeWidth={2} />
          <rect x={860} y={600} width={200} height={54} rx={6} fill={hi} opacity={0.2 + registerGlow * 0.5} />
        </svg>
      </AbsoluteFill>

      {/* small-tender chips light up, staggered */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', gap: 18, flexDirection: 'row', paddingTop: 40}}>
        {tender.map((t, i) => {
          const cs = spring({frame: frame - sec(fps, 0.7 + i * 0.18), fps, config: {damping: 16, mass: 1}});
          const y = interpolate(cs, [0, 1], [40, 0]);
          const o = interpolate(cs, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
          return (
            <div
              key={i}
              style={{
                transform: `translateY(${y}px)`,
                opacity: o,
                padding: '12px 22px',
                borderRadius: 8,
                border: `2px solid ${hi}`,
                background: `${ac}22`,
                color: INK,
                fontFamily: 'Inter, sans-serif',
                fontWeight: 700,
                fontSize: 26,
                boxShadow: `0 0 20px ${hi}44`,
              }}
            >
              {t.label} · {t.amt}
            </div>
          );
        })}
      </AbsoluteFill>

      <AbsoluteFill style={{padding: '0 96px', justifyContent: 'flex-end', paddingBottom: 130}}>
        <Line text="McLELLAN'S · NORTH CAROLINA" start={0.16} size={26} color={INK2} ls={3} />
        <Line text="Nickel-and-dime cash — then $107,702.66 seized" start={0.4} size={44} color={INK} weight={800} />
      </AbsoluteFill>

      <FigureFX />
    </AbsoluteFill>
  );
};

// =====================================================================
// NON-HERO THIN-WRAPS (MOTIONKIT + lane chrome)
// =====================================================================

/** F1 Register38Years → NumberTicker */
export const Register38Years: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="THE REGISTER">
    <NumberTicker value={38} suffix="yrs" topLabel="Behind the counter" label="38 years · an all-cash trade" dur={p.dur} />
  </Wrapped>
);

/** F4 ThresholdBreach → MechanismReveal faultsplit (crack along the line) */
export const ThresholdBreach: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="$10,000 LINE BREACHED">
    <MechanismReveal kind="faultsplit" dur={p.dur} />
  </Wrapped>
);

/** F6 CaseCaptionNameplate → EvidenceCard (in-rem caption, $32,820.56 verbatim) */
export const CaseCaptionNameplate: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="IN REM">
    <EvidenceCard tag="IN REM" caption="United States v. $32,820.56 · CLM-0002" dur={p.dur} />
  </Wrapped>
);

/** F7 WalkAwayTally → ProcessSteps (the decision to abandon the claim) */
export const WalkAwayTally: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="MOST NEVER FIGHT">
    <ProcessSteps
      steps={[
        {title: 'Seizure notice', desc: 'Your money is gone'},
        {title: 'Legal cost > claim', desc: 'Fighting costs more than it is worth'},
        {title: 'Walk away', desc: 'So most owners give up'},
      ]}
      dur={p.dur}
    />
  </Wrapped>
);

/** F8 CivilForfeitureInvert → MechanismReveal gears (the machinery of the flip) */
export const CivilForfeitureInvert: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="INNOCENT UNTIL… REVERSED">
    <MechanismReveal kind="gears" dur={p.dur} />
  </Wrapped>
);

/** F9 CoinFlip → RadialGauge (outcome left to chance) */
export const CoinFlip: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="LEFT TO CHANCE">
    <RadialGauge value={50} max={100} label="Your odds · a coin toss" dur={p.dur} />
  </Wrapped>
);

/** F10 HeadlineKinetic → HeadlineStack (NYT 2014-10-25, direct quote allowed) */
export const HeadlineKinetic: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="THE PRESS NOTICED">
    <HeadlineStack
      headlines={[
        'Law Lets I.R.S. Seize Accounts on Suspicion, No Crime Required',
        'No charges. No conviction. Just a bank record.',
        'Small businesses drained by structuring seizures',
      ]}
      dur={p.dur}
    />
  </Wrapped>
);

/** F12 SeizureVsReturn → ComparisonBars (seized, then returned in full) */
export const SeizureVsReturn: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="TAKEN → RETURNED">
    <ComparisonBars
      items={[
        {label: 'Seized (100%)', value: 100, accent: LANES.federal.accent},
        {label: 'Returned (100%)', value: 100, accent: LANES.iowa.accent},
      ]}
      dur={p.dur}
    />
  </Wrapped>
);

/** F13 DismissedStamp → StampReveal */
export const DismissedStamp: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="WITHOUT PREJUDICE">
    <StampReveal text="DISMISSED WITHOUT PREJUDICE" color={resolveAccent(p)} dur={p.dur} />
  </Wrapped>
);

/** F15b LegalSourceBars → ComparisonBars (231 cases / $17.1M — TIGTA) */
export const LegalSourceBars: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="LEGAL-SOURCE SEIZURES">
    <ComparisonBars
      items={[
        {label: 'TIGTA cases', value: 231, accent: LANES.federal.accent},
        {label: 'Seized ($ millions)', value: 17.1, accent: LANES.federal.accentHi},
      ]}
      dur={p.dur}
    />
  </Wrapped>
);

/** F16 FeeDeniedCard → EvidenceCard (8th Cir. 2016 fee denial) */
export const FeeDeniedCard: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="8TH CIR. 2016">
    <EvidenceCard tag="8TH CIR. 2016" caption="Attorney fees DENIED · CLM-0011" dur={p.dur} />
  </Wrapped>
);

/** F17 ThreatReframeCard → QuoteCard ("still on the books" threat re-hook) */
export const ThreatReframeCard: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="STILL ON THE BOOKS">
    <QuoteCard quote="The law that did this is still on the books." attribution="Civil forfeiture — still in force today" dur={p.dur} />
  </Wrapped>
);

/** F17b FeeContrastCard → ComparisonBars (McLellan fees paid vs Carole fees denied) */
export const FeeContrastCard: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="SAME LAW · SPLIT OUTCOME">
    <ComparisonBars
      items={[
        {label: 'McLellan — FEES PAID', value: 1, accent: LANES.nc.accent},
        {label: 'Carole — FEES DENIED', value: 1, accent: LANES.iowa.accent},
      ]}
      dur={p.dur}
    />
  </Wrapped>
);

/** F18 CongressHearingCard → EvidenceCard (2015 hearing; NO verbatim testimony) */
export const CongressHearingCard: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="2015 HEARING">
    <EvidenceCard tag="CONGRESSIONAL HEARING · 2015" caption="Testimony on the record · CLM-0020" dur={p.dur} />
  </Wrapped>
);

/** F19 RESPECTActNode → YearSweep (2014 policy shift → 2019 RESPECT Act) */
export const RESPECTActNode: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="A LIMITED FIX">
    <YearSweep from={2014} to={2019} label="RESPECT Act · 2019 · CLM-0016" dur={p.dur} />
  </Wrapped>
);

/** F21 InfoDensitySpine → ProcessSteps (ED bridge — next-episode open loop) */
export const InfoDensitySpine: React.FC<FigureProps> = (p) => (
  <Wrapped lane={p.lane} accent={p.accent} dur={p.dur} label="WHAT COMES NEXT">
    <ProcessSteps
      steps={[
        {title: 'The rule remains', desc: 'Structuring is still a crime'},
        {title: 'The tool remains', desc: 'Civil forfeiture is still in force'},
        {title: 'Next', desc: 'Who does the state target now?'},
      ]}
      dur={p.dur}
    />
  </Wrapped>
);
