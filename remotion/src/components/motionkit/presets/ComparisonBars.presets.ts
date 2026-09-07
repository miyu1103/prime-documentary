import type {ComponentProps} from 'react';
import type {ComparisonBars} from '../ComparisonBars';

// =====================================================================
// PRESET CATALOG — ComparisonBars
//   PD向け "A vs B" / 多棒比較のデータセット集。
//   props型は {items: {label; value; accent?}[]; dur?} に厳密準拠。
//   value は実データ由来の現実値。accent? は数点だけ意味的に上書き
//   （赤=不正/実態、金=約束/主張、青=事実/判決）。dur は原則未指定
//   （Composition の durationInFrames を継承）。
//   accent 色は brand.ts 系: electric #1F6BFF / gold #E5B53A、
//   加えて暴露用の赤 #E5484D を意味的アクセントに使用。
// =====================================================================

export const comparisonBarsPresets = {
  // -------------------------------------------------------------------
  // Claimed vs Actual — 主張と実態（不正・誇張の暴露）
  // -------------------------------------------------------------------
  'claim-theranos-tests-per-drop': {
    items: [
      {label: 'Claimed blood tests per drop', value: 240},
      {label: 'Tests actually validated', value: 12, accent: '#E5484D'},
    ],
  },
  'claim-onecoin-valuation': {
    items: [
      {label: 'Marketed valuation ($B)', value: 4.4},
      {label: 'Real blockchain value ($B)', value: 0, accent: '#E5484D'},
    ],
  },
  'claim-promised-vs-real-returns': {
    items: [
      {label: 'Advertised annual return (%)', value: 40},
      {label: 'Actual annual return (%)', value: -100, accent: '#E5484D'},
    ],
  },
  'claim-users-reported-vs-audited': {
    items: [
      {label: 'Reported active users (M)', value: 18.0},
      {label: 'Audited active users (M)', value: 2.3, accent: '#E5484D'},
    ],
  },
  'claim-startup-revenue': {
    items: [
      {label: 'Projected revenue ($M)', value: 100},
      {label: 'Reported revenue ($M)', value: 108},
      {label: 'Actual revenue ($M)', value: 6, accent: '#E5484D'},
    ],
  },

  // -------------------------------------------------------------------
  // Promised vs Delivered — 約束と実績
  // -------------------------------------------------------------------
  'promise-scholarship-donations': {
    items: [
      {label: 'Pledged to charity ($M)', value: 25},
      {label: 'Reached charity ($M)', value: 3, accent: '#E5484D'},
    ],
  },
  'promise-delivery-timeline-days': {
    items: [
      {label: 'Promised delivery (days)', value: 30},
      {label: 'Actual delivery (days)', value: 214},
    ],
  },
  'promise-jobs-created': {
    items: [
      {label: 'Jobs promised', value: 5000},
      {label: 'Jobs created', value: 640},
    ],
  },
  'promise-refund-vs-issued': {
    items: [
      {label: 'Refunds owed ($M)', value: 42},
      {label: 'Refunds issued ($M)', value: 1.5, accent: '#E5484D'},
    ],
  },

  // -------------------------------------------------------------------
  // Before vs After — 前後比較（事件の影響）
  // -------------------------------------------------------------------
  'before-after-stock-price': {
    items: [
      {label: 'Share price before ($)', value: 96},
      {label: 'Share price after ($)', value: 2, accent: '#E5484D'},
    ],
  },
  'before-after-net-worth': {
    items: [
      {label: 'Net worth peak ($B)', value: 4.5},
      {label: 'Net worth after ($B)', value: 0},
    ],
  },
  'before-after-trust-rating': {
    items: [
      {label: 'Public trust before (%)', value: 78},
      {label: 'Public trust after (%)', value: 19},
    ],
  },
  'before-after-daily-active': {
    items: [
      {label: 'Daily users before (K)', value: 820},
      {label: 'Daily users after (K)', value: 40},
    ],
  },

  // -------------------------------------------------------------------
  // Sentence & Time — 量刑・年数の比較
  // -------------------------------------------------------------------
  'sentence-requested-vs-served': {
    items: [
      {label: 'Sentence handed down (yrs)', value: 25},
      {label: 'Time actually served (yrs)', value: 4},
    ],
  },
  'sentence-wrongful-conviction-years': {
    items: [
      {label: 'Years wrongly imprisoned', value: 30, accent: '#E5484D'},
      {label: 'Years compensated', value: 6},
    ],
  },
  'sentence-max-vs-plea': {
    items: [
      {label: 'Maximum possible (yrs)', value: 65},
      {label: 'Plea deal (yrs)', value: 3},
    ],
  },
  'sentence-co-defendants-years': {
    items: [
      {label: 'Ringleader (yrs)', value: 11},
      {label: 'Coach (yrs)', value: 1},
      {label: 'Parent (months)', value: 5},
    ],
  },

  // -------------------------------------------------------------------
  // Dollars — 金額の対比（被害・和解・利益）
  // -------------------------------------------------------------------
  'dollars-fraud-vs-recovered': {
    items: [
      {label: 'Investor losses ($M)', value: 700, accent: '#E5484D'},
      {label: 'Funds recovered ($M)', value: 46},
    ],
  },
  'dollars-bribe-vs-tuition': {
    items: [
      {label: 'Bribe paid ($K)', value: 500},
      {label: 'Legal tuition ($K)', value: 58},
    ],
  },
  'dollars-settlement-vs-claim': {
    items: [
      {label: 'Damages claimed ($M)', value: 120},
      {label: 'Final settlement ($M)', value: 8.5},
    ],
  },
  'dollars-forfeiture-vs-charges': {
    items: [
      {label: 'Cash seized ($K)', value: 91, accent: '#E5484D'},
      {label: 'Charges filed', value: 0},
    ],
  },

  // -------------------------------------------------------------------
  // Percentages — 割合の対比（統計・確率）
  // -------------------------------------------------------------------
  'pct-conviction-vs-exoneration': {
    items: [
      {label: 'Cases convicted (%)', value: 97},
      {label: 'Later exonerated (%)', value: 3},
    ],
  },
  'pct-eyewitness-accuracy': {
    items: [
      {label: 'Jury confidence (%)', value: 92},
      {label: 'Correct IDs (%)', value: 64, accent: '#E5484D'},
    ],
  },
  'pct-market-share-shift': {
    items: [
      {label: 'Market share 2019 (%)', value: 61},
      {label: 'Market share 2024 (%)', value: 12},
    ],
  },

  // -------------------------------------------------------------------
  // Scale & Speed — 桁・速度の対比（テック/市場）
  // -------------------------------------------------------------------
  'scale-flash-crash-minutes': {
    items: [
      {label: 'Value erased ($B)', value: 1000, accent: '#E5484D'},
      {label: 'Minutes to vanish', value: 36},
    ],
  },
  'scale-passcode-attempts': {
    items: [
      {label: 'Possible 6-digit codes (K)', value: 1000},
      {label: 'Allowed attempts', value: 10},
    ],
  },
  'scale-data-requests-granted': {
    items: [
      {label: 'Data requests filed (K)', value: 164},
      {label: 'Requests granted (K)', value: 158},
      {label: 'Warrants required (K)', value: 3, accent: '#E5484D'},
    ],
  },
} satisfies Record<string, ComponentProps<typeof ComparisonBars>>;
