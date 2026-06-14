import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

/**
 * Lower-third that burns in a source citation, optionally tied to claim_ids
 * (decisions/0002 §5: "burn in sources for major claims, linked to claim_id").
 * Slides up from the bottom-left.
 */
export const CitationLowerThird: React.FC<{
  label: string;
  source?: string;
  claimIds?: string[];
}> = ({label, source, claimIds = []}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: {damping: 200}});
  const y = interpolate(enter, [0, 1], [60, 0]);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-start'}}>
      <div
        style={{
          transform: `translateY(${y}px)`,
          opacity: enter,
          margin: '0 0 90px 90px',
          borderLeft: `4px solid ${BRAND.color.gold}`,
          background: `${BRAND.color.ink}D9`,
          padding: '16px 22px',
          backdropFilter: 'blur(2px)',
        }}
      >
        <div
          style={{
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontSize: 38,
            fontWeight: 900,
            letterSpacing: 1,
          }}
        >
          {label}
        </div>
        {source ? (
          <div
            style={{
              color: BRAND.color.silver,
              fontFamily: BRAND.font.body,
              fontSize: 22,
              marginTop: 4,
            }}
          >
            {source}
            {claimIds.length ? (
              <span style={{color: BRAND.color.gold}}> · {claimIds.join(', ')}</span>
            ) : null}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
