import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from '../components/Brand';

type Props = {
  backgroundSrc: string;
  line1: string;
  line2: string;
  badge: string;
  kicker?: string;
  variant?: 'red_alert' | 'gold_verdict' | 'blue_rights';
};

export const MirandaThumbnailFrame: React.FC<Props> = ({
  backgroundSrc,
  line1,
  line2,
  badge,
  kicker = 'MIRANDA v. ARIZONA',
  variant = 'red_alert',
}) => {
  const accent = variant === 'gold_verdict' ? BRAND.color.gold : variant === 'blue_rights' ? BRAND.color.electric : '#FF293D';
  const secondary = variant === 'blue_rights' ? BRAND.color.gold : BRAND.color.white;

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
          objectPosition: variant === 'gold_verdict' ? '54% 52%' : '64% 54%',
          transform: 'scale(1.16)',
          filter: 'brightness(1.18) contrast(1.32) saturate(1.22)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(90deg, #050508F8 0%, #050508E6 35%, #0505088A 62%, #05050818 100%), ' +
            'radial-gradient(circle at 78% 42%, transparent 0%, transparent 24%, #000000B8 82%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -110,
          top: 38,
          width: 760,
          height: 72,
          background: accent,
          transform: 'rotate(-8deg)',
          boxShadow: `0 0 34px ${accent}`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: -88,
          bottom: 84,
          width: 520,
          height: 34,
          background: accent,
          transform: 'rotate(-15deg)',
          opacity: 0.92,
          boxShadow: `0 0 30px ${accent}`,
        }}
      />
      <div style={{position: 'absolute', inset: 0, border: `5px solid ${accent}`}} />
      <div
        style={{
          position: 'absolute',
          left: 54,
          top: 48,
          color: BRAND.color.ink,
          background: accent,
          fontFamily: BRAND.font.body,
          fontSize: 32,
          fontWeight: 900,
          padding: '9px 18px',
          textTransform: 'uppercase',
        }}
      >
        {kicker}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 54,
          top: 150,
          right: 420,
          fontFamily: BRAND.font.display,
          fontWeight: 900,
          fontSize: 126,
          lineHeight: 0.88,
          letterSpacing: 0,
          textTransform: 'uppercase',
          textShadow: '8px 8px 0 #000, 0 0 32px #000',
        }}
      >
        <div style={{color: BRAND.color.white}}>{line1}</div>
        <div style={{color: accent}}>{line2}</div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 58,
          bottom: 84,
          color: secondary,
          background: '#000000D8',
          border: `4px solid ${accent}`,
          fontFamily: BRAND.font.body,
          fontSize: 34,
          fontWeight: 900,
          padding: '12px 20px',
          minWidth: 410,
          textTransform: 'uppercase',
          boxShadow: '0 8px 24px #000000AA',
        }}
      >
        {badge}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 58,
          bottom: 36,
          width: 510,
          height: 7,
          background: BRAND.color.gold,
          boxShadow: `0 0 22px ${BRAND.color.gold}`,
        }}
      />
      <div style={{position: 'absolute', right: 36, bottom: 26}}>
        <PdMonogram size={88} />
      </div>
    </AbsoluteFill>
  );
};
