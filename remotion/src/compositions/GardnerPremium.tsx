import React from 'react';
import {BRAND} from '../brand';
import {CasePremiumFromRoughCut, casePremiumDurationInFrames} from './CasePremiumFromRoughCut';
import {GARDNER_ROUGHCUT} from '../data/gardner_roughcut';

export const gardnerPremiumDurationInFrames = (fps: number): number =>
  casePremiumDurationInFrames(GARDNER_ROUGHCUT, fps, 1650);

// EP20 uses factory b-roll as the non-hero layer; hero still insertion waits for EP20-IMG-001..092.
export const GardnerPremium: React.FC = () => (
  <CasePremiumFromRoughCut
    data={GARDNER_ROUGHCUT}
    shortTitle="THE GARDNER HEIST"
    subtitle="The empty frames that still have no ending"
    overlayKind="generic"
    totalSec={1650}
  />
);
