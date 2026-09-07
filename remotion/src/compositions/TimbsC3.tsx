/**
 * TimbsC3 — PD Visual System P11 "C3" = B2 + finishing (grain / vignette / grade).
 *
 * Audio finishing: the narration mix (played by TimbsB1/B2) already has ducking
 * baked in; delivery color is the config canon (libx264 CRF16, bt709). This adds
 * the VISUAL finishing bed: film grain + breathing vignette + a subtle cinematic
 * cool-shadow / warm-highlight grade overlay. Preview-only test-bench.
 */
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {BRAND} from '../brand';
import {TimbsB2, timbsB2DurationInFrames} from './TimbsB2';
import {FilmGrain, VignetteBreath} from '../components/motionkit';

export const timbsC3DurationInFrames = timbsB2DurationInFrames;

export const TimbsC3: React.FC = () => (
  <AbsoluteFill>
    <TimbsB2 />
    {/* subtle cinematic grade: cool lift in shadows, faint warm highlight bloom */}
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at 50% 34%, ${BRAND.color.gold}0F 0%, transparent 42%),
                    linear-gradient(180deg, ${BRAND.color.navy}22 0%, transparent 30%, ${BRAND.color.ink}33 100%)`,
        mixBlendMode: 'soft-light',
        pointerEvents: 'none',
      }}
    />
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
