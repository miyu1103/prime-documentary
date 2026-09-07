import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../../brand';
import {money} from './util';

// =====================================================================
// HallEquityLadder（Hall 事件の収奪の段）
//   入力: Hall 宅 $1 移転 → 約 $308,000 転売 → 債務 約 $22,600（CLM-0021）
//   ★裏取りゲート: CLM-0021 が grade-A 化されるまで金額グリフを焼込まない。
//     `showAmounts=false`（既定）= 匿名象徴の段のみ。`verify_onscreen_text` のグリフ照合対象。
//   モーション: 段が下→上へ順に展開。登攀マーカーが段を昇る（持続キャリア）。
//     showAmounts 時のみ各段の数値がロール（cubic-out）。
//   深度レイヤー: 暗背景 / 段レール / 登攀マーカー+グロー / 段ラベル
// =====================================================================

const {ink, navy, electric, silver, gold, white} = BRAND.color;

type Rung = {label: string; amount: number; sub: string};

const RUNGS: Rung[] = [
  {label: 'Home signed over', amount: 1, sub: 'transfer'},
  {label: 'Resold by the taker', amount: 308_000, sub: 'resale'},
  {label: 'Debt actually owed', amount: 22_600, sub: 'debt'},
];

export const HallEquityLadder: React.FC<{dur: number; showAmounts?: boolean}> = ({dur, showAmounts = false}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const n = RUNGS.length;
  const stepH = 150;
  const baseY = 820;

  // 登攀マーカー進行（持続・cubic-out で段を昇る）
  const climb = interpolate(frame, [16, dur - 20], [0, n - 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const climbEased = climb; // 段間は spring で個別演出するため線形位置＋発光で表現

  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 45%, ${navy} 0%, ${ink} 86%)`, overflow: 'hidden'}}>
      {/* 大気グロー */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(50% 60% at 50% 60%, ${electric}18 0%, transparent 70%)`,
          mixBlendMode: 'screen',
          transform: `translateY(${Math.sin(frame / 36) * 8}px)`,
        }}
      />

      <div
        style={{
          position: 'absolute',
          top: 70,
          width: '100%',
          textAlign: 'center',
          fontFamily: BRAND.font.body,
          fontSize: 26,
          letterSpacing: 6,
          textTransform: 'uppercase',
          color: silver,
          opacity: interpolate(frame, [4, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        }}
      >
        Another taking — the Hall case
      </div>

      {/* 段レール（縦） */}
      <div style={{position: 'absolute', left: '50%', top: baseY - (n - 1) * stepH - 40, width: 4, height: (n - 1) * stepH + 40, background: `${silver}33`, transform: 'translateX(-140px)'}} />

      {RUNGS.map((r, i) => {
        const y = baseY - i * stepH;
        const app = spring({frame: frame - i * 16 - 10, fps, config: {damping: 15}});
        const active = climb >= i - 0.25;
        // 数値ロール（showAmounts 時のみ・cubic-out）
        const rollT = interpolate(frame, [i * 16 + 12, i * 16 + 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const rolled = Math.round(r.amount * (1 - Math.pow(1 - rollT, 3)));
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: '50%',
              top: y,
              transform: `translate(-140px, -50%) scale(${app})`,
              display: 'flex',
              alignItems: 'center',
              gap: 22,
            }}
          >
            {/* 段ノード */}
            <div
              style={{
                width: 30,
                height: 30,
                borderRadius: '50%',
                background: active ? gold : navy,
                border: `3px solid ${active ? gold : silver}`,
                boxShadow: active ? `0 0 20px ${gold}` : 'none',
                transition: 'none',
              }}
            />
            <div style={{minWidth: 520}}>
              <div style={{fontFamily: BRAND.font.body, fontSize: 24, letterSpacing: 2, color: silver, textTransform: 'uppercase'}}>{r.label}</div>
              <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: active ? white : silver, textShadow: active ? `0 0 16px ${gold}88` : 'none', lineHeight: 1.1}}>
                {showAmounts ? money(rolled) : '—'}
              </div>
            </div>
          </div>
        );
      })}

      {/* 登攀マーカー（レール上を昇る・持続キャリア） */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: baseY - climbEased * stepH,
          transform: 'translate(-155px, -50%)',
          width: 14,
          height: 14,
          borderRadius: '50%',
          background: electric,
          boxShadow: `0 0 18px ${electric}, 0 0 40px ${electric}88`,
        }}
      />

      {!showAmounts && (
        <div
          style={{
            position: 'absolute',
            bottom: 40,
            width: '100%',
            textAlign: 'center',
            fontFamily: BRAND.font.body,
            fontSize: 20,
            letterSpacing: 2,
            color: `${silver}aa`,
          }}
        >
          Figures withheld pending source verification (CLM-0021)
        </div>
      )}
    </AbsoluteFill>
  );
};
