import type {ComponentProps} from 'react';
import type {GridWarp} from '../GridWarp';

// =====================================================================
// GridWarp — プリセットカタログ（"data-space" 背景ベッド）。
//   GridWarp が受け取る唯一のプロップは `dur?: number`（ライフ尺・フレーム）。
//   dur を省くと Composition の durationInFrames をそのまま使う。
//   ここでは編集意図ごとに尺だけを差し替えた名前付きプリセットを供給する。
//   フレーム値は 60fps 前提（90f≈1.5s / 150f≈2.5s / 450f≈7.5s）。
//   キーは編集意図の kebab-case。値は ComponentProps<typeof GridWarp> を満たす。
// =====================================================================
export const gridWarpPresets = {
  // --- 既定（Composition の尺に追従） ---
  'data-space': {},

  // --- ショート尺（フック/データベッド・素早い一呼吸） ---
  'data-bed-90f': {dur: 90}, // 1.5s フックの一瞬の地
  'cyber-bed-120f': {dur: 120}, // 2.0s タイトル差し込みの下地
  'finance-grid-150f': {dur: 150}, // 2.5s 数字/相場のインサート背景

  // --- シーン尺（1カット〜1ビートの持続ベッド） ---
  'tech-scene-150f': {dur: 150}, // 2.5s 標準シーンベッド
  'data-scene-210f': {dur: 210}, // 3.5s ややゆったりした説明カット
  'grid-hold-300f': {dur: 300}, // 5.0s 長めのホールド（証言/引用の裏）

  // --- ロング尺（章またぎ・ディープダイブの通し背景） ---
  'deep-dive-450f': {dur: 450}, // 7.5s ディープダイブ節の通し地
  'archive-run-600f': {dur: 600}, // 10.0s アーカイブ連続カットの通し地
  'chapter-bed-900f': {dur: 900}, // 15.0s 章まるごとの持続ベッド
  'network-sweep-1200f': {dur: 1200}, // 20.0s 相関/ネットワーク解説の長回し
} satisfies Record<string, ComponentProps<typeof GridWarp>>;
