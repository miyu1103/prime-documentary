import type {ComponentProps} from 'react';
import type {VoteTally} from '../VoteTally';

// =====================================================================
// VoteTally プリセットカタログ（MOTIONKIT）
//   法廷・評議会・陪審の「評決の割れ方」を語るための定型。
//   props は VoteTally の厳密型に一致: {majority, dissent, label?, dur?}。
//   majority = 多数（ゴールド席）、dissent = 反対（マットレッド席）。
//   dur は指定しない（Composition の durationInFrames に従わせる）。
//   label は評決の物語的な意味づけ（'Unanimous' 等）。
// =====================================================================

export const voteTallyPresets = {
  // --- SCOTUS: 全9名がそろった評決（最も代表的な割れ方） ---
  'scotus-9-0': {majority: 9, dissent: 0, label: 'Unanimous'},
  'scotus-8-1': {majority: 8, dissent: 1, label: 'A single dissent'},
  'scotus-7-2': {majority: 7, dissent: 2, label: 'A clear majority'},
  'scotus-6-3': {majority: 6, dissent: 3, label: 'A divided court'},
  'scotus-5-4': {majority: 5, dissent: 4, label: 'The deciding vote'},
  'scotus-4-4': {majority: 4, dissent: 4, label: 'Evenly divided'},

  // --- SCOTUS: 忌避・欠員で8名または7名が投票した評決 ---
  'scotus-8-0': {majority: 8, dissent: 0, label: 'Unanimous, one recused'},
  'scotus-7-1': {majority: 7, dissent: 1, label: 'A single dissent'},
  'scotus-6-2': {majority: 6, dissent: 2, label: 'A clear majority'},
  'scotus-5-3': {majority: 5, dissent: 3, label: 'A divided court'},

  // --- 控訴審パネル（3名の裁判官） ---
  'panel-3-0': {majority: 3, dissent: 0, label: 'A unanimous panel'},
  'panel-2-1': {majority: 2, dissent: 1, label: 'A split panel'},

  // --- 大法廷（en banc、11名） ---
  'enbanc-11-0': {majority: 11, dissent: 0, label: 'Unanimous en banc'},
  'enbanc-7-4': {majority: 7, dissent: 4, label: 'A fractured court'},
  'enbanc-6-5': {majority: 6, dissent: 5, label: 'By a single vote'},

  // --- 陪審（12名・刑事評決） ---
  'jury-12-0': {majority: 12, dissent: 0, label: 'A unanimous verdict'},
  'jury-11-1': {majority: 11, dissent: 1, label: 'A lone holdout'},
  'jury-10-2': {majority: 10, dissent: 2, label: 'A majority verdict'},
  'jury-9-3': {majority: 9, dissent: 3, label: 'A divided jury'},
  'jury-8-4': {majority: 8, dissent: 4, label: 'Deadlocked'},
  'jury-6-6': {majority: 6, dissent: 6, label: 'A hung jury'},

  // --- 取締役会・委員会（議決の可否） ---
  'board-7-0': {majority: 7, dissent: 0, label: 'Approved unanimously'},
  'board-6-1': {majority: 6, dissent: 1, label: 'A single objection'},
  'board-5-2': {majority: 5, dissent: 2, label: 'The motion carries'},
  'board-4-3': {majority: 4, dissent: 3, label: 'Narrowly approved'},
  'board-3-2': {majority: 3, dissent: 2, label: 'By the slimmest margin'},
} satisfies Record<string, ComponentProps<typeof VoteTally>>;
