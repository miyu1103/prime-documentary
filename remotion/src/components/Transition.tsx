import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {BRAND} from '../brand';

/**
 * A gold-bar wipe transition (decisions/0002 §5 "mask reveals / match cuts").
 * Sweeps a bar across the frame over `durationFrames`. Pure code, $0.
 */
export const WipeTransition: React.FC<{durationFrames?: number}> = ({durationFrames = 18}) => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, durationFrames], [-20, 120], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: `${x}%`,
          width: '40%',
          background: `linear-gradient(90deg, transparent, ${BRAND.color.gold}, transparent)`,
          transform: 'skewX(-12deg)',
        }}
      />
    </AbsoluteFill>
  );
};
