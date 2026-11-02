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
  tone?: 'standard' | 'bright';
};

export const KingThumbnailFrame: React.FC<KingThumbnailProps> = ({
  backgroundSrc,
  line1,
  line2,
  badge,
  variant = 'left',
  tone = 'standard',
}) => {
  const centered = variant === 'center';
  const bright = tone === 'bright';
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <Img
        src={staticFile(backgroundSrc)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          filter: bright
            ? 'brightness(1.08) contrast(1.48) saturate(1.42)'
            : 'brightness(0.72) contrast(1.25) saturate(1.08)',
        }}
      />
      {bright ? (
        <>
          <AbsoluteFill
            style={{
              background:
                'radial-gradient(circle at 78% 34%, #35A8FF72 0%, #35A8FF22 26%, transparent 50%), radial-gradient(circle at 68% 46%, #F5BE2D6A 0%, #F5BE2D1B 18%, transparent 42%)',
              mixBlendMode: 'screen',
            }}
          />
          <div
            style={{
              position: 'absolute',
              right: -80,
              top: 84,
              width: 700,
              height: 170,
              transform: 'rotate(-13deg)',
              background:
                'linear-gradient(90deg, transparent 0%, #1FA7FF88 38%, #F7C52FBB 62%, transparent 100%)',
              filter: 'blur(22px)',
              opacity: 0.9,
              mixBlendMode: 'screen',
            }}
          />
        </>
      ) : null}
      <AbsoluteFill
        style={{
          background: centered
            ? 'linear-gradient(180deg, #05070A90 0%, #05070A20 48%, #05070AD8 100%)'
            : bright
              ? 'linear-gradient(90deg, #05070AE8 0%, #05070AB8 38%, #05070A18 72%, #05070A00 100%)'
              : 'linear-gradient(90deg, #05070AF4 0%, #05070ACC 43%, #05070A22 78%, #05070A00 100%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: centered ? 0 : bright ? 58 : 66,
          right: centered ? 0 : bright ? 520 : 540,
          top: bright ? 68 : 86,
          textAlign: centered ? 'center' : 'left',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            fontFamily: BRAND.font.body,
            fontSize: bright ? 32 : 30,
            fontWeight: 900,
            color: bright ? '#FFE27A' : BRAND.color.gold,
            background: bright ? '#030507E8' : '#000000B8',
            border: `3px solid ${BRAND.color.gold}`,
            padding: '8px 16px',
            textTransform: 'uppercase',
            boxShadow: bright ? `0 0 26px ${BRAND.color.gold}88` : undefined,
          }}
        >
          {badge}
        </div>
        <div
          style={{
            fontFamily: BRAND.font.display,
            color: BRAND.color.white,
            fontSize: bright ? 126 : 118,
            lineHeight: 0.94,
            textTransform: 'uppercase',
            textShadow: bright
              ? '0 8px 0 #000, 0 0 34px #1FA7FF, 0 9px 42px #000'
              : '0 7px 30px #000',
            marginTop: bright ? 30 : 34,
          }}
        >
          <div>{line1}</div>
          <div
            style={{
              color: bright ? '#FFD23F' : BRAND.color.gold,
              textShadow: bright ? '0 8px 0 #000, 0 0 36px #F7C52F, 0 9px 42px #000' : undefined,
            }}
          >
            {line2}
          </div>
        </div>
      </div>
      <div
        style={{
          position: 'absolute',
          left: 66,
          bottom: 48,
          width: bright ? 600 : 520,
          height: bright ? 7 : 5,
          background: bright ? '#FFD23F' : BRAND.color.gold,
          boxShadow: bright ? '0 0 24px #FFD23F, 0 0 54px #1FA7FF' : `0 0 18px ${BRAND.color.gold}`,
        }}
      />
      <div style={{position: 'absolute', right: 42, bottom: 28}}>
        <PdMonogram size={94} />
      </div>
    </AbsoluteFill>
  );
};
