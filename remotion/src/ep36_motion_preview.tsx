/**
 * EP36 williams — MOTION-GRAPHICS preview (isolated entry; does NOT touch shared Root.tsx).
 *
 * Pre-built code-built motion-graphics that need NO Codex images, so that once the images
 * arrive only assembly remains. Renders each as its own composition for smoke/visual QC.
 *   - Custom EP36 signature graphics (new; not in motionkit): FaceMatchGrid, BiasBars, CaseTimeline.
 *   - Reused motionkit parts wired with EP36 grade-A content: NumberTicker (~30 hours held),
 *     PinDropMap (one city, new rules).
 *
 * Render one:  cd remotion && npx remotion render src/ep36_motion_preview.tsx <CompId> out/<name>.mp4
 * CompIds: Ep36FaceMatchGrid | Ep36BiasBars | Ep36CaseTimeline | Ep36HeldCounter | Ep36OneCityMap
 */
import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';
import {BRAND} from './brand';
import {FaceMatchGrid, BiasBars, CaseTimeline, LineupLoop, DatasetImbalance} from './components/williams';
import {NumberTicker, PinDropMap, ActTitle, StampReveal, KineticCaptions} from './components/motionkit';

const FPS = BRAND.video.fps;
const W = BRAND.video.width;
const H = BRAND.video.height;

// Reused motionkit parts wired with EP36 grade-A content (verify they work here).
const HeldCounter: React.FC = () => (
  <NumberTicker value={30} topLabel="HOURS IN A CELL" label="No charge. No crime. A face-match was enough." />
);
const OneCityMap: React.FC = () => (
  <PinDropMap pins={[{x: 0.72, y: 0.34, label: 'ONE CITY · NEW RULES'}]} />
);
const ActTwoTitle: React.FC = () => <ActTitle kicker="CHAPTER TWO" title="THE COMPUTER PICKED HIM" index={2} />;
const ChargesDropped: React.FC = () => <StampReveal text="CHARGES DROPPED" color="#3E8E5A" />;
// KineticCaptions is a transparent OVERLAY — put it over a dark fill for the preview.
const KineticSample: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <KineticCaptions lines={['MATCHED BY A MACHINE', 'ARRESTED BY MISTAKE']} style="maskslide" />
  </AbsoluteFill>
);

const Ep36MotionRoot: React.FC = () => (
  <>
    {/* EP36 signature graphics (new) */}
    <Composition id="Ep36FaceMatchGrid" component={FaceMatchGrid} durationInFrames={100} fps={FPS} width={W} height={H} />
    <Composition id="Ep36BiasBars" component={BiasBars} durationInFrames={130} fps={FPS} width={W} height={H} />
    <Composition id="Ep36CaseTimeline" component={CaseTimeline} durationInFrames={165} fps={FPS} width={W} height={H} />
    <Composition id="Ep36LineupLoop" component={LineupLoop} durationInFrames={130} fps={FPS} width={W} height={H} />
    <Composition id="Ep36DatasetImbalance" component={DatasetImbalance} durationInFrames={120} fps={FPS} width={W} height={H} />
    {/* Reused motionkit (verified with EP36 content) */}
    <Composition id="Ep36HeldCounter" component={HeldCounter} durationInFrames={90} fps={FPS} width={W} height={H} />
    <Composition id="Ep36OneCityMap" component={OneCityMap} durationInFrames={130} fps={FPS} width={W} height={H} />
    <Composition id="Ep36ActTitle" component={ActTwoTitle} durationInFrames={90} fps={FPS} width={W} height={H} />
    <Composition id="Ep36StampCharges" component={ChargesDropped} durationInFrames={80} fps={FPS} width={W} height={H} />
    <Composition id="Ep36KineticSample" component={KineticSample} durationInFrames={110} fps={FPS} width={W} height={H} />
  </>
);

registerRoot(Ep36MotionRoot);
