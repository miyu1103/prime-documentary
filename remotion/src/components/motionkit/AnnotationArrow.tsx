import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// AnnotationArrow — 実写フッテージに重ねる注釈用の矢印（オーバーレイ）
//   shaft : from→to へ strokeDashoffset を spring で描き上げる（等速なし）
//   head  : shaft がほぼ描き終わった所で spring scale でポップ（オーバーシュート）
//   label : tail 付近で overflow:hidden マスク切り上がり（任意）
//   アクセントは electric（主）/ gold（従）を座標シードで決定的に選択。
//   透明背景・root pointerEvents:'none'。座標は 0..1 のフレーム比率。
//   常時わずかに脈動（紙芝居/完全静止の回避）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const DROP = '0 3px 16px rgba(0,0,0,0.85), 0 1px 4px rgba(0,0,0,0.9)';

export const AnnotationArrow: React.FC<{
  from: [number, number];
  to: [number, number];
  label?: string;
  dur?: number;
}> = ({from, to, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- 座標（0..1 → px） --------------------------------------------
  const fx = from[0] * width;
  const fy = from[1] * height;
  const tx = to[0] * width;
  const ty = to[1] * height;
  const dx = tx - fx;
  const dy = ty - fy;
  const len = Math.max(1, Math.hypot(dx, dy));
  const angleDeg = (Math.atan2(dy, dx) * 180) / Math.PI;

  // ---- アクセント（座標シードで決定的に electric/gold） -------------
  const accent =
    random(`arrow-${from[0]}-${from[1]}-${to[0]}-${to[1]}`) > 0.74
      ? BRAND.color.gold
      : BRAND.color.electric;

  // ---- グループの出入り（opacity単独禁止 → 微translateYと併用） ------
  const outStart = total - sec(fps, 0.4);
  const groupY = interpolate(
    frame,
    [0, sec(fps, 0.25), outStart, total],
    [10, 0, 0, 10],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );
  const groupO = interpolate(
    frame,
    [0, sec(fps, 0.2), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- shaft：spring で描き上げ（strokeDashoffset） -----------------
  const shaftSpring = spring({
    frame: frame - sec(fps, 0.05),
    fps,
    config: {damping: 26, mass: 1, stiffness: 120},
  });
  const drawP = interpolate(shaftSpring, [0, 1], [0, 1]);
  const dashOffset = len * (1 - drawP);

  // ---- arrowhead：shaft がほぼ描けた所でポップ（overshoot） ---------
  const headSpring = spring({
    frame: frame - sec(fps, 0.42),
    fps,
    config: {damping: 10, mass: 0.7, stiffness: 170},
  });
  const headScale = interpolate(headSpring, [0, 0.6, 1], [0, 1.18, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const headLen = 34;
  const headW = 21;

  // ---- 常時わずかな脈動（完全静止の回避） --------------------------
  const pulse = 0.5 + 0.5 * Math.sin((frame / fps) * 3.2);
  const glowBlur = 7 + pulse * 6;

  // ---- label：tail 付近でマスク切り上がり --------------------------
  const labSpring = spring({
    frame: frame - sec(fps, 0.5),
    fps,
    config: {damping: 16, mass: 0.9, stiffness: 130},
  });
  const labY = interpolate(labSpring, [0, 1], [112, 0]);
  const labO = interpolate(labSpring, [0, 0.25], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{background: 'transparent', pointerEvents: 'none'}}>
      <AbsoluteFill
        style={{transform: `translateY(${groupY}px)`, opacity: groupO}}
      >
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          style={{position: 'absolute', inset: 0}}
        >
          {/* グロー下地（太い半透明のシャフト） */}
          <line
            x1={fx}
            y1={fy}
            x2={tx}
            y2={ty}
            stroke={accent}
            strokeWidth={11}
            strokeLinecap="round"
            opacity={0.22}
            strokeDasharray={len}
            strokeDashoffset={dashOffset}
          />
          {/* 本体シャフト */}
          <line
            x1={fx}
            y1={fy}
            x2={tx}
            y2={ty}
            stroke={accent}
            strokeWidth={5}
            strokeLinecap="round"
            strokeDasharray={len}
            strokeDashoffset={dashOffset}
            style={{filter: `drop-shadow(0 0 ${glowBlur}px ${accent}bb)`}}
          />
          {/* tail のアンカードット（脈動でわずかに動く） */}
          <circle
            cx={fx}
            cy={fy}
            r={5 + pulse * 1.4}
            fill={BRAND.color.white}
            stroke={accent}
            strokeWidth={2.5}
            opacity={labO || drawP}
          />
          {/* arrowhead：先端 (0,0) をローカル原点にして回転＋スケール */}
          <g
            transform={`translate(${tx}, ${ty}) rotate(${angleDeg}) scale(${headScale})`}
            style={{filter: `drop-shadow(0 0 ${glowBlur}px ${accent}cc)`}}
          >
            <polygon
              points={`0,0 ${-headLen},${-headW} ${-headLen * 0.62},0 ${-headLen},${headW}`}
              fill={accent}
            />
          </g>
        </svg>

        {/* label：tail 付近。overflow:hidden マスク切り上がり */}
        {label ? (
          <div
            style={{
              position: 'absolute',
              left: `${from[0] * 100}%`,
              top: `${from[1] * 100}%`,
              transform: 'translate(-50%, -150%)',
              maxWidth: 520,
            }}
          >
            <Trail layers={4} lagInFrames={1} trailOpacity={0.4}>
              <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
                <div
                  style={{
                    transform: `translateY(${labY}%)`,
                    opacity: labO,
                    color: BRAND.color.white,
                    fontFamily: BRAND.font.display,
                    fontWeight: 900,
                    fontSize: 40,
                    lineHeight: 1.05,
                    letterSpacing: 0.5,
                    textTransform: 'uppercase',
                    textAlign: 'center',
                    textShadow: `0 0 22px ${accent}88, ${DROP}`,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {label}
                </div>
              </div>
            </Trail>
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
