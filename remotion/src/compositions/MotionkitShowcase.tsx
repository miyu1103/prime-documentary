/**
 * MotionkitShowcase — a self-contained sizzle reel of the MOTIONKIT library.
 * Straight-cut tour of the components (driven by real presets) with a FilmGrain
 * bed and a few GlitchCut punches. No external media; fully deterministic.
 */
import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';

import {
  CinematicTitle, ActTitle, NumberTicker, VoteTally, ComparisonBars, PriceCrashChart,
  MoneyFlow, DonutReveal, PonziCurve, RadialGauge, RouteMap, PinDropMap,
  RegionHighlightMap, CorkboardWeb, ProcessSteps, TerminalType, RecordsScan,
  EvidenceCard, StampReveal, QuoteCard, HeadlineStack, YearSweep, CountdownClock,
  MechanismReveal, FilmGrain, GlitchCut,
} from '../components/motionkit';
import {
  actTitlePresets, numberTickerPresets, voteTallyPresets, comparisonBarsPresets,
  priceCrashChartPresets, moneyFlowPresets, donutRevealPresets, ponziCurvePresets,
  radialGaugePresets, routeMapPresets, pinDropMapPresets, regionHighlightMapPresets,
  corkboardWebPresets, processStepsPresets, terminalTypePresets, recordsScanPresets,
  evidenceCardPresets, stampRevealPresets, quoteCardPresets, headlineStackPresets,
  yearSweepPresets, countdownClockPresets, mechanismRevealPresets,
} from '../components/motionkit/presets';

// Pick the i-th preset from an object and drop any `dur` so each scene animates
// to fill its own Sequence window (presets author dur at varying fps).
const val = (o: Record<string, unknown>, i = 0): Record<string, unknown> => {
  const vals = Object.values(o) as Record<string, unknown>[];
  const {dur, ...rest} = (vals[i % vals.length] ?? {}) as Record<string, unknown>;
  void dur;
  return rest;
};

type Seg = {C: React.FC<any>; p: Record<string, unknown>; d: number};

const SCENES: Seg[] = [
  {C: ActTitle, p: {kicker: 'The Motion Library', title: 'MOTIONKIT', index: 1}, d: 80},
  {C: NumberTicker, p: val(numberTickerPresets, 0), d: 80},
  {C: VoteTally, p: val(voteTallyPresets, 4), d: 85},
  {C: ComparisonBars, p: val(comparisonBarsPresets, 0), d: 85},
  {C: PriceCrashChart, p: val(priceCrashChartPresets, 0), d: 95},
  {C: MoneyFlow, p: val(moneyFlowPresets, 0), d: 95},
  {C: DonutReveal, p: val(donutRevealPresets, 0), d: 85},
  {C: PonziCurve, p: val(ponziCurvePresets, 0), d: 90},
  {C: RadialGauge, p: val(radialGaugePresets, 0), d: 82},
  {C: RouteMap, p: val(routeMapPresets, 0), d: 90},
  {C: PinDropMap, p: val(pinDropMapPresets, 0), d: 85},
  {C: RegionHighlightMap, p: val(regionHighlightMapPresets, 0), d: 85},
  {C: CorkboardWeb, p: val(corkboardWebPresets, 0), d: 95},
  {C: ProcessSteps, p: val(processStepsPresets, 0), d: 100},
  {C: TerminalType, p: val(terminalTypePresets, 0), d: 95},
  {C: RecordsScan, p: val(recordsScanPresets, 0), d: 90},
  {C: EvidenceCard, p: val(evidenceCardPresets, 0), d: 85},
  {C: StampReveal, p: val(stampRevealPresets, 0), d: 72},
  {C: QuoteCard, p: val(quoteCardPresets, 0), d: 95},
  {C: HeadlineStack, p: val(headlineStackPresets, 0), d: 92},
  {C: YearSweep, p: val(yearSweepPresets, 0), d: 85},
  {C: CountdownClock, p: val(countdownClockPresets, 0), d: 82},
  {C: MechanismReveal, p: {kind: 'gears'}, d: 85},
];

const INTRO = 90;
const OUTRO = 96;

// Cut boundaries (frames) where a body scene begins, for GlitchCut punches.
const bodyStart = INTRO;

export const motionkitShowcaseDuration = (): number =>
  INTRO + SCENES.reduce((a, s) => a + s.d, 0) + OUTRO;

export const MotionkitShowcase: React.FC = () => {
  const {durationInFrames} = useVideoConfig();

  let acc = bodyStart;
  const scenes = SCENES.map((s, i) => {
    const from = acc;
    acc += s.d;
    return (
      <Sequence key={i} from={from} durationInFrames={s.d} name={s.C.name || `scene-${i}`}>
        <s.C {...s.p} />
      </Sequence>
    );
  });

  // GlitchCut punches at a few section boundaries (overlay, transparent).
  const punchAt = [
    bodyStart + SCENES.slice(0, 4).reduce((a, s) => a + s.d, 0),
    bodyStart + SCENES.slice(0, 9).reduce((a, s) => a + s.d, 0),
    bodyStart + SCENES.slice(0, 16).reduce((a, s) => a + s.d, 0),
  ];

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <Sequence from={0} durationInFrames={INTRO} name="intro">
        <CinematicTitle title="MOTIONKIT" subtitle="40 components · 926 presets" />
      </Sequence>

      {scenes}

      {punchAt.map((f, i) => (
        <Sequence key={`p${i}`} from={f - 7} durationInFrames={14} name={`punch-${i}`}>
          <GlitchCut dur={14} />
        </Sequence>
      ))}

      <Sequence from={acc} durationInFrames={OUTRO} name="outro">
        <CinematicTitle title="PRIME DOCUMENTARY" subtitle="the moving explanation" />
      </Sequence>

      {/* Filmic cohesion bed over the whole reel. */}
      <Sequence from={0} durationInFrames={durationInFrames} name="grain">
        <FilmGrain />
      </Sequence>
    </AbsoluteFill>
  );
};
