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
import {BRAND} from '../../brand';

// =====================================================================
// QuoteCard — 逐語引用のシネマティックSCENE（MOTIONKIT）
//   大きなセリフ体の引用が「語群ごと」にマスク切り上がりで出現（イージング）。
//   ゴールドの引用符グリフが裏でスケールイン。帰属（attribution）は下段で
//   マスク切り上がり＋ゴールドのアンダーラインが scaleX spring で描かれる。
//   フルスクリーンのダーク背景・抑制的で映画的。opacity単独リビール無し。
//   全モーションにイージング/spring・常時わずかに動く（紙芝居回避）・決定論的。
// =====================================================================

// セリフ体（Figures.tsx の house style を踏襲・引用に最適）
const SERIF = "'Georgia', 'Times New Roman', 'Times', serif";

// 秒→フレーム（fps基準・フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

export const QuoteCard: React.FC<{
  quote: string;
  attribution: string;
  dur?: number;
}> = ({quote, attribution, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 語ごとに（インラインフローを保ったまま）スタッガーでマスク切り上がり
  const words = quote.trim().split(/\s+/).filter(Boolean);

  // タイムライン（すべて fps 由来の定数）
  const glyphStart = sec(fps, 0.12); // 引用符グリフのスケールイン開始
  const quoteStart = sec(fps, 0.34); // 引用テキスト開始
  const wordStagger = Math.max(1, sec(fps, 0.05)); // 語ごとのディレイ
  const attrStart = quoteStart + words.length * wordStagger + sec(fps, 0.3);
  const outStart = total - sec(fps, 0.5); // シーン退出開始

  // シーン全体の出入り（opacity単独禁止 → 微translateYと必ず併用）
  const sceneO = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const sceneY = interpolate(
    frame,
    [0, sec(fps, 0.4), outStart, total],
    [22, 0, 0, 18],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // 常時わずかな呼吸ドリフト（静止させない）
  const breath = Math.sin((frame / fps) * 1.15) * 3;

  // 引用符グリフ：spring でスケールイン＋ごくわずかに沈む（scale＋translateで
  // opacity単独を回避）。裏レイヤーのヒーロー要素。
  const glyphS = spring({
    frame: frame - glyphStart,
    fps,
    config: {damping: 12, mass: 1.1, stiffness: 120},
  });
  const glyphScale = interpolate(glyphS, [0, 1], [0.5, 1]);
  const glyphY = interpolate(glyphS, [0, 1], [40, 0]);
  const glyphO = interpolate(glyphS, [0, 0.4], [0, 0.9], {extrapolateRight: 'clamp'});
  const glyphDrift = Math.sin((frame / fps) * 0.85) * 6;

  // アンダーライン描画（scaleX spring・左origin）
  const underlineS = spring({
    frame: frame - attrStart - sec(fps, 0.12),
    fps,
    config: {damping: 22, mass: 1, stiffness: 90},
  });
  const underlineX = interpolate(underlineS, [0, 1], [0, 1]);

  // 帰属テキストのマスク切り上がり
  const attrS = spring({
    frame: frame - attrStart,
    fps,
    config: {damping: 18, mass: 0.9, stiffness: 120},
  });
  const attrY = interpolate(attrS, [0, 1], [110, 0]);
  const attrO = interpolate(attrS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // 決定論的なダスト（背景の浮遊粒子・常時ドリフト）
  const DUST = 16;

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* Layer 1: フルスクリーン背景グラデ（指定の SCENE backdrop） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 抑えたグリッド＋ビネット（奥行き） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 96px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 96px)`,
          transform: `translateY(${breath * 1.4}px)`,
          maskImage: 'radial-gradient(120% 85% at 50% 46%, black 24%, transparent 78%)',
          WebkitMaskImage:
            'radial-gradient(120% 85% at 50% 46%, black 24%, transparent 78%)',
        }}
      />

      {/* Layer 3: 決定論的な浮遊ダスト（常時ドリフト・静止しない） */}
      <AbsoluteFill style={{opacity: 0.5}}>
        {new Array(DUST).fill(0).map((_, i) => {
          const bx = random('dust-x' + i) * width;
          const by = random('dust-y' + i) * height;
          const size = 1.5 + random('dust-s' + i) * 3.2;
          const speed = 0.25 + random('dust-v' + i) * 0.5;
          const phase = random('dust-p' + i) * Math.PI * 2;
          const dx = Math.sin((frame / fps) * speed + phase) * 22;
          const dy = Math.cos((frame / fps) * speed * 0.8 + phase) * 16;
          const tw = 0.25 + (Math.sin((frame / fps) * 1.3 + phase) * 0.5 + 0.5) * 0.6;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: bx,
                top: by,
                width: size,
                height: size,
                borderRadius: '50%',
                backgroundColor: BRAND.color.silver,
                opacity: tw,
                transform: `translate(${dx}px, ${dy}px)`,
                boxShadow: `0 0 ${size * 3}px ${BRAND.color.electric}66`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* Layer 4: 引用符グリフ（引用の上に発光ヒーローとしてスケールイン） */}
      <AbsoluteFill
        style={{
          justifyContent: 'flex-start',
          alignItems: 'center',
          paddingTop: 96,
        }}
      >
        <div
          style={{
            fontFamily: SERIF,
            fontWeight: 700,
            fontSize: 300,
            lineHeight: 1,
            color: BRAND.color.gold,
            opacity: glyphO * 0.26,
            transform: `translateY(${glyphY + glyphDrift}px) scale(${glyphScale})`,
            transformOrigin: 'center top',
            textShadow: `0 0 80px ${BRAND.color.gold}55`,
            userSelect: 'none',
          }}
        >
          {'“'}
        </div>
      </AbsoluteFill>

      {/* Layer 5: 引用テキスト＋帰属（前面） */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 220px',
          opacity: sceneO,
          transform: `translateY(${sceneY + breath}px)`,
        }}
      >
        <div style={{maxWidth: 1360, width: '100%', textAlign: 'center'}}>
          {/* 引用本文：語ごとにマスク切り上がり（overflow:hidden + 内側translateY）。
              各語は通常のインラインフローに置かれ、行を折り返して中央寄せで多段になる。 */}
          <div
            style={{
              fontFamily: SERIF,
              fontWeight: 500,
              fontSize: 78,
              lineHeight: 1.32,
              letterSpacing: 0.2,
              color: BRAND.color.white,
              textAlign: 'center',
            }}
          >
            {words.map((w, i) => {
              const ws = spring({
                frame: frame - quoteStart - i * wordStagger,
                fps,
                config: {damping: 17, mass: 0.9, stiffness: 130},
              });
              const wy = interpolate(ws, [0, 1], [118, 0]);
              const wo = interpolate(ws, [0, 0.26], [0, 1], {extrapolateRight: 'clamp'});
              return (
                <span
                  key={i}
                  style={{
                    display: 'inline-block',
                    overflow: 'hidden',
                    verticalAlign: 'top',
                    paddingBottom: '0.16em',
                    marginRight: '0.28em',
                  }}
                >
                  <span
                    style={{
                      display: 'inline-block',
                      transform: `translateY(${wy}%)`,
                      opacity: wo,
                      whiteSpace: 'pre',
                    }}
                  >
                    {w}
                  </span>
                </span>
              );
            })}
          </div>

          {/* 帰属：マスク切り上がり＋描かれるゴールドのアンダーライン */}
          <div style={{marginTop: 54, display: 'inline-block', textAlign: 'left'}}>
            <div style={{overflow: 'hidden', paddingBottom: '0.12em'}}>
              <div
                style={{
                  transform: `translateY(${attrY}%)`,
                  opacity: attrO,
                  fontFamily: BRAND.font.body,
                  fontWeight: 600,
                  fontSize: 32,
                  letterSpacing: 4,
                  textTransform: 'uppercase',
                  color: BRAND.color.silver,
                  // 2026-08-25 EP75/EP76: nowrap は 70 文字超の帰属を右端で切り落として出荷した
                  // （"…ASKED WHETHER HE R" / "…MOST SIGNIFICANT IMMEDIA"）。折り返して全文を出す。
                  whiteSpace: 'normal',
                  maxWidth: 1360,
                  lineHeight: 1.35,
                }}
              >
                {'— '}
                {attribution}
              </div>
            </div>
            {/* アンダーライン：scaleX spring（左origin）で描画 */}
            <div
              style={{
                marginTop: 16,
                height: 3,
                borderRadius: 2,
                backgroundColor: BRAND.color.gold,
                transform: `scaleX(${underlineX})`,
                transformOrigin: 'left center',
                boxShadow: `0 0 18px ${BRAND.color.gold}aa`,
              }}
            />
          </div>
        </div>
      </AbsoluteFill>

      {/* Layer 6: シネマティックなビネット（最前面の抑え） */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 52%, rgba(0,0,0,0.55) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
