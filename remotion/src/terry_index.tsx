import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {TerryPremium, terryPremiumDurationInFrames} from './compositions/TerryPremium';

const TerryRoot: React.FC = () => (
  <Composition
    id="TerryPremium"
    component={TerryPremium}
    durationInFrames={terryPremiumDurationInFrames(BRAND.video.fps)}
    fps={BRAND.video.fps}
    width={BRAND.video.width}
    height={BRAND.video.height}
  />
);

registerRoot(TerryRoot);
