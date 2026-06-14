import React from 'react';
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from '../components/Brand';
import {Vignette, Particles} from '../components/Motion';
import {Grain} from '../components/Grain';

export type OpeningProps = {
  channelName: string;
};

// 6s at 30fps
export const OPENING_DURATION_FRAMES = 180;

const BannerBg: React.FC = () => {
  const f = useCurrentFrame();
  const scale = interpolate(f, [0, OPENING_DURATION_FRAMES], [1.0, 1.07], {
    extrapolateRight: 'clamp',
  });
  // 暗いグラデーション処理：上下に深い影、中央はやや明るく
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Img
        src={staticFile('banner_sunrise.png')}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: '50% 40%',
          transform: `scale(${scale})`,
          transformOrigin: '50% 55%',
          filter: 'brightness(0.55) contrast(1.15) saturate(0.85)',
        }}
      />
    </AbsoluteFill>
  );
};

const DarkOverlay: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        'linear-gradient(to bottom,' +
        'rgba(10,10,12,0.70) 0%,' +
        'rgba(10,10,12,0.25) 40%,' +
        'rgba(10,10,12,0.60) 75%,' +
        'rgba(10,10,12,0.95) 100%)',
    }}
  />
);

// PD マークのみ（SVG、アルファあり）— pd_logo.png は白背景なので使わない
const LogoMark: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const delay = Math.round(fps * 0.55);
  const s = spring({
    frame: Math.max(0, f - delay),
    fps,
    config: {stiffness: 50, damping: 13, mass: 1.1},
  });
  const y  = interpolate(s, [0, 1], [72, 0]);
  const op = interpolate(s, [0, 0.2], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{transform: `translateY(${y}px)`, opacity: op}}>
        <PdMonogram size={340} />
      </div>
    </AbsoluteFill>
  );
};

// ゴールドの水平ライン（ロゴ下）
const GoldRule: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const start = Math.round(fps * 1.2);
  const w = interpolate(f, [start, start + 24], [0, 480], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const op = interpolate(f, [start, start + 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{marginTop: 220, opacity: op}}>
        <div
          style={{
            width: w,
            height: 2,
            background: BRAND.color.gold,
            boxShadow: `0 0 16px 3px ${BRAND.color.gold}99`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const FadeOut: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [152, OPENING_DURATION_FRAMES], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill
      style={{background: BRAND.color.ink, opacity: op, pointerEvents: 'none'}}
    />
  );
};

export const Opening: React.FC<OpeningProps> = () => (
  <AbsoluteFill style={{background: BRAND.color.ink}}>
    <BannerBg />
    <DarkOverlay />
    <LogoMark />
    <GoldRule />
    <Particles count={14} seed="op" color={BRAND.color.gold} />
    <Vignette strength={1} />
    <FadeOut />
    <Grain opacity={0.05} />
  </AbsoluteFill>
);
