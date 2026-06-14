import React from 'react';
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  interpolate,
} from 'remotion';
import {BRAND} from '../brand';
import {CameraRig, Vignette, Particles} from '../components/Motion';
import {Grain} from '../components/Grain';

/**
 * Proof-of-concept: real video clip with cinematic motion layer.
 * Clip must be at public/proof_clip.mp4 before rendering.
 * Invariant 11 still applies — never present as authentic documentary evidence.
 */

const Overlay: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 20], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(to top, rgba(10,10,12,0.65) 0%, transparent 38%, rgba(10,10,12,0.30) 100%)',
      opacity: o,
    }} />
  );
};

const Label: React.FC = () => {
  const f = useCurrentFrame();
  const o = interpolate(f, [8, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-start', padding: '0 48px 48px'}}>
      <div style={{
        opacity: o,
        color: `${BRAND.color.silver}cc`,
        fontFamily: BRAND.font.body,
        fontSize: 18,
        letterSpacing: 2,
        textTransform: 'uppercase',
        borderLeft: `3px solid ${BRAND.color.gold}`,
        paddingLeft: 12,
      }}>
        Reconstruction — symbolic reference only
      </div>
    </AbsoluteFill>
  );
};

export const ClipProof: React.FC = () => {
  return (
    <AbsoluteFill style={{background: BRAND.color.ink}}>
      <CameraRig seed="clip-proof" intensity={0.6}>
        <AbsoluteFill>
          <OffthreadVideo
            src={staticFile('proof_clip.mp4')}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
        </AbsoluteFill>
      </CameraRig>
      <Overlay />
      <Vignette />
      <Particles count={18} seed="cp" />
      <Label />
      <Grain opacity={0.06} />
    </AbsoluteFill>
  );
};

// クリップの実尺: 5.208s（ffprobe 計測）
export const CLIP_PROOF_DURATION_SEC = 5.208;
