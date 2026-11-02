# Premium shotlist — PD-2026-032-carsearch v001

Expands `scene_plan.v001.json` into a first-assembly target and locks the **perceptual motion budget** (EP32_carsearch_DESIGN.v001 §3): depth ≥40% of still cuts, moving FigureBeats ≥6, hero motion surfaces ≥2, **~2.2s average cut** (fast), and **ForcefulCut transitions only** (push / slide / zoompunch / whip — the gold vertical-sweep `WipeTransition` is banned). It preserves the locked script and maps every shot to the approved scene/span structure. No real-person likeness. All AI reenactments are symbolic reconstruction and must be rights-registered before edit use.

**Target runtime:** 690s · **Target cuts:** 314 · **Avg cut:** 690 / 314 = 2.20s.
**Source key:** `COD` = Codex/SDXL symbolic still (S0NN) · `GFX` = Remotion motion-graphic (carsearch / motionkit component) · `FTG` = commercial factory b-roll (eyeballed) · `DEPTH` = DepthStill depth-parallax on a still · `M` = motion treatment (parallax / Ken Burns / graphic-anim) · `KIN` = kinetic type · `AMB/SFX` = audio cue. The **cuts** column is how many ~2.2s cuts that row subdivides into in the final assembly (variant crops / graphic sub-beats).

---

## HOOK — S001 (10s · 4 cuts · in: hard cut from black · out: whip)

| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S001 | COD S001 + DEPTH | night traffic stop, trunk lifting open, red-blue on wet asphalt | depth parallax | 1 | — |
| S001 | COD S002 + DEPTH | quiet suburban driveway at dusk | depth parallax | 1 | — |
| S001 | GFX BrightLine `draw` | the line begins between a car and a house **(HERO surface #1)** | graphic-anim | 1 | A HUNDRED YEARS |
| S001 | GFX BrightLine `slam`-preview + KIN | line snaps; kinetic slam-in | Trail blur | 1 | ONE LINE THEY CAN'T CROSS |

## OPENING — S002 (18s · 7 cuts · in: zoompunch · out: push)

| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S002 | GFX BrandOpening | gold canonical opening + title | graphic-anim | 3 | CAN THE POLICE SEARCH YOUR CAR? |
| S002 | GFX RouteMap | 1925 → 2018 sweep across a stylized map | graphic-anim | 2 | — |
| S002 | GFX CaseTimeline preview | dots seed 1925 and 2018, ending on the bright line | graphic-anim | 2 | — |

## ACT I — THE HUNDRED-YEAR RULE

### S003 (26s · 12 cuts · in: push · out: slide)
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S003 | FTG warrant document macro | a judge's signature, probable cause written down | ken burns | 2 | — |
| S003 | COD S036 + DEPTH | the porch — a house wrapped in a protective glow | depth parallax | 3 | HOUSE = WARRANT |
| S003 | GFX CurtilageShield-hint | the home's outline glows | graphic-anim | 3 | — |
| S003 | COD S036 var + DEPTH | tighter porch/window detail | depth parallax | 1 | CAR = ? |
| S003 | GFX CaseTimeline `1925` | timeline snaps back to the 1925 dot | graphic-anim | 3 | 1925 |

### S004 (40s · 18 cuts · in: slide · out: zoompunch) — Carroll / 68 bottles
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S004 | COD S004 + DEPTH | 1920s automobile on a dark highway, headlights in fog | depth parallax | 2 | 1925 · PROHIBITION |
| S004 | COD S027 + DEPTH | very wide lonely 1920s highway, one small car | depth parallax | 2 | — |
| S004 | COD S028 | the tail car following at a distance | ken burns | 2 | — |
| S004 | FTG vintage headlight / night road | ambient period road | video native | 3 | — |
| S004 | COD S006 + DEPTH | gloved hands tearing the seat upholstery | depth parallax | 3 | — |
| S004 | FTG fabric tear macro | ripped upholstery detail | video native | 1 | — |
| S004 | GFX NumberTicker `0→68` | counter climbs as bottles are pulled | graphic-anim | 3 | 68 BOTTLES · 68 |
| S004 | COD S029 + DEPTH | one bottle held up to the light | depth parallax | 2 | — |

### S005 (22s · 10 cuts · in: push · out: push) — to the Court
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S005 | COD S008 + DEPTH | 1925 marble courthouse, low dramatic angle | depth parallax | 3 | — |
| S005 | COD S030 | gavel on an empty bench, cold shaft of light | ken burns | 3 | — |
| S005 | GFX CitationLowerThird | case citation card | graphic-anim | 2 | CARROLL v. UNITED STATES · 1925 |
| S005 | COD S009 | HOUSE \| CAR split forms | ken burns | 2 | — |

### S006 (46s · 20 cuts · in: push · out: zoompunch) — core holding
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S006 | COD S009 + DEPTH | house holding still vs car streaking away | depth parallax | 2 | — |
| S006 | FTG car accelerating off at night | the car flees the frame | video native | 4 | — |
| S006 | GFX QuoteCard (Taft) | the jurisdiction line types on, attributed | graphic-anim | 6 | "quickly moved out of the jurisdiction" |
| S006 | GFX KineticType + CurtilageShield | THE AUTOMOBILE EXCEPTION locks; house keeps shield, car shield thins | Trail blur | 8 | THE AUTOMOBILE EXCEPTION |

### S007 (28s · 13 cuts · in: zoompunch · out: whip) — open loop
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S007 | GFX PinDropMap | a single stop multiplies into a night grid | graphic-anim | 5 | — |
| S007 | FTG aerial night roads | scale of everyday stops | video native | 4 | — |
| S007 | GFX KineticType lock | PROBABLE CAUSE ignites and locks (open-loop marker) | Trail blur | 4 | PROBABLE CAUSE |

## ACT II — WHAT "PROBABLE CAUSE" MEANS

### S008 (32s · 15 cuts · in: whip · out: push) — myth correction
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S008 | COD S010 + DEPTH | officer torso/flashlight at a driver's window, no face | depth parallax | 2 | — |
| S008 | FTG routine traffic stop | ordinary stop bed | video native | 2 | — |
| S008 | GFX KineticType stamp | red NOT stamps over the stop | Trail blur | 3 | NOT A BLANK CHECK |
| S008 | GFX ProbableCauseMeter `stall` | a HUNCH bar stalls below the line | graphic-anim | 5 | A HUNCH ISN'T ENOUGH |
| S008 | COD S026 + DEPTH + GFX HighlightRing | driver POV; ring on a busted taillight | depth + graphic | 3 | — |

### S009 (30s · 14 cuts · in: push · out: slide) — clearing the bar
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S009 | GFX ProbableCauseMeter `cross` | evidence chips push the fill across; threshold locks gold | graphic-anim | 9 | PLAIN VIEW · K-9 ALERT · ADMISSION |
| S009 | COD S011 + DEPTH | a plain-view item / glovebox latch | depth parallax | 2 | — |
| S009 | GFX KineticType | chips lock in | Trail blur | 3 | — |

### S010 (30s · 14 cuts · in: slide · out: push) — scope reach
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S010 | GFX CarCutaway `all` | GLOVEBOX / TRUNK / BACK SEAT / A ZIPPED BAG light zone-by-zone | graphic-anim | 9 | GLOVEBOX · TRUNK · ANY CONTAINER |
| S010 | COD S012 + DEPTH | open trunk with a duffel and a shoebox | depth parallax | 2 | — |
| S010 | FTG hand pulling a bag | container reached | video native | 2 | — |
| S010 | COD S032 | gloved hand lifting a zipped bag from the back seat | ken burns | 1 | — |

### S011 (46s · 20 cuts · in: push · out: push) — scope as leash
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S011 | GFX CarCutaway `big` | only TRUNK + BACK SEAT glow (a big item can't hide small) | graphic-anim | 7 | SCOPE = THE OBJECT |
| S011 | GFX CarCutaway `small` | whole car incl. CONSOLE / ASHTRAY lights | graphic-anim | 7 | — |
| S011 | GFX DiagramFlow checklist | readily-mobile ✓ / probable-cause ✓ → permitted; third emergency box absent | graphic-anim | 2 | NO EXTRA EMERGENCY NEEDED |
| S011 | COD S012 + DEPTH | trunk/console detail | depth parallax | 2 | — |
| S011 | FTG console + pill bottle | small container contrast | video native | 2 | — |

### S012 (38s · 17 cuts · in: push · out: zoompunch) — rehook
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S012 | COD S013 + DEPTH | aerial night highway, thousands of lit cars | depth parallax | 5 | — |
| S012 | FTG aerial highway night | ambient scale bed | video native | 4 | — |
| S012 | COD S013 var + DEPTH | slow pull-back on the sea of cars | depth parallax | 3 | — |
| S012 | GFX BrightLine `hold` + KIN | motif flickers at the frame edge | graphic-anim | 5 | WHERE DOES IT STOP? |

## ACT III — THE MOTORCYCLE UNDER THE TARP

### S013 (35s · 16 cuts · in: whip · out: push) — turn to Virginia
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S013 | COD S014 + DEPTH | orange-and-black motorcycle blurs past a patrol car | depth parallax | 3 | VIRGINIA |
| S013 | COD S033 + DEPTH | motorcycle tank detail, chrome catching light | depth parallax | 2 | THE BIKE THAT GOT AWAY |
| S013 | GFX PinDropMap | pin drops on a residential address | graphic-anim | 4 | — |
| S013 | COD S015 + DEPTH | the quiet house, a covered shape in the driveway | depth parallax | 3 | — |
| S013 | COD S034 | wide quiet residential street at blue hour | ken burns | 1 | — |
| S013 | FTG suburban dusk | ambient hush | video native | 3 | — |

### S014 (40s · 18 cuts · in: push · out: slide) — the tarp
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S014 | COD S017 + DEPTH | boots walking up the residential driveway | depth parallax | 3 | — |
| S014 | COD S016 + DEPTH | a hand peeling back the tarp, chrome revealed | depth parallax | 3 | — |
| S014 | COD S035 + DEPTH | tarp half-lifted, a slice of orange/chrome | depth parallax | 2 | — |
| S014 | GFX KineticType chip | plate/number run | Trail blur | 3 | STOLEN — CONFIRMED |
| S014 | FTG tarp / wind ambient | light wind on the cover | video native | 3 | — |
| S014 | COD S017 var + GFX HighlightRing | replay on a public curb, green check | depth + graphic | 4 | ON A STREET = LEGAL |

### S015 (36s · 16 cuts · in: slide · out: zoompunch) — the stakes
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S015 | GFX KineticType | the automobile-exception rule stretches up the driveway | graphic-anim | 4 | — |
| S015 | GFX CarKeyLock | a car-shaped key turns in a house-door lock **(HERO surface #2)** | Trail blur | 10 | A CAR = A KEY TO YOUR HOME? |
| S015 | COD S018 + DEPTH | the home's edge (curtilage concept) | depth parallax | 1 | — |
| S015 | FTG house wall at dusk | ambient wall | video native | 1 | — |

### S016 (38s · 16 cuts · in: zoompunch · out: push) — the payoff
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S016 | GFX BrightLine `slam` | the line SLAMS across the driveway — the Court said NO **(HERO surface #3)** | Trail blur + flash | 5 | THE COURT SAID NO |
| S016 | GFX VoteTally `8-1` | 8 gold + 1 muted red seats light | graphic-anim | 4 | COLLINS v. VIRGINIA · 8–1 |
| S016 | GFX CurtilageShield | the home's glow expands to wrap the driveway | graphic-anim | 4 | CURTILAGE |
| S016 | GFX CaseTimeline `2018` + COD S018 + DEPTH | 2018 dot beside 1925; curtilage-edge still | graphic + depth | 3 | — |

### S017 (30s · 14 cuts · in: push · out: push) — quote resolve
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S017 | GFX QuoteCard (Sotomayor) | the line types on, attributed | graphic-anim | 6 | "no further than the automobile itself" · — Justice Sotomayor |
| S017 | GFX BrightLine `hold` | the car-search glow stops dead at the line; warrant icon on the house side | graphic-anim | 4 | — |
| S017 | COD S019 + DEPTH | empty supreme-court-style chamber | depth parallax | 2 | — |
| S017 | GFX CitationLowerThird | lone Alito dissent card | graphic-anim | 2 | — |

## ACT IV — WHERE THE LINE LEAVES YOU

### S018 (25s · 13 cuts · in: push · out: push) — summary map
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S018 | GFX ActTitle | title assembles | graphic-anim | 3 | YOUR RIGHTS ON THE ROAD |
| S018 | GFX DiagramFlow | STREET → probable-cause gate → zoned car | graphic-anim | 5 | — |
| S018 | GFX CarCutaway recap | the zoned car returns in summary form | graphic-anim | 3 | — |
| S018 | COD S023 + FTG | car and home establishing beat | ken burns | 2 | — |

### S019 (35s · 16 cuts · in: push · out: slide) — Gant / Byrd limits
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S019 | COD S020 + DEPTH | a person cuffed on a curb, car shut several feet away | depth parallax | 3 | ARREST ≠ A BLANK CHECK |
| S019 | GFX CaseTimeline `2009` | Gant dot lands beside 1925/2018 | graphic-anim | 3 | GANT · 2009 |
| S019 | COD S021 + DEPTH | rental keys on an agreement, name not listed | depth parallax | 3 | — |
| S019 | COD S038 | rental lot at dusk | ken burns | 2 | — |
| S019 | GFX KineticType + shield | a shield settles over the rental | graphic-anim | 2 | — |
| S019 | FTG parking-lot dusk | ambient lot | video native | 3 | — |

### S020 (28s · 13 cuts · in: slide · out: push) — the gray area
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S020 | GFX RegionHighlightMap `varied` | US states light non-uniformly | graphic-anim | 6 | SMELL = PROBABLE CAUSE? |
| S020 | GFX StateMap | unresolving shimmer, legend YES / FACTOR ONLY / UNDECIDED | graphic-anim | 4 | IT DEPENDS WHERE YOU ARE |
| S020 | COD S022 + FTG | driver at a window, uneasy | ken burns | 3 | — |

### S021 (24s · 14 cuts · in: push · out: push) — throughline
| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S021 | COD S022 + DEPTH | a calm driver, hands at ten-and-two | depth parallax | 3 | A REASON, NOT A MOOD |
| S021 | COD S023 + DEPTH | car and home with the bright line between them | depth parallax | 4 | — |
| S021 | COD S039 + DEPTH | family car in a driveway beside the home, golden hour | depth parallax | 3 | — |
| S021 | GFX BrightLine `hold` slow-push | slow push into the line — the film's resolving image | graphic-anim | 2 | IT STOPS AT YOUR HOME |
| S021 | FTG quiet driveway | ambient bed | video native | 2 | — |

## ENDING / CTA — S022 (33s · 14 cuts · in: push · out: fade to black)

| scene | source | visual | motion | cuts | overlay / text |
|---|---|---|---|---:|---|
| S022 | GFX BrandEndcard | canonical endcard | graphic-anim | 5 | THE LINE IS YOURS |
| S022 | GFX BrightLine sign-off + KIN | motif as the sign-off; like/subscribe cue | graphic-anim | 4 | — |
| S022 | FTG quiet driveway | settled outro bed | video native | 3 | — |
| S022 | COD S024 + DEPTH | a phone lock screen glowing awake (next-episode teaser) | depth parallax | 2 | — |

---

## Floors Check (perceptual motion budget)

- **Runtime / cuts / cadence:** 690s · 314 cuts · **avg 2.20s** (fast). No scene holds a static frame.
- **Depth ≥40%:** still cuts = **95**, depth-treated = **54** → **56.8%** (PASS). DepthStill parallax; the remaining stills get Ken Burns; depth maps pre-generated by `gen_depth.py`.
- **Moving FigureBeats ≥6:** **9** distinct — NumberTicker 0→68, VoteTally 8-1, ProbableCauseMeter (stall+cross), CarCutaway (all/big/small), CaseTimeline (1925/2009/2018), RegionHighlightMap/StateMap, CurtilageShield, CarKeyLock, PinDropMap (PASS).
- **Hero motion surfaces ≥2:** **3** — S001 BrightLine draw→slam, S015 CarKeyLock, S016 BrightLine slam (PASS).
- **Transitions:** ForcefulCut only — push/slide/zoompunch/whip. Bookend hard-cut-from-black (open) and fade-to-black (endcard). **Banned:** `WipeTransition` gold vertical sweep, default crossfades.
- **Cut-source mix:** graphic cuts = 174 · still cuts = 95 · footage cuts = 45 (sum 314).
- **Motion on stills:** every still receives DepthStill parallax or Ken Burns; every graphic animates with spring/easing + motion blur; no linear/opacity-only moves.
- **Disclosure:** symbolic-reconstruction label on every AI reenactment/location sequence.
- **Rights:** no generated asset or factory clip is edit-ready until registered in the rights manifest (origin, creator, license, hash, verified_at) AND passed visual QC (see `visual_qc_plan.v001.md`).
- **Factory footage:** every clip is contact-sheet eyeballed before staging — shelf labels are known-corrupt; off-theme footage (cowboy / cartoon) must not slip in.
