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
// EP36 williams — DatasetImbalance (code-built motion-graphic · SCENE)
//   SPN-0011「これらは見せられた顔から学ぶ。長年、一部の顔は少ししか見せられなかった」
//   を中立・尊厳をもって可視化：匿名の頭部シルエットの大集団（多数=cool）と、
//   まばらな少数（gold）。実在顔なし・数値なし・煽りなし（人種差は測定値＋ナレの反証で扱う）。
//   規則: 全モーションにイージング/spring・opacity単独無し（scale併用）・スタッガー・
//   裏≥3レイヤー・マスク切れ上がり文字・秒はfpsから算出・決定論。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const COLS = 20;
const ROWS = 9;
const N = COLS * ROWS;
const MINORITY = 0.16; // まばらな少数の割合（視覚上の偏り）

// 頭部＋肩の簡易シルエット（実在顔ではない）
const Silhouette: React.FC<{size: number; color: string; op: number; scale: number}> = ({size, color, op, scale}) => (
  <div style={{width: size, height: size, opacity: op, transform: `scale(${scale})`}}>
    <svg viewBox="0 0 24 24" width={size} height={size}>
      <circle cx="12" cy="8" r="5" fill={color} />
      <path d="M3 24 C3 16 21 16 21 24 Z" fill={color} />
    </svg>
  </div>
);

export const DatasetImbalance: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const groupO = interpolate(frame, [0, sec(fps, 0.3), total - sec(fps, 0.5), total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = Math.sin(frame * 0.05) * 4;

  const areaW = width * 0.72;
  const areaH = height * 0.5;
  const left = (width - areaW) / 2;
  const top = height * 0.32;
  const cw = areaW / COLS;
  const ch = areaH / ROWS;
  const dot = Math.min(cw, ch) * 0.7;

  // 見出し（マスク切れ上がり）
  const head = spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 18}});
  const headY = interpolate(head, [0, 1], [90, 0]);
  const headO = interpolate(head, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  // 下段ラベル
  const foot = spring({frame: frame - sec(fps, 2.2), fps, config: {damping: 18}});
  const footY = interpolate(foot, [0, 1], [90, 0]);
  const footO = interpolate(foot, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* レイヤー1: グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 100% at 50% 46%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 66%, #05070d 100%)`,
        }}
      />
      {/* レイヤー2: 微グリッド（ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${drift}px)`,
          backgroundImage: `repeating-linear-gradient(0deg, ${BRAND.color.electric}16 0px, ${BRAND.color.electric}16 1px, transparent 1px, transparent 74px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
        }}
      />
      {/* レイヤー3: グロー */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: areaW * 0.9,
            height: areaH * 0.9,
            background: `radial-gradient(closest-side, ${BRAND.color.electric}1e 0%, transparent 72%)`,
            filter: 'blur(30px)',
            opacity: groupO,
          }}
        />
      </AbsoluteFill>

      {/* 見出し */}
      <AbsoluteFill style={{opacity: groupO}}>
        <div style={{position: 'absolute', left, top: height * 0.2, overflow: 'hidden', paddingBottom: '0.12em'}}>
          <div
            style={{
              transform: `translateY(${headY}%)`,
              opacity: headO,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: 34,
              letterSpacing: 3,
              color: BRAND.color.silver,
            }}
          >
            THEY LEARN FROM THE FACES THEY'RE SHOWN
          </div>
        </div>
      </AbsoluteFill>

      {/* シルエット集団（スタッガー・偏り） */}
      <AbsoluteFill style={{opacity: groupO, transform: `translateY(${drift * 0.4}px)`}}>
        {Array.from({length: N}).map((_, i) => {
          const row = Math.floor(i / COLS);
          const col = i % COLS;
          const x = left + col * cw + (cw - dot) / 2;
          const y = top + row * ch + (ch - dot) / 2;
          const isMinority = random(`min-${i}`) < MINORITY;
          const s = spring({
            frame: frame - sec(fps, 0.3) - i * Math.max(1, sec(fps, 0.012)),
            fps,
            config: {damping: 16, mass: 0.7},
          });
          const sc = interpolate(s, [0, 1], [0.4, 1]);
          const o = interpolate(s, [0, 0.5], [0, 1], {extrapolateRight: 'clamp'});
          const color = isMinority ? BRAND.color.gold : `${BRAND.color.silver}66`;
          return (
            <div key={i} style={{position: 'absolute', left: x, top: y}}>
              <Silhouette size={dot} color={color} op={o * (isMinority ? 1 : 0.9)} scale={sc} />
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 下段ラベル */}
      <AbsoluteFill style={{opacity: groupO}}>
        <div style={{position: 'absolute', left, top: top + areaH + 26, overflow: 'hidden', paddingBottom: '0.12em'}}>
          <div
            style={{
              transform: `translateY(${footY}%)`,
              opacity: footO,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 26,
              letterSpacing: 1.5,
              color: BRAND.color.white,
            }}
          >
            …and for years, they were shown{' '}
            <span style={{color: BRAND.color.gold, fontWeight: 900}}>too few of some of us.</span>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
