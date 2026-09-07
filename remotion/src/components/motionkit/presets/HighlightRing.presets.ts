import type {ComponentProps} from 'react';
import type {HighlightRing} from '../HighlightRing';

/**
 * Ready-made prop fills for HighlightRing.
 * cx/cy/r are 0..1 fractions of the frame (cx=0 left, cy=0 top). r is a
 * fraction of frame WIDTH (kept within ~0.05..0.35). Usage:
 *   <HighlightRing {...highlightRingPresets['key']} />
 */
export const highlightRingPresets = {
  // ── Center framings ──────────────────────────────────────────────
  'center-tight': {cx: 0.5, cy: 0.5, r: 0.09, label: 'the key detail'},
  'center-medium': {cx: 0.5, cy: 0.5, r: 0.16, label: 'the whole picture'},
  'center-wide': {cx: 0.5, cy: 0.5, r: 0.26, label: 'the scene'},
  'center-hero': {cx: 0.5, cy: 0.46, r: 0.2, label: 'the subject'},

  // ── Rule-of-thirds points ────────────────────────────────────────
  'thirds-top-left': {cx: 0.333, cy: 0.333, r: 0.12, label: 'the witness'},
  'thirds-top-right': {cx: 0.667, cy: 0.333, r: 0.12, label: 'the second shooter'},
  'thirds-bottom-left': {cx: 0.333, cy: 0.667, r: 0.12, label: 'the accomplice'},
  'thirds-bottom-right': {cx: 0.667, cy: 0.667, r: 0.12, label: 'the getaway car'},

  // ── Faces / people area (upper-center, portrait crop) ────────────
  'face-center': {cx: 0.5, cy: 0.36, r: 0.11, label: 'the defendant'},
  'face-left': {cx: 0.37, cy: 0.38, r: 0.1, label: 'the informant'},
  'face-right': {cx: 0.63, cy: 0.38, r: 0.1, label: 'the mastermind'},
  'face-tight': {cx: 0.5, cy: 0.34, r: 0.07, label: 'the tell'},
  'crowd-single-face': {cx: 0.58, cy: 0.42, r: 0.06, label: 'the only witness'},

  // ── Document corners & fields ────────────────────────────────────
  'doc-signature': {cx: 0.68, cy: 0.78, r: 0.1, label: 'the signature'},
  'doc-corner-tl': {cx: 0.28, cy: 0.26, r: 0.08, label: 'the letterhead'},
  'doc-corner-br': {cx: 0.74, cy: 0.76, r: 0.09, label: 'the date stamp'},
  'doc-fine-print': {cx: 0.5, cy: 0.82, r: 0.13, label: 'the hidden clause'},
  'doc-figure': {cx: 0.62, cy: 0.5, r: 0.09, label: 'the missing millions'},
  'doc-redaction': {cx: 0.44, cy: 0.55, r: 0.08, label: 'the redacted name'},

  // ── Screen / timestamp / evidence corners ────────────────────────
  'timestamp': {cx: 0.83, cy: 0.11, r: 0.07, label: 'the timestamp'},
  'ticker-corner': {cx: 0.16, cy: 0.88, r: 0.08, label: 'the ticker'},
  'evidence-tag': {cx: 0.8, cy: 0.7, r: 0.09, label: 'exhibit A'},

  // ── Wide framings / whole zones ──────────────────────────────────
  'upper-band': {cx: 0.5, cy: 0.24, r: 0.22, label: 'the headline'},
  'lower-band': {cx: 0.5, cy: 0.74, r: 0.22, label: 'the fine print'},
  'establishing-wide': {cx: 0.5, cy: 0.5, r: 0.32, label: 'the crime scene'},
} satisfies Record<string, ComponentProps<typeof HighlightRing>>;
