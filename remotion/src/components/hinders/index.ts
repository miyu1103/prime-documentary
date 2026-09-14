// =====================================================================
// EP35 "hinders" — FigureBeats barrel (27 figures, 8 heroes).
//
//   theme.tsx     shared palette (3 lanes) / deterministic rng / primitives
//   figures.tsx   22 figures: 3 Blender-hero OffthreadVideo wrappers (F2/F5/F20)
//                 + 3 bespoke new (F2b/F5b/F14c) + 16 MOTIONKIT-preset wrappers
//   heroes3d.tsx  5 @remotion/three heroes (F3/F11/F14/F14b/F15)
//
// The film builder (別担当) imports figures by name or via FIGURE_REGISTRY.
// Every figure is `React.FC<FigureProps>` — pass {lane?, accent?, dur}.
// =====================================================================
import type React from 'react';
import type {FigureProps} from './theme';

export * from './theme';
export * from './figures';
export * from './heroes3d';

import {
  Register38Years,
  BSAOriginFlow,
  StructuringExplainer,
  ThresholdBreach,
  FrozenAccount,
  BurdenShiftScale,
  CaseCaptionNameplate,
  WalkAwayTally,
  CivilForfeitureInvert,
  CoinFlip,
  HeadlineKinetic,
  SeizureVsReturn,
  DismissedStamp,
  McLellanStore,
  LegalSourceBars,
  FeeDeniedCard,
  ThreatReframeCard,
  FeeContrastCard,
  CongressHearingCard,
  RESPECTActNode,
  CaroleAfterCard,
  InfoDensitySpine,
} from './figures';
import {
  ThresholdMeter,
  PolicyReversalTimeline,
  McLellanParallel,
  McLellanLedger,
  TIGTADots,
} from './heroes3d';

/** F-id → component, so the film builder can address a beat by design id. */
export const FIGURE_REGISTRY: Record<string, React.FC<FigureProps>> = {
  F1: Register38Years,
  F2: BSAOriginFlow, // ★hero (Blender fluid)
  F2b: StructuringExplainer,
  F3: ThresholdMeter, // ★hero (@remotion/three)
  F4: ThresholdBreach,
  F5: FrozenAccount, // ★hero (Blender ice-fracture)
  F5b: BurdenShiftScale,
  F6: CaseCaptionNameplate,
  F7: WalkAwayTally,
  F8: CivilForfeitureInvert,
  F9: CoinFlip,
  F10: HeadlineKinetic,
  F11: PolicyReversalTimeline, // ★hero (@remotion/three)
  F12: SeizureVsReturn,
  F13: DismissedStamp,
  F14: McLellanParallel, // ★hero (@remotion/three)
  F14b: McLellanLedger, // ★hero (@remotion/three)
  F14c: McLellanStore,
  F15: TIGTADots, // ★hero (@remotion/three)
  F15b: LegalSourceBars,
  F16: FeeDeniedCard,
  F17: ThreatReframeCard,
  F17b: FeeContrastCard,
  F18: CongressHearingCard,
  F19: RESPECTActNode,
  F20: CaroleAfterCard, // ★hero (Blender Cycles room dolly)
  F21: InfoDensitySpine,
};

/** The 8 super-heavy hero beats (manifest §SH). */
export const HERO_FIGURE_IDS = ['F2', 'F3', 'F5', 'F11', 'F14', 'F14b', 'F15', 'F20'] as const;
