import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

/**
 * AmbientMotion — procedural, on-brand motion graphics composited over every beat so no frame is ever
 * static (kills the "still slideshow" look). No external stock: everything is drawn and animated here,
 * fully deterministic (index + frame only, no Math.random), screen-blended, tasteful and subtle.
 *
 * One layer (the orbiting glows were removed 2026-07-06 — owner found the slow-circling
 * faint light overused/annoying):
 *  - drifting bokeh particles (navy/cyan/pale-gold), rising with a gentle horizontal sway
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
      {/* The two large orbiting glows that used to sit here were removed — owner 2026-07-06
          found the "淡い光がくるくる回ってる" (slow-orbiting faint light) overused/annoying.
          Only the rising bokeh particles remain: they travel vertically, never circle. */}
      {Array.from({length: count}).map((_, i) => (
        <Particle key={i} i={i} />
      ))}
    </AbsoluteFill>
  );
};
