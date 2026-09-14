import type {ComponentProps} from 'react';
import type {MarketTicker} from '../MarketTicker';

// =====================================================================
// MOTIONKIT — MarketTicker PRESETS (Prime Documentary)
//   放送級の下部フィナンス・ティッカー帯の使い回しカタログ。
//   すべて MarketTicker の props 型に厳密適合。
//   props: items(必須: {symbol, change}[]) / dur?(任意・未指定推奨)
//   ・symbol は総称/指数風の架空ティッカー（実在社名の断定を避ける）。
//   ・change は符号付き % 数値（正=上げ緑 / 負=下げ赤）。
//   ・1セットあたり 4〜8 銘柄。dur は意図的に未指定（Composition の
//     durationInFrames をそのまま使う）。
//   使い方: <MarketTicker {...marketTickerPresets['crash-day-all-red']} />
// =====================================================================

export const marketTickerPresets = {
  // --- 暴落デー（Crash day：全面安・パニック） -----------------------
  'crash-day-all-red': {
    items: [
      {symbol: 'DJIA', change: -6.98},
      {symbol: 'SPX', change: -7.41},
      {symbol: 'NDX', change: -8.12},
      {symbol: 'RUT', change: -9.24},
      {symbol: 'VIX', change: 61.7},
      {symbol: 'OIL', change: -12.4},
    ],
  },
  'black-monday': {
    items: [
      {symbol: 'DJIA', change: -22.61},
      {symbol: 'SPX', change: -20.47},
      {symbol: 'NDX', change: -19.88},
      {symbol: 'NKY', change: -14.9},
      {symbol: 'FTSE', change: -10.84},
    ],
  },
  'flash-crash-intraday': {
    items: [
      {symbol: 'DJIA', change: -9.16},
      {symbol: 'SPX', change: -8.6},
      {symbol: 'NDX', change: -10.3},
      {symbol: 'VIX', change: 45.8},
      {symbol: 'ACME', change: -36.2},
      {symbol: 'CRDX', change: -41.7},
    ],
  },
  'banking-panic-red': {
    items: [
      {symbol: 'KBW', change: -14.7},
      {symbol: 'FRST', change: -60.4},
      {symbol: 'SVBX', change: -68.9},
      {symbol: 'SPX', change: -4.62},
      {symbol: 'GOLD', change: 3.11},
      {symbol: 'US10Y', change: -8.4},
    ],
  },

  // --- バブル相場（Bubble：全面高・過熱） ----------------------------
  'bubble-day-all-green': {
    items: [
      {symbol: 'NDX', change: 8.44},
      {symbol: 'SPX', change: 5.9},
      {symbol: 'DJIA', change: 4.72},
      {symbol: 'SOXX', change: 11.3},
      {symbol: 'ARKX', change: 14.8},
      {symbol: 'VIX', change: -18.6},
    ],
  },
  'dotcom-melt-up': {
    items: [
      {symbol: 'NDX', change: 12.6},
      {symbol: 'PETS', change: 87.4},
      {symbol: 'WEBX', change: 64.2},
      {symbol: 'NETZ', change: 51.9},
      {symbol: 'SPX', change: 3.88},
    ],
  },
  'ipo-pop-euphoria': {
    items: [
      {symbol: 'HYPE', change: 128.5},
      {symbol: 'GLOW', change: 74.9},
      {symbol: 'NOVA', change: 42.3},
      {symbol: 'SPX', change: 1.94},
      {symbol: 'NDX', change: 2.71},
    ],
  },
  'meme-stock-squeeze': {
    items: [
      {symbol: 'MEME', change: 214.3},
      {symbol: 'MOON', change: 96.7},
      {symbol: 'YOLO', change: 58.1},
      {symbol: 'VIX', change: 22.4},
      {symbol: 'HEDG', change: -31.6},
    ],
  },

  // --- 通常のミックス（Mixed session：まちまち） ---------------------
  'mixed-session': {
    items: [
      {symbol: 'DJIA', change: 0.42},
      {symbol: 'SPX', change: -0.18},
      {symbol: 'NDX', change: 0.87},
      {symbol: 'RUT', change: -0.64},
      {symbol: 'VIX', change: -2.1},
      {symbol: 'GOLD', change: 0.33},
    ],
  },
  'quiet-drift': {
    items: [
      {symbol: 'SPX', change: 0.09},
      {symbol: 'DJIA', change: -0.12},
      {symbol: 'NDX', change: 0.21},
      {symbol: 'OIL', change: -0.44},
      {symbol: 'GOLD', change: 0.06},
    ],
  },
  'rotation-day': {
    items: [
      {symbol: 'XLF', change: 2.34},
      {symbol: 'XLE', change: 1.87},
      {symbol: 'XLK', change: -1.62},
      {symbol: 'SOXX', change: -2.9},
      {symbol: 'RUT', change: 1.44},
      {symbol: 'SPX', change: 0.11},
    ],
  },
  'earnings-mixed': {
    items: [
      {symbol: 'ACME', change: 6.8},
      {symbol: 'ORBX', change: -4.2},
      {symbol: 'VERT', change: 2.15},
      {symbol: 'NOVA', change: -1.73},
      {symbol: 'HELX', change: 3.94},
      {symbol: 'SPX', change: 0.28},
    ],
  },

  // --- 主要指数（Indices：ワールドマーケット） ----------------------
  'world-indices': {
    items: [
      {symbol: 'SPX', change: 0.63},
      {symbol: 'FTSE', change: -0.24},
      {symbol: 'DAX', change: 0.41},
      {symbol: 'NKY', change: 1.12},
      {symbol: 'HSI', change: -0.88},
      {symbol: 'CAC', change: 0.19},
    ],
  },
  'us-headline-indices': {
    items: [
      {symbol: 'DJIA', change: 0.35},
      {symbol: 'SPX', change: 0.52},
      {symbol: 'NDX', change: 0.94},
      {symbol: 'RUT', change: -0.31},
      {symbol: 'VIX', change: -3.7},
    ],
  },
  'safe-haven-bid': {
    items: [
      {symbol: 'GOLD', change: 2.61},
      {symbol: 'US10Y', change: -4.9},
      {symbol: 'JPY', change: 1.28},
      {symbol: 'CHF', change: 0.94},
      {symbol: 'SPX', change: -1.42},
      {symbol: 'VIX', change: 14.6},
    ],
  },

  // --- コモディティ／為替（Commodities & FX） ------------------------
  'commodities-tape': {
    items: [
      {symbol: 'OIL', change: 3.47},
      {symbol: 'GOLD', change: -0.62},
      {symbol: 'SILV', change: 1.19},
      {symbol: 'NATGAS', change: -5.8},
      {symbol: 'COPR', change: 2.04},
      {symbol: 'WHEAT', change: 0.71},
    ],
  },
  'oil-shock': {
    items: [
      {symbol: 'OIL', change: 18.9},
      {symbol: 'NATGAS', change: 11.2},
      {symbol: 'GOLD', change: 4.33},
      {symbol: 'SPX', change: -2.71},
      {symbol: 'XLE', change: 7.64},
    ],
  },
  'fx-majors': {
    items: [
      {symbol: 'EUR', change: 0.38},
      {symbol: 'JPY', change: -0.72},
      {symbol: 'GBP', change: 0.21},
      {symbol: 'CHF', change: 0.14},
      {symbol: 'DXY', change: -0.29},
    ],
  },

  // --- 暗号資産（Crypto tokens） ------------------------------------
  'crypto-tokens-mixed': {
    items: [
      {symbol: 'BTC', change: 2.84},
      {symbol: 'ETH', change: 4.11},
      {symbol: 'SOL', change: -3.62},
      {symbol: 'XRP', change: 1.05},
      {symbol: 'DOGE', change: 7.9},
      {symbol: 'ADA', change: -1.48},
    ],
  },
  'crypto-bull-run': {
    items: [
      {symbol: 'BTC', change: 14.7},
      {symbol: 'ETH', change: 21.3},
      {symbol: 'SOL', change: 38.6},
      {symbol: 'DOGE', change: 62.4},
      {symbol: 'AVAX', change: 27.1},
    ],
  },
  'crypto-capitulation': {
    items: [
      {symbol: 'BTC', change: -19.8},
      {symbol: 'ETH', change: -24.6},
      {symbol: 'SOL', change: -33.9},
      {symbol: 'LUNA', change: -99.7},
      {symbol: 'DOGE', change: -28.4},
      {symbol: 'ADA', change: -22.1},
    ],
  },
  'stablecoin-depeg': {
    items: [
      {symbol: 'USTC', change: -87.3},
      {symbol: 'LUNA', change: -96.1},
      {symbol: 'BTC', change: -12.7},
      {symbol: 'ETH', change: -15.9},
      {symbol: 'DAI', change: -1.4},
    ],
  },
  'exchange-collapse': {
    items: [
      {symbol: 'FTT', change: -78.6},
      {symbol: 'BTC', change: -14.2},
      {symbol: 'ETH', change: -16.8},
      {symbol: 'SOL', change: -41.3},
      {symbol: 'BNB', change: -9.7},
    ],
  },
} satisfies Record<string, ComponentProps<typeof MarketTicker>>;
