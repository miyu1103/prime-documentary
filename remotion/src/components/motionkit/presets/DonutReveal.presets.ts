import type {ComponentProps} from 'react';
import type {DonutReveal} from '../DonutReveal';

// =====================================================================
// DonutReveal — PRESET CATALOG for Prime Documentary.
//   割合の内訳（お金の行き先・票のシェア・予算配分・時間配分・結末分布）を
//   汎用ラベルで供給。値はリアルな比率、スライスは2〜5枚。
//   accent は BRAND トークンのみ（electric #1F6BFF / gold #E5B53A /
//   silver #C8CDD6 / white #F5F7FA）。デフォルト配色でも成立するよう、
//   accent は「特定スライスを主役に立てたい」時だけ上書き。
//   dur は既定（durationInFrames）に任せ、明示指定はしない。
// =====================================================================

const ELECTRIC = '#1F6BFF';
const GOLD = '#E5B53A';
const SILVER = '#C8CDD6';
const WHITE = '#F5F7FA';

export const donutRevealPresets = {
  // ---------------------------------------------------------------
  // Where the money went — 資金の行き先・使途の内訳
  // ---------------------------------------------------------------
  'money-where-it-went': {
    slices: [
      {label: 'Personal Luxury', value: 41},
      {label: 'Repaid Earlier Investors', value: 34},
      {label: 'Legal & PR', value: 16},
      {label: 'Actual Operations', value: 9},
    ],
    centerLabel: 'The Trail',
  },
  'money-three-way-split': {
    slices: [
      {label: 'Diverted', value: 58, accent: GOLD},
      {label: 'Recovered', value: 27},
      {label: 'Never Traced', value: 15},
    ],
    centerLabel: 'Follow It',
  },
  'money-vanished-vs-recovered': {
    slices: [
      {label: 'Vanished', value: 71, accent: GOLD},
      {label: 'Clawed Back', value: 29},
    ],
    centerLabel: 'The Gap',
  },
  'money-offshore-flow': {
    slices: [
      {label: 'Offshore Shells', value: 47},
      {label: 'Front Companies', value: 28},
      {label: 'Real Estate', value: 16},
      {label: 'Cash Withdrawn', value: 9},
    ],
    centerLabel: 'Laundered',
  },

  // ---------------------------------------------------------------
  // Votes share — 票のシェア・評決・審議の割れ方
  // ---------------------------------------------------------------
  'votes-narrow-majority': {
    slices: [
      {label: 'Majority', value: 54, accent: ELECTRIC},
      {label: 'Dissent', value: 46},
    ],
    centerLabel: 'The Ruling',
  },
  'votes-supreme-court-5-4': {
    slices: [
      {label: 'For', value: 5, accent: ELECTRIC},
      {label: 'Against', value: 4},
    ],
    centerLabel: '5–4',
  },
  'votes-three-camps': {
    slices: [
      {label: 'Convict', value: 43},
      {label: 'Acquit', value: 39},
      {label: 'Undecided', value: 18},
    ],
    centerLabel: 'The Jury',
  },
  'votes-landslide': {
    slices: [
      {label: 'Prevailing', value: 78, accent: ELECTRIC},
      {label: 'Opposed', value: 22},
    ],
    centerLabel: 'The Verdict',
  },
  'votes-board-decision': {
    slices: [
      {label: 'Approved Merger', value: 61},
      {label: 'Voted No', value: 31},
      {label: 'Abstained', value: 8},
    ],
    centerLabel: 'The Board',
  },

  // ---------------------------------------------------------------
  // Budget split — 予算配分・費用の内訳
  // ---------------------------------------------------------------
  'budget-production-split': {
    slices: [
      {label: 'Marketing', value: 46},
      {label: 'Product', value: 24},
      {label: 'Overhead', value: 19},
      {label: 'Reserve', value: 11},
    ],
    centerLabel: 'The Budget',
  },
  'budget-marketing-heavy': {
    slices: [
      {label: 'Advertising', value: 63, accent: GOLD},
      {label: 'Everything Else', value: 37},
    ],
    centerLabel: 'The Spend',
  },
  'budget-legal-defense': {
    slices: [
      {label: 'Attorneys', value: 52},
      {label: 'Experts', value: 23},
      {label: 'Investigators', value: 15},
      {label: 'Filings', value: 10},
    ],
    centerLabel: 'The Defense',
  },
  'budget-four-departments': {
    slices: [
      {label: 'Engineering', value: 38},
      {label: 'Sales', value: 27},
      {label: 'Support', value: 21},
      {label: 'Admin', value: 14},
    ],
    centerLabel: 'Allocation',
  },
  'budget-rd-vs-hype': {
    slices: [
      {label: 'Publicity', value: 68, accent: GOLD},
      {label: 'Research', value: 32, accent: ELECTRIC},
    ],
    centerLabel: 'The Priority',
  },

  // ---------------------------------------------------------------
  // Time allocation — 時間配分・工程の割合
  // ---------------------------------------------------------------
  'time-investigation-phases': {
    slices: [
      {label: 'Surveillance', value: 44},
      {label: 'Interviews', value: 29},
      {label: 'Forensics', value: 27},
    ],
    centerLabel: 'The Timeline',
  },
  'time-trial-days': {
    slices: [
      {label: 'Prosecution', value: 55},
      {label: 'Defense', value: 34},
      {label: 'Deliberation', value: 11},
    ],
    centerLabel: 'In Court',
  },
  'time-decade-long': {
    slices: [
      {label: 'The Scheme', value: 62},
      {label: 'The Unraveling', value: 24},
      {label: 'The Reckoning', value: 14},
    ],
    centerLabel: 'A Decade',
  },
  'time-daily-routine': {
    slices: [
      {label: 'On the Con', value: 47},
      {label: 'Covering Tracks', value: 33},
      {label: 'Living Large', value: 20, accent: GOLD},
    ],
    centerLabel: 'His Day',
  },
  'time-two-thirds-waiting': {
    slices: [
      {label: 'Appeals', value: 67},
      {label: 'The Original Trial', value: 33},
    ],
    centerLabel: '30 Years',
  },

  // ---------------------------------------------------------------
  // Outcome distribution — 結末・被害・回収の分布
  // ---------------------------------------------------------------
  'outcome-victims-recovery': {
    slices: [
      {label: 'Lost Everything', value: 64},
      {label: 'Partial Recovery', value: 26},
      {label: 'Made Whole', value: 10, accent: ELECTRIC},
    ],
    centerLabel: 'The Investors',
  },
  'outcome-guilty-plea-split': {
    slices: [
      {label: 'Pleaded Guilty', value: 72},
      {label: 'Went to Trial', value: 19},
      {label: 'Charges Dropped', value: 9},
    ],
    centerLabel: 'Defendants',
  },
  'outcome-convicted-vs-free': {
    slices: [
      {label: 'Convicted', value: 38, accent: ELECTRIC},
      {label: 'Walked Free', value: 62},
    ],
    centerLabel: 'The Odds',
  },
  'outcome-sentence-breakdown': {
    slices: [
      {label: 'Served Full Term', value: 49},
      {label: 'Early Release', value: 33},
      {label: 'Overturned', value: 18, accent: WHITE},
    ],
    centerLabel: 'The Sentence',
  },
  'outcome-two-way-fate': {
    slices: [
      {label: 'Exonerated', value: 44, accent: WHITE},
      {label: 'Still Imprisoned', value: 56, accent: SILVER},
    ],
    centerLabel: 'The Fate',
  },
  'outcome-whistleblower-effect': {
    slices: [
      {label: 'Ignored Warnings', value: 81},
      {label: 'Acted On', value: 19, accent: ELECTRIC},
    ],
    centerLabel: 'The Flags',
  },
} satisfies Record<string, ComponentProps<typeof DonutReveal>>;
