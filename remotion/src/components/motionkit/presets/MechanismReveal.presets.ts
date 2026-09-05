import type {ComponentProps} from 'react';
import type {MechanismReveal} from '../MechanismReveal';

// =====================================================================
// MechanismReveal プリセット集
//   フルスクリーンの「概念メカニズム」演出カタログ（PDの転換モーメント用）。
//   props は 2 つだけ:
//     kind : 'closingdoor' | 'gears' | 'faultsplit'（唯一の必須プロップ）
//       - closingdoor = 扉が閉まりボルト錠がカチッと差し込まれる（＝退路が断たれる/合法の抜け道が閉じる）
//       - gears       = 噛み合う歯車が順にスピンアップ（＝仕組み/機構/システムが回り出す）
//       - faultsplit  = 地盤が断層線に沿って割れ破片が散る（＝制度/構造が崩壊・亀裂）
//     dur  : この演出に割く有効フレーム数（省略時は Composition の durationInFrames）。
//            fps=60 前提の目安 —— quick=90(1.5s) / normal=180(3.0s) / slow=300(5.0s) /
//            beat=120(2.0s) / hold=240(4.0s)。フレーム直書きは秒×fps の値。
//   キーは kebab-case、kind ごとに // でグループ化。
//   PD モーメント名（意味づけ）→ kind のマッピングをキー名で明示する。
// =====================================================================

// fps=60 前提の尺定数（フレーム）
const QUICK = 90; // 1.5s
const BEAT = 120; // 2.0s
const NORMAL = 180; // 3.0s
const HOLD = 240; // 4.0s
const SLOW = 300; // 5.0s

export const mechanismRevealPresets = {
  // --- closingdoor: 退路が断たれる / 抜け道が閉じる / 封鎖 ---
  'closing-door': {kind: 'closingdoor', dur: NORMAL},
  'closing-door-quick': {kind: 'closingdoor', dur: QUICK},
  'closing-door-slow': {kind: 'closingdoor', dur: SLOW},
  'the-loophole-closes': {kind: 'closingdoor', dur: NORMAL},
  'no-way-out': {kind: 'closingdoor', dur: BEAT},
  'the-door-locks': {kind: 'closingdoor', dur: HOLD},
  'case-closed': {kind: 'closingdoor', dur: NORMAL},
  'the-trap-shuts': {kind: 'closingdoor', dur: QUICK},

  // --- gears: 仕組み / 機構 / システムが回り出す ---
  'gears': {kind: 'gears', dur: NORMAL},
  'gears-quick': {kind: 'gears', dur: QUICK},
  'gears-slow': {kind: 'gears', dur: SLOW},
  'the-machine': {kind: 'gears', dur: NORMAL},
  'how-the-system-works': {kind: 'gears', dur: HOLD},
  'the-mechanism': {kind: 'gears', dur: NORMAL},
  'set-in-motion': {kind: 'gears', dur: BEAT},
  'the-scheme-turns': {kind: 'gears', dur: SLOW},

  // --- faultsplit: 制度 / 構造が崩壊・亀裂 ---
  'fault-split': {kind: 'faultsplit', dur: NORMAL},
  'fault-split-quick': {kind: 'faultsplit', dur: QUICK},
  'fault-split-slow': {kind: 'faultsplit', dur: SLOW},
  'the-system-cracks': {kind: 'faultsplit', dur: NORMAL},
  'the-collapse': {kind: 'faultsplit', dur: HOLD},
  'everything-breaks': {kind: 'faultsplit', dur: BEAT},
  'the-rupture': {kind: 'faultsplit', dur: QUICK},
  'the-foundation-splits': {kind: 'faultsplit', dur: SLOW},
} satisfies Record<string, ComponentProps<typeof MechanismReveal>>;
