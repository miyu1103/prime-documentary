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
// Atmospherics — 実映像/カットの上に重ねる「空気感」オーバーレイ4種。
//   すべて透明・screen/overlay 合成・pointerEvents:'none'・不透明背景なし。
//   すべての動きはイージング付き（等速線形禁止）。乱数は remotion `random`
//   （seed 固定）で決定論的。時間は fps から算出。静止フレームを作らない。
//   ブランド色トークンのみ使用。黄縦スイープ/全面黄ウォッシュ/実在肖像/
//   画面内ロゴは禁止（本ファイルはいずれも生成しない）。
//
//   DustMotes      … 上昇する塵。決定論的な位置/速度、横ゆれ、scale 明滅。
//   SoftGlow       … 大きな柔らかい放射グローが緩やかに周回（ハード線でない）。
//   FilmGrain      … 毎フレーム feTurbulence のフィルムグレイン（overlay）。
//   VignetteBreath … 周辺減光ビネットが息づく（イーズド正弦）。
// =====================================================================

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// ブランドHEX → rgba（ビネットのエッジ用。トークン以外の色は生成しない）
const hexToRgba = (hex: string, a: number): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};

// 各レイヤ共通の出入りエンベロープ（先頭で立ち上げ・終端で畳む、必ずイーズド）。
// 任意の dur で interpolate の入力が単調増加になるようフェード幅を dur から算出。
const envelope = (frame: number, dur: number, fps: number): number => {
  const inN = Math.min(sec(fps, 0.35), Math.max(1, Math.floor(dur / 3)));
  const outN = Math.min(sec(fps, 0.4), Math.max(1, Math.floor(dur / 3)));
  const p1 = inN;
  const p2 = Math.max(p1 + 1, dur - outN);
  return interpolate(frame, [0, p1, p2, dur], [0, 1, 1, 0], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// ---------------------------------------------------------------------
// DustMotes — 漂って上昇する塵。位置/速度/明滅は remotion random で決定論化。
//   縦ドリフトは正弦ワープで速度が変化する（＝イーズド、等速でない）。
//   横ゆれは正弦（本質的にイーズド）。明滅は opacity 単独でなく scale で行う。
//   Trail で微かなモーションブラーを付与。screen 合成・透明。
// ---------------------------------------------------------------------
export const DustMotes: React.FC<{
  count?: number;
  color?: string;
  dur?: number;
}> = ({count = 40, color = BRAND.color.silver, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // レイヤ全体の柔らかな立ち上げ（先頭のポップ防止）
  const appear = spring({frame, fps, config: {damping: 22, mass: 1, stiffness: 80}});
  const env = envelope(frame, total, fps);

  const t = frame / fps; // 秒

  return (
    <AbsoluteFill
      style={{
        mixBlendMode: 'screen',
        pointerEvents: 'none',
        background: 'transparent',
        opacity: appear * env,
      }}
    >
      <Trail layers={3} lagInFrames={1.4} trailOpacity={0.55}>
        {Array.from({length: count}).map((_, i) => {
          // 決定論的パラメータ（seed 固定・Math.random/Date 不使用）
          const r0 = random('mote-x' + i); // 0..1 横位置
          const r1 = random('mote-spd' + i); // 速度
          const r2 = random('mote-size' + i); // サイズ
          const r3 = random('mote-sway' + i); // 横ゆれ量
          const r4 = random('mote-ph' + i); // 位相
          const r5 = random('mote-tw' + i); // 明滅位相
          const r6 = random('mote-start' + i); // 縦の初期位相

          const size = 2 + r2 * 6; // 2..8px
          const speed = 0.45 + r1 * 0.8; // サイクル速度
          const swayAmp = 16 + r3 * 46; // 横ゆれ振幅
          const swayPh = r4 * Math.PI * 2;
          const twPh = r5 * Math.PI * 2;

          // 縦ドリフト：連続的に循環する位相を正弦でワープ → 速度が変化（イーズド）。
          // 位相 0 と 1 で sin=0 のため循環境界で不連続なし（ポップしない）。
          const cyc = t * speed * 0.11 + r6;
          const ph = cyc - Math.floor(cyc); // 0..1 連続ランプ
          const warped = ph + 0.13 * Math.sin(ph * Math.PI * 2); // 速度可変・周期連続
          const y = (1 - warped) * (height + 160) - 80; // 下→上へ上昇

          // 横ゆれ（正弦＝イーズド）
          const x = r0 * width + Math.sin(t * 0.9 + swayPh) * swayAmp;

          // 明滅は scale で（opacity 単独禁止）。opacity は控えめな下限を保つ。
          const tw = 0.5 + 0.5 * Math.sin(t * 1.8 + twPh);
          const scale = 0.7 + tw * 0.7; // 0.7..1.4
          const op = 0.35 + tw * 0.4; // 0.35..0.75（scale と併走）

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: size,
                height: size,
                marginLeft: -size / 2,
                marginTop: -size / 2,
                borderRadius: '50%',
                background: color,
                opacity: op,
                transform: `scale(${scale})`,
                filter: `blur(${0.6 + (i % 3) * 0.5}px)`,
                boxShadow: `0 0 ${size * 2.2}px ${color}`,
              }}
            />
          );
        })}
      </Trail>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// SoftGlow — 大きく柔らかい放射グローが2つ、緩やかに周回する。
//   位置は「正弦をイーズドに interpolate した」値（ハードなスイープ線でない）。
//   screen 合成・低不透明度。
// ---------------------------------------------------------------------
export const SoftGlow: React.FC<{color?: string; dur?: number}> = ({
  color = BRAND.color.electric,
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const appear = spring({frame, fps, config: {damping: 26, mass: 1, stiffness: 70}});
  const env = envelope(frame, total, fps);
  const t = frame / fps;

  // 正弦（[-1..1]）を位置レンジへ interpolate。周回はゆっくり・イーズド。
  const g1x = interpolate(Math.sin(t * 0.16), [-1, 1], [width * 0.28, width * 0.62]);
  const g1y = interpolate(Math.cos(t * 0.12), [-1, 1], [height * 0.30, height * 0.72]);
  const g2x = interpolate(Math.sin(t * 0.11 + 2.1), [-1, 1], [width * 0.40, width * 0.78]);
  const g2y = interpolate(Math.cos(t * 0.09 + 1.3), [-1, 1], [height * 0.24, height * 0.66]);

  const s1 = 1200;
  const s2 = 1450;

  const glow = (cx: number, cy: number, size: number, col: string, op: number): React.CSSProperties => ({
    position: 'absolute',
    left: cx - size / 2,
    top: cy - size / 2,
    width: size,
    height: size,
    borderRadius: '50%',
    background: `radial-gradient(circle, ${col} 0%, transparent 68%)`,
    opacity: op,
  });

  return (
    <AbsoluteFill
      style={{
        mixBlendMode: 'screen',
        pointerEvents: 'none',
        background: 'transparent',
        opacity: appear * env,
      }}
    >
      <div style={glow(g1x, g1y, s1, color, 0.14)} />
      <div style={glow(g2x, g2y, s2, BRAND.color.navy, 0.16)} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// FilmGrain — 毎フレーム再シードする feTurbulence のフィルムグレイン。
//   seed = frame % 131（毎フレーム変化＝静止しない）。overlay 合成。
//   opacity は 0.05–0.09 のイーズド正弦で微呼吸。
// ---------------------------------------------------------------------
export const FilmGrain: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const seed = frame % 131;
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const filterId = `grain-${uid}-${seed}`;

  // 0.05–0.09 の範囲で微かに呼吸（正弦＝イーズド）。終端でエンベロープ減衰。
  const breath = 0.07 + 0.02 * Math.sin((frame / fps) * 1.4);
  const op = breath * envelope(frame, total, fps);

  return (
    <AbsoluteFill
      style={{pointerEvents: 'none', mixBlendMode: 'overlay', opacity: op, background: 'transparent'}}
    >
      <svg width="100%" height="100%" style={{display: 'block'}}>
        <filter id={filterId}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#${filterId})`} />
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// VignetteBreath — 中心透明→周辺暗のビネット。強さがイーズド正弦で息づく。
//   中心は完全透明（不透明背景なし）。overlay 合成でエッジを沈める。
// ---------------------------------------------------------------------
export const VignetteBreath: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 正弦（[-1..1]）をエッジ暗部の強さへ interpolate（イーズド）。
  const strength = interpolate(
    Math.sin((frame / fps) * 0.85),
    [-1, 1],
    [0.28, 0.5],
    {easing: Easing.inOut(Easing.sin)},
  );
  const edge = hexToRgba(BRAND.color.ink, strength * envelope(frame, total, fps));

  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        mixBlendMode: 'overlay',
        background: `radial-gradient(120% 100% at 50% 48%, transparent 52%, ${edge} 100%)`,
      }}
    />
  );
};
