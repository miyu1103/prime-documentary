// EP36 williams — code-built motion-graphics barrel (image-independent).
// New EP36-specific signature graphics that do not exist in motionkit (invariant 14:
// FaceMatchGrid / BiasBars / CaseTimeline are genuinely missing capabilities).
// Reused motionkit parts (NumberTicker, PinDropMap, KineticCaptions, ActTitle,
// EvidenceCard, StampReveal, beds/overlays) are imported directly where used.
export {WilliamsScene} from './WilliamsScene';
export type {Treatment} from './WilliamsScene';
export {FaceMatchGrid} from './FaceMatchGrid';
export {BiasBars} from './BiasBars';
export {CaseTimeline} from './CaseTimeline';
export {LineupLoop} from './LineupLoop';
export {DatasetImbalance} from './DatasetImbalance';
