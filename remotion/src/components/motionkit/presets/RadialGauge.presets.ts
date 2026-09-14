import type {ComponentProps} from 'react';
import type {RadialGauge} from '../RadialGauge';

// =====================================================================
// MOTIONKIT — RadialGauge PRESET CATALOG
//   計器風フル円弧ダイヤルの読取り値プリセット集。PD の documentary 演出向けに
//   「リスク指数 / 確からしさ / 深刻度 / 確信度 / 承認率 / 脅威度」等を
//   低・中・高の3段で、一部は custom max（例 7/10）でチューニング。
//   props 型: {value:number; max?:number; label?:string; dur?:number}
//   dur は既定（Composition の durationInFrames）を使うため原則未指定。
// =====================================================================

export const radialGaugePresets = {
  // --- リスク指数（RISK INDEX・0..100 の合成スコア） ---
  'risk-index-low': {value: 18, label: 'RISK INDEX'},
  'risk-index-mid': {value: 54, label: 'RISK INDEX'},
  'risk-index-high': {value: 87, label: 'RISK INDEX'},
  'risk-index-critical': {value: 96, label: 'RISK INDEX'},

  // --- 確からしさ / 相当の理由（PROBABLE CAUSE・%） ---
  'probable-cause-weak': {value: 22, label: 'PROBABLE CAUSE'},
  'probable-cause-borderline': {value: 51, label: 'PROBABLE CAUSE'},
  'probable-cause-strong': {value: 84, label: 'PROBABLE CAUSE'},

  // --- 確率（PROBABILITY・%） ---
  'probability-low': {value: 12, label: 'PROBABILITY'},
  'probability-even': {value: 50, label: 'PROBABILITY'},
  'probability-high': {value: 78, label: 'PROBABILITY'},

  // --- 深刻度（SEVERITY・1..10 スケール） ---
  'severity-minor': {value: 3, max: 10, label: 'SEVERITY'},
  'severity-serious': {value: 7, max: 10, label: 'SEVERITY'},
  'severity-catastrophic': {value: 10, max: 10, label: 'SEVERITY'},

  // --- 確信度（CONFIDENCE・%） ---
  'confidence-low': {value: 34, label: 'CONFIDENCE'},
  'confidence-moderate': {value: 62, label: 'CONFIDENCE'},
  'confidence-high': {value: 93, label: 'CONFIDENCE'},

  // --- 承認率 / 支持率（APPROVAL・%） ---
  'approval-underwater': {value: 27, label: 'APPROVAL'},
  'approval-split': {value: 49, label: 'APPROVAL'},
  'approval-landslide': {value: 71, label: 'APPROVAL'},

  // --- 脅威度（THREAT LEVEL・1..5 段階） ---
  'threat-level-guarded': {value: 2, max: 5, label: 'THREAT LEVEL'},
  'threat-level-elevated': {value: 3, max: 5, label: 'THREAT LEVEL'},
  'threat-level-severe': {value: 5, max: 5, label: 'THREAT LEVEL'},

  // --- 信用度 / 与信スコア（CREDIT SCORE・0..850） ---
  'credit-score-subprime': {value: 540, max: 850, label: 'CREDIT SCORE'},
  'credit-score-prime': {value: 760, max: 850, label: 'CREDIT SCORE'},

  // --- 評決の一致（JURY CONSENSUS・12人中） ---
  'jury-consensus-hung': {value: 6, max: 12, label: 'JURY CONSENSUS'},
  'jury-consensus-unanimous': {value: 12, max: 12, label: 'JURY CONSENSUS'},
} satisfies Record<string, ComponentProps<typeof RadialGauge>>;
