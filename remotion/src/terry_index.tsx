import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {TerryPremium, terryPremiumDurationInFrames} from './compositions/TerryPremium';
import {TerryThumbnail, terryThumbnailVariants} from './compositions/TerryThumbnails';

const TerryRoot: React.FC = () => (
  <>
    <Composition
      id="TerryPremium"
      component={TerryPremium}
      durationInFrames={terryPremiumDurationInFrames(BRAND.video.fps)}
      fps={BRAND.video.fps}
      width={BRAND.video.width}
      height={BRAND.video.height}
    />
    {terryThumbnailVariants.map((variant, index) => (
      <Composition
        key={variant.id}
        id={`Terry-${variant.id}`}
        component={TerryThumbnail}
        durationInFrames={1}
        fps={BRAND.video.fps}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{variantIndex: index}}
      />
    ))}
  </>
);

registerRoot(TerryRoot);
