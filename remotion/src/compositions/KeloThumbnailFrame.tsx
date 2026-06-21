import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from '../components/Brand';

type Props = {
  backgroundSrc: string;
  headlineTop?: string;
  headlineBottom?: string;
  badge?: string;
  variant?: 'taken' | 'developer' | 'vote';
};

export const KeloThumbnailFrame: React.FC<Props> = ({
  backgroundSrc,
  headlineTop = 'YOUR HOME',
  headlineBottom = 'TAKEN?',
  badge = 'FOR A DEVELOPER',
  variant = 'taken',
}) => {
  const bottomColor = variant === 'developer' ? BRAND.color.white : BRAND.color.gold;
  const badgeText = variant === 'vote' ? '5-4 SUPREME COURT' : badge;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <Img
        src={staticFile(backgroundSrc)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: '63% 55%',
          transform: 'scale(1.24)',
          filter: 'brightness(1.22) contrast(1.13) saturate(1.14)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            `linear-gradient(90deg, ${BRAND.color.ink}F2 0%, ${BRAND.color.ink}D8 34%, ${BRAND.color.ink}55 61%, transparent 100%), ` +
            `linear-gradient(0deg, ${BRAND.color.ink}B8 0%, transparent 32%, transparent 100%)`,
        }}
      />
      <div style={{position: 'absolute', inset: 0, border: `3px solid ${BRAND.color.gold}`}} />
      <div style={{position: 'absolute', left: 52, top: 52, fontFamily: BRAND.font.body, fontSize: 34, color: BRAND.color.electric, fontWeight: 900, letterSpacing: 0}}>
        EMINENT DOMAIN
      </div>
      <div style={{position: 'absolute', left: 52, top: 102, width: 340, height: 11, background: BRAND.color.gold}} />
      <div
        style={{
          position: 'absolute',
          left: 50,
          top: 168,
          fontFamily: BRAND.font.display,
          fontWeight: 900,
          fontSize: 116,
          lineHeight: 0.9,
          letterSpacing: 0,
          textTransform: 'uppercase',
          textShadow: `7px 8px 0 ${BRAND.color.ink}, 0 0 26px ${BRAND.color.ink}`,
        }}
      >
        <div style={{color: BRAND.color.white}}>{headlineTop}</div>
        <div style={{color: bottomColor}}>{headlineBottom}</div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 54,
          top: 472,
          border: `2px solid ${BRAND.color.gold}`,
          color: BRAND.color.silver,
          background: `${BRAND.color.ink}D8`,
          fontFamily: BRAND.font.body,
          fontSize: 31,
          fontWeight: 900,
          padding: '12px 20px',
          minWidth: 355,
        }}
      >
        {badgeText}
      </div>
      <div style={{position: 'absolute', left: 56, bottom: 46, fontFamily: BRAND.font.body, color: BRAND.color.silver, fontSize: 24, fontWeight: 900}}>
        PRIME DOCUMENTARY
      </div>
      <div style={{position: 'absolute', right: 40, bottom: 30}}>
        <PdMonogram size={84} />
      </div>
    </AbsoluteFill>
  );
};
