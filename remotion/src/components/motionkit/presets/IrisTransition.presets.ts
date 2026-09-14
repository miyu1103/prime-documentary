import type {ComponentProps} from 'react';
import type {IrisTransition} from '../IrisTransition';

/**
 * Preset catalog for <IrisTransition />.
 *
 * Props (from IrisTransition.tsx):
 *   mode?:  'in' | 'out'   — 'out' closes the iris (hole shrinks to ink),
 *                            'in' opens it (hole grows from 0). Default 'out'.
 *   shape?: 'circle' | 'diamond' — hole geometry. Default 'circle'.
 *   dur?:   number         — spring duration in frames; smaller = snappier.
 *                            Falls back to composition durationInFrames when omitted.
 *
 * Speed convention used below: fast = 12f, normal = 20f, slow = 30f.
 */
export const irisTransitionPresets = {
  // ── OUT × circle (scene close, hole shrinks to ink) ──
  'iris-out-circle-fast': {mode: 'out', shape: 'circle', dur: 12},
  'iris-out-circle-normal': {mode: 'out', shape: 'circle', dur: 20},
  'iris-out-circle-slow': {mode: 'out', shape: 'circle', dur: 30},

  // ── IN × circle (scene open, hole grows from 0) ──
  'iris-in-circle-fast': {mode: 'in', shape: 'circle', dur: 12},
  'iris-in-circle-normal': {mode: 'in', shape: 'circle', dur: 20},
  'iris-in-circle-slow': {mode: 'in', shape: 'circle', dur: 30},

  // ── OUT × diamond ──
  'iris-out-diamond-fast': {mode: 'out', shape: 'diamond', dur: 12},
  'iris-out-diamond-normal': {mode: 'out', shape: 'diamond', dur: 20},
  'iris-out-diamond-slow': {mode: 'out', shape: 'diamond', dur: 30},

  // ── IN × diamond ──
  'iris-in-diamond-fast': {mode: 'in', shape: 'diamond', dur: 12},
  'iris-in-diamond-normal': {mode: 'in', shape: 'diamond', dur: 20},
  'iris-in-diamond-slow': {mode: 'in', shape: 'diamond', dur: 30},

  // ── Semantic aliases (editorial intent) ──
  'scene-close': {mode: 'out', shape: 'circle', dur: 20},
  'reveal-open': {mode: 'in', shape: 'circle', dur: 20},
  'hard-cut-out': {mode: 'out', shape: 'circle', dur: 12},
  'gem-reveal': {mode: 'in', shape: 'diamond', dur: 24},
  'slow-fade-to-ink': {mode: 'out', shape: 'circle', dur: 30},
} satisfies Record<string, ComponentProps<typeof IrisTransition>>;
