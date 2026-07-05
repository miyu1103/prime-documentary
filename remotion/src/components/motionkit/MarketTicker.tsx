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
// MarketTicker — broadcast-grade finance ticker strip (bottom-safe OVERLAY).
//   ・ルート透過＋pointerEvents:none（帯以外は一切描かない）。
//   ・各銘柄 = symbol ＋ 符号付き change% ＋ 上/下トライアングル。
//     上げ=抑えたグリーン #3FB170 / 下げ=くすんだレッド #C0473E（BRAND外の許可2色）。
//   ・入場: 銘柄ごとに spring ポップ（translateY＋scale＋opacityの複合／opacity単独禁止）。
//   ・スクロール: 等速線形(frame*speed)を使わず、Easing.inOut(Easing.sin) の
//     イーズド・ランプ位置を W で剰余ラップ＋ゆるいイーズド・スウェイ。
//   ・帯のグロー(電光ブルー)とトップ罫線がイーズド・サインで脈動＝完全静止しない。
//   ・左の "MARKETS" タブはマスク切れ上がりで見出しを出す。
//   ・動く行は @remotion/motion-blur の Trail で微モーションブラー。
//   ・全乱数は remotion random('seed'+i) で決定論（Math.random/Date不使用）。
// 色は BRAND トークン＋許可2リテラルのみ。フォントは BRAND.font.{display,body}。
// =====================================================================

const UP = '#3FB170'; // 上げ（許可リテラル）
const DOWN = '#C0473E'; // 下げ（許可リテラル）

const PANEL_H = 88;
const TAB_W = 262;
const ITEM_W = 340;
const BOTTOM = 46; // bottom-safe オフセット

// 上下トライアングル（CSSボーダー三角）
const Tri: React.FC<{up: boolean; color: string}> = ({up, color}) => (
  <span
    style={{
      display: 'inline-block',
      width: 0,
      height: 0,
      borderLeft: '7px solid transparent',
      borderRight: '7px solid transparent',
      ...(up
        ? {borderBottom: `11px solid ${color}`}
        : {borderTop: `11px solid ${color}`}),
    }}
  />
);

