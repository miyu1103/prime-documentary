import React from 'react';
import {BRAND} from '../brand';
import {CasePremiumFromRoughCut, casePremiumDurationInFrames} from './CasePremiumFromRoughCut';
import {VARSITYBLUES_ROUGHCUT} from '../data/varsityblues_roughcut';

export const varsityBluesPremiumDurationInFrames = (fps: number): number =>
  casePremiumDurationInFrames(VARSITYBLUES_ROUGHCUT, fps, 1660.313);

// EP19 uses factory b-roll as the non-hero layer; hero still images are inserted later.
export const VarsityBluesPremium: React.FC = () => (
  <CasePremiumFromRoughCut
    data={VARSITYBLUES_ROUGHCUT}
    shortTitle="OPERATION VARSITY BLUES"
    subtitle="The side door into elite colleges"
    overlayKind="generic"
    totalSec={1660.313}
  />
);
