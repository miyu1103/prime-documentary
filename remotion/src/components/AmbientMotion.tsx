import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

/**
 * AmbientMotion — procedural, on-brand motion graphics composited over every beat so no frame is ever
 * static (kills the "still slideshow" look). No external stock: everything is drawn and animated here,
 * fully deterministic (index + frame only, no Math.random), screen-blended, tasteful and subtle.
 *
 * Two layers:
 *  - drifting bokeh particles (navy/cyan/pale-gold), rising with a gentle horizontal sway
 *  - two large soft glows slowly orbiting for volumetric depth
 * Palette stays navy / electric-blue / restrained gold — never a yellow wash or a vertical gold sweep.
 */

const PARTICLE_COLORS = ['#eaf2ff', BRAND.color.electric, '#cfe0ff', '#e9c98a'];

const Particle: React.FC<{i: number}> = ({i}) => {
  const frame = useCurrentFrame();
  const {durationInFrames: d, height} = useVideoConfig();
  // deterministic per-particle constants
  const baseX = ((i * 137.5) % 100) / 100; // golden-angle spread across width
  const size = 4 + ((i * 7) % 13);
  const speed = 0.5 + ((i * 13) % 10) / 10; // 0.5–1.4
  const swayAmp = 18 + ((i * 11) % 40);
  const colr = PARTICLE_COLORS[i % PARTICLE_COLORS.length];
  const startY = 1 - ((i * 0.19) % 1); // 0..1 down the frame
  // rise upward over the beat, wrapping, with a horizontal sine sway
  const prog = (startY - (frame / d) * speed * 0.9) % 1;
  const y = ((prog < 0 ? prog + 1 : prog)) * (height + 120) - 60;
  // faster sway + twinkle so every frame changes enough to clear the freezedetect
  // noise floor even over a slow footage clip (animation_density: no near-still > 3s).
  const x = baseX * 1080 + Math.sin(frame / 15 + i) * (swayAmp + 10);
  const twinkle = 0.32 + 0.32 * (0.5 + 0.5 * Math.sin(frame / 10 + i * 1.7));
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: size,
        height: size,
        borderRadius: '50%',
        background: colr,
        opacity: twinkle,
        filter: `blur(${1 + (i % 4)}px)`,
        boxShadow: `0 0 ${size * 2}px ${colr}`,
      }}
    />
  );
};

const Glow: React.FC<{i: number; color: string; size: number; opacity: number}> = ({
  i,
  color,
  size,
  opacity,
}) => {
  const frame = useCurrentFrame();
  // slow lissajous orbit
  const cx = 540 + Math.sin(frame / 90 + i * 2) * 320;
  const cy = 900 + Math.cos(frame / 70 + i * 3) * 520;
  return (
    <div
      style={{
        position: 'absolute',
        left: cx - size / 2,
        top: cy - size / 2,
        width: size,
        height: size,
        borderRadius: '50%',
        background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
        opacity,
        pointerEvents: 'none',
      }}
    />
  );
};

export const AmbientMotion: React.FC<{count?: number; intensity?: number}> = ({
  count = 16,
  intensity = 1,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  // fade the whole layer in over the first ~8 frames of each beat so cuts feel clean
  const fade = interpolate(frame, [0, 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const out = interpolate(frame, [d - 8, d], [1, 0.8], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none', opacity: fade * out * intensity}}>
      <Glow i={0} color={BRAND.color.electric} size={1100} opacity={0.1} />
      <Glow i={1} color={BRAND.color.navy} size={1300} opacity={0.14} />
      {Array.from({length: count}).map((_, i) => (
        <Particle key={i} i={i} />
      ))}
    </AbsoluteFill>
  );
};
