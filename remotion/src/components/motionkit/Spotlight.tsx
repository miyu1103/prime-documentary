import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../../brand';

// =====================================================================
// Spotlight — 実映像の上に重ねる「一点だけ残す」暗幕オーバーレイ（透明）。
//   画面全体を BRAND.color.ink で暗くし、cx,cy を中心に半径 r の柔らかい
//   円窓だけを開けて素材を覗かせる（混み合ったショットのディテール強調用）。
//   窓は r が spring で 0 から開き、常時わずかに息づく（静止禁止）。
//   SVG マスク（白 rect ＋ feGaussianBlur した黒円の穴）で実装。
//   root は pointerEvents:'none'、暗幕以外は完全に透明。
//   cx, cy, r は 0..1 のフレーム比。dim=暗部の不透明度(既定0.72)。
//   dur=有効フレーム数(既定 durationInFrames)。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

export const Spotlight: React.FC<{
  cx: number;
  cy: number;
  r: number;
  dim?: number;
  dur?: number;
}> = ({cx, cy, r, dim = 0.72, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 複数マウントしても衝突しない一意 id（mask/filter 参照用）
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const maskId = `spot-mask-${uid}`;
  const blurId = `spot-blur-${uid}`;

  // 半径の基準は短辺。r=0.5 で短辺の半分（≒画面中央に収まる円）。
  const base = Math.min(width, height);

  // 窓が開く：r を spring で 0 → 1（イージング必須・線形禁止）
  const open = spring({
    frame,
    fps,
    config: {damping: 18, mass: 1, stiffness: 90},
  });

  // 常時わずかに息づく（静止しない）— sin は本質的にイーズド
  const breath = Math.sin((frame / fps) * 1.25) * 0.012; // ±1.2% の呼吸
  const rFrac = Math.max(0, r * open + r * breath);
  const rPx = rFrac * base;

  // 柔らかいエッジ：半径に比例したガウスぼかし（下限あり）
  const blurPx = Math.max(8, rPx * 0.16);

  // 暗幕の出入り：0 → dim（開き）… 終端 0.5s で dim → 0（畳む）
  const outStart = total - sec(fps, 0.5);
  const dimNow = interpolate(
    frame,
    [0, sec(fps, 0.35), Math.max(sec(fps, 0.35) + 1, outStart), total],
    [0, dim, dim, 0],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // 円窓のリムに微かな electric ブルーの光（開きと呼吸に同調・素材の上に加算）
  const rimO = interpolate(open, [0, 0.6, 1], [0, 0.28, 0.22], {
    extrapolateRight: 'clamp',
  });
  const rimStroke = Math.max(2, rPx * 0.02);
  const rimBlur = Math.max(4, rPx * 0.05);

  const cxPx = cx * width;
  const cyPx = cy * height;

  return (
    <AbsoluteFill style={{pointerEvents: 'none', background: 'transparent'}}>
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{position: 'absolute', inset: 0, display: 'block'}}
      >
        <defs>
          <filter
            id={blurId}
            x="-50%"
            y="-50%"
            width="200%"
            height="200%"
            filterUnits="objectBoundingBox"
          >
            <feGaussianBlur stdDeviation={blurPx} />
          </filter>
          <mask
            id={maskId}
            maskUnits="userSpaceOnUse"
            x={0}
            y={0}
            width={width}
            height={height}
          >
            {/* 白 = 暗幕を残す */}
            <rect x={0} y={0} width={width} height={height} fill="#ffffff" />
            {/* 黒（ぼかし）= 円窓の穴。ぼけたグレー縁が柔らかいエッジになる */}
            <circle
              cx={cxPx}
              cy={cyPx}
              r={rPx}
              fill="#000000"
              filter={`url(#${blurId})`}
            />
          </mask>
        </defs>

        {/* 暗幕本体（円窓以外を暗く） */}
        <rect
          x={0}
          y={0}
          width={width}
          height={height}
          fill={BRAND.color.ink}
          fillOpacity={dimNow}
          mask={`url(#${maskId})`}
        />

        {/* 円窓リムの微光（加算的なアクセント／素材の上） */}
        <circle
          cx={cxPx}
          cy={cyPx}
          r={rPx}
          fill="none"
          stroke={BRAND.color.electric}
          strokeWidth={rimStroke}
          strokeOpacity={rimO * (dim === 0 ? 0 : dimNow / dim)}
          style={{filter: `blur(${rimBlur}px)`}}
        />
      </svg>
    </AbsoluteFill>
  );
};
