import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {CashStack} from '../components/aircash/CashStack';
import {BurdenFlipScale} from '../components/aircash/BurdenFlipScale';
import {SignSwapMorph} from '../components/aircash/SignSwapMorph';
import {CarryOnXrayScan} from '../components/aircash/CarryOnXrayScan';
import {CheckpointConvergeMap} from '../components/aircash/CheckpointConvergeMap';
import {ReportThresholdMeter} from '../components/aircash/ReportThresholdMeter';
import {ReturnLedgerMotion} from '../components/aircash/ReturnLedgerMotion';
import {BRAND} from '../brand';

/**
 * AircashFigTest — smoke-test harness for the 7 EP34 rolin bespoke figure components.
 * Each figure plays full-frame for BEAT seconds so a still-render at any beat's mid-point proves
 * the component renders (no runtime error) and its motion reads. Dev/verification only — not shipped.
 */
const BEAT = 6; // seconds per figure

export const AircashFigTest: React.FC = () => {
  const {fps} = useVideoConfig();
  const d = Math.round(BEAT * fps);
  const figs: React.ReactNode[] = [
    <CashStack dur={d} />,
    <BurdenFlipScale dur={d} />,
    <SignSwapMorph dur={d} />,
    <CarryOnXrayScan dur={d} />,
    <CheckpointConvergeMap dur={d} />,
    <ReportThresholdMeter dur={d} />,
    <ReturnLedgerMotion dur={d} />,
  ];
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {figs.map((f, i) => (
        <Sequence key={i} from={i * d} durationInFrames={d} name={`fig-${i}`}>
          {f}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const AIRCASH_FIG_TEST_FRAMES = 7 * Math.round(BEAT * BRAND.video.fps);
