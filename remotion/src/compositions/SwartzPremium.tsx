import React from 'react';
import {BRAND} from '../brand';
import {SWARTZ_ROUGHCUT} from '../data/swartz_roughcut';
import {CasePremiumFromRoughCut, casePremiumDurationInFrames} from './CasePremiumFromRoughCut';

// EP23 uses the staged swartz/factory shelf entries embedded in SWARTZ_ROUGHCUT.
export const swartzPremiumDurationInFrames = (fps = BRAND.video.fps): number =>
  casePremiumDurationInFrames(SWARTZ_ROUGHCUT, fps, 30 * 60);

export const SwartzPremium: React.FC = () => (
  <CasePremiumFromRoughCut
    data={SWARTZ_ROUGHCUT}
    shortTitle="THE INTERNET'S OWN BOY"
    subtitle="Aaron Swartz and the open web"
    overlayKind="generic"
    totalSec={30 * 60}
  />
);
