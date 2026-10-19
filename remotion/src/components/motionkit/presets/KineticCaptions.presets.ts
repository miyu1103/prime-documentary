import type {ComponentProps} from 'react';
import type {KineticCaptions} from '../KineticCaptions';

/** Ready-made prop fills for KineticCaptions. Usage: <KineticCaptions {...kineticCaptionsPresets['key']} /> */
export const kineticCaptionsPresets = {
  // ── Supreme Court / legal cases ──────────────────────────────────
  'scotus-cert-granted': {
    lines: ['The nation waited', 'for one ruling'],
    style: 'emphasis',
    emphasisWords: ['one', 'ruling'],
  },
  'landmark-decision': {
    lines: ['A single decision', 'would rewrite the law'],
    style: 'emphasis',
    emphasisWords: ['single', 'law'],
  },
  'right-to-remain-silent': {
    lines: ['You have the right', 'to remain silent'],
    style: 'maskslide',
  },
  'oral-argument': {
    lines: ['Nine justices', 'one impossible question'],
    style: 'emphasis',
    emphasisWords: ['nine', 'impossible'],
  },
  'dissent-warning': {
    lines: ['In dissent', 'she saw the danger coming'],
    style: 'maskslide',
  },
  'constitutional-stakes': {
    lines: ['This was no longer', 'about one man'],
    style: 'emphasis',
    emphasisWords: ['one', 'man'],
  },
  'the-verdict': {
    lines: ['The verdict', 'changed everything'],
    style: 'wordpop',
    emphasisWords: ['verdict'],
  },
  'precedent-set': {
    lines: ['One case', 'became the rule', 'for every case after'],
    style: 'maskslide',
  },

  // ── Financial fraud ──────────────────────────────────────────────
  'billions-vanished': {
    lines: ['Billions of dollars', 'simply vanished'],
    style: 'emphasis',
    emphasisWords: ['billions', 'vanished'],
  },
  'house-of-cards': {
    lines: ['The numbers were perfect', 'because they were fake'],
    style: 'emphasis',
    emphasisWords: ['perfect', 'fake'],
  },
  'follow-the-money': {
    lines: ['Follow the money', 'and it disappears'],
    style: 'wordpop',
    emphasisWords: ['money'],
  },
  'investor-trust': {
    lines: ['They trusted him', 'with everything'],
    style: 'maskslide',
  },
  'ponzi-collapse': {
    lines: ['It only works', 'until it stops'],
    style: 'emphasis',
    emphasisWords: ['stops'],
  },
  'audit-red-flag': {
    lines: ['Every red flag', 'was ignored'],
    style: 'emphasis',
    emphasisWords: ['red', 'ignored'],
  },
  'the-reckoning': {
    lines: ['The reckoning', 'came all at once'],
    style: 'wordpop',
    emphasisWords: ['reckoning'],
  },

  // ── True crime ───────────────────────────────────────────────────
  'cold-case': {
    lines: ['For thirty years', 'the case stayed cold'],
    style: 'emphasis',
    emphasisWords: ['thirty', 'cold'],
  },
  'the-perfect-alibi': {
    lines: ['His alibi', 'was airtight', 'or so it seemed'],
    style: 'maskslide',
  },
  'one-piece-of-evidence': {
    lines: ['One piece of evidence', 'broke the whole case'],
    style: 'emphasis',
    emphasisWords: ['one', 'broke'],
  },
  'missing-without-trace': {
    lines: ['She left', 'and never came home'],
    style: 'maskslide',
  },
  'the-confession': {
    lines: ['Then he confessed', 'to something else'],
    style: 'emphasis',
    emphasisWords: ['confessed'],
  },
  'wrongfully-convicted': {
    lines: ['Convicted', 'for a crime', 'he did not commit'],
    style: 'maskslide',
  },

  // ── General explainer / hooks & transitions ──────────────────────
  'hook-what-if': {
    lines: ['What if everything', 'you were told', 'was wrong'],
    style: 'wordpop',
    emphasisWords: ['everything', 'wrong'],
  },
  'chapter-turn': {
    lines: ['But first', 'we have to go back'],
    style: 'maskslide',
  },
  'the-real-question': {
    lines: ['The real question', 'is not what', 'but why'],
    style: 'emphasis',
    emphasisWords: ['why'],
  },
  'here-is-the-catch': {
    lines: ['Here is the catch'],
    style: 'wordpop',
    emphasisWords: ['catch'],
  },
  'remember-this-name': {
    lines: ['Remember this name'],
    style: 'emphasis',
    emphasisWords: ['name'],
  },
} satisfies Record<string, ComponentProps<typeof KineticCaptions>>;
