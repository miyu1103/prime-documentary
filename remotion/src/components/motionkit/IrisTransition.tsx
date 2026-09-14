import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

/**
 * IrisTransition — cinematic iris wipe rendered as a full-screen `BRAND.color.ink`
 * cover with a growing / shrinking soft-edged hole (SVG mask, circle or diamond),
 * centered on frame. `mode='out'` closes the iris (hole shrinks to reveal ink);
 * `mode='in'` opens it (hole grows from 0). A thin electric rim glow rides the hole
 * edge (motion-blurred via Trail) and the radius rides a spring with a subtle eased
 * overshoot. Transparent transition OVERLAY — draws only the ink mask; never linear;
 * fully deterministic from the current frame.
 */

const clamp01 = (v: number): number => Math.max(0, Math.min(1, v));

type Openness = {openness: number; raw: number};

// Pure (non-hook) spring evaluation shared by the ink mask and the rim edge so the
// hole and its glow stay perfectly registered across Trail's time-shifted layers.
const evalIris = (
  frame: number,
  fps: number,
  runDur: number,
  mode: 'in' | 'out',
): Openness => {
  const raw = spring({
    frame,
    fps,
    durationInFrames: runDur,
    config: {damping: 14, mass: 0.9, stiffness: 120, overshootClamping: false},
  });
  // 'in' opens the hole (0 -> 1); 'out' closes it (1 -> 0). Overshoot is allowed to
  // sail past 1 (off-screen) and is clamped at 0 so the ink never inverts.
  const openness = mode === 'in' ? raw : 1 - raw;
  return {openness: Math.max(0, openness), raw};
};

// Renders the correct hole geometry (soft blur applied by the caller's filter/stroke).
const IrisShape: React.FC<
  {
    shape: 'circle' | 'diamond';
    cx: number;
    cy: number;
    r: number;
  } & React.SVGProps<SVGGeometryElement>
> = ({shape, cx, cy, r, ...svgProps}) => {
  if (shape === 'diamond') {
    const points = `${cx},${cy - r} ${cx + r},${cy} ${cx},${cy + r} ${cx - r},${cy}`;
    return (
      <polygon
        points={points}
        strokeLinejoin="round"
        {...(svgProps as React.SVGProps<SVGPolygonElement>)}
      />
    );
  }
  return (
    <circle
      cx={cx}
      cy={cy}
      r={Math.max(0, r)}
      {...(svgProps as React.SVGProps<SVGCircleElement>)}
    />
  );
};

// The electric rim glow. Kept as its own frame-reading component so Trail can
// re-render it at lagged frames and smear the fast-moving edge into motion blur.
const RimEdge: React.FC<{
  mode: 'in' | 'out';
  shape: 'circle' | 'diamond';
  runDur: number;
}> = ({mode, shape, runDur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const cx = width / 2;
  const cy = height / 2;
  const maxR = Math.hypot(cx, cy) * 1.05;

  const {openness, raw} = evalIris(frame, fps, runDur, mode);
  const r = openness * maxR;

  // Rim brightness rides a smooth bell so the glow blooms while the edge travels
  // and fades to nothing at the fully-open / fully-closed rest states.
  const bell = Math.sin(clamp01(raw) * Math.PI);
  const glowOpacity = interpolate(bell, [0, 1], [0, 0.9], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const coreOpacity = interpolate(bell, [0, 1], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{position: 'absolute', inset: 0}}
      >
        <defs>
          <filter id="iris-rim-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation={12} />
          </filter>
        </defs>
        {/* Wide soft bloom */}
        <IrisShape
          shape={shape}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={BRAND.color.electric}
          strokeWidth={11}
          opacity={glowOpacity}
          filter="url(#iris-rim-glow)"
        />
        {/* Crisp electric line on the exact edge */}
        <IrisShape
          shape={shape}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={BRAND.color.electric}
          strokeWidth={3}
          opacity={coreOpacity}
        />
        {/* Hairline white highlight for a premium specular edge */}
        <IrisShape
          shape={shape}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={BRAND.color.white}
          strokeWidth={1.25}
          opacity={coreOpacity * 0.55}
        />
      </svg>
    </AbsoluteFill>
  );
};

export const IrisTransition: React.FC<{
  mode?: 'in' | 'out';
  shape?: 'circle' | 'diamond';
  dur?: number;
}> = ({mode = 'out', shape = 'circle', dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const runDur = dur ?? durationInFrames;

  const cx = width / 2;
  const cy = height / 2;
  const maxR = Math.hypot(cx, cy) * 1.05;

  const {openness} = evalIris(frame, fps, runDur, mode);
  const r = openness * maxR;

  // Soft mask edge feathers a touch wider as the hole opens, for a filmic falloff.
  const feather = interpolate(clamp01(openness), [0, 1], [9, 24], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {/* Ink cover with a soft-edged hole punched out (black in mask = transparent). */}
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{position: 'absolute', inset: 0}}
      >
        <defs>
          <filter
            id="iris-feather"
            x="-30%"
            y="-30%"
            width="160%"
            height="160%"
          >
            <feGaussianBlur stdDeviation={feather} />
          </filter>
          <mask id="iris-hole" maskUnits="userSpaceOnUse">
            <rect x={0} y={0} width={width} height={height} fill="#ffffff" />
            <g filter="url(#iris-feather)">
              <IrisShape shape={shape} cx={cx} cy={cy} r={r} fill="#000000" />
            </g>
          </mask>
        </defs>
        <rect
          x={0}
          y={0}
          width={width}
          height={height}
          fill={BRAND.color.ink}
          mask="url(#iris-hole)"
        />
      </svg>

      {/* Motion-blurred electric rim tracking the hole edge. */}
      <Trail layers={5} lagInFrames={1.4} trailOpacity={0.55}>
        <RimEdge mode={mode} shape={shape} runDur={runDur} />
      </Trail>
    </AbsoluteFill>
  );
};
