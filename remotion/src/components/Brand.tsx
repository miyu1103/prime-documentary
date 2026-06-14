import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';

/**
 * Vector "PD" monogram — primary logo reproduction (decisions/0002 §G).
 * If assets/brand/pd-logo.png is wired via staticFile later, composite it on top;
 * the vector keeps everything crisp and works before the PNG arrives.
 */
export const PdMonogram: React.FC<{size?: number; opacity?: number}> = ({
  size = 220,
  opacity = 1,
}) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      style={{opacity, overflow: 'visible'}}
    >
      {/* sun/horizon mark behind the monogram */}
      <circle cx="50" cy="46" r="26" fill="none" stroke={BRAND.color.gold} strokeWidth="2.5" />
      <line x1="6" y1="72" x2="94" y2="72" stroke={BRAND.color.gold} strokeWidth="2.5" />
      <text
        x="50"
        y="56"
        textAnchor="middle"
        fontFamily={BRAND.font.display}
        fontSize="34"
        fontWeight={900}
        fill={BRAND.color.white}
        letterSpacing="-2"
      >
        PD
      </text>
    </svg>
  );
};

/** Optional PNG logo composite (only renders if the file is present at build time). */
export const PdLogoImage: React.FC<{src?: string; size?: number}> = ({
  src = 'brand/pd-logo.png',
  size = 220,
}) => {
  try {
    return <Img src={staticFile(src)} style={{width: size, height: 'auto'}} />;
  } catch {
    return <PdMonogram size={size} />;
  }
};

/** Gold horizon line with a soft electric-blue glow. `y` is 0..1 of height. */
export const Horizon: React.FC<{y: number; glow?: boolean}> = ({y, glow = true}) => (
  <AbsoluteFill>
    <div
      style={{
        position: 'absolute',
        top: `${y * 100}%`,
        left: 0,
        right: 0,
        height: 3,
        background: BRAND.color.gold,
        boxShadow: glow ? `0 0 60px 8px ${BRAND.color.electric}` : undefined,
      }}
    />
  </AbsoluteFill>
);
