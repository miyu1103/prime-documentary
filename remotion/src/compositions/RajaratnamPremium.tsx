import React from 'react';
import {RoughCut} from './RoughCut';
import {RAJARATNAM_ROUGHCUT} from '../data/rajaratnam_roughcut';

export const rajaratnamPremiumDurationInFrames = (fps: number) => Math.round(30 * 60 * fps);

export const RajaratnamPremium: React.FC = () => {
  // factory layer is referenced through RAJARATNAM_ROUGHCUT.shots[*].factory / clips.
  return <RoughCut data={RAJARATNAM_ROUGHCUT} />;
};
