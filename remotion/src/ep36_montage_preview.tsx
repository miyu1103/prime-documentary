/**
 * EP36 williams — MONTAGE preview (isolated entry; does NOT touch shared Root.tsx/CaseFilm).
 *
 * Chains the verified pre-built pieces in script order — canonical BrandOpening -> a hero
 * WilliamsScene (placeholder) -> the signature motion-graphics -> a closing WilliamsScene ->
 * canonical BrandEndcard, with GlitchCut transitions — to prove the animation track flows
 * end-to-end BEFORE Codex images land. When images arrive, the WilliamsScene `src` props are
 * filled and this logic maps 1:1 onto the real CaseFilm cuts (scene_plan.v001.json).
 *
 * Render: cd remotion && npx remotion render src/ep36_montage_preview.tsx Ep36Montage out/ep36_montage.mp4
 */
import React from 'react';
import {AbsoluteFill, Sequence, registerRoot, Composition} from 'remotion';
import {BRAND} from './brand';
import {BrandOpening, BrandEndcard} from './components/Bookends';
import {
  WilliamsScene,
  FaceMatchGrid,
  LineupLoop,
  BiasBars,
  CaseTimeline,
} from './components/williams';
import {GlitchCut} from './components/motionkit';

const FPS = BRAND.video.fps;

// beat = [component, durationInFrames]
const Montage: React.FC = () => {
  let t = 0;
  const at = (d: number) => {
    const from = t;
    t += d;
    return {from, durationInFrames: d};
  };
  const op = at(105);
  const hook = at(96);
  const grid = at(96);
  const loop = at(120);
  const bias = at(120);
  const timeline = at(150);
  const ending = at(96);
  const ed = at(96);

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Sequence {...op} name="OP">
        <BrandOpening
          seriesLabel="YOUR RIGHTS VS. THE MACHINE"
          title="The Algorithm Said It Was You"
          subtitle="Facial recognition · a wrongful arrest · one city's new rules"
        />
      </Sequence>

      <Sequence {...hook} name="S001-hook">
        <WilliamsScene treatment="pixel" placeholderLabel="S001" onScreen={['A BLURRY PHOTO.', "A COMPUTER'S GUESS."]} />
      </Sequence>

      <Sequence {...grid} name="S007-facematch">
        <FaceMatchGrid />
      </Sequence>

      <Sequence {...loop} name="S008-lineuploop">
        <LineupLoop />
      </Sequence>

      <Sequence {...bias} name="S010-biasbars">
        <BiasBars />
      </Sequence>

      <Sequence {...timeline} name="S013-timeline">
        <CaseTimeline />
      </Sequence>

      <Sequence {...ending} name="S030-ending">
        <WilliamsScene treatment="push" accent={BRAND.color.gold} placeholderLabel="S030" onScreen={['YOUR FACE IS A PASSWORD', "YOU CAN'T CHANGE"]} />
      </Sequence>

      <Sequence {...ed} name="ED">
        <BrandEndcard />
      </Sequence>

      {/* GlitchCut トランジション（境界に薄く重ねる） */}
      <Sequence from={hook.from - 7} durationInFrames={15} name="tx1">
        <GlitchCut dur={15} />
      </Sequence>
      <Sequence from={loop.from - 7} durationInFrames={15} name="tx2">
        <GlitchCut dur={15} />
      </Sequence>
      <Sequence from={ending.from - 7} durationInFrames={15} name="tx3">
        <GlitchCut dur={15} />
      </Sequence>
    </AbsoluteFill>
  );
};

const Root: React.FC = () => (
  <Composition id="Ep36Montage" component={Montage} durationInFrames={879} fps={FPS} width={BRAND.video.width} height={BRAND.video.height} />
);

registerRoot(Root);
