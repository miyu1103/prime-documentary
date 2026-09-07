import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  OffthreadVideo,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../../brand';
import {Grain} from '../Grain';
import {KineticCaptions} from '../motionkit';

// =====================================================================
// EP36 williams — WilliamsFactoryCut (reusable graded FACTORY-clip block)
//   1本の factory .mp4 を「動くカット」に変える組み立て部品。
//   構成: ①クリップに house duotone/ink グレード（navy乗算＋accentスクリーン＋周辺ビネット）
//         ②ゆっくりした spring イージングの Ken-Burns（scale/parallax ドリフト＝静止禁止）
//         ③下スクリム（字幕可読性）④KineticCaptions(maskslide) で on-screen ⑤フィルムグレイン
//   規則: 全モーションにイージング（linear禁止）・opacity単独なし（scale/translateと併用）。
//   src が無ければ暗いスレートのプレースホルダーで描画（drop-in）。
// =====================================================================

export const WilliamsFactoryCut: React.FC<{
  src?: string; // staticFile 相対パス（例 'williams/factory/AF-*.mp4'）
  onScreen?: string[]; // grade-A のみ（アセンブリ側で担保）
  accent?: string; // グレードのスクリーン色（既定=electric cyan）
  dur?: number;
}> = ({src, onScreen, accent = BRAND.color.electric, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ①ゆっくりした spring-eased Ken-Burns（等速禁止・尺いっぱい旅する＝静止しない）
  //   spring は heavy-overdamped で尺内は上昇し続けるが、後半は速度が落ちる。
  //   → 位相ずらしの低周波サイン・ブレスを常時重ね、後半も速度が 0 に落ちない保険にする。
  const drift = spring({frame, fps, config: {damping: 200, mass: 3, stiffness: 22}});
  const wanderX = Math.sin((frame / total) * Math.PI * 1.5 + 0.4);
  const wanderY = Math.cos((frame / total) * Math.PI * 1.4 + 0.2);
  const scale = interpolate(drift, [0, 1], [1.06, 1.16]) + Math.sin((frame / total) * Math.PI * 2) * 0.008;
  const px = interpolate(drift, [0, 1], [-20, 20]) + wanderX * 8;
  const py = interpolate(drift, [0, 1], [12, -12]) + wanderY * 7;

  // 頭0.27s / 尻0.33s のフェード（scaleドリフトと併用＝opacity単独ではない）
  const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [total - 10, total], [1, 0], {extrapolateLeft: 'clamp'});
  const o = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, opacity: o}}>
      {/* ①クリップ or プレースホルダー */}
      <AbsoluteFill style={{overflow: 'hidden'}}>
        {src ? (
          <OffthreadVideo
            src={staticFile(src)}
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `translate(${px}px, ${py}px) scale(${scale})`,
              filter: 'brightness(1.02) contrast(1.06) saturate(0.72)',
            }}
          />
        ) : (
          <AbsoluteFill
            style={{background: `radial-gradient(120% 100% at 50% 42%, #10202f 0%, ${BRAND.color.ink} 70%)`}}
          />
        )}
      </AbsoluteFill>

      {/* ②house duotone/ink グレード（navy乗算 → accentスクリーン微光 → 周辺ビネット） */}
      <AbsoluteFill style={{pointerEvents: 'none', backgroundColor: BRAND.color.navy, opacity: 0.16, mixBlendMode: 'multiply'}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: `radial-gradient(60% 44% at 50% 46%, ${accent}14 0%, transparent 64%)`, mixBlendMode: 'screen'}} />
      <AbsoluteFill style={{pointerEvents: 'none', background: `radial-gradient(135% 108% at 50% 44%, transparent 58%, ${BRAND.color.ink}66 100%)`}} />

      {/* ③下スクリム（字幕可読性） */}
      <AbsoluteFill style={{background: `linear-gradient(to top, ${BRAND.color.ink}dd 0%, ${BRAND.color.ink}00 34%)`}} />

      {/* ④on-screen（maskslide）— UPPER THIRD 配置: ボトムの焼き込みナレーション字幕と衝突させない */}
      {onScreen && onScreen.length ? (
        <KineticCaptions lines={onScreen} style="maskslide" dur={total} anchor="top" />
      ) : null}

      {/* ⑤フィルムグレイン */}
      <Grain opacity={0.06} />
    </AbsoluteFill>
  );
};
