/**
 * TimbsParallax — PD Visual System P08 2.5D PoC (no-warp cutout path).
 *
 * Reuses the existing Parallax.tsx (rigid per-layer translate+scale) with a
 * depth-derived FOREGROUND cutout + inpainted BACKGROUND plate
 * (scripts/pd-visual-system/layer_cutout_poc.py). Because each layer moves as a
 * rigid image, thin structures (chains, scale beam) DO NOT warp — fixing the
 * DepthStill mesh-displacement failure documented in P08_FINDING.md.
 *
 * A gentle shared Ken-Burns push adds depth on top of the layer parallax
 * differential (owner constraints: small move, no warp, no holes). Preview-only.
 */
import React from 'react';
import {AbsoluteFill, Img, staticFile, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {Parallax} from '../components/Parallax';

export const timbsParallaxDuration = 90;

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

export const TimbsParallax: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  // gentle shared push-in (rigid scale → no warp)
  const kb = interpolate(frame, [0, durationInFrames], [1.02, 1.07]);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${kb})`}}>
        <Parallax
          amount={46}
          layers={[
            {depth: 0.16, node: <Plate src="timbs/_p08/SPN-0007_bg.png" />},
            {depth: 0.95, node: <Plate src="timbs/_p08/SPN-0007_fg.png" />},
          ]}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
