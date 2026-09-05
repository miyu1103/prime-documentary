import type {ComponentProps} from 'react';
import type {NumberTicker} from '../NumberTicker';

// =====================================================================
// MOTIONKIT — NumberTicker PRESETS (Prime Documentary)
//   ヒーロー数値の使い回しカタログ。すべて NumberTicker の props 型に厳密適合。
//   props: value(必須) / prefix? / suffix? / decimals? / topLabel? / label?
//   ・prefix は通貨記号など（例 '$'）、suffix は単位（例 'B' 'M' '%'）
//   ・大きな金額は B(十億)/M(百万) に丸めて decimals で小数桁を制御
//   ・dur は意図的に未指定（Composition の durationInFrames をそのまま使う）
//   使い方: <NumberTicker {...numberTickerPresets['fraud-loss-65b']} />
// =====================================================================

export const numberTickerPresets = {
  // --- 金銭被害（Dollar losses：詐欺・破綻・崩壊） ---------------------
  'fraud-loss-65b': {
    value: 65,
    prefix: '$',
    suffix: 'B',
    decimals: 0,
    topLabel: 'Total investor losses',
    label: 'Wiped out in the collapse',
  },
  'ponzi-loss-4-8b': {
    value: 4.8,
    prefix: '$',
    suffix: 'B',
    decimals: 1,
    topLabel: 'Vanished funds',
    label: 'Never recovered by victims',
  },
  'valuation-9b': {
    value: 9,
    prefix: '$',
    suffix: 'B',
    decimals: 0,
    topLabel: 'Peak valuation',
    label: 'Before the fraud unraveled',
  },
  'crypto-missing-2b': {
    value: 2,
    prefix: '$',
    suffix: 'B',
    decimals: 0,
    topLabel: 'Investor money missing',
    label: 'The founder disappeared',
  },
  'settlement-140m': {
    value: 140,
    prefix: '$',
    suffix: 'M',
    decimals: 0,
    topLabel: 'Court settlement',
    label: 'Paid to the plaintiffs',
  },
  'restitution-27m': {
    value: 27.5,
    prefix: '$',
    suffix: 'M',
    decimals: 1,
    topLabel: 'Restitution ordered',
    label: 'For defrauded families',
  },
  'daily-burn-1m': {
    value: 1,
    prefix: '$',
    suffix: 'M',
    decimals: 0,
    topLabel: 'Burned every day',
    label: 'To keep the scheme alive',
  },
  'flash-crash-1t': {
    value: 1,
    prefix: '$',
    suffix: 'T',
    decimals: 0,
    topLabel: 'Erased in minutes',
    label: 'The 2010 Flash Crash',
  },

  // --- 被害者・人数（Victim counts） ---------------------------------
  'victims-count': {
    value: 38000,
    topLabel: 'Victims worldwide',
    label: 'Across 175 countries',
  },
  'defrauded-investors': {
    value: 4900,
    topLabel: 'Defrauded investors',
    label: 'Lost their life savings',
  },
  'families-affected': {
    value: 720,
    topLabel: 'Families affected',
    label: 'In a single county',
  },
  'patients-at-risk': {
    value: 890000,
    topLabel: 'Blood tests processed',
    label: 'On unproven machines',
  },

  // --- 服役年数・刑期（Years in prison / sentences） ------------------
  'sentence-years-150': {
    value: 150,
    suffix: ' yrs',
    decimals: 0,
    topLabel: 'Prison sentence',
    label: 'The maximum handed down',
  },
  'sentence-years-11': {
    value: 11,
    suffix: ' yrs',
    decimals: 0,
    topLabel: 'Years in federal prison',
    label: 'For wire fraud',
  },
  'wrongful-years-30': {
    value: 30,
    suffix: ' yrs',
    decimals: 0,
    topLabel: 'Years wrongfully imprisoned',
    label: 'Before exoneration',
  },
  'time-on-death-row': {
    value: 22,
    suffix: ' yrs',
    decimals: 0,
    topLabel: 'Years on death row',
    label: 'An innocent man',
  },

  // --- 割合・確率（Percentages） -------------------------------------
  'apy-promised-48': {
    value: 48,
    suffix: '%',
    decimals: 0,
    topLabel: 'Returns promised',
    label: 'A mathematical impossibility',
  },
  'error-rate-accuracy': {
    value: 3.9,
    suffix: '%',
    decimals: 1,
    topLabel: 'Tests that were accurate',
    label: 'The rest were unreliable',
  },
  'recovery-rate': {
    value: 0.5,
    suffix: '%',
    decimals: 1,
    topLabel: 'Of losses recovered',
    label: 'For every dollar stolen',
  },
  'conviction-rate': {
    value: 97,
    suffix: '%',
    decimals: 0,
    topLabel: 'Federal conviction rate',
    label: 'Once charges are filed',
  },

  // --- 期間・日数（Days / duration） ---------------------------------
  'days-on-the-run': {
    value: 1400,
    suffix: ' days',
    decimals: 0,
    topLabel: 'Days as a fugitive',
    label: 'Before the arrest',
  },
  'trial-length-days': {
    value: 74,
    suffix: ' days',
    decimals: 0,
    topLabel: 'Days on trial',
    label: 'The longest in state history',
  },

  // --- 比率・倍率（Ratios / multiples） ------------------------------
  'leverage-ratio': {
    value: 30,
    suffix: '×',
    decimals: 0,
    topLabel: 'Leverage on the books',
    label: 'When the market turned',
  },
  'return-multiple': {
    value: 12,
    suffix: '×',
    decimals: 0,
    topLabel: 'Claimed return',
    label: 'On the original stake',
  },
} satisfies Record<string, ComponentProps<typeof NumberTicker>>;
