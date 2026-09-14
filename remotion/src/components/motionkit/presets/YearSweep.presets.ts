import type {ComponentProps} from 'react';
import type {YearSweep} from '../YearSweep';

// =====================================================================
// MOTIONKIT — YearSweep PRESETS (Prime Documentary)
//   「時の経過」ヒーローシーンの使い回しカタログ。すべて YearSweep の
//   props 型に厳密適合。
//   props: from(必須・西暦) / to(必須・西暦) / label?(見出し) / dur?(尺)
//   ・from → to へ巨大年号がオドメーター式に転がる。span が数年なら短い
//     経過、数十年なら長い経過として読める。
//   ・label は大文字マスク切れ上がりの見出し（英語・簡潔に）。
//   ・dur は意図的に未指定（Composition の durationInFrames をそのまま
//     使う）。長い経過をゆっくり見せたい特別な場合のみ設定する。
//   使い方: <YearSweep {...yearSweepPresets['scheme-2001-2009']} />
// =====================================================================

export const yearSweepPresets = {
  // --- 詐欺スキームが走った年月（The scheme ran for years） -------------
  'scheme-2001-2009': {
    from: 2001,
    to: 2009,
    label: 'The scheme ran for years',
  },
  'ponzi-1992-2008': {
    from: 1992,
    to: 2008,
    label: 'Sixteen years of lies',
  },
  'fraud-2003-2015': {
    from: 2003,
    to: 2015,
    label: 'Twelve years unravel',
  },
  'onecoin-2014-2017': {
    from: 2014,
    to: 2017,
    label: 'Before she vanished',
  },
  'skimming-1998-2004': {
    from: 1998,
    to: 2004,
    label: 'Six years undetected',
  },

  // --- 会社の栄枯盛衰（From founding to collapse） ---------------------
  'rise-and-fall-2003-2018': {
    from: 2003,
    to: 2018,
    label: 'From founding to collapse',
  },
  'startup-decade-2009-2019': {
    from: 2009,
    to: 2019,
    label: "A company's rise and fall",
  },
  'boom-to-bust-2004-2014': {
    from: 2004,
    to: 2014,
    label: 'The rise-and-fall decade',
  },
  'ipo-to-bankruptcy-2011-2016': {
    from: 2011,
    to: 2016,
    label: 'From IPO to bankruptcy',
  },
  'peak-to-zero-2015-2018': {
    from: 2015,
    to: 2018,
    label: 'From peak to zero',
  },

  // --- 未解決事件・コールドケース（Decades cold） ---------------------
  'cold-case-1984-2014': {
    from: 1984,
    to: 2014,
    label: 'Decades cold',
  },
  'unsolved-1974-2005': {
    from: 1974,
    to: 2005,
    label: 'Thirty-one years unsolved',
  },
  'reopened-1991-2019': {
    from: 1991,
    to: 2019,
    label: 'The case reopened',
  },
  'dna-break-1988-2018': {
    from: 1988,
    to: 2018,
    label: 'Until the DNA matched',
  },
  'missing-1979-1996': {
    from: 1979,
    to: 1996,
    label: 'Seventeen years missing',
  },

  // --- 冤罪と釈放（Wrongfully imprisoned） ----------------------------
  'wrongful-1986-2016': {
    from: 1986,
    to: 2016,
    label: 'Thirty years behind bars',
  },
  'exoneration-1993-2013': {
    from: 1993,
    to: 2013,
    label: 'Twenty years to freedom',
  },
  'death-row-1985-2015': {
    from: 1985,
    to: 2015,
    label: 'An innocent man waits',
  },

  // --- 法廷・判例の時代（A legal precedent era） ----------------------
  'precedent-era-1966-1986': {
    from: 1966,
    to: 1986,
    label: 'A legal precedent era',
  },
  'landmark-1963-1972': {
    from: 1963,
    to: 1972,
    label: 'The law is rewritten',
  },
  'appeals-2001-2011': {
    from: 2001,
    to: 2011,
    label: 'A decade of appeals',
  },
  'privacy-era-2001-2018': {
    from: 2001,
    to: 2018,
    label: 'Privacy meets the digital age',
  },

  // --- 世代をまたぐ長い経過（Across the decades） --------------------
  'a-lifetime-1958-2008': {
    from: 1958,
    to: 2008,
    label: 'Half a century passes',
  },
  'generations-1929-1999': {
    from: 1929,
    to: 1999,
    label: 'Across the generations',
  },
} satisfies Record<string, ComponentProps<typeof YearSweep>>;
