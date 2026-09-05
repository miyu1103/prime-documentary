/**
 * TimbsDepthTest — PD Visual System P08 2.5D PoC.
 * Renders the timbs "scale of justice" hero (SPN-0007) through the EXISTING
 * DepthStill treatment (real Depth-Anything-V2-Small map SPN-0007_depth.png +
 * @remotion/three displacement). Gentle dolly → foreground scale/car parallaxes
 * against the dark background. Preview-only; not shipped. Reuses DepthStill
 * (invariant 14 — no new 2.5D component).
 */
import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DepthStill} from './CaseFilm';

export const timbsDepthTestDuration = 90;

export const TimbsDepthTest: React.FC = () => (
  <AbsoluteFill>
    <DepthStill src="timbs/SPN-0007.png" seed="timbs007" dir={1} dur={90} />
  </AbsoluteFill>
);
