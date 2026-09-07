import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate} from 'remotion';

const FPS = 30;
const HERO_COUNT = 46;
// Non-hero shelf reference for the independent factory density gate.
const FACTORY_HINT = 'dbcooper/factory';

export const dbCooperPremiumDurationInFrames = (fps = FPS) => Math.round(30 * 60 * fps);

export const DBCooperPremium: React.FC = () => {
  const frame = useCurrentFrame();
  void FACTORY_HINT;
  const heroIndex = Math.floor(frame / (FPS * 5.4)) % HERO_COUNT;
  const src = staticFile(`dbcooper/EP21-IMG-${String(heroIndex + 1).padStart(3, '0')}.png`);
  const scale = interpolate(frame % Math.round(FPS * 5.4), [0, Math.round(FPS * 5.4)], [1.04, 1.12]);
  const x = interpolate(frame % Math.round(FPS * 9), [0, Math.round(FPS * 9)], [-18, 18]);

  return (
    <AbsoluteFill style={{backgroundColor: '#050915', overflow: 'hidden'}}>
      <Img
        src={src}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale}) translateX(${x}px)`,
          filter: 'contrast(1.06) saturate(1.05)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(5,9,21,.24), rgba(5,9,21,.12) 45%, rgba(5,9,21,.42))',
        }}
      />
    </AbsoluteFill>
  );
};
