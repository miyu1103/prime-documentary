import type {ComponentProps} from 'react';
import type {DepthParticles} from '../DepthParticles';

// =====================================================================
// DepthParticles プリセット集
//   props は {count?: number; dur?: number} のみ。
//     count = 粒子総数（4奥行きレイヤへ配分される密度）。既定 90。
//     dur   = エンベロープ全長（フレーム）。未指定なら Composition 尺。
//   ここでは編集意図別に count（疎/標準/密）と dur を差し替えるだけ。
//   count 目安: sparse≈40 / normal≈90 / dense≈160。
// =====================================================================

export const depthParticlesPresets = {
  // --- 密度ベッド（背景常設。dur 省略＝Composition 全尺に追従） -----------
  'sparse-bed': {count: 40},
  'normal-bed': {count: 90},
  'dense-bed': {count: 160},

  // --- 編集意図つき（キー名がそのまま演出の狙い） ------------------------
  'minimal-drift': {count: 28}, // ごく少数・静かな余白ショット向け
  'title-depth': {count: 70}, // タイトル裏の落ち着いた奥行き
  'dense-cosmos': {count: 210}, // 満天の星／宇宙感の最密ベッド
  'atmosphere-fill': {count: 120}, // 標準より一段濃い雰囲気埋め

  // --- 短尺スティング（速い立ち上げ・畳み。60fps 前提の秒換算） ----------
  'quick-sparse': {count: 40, dur: 60}, // 1.0s・疎めのアクセント
  'quick-normal': {count: 90, dur: 90}, // 1.5s・標準密度のブリッジ

  // --- 長回しアンビエント（ゆったり呼吸する背景） ------------------------
  'long-sparse': {count: 48, dur: 300}, // 5.0s・薄いロング背景
  'long-normal': {count: 100, dur: 360}, // 6.0s・標準ロング背景
  'long-dense': {count: 170, dur: 300}, // 5.0s・濃密ロング背景

  // --- インサート尺（章間の短いつなぎ） --------------------------------
  'insert-normal': {count: 85, dur: 150}, // 2.5s
  'insert-dense': {count: 150, dur: 180}, // 3.0s・密度で見せるつなぎ
} satisfies Record<string, ComponentProps<typeof DepthParticles>>;
