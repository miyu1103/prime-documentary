/**
 * Prime Documentary brand tokens — single source of truth (decisions/0002 §G).
 * Palette: black / deep navy + electric blue + silver + gold accent.
 * Replace hexes with the exact brand values when finalized; everything reads from here.
 */
export const BRAND = {
  color: {
    ink: '#0A0A0C', // base black
    navy: '#0B1A2B', // deep navy ground
    electric: '#1F6BFF', // primary electric blue
    silver: '#C8CDD6',
    gold: '#E5B53A', // accent
    white: '#F5F7FA',
  },
  font: {
    // Premium typography upgrade (owner-approved 2026-07-17). Loaded via @font-face
    // from remotion/public/fonts (OFL, commercial-OK). See public/fonts/LICENSE_FONTS.md.
    display: '"Oswald", "Archivo", Impact, "Arial Black", sans-serif',
    number: '"Anton", "Oswald", Impact, sans-serif', // big number cards / verdict
    body: '"Oswald", "Trebuchet MS", "Helvetica Neue", Arial, sans-serif',
  },
  video: {fps: 30, width: 1920, height: 1080},
  thumb: {width: 1280, height: 720},
} as const;

export type Brand = typeof BRAND;
