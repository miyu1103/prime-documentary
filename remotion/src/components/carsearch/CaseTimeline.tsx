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
// CaseTimeline — dark-noir horizontal case timeline (car-search doc)
//   ・ベースLINEがL→Rにspringで描画
//   ・イベントDOTが約0.18秒ずつスタッガーでポップ
//   ・YEAR(大)＋短いキャプションが上下交互にマスク切れ上がり
//   ・線の先端をelectricグローが走る／gold微アクセント
//   ・凍らない：線・点がずっと微シマー
// 全モーションeased(spring/Easing.out(cubic))・opacity単独なし・fps算出。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, ${BG} 82%)`;

const sec = (fps: number, s: number) => Math.round(fps * s);

type CaseEvent = {year: string; text: string};

const DEFAULT_EVENTS: CaseEvent[] = [
  {year: '1925', text: 'Carroll — the exception is born'},
  {year: '2009', text: 'Gant — arrest is not a blank check'},
  {year: '2018', text: 'Collins — it stops at your home'},
];

// マスク切れ上がりの一語（overflow:hidden + translateY）
const MaskLine: React.FC<{
  text: string;
  progress: number; // 0..1 spring driven
  size: number;
  weight: number;
  color: string;
  font: string;
  glow?: string;
  letterSpacing?: number;
}> = ({text, progress, size, weight, color, font, glow, letterSpacing = 0}) => {
  const y = interpolate(progress, [0, 1], [118, 0]);
  const o = interpolate(progress, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
        lineHeight: 1.05,
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          whiteSpace: 'nowrap',
          fontFamily: font,
          fontWeight: weight,
          fontSize: size,
          letterSpacing,
          color,
          textShadow: glow ? `0 0 22px ${glow}` : undefined,
        }}
      >
        {text}
      </span>
    </span>
  );
};

export const CaseTimeline: React.FC<{
  events?: CaseEvent[];
  dur?: number;
}> = ({events = DEFAULT_EVENTS, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  const x0 = 260;
  const x1 = width - 260;
  const cy = height / 2;
  const span = x1 - x0;
  const n = events.length;

  // 線の描画進捗（spring）
  const lineP = interpolate(
    spring({frame: frame - sec(fps, 0.25), fps, config: {damping: 30, mass: 1.1}}),
    [0, 1],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const tipX = x0 + span * lineP;

  // 凍らない微シマー（線の太さ／グローが呼吸する）
  const shimmer = interpolate(
    Math.sin(frame / 9),
    [-1, 1],
    [0.72, 1],
  );
  // 先端グローの上下ゆらぎ
  const tipDrift = Math.sin(frame / 6) * 2;

  // シーン出入り（微translateY併用でopacity単独を回避）
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 12], [22, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 うっすらグリッド（電子ブルー） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 46%, black 32%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 46%, black 32%, transparent 84%)',
        }}
      />
      {/* L3 中央グロー */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 40% at 50% 50%, ${BRAND.color.electric}1e 0%, transparent 70%)`,
        }}
      />

      <AbsoluteFill
        style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}
      >
        {/* 見出し */}
        <div style={{position: 'absolute', top: cy - 260, left: x0}}>
          <MaskLine
            text="TIMELINE OF THE DOCTRINE"
            progress={interpolate(
              spring({frame: frame - sec(fps, 0.12), fps, config: {damping: 18}}),
              [0, 1],
              [0, 1],
            )}
            size={34}
            weight={700}
            color={BRAND.color.silver}
            font={BRAND.font.body}
            letterSpacing={6}
          />
        </div>

        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0}}
        >
          <defs>
            <linearGradient id="ct-line" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={BRAND.color.electric} />
              <stop offset="100%" stopColor={BRAND.color.gold} />
            </linearGradient>
          </defs>

          {/* うっすら全長ガイド線（gold微アクセント） */}
          <line
            x1={x0}
            y1={cy}
            x2={x1}
            y2={cy}
            stroke={BRAND.color.gold}
            strokeWidth={1}
            opacity={0.14}
          />
          {/* 描画中のベースライン */}
          <line
            x1={x0}
            y1={cy}
            x2={tipX}
            y2={cy}
            stroke="url(#ct-line)"
            strokeWidth={3 * shimmer}
            strokeLinecap="round"
            opacity={0.9}
          />

          {events.map((e, i) => {
            const ex = x0 + (span * i) / (n - 1);
            const cs = spring({
              frame: frame - sec(fps, 0.5) - i * sec(fps, 0.18),
              fps,
              config: {damping: 14, mass: 0.8},
            });
            const r = interpolate(cs, [0, 1], [0, 10]);
            const reveal = interpolate(cs, [0, 1], [0, 1]);
            // 点ごとの独立シマー（凍らない）
            const dotPulse = interpolate(
              Math.sin(frame / 8 + i * 1.7),
              [-1, 1],
              [0.55, 1],
            );
            const up = i % 2 === 0;
            const yLabel = up ? cy - 46 : cy + 46;
            return (
              <g key={i}>
                {/* グロー環 */}
                <circle
                  cx={ex}
                  cy={cy}
                  r={r + 12}
                  fill={BRAND.color.electric}
                  opacity={reveal * 0.16 * dotPulse}
                />
                {/* 本体ドット */}
                <circle
                  cx={ex}
                  cy={cy}
                  r={r}
                  fill={BG}
                  stroke={BRAND.color.electric}
                  strokeWidth={3}
                  opacity={interpolate(cs, [0, 0.2], [0, 1], {
                    extrapolateRight: 'clamp',
                  })}
                />
                {/* 中央gold核 */}
                <circle
                  cx={ex}
                  cy={cy}
                  r={r * 0.34}
                  fill={BRAND.color.gold}
                  opacity={reveal}
                />
                {/* 縦のつなぎ線（点→ラベル） */}
                <line
                  x1={ex}
                  y1={cy}
                  x2={ex}
                  y2={yLabel + (up ? 6 : -6)}
                  stroke={BRAND.color.silver}
                  strokeWidth={1}
                  opacity={reveal * 0.35}
                />
                {/* ラベル（foreignObjectでマスク切れ上がり） */}
                <foreignObject
                  x={ex - 220}
                  y={up ? cy - 190 : cy + 22}
                  width={440}
                  height={170}
                >
                  <div
                    style={{
                      width: '100%',
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: up ? 'flex-end' : 'flex-start',
                      gap: 6,
                    }}
                  >
                    <MaskLine
                      text={e.year}
                      progress={reveal}
                      size={70}
                      weight={800}
                      color={BRAND.color.white}
                      font={BRAND.font.display}
                      glow={`${BRAND.color.electric}66`}
                      letterSpacing={1}
                    />
                    <MaskLine
                      text={e.text}
                      progress={interpolate(cs, [0.12, 1], [0, 1], {
                        extrapolateLeft: 'clamp',
                      })}
                      size={22}
                      weight={500}
                      color={BRAND.color.silver}
                      font={BRAND.font.body}
                      letterSpacing={0.5}
                    />
                  </div>
                </foreignObject>
              </g>
            );
          })}
        </svg>

        {/* 描画中の先端を走る electric グロー（Trailでモーションブラー） */}
        {lineP < 0.999 && lineP > 0.001 ? (
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <div
              style={{
                position: 'absolute',
                left: tipX - 11,
                top: cy - 11 + tipDrift,
                width: 22,
                height: 22,
                borderRadius: '50%',
                background: BRAND.color.white,
                boxShadow: `0 0 26px 8px ${BRAND.color.electric}, 0 0 10px 2px ${BRAND.color.white}`,
              }}
            />
          </Trail>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
