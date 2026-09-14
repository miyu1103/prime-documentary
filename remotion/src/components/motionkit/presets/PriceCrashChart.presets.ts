import type {ComponentProps} from 'react';
import type {PriceCrashChart} from '../PriceCrashChart';

// =====================================================================
// PriceCrashChart — プリセットカタログ
//   各プリセットは series（rise→crash の生値・コンポーネントが自動正規化）、
//   label（Y軸/系列名）、crashLabel（最安値マーカーの見出し）を持つ。
//   series は明示配列（~14-24 点）で崩壊プロファイルを作り分ける:
//     slow bleed / sudden cliff / bubble-then-pop / dead-cat-bounce / flash crash。
//   dur は既定（Composition の durationInFrames）に任せる（必要時のみ）。
// =====================================================================

export const priceCrashChartPresets = {
  // ---------------------------------------------------------------
  // Equity indices — 指数のドローダウン（緩やかな山→急落）
  // ---------------------------------------------------------------
  'dow-black-monday': {
    label: 'DOW JONES',
    crashLabel: 'BLACK MONDAY',
    // なだらかに高値更新 → 一日で断崖
    series: [
      2050, 2120, 2180, 2240, 2310, 2360, 2405, 2440, 2470, 2495,
      2510, 2500, 2460, 1990, 1760, 1740, 1755, 1730,
    ],
  },

  'sp500-slow-bleed': {
    label: 'S&P 500',
    crashLabel: 'THE COLLAPSE',
    // 長く続く緩やかな出血（slow bleed・戻りなし）
    series: [
      480, 476, 470, 465, 458, 452, 447, 441, 434, 428,
      421, 415, 408, 402, 396, 389, 383, 377, 371, 366,
    ],
  },

  'nasdaq-dotcom': {
    label: 'NASDAQ',
    crashLabel: 'THE BUBBLE BURSTS',
    // ドットコム・バブル→ポップ（bubble-then-pop）
    series: [
      1400, 1700, 2100, 2600, 3200, 3900, 4700, 5048, 4600, 4100,
      3500, 2900, 2400, 2050, 1780, 1620, 1500, 1420,
    ],
  },

  'ftse-margin-call': {
    label: 'FTSE 100',
    crashLabel: 'MARGIN CALL',
    // 高値圏で失速 → 二段の投げ売り
    series: [
      6200, 6420, 6580, 6690, 6740, 6700, 6560, 6100, 5720, 5680,
      5610, 5230, 4980, 4910, 4870, 4920,
    ],
  },

  'nikkei-lost-decade': {
    label: 'NIKKEI 225',
    crashLabel: 'THE UNWIND',
    // 天井→長期の階段状デフレ（slow structural bleed）
    series: [
      38900, 38100, 36500, 34200, 31800, 29500, 27100, 24800, 22600, 20500,
      18700, 17200, 16050, 15200, 14700, 14350, 14100,
    ],
  },

  // ---------------------------------------------------------------
  // Crypto — 高ボラのトークン崩壊
  // ---------------------------------------------------------------
  'token-price-rugpull': {
    label: 'TOKEN PRICE',
    crashLabel: 'THE RUG PULL',
    // 一気に垂直落下（sudden cliff・ほぼゼロへ）
    series: [
      0.42, 0.55, 0.71, 0.98, 1.34, 1.88, 2.55, 3.1, 3.4, 3.36,
      0.62, 0.18, 0.09, 0.06, 0.05, 0.05,
    ],
  },

  'token-price-flash': {
    label: 'TOKEN PRICE',
    crashLabel: 'FLASH CRASH',
    // 瞬間急落 → 部分回復（flash crash）
    series: [
      118, 121, 124, 126, 129, 131, 132, 133, 71, 58,
      64, 88, 101, 108, 110, 109,
    ],
  },

  'stablecoin-depeg': {
    label: 'STABLECOIN',
    crashLabel: 'THE DEPEG',
    // 1.00 固定→ペグ崩壊→ゼロへ（sudden cliff）
    series: [
      1.0, 1.0, 1.0, 0.999, 1.0, 0.998, 0.985, 0.94, 0.72, 0.41,
      0.22, 0.11, 0.05, 0.02, 0.01, 0.01,
    ],
  },

  'meme-coin-pump-dump': {
    label: 'MEME COIN',
    crashLabel: 'PUMP & DUMP',
    // 放物線の急騰 → 即崩壊（bubble-then-pop）
    series: [
      0.002, 0.004, 0.009, 0.021, 0.048, 0.11, 0.24, 0.41, 0.58, 0.55,
      0.19, 0.07, 0.03, 0.014, 0.009, 0.007,
    ],
  },

  'exchange-token-insolvency': {
    label: 'EXCHANGE TOKEN',
    crashLabel: 'INSOLVENCY',
    // ジリ高→取り付け騒ぎで一晩崩壊
    series: [
      22.4, 23.1, 24.0, 25.2, 25.9, 26.3, 25.7, 22.1, 12.8, 6.4,
      3.2, 1.9, 1.4, 1.2, 1.1,
    ],
  },

  // ---------------------------------------------------------------
  // Funds & firms — ファンド/企業の破綻
  // ---------------------------------------------------------------
  'fund-value-blowup': {
    label: 'FUND VALUE',
    crashLabel: 'THE BLOWUP',
    // レバレッジ膨張 → 強制清算（sudden cliff）
    series: [
      100, 108, 117, 126, 138, 149, 161, 172, 168, 141,
      96, 52, 28, 15, 9, 7,
    ],
  },

  'fund-value-slow-drawdown': {
    label: 'FUND VALUE',
    crashLabel: 'REDEMPTIONS',
    // 解約連鎖でじわじわ縮小（slow bleed）
    series: [
      100, 99, 97, 96, 94, 91, 89, 86, 83, 80,
      77, 74, 71, 68, 66, 63, 61, 59,
    ],
  },

  'share-price-fraud': {
    label: 'SHARE PRICE',
    crashLabel: 'THE FRAUD EXPOSED',
    // 高値横ばい → 内部告発で断崖
    series: [
      88, 91, 93, 95, 96, 96, 95, 94, 92, 58,
      31, 17, 9, 5, 3, 2,
    ],
  },

  'share-price-bankruptcy': {
    label: 'SHARE PRICE',
    crashLabel: 'CHAPTER 11',
    // 段階的な失望売り → 上場廃止圏
    series: [
      64, 61, 57, 52, 48, 43, 39, 34, 29, 24,
      19, 14, 9, 5, 2, 1,
    ],
  },

  'valuation-down-round': {
    label: 'VALUATION',
    crashLabel: 'THE DOWN ROUND',
    // ユニコーン評価額の急収縮
    series: [
      12, 18, 26, 37, 47, 47, 44, 38, 29, 19,
      12, 8, 6, 5, 4.5,
    ],
  },

  // ---------------------------------------------------------------
  // Market cap — 時価総額の蒸発
  // ---------------------------------------------------------------
  'market-cap-wipeout': {
    label: 'MARKET CAP',
    crashLabel: 'THE WIPEOUT',
    // 記録的高値 → 数週間で半減以下
    series: [
      620, 690, 760, 830, 900, 970, 1030, 1080, 1005, 880,
      720, 560, 430, 360, 320, 300,
    ],
  },

  'market-cap-single-day': {
    label: 'MARKET CAP',
    crashLabel: 'ONE TRADING DAY',
    // 決算ミスで一日蒸発（sudden cliff）
    series: [
      240, 242, 244, 245, 246, 247, 247, 248, 176, 168,
      171, 169, 170, 170,
    ],
  },

  'market-cap-dead-cat': {
    label: 'MARKET CAP',
    crashLabel: 'DEAD CAT BOUNCE',
    // 急落→戻し（罠）→再び安値更新（dead-cat-bounce）
    series: [
      500, 520, 535, 542, 500, 430, 360, 300, 355, 400,
      372, 300, 240, 205, 190, 185,
    ],
  },

  // ---------------------------------------------------------------
  // Commodities & FX — 商品/通貨のショック
  // ---------------------------------------------------------------
  'oil-negative-price': {
    label: 'CRUDE OIL',
    crashLabel: 'BELOW ZERO',
    // 需要消滅で史上初のマイナス（sudden cliff）
    series: [
      61, 58, 54, 49, 43, 38, 32, 27, 21, 15,
      8, 2, -4, -12, -6, 4,
    ],
  },

  'currency-devaluation': {
    label: 'EXCHANGE RATE',
    crashLabel: 'THE DEVALUATION',
    // ペッグ防衛失敗 → 一夜で切り下げ
    series: [
      100, 100, 99, 100, 99, 98, 96, 91, 74, 55,
      44, 38, 35, 33, 32,
    ],
  },

  'gold-panic-liquidation': {
    label: 'GOLD (USD/oz)',
    crashLabel: 'PANIC SELLING',
    // 逃避買い→現金化売りでV字の谷（flash crash）
    series: [
      1920, 1948, 1965, 1980, 1972, 1910, 1790, 1680, 1611, 1690,
      1760, 1815, 1848, 1860,
    ],
  },

  // ---------------------------------------------------------------
  // Housing & credit — 不動産/信用の崩壊
  // ---------------------------------------------------------------
  'home-price-index-2008': {
    label: 'HOME PRICE INDEX',
    crashLabel: 'THE SUBPRIME CRASH',
    // 住宅バブル→数年の下落（bubble-then-slow-bleed）
    series: [
      140, 152, 165, 178, 189, 196, 200, 197, 188, 176,
      162, 148, 136, 128, 122, 119, 118,
    ],
  },

  'bond-yield-spike': {
    label: 'BOND PRICE',
    crashLabel: 'THE ROUT',
    // 利上げで債券価格が階段状に下落（slow bleed）
    series: [
      102, 101, 100, 98, 96, 93, 90, 87, 84, 81,
      78, 75, 72, 70, 68, 67,
    ],
  },

  // ---------------------------------------------------------------
  // Generic / hero — 汎用の見せ場（既定尺）
  // ---------------------------------------------------------------
  'index-price-classic': {
    label: 'INDEX / PRICE (USD)',
    crashLabel: 'FLASH CRASH',
    // 教科書的な山→鋭い急落→弱いリバウンド
    series: [
      120, 148, 176, 205, 236, 268, 300, 330, 352, 360,
      300, 210, 132, 96, 118, 140, 128,
    ],
  },

  'index-cliff-no-recovery': {
    label: 'INDEX / PRICE (USD)',
    crashLabel: 'THE COLLAPSE',
    // 高値圏の横ばい → 一直線の断崖（sudden cliff・戻りなし）
    series: [
      410, 418, 424, 428, 430, 431, 430, 428, 425, 300,
      190, 120, 78, 52, 40, 36,
    ],
  },

  'index-double-top': {
    label: 'MARKET INDEX',
    crashLabel: 'THE UNRAVELING',
    // ダブルトップ → 二段崩落
    series: [
      300, 340, 372, 388, 360, 384, 396, 340, 268, 300,
      250, 176, 120, 92, 80, 76,
    ],
  },
} satisfies Record<string, ComponentProps<typeof PriceCrashChart>>;
