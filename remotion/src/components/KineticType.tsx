import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

export type KineticLine = {
  text: string;
  emphasis?: boolean;
  /** frame offset (relative to this component) when the line enters. */
  at: number;
};

/** Staggered kinetic typography — lines spring up and fade in (decisions/0002 §5). */
export const KineticType: React.FC<{
  lines: KineticLine[];
  align?: 'center' | 'flex-start';
}> = ({lines, align = 'center'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at 50% 45%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 80%)`,
        justifyContent: 'center',
        alignItems: align,
        padding: 120,
        gap: 18,
      }}
    >
      {lines.map((l, i) => {
        const local = frame - l.at;
        const enter = spring({frame: local, fps, config: {damping: 18, stiffness: 120, mass: 0.7}});
        const dir = i % 2 === 0 ? 1 : -1;
        const y   = interpolate(enter, [0, 1], [60, 0]);
        const x   = interpolate(enter, [0, 1], [dir * 40, 0]);
        const sc  = interpolate(enter, [0, 1], [0.82, 1]);
        return (
          <div
            key={i}
            style={{
              transform: `translate(${x}px, ${y}px) scale(${sc})`,
              opacity: Math.min(enter * 1.5, 1),
              color: l.emphasis ? BRAND.color.gold : BRAND.color.white,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: l.emphasis ? 88 : 62,
              lineHeight: 1.05,
              letterSpacing: -1,
              textAlign: align === 'center' ? 'center' : 'left',
              maxWidth: '85%',
              textTransform: 'uppercase',
              textShadow: l.emphasis
                ? `0 0 40px ${BRAND.color.gold}88`
                : `0 2px 16px rgba(0,0,0,0.6)`,
            }}
          >
            {l.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
