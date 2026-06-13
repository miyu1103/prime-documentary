import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Horizon, PdMonogram} from './Brand';

export type ThumbnailProps = {
  /** Title in large white caps (curiosity/question form, docs/27). */
  title: string;
  /** Optional background still (Midjourney) — logical/static path; falls back to gradient. */
  backgroundSrc?: string | null;
  /** A/B layout variant. */
  variant?: 'left' | 'center';
};

/**
 * Thumbnail still (decisions/0002 §D/§G): black ground + gold horizon + large white
 * caps title + PD mark. Background = a Midjourney still when supplied, else brand gradient.
 * Rendered as a Remotion <Still>; A/B variants are produced by changing props.
 */
export const ThumbnailFrame: React.FC<ThumbnailProps> = ({
  title,
  backgroundSrc = null,
  variant = 'left',
}) => {
  const alignItems = variant === 'center' ? 'center' : 'flex-start';
  const textAlign = variant === 'center' ? 'center' : 'left';

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {backgroundSrc ? (
        <Img
          src={backgroundSrc.startsWith('http') ? backgroundSrc : staticFile(backgroundSrc)}
          style={{width: '100%', height: '100%', objectFit: 'cover', opacity: 0.55}}
        />
      ) : (
        <AbsoluteFill
          style={{
            background: `radial-gradient(110% 90% at 70% 30%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 80%)`,
          }}
        />
      )}
      {/* darkening scrim for legibility (docs/27) */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(90deg, ${BRAND.color.ink}E6 0%, ${BRAND.color.ink}66 60%, transparent 100%)`,
        }}
      />
      <Horizon y={0.78} />
      <AbsoluteFill
        style={{
          padding: 72,
          justifyContent: 'center',
          alignItems,
        }}
      >
        <div
          style={{
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 92,
            lineHeight: 1.02,
            letterSpacing: -1,
            textTransform: 'uppercase',
            textAlign,
            maxWidth: '78%',
            textShadow: `0 4px 24px ${BRAND.color.ink}`,
          }}
        >
          {title}
        </div>
      </AbsoluteFill>
      <div style={{position: 'absolute', right: 40, bottom: 28}}>
        <PdMonogram size={96} />
      </div>
    </AbsoluteFill>
  );
};
