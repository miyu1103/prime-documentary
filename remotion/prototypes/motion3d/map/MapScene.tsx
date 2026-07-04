import React, {useMemo} from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import mapData from './us_map.json';

// =====================================================================
// MapScene — 「アニメーション地図」: 米国州がスタッガーで描かれて光り、都市ピンが
//   波紋で出現、資金ルートの弧が引かれて光の点が走る。ドキュメンタリーの地理可視化。
//   データ: us_map.json（US Census/us-atlas由来＝パブリックドメイン, d3 geoAlbersUsaで投影）。
// =====================================================================

export type MapSceneProps = {accent: string; title: string; highlight: string[]};
export const mapSceneDurationInFrames = (fps: number) => Math.round(fps * 9);

const BG = '#06080f';
const sec = (fps: number, s: number) => Math.round(fps * s);

type Pin = {name: string; x: number; y: number};
const data = mapData as {
  W: number;
  H: number;
  states: {name: string; d: string}[];
  pins: Pin[];
};

// 資金ルート（pin index）
const ROUTES: [number, number][] = [
  [0, 4], // NY → Washington
  [4, 3], // Washington → Chicago
  [3, 1], // Chicago → LA
  [2, 0], // Miami → NY
];

// 二次ベジェ上の点
const qbez = (p0: number[], c: number[], p2: number[], t: number) => {
  const u = 1 - t;
  return [
    u * u * p0[0] + 2 * u * t * c[0] + t * t * p2[0],
    u * u * p0[1] + 2 * u * t * c[1] + t * t * p2[1],
  ];
};

export const MapScene: React.FC<MapSceneProps> = ({accent, title, highlight}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const hi = new Set(highlight);

  // 州の描画順（左→右でスタッガー）
  const order = useMemo(
    () =>
      data.states
        .map((s, i) => ({i, x: (s.d.match(/M([\d.]+)/)?.[1] ?? '0') as string}))
        .sort((a, b) => parseFloat(a.x) - parseFloat(b.x))
        .map((o) => o.i),
    [],
  );
  const rank = useMemo(() => {
    const r: Record<number, number> = {};
    order.forEach((idx, k) => (r[idx] = k));
    return r;
  }, [order]);

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* 背景グロー＋グリッド感 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(90% 90% at 50% 45%, #0e1626 0%, ${BG} 70%)`,
        }}
      />

      <svg width={width} height={height} viewBox={`0 0 ${data.W} ${data.H}`} style={{position: 'absolute', inset: 0}}>
        {/* 州 */}
        {data.states.map((s, i) => {
          const start = 0.2 + rank[i] * 0.012;
          const draw = spring({frame: frame - sec(fps, start), fps, config: {damping: 200, mass: 0.6}});
          const isHi = hi.has(s.name);
          const hiSpring = spring({frame: frame - sec(fps, 1.7 + (rank[i] % 6) * 0.06), fps, config: {damping: 18}});
          const fillA = isHi ? interpolate(hiSpring, [0, 1], [0, 0.32]) : 0.04 * draw;
          return (
            <path
              key={i}
              d={s.d}
              fill={isHi ? accent : '#8fb6d8'}
              fillOpacity={fillA}
              stroke={accent}
              strokeWidth={1}
              strokeOpacity={0.35 * draw}
              style={{
                strokeDasharray: 1200,
                strokeDashoffset: 1200 * (1 - draw),
              }}
            />
          );
        })}

        {/* 資金ルートの弧 */}
        {ROUTES.map(([a, b], i) => {
          const pa = data.pins[a];
          const pb = data.pins[b];
          const p0 = [pa.x, pa.y];
          const p2 = [pb.x, pb.y];
          const mid = [(pa.x + pb.x) / 2, (pa.y + pb.y) / 2];
          const dist = Math.hypot(pb.x - pa.x, pb.y - pa.y);
          const c = [mid[0], mid[1] - dist * 0.32];
          const dPath = `M${p0[0]},${p0[1]} Q${c[0]},${c[1]} ${p2[0]},${p2[1]}`;
          const start = 3.0 + i * 0.5;
          const p = interpolate(
            spring({frame: frame - sec(fps, start), fps, config: {damping: 26}}),
            [0, 1],
            [0, 1],
          );
          const len = dist * 1.6;
          // 弧上を走る光点
          const dot = qbez(p0, c, p2, p);
          return (
            <g key={`r${i}`}>
              <path
                d={dPath}
                fill="none"
                stroke={accent}
                strokeWidth={2.5}
                opacity={0.75}
                strokeLinecap="round"
                style={{strokeDasharray: len, strokeDashoffset: len * (1 - p)}}
              />
              {p > 0.02 && p < 0.999 ? (
                <circle cx={dot[0]} cy={dot[1]} r={7} fill="#fff">
                  <title>{`${data.pins[a].name}→${data.pins[b].name}`}</title>
                </circle>
              ) : null}
            </g>
          );
        })}

        {/* 都市ピン＋波紋 */}
        {data.pins.map((pin, i) => {
          const start = 2.3 + i * 0.14;
          const pop = spring({frame: frame - sec(fps, start), fps, config: {damping: 13, mass: 0.7}});
          const r = interpolate(pop, [0, 1], [0, 9]);
          const o = interpolate(pop, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
          // 波紋（繰り返し拡大）
          const rippleT = ((frame - sec(fps, start)) % sec(fps, 1.4)) / sec(fps, 1.4);
          const rr = interpolate(rippleT, [0, 1], [9, 46]);
          const ro = interpolate(rippleT, [0, 1], [0.5, 0]) * o;
          return (
            <g key={`p${i}`} opacity={o}>
              <circle cx={pin.x} cy={pin.y} r={rr} fill="none" stroke={accent} strokeWidth={2} opacity={ro} />
              <circle cx={pin.x} cy={pin.y} r={r + 8} fill={accent} opacity={0.18} />
              <circle cx={pin.x} cy={pin.y} r={r} fill="#0b1020" stroke={accent} strokeWidth={2.5} />
              <text x={pin.x} y={pin.y - 22} fill="#fff" fontFamily="Inter, system-ui" fontWeight={700} fontSize={20} textAnchor="middle">
                {pin.name}
              </text>
            </g>
          );
        })}
      </svg>

      {/* タイトル */}
      <div
        style={{
          position: 'absolute',
          top: 70,
          left: 90,
          fontFamily: 'Inter, system-ui, sans-serif',
          fontWeight: 800,
          fontSize: 54,
          letterSpacing: -1,
          color: '#fff',
          opacity: interpolate(frame, [6, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          transform: `translateY(${interpolate(frame, [6, 30], [16, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px)`,
        }}
      >
        {title}
      </div>

      {/* ビネット */}
      <AbsoluteFill
        style={{
          background: 'radial-gradient(120% 100% at 50% 50%, transparent 50%, rgba(0,0,0,0.62) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
