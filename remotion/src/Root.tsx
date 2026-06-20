import React from 'react';
import {Composition, Still} from 'remotion';
import {BRAND} from './brand';
import {Opening} from './compositions/Opening';
import {Episode, TEMPLATE_12MIN} from './compositions/Episode';
import {StyleTest} from './compositions/StyleTest';
import {Animatic, animaticDurationInFrames, durationInFramesFor} from './compositions/Animatic';
import {GIDEON_ANIMATIC, GIDEON_SCENE_IMG} from './data/gideon_animatic';
import {GideonPremium, gideonPremiumDurationInFrames} from './compositions/GideonPremium';
import {MappPremium, mappPremiumDurationInFrames} from './compositions/MappPremium';
import {MadoffPremium, madoffPremiumDurationInFrames} from './compositions/MadoffPremium';
import {ClipProof} from './compositions/ClipProof';
import {ColdOpen, MIRANDA_HOOK, hookDurationInFrames} from './compositions/ColdOpen';
import {ThumbConcept} from './compositions/ThumbConcept';
import {ThumbnailFrame} from './components/ThumbnailFrame';
import {RoughCut, roughCutDurationInFrames} from './compositions/RoughCut';
import {MAHANOY_ROUGHCUT} from './data/mahanoy_roughcut';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="RoughCut_mahanoy"
        component={RoughCut}
        durationInFrames={roughCutDurationInFrames(MAHANOY_ROUGHCUT)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{data: MAHANOY_ROUGHCUT}}
      />
      <Composition
        id="Opening"
        component={Opening}
        durationInFrames={Math.round(BRAND.video.fps * 2.5)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{channelName: 'Prime Documentary'}}
      />
      <Composition
        id="MirandaEpisode"
        component={Episode}
        durationInFrames={Math.round(BRAND.video.fps * 12 * 60)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          title: 'Why Do Police Read You Your Rights?',
          channelName: 'Prime Documentary',
          sections: TEMPLATE_12MIN,
        }}
      />
      <Composition
        id="GideonAnimatic"
        component={Animatic}
        durationInFrames={durationInFramesFor(GIDEON_ANIMATIC, BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          bgmSrc: null as string | null,
          scenes: GIDEON_ANIMATIC,
          sceneImg: GIDEON_SCENE_IMG,
        }}
      />
      <Composition
        id="GideonPremium"
        component={GideonPremium}
        durationInFrames={gideonPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MappPremium"
        component={MappPremium}
        durationInFrames={mappPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="MadoffPremium"
        component={MadoffPremium}
        durationInFrames={madoffPremiumDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
      />
      <Composition
        id="StyleTest"
        component={StyleTest}
        durationInFrames={BRAND.video.fps * 60}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{bgmSrc: 'bgm_placeholder.wav' as string | null}}
      />
      <Composition
        id="Animatic"
        component={Animatic}
        durationInFrames={animaticDurationInFrames(BRAND.video.fps)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{bgmSrc: 'bgm_placeholder.wav' as string | null}}
      />
      <Composition
        id="ClipProof"
        component={ClipProof}
        durationInFrames={Math.round(BRAND.video.fps * 5)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{
          src: 'proof_clip.mp4',
          hook: 'You have the right to remain silent.',
          citation: 'Miranda v. Arizona, 384 U.S. 436 (1966)',
          reconstruction: true,
        }}
      />
      <Composition
        id="ColdOpen"
        component={ColdOpen}
        durationInFrames={hookDurationInFrames(MIRANDA_HOOK)}
        fps={BRAND.video.fps}
        width={BRAND.video.width}
        height={BRAND.video.height}
        defaultProps={{beats: MIRANDA_HOOK}}
      />
      <Still
        id="ThumbConcept"
        component={ThumbConcept}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          kicker: 'MIRANDA v. ARIZONA',
          line1: 'Won.',
          line2: 'Still jailed.',
          sub: 'How 4 words rewrote every U.S. arrest',
          symbol: 'bars' as const,
        }}
      />
      <Still
        id="ThumbnailFrame"
        component={ThumbnailFrame}
        width={BRAND.thumb.width}
        height={BRAND.thumb.height}
        defaultProps={{
          title: 'Why Do Police Read You Your Rights?',
          backgroundSrc: null,
          variant: 'left' as const,
        }}
      />
    </>
  );
};
