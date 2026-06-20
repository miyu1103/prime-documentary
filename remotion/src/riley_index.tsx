import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {RileyPremium, rileyPremiumDurationInFrames} from './compositions/RileyPremium';
import {RileyThumbnail, rileyThumbnailVariants} from './compositions/RileyThumbnails';

const RileyRoot: React.FC = () => (
  <>
    <Composition
      id="RileyPremium"
      component={RileyPremium}
      durationInFrames={rileyPremiumDurationInFrames(BRAND.video.fps)}
      fps={BRAND.video.fps}
      width={BRAND.video.width}
      height={BRAND.video.height}
    />
    {rileyThumbnailVariants.map((variant, index) => (
      <Composition
        key={variant.id}
        id={`Riley-${variant.id}`}
        component={RileyThumbnail}
        durationInFrames={1}
        fps={BRAND.video.fps}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{variantIndex: index}}
      />
    ))}
  </>
);

registerRoot(RileyRoot);
