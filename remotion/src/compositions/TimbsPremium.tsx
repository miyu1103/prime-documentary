import React from 'react';
import {BRAND} from '../brand';
import {TIMBS_CAPTIONS} from '../data/timbs_captions';
import {TIMBS_ROUGHCUT} from '../data/timbs_roughcut';
import {CasePremiumFromRoughCut, casePremiumDurationInFrames} from './CasePremiumFromRoughCut';

export const TimbsPremium: React.FC = () => (
  <CasePremiumFromRoughCut
    data={{...TIMBS_ROUGHCUT, narrationSrc: 'timbs/timbs_final_mix_v001.mp3', captions: TIMBS_CAPTIONS}}
    shortTitle="Timbs"
    subtitle="The car the Constitution would not let them keep"
    overlayKind="generic"
  />
);

export const timbsPremiumDurationInFrames = (fps: number = BRAND.video.fps): number =>
  casePremiumDurationInFrames(TIMBS_ROUGHCUT, fps);
