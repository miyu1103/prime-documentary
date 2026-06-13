import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

/**
 * Animated explanatory flow A -> B -> C (decisions/0002 §B: Remotion diagrams).
 * Boxes pop in in sequence; connectors draw between them. Pure code, $0.
 */
export const DiagramFlow: React.FC<{steps: string[]; stagger?: number}> = ({
  steps,
  stagger = 22,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 100% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 85%)`,
        justifyContent: 'center',
        alignItems: 'center',
        gap: 0,
        flexDirection: 'row',
      }}
    >
      {steps.map((label, i) => {
        const appear = spring({frame: frame - i * stagger, fps, config: {damping: 200}});
        const connector =
          i > 0
            ? interpolate(frame - i * stagger, [-stagger, 0], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              })
            : 0;
        return (
          <React.Fragment key={i}>
            {i > 0 ? (
              <div style={{position: 'relative', width: 90, height: 4}}>
                <div
                  style={{
                    position: 'absolute',
                    height: 4,
                    width: `${connector * 100}%`,
                    background: BRAND.color.electric,
                  }}
                />
              </div>
            ) : null}
            <div
              style={{
                transform: `scale(${interpolate(appear, [0, 1], [0.8, 1])})`,
                opacity: appear,
                background: `${BRAND.color.ink}`,
                border: `2px solid ${BRAND.color.electric}`,
                borderRadius: 14,
                padding: '28px 26px',
                maxWidth: 300,
                textAlign: 'center',
                color: BRAND.color.white,
                fontFamily: BRAND.font.body,
                fontSize: 30,
                fontWeight: 700,
                boxShadow: `0 0 40px ${BRAND.color.electric}22`,
              }}
            >
              {label}
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};
