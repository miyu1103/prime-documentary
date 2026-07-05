import type {ComponentProps} from 'react';
import type {StampReveal} from '../StampReveal';

// =====================================================================
// StampReveal — プリセットカタログ（MOTIONKIT）
//   ラバースタンプ「判決/評決」リビール用の定番ワード集。
//   PD の legal / crime / finance テーマに合わせて調律。
//   props 型は {text: string; color?: string; dur?: number} と厳密一致。
//   color 既定は色あせた赤（#C0473E）。区別のため一部を色替え：
//     ・INK_RED     '#C0473E' 既定の色あせた朱肉赤（有罪・否定系の主役）
//     ・INK_CRIMSON '#9E2B25' より濃い血赤（重罪・破産などの強調）
//     ・INK_ELECTRIC'#2E7DEF' 電光ブルー（機密・封印のクール系）
//     ・INK_GOLD    '#C9A227' 褪せた金（和解・支払い・認可の落ち着き）
//     ・INK_GREEN   '#2F8F5B' 緑（承認・支払い済みの肯定系）
//     ・INK_MUTED   '#6B7079' くすんだグレー（却下・棄却・終結の中立）
//   dur は既定（Composition の durationInFrames）に委ねるため未指定。
// =====================================================================

const INK_RED = '#C0473E';
const INK_CRIMSON = '#9E2B25';
const INK_ELECTRIC = '#2E7DEF';
const INK_GOLD = '#C9A227';
const INK_GREEN = '#2F8F5B';
const INK_MUTED = '#6B7079';

export const stampRevealPresets = {
  // --- Verdict：評決（有罪・無罪） ---
  'verdict-guilty': {text: 'GUILTY', color: INK_RED},
  'verdict-convicted': {text: 'CONVICTED', color: INK_CRIMSON},
  'verdict-acquitted': {text: 'ACQUITTED', color: INK_GREEN},
  'verdict-indicted': {text: 'INDICTED', color: INK_RED},

  // --- Ruling：裁判所の処分（認容・棄却） ---
  'ruling-overruled': {text: 'OVERRULED', color: INK_CRIMSON},
  'ruling-sustained': {text: 'SUSTAINED', color: INK_ELECTRIC},
  'ruling-granted': {text: 'GRANTED', color: INK_GREEN},
  'ruling-denied': {text: 'DENIED', color: INK_RED},
  'ruling-dismissed': {text: 'DISMISSED', color: INK_MUTED},
  'ruling-settled': {text: 'SETTLED', color: INK_GOLD},

  // --- Records：記録の取り扱い（封印・機密） ---
  'record-sealed': {text: 'SEALED', color: INK_ELECTRIC},
  'record-classified': {text: 'CLASSIFIED', color: INK_ELECTRIC},
  'record-confidential': {text: 'CONFIDENTIAL', color: INK_ELECTRIC},
  'record-redacted': {text: 'REDACTED', color: INK_MUTED},
  'record-evidence': {text: 'EVIDENCE', color: INK_GOLD},
  'record-exhibit-a': {text: 'EXHIBIT A', color: INK_GOLD},

  // --- Crime / fraud：不正・犯罪 ---
  'crime-fraud': {text: 'FRAUD', color: INK_RED},
  'crime-void': {text: 'VOID', color: INK_CRIMSON},
  'crime-forged': {text: 'FORGED', color: INK_CRIMSON},
  'crime-wanted': {text: 'WANTED', color: INK_RED},

  // --- Finance：金融・会計 ---
  'finance-paid': {text: 'PAID', color: INK_GREEN},
  'finance-bankrupt': {text: 'BANKRUPT', color: INK_CRIMSON},
  'finance-overdue': {text: 'OVERDUE', color: INK_RED},
  'finance-approved': {text: 'APPROVED', color: INK_GREEN},
  'finance-rejected': {text: 'REJECTED', color: INK_RED},

  // --- Status：進行状態（終結・終了） ---
  'status-closed': {text: 'CLOSED', color: INK_MUTED},
  'status-final': {text: 'FINAL', color: INK_GOLD},
} satisfies Record<string, ComponentProps<typeof StampReveal>>;
