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
// FocusPull — 実映像/カット間に重ねる映画的ラックフォーカス・トランジション。
//   ピントが一度大きく外れ（中盤でピーク）、再び戻る "focus pulled then
//   regained" の呼吸を作る透明オーバーレイ。中身:
//     1) frosted veil … backdropFilter の blur をイーズド・ベルで増減。
//        ただし backdropFilter は一部パイプラインで描画されないため、
//        同じベルで濃度が動く「半透明ぼかしグラデ幕」を必ず併置し、
//        backdropFilter 無しでも効果が読めるようにする。
//     2) bokeh discs … electric/silver の柔らかいボケ玉が決定論的に漂い、
//        ピーク付近で膨らみ・明滅して沈む。Trail で微モーションブラー。
//   すべての動きはイージング付き（等速線形禁止）。乱数は remotion `random`
//   （seed 固定）で決定論的（Math.random/Date 不使用）。時間は fps 由来。
//   透明背景・不透明バックドロップなし・root pointerEvents:'none'。
//   ブランド色トークンのみ。黄縦スイープ/全面黄ウォッシュ/実在肖像/
//   画面内ロゴ/ただのズームパンは禁止（本ファイルはいずれも生成しない）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

// ブランドHEX → rgba（グラデ幕・グロー用。トークン以外の色は生成しない）
const hexToRgba = (hex: string, a: number): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};

// 中盤でピークするイーズド・ベル（0→1→0）。"ピントを外して戻す" 主エンベロープ。
// 立ち上がりと戻りに別々の cubic イージングを掛けて対称すぎない有機的な曲線に。
const focusBell = (frame: number, dur: number): number => {
  const mid = dur / 2;
  const rise = interpolate(frame, [0, mid], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fall = interpolate(frame, [mid, dur], [1, 0], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return frame <= mid ? rise : fall;
};

export const FocusPull: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 主エンベロープ（中盤ピーク）。すべての強度はここから派生。
  const bell = focusBell(frame, total);

  // 先頭のポップを避ける柔らかな立ち上げ（spring＝イーズド）。
  const appear = spring({
    frame,
    fps,
    config: {damping: 200, mass: 1, stiffness: 90},
    durationInFrames: sec(fps, 0.5),
  });
  const gate = bell * appear;

  // frosted veil のぼかし量（px）。ピークで最も強くピントが外れる。
  const blurPx = interpolate(bell, [0, 1], [0, 26]);
  // グラデ幕の濃度（backdropFilter が無くても効果が読める保険）。
  const veilAlpha = interpolate(gate, [0, 1], [0, 0.34]);
  // グラデ幕自身にも軽い CSS blur を掛け、縁を溶かす（ハード境界を作らない）。
  const veilSoft = interpolate(bell, [0, 1], [6, 22]);

  // ずっと微かに揺れる中心（静止フレームを作らない・sin は本質的にイーズド）。
  const t = frame / fps;
  const cx = 50 + Math.sin(t * 0.6) * 3; // %
  const cy = 48 + Math.cos(t * 0.5) * 3; // %

  // グラデ幕: 中心はやや透明・周辺へ navy/electric が滲む半透明ぼかし膜。
  const veilBg =
    `radial-gradient(130% 120% at ${cx}% ${cy}%, ` +
    `${hexToRgba(BRAND.color.electric, veilAlpha * 0.5)} 0%, ` +
    `${hexToRgba(BRAND.color.navy, veilAlpha)} 55%, ` +
    `${hexToRgba(BRAND.color.ink, veilAlpha * 0.85)} 100%)`;

  const DISC_COUNT = 16;

  return (
    <AbsoluteFill style={{pointerEvents: 'none', background: 'transparent'}}>
      {/* (1a) frosted veil — 実映像を実際にぼかす（対応パイプラインのみ）。 */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          backdropFilter: `blur(${blurPx}px)`,
          WebkitBackdropFilter: `blur(${blurPx}px)`,
          opacity: appear,
        }}
      />

      {/* (1b) グラデぼかし幕 — backdropFilter 非対応でも "ピントが溶ける" 保険。 */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: veilBg,
          filter: `blur(${veilSoft}px)`,
          opacity: gate,
        }}
      />

      {/* (2) bokeh discs — 決定論的に漂い、ピークで膨らみ明滅して沈むボケ玉。 */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          mixBlendMode: 'screen',
          background: 'transparent',
          opacity: appear,
        }}
      >
        <Trail layers={3} lagInFrames={1.6} trailOpacity={0.5}>
          {Array.from({length: DISC_COUNT}).map((_, i) => {
            // 決定論的パラメータ（seed 固定・Math.random/Date 不使用）
            const r0 = random('fp-x' + i); // 横位置 0..1
            const r1 = random('fp-y' + i); // 縦位置 0..1
            const r2 = random('fp-size' + i); // 基準サイズ
            const r3 = random('fp-drift' + i); // ドリフト量
            const r4 = random('fp-phase' + i); // ドリフト位相
            const r5 = random('fp-tw' + i); // 明滅位相
            const r6 = random('fp-col' + i); // 色選択
            const r7 = random('fp-spd' + i); // ドリフト速度

            // electric と silver を決定論的に振り分け（トークン色のみ）。
            const col = r6 < 0.62 ? BRAND.color.electric : BRAND.color.silver;

            const base = 120 + r2 * 260; // 120..380px の大きなボケ玉
            const driftAmp = 30 + r3 * 90; // ドリフト振幅
            const phase = r4 * Math.PI * 2;
            const twPh = r5 * Math.PI * 2;
            const spd = 0.35 + r7 * 0.5;

            // 位置ドリフト（正弦＝イーズド）。x/y で別位相・別軸に流す。
            const x = r0 * width + Math.sin(t * spd + phase) * driftAmp;
            const y =
              r1 * height + Math.cos(t * spd * 0.8 + phase * 1.3) * driftAmp;

            // ボケ玉個別の遅延ベル（隣どうしスタッガー）。ピーク前後で膨張。
            // 位相をずらした sin をベルに乗せ、膨らみ/明滅を有機的にする。
            const swell = 0.65 + 0.55 * Math.sin(t * 1.4 + twPh); // 0.1..1.2
            const scale = interpolate(bell, [0, 1], [0.4, 1]) * swell;

            // opacity は scale と必ず併走（opacity 単独演出の禁止に準拠）。
            const op = gate * (0.28 + 0.34 * (0.5 + 0.5 * Math.sin(t * 1.1 + twPh)));

            // ボケ玉自体のソフトぼかし（ピークでより溶ける）。
            const discBlur = interpolate(bell, [0, 1], [10, 26]) + (i % 3) * 3;

            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: x,
                  top: y,
                  width: base,
                  height: base,
                  marginLeft: -base / 2,
                  marginTop: -base / 2,
                  borderRadius: '50%',
                  background: `radial-gradient(circle, ${hexToRgba(
                    col,
                    0.9,
                  )} 0%, ${hexToRgba(col, 0.35)} 45%, transparent 70%)`,
                  opacity: Math.max(0, op),
                  transform: `scale(${Math.max(0, scale)})`,
                  filter: `blur(${discBlur}px)`,
                }}
              />
            );
          })}
        </Trail>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
