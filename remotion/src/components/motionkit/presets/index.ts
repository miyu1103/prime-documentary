/**
 * MOTIONKIT preset catalog — ready-made prop fills for every component (~926 total).
 * Each object is typed `satisfies Record<string, ComponentProps<typeof Component>>`,
 * so every preset is compile-time-checked against the real component props.
 *
 * Usage:
 *   import {VoteTally} from '../components/motionkit';
 *   import {voteTallyPresets} from '../components/motionkit/presets';
 *   <VoteTally {...voteTallyPresets['5-4-landmark']} />
 */

// v001 core grammar
export {kineticCaptionsPresets} from './KineticCaptions.presets';
export {quoteCardPresets} from './QuoteCard.presets';
export {actTitlePresets} from './ActTitle.presets';
export {lowerThirdPresets} from './LowerThird.presets';
export {highlightRingPresets} from './HighlightRing.presets';
export {annotationArrowPresets} from './AnnotationArrow.presets';
export {spotlightPresets} from './Spotlight.presets';
export {docHighlightPresets} from './DocHighlight.presets';
export {routeMapPresets} from './RouteMap.presets';
export {pinDropMapPresets} from './PinDropMap.presets';
export {regionHighlightMapPresets} from './RegionHighlightMap.presets';
export {voteTallyPresets} from './VoteTally.presets';
export {comparisonBarsPresets} from './ComparisonBars.presets';
export {numberTickerPresets} from './NumberTicker.presets';
export {mechanismRevealPresets} from './MechanismReveal.presets';
export {
  dustMotesPresets,
  softGlowPresets,
  filmGrainPresets,
  vignetteBreathPresets,
} from './Atmospherics.presets';

// v002 money & data
export {priceCrashChartPresets} from './PriceCrashChart.presets';
export {moneyFlowPresets} from './MoneyFlow.presets';
export {donutRevealPresets} from './DonutReveal.presets';
export {ponziCurvePresets} from './PonziCurve.presets';
export {stackedProportionPresets} from './StackedProportion.presets';
export {marketTickerPresets} from './MarketTicker.presets';

// v002 titles & transitions
export {cinematicTitlePresets} from './CinematicTitle.presets';
export {irisTransitionPresets} from './IrisTransition.presets';
export {glitchCutPresets} from './GlitchCut.presets';
export {focusPullPresets} from './FocusPull.presets';
export {terminalTypePresets} from './TerminalType.presets';

// v002 evidence & investigation
export {evidenceCardPresets} from './EvidenceCard.presets';
export {stampRevealPresets} from './StampReveal.presets';
export {corkboardWebPresets} from './CorkboardWeb.presets';
export {recordsScanPresets} from './RecordsScan.presets';
export {headlineStackPresets} from './HeadlineStack.presets';

// v002 time & process
export {countdownClockPresets} from './CountdownClock.presets';
export {processStepsPresets} from './ProcessSteps.presets';
export {yearSweepPresets} from './YearSweep.presets';
export {radialGaugePresets} from './RadialGauge.presets';

// v002 dynamic backdrops / overlays
export {auroraFieldPresets} from './AuroraField.presets';
export {depthParticlesPresets} from './DepthParticles.presets';
export {lightRaysPresets} from './LightRays.presets';
export {gridWarpPresets} from './GridWarp.presets';
