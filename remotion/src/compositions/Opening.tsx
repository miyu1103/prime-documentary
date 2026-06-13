import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Horizon, PdMonogram} from '../components/Brand';

export type OpeningProps = {
  channelName: string;
};

/** Logo reveal over a rising horizon (decisions/0002 §G). ~2.5s at 30fps. */
export const Opening: React.FC<OpeningProps> = ({channelName}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  // Horizon rises from bottom to ~58% over the first second.
  const horizonY = interpolate(frame, [0, fps], [1.05, 0.58], {
    extrapolateRight: 'clamp',
  });

  // Logo springs in after the horizon settles.
  const logoIn = spring({frame: frame - fps * 0.6, fps, config: {damping: 200}});
  const logoScale = interpolate(logoIn, [0, 1], [0.8, 1]);

  // Wordmark fades in, then everything fades out at the end.
  const wordOpacity = interpolate(frame, [fps, fps * 1.4], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fadeOut = interpolate(
    frame,
    [durationInFrames - fps * 0.5, durationInFrames],
    [1, 0],
    {extrapolateLeft: 'clamp'},
  );

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 75%)`,
        opacity: fadeOut,
      }}
    >
      <Horizon y={horizonY} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{transform: `scale(${logoScale})`, opacity: logoIn}}>
          <PdMonogram size={260} />
        </div>
        <div
          style={{
            marginTop: 28,
            opacity: wordOpacity,
            color: BRAND.color.silver,
            fontFamily: BRAND.font.display,
            fontSize: 40,
            letterSpacing: 8,
            textTransform: 'uppercase',
          }}
        >
          {channelName}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
