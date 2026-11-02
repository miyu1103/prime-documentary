/**
 * TimbsB1 — PD Visual System P06 "B1" test-bench.
 *
 * Rebuilds the timbs 80.4s baseline window (SPN-0005/0006/0007, source-video
 * 110.1–190.5s) using ONLY existing footage + the core-5 components + the SAME
 * narration (no new tools; WhisperX/2.5D/Blender/AI-video are later phases).
 *
 * Goal: replace the two near-still shots measured in P01 (SPN-0006 motion 0.87,
 * SPN-0007 motion 0.63) with meaningful motion:
 *   beat1 "no prison"      -> real footage + kinetic telop      (Reveal)
 *   beat2 "$10k vs $42k"   -> PenaltyVsProperty                 (Compare)
 *   beat3 "grossly dispro" -> QuoteUnderExamination             (Isolate)
 *
 * Same narration as baseline_A: narration mix played from 110.1s (frame 3303).
 * Duration 2412f @30fps == baseline_A, so A/B compare on identical audio.
 */
import React from 'react';
import {
  AbsoluteFill, Audio, OffthreadVideo, Series, staticFile, useVideoConfig, interpolate, useCurrentFrame,
} from 'remotion';
import {BRAND} from '../brand';
import {PenaltyVsProperty, QuoteUnderExamination} from '../components/core5';
import {KineticCaptions, LowerThird, SoftGlow, VignetteBreath} from '../components/motionkit';

const FPS = 30;
const WINDOW_START_SEC = 110.1; // == baseline_A in-point
export const timbsB1DurationInFrames = 2412; // 80.4s @30fps (SPN-0005+0006+0007)
const BEATS = {five: Math.round(25.2 * FPS), six: Math.round(28.6 * FPS), seven: Math.round(26.6 * FPS)};

/** beat1: existing footage with a slow push-in so it is never a still. */
const FootageBeat: React.FC<{src: string; telop: string; source: string}> = ({src, telop, source}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scale = interpolate(frame, [0, durationInFrames], [1.06, 1.14]); // Ken-Burns push
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${scale})`}}>
        <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <VignetteBreath />
      <KineticCaptions lines={[telop]} style="maskslide" anchor="top" />
      <LowerThird primary={source} />
    </AbsoluteFill>
  );
};

export const TimbsB1: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      <Series.Sequence durationInFrames={BEATS.five}>
        <FootageBeat
          src="timbs/pexels_v_5243246.mp4"
          telop="No prison — home detention + probation"
          source="Sentencing record"
        />
      </Series.Sequence>
      <Series.Sequence durationInFrames={BEATS.six}>
        <PenaltyVsProperty
          left={{label: 'Maximum fine', value: 10000}}
          right={{label: 'Seized vehicle', value: 42000}}
          mode="currency"
          sourceLabel="Statutory maximum vs. seized value"
          jaNote="最大罰金1万ドル 対 没収された車 約4.2万ドル"
          dur={BEATS.six}
        />
      </Series.Sequence>
      <Series.Sequence durationInFrames={BEATS.seven}>
        <QuoteUnderExamination
          quote="grossly disproportionate"
          attribution="the Supreme Court"
          sourceLabel="Timbs v. Indiana"
          dur={BEATS.seven}
        />
      </Series.Sequence>
    </Series>
    {/* atmosphere bed + SAME narration as baseline_A (offset to the window in-point) */}
    <SoftGlow />
    <Audio src={staticFile('timbs/timbs_final_mix_v001.mp3')} startFrom={Math.round(WINDOW_START_SEC * FPS)} />
  </AbsoluteFill>
);
