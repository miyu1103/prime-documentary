import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';

const GOLD = '#f5c84b';
const WHITE = '#f4f7fb';
const BLACK = '#030303';
const BLUE = '#42c4ff';
const ACCENT_RED = '#ff4d4f';

const OPTIONS = {
  A: {
    background: 'onecoin/hero/T-IMG-003.png',
    line1: 'NO COIN',
    line2: 'MILLIONS BELIEVED',
    kicker: 'NO COIN',
    kickerBadge: 'INTRIGUED? PAID.',
    accent: GOLD,
  },
  B: {
    background: 'onecoin/hero/T-IMG-012.png',
    line1: 'SHE VANISHED',
    line2: 'STILL ON FBI LIST',
    kicker: "WANTED",
    kickerBadge: 'CHARGED / NOT CONVICTED',
    accent: BLUE,
  },
  C: {
    background: 'onecoin/hero/T-IMG-002.png',
    line1: '$4 BILLION',
    line2: 'GONE',
    kicker: 'COLD VOID',
    kickerBadge: 'PROMISE -> SMOKE',
    accent: GOLD,
  },
} as const;

type OptionId = keyof typeof OPTIONS;

export const OneCoinThumbnailFrame: React.FC<{option: OptionId}> = ({option}) => {
  const item = OPTIONS[option];
  return (
    <AbsoluteFill style={{background: BLACK, overflow: 'hidden'}}>
      <Img
        src={staticFile(item.background)}
        style={{
          position: 'absolute',
          width: '112%',
          height: '112%',
          left: '-6%',
          top: '-6%',
          objectFit: 'cover',
          filter: 'contrast(1.26) saturate(1.28) brightness(0.72)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, #000000B0 0%, #000000A8 26%, #00000040 62%, #00000010 100%)'}} />
      <div
        style={{
          position: 'absolute',
          inset: 28,
          border: `2px solid ${item.accent}CC`,
          boxShadow: `0 0 32px ${item.accent}80, inset 0 0 0 4px #0007`,
          pointerEvents: 'none',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -160,
          top: -160,
          width: 430,
          height: 430,
          borderRadius: '50%',
          background: `${item.accent}22`,
          filter: 'blur(14px)',
          opacity: 0.85,
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: -160,
          bottom: -160,
          width: 430,
          height: 430,
          borderRadius: '50%',
          background: `${item.accent}33`,
          filter: 'blur(14px)',
          opacity: 0.75,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 58,
          top: 46,
          padding: '10px 16px',
          border: `4px solid ${item.accent}`,
          color: item.accent,
          fontFamily: BRAND.font.body,
          fontSize: option === 'C' ? 28 : 30,
          lineHeight: 1,
          letterSpacing: 0.4,
          textTransform: 'uppercase',
          textShadow: `0 0 12px ${item.accent}AA, 0 0 1px #000`,
          background: `${item.accent}16`,
          transform: 'skew(-7deg)',
          fontWeight: 950,
        }}
      >
        {item.kicker}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 56,
          top: 84,
          width: 420,
          height: 1,
          background: `linear-gradient(90deg, ${item.accent}, transparent)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: 52,
          top: 90,
          width: 340,
          height: 44,
          border: `3px solid ${item.accent}CC`,
          background: '#031121CC',
          color: WHITE,
          fontFamily: BRAND.font.body,
          fontSize: 20,
          fontWeight: 900,
          letterSpacing: 0.2,
          padding: '8px 14px',
          textTransform: 'uppercase',
          textAlign: 'right',
          lineHeight: 1.1,
          boxShadow: `0 0 26px ${item.accent}55`,
        }}
      >
        {item.kickerBadge}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 56,
          right: 430,
          bottom: 64,
          fontFamily: BRAND.font.display,
          color: WHITE,
          fontWeight: 950,
          textTransform: 'uppercase',
          textShadow: `0 10px 28px #000, 0 0 44px ${item.accent}55`,
        }}
      >
        <div style={{fontSize: 108, lineHeight: 0.9, letterSpacing: 0.4}}>{item.line1}</div>
        <div style={{fontSize: option === 'A' ? 134 : 148, lineHeight: 0.86, color: item.accent}}>{item.line2}</div>
      </div>
      <div
        style={{
          position: 'absolute',
          right: 34,
          bottom: 36,
          width: 300,
          height: 300,
          borderRadius: '50%',
          border: `8px solid ${item.accent}`,
          boxShadow: `0 0 54px ${item.accent}BB, inset 0 0 46px #000`,
          background: '#00000088',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: 126,
            top: 20,
            width: 38,
            height: 250,
            background: item.accent,
            transform: 'rotate(25deg)',
            boxShadow: `0 0 20px ${item.accent}`,
          }}
        />
        <div
          style={{
            position: 'absolute',
            left: 80,
            top: -36,
            width: 20,
            height: 380,
            background: item.accent,
            transform: 'rotate(25deg)',
            opacity: 0.84,
          }}
        />
      </div>
      <div style={{position: 'absolute', left: 58, right: 58, bottom: 28, height: 6, background: item.accent}} />
      <div
        style={{
          position: 'absolute',
          left: 58,
          right: 58,
          bottom: 20,
          height: 3,
          background: `${item.accent}66`,
        }}
      />
    </AbsoluteFill>
  );
};
