import React from 'react';
import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';

/**
 * Single-clip proof: an AI-generated motion clip composited into the channel look
 * — sparse hook caption, brand colour grade, vignette, grain, citation lower-third
 * and a reconstruction notice (invariant 11). This is the *target* look: a moving
 * video clip is the hero, not a coded placeholder. Captions are intentionally
 * sparse (one key line), per the owner's direction.
 *
 * Drop the downloaded clip at remotion/public/proof_clip.mp4 and render:
 *   npx remotion render ClipProof out/proof.mp4
 */
export type ClipProofProps = {
  src: string;
  hook: string;
  citation: string;
  reconstruction: boolean;
};

export const ClipProof: React.FC<ClipProofProps> = ({src, hook, citation, reconstruction}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();

  const capIn = interpolate(f, [10, 28], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const capOut = interpolate(f, [durationInFrames - 34, durationInFrames - 12], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const capO = Math.min(capIn, capOut);
  const capY = interpolate(capIn, [0, 1], [18, 0]);

  // a touch of extra push-in on top of the clip's own motion
  const scale = interpolate(f, [0, durationInFrames], [1.02, 1.09]);

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 50%'}}>
        <OffthreadVideo
          src={staticFile(src)}
          muted
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>

      {/* brand colour grade: cool navy wash + bottom sink for caption legibility */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `linear-gradient(180deg, ${BRAND.color.navy}33 0%, transparent 28%, transparent 62%, ${BRAND.color.ink}99 100%)`,
        }}
      />
      <Vignette />
      <Grain opacity={0.06} />

      {/* sparse hook caption */}
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 130}}>
        <div
          style={{
            opacity: capO,
            transform: `translateY(${capY}px)`,
            maxWidth: '80%',
            textAlign: 'center',
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 64,
            lineHeight: 1.08,
            letterSpacing: -1,
            textShadow: `0 6px 36px ${BRAND.color.ink}`,
          }}
        >
          {hook}
        </div>
      </AbsoluteFill>

      {/* citation lower-third */}
      <div
        style={{
          position: 'absolute',
          left: 48,
          bottom: 56,
          color: BRAND.color.silver,
          fontFamily: BRAND.font.body,
          fontSize: 22,
          borderLeft: `3px solid ${BRAND.color.gold}`,
          paddingLeft: 12,
          opacity: 0.92,
        }}
      >
        {citation}
      </div>

      {/* reconstruction notice — AI-generated, not authentic record (invariant 11) */}
      {reconstruction ? (
        <div
          style={{
            position: 'absolute',
            right: 36,
            top: 30,
            color: `${BRAND.color.silver}AA`,
            fontFamily: BRAND.font.body,
            fontSize: 18,
            letterSpacing: 0.3,
          }}
        >
          Reconstruction — not authentic footage
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
