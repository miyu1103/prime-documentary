/**
 * EP36 williams — OPENING preview (isolated entry, does NOT touch the shared Root.tsx).
 *
 * Renders the CANONICAL BrandOpening (remotion/src/components/Bookends.tsx) with EP36's
 * seriesLabel/title/subtitle. Per invariant 14 (OP/ED canonical = Bookends, do NOT fork)
 * and the owner directive (bespoke cyan openings are 未採用; existing taste only), this
 * reuses the house bookend as-is and only swaps the three text props.
 *
 * Preview/verify only — the real per-episode registration happens later inside the main
 * Root.tsx CaseFilm composition, wired carefully so it does not collide with the concurrent
 * worker's uncommitted Root.tsx changes.
 *
 * Render stills:
 *   cd remotion && npx remotion still src/ep36_opening_preview.tsx Ep36OpeningPreview out/ep36_op_f<N>.png --frame=<N>
 * Render mp4:
 *   cd remotion && npx remotion render src/ep36_opening_preview.tsx Ep36OpeningPreview out/ep36_opening.mp4
 */
import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';
import {BrandOpening, OPENING_SEC} from './components/Bookends';

const FPS = 30;

const Ep36Opening: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#000'}}>
    <BrandOpening
      seriesLabel="YOUR RIGHTS VS. THE MACHINE"
      title="The Algorithm Said It Was You"
      subtitle="Facial recognition · a wrongful arrest · one city's new rules"
    />
  </AbsoluteFill>
);

const Ep36PreviewRoot: React.FC = () => (
  <Composition
    id="Ep36OpeningPreview"
    component={Ep36Opening}
    durationInFrames={Math.round(OPENING_SEC * FPS)}
    fps={FPS}
    width={1920}
    height={1080}
  />
);

registerRoot(Ep36PreviewRoot);
