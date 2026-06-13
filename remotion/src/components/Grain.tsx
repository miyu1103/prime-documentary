import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';

/** Subtle film grain overlay (decisions/0002 §5 "light/dust/grain"). Pure SVG, $0. */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.06}) => {
  const frame = useCurrentFrame();
  const seed = frame % 8; // re-seed to animate the grain
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity, mixBlendMode: 'overlay'}}>
      <svg width="100%" height="100%">
        <filter id={`grain-${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} />
        </filter>
        <rect width="100%" height="100%" filter={`url(#grain-${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};
