import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

/**
 * Vertical "meaningful animation" components for 9:16 Shorts (1080x1920).
 * SHORTS_MOTION_DESIGN.md §4: the long-form Premium viz (Vote/BigNumber/DiagramFlow) are
 * hard-coded for 1920x1080 and break in vertical. These are vertical-native re-coordinates of
 * the same motifs. All art sits in the MIDDLE zone (y≈600–1240) and must NOT enter the telop
 * zone (y180–560) or the caption zone (y1280–1560). CitationTopLeft lives at the top-left
 * (y≈200) because CitationLowerThird's bottom-left collides with the caption band.
 */

/** Number hook / count (e.g. "127日" / "令状なし"). BigNumber's vertical coordinate version. */
export const BigNumberVertical: React.FC<{top: string; bottom?: string}> = ({top, bottom}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const pop = spring({frame, fps, config: {damping: 14, stiffness: 140, mass: 0.7}});
  const scale = interpolate(pop, [0, 1], [0.6, 1]);
  const glow = interpolate(pop, [0, 1], [0, 1]);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{transform: `scale(${scale})`, textAlign: 'center'}}>
        <div
          style={{
            color: BRAND.color.gold,
            fontFamily: BRAND.font.display,
            fontSize: 300,
            fontWeight: 900,
            lineHeight: 0.9,
            letterSpacing: -4,
            textShadow: `0 0 ${60 * glow}px ${BRAND.color.gold}aa, 0 8px 30px ${BRAND.color.ink}`,
          }}
        >
          {top}
        </div>
        {bottom ? (
          <div
            style={{
              marginTop: 24,
              color: BRAND.color.white,
              fontFamily: BRAND.font.display,
              fontSize: 96,
              letterSpacing: 2,
              textShadow: `0 4px 20px ${BRAND.color.ink}`,
            }}
          >
            {bottom}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/** Decision vote tally (e.g. 5–4). Variable yes/no (NEVER hard-coded). Vote's vertical version. */
export const VoteVertical: React.FC<{yes: number; no: number}> = ({yes, no}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const total = yes + no;
  const cells = Array.from({length: total}, (_, i) => i < yes);
  const label = spring({frame: frame - 6, fps, config: {damping: 16, stiffness: 130}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 36}}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${Math.min(total, 3)}, 150px)`,
            gap: 22,
            justifyContent: 'center',
          }}
        >
          {cells.map((isYes, i) => {
            const pop = spring({frame: frame - i * 4, fps, config: {damping: 13, stiffness: 160}});
            return (
              <div
                key={i}
                style={{
                  width: 150,
                  height: 150,
                  borderRadius: 18,
                  transform: `scale(${interpolate(pop, [0, 1], [0.3, 1])})`,
                  opacity: Math.min(pop * 1.4, 1),
                  background: isYes ? BRAND.color.electric : `${BRAND.color.silver}40`,
                  border: `4px solid ${isYes ? BRAND.color.gold : `${BRAND.color.silver}aa`}`,
                  boxShadow: isYes ? `0 0 30px ${BRAND.color.electric}77` : 'none',
                }}
              />
            );
          })}
        </div>
        <div
          style={{
            transform: `scale(${interpolate(label, [0, 1], [0.7, 1])})`,
            opacity: Math.min(label * 1.4, 1),
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontSize: 170,
            letterSpacing: 2,
            textShadow: `0 6px 26px ${BRAND.color.ink}`,
          }}
        >
          {yes}–{no}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/** A→B→C chain stacked VERTICALLY with downward connectors (DiagramFlow is row-only). Max 3 boxes. */
export const DiagramFlowVertical: React.FC<{steps: string[]; stagger?: number}> = ({
  steps,
  stagger = 12,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items = steps.slice(0, 3);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0}}>
        {items.map((step, i) => {
          const enter = spring({frame: frame - i * stagger, fps, config: {damping: 18, stiffness: 120}});
          const y = interpolate(enter, [0, 1], [40, 0]);
          return (
            <React.Fragment key={i}>
              <div
                style={{
                  transform: `translateY(${y}px)`,
                  opacity: Math.min(enter * 1.4, 1),
                  width: 640,
                  padding: '30px 36px',
                  borderRadius: 16,
                  background: `${BRAND.color.navy}ee`,
                  border: `3px solid ${BRAND.color.electric}`,
                  color: BRAND.color.white,
                  fontFamily: BRAND.font.body,
                  fontWeight: 800,
                  fontSize: 52,
                  textAlign: 'center',
                  lineHeight: 1.15,
                  boxShadow: `0 8px 30px ${BRAND.color.ink}aa`,
                }}
              >
                {step}
              </div>
              {i < items.length - 1 ? (
                <div
                  style={{
                    opacity: Math.min(enter * 1.4, 1),
                    color: BRAND.color.gold,
                    fontSize: 64,
                    lineHeight: 1,
                    margin: '6px 0',
                  }}
                >
                  ↓
                </div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/** Phone-content reveal for Riley: stacked life categories, kept between telop and captions. */
export const DoorsVertical: React.FC<{items: string[]; title?: string; stagger?: number}> = ({
  items,
  title = 'スマホの中身',
  stagger = 10,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const shown = items.slice(0, 4);
  const titleEnter = spring({frame, fps, config: {damping: 18, stiffness: 125}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{width: 720, display: 'flex', flexDirection: 'column', gap: 18, alignItems: 'stretch'}}>
        <div
          style={{
            transform: `translateY(${interpolate(titleEnter, [0, 1], [30, 0])}px)`,
            opacity: Math.min(titleEnter * 1.4, 1),
            color: BRAND.color.gold,
            fontFamily: BRAND.font.display,
            fontSize: 78,
            textAlign: 'center',
            textShadow: `0 5px 24px ${BRAND.color.ink}`,
          }}
        >
          {title}
        </div>
        {shown.map((item, i) => {
          const enter = spring({frame: frame - 8 - i * stagger, fps, config: {damping: 16, stiffness: 140}});
          return (
            <div
              key={item}
              style={{
                transform: `translateX(${interpolate(enter, [0, 1], [-80, 0])}px)`,
                opacity: Math.min(enter * 1.4, 1),
                padding: '24px 34px',
                borderRadius: 14,
                background: `${BRAND.color.ink}d8`,
                border: `3px solid ${i === shown.length - 1 ? BRAND.color.gold : BRAND.color.electric}`,
                boxShadow: `0 10px 32px ${BRAND.color.ink}aa`,
                color: BRAND.color.white,
                fontFamily: BRAND.font.body,
                fontWeight: 900,
                fontSize: 58,
                lineHeight: 1.08,
                textAlign: 'center',
              }}
            >
              {item}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/** Citation / year burn-in for vertical — top-left (y≈200), clear of the caption band. */
export const CitationTopLeft: React.FC<{label: string; source?: string}> = ({label, source}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: {damping: 20, stiffness: 120}});
  return (
    <div
      style={{
        position: 'absolute',
        top: 210,
        left: 64,
        maxWidth: 720,
        opacity: enter,
        transform: `translateX(${interpolate(enter, [0, 1], [-24, 0])}px)`,
        borderLeft: `5px solid ${BRAND.color.gold}`,
        padding: '8px 18px',
        background: `${BRAND.color.ink}aa`,
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          color: BRAND.color.white,
          fontFamily: BRAND.font.body,
          fontWeight: 800,
          fontSize: 38,
          lineHeight: 1.15,
        }}
      >
        {label}
      </div>
      {source ? (
        <div style={{color: BRAND.color.gold, fontFamily: BRAND.font.body, fontSize: 30, marginTop: 4}}>
          {source}
        </div>
      ) : null}
    </div>
  );
};
