import type {ComponentProps} from 'react';
import type {PonziCurve} from '../PonziCurve';

// =====================================================================
// PonziCurve プリセットカタログ（MOTIONKIT）
//   「約束されたリターン（GOLD 破線・指数）」が上へ描かれ、その裏で
//   「実際の価値（electric 実線）」が低く追従、ピークで乖離し、直後に
//   実際の曲線が 0 へ垂直落下＝崩壊する定型モーション。
//   詐欺の物語（ポンジ／仮想通貨トークン／不動産バブル／pump-and-dump／
//   年金詐欺）の「絶頂 → 崩壊」を一枚で語るための語彙。
//   props は PonziCurve の厳密型に一致: {peakLabel?, collapseLabel?, dur?}。
//   peakLabel   = ピーク（約束・絶頂）の見出し（上部の THE PROMISE 下）。
//   collapseLabel = 崩壊マーカーの見出し（赤・底）。
//   dur は指定しない（Composition の durationInFrames に従わせる）。
// =====================================================================

export const ponziCurvePresets = {
  // --- 古典的ポンジ・スキーム（新規資金で配当を偽装 → 破綻） ---
  'ponzi-paper-profits': {
    peakLabel: 'Paper profits',
    collapseLabel: 'The scheme collapses',
  },
  'ponzi-guaranteed-returns': {
    peakLabel: 'Guaranteed returns',
    collapseLabel: 'Nothing was real',
  },
  'ponzi-steady-gains': {
    peakLabel: 'Impossibly steady gains',
    collapseLabel: 'The music stops',
  },
  'ponzi-too-good': {
    peakLabel: 'Too good to be true',
    collapseLabel: 'Investors wiped out',
  },
  'ponzi-consistent-monthly': {
    peakLabel: 'Consistent monthly checks',
    collapseLabel: 'The payouts stop',
  },

  // --- 仮想通貨トークン（誇張された時価総額 → ラグプル／取引停止） ---
  'crypto-all-time-high': {
    peakLabel: 'All-time high',
    collapseLabel: 'Zero',
  },
  'crypto-to-the-moon': {
    peakLabel: 'To the moon',
    collapseLabel: 'The token goes to zero',
  },
  'crypto-promised-20': {
    peakLabel: 'Promised 20% returns',
    collapseLabel: 'Withdrawals frozen',
  },
  'crypto-rug-pull': {
    peakLabel: 'Everyone is buying',
    collapseLabel: 'The founders vanish',
  },
  'crypto-staking-yield': {
    peakLabel: 'Guaranteed staking yield',
    collapseLabel: 'Liquidity gone',
  },

  // --- 不動産バブル（値上がり期待の連鎖 → 崩壊） ---
  'property-prices-only-rise': {
    peakLabel: 'Prices only go up',
    collapseLabel: 'The bubble bursts',
  },
  'property-boom': {
    peakLabel: 'The property boom',
    collapseLabel: 'Values collapse',
  },
  'property-paper-equity': {
    peakLabel: 'Paper equity',
    collapseLabel: 'Underwater',
  },
  'property-guaranteed-flip': {
    peakLabel: 'A guaranteed flip',
    collapseLabel: 'The market seizes up',
  },

  // --- Pump-and-dump（相場操縦で吊り上げ → 主犯が売り抜け暴落） ---
  'pump-hot-tip': {
    peakLabel: 'The hot stock tip',
    collapseLabel: 'The insiders cash out',
  },
  'pump-going-vertical': {
    peakLabel: 'Going vertical',
    collapseLabel: 'The dump',
  },
  'pump-cant-lose': {
    peakLabel: "Can't-lose bet",
    collapseLabel: 'The floor drops out',
  },
  'pump-record-volume': {
    peakLabel: 'Record volume',
    collapseLabel: 'A worthless share',
  },

  // --- 年金・退職金詐欺（安全神話 → 資産消失） ---
  'pension-secure-retirement': {
    peakLabel: 'A secure retirement',
    collapseLabel: 'The fund is empty',
  },
  'pension-lifetime-income': {
    peakLabel: 'Guaranteed lifetime income',
    collapseLabel: 'Redemptions halted',
  },
  'pension-safe-haven': {
    peakLabel: 'A safe haven',
    collapseLabel: 'Savings gone',
  },
  'pension-nest-egg': {
    peakLabel: 'Their entire nest egg',
    collapseLabel: 'Nothing left',
  },
} satisfies Record<string, ComponentProps<typeof PonziCurve>>;
