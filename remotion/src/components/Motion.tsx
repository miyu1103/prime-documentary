import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';

/**
 * Reusable cinematic motion primitives — pure code, $0 (no Midjourney/Runway).
 * The point: make the animatic read as a *moving film*, not a slideshow, by
 * layering continuous camera movement, drifting particles and travelling light
 * under every scene (decisions/0002 §5 "light/dust/grain, slow push-ins").
 */

/** Deterministic 0..1 hash from a string seed, so each scene moves differently. */
const hash01 = (s: string): number => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return ((h >>> 0) % 100000) / 100000;
};

/**
 * Slow Ken-Burns camera: a continuous push-in (or pull-out) plus a gentle pan,
 * direction seeded per scene. Wrap any scene visual to give it life and depth.
 */
export const CameraRig: React.FC<{
  seed?: string;
  intensity?: number;
  children: React.ReactNode;
}> = ({seed = 'pd', intensity = 1, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const a = hash01(seed);
  const b = hash01(`${seed}~`);
  const base = 1.05;
  const amp = 0.1 * intensity;
  const scale = a > 0.5 ? base + amp * p : base + amp * (1 - p);
  // pan a few dozen px in a seeded direction over the whole scene
  const px = (p - 0.5) * 70 * (a - 0.5) * 2 * intensity;
  const py = (p - 0.5) * 46 * (b - 0.5) * 2 * intensity;
  return (
    <AbsoluteFill
      style={{
        transform: `translate(${px}px, ${py}px) scale(${scale})`,
        transformOrigin: '50% 44%',
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/** Drifting dust/light motes that slowly rise and twinkle. Deterministic. */
export const Particles: React.FC<{
  count?: number;
  seed?: string;
  color?: string;
}> = ({count = 30, seed = 'p', color = BRAND.color.electric}) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const t = frame / fps;
  const span = height + 60;
  const dots = Array.from({length: count}, (_, i) => {
    const x0 = random(`${seed}-x-${i}`) * width;
    const y0 = random(`${seed}-y-${i}`) * span;
    const r = 1 + random(`${seed}-r-${i}`) * 2.4;
    const speed = 6 + random(`${seed}-s-${i}`) * 16; // px/sec upward
    const drift = (random(`${seed}-d-${i}`) - 0.5) * 36;
    const y = (((y0 - speed * t) % span) + span) % span;
    const x = x0 + Math.sin((t + i) * 0.6) * drift;
    const tw = 0.25 + 0.45 * (0.5 + 0.5 * Math.sin((frame + i * 13) * 0.08));
    return {x, y, r, o: tw};
  });
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} ${height}`}>
        {dots.map((d, i) => (
          <circle key={i} cx={d.x} cy={d.y} r={d.r} fill={color} opacity={d.o * 0.5} />
        ))}
      </svg>
    </AbsoluteFill>
  );
};

/** A soft pool of light that slowly travels across the frame. */
export const LightSweep: React.FC<{seed?: string; color?: string}> = ({
  seed = 'l',
  color = BRAND.color.electric,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const x = 50 + 30 * Math.sin(p * Math.PI * 2 + hash01(seed) * 6.28);
  const y = 32 + 8 * Math.cos(p * Math.PI * 2);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        background: `radial-gradient(42% 55% at ${x}% ${y}%, ${color}16 0%, transparent 70%)`,
      }}
    />
  );
};

/** Static-ish vignette to seat the eye centre and add depth. */
export const Vignette: React.FC<{strength?: number}> = ({strength = 1}) => (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background: `radial-gradient(120% 100% at 50% 44%, transparent 52%, ${BRAND.color.ink}${
        strength >= 1 ? 'cc' : 'aa'
      } 100%)`,
    }}
  />
);

/** Wrap a scene with the full moving stage: camera + particles + light + vignette. */
export const MovingStage: React.FC<{
  seed: string;
  intensity?: number;
  particles?: number;
  children: React.ReactNode;
}> = ({seed, intensity = 1, particles = 30, children}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
    <CameraRig seed={seed} intensity={intensity}>
      {children}
    </CameraRig>
    <LightSweep seed={seed} />
    <Particles seed={seed} count={particles} />
    <Vignette />
  </AbsoluteFill>
);
