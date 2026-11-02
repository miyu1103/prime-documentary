import type {ComponentProps} from 'react';
import type {CinematicTitle} from '../CinematicTitle';

// =====================================================================
// CinematicTitle — PRESET CATALOG
//
// Hero title cards tuned to Prime Documentary's slate: landmark legal
// cases, financial fraud, true crime, and general investigative docs.
// Each entry is a top-tier documentary voice — a punchy display title
// paired with a promise-of-story subtitle.
//
// All titles/subtitles are original and evocative. NO real-person names,
// likeness, or real company/logo references. `dur` is intentionally
// omitted so each card inherits the composition duration.
//
// Usage:
//   <CinematicTitle {...cinematicTitlePresets['the-flash-crash']} />
// =====================================================================

export const cinematicTitlePresets = {
  // ---------------------------------------------------------------
  // Financial fraud & market collapse
  // ---------------------------------------------------------------
  'the-flash-crash': {
    title: 'THE FLASH CRASH',
    subtitle: 'How 36 minutes erased a trillion dollars',
  },
  'the-paper-empire': {
    title: 'THE PAPER EMPIRE',
    subtitle: 'A fortune that only existed on paper',
  },
  'the-ponzi-machine': {
    title: 'THE PONZI MACHINE',
    subtitle: 'The math that could never add up',
  },
  'the-vanishing-billions': {
    title: 'THE VANISHING BILLIONS',
    subtitle: 'Wired away before anyone noticed',
  },
  'the-house-of-cards': {
    title: 'HOUSE OF CARDS',
    subtitle: 'One bad quarter from total collapse',
  },
  'the-shell-game': {
    title: 'THE SHELL GAME',
    subtitle: 'A thousand companies, not one factory',
  },
  'the-audit': {
    title: 'THE AUDIT',
    subtitle: 'The morning the numbers stopped lying',
  },

  // ---------------------------------------------------------------
  // Landmark legal cases & courtroom
  // ---------------------------------------------------------------
  'the-verdict': {
    title: 'THE VERDICT',
    subtitle: 'Twelve strangers. One impossible decision.',
  },
  'the-right-to-remain': {
    title: 'THE RIGHT TO REMAIN',
    subtitle: 'The words that rewrote every arrest',
  },
  'the-fourth-amendment': {
    title: 'SEARCH & SEIZURE',
    subtitle: 'Where does the badge have to stop?',
  },
  'the-precedent': {
    title: 'THE PRECEDENT',
    subtitle: 'One ruling that changed the law forever',
  },
  'the-appeal': {
    title: 'THE FINAL APPEAL',
    subtitle: 'The last door before the last day',
  },
  'the-dissent': {
    title: 'THE DISSENT',
    subtitle: 'One judge who refused to sign',
  },
  'reasonable-doubt': {
    title: 'REASONABLE DOUBT',
    subtitle: 'The thinnest line in the law',
  },

  // ---------------------------------------------------------------
  // True crime & investigation
  // ---------------------------------------------------------------
  'the-cold-case': {
    title: 'THE COLD CASE',
    subtitle: 'Forty years. One overlooked detail.',
  },
  'the-perfect-alibi': {
    title: 'THE PERFECT ALIBI',
    subtitle: 'Everyone believed it. No one checked it.',
  },
  'the-confession': {
    title: 'THE CONFESSION',
    subtitle: 'The statement that never should have counted',
  },
  'the-wrong-man': {
    title: 'THE WRONG MAN',
    subtitle: 'Thirty years for a crime he never committed',
  },
  'the-vanishing': {
    title: 'THE VANISHING',
    subtitle: 'She left for work and never arrived',
  },
  'the-heist': {
    title: 'THE HEIST',
    subtitle: 'Gone in the dark, missing to this day',
  },
  'the-witness': {
    title: 'THE ONLY WITNESS',
    subtitle: 'What one memory got dangerously wrong',
  },

  // ---------------------------------------------------------------
  // General investigative / documentary
  // ---------------------------------------------------------------
  'the-whistleblower': {
    title: 'THE WHISTLEBLOWER',
    subtitle: 'The insider who chose to speak',
  },
  'the-experiment': {
    title: 'THE EXPERIMENT',
    subtitle: 'How far people go when told to obey',
  },
  'the-algorithm': {
    title: 'THE ALGORITHM',
    subtitle: 'The code that decided who to trust',
  },
  'the-recall': {
    title: 'THE RECALL',
    subtitle: 'They knew, and they shipped it anyway',
  },
  'the-breakthrough': {
    title: 'THE BREAKTHROUGH',
    subtitle: 'A cure too good to be true',
  },
} satisfies Record<string, ComponentProps<typeof CinematicTitle>>;
