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
        const enter = spring({frame: local, fps, config: {damping: 200}});
        const y = interpolate(enter, [0, 1], [40, 0]);
        return (
          <div
            key={i}
            style={{
              transform: `translateY(${y}px)`,
              opacity: enter,
              color: l.emphasis ? BRAND.color.gold : BRAND.color.white,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: l.emphasis ? 84 : 58,
              lineHeight: 1.05,
              letterSpacing: -1,
              textAlign: align === 'center' ? 'center' : 'left',
              maxWidth: '85%',
              textTransform: 'uppercase',
            }}
          >
            {l.text}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
