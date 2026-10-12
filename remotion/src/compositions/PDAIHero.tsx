/**
 * PDAIHero — a full-frame AI-generated hero shot (Wan2.2) with PD-brand finishing.
 *
 * The source clip (`_ai/wan22_justice_720p.mp4`, 1280x720, ~3.4s) is a cinematic
 * golden scale of justice in fog. It is presented FULL-FRAME (objectFit cover) and
 * SLOWED to ~0.45× playbackRate so a ~3.4s clip fills the ~8s hero beat as one long,
 * unhurried push — cleaner than a loop seam or a frozen hold for a hero shot.
 *
 * Finishing bed matches TimbsC3 / PDForfeiture60: a faint gold radial soft-light
 * grade + VignetteBreath + FilmGrain. A gentle Ken-Burns (1.0→1.05) keeps it alive.
 *
 * Disclosure: a BRIEF lower-third (fades in ~1s, out by ~4s) labels the footage as
 * AI-generated (invariant 11 — generated visuals are never presented as authentic).
 * No real-person likeness; brand tokens only.
 *
 * 240f @30fps = 8s.
 */
import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {FilmGrain, VignetteBreath} from '../components/motionkit';

// 秒→フレーム（fps基準、フレーム直書き禁止）
const AI_CLIP = '_ai/wan22_atmos.mp4';
const DURATION_SECONDS = 3.4; // play the AI clip at its natural length
const PLAYBACK_RATE = 1.0; // full speed — show the AI's own motion, no fake zoom

export const pdAIHeroDuration = Math.round(BRAND.video.fps * DURATION_SECONDS);

// ---------------------------------------------------------------------
// Disclosure lower-third — bottom-left safe area, semi-transparent dark
//   strip with a gold left border. Fades in ~1s, out by ~4s. opacity は
//   translateY と併用（opacity 単独禁止）。
// ---------------------------------------------------------------------
const Disclosure: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const inStart = Math.round(fps * 0.8);
  const inEnd = Math.round(fps * 1.2);
  const outStart = Math.round(fps * 3.6);
  const outEnd = Math.round(fps * 4.0);

  const opacity = interpolate(
    frame,
    [inStart, inEnd, outStart, outEnd],
    [0, 1, 1, 0],
    {
      easing: Easing.inOut(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // 入りは下から、退きは下へ（opacity 単独にしない）
  const enterY = interpolate(frame, [inStart, inEnd], [18, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const exitY = interpolate(frame, [outStart, outEnd], [0, 14], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'flex-end',
        alignItems: 'flex-start',
        pointerEvents: 'none',
        backgroundColor: 'transparent',
      }}
    >
      <div
        style={{
          transform: `translateY(${enterY + exitY}px)`,
          opacity,
          margin: '0 0 96px 92px',
          display: 'flex',
          alignItems: 'stretch',
        }}
      >
        {/* gold left border */}
        <div
          style={{
            width: 6,
            alignSelf: 'stretch',
            backgroundColor: BRAND.color.gold,
            borderRadius: 2,
            boxShadow: `0 0 18px ${BRAND.color.gold}66`,
          }}
        />
        {/* semi-transparent dark strip */}
        <div
          style={{
            background: `linear-gradient(100deg, ${BRAND.color.navy}D9 0%, ${BRAND.color.ink}CC 100%)`,
            backdropFilter: 'blur(3px)',
            padding: '14px 26px 16px 22px',
          }}
        >
          <div
            style={{
              color: BRAND.color.gold,
              fontFamily: BRAND.font.body,
              fontSize: 20,
              fontWeight: 700,
              letterSpacing: 3,
            }}
          >
            AI-GENERATED · Wan2.2
          </div>
          <div
            style={{
              marginTop: 6,
              color: BRAND.color.white,
              fontFamily: BRAND.font.body,
              fontSize: 30,
              fontWeight: 500,
              letterSpacing: 0.5,
            }}
          >
            footage that never existed
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const PDAIHero: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* full-frame AI clip at full speed — no added zoom, so the AI's own motion shows */}
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <OffthreadVideo
          src={staticFile(AI_CLIP)}
          muted
          playbackRate={PLAYBACK_RATE}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>

      {/* finishing bed: faint gold radial soft-light grade（TimbsC3/PDForfeiture60 と同系） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 90% at 50% 40%, ${BRAND.color.gold}14 0%, transparent 46%),
                      linear-gradient(180deg, ${BRAND.color.navy}1F 0%, transparent 32%, ${BRAND.color.ink}3A 100%)`,
          mixBlendMode: 'soft-light',
          pointerEvents: 'none',
        }}
      />
      <VignetteBreath />
      <FilmGrain />

      <Disclosure />
    </AbsoluteFill>
  );
};
