import type {ComponentProps} from 'react';
import type {RouteMap} from '../RouteMap';

// =====================================================================
// RouteMap — PRESET CATALOG (MOTIONKIT)
//   決定論的な発光ルートマップ。pins は {x, y, label?} を 0..1 正規化座標で
//   与える（x=左→右, y=上→下）。ラベルは総称語のみ（実在ロゴ/実名なし）。
//   dur はコンポジション既定尺を使う場合は設定しない（指示準拠）。
//   PD向けドキュメンタリーの典型ルート（逃走/資金追跡/密輸/追跡）に調律。
// =====================================================================

export const routeMapPresets = {
  // --- Escape & flight（逃走・逃亡ルート） -----------------------------
  'escape-two-stop': {
    pins: [
      {x: 0.22, y: 0.68, label: 'Scene'},
      {x: 0.5, y: 0.52, label: 'Safe house'},
      {x: 0.8, y: 0.34, label: 'Border'},
    ],
  },
  'escape-getaway-car': {
    pins: [
      {x: 0.16, y: 0.4, label: 'Bank'},
      {x: 0.38, y: 0.62, label: 'Switch point'},
      {x: 0.64, y: 0.5, label: 'Hideout'},
    ],
  },
  'escape-prison-break': {
    pins: [
      {x: 0.28, y: 0.3, label: 'Prison'},
      {x: 0.44, y: 0.58, label: 'Tree line'},
      {x: 0.66, y: 0.44, label: 'River'},
      {x: 0.84, y: 0.66, label: 'Freedom'},
    ],
  },
  'escape-night-run': {
    pins: [
      {x: 0.2, y: 0.72, label: 'Apartment'},
      {x: 0.5, y: 0.44, label: 'Train station'},
      {x: 0.82, y: 0.28, label: 'Coast'},
    ],
  },

  // --- Manhunt & pursuit（追跡・手配） ---------------------------------
  'manhunt-cross-country': {
    pins: [
      {x: 0.14, y: 0.34, label: 'Last seen'},
      {x: 0.34, y: 0.56, label: 'Sighting'},
      {x: 0.56, y: 0.4, label: 'Roadblock'},
      {x: 0.74, y: 0.62, label: 'Motel'},
      {x: 0.9, y: 0.42, label: 'Capture'},
    ],
  },
  'manhunt-fugitive-arc': {
    pins: [
      {x: 0.12, y: 0.7, label: 'Home town'},
      {x: 0.4, y: 0.5, label: 'Alias city'},
      {x: 0.7, y: 0.66, label: 'Tip line'},
      {x: 0.88, y: 0.5, label: 'Arrest'},
    ],
  },
  'manhunt-border-chase': {
    pins: [
      {x: 0.18, y: 0.5, label: 'Checkpoint'},
      {x: 0.46, y: 0.34, label: 'Desert road'},
      {x: 0.78, y: 0.46, label: 'Border town'},
    ],
  },

  // --- Money trail & finance（資金の流れ） -----------------------------
  'money-three-city': {
    pins: [
      {x: 0.18, y: 0.62, label: 'Bank HQ'},
      {x: 0.5, y: 0.38, label: 'Shell company'},
      {x: 0.82, y: 0.6, label: 'Offshore'},
    ],
  },
  'money-laundering-loop': {
    pins: [
      {x: 0.2, y: 0.5, label: 'Cash'},
      {x: 0.42, y: 0.3, label: 'Casino'},
      {x: 0.64, y: 0.52, label: 'Front business'},
      {x: 0.84, y: 0.34, label: 'Clean account'},
    ],
  },
  'money-offshore-hop': {
    pins: [
      {x: 0.14, y: 0.44, label: 'Investor'},
      {x: 0.38, y: 0.62, label: 'Broker'},
      {x: 0.62, y: 0.4, label: 'Tax haven'},
      {x: 0.86, y: 0.58, label: 'Vault'},
    ],
  },
  'money-wire-transfer': {
    pins: [
      {x: 0.22, y: 0.36, label: 'Payer'},
      {x: 0.52, y: 0.56, label: 'Intermediary'},
      {x: 0.8, y: 0.4, label: 'Beneficiary'},
    ],
  },
  'money-ponzi-flow': {
    pins: [
      {x: 0.16, y: 0.68, label: 'New investors'},
      {x: 0.44, y: 0.46, label: 'Fund'},
      {x: 0.68, y: 0.66, label: 'Payouts'},
      {x: 0.88, y: 0.44, label: 'Founder'},
    ],
  },

  // --- Smuggling & trafficking（密輸ルート） ---------------------------
  'smuggle-sea-route': {
    pins: [
      {x: 0.14, y: 0.58, label: 'Source port'},
      {x: 0.42, y: 0.72, label: 'Transit island'},
      {x: 0.72, y: 0.5, label: 'Drop point'},
      {x: 0.9, y: 0.36, label: 'Market'},
    ],
  },
  'smuggle-overland': {
    pins: [
      {x: 0.16, y: 0.44, label: 'Farm'},
      {x: 0.4, y: 0.58, label: 'Warehouse'},
      {x: 0.66, y: 0.4, label: 'Border crossing'},
      {x: 0.86, y: 0.56, label: 'Distribution'},
    ],
  },
  'smuggle-air-corridor': {
    pins: [
      {x: 0.2, y: 0.66, label: 'Airstrip'},
      {x: 0.54, y: 0.34, label: 'Refuel stop'},
      {x: 0.84, y: 0.62, label: 'Landing'},
    ],
  },
  'smuggle-supply-chain': {
    pins: [
      {x: 0.12, y: 0.5, label: 'Origin'},
      {x: 0.32, y: 0.66, label: 'Broker'},
      {x: 0.52, y: 0.4, label: 'Free port'},
      {x: 0.72, y: 0.6, label: 'Buyer'},
      {x: 0.9, y: 0.44, label: 'Street'},
    ],
  },

  // --- Investigation & evidence（捜査・証拠の地理） --------------------
  'investigation-crime-scene': {
    pins: [
      {x: 0.24, y: 0.6, label: 'Body found'},
      {x: 0.5, y: 0.42, label: 'Suspect home'},
      {x: 0.76, y: 0.58, label: 'Evidence'},
    ],
  },
  'investigation-witness-map': {
    pins: [
      {x: 0.18, y: 0.38, label: 'Witness A'},
      {x: 0.46, y: 0.62, label: 'Witness B'},
      {x: 0.72, y: 0.36, label: 'Witness C'},
      {x: 0.88, y: 0.6, label: 'Crime scene'},
    ],
  },
  'investigation-cell-ping': {
    pins: [
      {x: 0.2, y: 0.5, label: 'Tower 1'},
      {x: 0.42, y: 0.34, label: 'Tower 2'},
      {x: 0.62, y: 0.56, label: 'Tower 3'},
      {x: 0.84, y: 0.4, label: 'Last ping'},
    ],
  },

  // --- Journey & expedition（移動・旅程） ------------------------------
  'journey-immigrant-route': {
    pins: [
      {x: 0.12, y: 0.62, label: 'Homeland'},
      {x: 0.36, y: 0.44, label: 'Transit camp'},
      {x: 0.62, y: 0.58, label: 'Port of entry'},
      {x: 0.88, y: 0.4, label: 'New home'},
    ],
  },
  'journey-expedition-line': {
    pins: [
      {x: 0.16, y: 0.7, label: 'Base camp'},
      {x: 0.4, y: 0.5, label: 'Ridge'},
      {x: 0.62, y: 0.34, label: 'High camp'},
      {x: 0.82, y: 0.2, label: 'Summit'},
    ],
  },
  'journey-shipwreck-drift': {
    pins: [
      {x: 0.2, y: 0.3, label: 'Departure'},
      {x: 0.5, y: 0.5, label: 'Storm'},
      {x: 0.7, y: 0.68, label: 'Wreck site'},
      {x: 0.88, y: 0.5, label: 'Rescue'},
    ],
  },

  // --- Conspiracy & network（人物ネットワークの地理） ------------------
  'network-cartel-chain': {
    pins: [
      {x: 0.14, y: 0.5, label: 'Boss'},
      {x: 0.38, y: 0.68, label: 'Lieutenant'},
      {x: 0.62, y: 0.44, label: 'Cell'},
      {x: 0.86, y: 0.62, label: 'Buyer'},
    ],
  },
  'network-spy-dead-drop': {
    pins: [
      {x: 0.22, y: 0.4, label: 'Embassy'},
      {x: 0.48, y: 0.6, label: 'Dead drop'},
      {x: 0.74, y: 0.42, label: 'Handler'},
    ],
  },
  'network-heist-crew': {
    pins: [
      {x: 0.18, y: 0.64, label: 'Meet point'},
      {x: 0.42, y: 0.42, label: 'Vault'},
      {x: 0.64, y: 0.6, label: 'Switch'},
      {x: 0.86, y: 0.38, label: 'Split'},
    ],
  },
} satisfies Record<string, ComponentProps<typeof RouteMap>>;
