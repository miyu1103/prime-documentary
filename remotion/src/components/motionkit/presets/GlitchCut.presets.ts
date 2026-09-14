import type {ComponentProps} from 'react';
import type {GlitchCut} from '../GlitchCut';

// =====================================================================
// GlitchCut プリセット・カタログ
//   GlitchCut は `dur?: number`（グリッチ全体の尺＝フレーム数）だけを受ける。
//   env（山は中央 total/2）が dur で駆動されるため、dur が短いほど鋭く速い一撃、
//   長いほど尾を引く緊張のホールドになる。省略時は Composition の
//   durationInFrames にフォールバックする。以下は @60fps 前提の目安。
//   キーは編集上の用途（editorial intent）に対応させたケバブケース。
// =====================================================================

export const glitchCutPresets = {
  // --- Default（尺は Composition の durationInFrames に委ねる） ---
  'default': {},

  // --- Flash / スタッブ系（最速・一瞬の断裂。ハードカットの継ぎ目に重ねる） ---
  'flash-4f': {dur: 4}, // 極短スタッブ。ほぼ1フレームの断絶感
  'flash-6f': {dur: 6}, // 標準フラッシュ。鋭いデジタル・パンチ
  'hard-cut': {dur: 8}, // ハードカットの一拍。継ぎ目を裂く
  'reveal-punch': {dur: 10}, // 情報リビール直前の打撃

  // --- Quick / スナップ系（速いが読める。カット転換の主力） ---
  'quick-12f': {dur: 12}, // 標準クイック・グリッチ
  'snap-16f': {dur: 16}, // 少し伸びたスナップ。転換の存在感
  'memory-glitch': {dur: 18}, // 回想/記憶の乱れ。滲む一瞬

  // --- Beat / ビート系（音の拍に乗る中尺。強調） ---
  'beat-20f': {dur: 20}, // 拍に合わせる標準ビート・グリッチ
  'signal-lost': {dur: 24}, // 信号途絶。ノイズが立ち上がって崩れる
  'evidence-cut': {dur: 28}, // 証拠提示の緊張ある切り替え

  // --- Tension / ホールド系（長尺・尾を引く。溜めと緊張の維持） ---
  'tension-hold-30f': {dur: 30}, // 緊張のホールド。ゆっくり山へ登り畳む
  'dread-build-40f': {dur: 40}, // 不穏の醸成。長い立ち上がり
  'systemic-glitch-48f': {dur: 48}, // 系全体の破綻を思わせる最長ホールド
} satisfies Record<string, ComponentProps<typeof GlitchCut>>;
