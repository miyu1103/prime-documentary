import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

export type ParallaxLayer = {
  /** 0 = far (slow), 1 = near (fast). */
  depth: number;
  node: React.ReactNode;
};

/**
 * 2.5D parallax: layers drift horizontally at speeds scaled by depth, giving a
 * sense of dimension to flat symbolic shapes (decisions/0002 §5). Pure code, $0.
 */
export const Parallax: React.FC<{layers: ParallaxLayer[]; amount?: number}> = ({
  layers,
  amount = 60,
}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const progress = interpolate(frame, [0, durationInFrames], [0, 1]);
  return (
    <AbsoluteFill>
      {layers.map((l, i) => {
        const dx = (progress - 0.5) * amount * (0.3 + l.depth);
        const scale = 1 + l.depth * 0.08;
        return (
          <AbsoluteFill
            key={i}
            style={{transform: `translateX(${dx}px) scale(${scale})`}}
          >
            {l.node}
          </AbsoluteFill>
        );
      })}
    </AbsoluteFill>
  );
};

/** A few symbolic shape layers (a courtroom-ish geometry) for the style test. */
export const SymbolicScene: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 100% at 50% 30%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 80%)`,
    }}
  >
    <Parallax
      layers={[
        {
          depth: 0.1,
          node: (
            <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
              <div
                style={{
                  width: 900,
                  height: 900,
                  borderRadius: '50%',
                  border: `2px solid ${BRAND.color.electric}33`,
                }}
              />
            </AbsoluteFill>
          ),
        },
        {
          depth: 0.5,
          node: (
            <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
              <div style={{width: 4, height: 520, background: `${BRAND.color.silver}55`}} />
            </AbsoluteFill>
          ),
        },
        {
          depth: 1,
          node: (
            <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
              {/* gavel-as-symbol: a bar + block */}
              <div style={{transform: 'rotate(-18deg)'}}>
                <div style={{width: 240, height: 26, background: BRAND.color.gold, borderRadius: 6}} />
                <div
                  style={{
                    width: 70,
                    height: 70,
                    background: BRAND.color.gold,
                    borderRadius: 8,
                    margin: '18px auto 0',
                  }}
                />
              </div>
            </AbsoluteFill>
          ),
        },
      ]}
    />
  </AbsoluteFill>
);
