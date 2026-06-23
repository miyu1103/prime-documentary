import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from '../components/Brand';

export type KingThumbnailProps = {
  backgroundSrc: string;
  line1: string;
  line2: string;
  badge: string;
  variant?: 'left' | 'center';
};

export const KingThumbnailFrame: React.FC<KingThumbnailProps> = ({
  backgroundSrc,
  line1,
  line2,
  badge,
  variant = 'left',
}) => {
  const centered = variant === 'center';
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <Img src={staticFile(backgroundSrc)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.72) contrast(1.25) saturate(1.08)'}} />
      <AbsoluteFill
        style={{
          background: centered
            ? 'linear-gradient(180deg, #05070A90 0%, #05070A20 48%, #05070AD8 100%)'
            : 'linear-gradient(90deg, #05070AF4 0%, #05070ACC 43%, #05070A22 78%, #05070A00 100%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: centered ? 0 : 66,
          right: centered ? 0 : 540,
          top: 86,
          textAlign: centered ? 'center' : 'left',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            fontFamily: BRAND.font.body,
            fontSize: 30,
            fontWeight: 900,
            color: BRAND.color.gold,
            background: '#000000B8',
            border: `3px solid ${BRAND.color.gold}`,
            padding: '8px 16px',
            textTransform: 'uppercase',
          }}
        >
          {badge}
        </div>
        <div style={{fontFamily: BRAND.font.display, color: BRAND.color.white, fontSize: 118, lineHeight: 0.96, textTransform: 'uppercase', textShadow: '0 7px 30px #000', marginTop: 34}}>
          <div>{line1}</div>
          <div style={{color: BRAND.color.gold}}>{line2}</div>
        </div>
      </div>
      <div style={{position: 'absolute', left: 66, bottom: 48, width: 520, height: 5, background: BRAND.color.gold, boxShadow: `0 0 18px ${BRAND.color.gold}`}} />
      <div style={{position: 'absolute', right: 42, bottom: 28}}>
        <PdMonogram size={94} />
      </div>
    </AbsoluteFill>
  );
};
