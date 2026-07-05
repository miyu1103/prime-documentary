import type {ComponentProps} from 'react';
import type {AuroraField} from '../AuroraField';

/**
 * Preset catalog for <AuroraField />.
 *
 * AuroraField's ONLY prop is `dur?: number` — the number of frames over which the
 * field settles in and whispers out (fade-in ~1.2s, tail fade over the final 1s).
 * When omitted it inherits the composition's `durationInFrames`. These presets pin
 * `dur` explicitly so the aurora's breath / fade envelope is matched to the length
 * of the shot it backs, independent of the enclosing Composition length.
 *
 * Frame values assume the PD canonical fps = 60 (see root CLAUDE.md §0).
 * Editorial-intent keys are kebab-case; raw duration keys carry the frame count.
 */
export const auroraFieldPresets = {
  // --- bare default: inherit the composition duration ------------------------
  default: {},

  // --- short beds (backing a single line / lower-third) ----------------------
  'bed-short-90f': {dur: 90}, // 1.5s
  'bed-beat-120f': {dur: 120}, // 2.0s
  'bed-scene-150f': {dur: 150}, // 2.5s
  'bed-scene-240f': {dur: 240}, // 4.0s

  // --- medium beds (a paragraph of narration, a held statement) --------------
  'bed-long-450f': {dur: 450}, // 7.5s
  'establishing-600f': {dur: 600}, // 10.0s

  // --- editorial-intent aliases (name the moment, not the frame count) -------
  'title-bed': {dur: 180}, // 3.0s — under an opening title card
  'somber-bed': {dur: 540}, // 9.0s — long, calm bed for a heavy beat
  interlude: {dur: 300}, // 5.0s — breather between sequences
  'chapter-open': {dur: 210}, // 3.5s — chapter / act break
  'end-bed': {dur: 420}, // 7.0s — settle under end-card / credits roll-in
} satisfies Record<string, ComponentProps<typeof AuroraField>>;
