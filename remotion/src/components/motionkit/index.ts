/**
 * MOTIONKIT — reusable premium motion-graphics library (single import point).
 * Episode-agnostic components. Import from here: `import {VoteTally} from '../components/motionkit'`.
 * Every component takes an optional `dur?: number` (frames; default = full composition).
 * See CATALOG.md for the human-readable index + which case-types each fits.
 */

// --- v001: core grammar ---
export {KineticCaptions} from './KineticCaptions';
export {QuoteCard} from './QuoteCard';
export {ActTitle} from './ActTitle';
export {LowerThird} from './LowerThird';
export {HighlightRing} from './HighlightRing';
export {AnnotationArrow} from './AnnotationArrow';
export {Spotlight} from './Spotlight';
export {DocHighlight} from './DocHighlight';
export {RouteMap} from './RouteMap';
export {PinDropMap} from './PinDropMap';
export {RegionHighlightMap} from './RegionHighlightMap';
export {VoteTally} from './VoteTally';
export {ComparisonBars} from './ComparisonBars';
export {NumberTicker} from './NumberTicker';
export {MechanismReveal} from './MechanismReveal';
export {DustMotes, SoftGlow, FilmGrain, VignetteBreath} from './Atmospherics';

// --- v002: money & data storytelling ---
export {PriceCrashChart} from './PriceCrashChart';
export {MoneyFlow} from './MoneyFlow';
export {DonutReveal} from './DonutReveal';
export {PonziCurve} from './PonziCurve';
export {StackedProportion} from './StackedProportion';
export {MarketTicker} from './MarketTicker';

// --- v002: cinematic titles & transitions ---
export {CinematicTitle} from './CinematicTitle';
export {IrisTransition} from './IrisTransition';
export {GlitchCut} from './GlitchCut';
export {FocusPull} from './FocusPull';
export {TerminalType} from './TerminalType';

// --- v002: evidence & investigation ---
export {EvidenceCard} from './EvidenceCard';
export {StampReveal} from './StampReveal';
export {CorkboardWeb} from './CorkboardWeb';
export {RecordsScan} from './RecordsScan';
export {HeadlineStack} from './HeadlineStack';

// --- v002: time & process ---
export {CountdownClock} from './CountdownClock';
export {ProcessSteps} from './ProcessSteps';
export {YearSweep} from './YearSweep';
export {RadialGauge} from './RadialGauge';

// --- v002: premium dynamic backdrops / overlays ---
export {AuroraField} from './AuroraField';
export {DepthParticles} from './DepthParticles';
export {LightRays} from './LightRays';
export {GridWarp} from './GridWarp';
