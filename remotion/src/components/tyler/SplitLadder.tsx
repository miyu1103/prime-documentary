import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// SplitLadder（三審の上昇・11:15 再フック）
//   入力: District Court → 8th Circuit → SCOTUS（CLM-0008）
//   モーション: 三段の階段が左下→右上へ組上がり、上昇プレイヘッド（発光ノード）が
//     段を昇って最上段 SCOTUS で着弾（Trail + 発火）。持続キャリア=段上昇プレイヘッド。
//   深度レイヤー: 暗背景 / 斜光ベッド / 階段段板 / 上昇プレイヘッド+グロー / 段ラベル
// =====================================================================

const {ink, navy, electric, silver, gold, white} = BRAND.color;

const STEPS = [
  {label: 'District Court', sub: 'dismissed'},
  {label: '8th Circuit', sub: 'affirmed'},
  {label: 'Supreme Court', sub: 'granted cert'},
];

export const SplitLadder: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const n = STEPS.length;
  // 各段の位置（左下→右上）
  const pos = (i: number) => ({x: 300 + i * 520, y: 780 - i * 220});

  // 上昇プレイヘッド進行（0..n-1・cubic-out）
  const prog = interpolate(frame, [18, dur - 16], [0, n - 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const seg = Math.floor(prog);
  const segT = prog - seg;
  const a = pos(Math.min(seg, n - 1));
  const b = pos(Math.min(seg + 1, n - 1));
  const easeT = 1 - Math.pow(1 - segT, 3);
  const headX = a.x + (b.x - a.x) * easeT;
  const headY = a.y + (b.y - a.y) * easeT;

  // 最上段着弾フラッシュ
  const landF = dur - 16;
  const land = spring({frame: frame - landF, fps, config: {damping: 8, mass: 0.6}});
  const moving = prog < n - 1.02;

  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 40% 60%, ${navy} 0%, ${ink} 86%)`, overflow: 'hidden'}}>
      {/* 斜光ベッド */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(120deg, transparent 30%, ${electric}14 50%, transparent 70%)`,
          mixBlendMode: 'screen',
          transform: `translateX(${Math.sin(frame / 40) * 14}px)`,
        }}
      />

      <div style={{position: 'absolute', top: 66, width: '100%', textAlign: 'center', fontFamily: BRAND.font.body, fontSize: 26, letterSpacing: 6, textTransform: 'uppercase', color: silver, opacity: interpolate(frame, [4, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
        The climb to the Court
      </div>

      <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position: 'absolute', inset: 0}}>
        {/* 連結ライン */}
        {STEPS.slice(1).map((_, i) => {
          const p0 = pos(i);
          const p1 = pos(i + 1);
          const draw = interpolate(frame, [18 + i * 20, 40 + i * 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <line
              key={i}
              x1={p0.x}
              y1={p0.y}
              x2={p0.x + (p1.x - p0.x) * draw}
              y2={p0.y + (p1.y - p0.y) * draw}
              stroke={`${silver}66`}
              strokeWidth={3}
              strokeDasharray="10 10"
            />
          );
        })}
      </svg>

      {/* 段板 */}
      {STEPS.map((s, i) => {
        const p = pos(i);
        const app = spring({frame: frame - i * 20 - 12, fps, config: {damping: 15}});
        const reached = prog >= i - 0.2;
        const topStep = i === n - 1;
        return (
          <div key={i} style={{position: 'absolute', left: p.x, top: p.y, transform: `translate(-50%, -50%) scale(${app})`}}>
            <div
              style={{
                width: 340,
                height: 96,
                background: `linear-gradient(180deg, ${navy} 0%, ${ink} 100%)`,
                border: `2px solid ${reached ? gold : electric}`,
                boxShadow: reached ? `0 0 26px ${gold}55, 0 10px 30px #000a` : `0 10px 30px #000a`,
                borderRadius: 8,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                transform: topStep ? `scale(${1 + land * 0.06})` : 'none',
              }}
            >
              <div style={{fontFamily: BRAND.font.display, fontSize: 40, color: reached ? white : silver, textShadow: reached ? `0 0 14px ${gold}` : 'none'}}>{s.label}</div>
              <div style={{fontFamily: BRAND.font.body, fontSize: 20, letterSpacing: 3, textTransform: 'uppercase', color: silver, opacity: 0.8}}>{s.sub}</div>
            </div>
          </div>
        );
      })}

      {/* 上昇プレイヘッド（Trail で軌跡） */}
      <Trail layers={6} lagInFrames={0.35} trailOpacity={0.5}>
        <div
          style={{
            position: 'absolute',
            left: headX,
            top: headY,
            transform: 'translate(-50%, -50%)',
            width: moving ? 20 : 26,
            height: moving ? 20 : 26,
            borderRadius: '50%',
            background: moving ? electric : gold,
            boxShadow: `0 0 24px ${moving ? electric : gold}, 0 0 60px ${moving ? electric : gold}aa`,
          }}
        />
      </Trail>
    </AbsoluteFill>
  );
};
