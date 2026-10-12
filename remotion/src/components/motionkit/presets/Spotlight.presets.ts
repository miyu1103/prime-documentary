import type {ComponentProps} from 'react';
import type {Spotlight} from '../Spotlight';

// =====================================================================
// Spotlight プリセット集
//   実映像の上に重ねる「一点だけ残す」暗幕オーバーレイの窓位置カタログ。
//   cx, cy, r はすべて 0..1 のフレーム比（r の基準は短辺）。
//     r ≈ 0.16 = 小窓 / 0.28 = 中窓 / 0.42 = 大窓。
//   dim は暗部の不透明度（未指定＝コンポーネント既定 0.72）。
//     subtle ≈ 0.5 / strong ≈ 0.85。
//   dur は基本設定しない（Composition の durationInFrames を使う）。
//   キーは kebab-case、テーマごとに // でグループ化。
// =====================================================================

export const spotlightPresets = {
  // --- center: 画面中央の窓（小・中・大） ---
  'center-small': {cx: 0.5, cy: 0.5, r: 0.16},
  'center-medium': {cx: 0.5, cy: 0.5, r: 0.28},
  'center-large': {cx: 0.5, cy: 0.5, r: 0.42},

  // --- thirds: 三分割点（左右）の中窓 ---
  'left-third': {cx: 0.33, cy: 0.5, r: 0.26},
  'right-third': {cx: 0.67, cy: 0.5, r: 0.26},
  'upper-third': {cx: 0.5, cy: 0.33, r: 0.24},
  'lower-third': {cx: 0.5, cy: 0.67, r: 0.24},

  // --- corners: 四隅（やや内側・小窓） ---
  'top-left-corner': {cx: 0.24, cy: 0.24, r: 0.18},
  'top-right-corner': {cx: 0.76, cy: 0.24, r: 0.18},
  'bottom-left-corner': {cx: 0.24, cy: 0.76, r: 0.18},
  'bottom-right-corner': {cx: 0.76, cy: 0.76, r: 0.18},

  // --- face: 人物の顔まわり（構図別の小〜中窓） ---
  'face-center': {cx: 0.5, cy: 0.4, r: 0.2},
  'face-left': {cx: 0.38, cy: 0.4, r: 0.18},
  'face-right': {cx: 0.62, cy: 0.4, r: 0.18},
  'face-tight': {cx: 0.5, cy: 0.38, r: 0.14},
  'eyes-line': {cx: 0.5, cy: 0.36, r: 0.12},

  // --- document: 書類・証拠のディテール領域 ---
  'document-center': {cx: 0.5, cy: 0.55, r: 0.24},
  'document-signature': {cx: 0.62, cy: 0.72, r: 0.14},
  'document-header': {cx: 0.5, cy: 0.3, r: 0.2},
  'document-detail': {cx: 0.45, cy: 0.58, r: 0.12},

  // --- dim variations: 暗さの調整（subtle / strong） ---
  'center-subtle': {cx: 0.5, cy: 0.5, r: 0.3, dim: 0.5},
  'center-strong': {cx: 0.5, cy: 0.5, r: 0.24, dim: 0.85},
  'face-subtle': {cx: 0.5, cy: 0.4, r: 0.2, dim: 0.5},
  'face-strong': {cx: 0.5, cy: 0.4, r: 0.18, dim: 0.85},
  'document-strong': {cx: 0.5, cy: 0.55, r: 0.22, dim: 0.85},
} satisfies Record<string, ComponentProps<typeof Spotlight>>;
