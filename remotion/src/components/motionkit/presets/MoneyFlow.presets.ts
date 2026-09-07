import type {ComponentProps} from 'react';
import type {MoneyFlow} from '../MoneyFlow';

// =====================================================================
// MoneyFlow — PRESET CATALOG (MOTIONKIT)  「Follow the money」
//   決定論的な資金フロー図。nodes は {x, y, label?} を 0..1 正規化座標で
//   与える（x=左→右, y=上→下）。edges は {from, to, weight?} で nodes 配列の
//   index を指す（from→to へ金が流れる）。weight は太さ/流量スケール（未指定=1）。
//   ラベルは総称語のみ（実在企業名/実在人物なし）。
//   dur はコンポジション既定尺を使う場合は設定しない（指示準拠）。
//   PD向けドキュメンタリーの典型トポロジー（洗浄チェーン/ハブ&スポーク/
//   オフショア・ファネル/キックバック・ループ/ポンジ再分配）に調律。
//
//   ※ すべての edge index は対応する nodes 配列内で有効であることを確認済み。
// =====================================================================

export const moneyFlowPresets = {
  // --- Laundering chains（単純な洗浄チェーン A→B→C） -------------------
  'chain-simple-abc': {
    nodes: [
      {x: 0.15, y: 0.5, label: 'Source'},
      {x: 0.5, y: 0.5, label: 'Shell Co'},
      {x: 0.85, y: 0.5, label: 'Offshore'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2.4},
      {from: 1, to: 2, weight: 2.4},
    ],
  },
  'chain-four-stage': {
    nodes: [
      {x: 0.12, y: 0.6, label: 'Dirty Cash'},
      {x: 0.38, y: 0.4, label: 'Front Business'},
      {x: 0.64, y: 0.6, label: 'Shell Co'},
      {x: 0.88, y: 0.4, label: 'Clean Account'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2.2},
      {from: 1, to: 2, weight: 2},
      {from: 2, to: 3, weight: 1.8},
    ],
  },
  'chain-placement-layering-integration': {
    nodes: [
      {x: 0.1, y: 0.5, label: 'Cash'},
      {x: 0.31, y: 0.3, label: 'Casino'},
      {x: 0.52, y: 0.62, label: 'Broker'},
      {x: 0.74, y: 0.32, label: 'Shell Co'},
      {x: 0.92, y: 0.58, label: 'Clean Fund'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2.6},
      {from: 1, to: 2, weight: 2.2},
      {from: 2, to: 3, weight: 1.9},
      {from: 3, to: 4, weight: 1.6},
    ],
  },
  'chain-wire-relay': {
    nodes: [
      {x: 0.16, y: 0.32, label: 'Payer'},
      {x: 0.42, y: 0.58, label: 'Bank'},
      {x: 0.68, y: 0.34, label: 'Intermediary'},
      {x: 0.9, y: 0.6, label: 'Beneficiary'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2},
      {from: 1, to: 2, weight: 2},
      {from: 2, to: 3, weight: 2},
    ],
  },

  // --- Hub & spoke（一つの源泉から複数のシェルへ） --------------------
  'hub-one-to-many-shells': {
    nodes: [
      {x: 0.16, y: 0.5, label: 'Fund'},
      {x: 0.72, y: 0.16, label: 'Shell A'},
      {x: 0.84, y: 0.38, label: 'Shell B'},
      {x: 0.84, y: 0.62, label: 'Shell C'},
      {x: 0.72, y: 0.84, label: 'Shell D'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.4},
      {from: 0, to: 2, weight: 1.8},
      {from: 0, to: 3, weight: 1.6},
      {from: 0, to: 4, weight: 1.2},
    ],
  },
  'hub-payout-fan': {
    nodes: [
      {x: 0.15, y: 0.5, label: 'Fund'},
      {x: 0.7, y: 0.2, label: 'Payout'},
      {x: 0.82, y: 0.4, label: 'Payout'},
      {x: 0.82, y: 0.6, label: 'Payout'},
      {x: 0.7, y: 0.8, label: 'Payout'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.3},
      {from: 0, to: 2, weight: 1.3},
      {from: 0, to: 3, weight: 1.3},
      {from: 0, to: 4, weight: 1.3},
    ],
  },
  'hub-collector-fan-in': {
    nodes: [
      {x: 0.15, y: 0.18, label: 'Investors'},
      {x: 0.15, y: 0.4, label: 'Investors'},
      {x: 0.15, y: 0.62, label: 'Investors'},
      {x: 0.15, y: 0.84, label: 'Investors'},
      {x: 0.82, y: 0.5, label: 'Collector'},
    ],
    edges: [
      {from: 0, to: 4, weight: 1.5},
      {from: 1, to: 4, weight: 1.7},
      {from: 2, to: 4, weight: 1.6},
      {from: 3, to: 4, weight: 1.4},
    ],
  },
  'hub-source-six-shells': {
    nodes: [
      {x: 0.13, y: 0.5, label: 'Source'},
      {x: 0.68, y: 0.14, label: 'Shell'},
      {x: 0.85, y: 0.3, label: 'Shell'},
      {x: 0.9, y: 0.5, label: 'Shell'},
      {x: 0.85, y: 0.7, label: 'Shell'},
      {x: 0.68, y: 0.86, label: 'Shell'},
      {x: 0.5, y: 0.5, label: 'Broker'},
    ],
    edges: [
      {from: 0, to: 6, weight: 3},
      {from: 6, to: 1, weight: 1.2},
      {from: 6, to: 2, weight: 1.4},
      {from: 6, to: 3, weight: 1.6},
      {from: 6, to: 4, weight: 1.3},
      {from: 6, to: 5, weight: 1.1},
    ],
  },

  // --- Layered offshore funnel（多層オフショア・ファネル） -------------
  'funnel-narrowing-vault': {
    nodes: [
      {x: 0.12, y: 0.2, label: 'Investors'},
      {x: 0.12, y: 0.5, label: 'Investors'},
      {x: 0.12, y: 0.8, label: 'Investors'},
      {x: 0.46, y: 0.34, label: 'Broker'},
      {x: 0.46, y: 0.66, label: 'Broker'},
      {x: 0.86, y: 0.5, label: 'Vault'},
    ],
    edges: [
      {from: 0, to: 3, weight: 1.4},
      {from: 1, to: 3, weight: 1.6},
      {from: 2, to: 4, weight: 1.5},
      {from: 3, to: 5, weight: 2.4},
      {from: 4, to: 5, weight: 2},
    ],
  },
  'funnel-three-tier': {
    nodes: [
      {x: 0.12, y: 0.3, label: 'Source'},
      {x: 0.12, y: 0.7, label: 'Source'},
      {x: 0.44, y: 0.5, label: 'Fund'},
      {x: 0.68, y: 0.5, label: 'Shell Co'},
      {x: 0.9, y: 0.5, label: 'Offshore'},
    ],
    edges: [
      {from: 0, to: 2, weight: 1.7},
      {from: 1, to: 2, weight: 1.7},
      {from: 2, to: 3, weight: 2.6},
      {from: 3, to: 4, weight: 2.2},
    ],
  },
  'funnel-offshore-cascade': {
    nodes: [
      {x: 0.1, y: 0.5, label: 'Cash'},
      {x: 0.35, y: 0.28, label: 'Shell A'},
      {x: 0.35, y: 0.72, label: 'Shell B'},
      {x: 0.63, y: 0.5, label: 'Offshore'},
      {x: 0.9, y: 0.5, label: 'Vault'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.6},
      {from: 0, to: 2, weight: 1.6},
      {from: 1, to: 3, weight: 1.7},
      {from: 2, to: 3, weight: 1.7},
      {from: 3, to: 4, weight: 2.8},
    ],
  },
  'funnel-shell-web': {
    nodes: [
      {x: 0.12, y: 0.5, label: 'Source'},
      {x: 0.4, y: 0.28, label: 'Shell A'},
      {x: 0.4, y: 0.72, label: 'Shell B'},
      {x: 0.66, y: 0.5, label: 'Shell C'},
      {x: 0.9, y: 0.5, label: 'Offshore'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.8},
      {from: 0, to: 2, weight: 1.8},
      {from: 1, to: 2, weight: 0.9},
      {from: 1, to: 3, weight: 1.5},
      {from: 2, to: 3, weight: 1.5},
      {from: 3, to: 4, weight: 2.6},
    ],
  },

  // --- Kickback loops（キックバック・ループ） --------------------------
  'kickback-loop-three': {
    nodes: [
      {x: 0.25, y: 0.28, label: 'Contractor'},
      {x: 0.78, y: 0.5, label: 'Shell Co'},
      {x: 0.25, y: 0.78, label: 'Official'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2},
      {from: 1, to: 2, weight: 1.6},
      {from: 2, to: 0, weight: 2.4},
    ],
  },
  'kickback-bribe-triangle': {
    nodes: [
      {x: 0.2, y: 0.34, label: 'Vendor'},
      {x: 0.8, y: 0.34, label: 'Middleman'},
      {x: 0.5, y: 0.82, label: 'Official'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.8},
      {from: 1, to: 2, weight: 1.4},
      {from: 2, to: 0, weight: 2.2},
    ],
  },
  'kickback-procurement-ring': {
    nodes: [
      {x: 0.5, y: 0.14, label: 'Agency'},
      {x: 0.86, y: 0.5, label: 'Contractor'},
      {x: 0.5, y: 0.86, label: 'Shell Co'},
      {x: 0.14, y: 0.5, label: 'Official'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2.4},
      {from: 1, to: 2, weight: 1.8},
      {from: 2, to: 3, weight: 1.5},
      {from: 3, to: 0, weight: 1.3},
    ],
  },

  // --- Ponzi redistribution（ポンジ再分配） ---------------------------
  'ponzi-redistribution': {
    nodes: [
      {x: 0.14, y: 0.5, label: 'New Investors'},
      {x: 0.46, y: 0.5, label: 'Fund'},
      {x: 0.8, y: 0.28, label: 'Payouts'},
      {x: 0.8, y: 0.72, label: 'Founder'},
    ],
    edges: [
      {from: 0, to: 1, weight: 3},
      {from: 1, to: 2, weight: 1.8},
      {from: 1, to: 3, weight: 1.1},
    ],
  },
  'ponzi-feeder-funds': {
    nodes: [
      {x: 0.12, y: 0.24, label: 'Feeder Fund'},
      {x: 0.12, y: 0.5, label: 'Feeder Fund'},
      {x: 0.12, y: 0.76, label: 'Feeder Fund'},
      {x: 0.5, y: 0.5, label: 'Fund'},
      {x: 0.86, y: 0.5, label: 'Founder'},
    ],
    edges: [
      {from: 0, to: 3, weight: 1.5},
      {from: 1, to: 3, weight: 1.7},
      {from: 2, to: 3, weight: 1.4},
      {from: 3, to: 4, weight: 3},
    ],
  },
  'ponzi-rob-peter-pay-paul': {
    nodes: [
      {x: 0.15, y: 0.3, label: 'New Investors'},
      {x: 0.5, y: 0.5, label: 'Fund'},
      {x: 0.85, y: 0.3, label: 'Old Investors'},
      {x: 0.85, y: 0.72, label: 'Founder'},
    ],
    edges: [
      {from: 0, to: 1, weight: 3},
      {from: 1, to: 2, weight: 2},
      {from: 1, to: 3, weight: 1.2},
    ],
  },

  // --- Advanced layering（構造化・ミキシング・環流） -------------------
  'smurfing-structured-deposits': {
    nodes: [
      {x: 0.12, y: 0.5, label: 'Cash'},
      {x: 0.42, y: 0.18, label: 'Deposit'},
      {x: 0.42, y: 0.39, label: 'Deposit'},
      {x: 0.42, y: 0.61, label: 'Deposit'},
      {x: 0.42, y: 0.82, label: 'Deposit'},
      {x: 0.86, y: 0.5, label: 'Account'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1},
      {from: 0, to: 2, weight: 1},
      {from: 0, to: 3, weight: 1},
      {from: 0, to: 4, weight: 1},
      {from: 1, to: 5, weight: 1},
      {from: 2, to: 5, weight: 1},
      {from: 3, to: 5, weight: 1},
      {from: 4, to: 5, weight: 1},
    ],
  },
  'mule-network-relay': {
    nodes: [
      {x: 0.12, y: 0.5, label: 'Source'},
      {x: 0.44, y: 0.25, label: 'Money Mule'},
      {x: 0.44, y: 0.5, label: 'Money Mule'},
      {x: 0.44, y: 0.75, label: 'Money Mule'},
      {x: 0.86, y: 0.5, label: 'Collector'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.3},
      {from: 0, to: 2, weight: 1.3},
      {from: 0, to: 3, weight: 1.3},
      {from: 1, to: 4, weight: 1.3},
      {from: 2, to: 4, weight: 1.3},
      {from: 3, to: 4, weight: 1.3},
    ],
  },
  'crypto-mixer-tumble': {
    nodes: [
      {x: 0.12, y: 0.3, label: 'Wallet'},
      {x: 0.12, y: 0.7, label: 'Wallet'},
      {x: 0.5, y: 0.5, label: 'Mixer'},
      {x: 0.88, y: 0.24, label: 'Exit'},
      {x: 0.88, y: 0.5, label: 'Exit'},
      {x: 0.88, y: 0.76, label: 'Exit'},
    ],
    edges: [
      {from: 0, to: 2, weight: 2},
      {from: 1, to: 2, weight: 2},
      {from: 2, to: 3, weight: 1.3},
      {from: 2, to: 4, weight: 1.3},
      {from: 2, to: 5, weight: 1.3},
    ],
  },
  'round-tripping-loop': {
    nodes: [
      {x: 0.22, y: 0.4, label: 'Company'},
      {x: 0.78, y: 0.4, label: 'Offshore'},
      {x: 0.5, y: 0.82, label: 'Shell Co'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2.2},
      {from: 1, to: 2, weight: 2},
      {from: 2, to: 0, weight: 2.2},
    ],
  },
  'correspondent-bank-chain': {
    nodes: [
      {x: 0.12, y: 0.6, label: 'Origin Bank'},
      {x: 0.37, y: 0.4, label: 'Bank'},
      {x: 0.62, y: 0.6, label: 'Bank'},
      {x: 0.88, y: 0.4, label: 'Beneficiary'},
    ],
    edges: [
      {from: 0, to: 1, weight: 2},
      {from: 1, to: 2, weight: 2},
      {from: 2, to: 3, weight: 2},
    ],
  },
  'trade-based-layering': {
    nodes: [
      {x: 0.1, y: 0.5, label: 'Exporter'},
      {x: 0.33, y: 0.3, label: 'Freight'},
      {x: 0.56, y: 0.62, label: 'Importer'},
      {x: 0.78, y: 0.34, label: 'Shell Co'},
      {x: 0.92, y: 0.62, label: 'Offshore'},
    ],
    edges: [
      {from: 0, to: 1, weight: 1.8},
      {from: 1, to: 2, weight: 1.8},
      {from: 2, to: 3, weight: 1.6},
      {from: 3, to: 4, weight: 2},
    ],
  },
} satisfies Record<string, ComponentProps<typeof MoneyFlow>>;
