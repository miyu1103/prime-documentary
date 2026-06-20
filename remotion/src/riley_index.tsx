import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {RileyPremium, rileyPremiumDurationInFrames} from './compositions/RileyPremium';

const RileyRoot: React.FC = () => (
  <Composition
    id="RileyPremium"
    component={RileyPremium}
    durationInFrames={rileyPremiumDurationInFrames(BRAND.video.fps)}
    fps={BRAND.video.fps}
    width={BRAND.video.width}
    height={BRAND.video.height}
  />
);

registerRoot(RileyRoot);
