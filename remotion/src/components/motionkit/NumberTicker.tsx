import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// MOTIONKIT — NumberTicker
//   ヒーロー数値が 0→value をカウントアップする単体シーン（standalone StatCounter）。
//   ・カウントは Easing.out(Easing.cubic)（等速禁止）／tabular-nums で桁ゆれなし
//   ・prefix / suffix / decimals で整形
//   ・ゴールドのアクセント下線が scaleX spring で描かれる
//   ・topLabel（kicker）と label は overflow:hidden＋translateY のマスク切れ上がり
//   ・着地後も止まらない：数値に微小なブレス（呼吸）
//   ・フルスクリーン背景＋3層以上のデプス（グラデ / グリッド / グロー）
// =====================================================================

// 秒→フレーム（fps 由来。フレーム直書き禁止）
const sec = (fps: number, s: number): number => Math.round(fps * s);

export const NumberTicker: React.FC<{
  value: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  topLabel?: string;
  label?: string;
  dur?: number;
}> = ({
  value,
  prefix = '',
  suffix = '',
  decimals = 0,
  topLabel = 'By the numbers',
  label,
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // --- シーン全体の出入り（opacity単独禁止 → 微 translateY と併用） ---
  const sceneY = interpolate(frame, [0, sec(fps, 0.33)], [18, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sceneO = interpolate(
    frame,
    [0, sec(fps, 0.33), D - sec(fps, 0.4), D],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // --- カウント（等速禁止：out cubic） ---
  const countStart = sec(fps, 0.25);
  const countEnd = sec(fps, 1.6);
  const p = interpolate(frame, [countStart, countEnd], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const shown = (value * p).toFixed(Math.max(0, decimals));

  // --- 着地後のブレス（決定論・useCurrentFrameのみ。静止させない） ---
  const settle = Math.max(0, frame - countEnd);
  const breath =
    1 + 0.01 * Math.sin((settle / fps) * Math.PI * 2 * 0.42);

  // --- ゴールド下線が描かれる（scaleX spring） ---
  const underline = spring({
    frame: frame - sec(fps, 0.45),
    fps,
    config: {damping: 18, mass: 1},
  });

  // --- 背景グリッドのゆっくりドリフト（静止しない下地） ---
  const drift = interpolate(frame, [0, D], [0, 34], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });

  // --- マスク切れ上がりラベル ---
  const MaskLine: React.FC<{
    text: string;
    delay: number;
    size: number;
    letterSpacing: number;
    weight: number;
    color: string;
    upper?: boolean;
    marginTop?: number;
  }> = ({
    text,
    delay,
    size,
    letterSpacing,
    weight,
    color,
    upper = false,
    marginTop = 0,
  }) => {
    const cs = spring({
      frame: frame - sec(fps, delay),
      fps,
      config: {damping: 16, mass: 1},
    });
    const ty = interpolate(cs, [0, 1], [112, 0]);
    const o = interpolate(cs, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
    return (
      <div
        style={{
          overflow: 'hidden',
          paddingBottom: '0.14em',
          marginTop,
        }}
      >
        <div
          style={{
            transform: `translateY(${ty}%)`,
            opacity: o,
            fontFamily: BRAND.font.body,
            fontWeight: weight,
            fontSize: size,
            letterSpacing,
            textTransform: upper ? 'uppercase' : 'none',
            color,
            whiteSpace: 'pre',
            lineHeight: 1.1,
          }}
        >
          {text}
        </div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {/* Depth 1 — フルスクリーン背景グラデ */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Depth 2 — うっすらグリッド（electric・ゆっくりドリフト＋放射マスク） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 74px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 74px)`,
          maskImage:
            'radial-gradient(120% 90% at 50% 44%, black 28%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 44%, black 28%, transparent 80%)',
        }}
      />

      {/* Depth 3 — 数値裏のグロー（数値の登場に合わせて立ち上がる） */}
      <AbsoluteFill
        style={{
          opacity: interpolate(p, [0, 1], [0.18, 0.5]),
          background: `radial-gradient(46% 40% at 50% 46%, ${BRAND.color.electric}33 0%, transparent 62%)`,
        }}
      />

      {/* Depth 4 — ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 46%, rgba(0,0,0,0.6) 100%)',
        }}
      />

      {/* 前景コンテンツ */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          opacity: sceneO,
          transform: `translateY(${sceneY}px)`,
        }}
      >
        {/* kicker（マスク切れ上がり） */}
        <MaskLine
          text={topLabel}
          delay={0.12}
          size={26}
          letterSpacing={8}
          weight={600}
          color={BRAND.color.silver}
          upper
          marginTop={0}
        />

        {/* ヒーロー数値（motion-blur Trail＋着地後ブレス） */}
        <div style={{marginTop: 20, marginBottom: 8}}>
          <Trail layers={4} lagInFrames={1} trailOpacity={0.32}>
            <div
              style={{
                display: 'flex',
                alignItems: 'baseline',
                color: BRAND.color.white,
                fontFamily: BRAND.font.display,
                fontWeight: 800,
                transform: `scale(${breath})`,
                transformOrigin: '50% 50%',
              }}
            >
              {prefix ? (
                <span style={{fontSize: 92, color: BRAND.color.gold}}>
                  {prefix}
                </span>
              ) : null}
              <span
                style={{
                  fontSize: 214,
                  letterSpacing: -6,
                  lineHeight: 0.9,
                  fontVariantNumeric: 'tabular-nums',
                  fontFeatureSettings: '"tnum" 1',
                }}
              >
                {shown}
              </span>
              {suffix ? (
                <span
                  style={{
                    fontSize: 92,
                    color: BRAND.color.gold,
                    marginLeft: 10,
                  }}
                >
                  {suffix}
                </span>
              ) : null}
            </div>
          </Trail>
        </div>

        {/* ゴールド下線（scaleX spring で描かれる） */}
        <div
          style={{
            width: 260,
            height: 5,
            borderRadius: 3,
            backgroundColor: BRAND.color.gold,
            boxShadow: `0 0 24px ${BRAND.color.gold}aa`,
            transform: `scaleX(${underline})`,
            transformOrigin: 'left center',
          }}
        />

        {/* 下ラベル（マスク切れ上がり） */}
        {label ? (
          <MaskLine
            text={label}
            delay={0.7}
            size={30}
            letterSpacing={2}
            weight={500}
            color={BRAND.color.silver}
            marginTop={22}
          />
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
