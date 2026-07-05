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
// MOTIONKIT — ComparisonBars
//   横棒が左のベースラインから 0→value へスタッガーで伸び、値が同期して
//   カウントアップする「A vs B」比較図。BarChart（Figures.tsx）の作法に準拠:
//   単一アクセント / 抑えた軸 / 直接ラベル / マスク切れ上がり文字 /
//   全モーションにイージング（等速禁止）/ 決定論（useCurrentFrame + index）。
//   速い伸長には @remotion/motion-blur の Trail でモーションブラー。
// =====================================================================

// 秒→フレーム（フレーム直書き禁止・fpsから算出）
const sec = (fps: number, s: number) => Math.round(fps * s);

// 値フォーマット（整数ターゲットは整数・小数ターゲットは1桁 / tabular-nums前提）
const formatVal = (target: number, current: number): string =>
  current.toFixed(Number.isInteger(target) ? 0 : 1);

// 直接ラベル（overflow:hidden + translateY のマスク切れ上がり）
const MaskLabel: React.FC<{
  text: string;
  reveal: number; // 0→1 (eased spring progress)
  size: number;
  weight: number;
  color: string;
  letterSpacing?: number;
}> = ({text, reveal, size, weight, color, letterSpacing = 0.5}) => {
  const y = interpolate(reveal, [0, 1], [118, 0]);
  const o = interpolate(reveal, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
        fontFamily: BRAND.font.body,
        fontWeight: weight,
        fontSize: size,
        letterSpacing,
        color,
        lineHeight: 1.05,
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          whiteSpace: 'pre',
        }}
      >
        {text}
      </span>
    </span>
  );
};

export const ComparisonBars: React.FC<{
  items: {label: string; value: number; accent?: string}[];
  dur?: number;
}> = ({items, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- レイアウト定数（全て定数化） ----
  const axisX = 320; // 左ベースライン x
  const plotRight = width - 320;
  const plotWidth = plotRight - axisX;
  const barH = 66;
  const rowGap = 96; // 棒間（ラベル分を含む）
  const n = Math.max(1, items.length);
  const contentH = n * barH + (n - 1) * rowGap;
  const top0 = (height - contentH) / 2 + 24;
  const rowStride = barH + rowGap;
  const max = Math.max(...items.map((d) => d.value), 1e-9);

  // ---- 背景ドリフト（決してフルスタティックにしない・sinイージング） ----
  const drift = interpolate(frame, [0, total], [0, 34], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  const glowPulse = interpolate(
    Math.sin((frame / fps) * 1.4),
    [-1, 1],
    [0.42, 0.64],
  );

  // シーン全体の出入り（opacity単独禁止 → 微translateYと併用）
  const sceneY = interpolate(frame, [0, 12], [18, 0], {
    extrapolateRight: 'clamp',
  });
  const sceneO = interpolate(
    frame,
    [0, 12, total - 12, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {/* Layer 1: フルスクリーン・シーン背景（グラデ） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 抑えたグリッド（ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 45%, black 28%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 45%, black 28%, transparent 84%)',
        }}
      />

      {/* Layer 3: アクセントグロー（微パルス） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 46% at 50% 46%, ${BRAND.color.electric}1f 0%, transparent 70%)`,
          opacity: glowPulse,
        }}
      />

      {/* Layer 4: ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.62) 100%)',
        }}
      />

      {/* ---- 主役: 比較バー ---- */}
      <AbsoluteFill
        style={{opacity: sceneO, transform: `translateY(${sceneY}px)`}}
      >
        {/* 抑えた軸: 左の縦ベースライン（recessive） */}
        <div
          style={{
            position: 'absolute',
            left: axisX,
            top: top0 - 34,
            width: 2,
            height: contentH + 68,
            backgroundColor: BRAND.color.silver,
            opacity: 0.22,
          }}
        />

        {items.map((item, i) => {
          const barTop = top0 + i * rowStride;
          const barColor =
            item.accent ??
            (i % 2 === 0 ? BRAND.color.gold : BRAND.color.electric);

          // スタッガー伸長（spring・等速禁止）
          const cs = spring({
            frame: frame - sec(fps, 0.3) - i * sec(fps, 0.14),
            fps,
            config: {damping: 18, mass: 1},
          });
          const grow = interpolate(cs, [0, 1], [0, 1]);
          const curW = Math.max(0, (item.value / max) * plotWidth * grow);
          const shown = formatVal(item.value, item.value * grow);

          // ラベルのマスク切れ上がり（棒と同じ位相でスタッガー）
          const labelReveal = spring({
            frame: frame - sec(fps, 0.18) - i * sec(fps, 0.14),
            fps,
            config: {damping: 16, mass: 0.9},
          });

          // 値ラベルの出（移動＋opacity＝opacity単独ではない）
          const valO = interpolate(cs, [0.2, 0.6], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <React.Fragment key={i}>
              {/* カテゴリ直接ラベル（棒の上・マスク切れ上がり） */}
              <div
                style={{
                  position: 'absolute',
                  left: axisX + 4,
                  top: barTop - 44,
                }}
              >
                <MaskLabel
                  text={item.label}
                  reveal={labelReveal}
                  size={30}
                  weight={600}
                  color={BRAND.color.white}
                  letterSpacing={1}
                />
              </div>

              {/* 抑えたトラック（データ端の伸び先を示す・depth） */}
              <div
                style={{
                  position: 'absolute',
                  left: axisX,
                  top: barTop,
                  width: plotWidth,
                  height: barH,
                  borderRadius: 4,
                  backgroundColor: BRAND.color.silver,
                  opacity: 0.06,
                }}
              />

              {/* 棒本体: 左ベースライン接地・4px角丸端・単一アクセント。
                  速い伸長に Trail でモーションブラー */}
              <div
                style={{
                  position: 'absolute',
                  left: axisX,
                  top: barTop,
                  width: plotWidth,
                  height: barH,
                }}
              >
                <Trail layers={4} lagInFrames={1.1} trailOpacity={0.5}>
                  <div
                    style={{
                      width: curW,
                      height: barH,
                      borderRadius: 4,
                      background: `linear-gradient(90deg, ${barColor}dd 0%, ${barColor} 100%)`,
                      boxShadow: `0 0 26px ${barColor}55`,
                    }}
                  />
                </Trail>
              </div>

              {/* 値の直接ラベル（棒の先端・カウントアップ・tabular-nums） */}
              <div
                style={{
                  position: 'absolute',
                  left: axisX + curW + 20,
                  top: barTop,
                  height: barH,
                  display: 'flex',
                  alignItems: 'center',
                  opacity: valO,
                  fontFamily: BRAND.font.display,
                  fontWeight: 400,
                  fontSize: 46,
                  color: BRAND.color.white,
                  fontVariantNumeric: 'tabular-nums',
                  letterSpacing: 0.5,
                  whiteSpace: 'nowrap',
                }}
              >
                {shown}
              </div>
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
