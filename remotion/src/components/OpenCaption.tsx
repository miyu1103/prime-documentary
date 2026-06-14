import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {BRAND} from '../brand';

/**
 * Open caption (burned-in, styled subtitle) — decisions/0002 §5. Word-by-word
 * reveal in sync with a narration line. Styled for small-size legibility (docs/27).
 */
export const OpenCaption: React.FC<{text: string; revealFrames?: number}> = ({
  text,
  revealFrames = 90,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');
  const shown = Math.round(interpolate(frame, [0, revealFrames], [0, words.length], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  }));
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 140}}>
      <div
        style={{
          maxWidth: '80%',
          textAlign: 'center',
          background: `${BRAND.color.ink}B3`,
          padding: '16px 28px',
          borderRadius: 10,
        }}
      >
        <span
          style={{
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: 44,
            lineHeight: 1.25,
            color: BRAND.color.white,
            textShadow: `0 2px 10px ${BRAND.color.ink}`,
          }}
        >
          {words.map((w, i) => (
            <span key={i} style={{opacity: i < shown ? 1 : 0.18, transition: 'none'}}>
              {w}
              {i < words.length - 1 ? ' ' : ''}
            </span>
          ))}
        </span>
      </div>
    </AbsoluteFill>
  );
};
