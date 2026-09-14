import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

/**
 * AuroraField — a slow, flowing aurora / nebula background bed for Prime Documentary.
 *
 * Full-screen premium BACKGROUND. It draws an opaque canonical dark base
 * (radial navy → near-black) and layers, in `screen` blend mode, several large soft
 * blurred colour ribbons (electric / navy / silver + a whisper of gold) that undulate
 * and drift via EASED SINUSOIDAL offsets and slowly morphing radial-gradient blobs.
 * Faint particles drift with a motion-blur Trail and the whole aurora "breathes" in
 * brightness. Can be used as an opaque base or (because the aurora is screen-blended)
 * dropped over other content.
 *
 * Fully deterministic (useCurrentFrame + index + remotion `random('seed'+i)` — no
 * Math.random / Date). No motion is ever linear: every drift is a sine of frame,
 * shaped further by eased envelopes. Never fully static.
 */

// --- eased sinusoid: a sine of frame whose phase advances non-linearly, so drift
// gently accelerates and decelerates instead of sweeping at constant speed.
const easedSine = (frame: number, periodFrames: number, phase: number): number => {
  const t = ((frame / periodFrames + phase) % 1 + 1) % 1; // 0..1 phase, wrapped
  const eased = Easing.inOut(Easing.sin)(t); // ease the phase itself
  return Math.sin(eased * Math.PI * 2);
};

type RibbonCfg = {
  color: string;
  opacity: number;
  radius: number; // base blob radius in px
  blur: number; // px
};

// electric / navy / silver, with a single whisper of gold. No gold wash, no sweep.
const RIBBONS: RibbonCfg[] = [
  {color: BRAND.color.electric, opacity: 0.42, radius: 720, blur: 120},
  {color: BRAND.color.navy, opacity: 0.55, radius: 900, blur: 140},
  {color: BRAND.color.silver, opacity: 0.22, radius: 620, blur: 130},
  {color: BRAND.color.electric, opacity: 0.34, radius: 800, blur: 150},
  {color: BRAND.color.gold, opacity: 0.12, radius: 520, blur: 160}, // whisper of gold
  {color: BRAND.color.silver, opacity: 0.16, radius: 560, blur: 120},
];

const Ribbon: React.FC<{i: number; cfg: RibbonCfg; fps: number; w: number; h: number}> = ({
  i,
  cfg,
  fps,
  w,
  h,
}) => {
  const frame = useCurrentFrame();

  // deterministic per-ribbon constants
  const homeX = 0.2 + random('rx' + i) * 0.6; // 0.2..0.8 of width
  const homeY = 0.18 + random('ry' + i) * 0.64; // 0.18..0.82 of height
  const px = random('px' + i); // phase seeds
  const py = random('py' + i);
  const pm = random('pm' + i);
  // long, slow periods (multiple seconds) so the field feels calm and continuous
  const periodX = fps * (14 + random('tx' + i) * 10); // ~14–24s
  const periodY = fps * (17 + random('ty' + i) * 11); // ~17–28s
  const periodM = fps * (9 + random('tm' + i) * 7); // morph ~9–16s

  const driftX = easedSine(frame, periodX, px) * (w * 0.16);
  const driftY = easedSine(frame, periodY, py) * (h * 0.16);
  // morph the blob: radius and roundness pulse (never a hard edge)
  const morph = easedSine(frame, periodM, pm); // -1..1
  const rx = cfg.radius * (1 + morph * 0.22);
  const ry = cfg.radius * (1 - morph * 0.18);

  const cx = homeX * w + driftX;
  const cy = homeY * h + driftY;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        opacity: cfg.opacity,
        filter: `blur(${cfg.blur}px)`,
        background: `radial-gradient(${rx}px ${ry}px at ${cx}px ${cy}px, ${cfg.color} 0%, ${cfg.color}88 34%, transparent 70%)`,
        willChange: 'background, opacity',
      }}
    />
  );
};

const PARTICLE_COLORS = [BRAND.color.white, BRAND.color.electric, BRAND.color.silver, BRAND.color.gold];

const Particles: React.FC<{count: number; fps: number; w: number; h: number}> = ({
  count,
  fps,
  w,
  h,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({length: count}).map((_, i) => {
        const baseX = random('cx' + i);
        const size = 2 + random('sz' + i) * 5;
        const swayAmp = 20 + random('sw' + i) * 46;
        const riseFrames = fps * (26 + random('rf' + i) * 24); // slow vertical drift
        const phase = random('ph' + i);
        const color = PARTICLE_COLORS[i % PARTICLE_COLORS.length];

        // eased vertical drift upward, wrapping continuously
        const prog = (((frame / riseFrames + phase) % 1) + 1) % 1;
        const y = (1 - prog) * (h + 160) - 80;
        // eased horizontal sway (sine of frame — never linear)
        const x = baseX * w + easedSine(frame, fps * 6, phase) * swayAmp;
        // gentle twinkle, always coupled with drift (never opacity-only staging)
        const twinkle = 0.18 + 0.24 * (0.5 + 0.5 * easedSine(frame, fps * 3.2, phase * 1.7));

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: size,
              height: size,
              borderRadius: '50%',
              background: color,
              opacity: twinkle,
              filter: `blur(${0.6 + (i % 3)}px)`,
              boxShadow: `0 0 ${size * 3}px ${color}`,
            }}
          />
        );
      })}
    </>
  );
};

export const AuroraField: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps, width, height} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // gentle overall brightness "breath" — eased, slow, never fully flat
  const breath = 0.9 + 0.16 * (0.5 + 0.5 * easedSine(frame, fps * 11, 0.2));
  // soft settle-in over the first ~1.2s and a whisper-out at the tail so it never pops
  const fadeIn = interpolate(frame, [0, fps * 1.2], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const fadeOut = interpolate(frame, [total - fps, total], [1, 0.82], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  const aura = fadeIn * fadeOut;

  return (
    <AbsoluteFill>
      {/* canonical opaque dark base */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* aurora ribbons — screen-blended, breathing brightness */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'screen',
          opacity: aura,
          filter: `brightness(${breath}) saturate(1.06)`,
          pointerEvents: 'none',
        }}
      >
        {RIBBONS.map((cfg, i) => (
          <Ribbon key={i} i={i} cfg={cfg} fps={fps} w={width} h={height} />
        ))}
      </AbsoluteFill>

      {/* faint drifting particles with a soft motion-blur trail */}
      <AbsoluteFill style={{mixBlendMode: 'screen', opacity: aura * 0.85, pointerEvents: 'none'}}>
        <Trail layers={4} lagInFrames={1.6} trailOpacity={0.55}>
          <Particles count={30} fps={fps} w={width} h={height} />
        </Trail>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
