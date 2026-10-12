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
// EP36 williams — LineupLoop (code-built motion-graphic · SCENE)
//   SPN-0008 の核心：防犯動画 → 顔ソフト → ラインナップ → 同じ防犯動画、という
//   「循環する証明」を図解。3ノードが三角に立ち、矢印が順に描かれて輪が閉じ、
//   最後に "IT ALL POINTS BACK TO THE SAME BLUR" が出る。実在顔なし・数値なし。
//   規則: 全モーションにイージング/spring・opacity単独無し・スタッガー・
//   矢印描画は strokeDashoffset・速い動きに Trail・裏≥3レイヤー・マスク切れ上がり文字。
//   motionkitに循環図は無い → EP36専用新規（invariant 14適合）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

type NodeDef = {id: string; x: number; y: number; kicker: string; title: string};

export const LineupLoop: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const cx = width / 2;
  const cy = height / 2 + 20;
  const NODES: NodeDef[] = [
    {id: 'A', x: cx, y: cy - 250, kicker: 'STEP 1', title: 'SECURITY VIDEO'},
    {id: 'B', x: cx + 360, y: cy + 150, kicker: 'STEP 2', title: 'FACE SOFTWARE'},
    {id: 'C', x: cx - 360, y: cy + 150, kicker: 'STEP 3', title: 'PHOTO LINEUP'},
  ];
  const NW = 300;
  const NH = 128;

  const groupO = interpolate(frame, [0, sec(fps, 0.3), total - sec(fps, 0.5), total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = Math.sin(frame * 0.05) * 4;

  // ノード出現（スタッガー spring・scale/translate）
  const nodeS = (i: number) =>
    spring({frame: frame - sec(fps, 0.2) - i * sec(fps, 0.28), fps, config: {damping: 13, mass: 0.9}});

  // 矢印: A→B (t1), B→C (t2), C→A (t3・輪が閉じる)
  const arrowP = (start: number, end: number) =>
    interpolate(frame, [sec(fps, start), sec(fps, end)], [0, 1], {
      easing: Easing.inOut(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  const p1 = arrowP(1.1, 1.7);
  const p2 = arrowP(1.7, 2.3);
  const p3 = arrowP(2.3, 3.0); // 閉じる矢印

  // 輪が閉じた後のパルス（循環を強調）
  const closed = spring({frame: frame - sec(fps, 3.0), fps, config: {damping: 14}});
  const loopPulse = 0.6 + 0.4 * Math.sin((frame - sec(fps, 3.0)) * 0.16);
  const closeGlow = interpolate(closed, [0, 1], [0, 1]);

  // 中央ラベル（マスク切れ上がり）
  const lab = spring({frame: frame - sec(fps, 3.2), fps, config: {damping: 16}});
  const labY = interpolate(lab, [0, 1], [110, 0]);
  const labO = interpolate(lab, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // ノード境界から相手方向へ少し内側の接続点を返す（矢印が箱に食い込まないように）
  const edgePoint = (from: NodeDef, to: NodeDef) => {
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const ang = Math.atan2(dy, dx);
    // 箱の半径方向おおよそ
    const ex = from.x + Math.cos(ang) * (NW / 2 + 8);
    const ey = from.y + Math.sin(ang) * (NH / 2 + 8);
    return {x: ex, y: ey};
  };

  const Arrow: React.FC<{from: NodeDef; to: NodeDef; p: number; color: string}> = ({from, to, p, color}) => {
    const a = edgePoint(from, to);
    const b = edgePoint(to, from);
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    // 現在の先端
    const hx = a.x + (b.x - a.x) * p;
    const hy = a.y + (b.y - a.y) * p;
    const ang = Math.atan2(b.y - a.y, b.x - a.x);
    return (
      <g>
        <line
          x1={a.x}
          y1={a.y}
          x2={b.x}
          y2={b.y}
          stroke={color}
          strokeWidth={4}
          strokeLinecap="round"
          strokeDasharray={len}
          strokeDashoffset={len * (1 - p)}
          style={{filter: `drop-shadow(0 0 8px ${color}88)`}}
        />
        {/* 先端の矢じり */}
        {p > 0.02 && p < 0.999 ? (
          <g transform={`translate(${hx},${hy}) rotate(${(ang * 180) / Math.PI})`}>
            <path d="M0,0 L-18,-9 L-18,9 Z" fill={color} />
          </g>
        ) : null}
        {/* 着地の矢じり（描画完了後は相手ノード手前に固定） */}
        {p >= 0.999 ? (
          <g transform={`translate(${b.x},${b.y}) rotate(${(ang * 180) / Math.PI})`}>
            <path d="M0,0 L-18,-9 L-18,9 Z" fill={color} />
          </g>
        ) : null}
      </g>
    );
  };

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* レイヤー1: グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 100% at 50% 45%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 64%, #05070d 100%)`,
        }}
      />
      {/* レイヤー2: 微グリッド（ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `repeating-linear-gradient(0deg, ${BRAND.color.electric}18 0px, ${BRAND.color.electric}18 1px, transparent 1px, transparent 70px), repeating-linear-gradient(90deg, ${BRAND.color.electric}18 0px, ${BRAND.color.electric}18 1px, transparent 1px, transparent 70px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
        }}
      />
      {/* レイヤー3: 中央グロー（閉輪で強まる） */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: 760,
            height: 620,
            marginTop: 20,
            background: `radial-gradient(closest-side, ${BRAND.color.gold}${closeGlow > 0.4 ? '2e' : '18'} 0%, transparent 72%)`,
            filter: 'blur(30px)',
            opacity: groupO * (0.6 + closeGlow * 0.4),
          }}
        />
      </AbsoluteFill>

      {/* 矢印（SVG・Trailでモーションブラー） */}
      <Trail layers={4} lagInFrames={1} trailOpacity={0.35}>
        <AbsoluteFill style={{opacity: groupO}}>
          <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0}}>
            <Arrow from={NODES[0]} to={NODES[1]} p={p1} color={BRAND.color.electric} />
            <Arrow from={NODES[1]} to={NODES[2]} p={p2} color={BRAND.color.electric} />
            <Arrow from={NODES[2]} to={NODES[0]} p={p3} color={BRAND.color.gold} />
          </svg>
        </AbsoluteFill>
      </Trail>

      {/* ノード箱 */}
      <AbsoluteFill style={{opacity: groupO, transform: `translateY(${drift * 0.4}px)`}}>
        {NODES.map((n, i) => {
          const s = nodeS(i);
          const sc = interpolate(s, [0, 1], [0.6, 1]);
          const o = interpolate(s, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});
          const isClose = n.id === 'A'; // 閉輪の戻り先を強調
          return (
            <div
              key={n.id}
              style={{
                position: 'absolute',
                left: n.x - NW / 2,
                top: n.y - NH / 2,
                width: NW,
                height: NH,
                borderRadius: 12,
                background: `linear-gradient(160deg, ${BRAND.color.navy}, ${BRAND.color.ink})`,
                border: `2px solid ${isClose && closeGlow > 0.4 ? BRAND.color.gold : BRAND.color.electric}${isClose && closeGlow > 0.4 ? 'ff' : '99'}`,
                boxShadow:
                  isClose && closeGlow > 0.4
                    ? `0 0 30px 4px ${BRAND.color.gold}${Math.round(loopPulse * 160).toString(16).padStart(2, '0')}`
                    : `0 0 18px ${BRAND.color.electric}33`,
                transform: `scale(${sc})`,
                opacity: o,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                gap: 6,
              }}
            >
              <div style={{fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 18, letterSpacing: 3, color: BRAND.color.gold}}>
                {n.kicker}
              </div>
              <div style={{fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 32, letterSpacing: 1, color: BRAND.color.white}}>
                {n.title}
              </div>
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 中央ラベル（輪が閉じた後） */}
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', opacity: groupO}}>
        <div style={{marginBottom: 70, overflow: 'hidden', paddingBottom: '0.14em', textAlign: 'center', maxWidth: 900}}>
          <div
            style={{
              transform: `translateY(${labY}%)`,
              opacity: labO,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: 40,
              letterSpacing: 1,
              color: BRAND.color.gold,
              textShadow: `0 0 22px ${BRAND.color.gold}66`,
            }}
          >
            IT ALL POINTS BACK TO THE SAME BLUR
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
