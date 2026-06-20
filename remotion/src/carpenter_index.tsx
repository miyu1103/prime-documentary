import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {CarpenterPremium, carpenterPremiumDurationInFrames} from './compositions/CarpenterPremium';

const CarpenterRoot: React.FC = () => (
  <Composition
    id="CarpenterPremium"
    component={CarpenterPremium}
    durationInFrames={carpenterPremiumDurationInFrames(BRAND.video.fps)}
    fps={BRAND.video.fps}
    width={BRAND.video.width}
    height={BRAND.video.height}
  />
);

registerRoot(CarpenterRoot);
