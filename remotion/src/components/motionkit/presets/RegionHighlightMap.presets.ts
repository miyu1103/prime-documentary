import type {ComponentProps} from 'react';
import type {RegionHighlightMap} from '../RegionHighlightMap';

// =====================================================================
// RegionHighlightMap — PRESET CATALOG
//   様式化USセル地図の量産プリセット。PDの法律・政策テーマ向け。
//   pattern='varied'  : 州ごとに非一様に明滅＝「住む場所で変わる／未確定／分裂」
//   pattern='uniform' : 全セル一斉点灯＝「全国一律／連邦法／どこでも同じ」
//   label は地図下部にマスク切り上がりで出る短句（英大文字化される）。
//   dur は指定しない（Composition の durationInFrames を継承）。
// =====================================================================

export const regionHighlightMapPresets = {
  // --- It depends on your state（州次第・非一様） -----------------
  'depends-on-state': {label: 'It depends on your state', pattern: 'varied'},
  'varies-by-state': {label: 'Varies by state', pattern: 'varied'},
  'check-your-state': {label: 'Check your state', pattern: 'varied'},
  'where-you-live': {label: 'Where you live matters', pattern: 'varied'},
  'a-patchwork-of-laws': {label: 'A patchwork of laws', pattern: 'varied'},
  'no-uniform-rule': {label: 'No uniform rule', pattern: 'varied'},

  // --- Counts / how many states（州の数・非一様） ----------------
  'legal-in-12-states': {label: 'Legal in 12 states', pattern: 'varied'},
  'banned-in-19-states': {label: 'Banned in 19 states', pattern: 'varied'},
  'legal-in-half': {label: 'Legal in half the country', pattern: 'varied'},
  'thirty-eight-states': {label: '38 states and counting', pattern: 'varied'},
  'only-a-handful': {label: 'Only a handful allow it', pattern: 'varied'},

  // --- Split jurisdictions（分裂・非一様） ------------------------
  'split-jurisdictions': {label: 'Split jurisdictions', pattern: 'varied'},
  'a-divided-map': {label: 'A divided map', pattern: 'varied'},
  'states-disagree': {label: 'The states disagree', pattern: 'varied'},
  'red-states-blue-states': {label: 'Red states, blue states', pattern: 'varied'},
  'circuit-split': {label: 'A circuit split', pattern: 'varied'},

  // --- Undecided / shifting（未確定・非一様） ---------------------
  'the-law-is-unsettled': {label: 'The law is unsettled', pattern: 'varied'},
  'still-being-decided': {label: 'Still being decided', pattern: 'varied'},
  'a-legal-gray-area': {label: 'A legal gray area', pattern: 'varied'},

  // --- A national ban / uniform（全国一律・一斉） -----------------
  'a-national-ban': {label: 'A national ban', pattern: 'uniform'},
  'legal-nationwide': {label: 'Legal nationwide', pattern: 'uniform'},
  'one-federal-law': {label: 'One federal law', pattern: 'uniform'},
  'the-law-of-the-land': {label: 'The law of the land', pattern: 'uniform'},
  'coast-to-coast': {label: 'Coast to coast', pattern: 'uniform'},
  'a-single-standard': {label: 'A single standard', pattern: 'uniform'},

  // --- No label（地図だけ・トランジション用の下地） ---------------
  'ambient-varied': {pattern: 'varied'},
  'ambient-uniform': {pattern: 'uniform'},
} satisfies Record<string, ComponentProps<typeof RegionHighlightMap>>;
