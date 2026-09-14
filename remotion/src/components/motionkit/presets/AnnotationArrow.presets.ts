import type {ComponentProps} from 'react';
import type {AnnotationArrow} from '../AnnotationArrow';

/**
 * Ready-made prop fills for AnnotationArrow (documentary overlay pointers).
 * `from`/`to` are [x, y] as 0..1 fractions of the frame; `from` is the tail
 * (where the label sits) and `to` is the arrowhead landing on the detail.
 * Usage: <AnnotationArrow {...annotationArrowPresets['key']} />
 */
export const annotationArrowPresets = {
  // ── Point from a label into a specific detail ────────────────────
  'here': {
    from: [0.28, 0.24],
    to: [0.5, 0.5],
    label: 'here',
  },
  'right-here': {
    from: [0.72, 0.28],
    to: [0.52, 0.52],
    label: 'right here',
  },
  'the-detail': {
    from: [0.24, 0.7],
    to: [0.46, 0.48],
    label: 'the detail',
  },
  'look-closer': {
    from: [0.76, 0.72],
    to: [0.54, 0.5],
    label: 'look closer',
  },
  'the-discrepancy': {
    from: [0.3, 0.78],
    to: [0.5, 0.56],
    label: 'the discrepancy',
  },
  'the-signature': {
    from: [0.68, 0.24],
    to: [0.5, 0.46],
    label: 'the signature',
  },

  // ── Follow-the-money / financial trail ───────────────────────────
  'follow-the-money': {
    from: [0.18, 0.5],
    to: [0.82, 0.5],
    label: 'follow the money',
  },
  'the-missing-millions': {
    from: [0.22, 0.28],
    to: [0.74, 0.62],
    label: 'the missing millions',
  },
  'offshore-account': {
    from: [0.7, 0.76],
    to: [0.3, 0.34],
    label: 'offshore account',
  },
  'the-payment': {
    from: [0.24, 0.66],
    to: [0.72, 0.4],
    label: 'the payment',
  },
  'shell-company': {
    from: [0.5, 0.2],
    to: [0.5, 0.62],
    label: 'shell company',
  },

  // ── Investigation / evidence pointers ────────────────────────────
  'the-evidence': {
    from: [0.3, 0.26],
    to: [0.52, 0.54],
    label: 'the evidence',
  },
  'entry-point': {
    from: [0.14, 0.3],
    to: [0.42, 0.58],
    label: 'entry point',
  },
  'the-witness': {
    from: [0.74, 0.32],
    to: [0.5, 0.5],
    label: 'the witness',
  },
  'the-timestamp': {
    from: [0.78, 0.82],
    to: [0.56, 0.6],
    label: 'the timestamp',
  },
  'first-clue': {
    from: [0.26, 0.74],
    to: [0.48, 0.5],
    label: 'first clue',
  },
  'the-contradiction': {
    from: [0.72, 0.7],
    to: [0.46, 0.44],
    label: 'the contradiction',
  },

  // ── Directional emphasis (no label — silent pointer) ─────────────
  'left-to-right': {
    from: [0.15, 0.5],
    to: [0.85, 0.5],
  },
  'right-to-left': {
    from: [0.85, 0.5],
    to: [0.15, 0.5],
  },
  'bottom-up': {
    from: [0.5, 0.85],
    to: [0.5, 0.28],
  },
  'top-down': {
    from: [0.5, 0.16],
    to: [0.5, 0.7],
  },
  'corner-to-center': {
    from: [0.14, 0.16],
    to: [0.5, 0.5],
  },
  'diagonal-rise': {
    from: [0.2, 0.82],
    to: [0.8, 0.24],
  },
  'diagonal-fall': {
    from: [0.2, 0.2],
    to: [0.8, 0.8],
  },

  // ── Narrative call-outs ──────────────────────────────────────────
  'this-changes-everything': {
    from: [0.3, 0.22],
    to: [0.5, 0.52],
    label: 'this changes everything',
  },
  'the-turning-point': {
    from: [0.7, 0.78],
    to: [0.48, 0.5],
    label: 'the turning point',
  },
  'watch-this': {
    from: [0.24, 0.3],
    to: [0.5, 0.5],
    label: 'watch this',
  },
} satisfies Record<string, ComponentProps<typeof AnnotationArrow>>;
