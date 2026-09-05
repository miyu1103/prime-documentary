import type {ComponentProps} from 'react';
import type {CountdownClock} from '../CountdownClock';

// =====================================================================
// MOTIONKIT — CountdownClock PRESETS (Prime Documentary)
//   時間切迫を煽る mm:ss カウントダウンのシーン別カタログ。
//   すべて CountdownClock の props 型に厳密適合。
//   props: from(必須・残り秒) / label?(上部に切れ上がり表示) / dur?(尺フレーム)
//   ・from は「秒」。残り約5秒で色が赤へ移行し鼓動が二連打になる演出があるため、
//     短いカウント（10〜36秒）ほど終盤の緊張が濃く出る。
//   ・dur は意図的に未指定（Composition の durationInFrames をそのまま使い、
//     クリップ尺いっぱいでゼロへ着地させる）。長回しを詰めたい時だけ設定する。
//   ・label は大文字・字間広めで表示されるため短い英語フレーズにする。
//   使い方: <CountdownClock {...countdownClockPresets['flash-crash-36s']} />
// =====================================================================

export const countdownClockPresets = {
  // --- フラッシュ・クラッシュ / 市場崩壊（36秒の伝説を軸に） -----------
  'flash-crash-36s': {
    from: 36,
    label: 'TIME TO COLLAPSE',
  },
  'market-close-60s': {
    from: 60,
    label: 'BEFORE THE MARKET CLOSED',
  },
  'trillion-gone-30s': {
    from: 30,
    label: 'A TRILLION DOLLARS VANISHING',
  },
  'liquidity-drain-10s': {
    from: 10,
    label: 'LIQUIDITY GONE',
  },
  'circuit-breaker-90s': {
    from: 90,
    label: 'UNTIL THE CIRCUIT BREAKER',
  },

  // --- 締切 / 提出期限（Deadlines） ------------------------------------
  'deadline-60s': {
    from: 60,
    label: 'DEADLINE',
  },
  'filing-deadline-300s': {
    from: 300,
    label: 'BEFORE THE FILING DEADLINE',
  },
  'wire-cutoff-90s': {
    from: 90,
    label: 'BEFORE THE WIRE CUTOFF',
  },
  'application-closes-30s': {
    from: 30,
    label: 'APPLICATIONS CLOSE',
  },

  // --- 最後通牒 / 交渉（Ultimatums） -----------------------------------
  'ultimatum-60s': {
    from: 60,
    label: 'THE ULTIMATUM',
  },
  'final-offer-30s': {
    from: 30,
    label: 'FINAL OFFER',
  },
  'ransom-window-600s': {
    from: 600,
    label: 'TO PAY THE RANSOM',
  },
  'last-warning-10s': {
    from: 10,
    label: 'LAST WARNING',
  },

  // --- 陪審評議 / 法廷（Jury & courtroom） -----------------------------
  'jury-deliberation-600s': {
    from: 600,
    label: 'JURY STILL OUT',
  },
  'verdict-in-90s': {
    from: 90,
    label: 'BEFORE THE VERDICT',
  },
  'appeal-window-300s': {
    from: 300,
    label: 'THE APPEAL WINDOW',
  },
  'stay-of-execution-60s': {
    from: 60,
    label: 'STAY OF EXECUTION',
  },

  // --- 強盗 / 侵入の窓（Heist window） ---------------------------------
  'heist-window-90s': {
    from: 90,
    label: 'THE HEIST WINDOW',
  },
  'alarm-response-30s': {
    from: 30,
    label: 'BEFORE THE ALARM',
  },
  'vault-timer-600s': {
    from: 600,
    label: 'ON THE VAULT TIMER',
  },
  'getaway-10s': {
    from: 10,
    label: 'TO GET AWAY',
  },

  // --- 汎用カウントダウン（無地・尺合わせ用） --------------------------
  'generic-60s': {
    from: 60,
  },
  'generic-30s': {
    from: 30,
  },
  'generic-10s': {
    from: 10,
    label: 'TEN SECONDS',
  },
} satisfies Record<string, ComponentProps<typeof CountdownClock>>;
