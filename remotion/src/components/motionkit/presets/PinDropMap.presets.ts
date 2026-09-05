import type {ComponentProps} from 'react';
import type {PinDropMap} from '../PinDropMap';

/**
 * Ready-made prop fills for PinDropMap — the "this happened in N places" beat.
 * `pins` is an ordered list of {x, y, label?} where x/y are 0..1 fractions of
 * the stylized map plane (0,0 = top-left, 1,1 = bottom-right). Pins drop in
 * order with a stagger and are wired together by electric arcs, so order = the
 * sequence the viewer reads. Labels are generic on purpose — swap for episode
 * specifics. Leave `dur` unset unless a shot needs a custom length.
 * Usage: <PinDropMap {...pinDropMapPresets['key']} />
 */
export const pinDropMapPresets = {
  // ── Two places — the connection / the pattern begins ──────────────
  'two-cities-scattered': {
    pins: [
      {x: 0.24, y: 0.34, label: 'City 1'},
      {x: 0.74, y: 0.66, label: 'City 2'},
    ],
  },
  'two-branches': {
    pins: [
      {x: 0.3, y: 0.6, label: 'Branch 1'},
      {x: 0.68, y: 0.36, label: 'Branch 2'},
    ],
  },
  'here-and-there': {
    pins: [
      {x: 0.18, y: 0.5, label: 'Here'},
      {x: 0.82, y: 0.5, label: 'There'},
    ],
  },
  'origin-and-endpoint': {
    pins: [
      {x: 0.2, y: 0.28, label: 'Origin'},
      {x: 0.76, y: 0.72, label: 'Endpoint'},
    ],
  },

  // ── Three places — the trail widens ──────────────────────────────
  'three-incidents-scattered': {
    pins: [
      {x: 0.22, y: 0.3, label: 'Incident 1'},
      {x: 0.56, y: 0.62, label: 'Incident 2'},
      {x: 0.82, y: 0.34, label: 'Incident 3'},
    ],
  },
  'three-victims': {
    pins: [
      {x: 0.28, y: 0.4, label: 'Victim 1'},
      {x: 0.5, y: 0.66, label: 'Victim 2'},
      {x: 0.72, y: 0.38, label: 'Victim 3'},
    ],
  },
  'three-cities-line': {
    pins: [
      {x: 0.2, y: 0.5, label: 'City 1'},
      {x: 0.5, y: 0.5, label: 'City 2'},
      {x: 0.8, y: 0.5, label: 'City 3'},
    ],
  },
  'three-branches-clustered': {
    pins: [
      {x: 0.44, y: 0.44, label: 'Branch 1'},
      {x: 0.58, y: 0.5, label: 'Branch 2'},
      {x: 0.5, y: 0.62, label: 'Branch 3'},
    ],
  },

  // ── Five places — it kept happening ──────────────────────────────
  'five-locations-scattered': {
    pins: [
      {x: 0.2, y: 0.28, label: 'Location 1'},
      {x: 0.68, y: 0.24, label: 'Location 2'},
      {x: 0.44, y: 0.52, label: 'Location 3'},
      {x: 0.78, y: 0.68, label: 'Location 4'},
      {x: 0.24, y: 0.72, label: 'Location 5'},
    ],
  },
  'five-victims-scattered': {
    pins: [
      {x: 0.26, y: 0.32, label: 'Victim 1'},
      {x: 0.6, y: 0.3, label: 'Victim 2'},
      {x: 0.8, y: 0.56, label: 'Victim 3'},
      {x: 0.5, y: 0.72, label: 'Victim 4'},
      {x: 0.22, y: 0.6, label: 'Victim 5'},
    ],
  },
  'five-incidents-clustered': {
    pins: [
      {x: 0.42, y: 0.4, label: 'Incident 1'},
      {x: 0.58, y: 0.42, label: 'Incident 2'},
      {x: 0.5, y: 0.54, label: 'Incident 3'},
      {x: 0.4, y: 0.58, label: 'Incident 4'},
      {x: 0.62, y: 0.6, label: 'Incident 5'},
    ],
  },
  'five-branches-numbered': {
    pins: [
      {x: 0.22, y: 0.42, label: 'Branch 1'},
      {x: 0.4, y: 0.3, label: 'Branch 2'},
      {x: 0.58, y: 0.36, label: 'Branch 3'},
      {x: 0.74, y: 0.5, label: 'Branch 4'},
      {x: 0.66, y: 0.7, label: 'Branch 5'},
    ],
  },

  // ── Eight places — a nationwide spread ───────────────────────────
  'eight-cities-scattered': {
    pins: [
      {x: 0.18, y: 0.26, label: 'City 1'},
      {x: 0.42, y: 0.2, label: 'City 2'},
      {x: 0.7, y: 0.26, label: 'City 3'},
      {x: 0.84, y: 0.5, label: 'City 4'},
      {x: 0.68, y: 0.74, label: 'City 5'},
      {x: 0.44, y: 0.78, label: 'City 6'},
      {x: 0.2, y: 0.7, label: 'City 7'},
      {x: 0.14, y: 0.48, label: 'City 8'},
    ],
  },
  'eight-incidents-grid': {
    pins: [
      {x: 0.3, y: 0.3, label: 'Incident 1'},
      {x: 0.5, y: 0.3, label: 'Incident 2'},
      {x: 0.7, y: 0.3, label: 'Incident 3'},
      {x: 0.3, y: 0.5, label: 'Incident 4'},
      {x: 0.7, y: 0.5, label: 'Incident 5'},
      {x: 0.3, y: 0.7, label: 'Incident 6'},
      {x: 0.5, y: 0.7, label: 'Incident 7'},
      {x: 0.7, y: 0.7, label: 'Incident 8'},
    ],
  },

  // ── Dense spread — unlabeled dots (scale, not detail) ────────────
  'a-dozen-unlabeled': {
    pins: [
      {x: 0.18, y: 0.3},
      {x: 0.34, y: 0.22},
      {x: 0.5, y: 0.28},
      {x: 0.66, y: 0.2},
      {x: 0.82, y: 0.32},
      {x: 0.26, y: 0.48},
      {x: 0.44, y: 0.5},
      {x: 0.6, y: 0.46},
      {x: 0.78, y: 0.54},
      {x: 0.32, y: 0.7},
      {x: 0.52, y: 0.72},
      {x: 0.72, y: 0.7},
    ],
  },
  'everywhere-scatter': {
    pins: [
      {x: 0.12, y: 0.2},
      {x: 0.28, y: 0.36},
      {x: 0.46, y: 0.18},
      {x: 0.62, y: 0.34},
      {x: 0.8, y: 0.22},
      {x: 0.88, y: 0.46},
      {x: 0.72, y: 0.6},
      {x: 0.54, y: 0.68},
      {x: 0.38, y: 0.58},
      {x: 0.2, y: 0.66},
      {x: 0.14, y: 0.48},
      {x: 0.66, y: 0.8},
      {x: 0.42, y: 0.82},
    ],
  },
  'tight-cluster-outbreak': {
    pins: [
      {x: 0.46, y: 0.42},
      {x: 0.54, y: 0.4},
      {x: 0.5, y: 0.5},
      {x: 0.44, y: 0.52},
      {x: 0.58, y: 0.5},
      {x: 0.48, y: 0.6},
      {x: 0.56, y: 0.6},
      {x: 0.52, y: 0.34},
    ],
  },

  // ── Financial / fraud footprint ──────────────────────────────────
  'four-shell-companies': {
    pins: [
      {x: 0.24, y: 0.3, label: 'Shell 1'},
      {x: 0.72, y: 0.32, label: 'Shell 2'},
      {x: 0.74, y: 0.7, label: 'Shell 3'},
      {x: 0.26, y: 0.68, label: 'Shell 4'},
    ],
  },
  'three-offshore-accounts': {
    pins: [
      {x: 0.26, y: 0.44, label: 'Account 1'},
      {x: 0.54, y: 0.28, label: 'Account 2'},
      {x: 0.78, y: 0.6, label: 'Account 3'},
    ],
  },
  'five-branch-offices': {
    pins: [
      {x: 0.22, y: 0.34, label: 'Office 1'},
      {x: 0.5, y: 0.24, label: 'Office 2'},
      {x: 0.78, y: 0.36, label: 'Office 3'},
      {x: 0.66, y: 0.66, label: 'Office 4'},
      {x: 0.32, y: 0.68, label: 'Office 5'},
    ],
  },

  // ── Route / sequence — one thing moving place to place ───────────
  'four-stop-route': {
    pins: [
      {x: 0.16, y: 0.7, label: 'Stop 1'},
      {x: 0.4, y: 0.4, label: 'Stop 2'},
      {x: 0.64, y: 0.56, label: 'Stop 3'},
      {x: 0.86, y: 0.3, label: 'Stop 4'},
    ],
  },
  'five-stop-trail': {
    pins: [
      {x: 0.14, y: 0.5, label: 'Stop 1'},
      {x: 0.34, y: 0.32, label: 'Stop 2'},
      {x: 0.54, y: 0.5, label: 'Stop 3'},
      {x: 0.74, y: 0.34, label: 'Stop 4'},
      {x: 0.88, y: 0.58, label: 'Stop 5'},
    ],
  },
  'crossing-the-country': {
    pins: [
      {x: 0.12, y: 0.42, label: 'Start'},
      {x: 0.5, y: 0.5, label: 'Midpoint'},
      {x: 0.88, y: 0.4, label: 'End'},
    ],
  },

  // ── Single emphasis — one place, one point ───────────────────────
  'single-site': {
    pins: [{x: 0.5, y: 0.46, label: 'The Site'}],
  },
  'ground-zero': {
    pins: [{x: 0.46, y: 0.5, label: 'Ground Zero'}],
  },
} satisfies Record<string, ComponentProps<typeof PinDropMap>>;
