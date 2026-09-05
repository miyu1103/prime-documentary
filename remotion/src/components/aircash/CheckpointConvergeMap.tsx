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
// CheckpointConvergeMap — 概略マップ（地理地図でない）：3つの主体
//   （TSA / 州警官 / DEA）が、それぞれ有向ルートに沿って「動く点」を
//   検問ノードへ送り込み、1点に CONVERGE（集結）する図。
//   ・主運動＝3ルートを走り続ける有向パーティクル（点が実移動）＝§7持続床
//   ・各ルートは先頭アロー(lead)が一度走破→到達で検問がパルス
//   ・その後もストリームは全編流れ続ける（凍らない・freeze>4s禁止）
//   ・奥行き≥3層（グラデ背景／グリッド＋塵／ルート線／パーティクル／ノード／ラベル）
//   ・単一アクセント=electric・暗navy背景・凍らない微シマー
//   全モーションeased(spring/Easing)・opacity単独リビール無し（rise/scale/描画/実移動と対）
//   ・fps算出・deterministic（useCurrentFrameのみ・seeded mulberry32）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);
const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 108% at 60% 46%, ${BRAND.color.navy} 0%, ${BG} 82%)`;

// 決定論的擬似乱数（Math.random禁止・塵フィールドの座標に使用）
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

type Pt = {x: number; y: number};

type Props = {
  dur?: number;
  actors?: [string, string, string];
  checkpointLabel?: string;
};

export const CheckpointConvergeMap: React.FC<Props> = ({
  dur,
  actors = ['TSA', 'STATE POLICE', 'DEA'],
  checkpointLabel = 'CHECKPOINT',
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  const ACCENT = BRAND.color.electric;

  // 検問ノード（右中央）と3つの起点（左に扇状）— 左→右へ集結
  const checkpoint: Pt = {x: width * 0.66, y: height * 0.5};
  const routes: {origin: Pt; label: string; delay: number}[] = [
    {origin: {x: width * 0.16, y: height * 0.22}, label: actors[0], delay: 0.15},
    {origin: {x: width * 0.11, y: height * 0.52}, label: actors[1], delay: 0.27},
    {origin: {x: width * 0.18, y: height * 0.82}, label: actors[2], delay: 0.39},
  ];

  // ルートごとの幾何（距離・角度）を確定
  const geom = routes.map((r) => {
    const dx = checkpoint.x - r.origin.x;
    const dy = checkpoint.y - r.origin.y;
    const len = Math.hypot(dx, dy);
    const ang = (Math.atan2(dy, dx) * 180) / Math.PI;
    return {...r, dx, dy, len, ang};
  });

  const lerp = (o: Pt, dx: number, dy: number, t: number): Pt => ({
    x: o.x + dx * t,
    y: o.y + dy * t,
  });

  // --- タイムライン（全て fps 算出）---
  // 1) 検問ノード立ち上がり（scale + rise）
  const cpS = spring({
    frame: frame - sec(fps, 0.2),
    fps,
    config: {damping: 18, mass: 0.9},
  });
  const cpScale = interpolate(cpS, [0, 1], [0.2, 1]);
  const cpRise = interpolate(cpS, [0, 1], [46, 0]);

  // 凍らない微シマー（検問コアの呼吸・主運動ではない補助）
  const corePulse = interpolate(Math.sin((frame / fps) * Math.PI * 2 * 0.5), [-1, 1], [0.55, 1]);
  const gridDrift = interpolate(frame, [0, D], [0, 26], {
    easing: Easing.inOut(Easing.sin),
  });

  // 連続ストリームの主運動パラメータ
  const streamPeriod = 2.35; // 1粒が起点→検問を走る秒数
  const particlesPerRoute = 5;

  // シーン出入り（opacityは補助・実移動/riseが主）
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 12], [22, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // 決定論的な塵フィールド（奥行き）
  const rand = mulberry32(0x34a1c);
  const dust = Array.from({length: 34}).map(() => ({
    x: rand() * width,
    y: rand() * height,
    r: 0.6 + rand() * 1.8,
    ph: rand() * Math.PI * 2,
    sp: 0.15 + rand() * 0.5,
  }));

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド（概略マップの地）＋ドリフト */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 74px),
            repeating-linear-gradient(90deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 74px)`,
          maskImage: 'radial-gradient(120% 95% at 55% 50%, black 32%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 95% at 55% 50%, black 32%, transparent 84%)',
        }}
      />
      {/* L3 検問裏のグロー（到達で強まる） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(24% 30% at ${(checkpoint.x / width) * 100}% ${
            (checkpoint.y / height) * 100
          }%, ${ACCENT}2a 0%, transparent 66%)`,
        }}
      />

      <AbsoluteFill
        style={{
          opacity: inO * outO,
          transform: `translateY(${inY}px)`,
        }}
      >
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="ccm-route" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={`${BRAND.color.silver}22`} />
              <stop offset="100%" stopColor={`${ACCENT}bb`} />
            </linearGradient>
          </defs>

          {/* 塵フィールド（奥行き・微シマー） */}
          {dust.map((d, i) => {
            const tw = interpolate(
              Math.sin((frame / fps) * Math.PI * 2 * d.sp + d.ph),
              [-1, 1],
              [0.12, 0.5],
            );
            return (
              <circle key={`d${i}`} cx={d.x} cy={d.y} r={d.r} fill={BRAND.color.silver} opacity={tw} />
            );
          })}

          {/* ---- ルート線（stroke描画＝リビールが実運動）---- */}
          {geom.map((r, i) => {
            const drawStart = 0.5 + i * 0.15;
            const drawP = interpolate(
              frame,
              [sec(fps, drawStart), sec(fps, drawStart + 0.55)],
              [0, 1],
              {
                easing: Easing.out(Easing.cubic),
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              },
            );
            return (
              <line
                key={`r${i}`}
                x1={r.origin.x}
                y1={r.origin.y}
                x2={checkpoint.x}
                y2={checkpoint.y}
                stroke="url(#ccm-route)"
                strokeWidth={2.5}
                strokeLinecap="round"
                strokeDasharray={r.len}
                strokeDashoffset={r.len * (1 - drawP)}
                opacity={0.8}
              />
            );
          })}

          {/* ---- 起点ノード（各主体・rise+scaleで登場）---- */}
          {geom.map((r, i) => {
            const s = spring({
              frame: frame - sec(fps, r.delay),
              fps,
              config: {damping: 17, mass: 0.9},
            });
            const sc = interpolate(s, [0, 1], [0.2, 1]);
            const ry = interpolate(s, [0, 1], [40, 0]);
            return (
              <g key={`o${i}`} transform={`translate(${r.origin.x},${r.origin.y + ry}) scale(${sc})`}>
                <circle r={30} fill={`${ACCENT}18`} />
                <circle r={19} fill={BRAND.color.navy} stroke={BRAND.color.silver} strokeWidth={3} />
                <circle r={7} fill={ACCENT} />
              </g>
            );
          })}

          {/* ---- 到達パルスリング（lead着弾で拡がる）---- */}
          {geom.map((r, i) => {
            const leadStart = 0.9 + i * 0.35;
            const arriveFrame = sec(fps, leadStart + 1.05);
            const ringS = spring({
              frame: frame - arriveFrame,
              fps,
              config: {damping: 12, mass: 0.7},
            });
            const ringScale = interpolate(ringS, [0, 1], [0.4, 1.9]);
            const ringO = interpolate(ringS, [0, 0.25, 1], [0, 0.85, 0], {
              extrapolateRight: 'clamp',
            });
            if (ringO <= 0.01) return null;
            return (
              <circle
                key={`pr${i}`}
                cx={checkpoint.x}
                cy={checkpoint.y + cpRise}
                r={54 * ringScale}
                fill="none"
                stroke={ACCENT}
                strokeWidth={3}
                opacity={ringO}
              />
            );
          })}

          {/* ---- 検問ノード（集結先・scale+riseで登場）---- */}
          <g transform={`translate(${checkpoint.x},${checkpoint.y + cpRise}) scale(${cpScale})`}>
            <circle r={64} fill={ACCENT} opacity={0.12 * corePulse} />
            <circle r={46} fill={BRAND.color.navy} stroke={ACCENT} strokeWidth={5} opacity={corePulse} />
            {/* 検問ゲートのバー（概略） */}
            <rect x={-34} y={-5} width={68} height={10} rx={3} fill={ACCENT} opacity={corePulse} />
            <rect x={-5} y={-34} width={10} height={68} rx={3} fill={`${ACCENT}88`} />
            <circle r={10} fill={BRAND.color.white} opacity={corePulse} />
          </g>
        </svg>

        {/* ---- 有向パーティクル（主運動：全編ルートを走り続ける実移動）---- */}
        {/* Trailは AbsoluteFill をラップ（inline flex rowは直接ラップしない） */}
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.45}>
          <AbsoluteFill>
            {geom.map((r, i) => {
              const streamStart = 0.5 + i * 0.15 + 0.55; // ルート描画完了後
              const active = frame >= sec(fps, streamStart);
              if (!active) return null;
              const tSec = frame / fps;
              return Array.from({length: particlesPerRoute}).map((_, k) => {
                const phase = k / particlesPerRoute;
                let t = ((tSec - streamStart) / streamPeriod + phase) % 1;
                if (t < 0) t += 1;
                const p = lerp(r.origin, r.dx, r.dy, t);
                // 端で生成/消滅（実移動が主・opacityは形状整形の補助）
                const edge = interpolate(
                  t,
                  [0, 0.08, 0.9, 1],
                  [0, 1, 1, 0],
                  {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
                );
                return (
                  <div
                    key={`p${i}-${k}`}
                    style={{
                      position: 'absolute',
                      left: p.x,
                      top: p.y,
                      width: 15,
                      height: 15,
                      marginLeft: -7.5,
                      marginTop: -7.5,
                      transform: `rotate(${r.ang}deg)`,
                      opacity: edge,
                    }}
                  >
                    {/* 進行方向を指す小アロー */}
                    <svg width={15} height={15} viewBox="-8 -8 16 16">
                      <path
                        d="M6,0 L-5,-5 L-2,0 L-5,5 Z"
                        fill={BRAND.color.white}
                        stroke={ACCENT}
                        strokeWidth={1.5}
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                );
              });
            })}
          </AbsoluteFill>
        </Trail>

        {/* ---- 先頭アロー（lead：各ルートを一度走破・到達で検問パルス）---- */}
        <Trail layers={6} lagInFrames={1.15} trailOpacity={0.5}>
          <AbsoluteFill>
            {geom.map((r, i) => {
              const leadStart = 0.9 + i * 0.35;
              const leadP = interpolate(
                frame,
                [sec(fps, leadStart), sec(fps, leadStart + 1.05)],
                [0, 1],
                {
                  easing: Easing.out(Easing.cubic),
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                },
              );
              if (leadP <= 0 || leadP >= 1) return null;
              const p = lerp(r.origin, r.dx, r.dy, leadP);
              return (
                <div
                  key={`lead${i}`}
                  style={{
                    position: 'absolute',
                    left: p.x - 13,
                    top: p.y - 13,
                    width: 26,
                    height: 26,
                    borderRadius: '50%',
                    background: BRAND.color.white,
                    boxShadow: `0 0 26px 8px ${ACCENT}, 0 0 9px 3px ${BRAND.color.white}`,
                  }}
                />
              );
            })}
          </AbsoluteFill>
        </Trail>

        {/* ---- 起点ラベル（overflow:hidden + translateY マスク切り上がり）---- */}
        {geom.map((r, i) => {
          const ls = spring({
            frame: frame - sec(fps, r.delay + 0.2),
            fps,
            config: {damping: 16, mass: 0.9},
          });
          const ly = interpolate(ls, [0, 1], [110, 0]);
          const lo = interpolate(ls, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
          return (
            <div
              key={`lb${i}`}
              style={{
                position: 'absolute',
                left: r.origin.x - 130,
                top: r.origin.y + 34,
                width: 260,
                textAlign: 'center',
                overflow: 'hidden',
                paddingBottom: '0.16em',
              }}
            >
              <div
                style={{
                  transform: `translateY(${ly}%)`,
                  opacity: lo,
                  fontFamily: BRAND.font.body,
                  fontWeight: 700,
                  fontSize: 28,
                  letterSpacing: 3,
                  color: BRAND.color.silver,
                }}
              >
                {r.label}
              </div>
            </div>
          );
        })}

        {/* ---- 検問ラベル（マスク切り上がり）---- */}
        <div
          style={{
            position: 'absolute',
            left: checkpoint.x - 200,
            top: checkpoint.y + 86,
            width: 400,
            textAlign: 'center',
            overflow: 'hidden',
            paddingBottom: '0.16em',
          }}
        >
          <div
            style={{
              transform: `translateY(${interpolate(
                spring({frame: frame - sec(fps, 1.5), fps, config: {damping: 16}}),
                [0, 1],
                [120, 0],
              )}%)`,
              fontFamily: BRAND.font.display,
              fontWeight: 800,
              fontSize: 42,
              letterSpacing: 6,
              color: ACCENT,
            }}
          >
            {checkpointLabel}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
