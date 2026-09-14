import type {ComponentProps} from 'react';
import type {CorkboardWeb} from '../CorkboardWeb';

/**
 * Ready-made prop fills for CorkboardWeb — the detective "conspiracy board"
 * beat where evidence cards pin down and red string wires them together.
 * `nodes` is an ordered list of {x, y, label?} where x/y are 0..1 fractions of
 * the frame (0,0 = top-left, 1,1 = bottom-right); each node is a photo/memo
 * card that drops in with a stagger, so order = the order cards appear.
 * `links` are [a, b] index pairs into `nodes` — every index MUST be a valid
 * position in that preset's `nodes` array — and each pair is one red string
 * drawn between the two cards. Labels are generic on purpose (Suspect, The
 * Broker, Shell Co, Witness, The Fixer); swap for episode specifics. Cards are
 * kept inside x 0.14..0.86 / y 0.20..0.80 so the 236x172 cards clear the edges.
 * Leave `dur` unset unless a shot needs a custom length.
 * Usage: <CorkboardWeb {...corkboardWebPresets['key']} />
 */
export const corkboardWebPresets = {
  // ── Suspects — the small closed set of people who could have done it ──
  'three-suspect-triangle': {
    nodes: [
      {x: 0.5, y: 0.26, label: 'Suspect A'},
      {x: 0.26, y: 0.68, label: 'Suspect B'},
      {x: 0.74, y: 0.68, label: 'Suspect C'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 0],
    ],
  },
  'prime-suspect-and-two': {
    nodes: [
      {x: 0.5, y: 0.28, label: 'Prime Suspect'},
      {x: 0.24, y: 0.7, label: 'Associate'},
      {x: 0.76, y: 0.7, label: 'Associate'},
    ],
    links: [
      [0, 1],
      [0, 2],
    ],
  },
  'love-triangle-motive': {
    nodes: [
      {x: 0.5, y: 0.7, label: 'The Victim'},
      {x: 0.26, y: 0.28, label: 'Suspect'},
      {x: 0.74, y: 0.28, label: 'The Other'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [1, 2],
    ],
  },

  // ── Ring leader — one figure at the center of every thread ───────────
  'ring-leader-and-crew': {
    nodes: [
      {x: 0.5, y: 0.5, label: 'Ring Leader'},
      {x: 0.5, y: 0.22, label: 'Enforcer'},
      {x: 0.82, y: 0.4, label: 'Runner'},
      {x: 0.72, y: 0.76, label: 'Runner'},
      {x: 0.28, y: 0.76, label: 'Lookout'},
      {x: 0.18, y: 0.4, label: 'Driver'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
      [0, 5],
    ],
  },
  'the-fixer-hub': {
    nodes: [
      {x: 0.5, y: 0.5, label: 'The Fixer'},
      {x: 0.24, y: 0.28, label: 'Client'},
      {x: 0.76, y: 0.28, label: 'Client'},
      {x: 0.76, y: 0.72, label: 'Client'},
      {x: 0.24, y: 0.72, label: 'Client'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
    ],
  },
  'kingpin-wheel': {
    nodes: [
      {x: 0.5, y: 0.5, label: 'The Boss'},
      {x: 0.5, y: 0.2, label: 'Lieutenant'},
      {x: 0.8, y: 0.34, label: 'Cell 1'},
      {x: 0.82, y: 0.66, label: 'Cell 2'},
      {x: 0.5, y: 0.8, label: 'Cell 3'},
      {x: 0.18, y: 0.66, label: 'Cell 4'},
      {x: 0.2, y: 0.34, label: 'Cell 5'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
      [0, 5],
      [0, 6],
    ],
  },

  // ── Chain of accomplices — the order it moved down the line ──────────
  'chain-of-accomplices': {
    nodes: [
      {x: 0.16, y: 0.32, label: 'The Insider'},
      {x: 0.38, y: 0.62, label: 'Accomplice'},
      {x: 0.62, y: 0.32, label: 'Accomplice'},
      {x: 0.84, y: 0.62, label: 'The Buyer'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
    ],
  },
  'command-chain': {
    nodes: [
      {x: 0.18, y: 0.5, label: 'The Boss'},
      {x: 0.39, y: 0.5, label: 'Lieutenant'},
      {x: 0.61, y: 0.5, label: 'Enforcer'},
      {x: 0.82, y: 0.5, label: 'The Runner'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
    ],
  },
  'money-trail-chain': {
    nodes: [
      {x: 0.16, y: 0.7, label: 'The Source'},
      {x: 0.34, y: 0.36, label: 'Shell Co'},
      {x: 0.52, y: 0.7, label: 'Shell Co'},
      {x: 0.7, y: 0.36, label: 'The Broker'},
      {x: 0.86, y: 0.7, label: 'The Payout'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
    ],
  },

  // ── Two clusters — two crews joined by a single go-between ───────────
  'two-cells-one-courier': {
    nodes: [
      {x: 0.2, y: 0.26, label: 'Cell A'},
      {x: 0.16, y: 0.62, label: 'Cell A'},
      {x: 0.34, y: 0.78, label: 'Cell A'},
      {x: 0.66, y: 0.26, label: 'Cell B'},
      {x: 0.84, y: 0.6, label: 'Cell B'},
      {x: 0.66, y: 0.78, label: 'Cell B'},
      {x: 0.5, y: 0.5, label: 'The Courier'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 0],
      [3, 4],
      [4, 5],
      [5, 3],
      [2, 6],
      [6, 3],
    ],
  },
  'rival-crews-one-deal': {
    nodes: [
      {x: 0.2, y: 0.3, label: 'The Seller'},
      {x: 0.2, y: 0.7, label: 'Muscle'},
      {x: 0.8, y: 0.3, label: 'The Buyer'},
      {x: 0.8, y: 0.7, label: 'Muscle'},
      {x: 0.5, y: 0.5, label: 'The Broker'},
    ],
    links: [
      [0, 1],
      [2, 3],
      [0, 4],
      [4, 2],
    ],
  },

  // ── Follow the money — shells, brokers, offshore layers ──────────────
  'shell-company-layers': {
    nodes: [
      {x: 0.16, y: 0.5, label: 'The Money'},
      {x: 0.38, y: 0.3, label: 'Shell Co'},
      {x: 0.5, y: 0.7, label: 'Shell Co'},
      {x: 0.64, y: 0.3, label: 'Shell Co'},
      {x: 0.86, y: 0.5, label: 'Offshore'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
      [0, 4],
    ],
  },
  'broker-fans-out': {
    nodes: [
      {x: 0.2, y: 0.5, label: 'The Broker'},
      {x: 0.54, y: 0.22, label: 'Shell Co'},
      {x: 0.6, y: 0.44, label: 'Shell Co'},
      {x: 0.6, y: 0.68, label: 'Shell Co'},
      {x: 0.54, y: 0.8, label: 'Shell Co'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
    ],
  },
  'offshore-web': {
    nodes: [
      {x: 0.3, y: 0.28, label: 'Shell Co'},
      {x: 0.7, y: 0.28, label: 'Shell Co'},
      {x: 0.82, y: 0.66, label: 'Offshore'},
      {x: 0.5, y: 0.78, label: 'The Broker'},
      {x: 0.18, y: 0.66, label: 'Offshore'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
      [4, 0],
      [0, 3],
    ],
  },

  // ── Witnesses & testimony — who saw what ─────────────────────────────
  'suspect-and-witnesses': {
    nodes: [
      {x: 0.5, y: 0.24, label: 'The Suspect'},
      {x: 0.22, y: 0.62, label: 'Witness'},
      {x: 0.5, y: 0.76, label: 'Witness'},
      {x: 0.78, y: 0.62, label: 'Witness'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
    ],
  },
  'broker-between-parties': {
    nodes: [
      {x: 0.5, y: 0.5, label: 'The Broker'},
      {x: 0.2, y: 0.3, label: 'The Buyer'},
      {x: 0.8, y: 0.3, label: 'The Seller'},
      {x: 0.5, y: 0.8, label: 'Shell Co'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [1, 2],
    ],
  },
  'inside-man-and-crew': {
    nodes: [
      {x: 0.28, y: 0.3, label: 'The Insider'},
      {x: 0.72, y: 0.28, label: 'The Fixer'},
      {x: 0.8, y: 0.68, label: 'Accomplice'},
      {x: 0.5, y: 0.78, label: 'Accomplice'},
      {x: 0.2, y: 0.66, label: 'Witness'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [1, 3],
      [0, 4],
      [3, 4],
    ],
  },

  // ── Full web — everyone is connected ─────────────────────────────────
  'everyone-is-connected': {
    nodes: [
      {x: 0.5, y: 0.2, label: 'The Boss'},
      {x: 0.82, y: 0.38, label: 'The Broker'},
      {x: 0.78, y: 0.72, label: 'Shell Co'},
      {x: 0.5, y: 0.82, label: 'The Fixer'},
      {x: 0.22, y: 0.72, label: 'Accomplice'},
      {x: 0.18, y: 0.38, label: 'The Insider'},
    ],
    links: [
      [0, 1],
      [1, 2],
      [2, 3],
      [3, 4],
      [4, 5],
      [5, 0],
      [0, 3],
      [1, 4],
      [2, 5],
    ],
  },
  'tangled-web': {
    nodes: [
      {x: 0.5, y: 0.5, label: 'The Fixer'},
      {x: 0.5, y: 0.2, label: 'Suspect'},
      {x: 0.82, y: 0.36, label: 'The Broker'},
      {x: 0.8, y: 0.7, label: 'Shell Co'},
      {x: 0.5, y: 0.82, label: 'Witness'},
      {x: 0.2, y: 0.7, label: 'Accomplice'},
      {x: 0.18, y: 0.36, label: 'The Insider'},
    ],
    links: [
      [0, 1],
      [0, 2],
      [0, 3],
      [0, 4],
      [0, 5],
      [0, 6],
      [1, 2],
      [3, 4],
      [5, 6],
    ],
  },

  // ── Minimal — a single link, the first connection ────────────────────
  'two-suspects-linked': {
    nodes: [
      {x: 0.3, y: 0.42, label: 'Suspect'},
      {x: 0.7, y: 0.58, label: 'Suspect'},
    ],
    links: [[0, 1]],
  },
  'broker-and-client': {
    nodes: [
      {x: 0.32, y: 0.5, label: 'The Broker'},
      {x: 0.68, y: 0.5, label: 'Client'},
    ],
    links: [[0, 1]],
  },
} satisfies Record<string, ComponentProps<typeof CorkboardWeb>>;