export const MarketTicker: React.FC<{
  items: {symbol: string; change: number}[];
  dur?: number;
}> = ({items, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const sec = (s: number) => Math.round(fps * s);
  const n = items.length;
  if (n === 0) return null;

  // --- スクロール: イーズド・ランプ（線形速度でない）を W で剰余ラップ ---------
  const W = n * ITEM_W;
  const loops = Math.max(2, Math.round(total / sec(4))); // クリップ長でペース調整
  const ramp = interpolate(frame, [0, total], [0, W * loops], {
    easing: Easing.inOut(Easing.sin),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sway = interpolate(Math.sin((frame / fps) * 0.7), [-1, 1], [-8, 8]); // ゆるい横スウェイ
  const scrollX = -(ramp % W) + sway;

  // 画面幅＋1周ぶんを埋めるコピー数（シームレスなラップ）
  const copies = Math.ceil(1920 / W) + 2;
  const rowW = copies * n * ITEM_W;

  // --- 帯のグロー脈動＆罫線グロー（イーズド・サイン） -------------------------
  const glowPulse = interpolate(Math.sin((frame / fps) * 1.3), [-1, 1], [0.28, 0.72]);
  const lineGlow = interpolate(Math.sin((frame / fps) * 1.3), [-1, 1], [9, 26]);

  // --- 左タブ "MARKETS" マスク切れ上がり ------------------------------------
  const tabSpring = spring({
    frame: frame - sec(0.15),
    fps,
    config: {damping: 16, mass: 0.8},
  });
  const tabY = interpolate(tabSpring, [0, 1], [110, 0]); // %（overflow:hidden内）

  const stagger = Math.max(1, sec(0.05));

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: BOTTOM, height: PANEL_H}}>
        {/* 背後グロー（脈動） */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: -8,
            height: PANEL_H + 16,
            background: BRAND.color.electric,
            filter: 'blur(34px)',
            opacity: glowPulse * 0.5,
            borderRadius: 22,
          }}
        />

        {/* 帯パネル（半透明ネイビー→インク・overflowで銘柄をクリップ） */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            overflow: 'hidden',
            background: `linear-gradient(180deg, ${BRAND.color.navy}ee 0%, ${BRAND.color.ink}f2 100%)`,
            boxShadow: `0 18px 48px rgba(0,0,0,0.45)`,
          }}
        >
          {/* トップ罫線（電光ブルー・グロー脈動） */}
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              top: 0,
              height: 2,
              background: BRAND.color.electric,
              boxShadow: `0 0 ${lineGlow}px ${BRAND.color.electric}`,
            }}
          />

          {/* スクロール行（Trailで微モーションブラー） */}
          <Trail layers={4} lagInFrames={1.1} trailOpacity={0.5}>
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                height: '100%',
                display: 'flex',
                width: rowW,
                transform: `translateX(${scrollX}px)`,
                willChange: 'transform',
              }}
            >
              {Array.from({length: copies * n}).map((_, j) => {
                const i = j % n;
                const {symbol, change} = items[i];
                const positive = change >= 0;
                const col = positive ? UP : DOWN;
                const label = `${positive ? '+' : ''}${change.toFixed(2)}%`;

                // 入場: symbol単位のスタッガー spring（決定論ジッター）
                const jitter = Math.floor(random('mt-d' + i) * sec(0.08));
                const inSpring = spring({
                  frame: frame - (i * stagger + jitter),
                  fps,
                  config: {damping: 14, mass: 0.6, stiffness: 140},
                });
                // 恒常マイクロボブ（静止しない・イーズド）
                const bob =
                  Math.sin((frame / fps) * 2.2 + random('mt-b' + i) * Math.PI * 2) * 1.6;
                const ty = interpolate(inSpring, [0, 1], [26, 0]) + bob;
                const sc = interpolate(inSpring, [0, 1], [0.72, 1]);
                const op = interpolate(inSpring, [0, 0.4], [0, 1], {
                  extrapolateRight: 'clamp',
                });

                return (
                  <div
                    key={j}
                    style={{
                      position: 'relative',
                      width: ITEM_W,
                      height: '100%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: 14,
                      transform: `translateY(${ty}px) scale(${sc})`,
                      opacity: op,
                    }}
                  >
                    <span
                      style={{
                        fontFamily: BRAND.font.display,
                        fontSize: 30,
                        letterSpacing: 0.5,
                        color: BRAND.color.white,
                      }}
                    >
                      {symbol.toUpperCase()}
                    </span>
                    <span
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 8,
                        color: col,
                      }}
                    >
                      <Tri up={positive} color={col} />
                      <span
                        style={{
                          fontFamily: BRAND.font.body,
                          fontWeight: 700,
                          fontSize: 26,
                          fontVariantNumeric: 'tabular-nums',
                        }}
                      >
                        {label}
                      </span>
                    </span>
                    {/* 銘柄区切りのヘアライン */}
                    <div
                      style={{
                        position: 'absolute',
                        right: 0,
                        top: '26%',
                        height: '48%',
                        width: 1,
                        background: `${BRAND.color.silver}33`,
                      }}
                    />
                  </div>
                );
              })}
            </div>
          </Trail>

          {/* 左タブ "MARKETS"（銘柄が背後から現れる・マスク切れ上がり見出し） */}
          <div
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              bottom: 0,
              width: TAB_W,
              zIndex: 2,
              display: 'flex',
              alignItems: 'center',
              paddingLeft: 34,
              background: `linear-gradient(90deg, ${BRAND.color.electric} 0%, ${BRAND.color.navy} 100%)`,
            }}
          >
            <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
              <span
                style={{
                  display: 'inline-block',
                  transform: `translateY(${tabY}%)`,
                  fontFamily: BRAND.font.display,
                  fontSize: 30,
                  letterSpacing: 3,
                  color: BRAND.color.white,
                  whiteSpace: 'pre',
                }}
              >
                MARKETS
              </span>
            </div>
            {/* タブ右端のゴールドアクセント（グロー脈動） */}
            <div
              style={{
                position: 'absolute',
                right: 0,
                top: 0,
                bottom: 0,
                width: 3,
                background: BRAND.color.gold,
                boxShadow: `0 0 ${lineGlow}px ${BRAND.color.gold}`,
              }}
            />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
