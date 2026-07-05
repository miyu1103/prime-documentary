# MOTIONKIT catalog

Reusable premium motion-graphics components. Import from the barrel: `import {X} from '../components/motionkit'`.
Every component takes optional `dur?: number` (frames; default = full composition). Colors are BRAND tokens only.
**Before building a new visual, check this list first — do not re-implement (CLAUDE invariant 14).**

Legend: **SCENE** = full-screen, renders own dark backdrop · **OVERLAY** = transparent, layers over footage/stills.

## v001 — core grammar
| Component | Kind | Use for | Key props |
|---|---|---|---|
| KineticCaptions | OVERLAY | kinetic lower-third captions (wordpop/maskslide/emphasis) | `lines, style?, emphasisWords?` |
| QuoteCard | SCENE | verbatim quotes / testimony | `quote, attribution` |
| ActTitle | SCENE | chapter / act title card | `kicker?, title, index?` |
| LowerThird | OVERLAY | broadcast name/role strip | `primary, secondary?, accent?` |
| HighlightRing | OVERLAY | ring a detail on real footage | `cx, cy, r, label?` |
| AnnotationArrow | OVERLAY | point at a thing | `from, to, label?` |
| Spotlight | OVERLAY | darken all but a detail | `cx, cy, r, dim?` |
| DocHighlight | OVERLAY | underline/box/redact document regions | `rects, mode?` |
| RouteMap | SCENE | route between places | `pins` |
| PinDropMap | SCENE | "happened in N places" | `pins` |
| RegionHighlightMap | SCENE | "it depends where you are" | `label?, pattern?` |
| VoteTally | SCENE | court votes (5–4, 8–1) | `majority, dissent, label?` |
| ComparisonBars | SCENE | A vs B contrast | `items` |
| NumberTicker | SCENE | hero stat count-up | `value, prefix?, suffix?, decimals?, topLabel?, label?` |
| MechanismReveal | SCENE | closingdoor / gears / faultsplit | `kind` |
| DustMotes / SoftGlow / FilmGrain / VignetteBreath | OVERLAY | always-alive atmosphere bed | (all optional) |

## v002 — money & data storytelling
| Component | Kind | Use for | Key props |
|---|---|---|---|
| PriceCrashChart | SCENE | stock/price rise → crash | `series?, label?, crashLabel?` |
| MoneyFlow | SCENE | follow-the-money between entities | `nodes, edges` |
| DonutReveal | SCENE | proportion breakdown (ring) | `slices, centerLabel?` |
| PonziCurve | SCENE | promised vs actual → collapse | `peakLabel?, collapseLabel?` |
| StackedProportion | SCENE | 100% single-bar breakdown | `parts, title?` |
| MarketTicker | OVERLAY | broadcast finance ticker strip | `items` |

## v002 — cinematic titles & transitions
| Component | Kind | Use for | Key props |
|---|---|---|---|
| CinematicTitle | SCENE | grand hero title | `title, subtitle?` |
| IrisTransition | OVERLAY | iris in/out wipe | `mode?, shape?` |
| GlitchCut | OVERLAY | digital tension cut | (dur) |
| FocusPull | OVERLAY | rack-focus transition | (dur) |
| TerminalType | SCENE | console / records typing | `lines, prompt?` |

## v002 — evidence & investigation
| Component | Kind | Use for | Key props |
|---|---|---|---|
| EvidenceCard | SCENE | exhibit card slam-in | `tag?, caption?` |
| StampReveal | SCENE | GUILTY/CONVICTED/SEALED stamp | `text, color?` |
| CorkboardWeb | SCENE | conspiracy board + red string | `nodes, links` |
| RecordsScan | SCENE | searching the records | `lines?, highlightIndex?` |
| HeadlineStack | SCENE | press-coverage montage | `headlines` |

## v002 — time & process
| Component | Kind | Use for | Key props |
|---|---|---|---|
| CountdownClock | SCENE | time-pressure countdown | `from, label?` |
| ProcessSteps | SCENE | how-it-worked numbered flow | `steps` |
| YearSweep | SCENE | passage of time | `from, to, label?` |
| RadialGauge | SCENE | risk/probability dial | `value, max?, label?` |

## v002 — premium dynamic backdrops / overlays
| Component | Kind | Use for | Key props |
|---|---|---|---|
| AuroraField | SCENE/BED | flowing aurora backdrop | (dur) |
| DepthParticles | SCENE/BED | parallax depth particle field | `count?` |
| LightRays | OVERLAY | volumetric god-rays | `color?` |
| GridWarp | SCENE/BED | Tron data-space grid | (dur) |

---
Verified: `npx tsc --noEmit` exit 0 · still-render smoke pass for all 40 (2 rounds).
Next phase: preset catalog (ready-made prop fills per component) → hundreds of drop-in "素材" variations.
