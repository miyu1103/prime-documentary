import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../../brand';
import {Grain} from '../Grain';
import {KineticCaptions, LightRays, DustMotes, VignetteBreath} from '../motionkit';

// =====================================================================
// EP36 williams — WilliamsScene (reusable hero-still SCENE block for assembly)
//   1枚のヒーロー静止画を「動くカット」に変える組み立て部品。
//   src が無ければプレースホルダー（cinematicグラデ＋"PLACEHOLDER"隅ラベル）で描画し、
//   Codex画像が届いたら src を差し替えるだけ（＝画像待ち後は drop-in）。
//   構成: ①画像/プレースホルダーに押し込み(scale 1.0→1.08 easing)＋微パララックス
//         ②cyanライトレイ＋ダスト＋ヴィネット呼吸＋フィルムグレイン（アトモス）
//         ③下スクリム（字幕可読性）④KineticCaptions(maskslide) で on-screen
//   規則: 全モーションにイージング・opacity単独なし・肖像は素材側で担保（本部品は載せるだけ）。
// =====================================================================

export type Treatment = 'push' | 'parallax' | 'pixel';

export const WilliamsScene: React.FC<{
  src?: string; // staticFile 相対パス（例 'img/PD-2026-036-S002.png'）。無ければプレースホルダー
  onScreen?: string[]; // grade-A のみ（アセンブリ側で担保）
  treatment?: Treatment;
  accent?: string; // ライトレイ色（既定=cyan electric）。人間ビートは warm gold も可
  placeholderLabel?: string; // 隅の "S0NN PLACEHOLDER"
  dur?: number;
}> = ({src, onScreen, treatment = 'push', accent = BRAND.color.electric, placeholderLabel, dur}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // --- CONTINUOUS full-duration Ken-Burns drift（尺いっぱい動き続ける＝リビール後に静止しない） ---
  //   inOut(sin) は速度が“ビート中盤”で最大 = リビールが落ち着いた区間をちょうど埋める。
  //   → animation_density の BODY near-still（リビール後の据わり）を解消する主役ドリフト。
  const drift = interpolate(frame, [0, total], [0, 1], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  //   inOut(sin) が両端で速度0になる欠点を、位相ずらしの低周波サインで常時補う
  //   （path が単調ランプにならず有機的・端でも velocity が 0 のまま止まらない）。
  const wanderX = Math.sin((frame / total) * Math.PI * 1.5 + 0.6);
  const wanderY = Math.cos((frame / total) * Math.PI * 1.3 + 0.3);

  // --- premium イントロ・リビール（従来どおり前寄せの push/pull-in・見た目は据え置き） ---
  const reveal = interpolate(frame, [0, total], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});

  // scale = イントロ押し込み + 連続ブレス（リビール据わり後もドリフトし続ける）
  const revealScale =
    treatment === 'pixel'
      ? interpolate(reveal, [0, 1], [1.14, 1.02]) // pixel: シャープ→着地の pull-in
      : interpolate(reveal, [0, 1], [1.03, 1.09]); // push/parallax: push-in
  const driftScale = interpolate(drift, [0, 1], [0, 0.06]); // +6%（尺いっぱいの連続ブレス）
  const scale = revealScale + driftScale;

  // position: 全treatmentに“持続する”スローパン + parallax だけ追加スイング
  const parX = treatment === 'parallax' ? interpolate(drift, [0, 1], [-16, 16]) : 0;
  const parY = treatment === 'parallax' ? interpolate(drift, [0, 1], [8, -8]) : 0;
  const px = interpolate(drift, [0, 1], [-20, 20]) + parX + wanderX * 7;
  const py = interpolate(drift, [0, 1], [14, -14]) + parY + wanderY * 6;

  // フェード（頭0.25s / 尻0.35s 相当・opacity単独ではなくscaleと併用済み）
  const fadeIn = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [total - 10, total], [1, 0], {extrapolateLeft: 'clamp'});
  const o = Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, opacity: o}}>
      {/* ①ヒーロー画像 or プレースホルダー */}
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <div style={{position: 'absolute', inset: 0, transform: `translate(${px}px, ${py}px) scale(${scale})`, transformOrigin: '50% 50%'}}>
          {src ? (
            <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          ) : (
            // cinematic プレースホルダー（暗いスレート×cyan中心グロー＋微グリッド）
            <AbsoluteFill
              style={{
                background: `radial-gradient(120% 100% at 50% 42%, #12202f 0%, ${BRAND.color.ink} 60%, #05070d 100%)`,
              }}
            >
              <AbsoluteFill
                style={{
                  opacity: 0.14,
                  backgroundImage: `repeating-linear-gradient(0deg, ${accent}22 0 1px, transparent 1px 70px), repeating-linear-gradient(90deg, ${accent}22 0 1px, transparent 1px 70px)`,
                }}
              />
              <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
                <div style={{width: 900, height: 500, background: `radial-gradient(closest-side, ${accent}22, transparent 72%)`, filter: 'blur(30px)'}} />
              </AbsoluteFill>
            </AbsoluteFill>
          )}
        </div>
      </AbsoluteFill>

      {/* ②アトモス（画像の上・OVERLAY） */}
      <LightRays color={accent} />
      <DustMotes count={26} />
      <VignetteBreath />

      {/* ③下スクリム（字幕可読性） */}
      <AbsoluteFill style={{background: `linear-gradient(to top, ${BRAND.color.ink}dd 0%, ${BRAND.color.ink}00 34%)`}} />

      {/* ④on-screen（maskslide）— UPPER THIRD 配置: ボトムの焼き込みナレーション字幕と衝突させない */}
      {onScreen && onScreen.length ? (
        <KineticCaptions lines={onScreen} style="maskslide" dur={total} anchor="top" />
      ) : null}

      {/* プレースホルダー隅ラベル（最終画像では src 指定で消える） */}
      {!src ? (
        <div
          style={{
            position: 'absolute',
            top: 28,
            left: 32,
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: 20,
            letterSpacing: 2,
            color: `${BRAND.color.silver}88`,
            border: `1px solid ${BRAND.color.silver}44`,
            borderRadius: 4,
            padding: '4px 10px',
          }}
        >
          {placeholderLabel ?? 'HERO PLACEHOLDER'} · swap src on delivery
        </div>
      ) : null}

      <Grain opacity={0.06} />
    </AbsoluteFill>
  );
};
