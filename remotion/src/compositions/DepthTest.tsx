import React from 'react';
import {AbsoluteFill} from 'remotion';
import {DepthStill} from './CaseFilm';

/**
 * DepthTest — dev harness for the CaseFilm `depth` treatment (real DPT depth-map
 * displacement in @remotion/three). Renders one still through DepthStill so the
 * treatment can be eyeballed before EP28's 40 images land. Preview-only; not shipped.
 */
export const DepthTest: React.FC = () => (
  <AbsoluteFill>
    <DepthStill src="_motiontest/test.jpg" seed="depthtest" dir={1} />
  </AbsoluteFill>
);
