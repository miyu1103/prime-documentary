# EP50 — THE EXONERATED FIVE — DESIGN ARCHITECTURE (v001)
### The creative + quality + guardrail spine for the channel's first 60-minute film. This is the SOURCE OF INTENT the full DESIGN doc, CODEX_A, and CODEX_B all inherit. Where a later doc conflicts with this one on VISUAL INTENT or QUALITY BAR, this wins.

> episode_id `PD-2026-050-centralpark` · slug `centralpark` · EP50 · fps 30 · 1920×1080 · id `Ep50Centralpark`
> Companions: `EP50_centralpark_script.en.v001.md` (locked voice), `..._STRUCTURE.v001.md` (7-act map), `..._PRODUCTION_SPEC.v001.json` (numbers — UPDATE to the 60:00 target), `..._facts.v001.json` (+CITATIONS) — the only fact source.

---

## 0. THE QUALITY BAR (what "past-best" means, operationally)
This film is judged against every prior episode and must beat them on all five axes at once. None is optional.

1. **Restraint that is also dense.** The *tone* is quiet — no flashing, no melodrama,细部で語る. The *motion* is relentless — something is always animating with intent. These are not in tension: restraint governs COLOR, PACING, and COPY; density governs how many beats carry real motion. A still, silent hold of 4+ seconds is a FAILURE unless it is a deliberate, earned breath (max 3 in the whole film, each ≤2.5s).
2. **Every cut earns its place.** ~1,080 cuts across ~60 min. mean_shot ≈ 3.1s, max 7.0s. No cut is a filler slide. still-share ≤ 0.45. first-use ≥ 0.70 (assets are not recycled to pad).
3. **Premium motion density (HARD, per the premium-animation mandate).** ≥ 140 in-film FigureBeats (≥2.5/min), variety ≥ 6 kinds, plus ~22 AE hero cards composited on top. The motion_density and animation_mix gates must PASS before any render is called final.
4. **Zero legibility/quality defects.** No garbled captions, no clipped AE text (measured-fit mandatory), no black frames, no desync (VO onset at 11.5s exactly), no dochighlight (reads as a bug — BANNED), no unsupported AE layout (crashes — BANNED).
5. **Truth, on living people.** Every on-screen number, name, date, and quote traces to `facts.json` at `confidence: high` with ≥2 sources, or it is hedged in copy or cut. No face of any real person, ever. The assault is never depicted.

If any one of these fails, the episode is not done — regardless of how good the rest looks.

---

## 1. VISUAL LANGUAGE (the elevated system)
The whole film is shot in one palette and one grammar, so that the DNA reveal in Act 5 can pay off a color the eye has been trained on since the hook.

- **Accent — cold forensic steel-cyan `#2F9FC4`** = RGB (47,159,196) = normalized **[0.184, 0.624, 0.769]**. This is the color of the lab, the DNA band, the truth that was in the file all along. It is used SPARINGLY in Acts 1–4 (a single cold light, a cursor, a cold edge) and then FLOODS the frame at the Act 5 DNA hinge — the visual thesis: the truth was always this color, waiting. INK base `#0A0A0C`. Bone-white `#EDEDE8` for type. One warm accent — a dawn amber `#C98A3C` — appears ONLY at exoneration (Act 6) and the close, and nowhere else, so it means something.
- **People (R2 — owner-revised, EP50).** **Anonymized, non-identifiable human figures and faces ARE allowed** as dramatized generic stand-ins (see CODEX_A §5.11 H-series). What stays banned is any **likeness of a real person** — the five, the victim/Meili, Reyes, Trump, or any real detective/judge/prosecutor — plus **any depiction of the victim and any assault imagery** (unchanged). The five and Reyes are still rendered non-identifiably (symbolic silhouettes as the default): five silhouettes at DESCENDING heights (children); hands, backs, the nape of a neck, a coat, a shoelace; Korey a recurring taller-but-still-young silhouette; Reyes a separate colder silhouette. Anonymized crowds/roles (youths, detectives, jurors, reporters, families, protesters) may appear as generic people with faces turned/shadowed/soft — never a real individual, never guilty-framed.
- **Recurring motifs (build a vocabulary, then pay it off):**
  - **The interrogation room**: empty chair, steel table, a wall clock with no readable time, and a red REC light that is *OFF* (the unrecorded hours). The OFF light is the film's signature image — establish in the hook, echo through Act 2, and invert it at the reform in Act 6/7 (the light comes ON).
  - **The signature**: a pen, a line on a page. It is written under pressure in Act 2; it *erases / dissolves* at the vacatur in Act 6.
  - **Cold-cyan DNA bands**: an abstract gel-electrophoresis ladder. Glimpsed cold and ignored in Act 2 (the lab report no one reads); it becomes the whole screen in Act 5.
  - **The lost years**: a single cell window, seasons crossing it; a silhouette imperceptibly aging (Korey). Never a literal calendar-flip cliché.
  - **The scale**: confession vs. evidence. Tips the wrong way in Act 3, rights itself in Act 6.
  - **The park at night**: rendered ABSTRACTLY — treeline, a lamp, cold — never crime imagery. Resolves to dawn light at exoneration.
- **Type & motion grammar:** all reveals use `overflow:hidden` + translateY mask lifts (channel house style); easing is spring OR `Easing.out(Easing.cubic)` — NEVER linear; multi-element reveals STAGGER 2–4 frames; fast moves get `@remotion/motion-blur` Trail. Opacity is NEVER used alone — always paired with translateY/scale.
- **Clear image, no wash (HARD — VISUAL INTENT, this doc wins).** The frame stays **clear and high-contrast**. **No global haze/fog/mist/vignette-wash layer and no global scanline/CRT texture over the film** — the milky low-contrast wash EP48/49 shipped was rejected ("全体的に画像に曇りがかかってる…改善して"). Any grade is minimal and neutral within the cold-cyan system. Local diegetic texture (e.g., the Act-3 videotape TV-glow scanline on that beat only) is fine; a persistent every-frame veil is not. Build enforcement: **CODEX_B §5.9**.
- **Real stock footage, woven at meaningful beats (owner directive).** EP48/49 used AI stills + AI-i2v only and left the downloaded stock library unused ("せっかくたくさんダウンロードしたんだから意味のある所に使ってほしい"). The channel's real stock library (`H:\pd-media\assets\stock` · 74 clips + 155 stills · pexels/pixabay · commercial-OK) is **woven into the footage lane semantically** (courthouse/NYC/precinct/prison/lab/protest/dawn matched to the story) and **preferred over AI-i2v wherever a relevant real clip exists** (real footage also avoids i2v warping); AI-i2v is reserved for the abstract/symbolic beats (DNA bands, silhouettes) where R-FACE/no-crime-imagery means real footage cannot be used. Stock is color-matched to the AI stills with one neutral grade. Build spec: **CODEX_B §5.8** + sourcing in **CODEX_A §7.4a**.

---

## 2. ANIMATION INTENT PER ACT (motion as dramaturgy)
Motion is not decoration; it tracks the story's emotional pressure. The density stays high throughout, but its CHARACTER changes.

- **HOOK (8.0s):** black → a single cold-cyan light finds the empty chair; the OFF REC light ticks once. One line of type mask-lifts. Absolute restraint — the whole film's stillness, promised.
- **ACT 1 — The Night:** cold, wide, documentary. Slow push-ins, the city as texture (subway, headlines as abstracted mass). Motion is *observational*. The one spike: the moment the two investigations merge — a hard graphic snap where "park trouble" and "the attack" collide into one file.
- **ACT 2 — Interrogations (the engine):** the tightest, most claustrophobic motion in the film. Close, handheld-feel micro-drifts; the clock; the story fed in as literal type fragments migrating from a detective silhouette into a child silhouette (visualize the false-evidence ploy). Multiply-by-five: five confession pages stacking, each citing the next — a visual house of cards. This act carries the highest figure-beat density.
- **ACT 3 — Trials:** the machine of publicity. Headlines as an oppressive kinetic wall; the Trump-ad beat as a single dated context card (NEVER reproduce the ad art). The scale tips. The videotape motif: a TV glow, a play triangle — the confession performed.
- **ACT 4 — Lost Years:** motion SLOWS and lengthens (earned — the only place holds run near 3.5–4s), then the individual portraits re-quicken as we name each of the four, then settle into Korey's long, quiet, aging silhouette. Solitary = the frame itself narrows.
- **ACT 5 — Confession & DNA:** the reversal. Reyes as a separate, colder silhouette. Then the DNA bands ignite — the ONE moment the film "raises its voice": cold-cyan floods, the ladder aligns to a single match, the numbers with many zeros resolve. The visual climax. Everything cold the eye has seen pays off here.
- **ACT 6 — Exoneration & Reckoning:** the signature dissolves; the vacatur card; the first dawn-amber. The Armstrong beat is handled as a small, dismissed footnote (visually minor, quickly set down). The settlement numbers land heavy and plain. The REC light finally comes ON (reform).
- **ACT 7 — What a Confession Is Worth:** back to the chair, the child, the second person. Strip the frame to essentials — chair, clock, the OFF/ON light, the five names. End on the names in bone-white, then the truth line. Restraint returns; the film ends as quietly as it began.

---

## 3. AE HERO PROGRAM — GO HEAVY (owner directive: "AEをガッツリ効かせて、時間はかかってもいい")
This is a flagship. AE is not a garnish on top of the Remotion film — it carries the film's biggest emotional peaks as bespoke After Effects set-pieces. **~36 AE moments total, in two tiers.** Time/effort is explicitly authorized to build this properly.

### Tier A — Standard hero cards (~24), on the SIX PROVEN layouts only
`ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`.
> ★★ **`DATE_STAMP` and `SEAM_TRANSITION` DO NOT EXIST** in the clone source `build_cleveland_hero_cards.py` (JSX ends in `else throw "unsupported layout"`). Using them CRASHES the build. Date cards = `CENTER_STACK`. Burned EP48/49 lesson.
- 7 act-title cards + content cards, e.g.: `CENTER_STACK` NO PHYSICAL EVIDENCE / A ROOM AND A PROMISE · `SPLIT_COMPARE` THE STORY, FED IN ↔ THE STORY, SIGNED · `CENTER_STACK` FIVE CHILDREN · AGES 14–16 · `CENTER_STACK` 1989 · TRIED IN THE PAPERS FIRST · tally CONVICTED · YET ACQUITTED OF ATTEMPTED MURDER (verify split) · `SPLIT_COMPARE` FOUR: JUVENILE, 5–10 YRS ↔ KOREY WISE, 16: TRIED AS AN ADULT · `CENTER_STACK` ~13 YEARS (Korey, hedge) · `QUOTE_CARD` "I DID IT. ALONE." (Reyes 2002) · `CENTER_STACK` DEC 19, 2002 · VACATED · `MONEY_STACK` ~$41 MILLION · 2014 · `CENTER_STACK` RECORD THE WHOLE INTERROGATION.

### Tier B — BESPOKE AE SET-PIECES (~12) — NEW layouts, implemented for real, THE "gutsy" part
Each is a NEW builder function added to `scripts/ae/build_centralpark_hero_cards.py` (which EXTENDS the cleveland clone — keep its 6, ADD these). Each new layout is **individually `--dryrun` tested and added to the `check_AE_layouts` allowlist BEFORE use** — this is how we go heavy WITHOUT repeating the phantom-layout crash: we don't reference layouts that don't exist; we IMPLEMENT them, prove them, then reference them. These are longer, richer comps (5–10s) placed at the story's emotional peaks, and they are the film's signature images:
1. **`DNA_LADDER`** — Act 5 climax (~8–10s). A gel-electrophoresis ladder builds; five lanes for the boys resolve to NO MATCH (cold, dim); then Reyes's lane snaps into a single aligned match and cold-cyan floods the frame. The visual thesis of the whole film. The most elaborate comp in the deck.
2. **`SIGNATURE_ERASE`** — the vacatur, Act 6 (~6s). A signed line on a confession page un-writes itself, ink lifting away stroke by stroke. Pairs with the DNA_LADDER as before/after.
3. **`CARD_STACK`** — Act 2 (~7s). Five confession pages stack, each with an arrow citing the next ("the others already named you"); then the DNA report slides underneath and the whole stack is revealed to have no foundation — a literal house of cards.
4. **`REC_LIGHT`** — the signature motif as a beat (used 2×). A red REC dot, dark all film → finally ILLUMINATES at the reform (Act 6/7). The off state also anchors the hook.
5. **`SCALE_TIP`** — confession vs. evidence (used 2×). Tips the wrong way in Act 3, rights itself in Act 6. Physical, weighted easing.
6. **`HERO_TIMELINE`** — a full-screen AE spine graphic Apr 19 1989 → 2002 → 2014 that RETURNS and extends across acts (introduced Act 1, extended Act 4, resolved Act 6). Distinct from the in-film Remotion `timeline` figures — this is the elevated hero rendition.
7. **`NAME_WALL`** — the five names + ages rise (Act 2), then are re-inscribed as "THE EXONERATED FIVE" at the close (used 2×). The renaming, made visual.
8. **`STAT_RESOLVE`** — the "one in billions" DNA statistic animating to a single match (Act 5); numeric odometer resolve.
9. (reserve 2–3 more if the storyboard surfaces another peak — e.g. a `HEADLINE_WALL` kinetic press-storm for Act 3, an `INTERROGATION_ROOM` establishing comp for the hook/Act 2.)

### Rules for the WHOLE AE program (both tiers)
- **ACCENT tuple** `[0.184, 0.624, 0.769]` (#2F9FC4) — RGB tuple, not just a hex comment. INK `[0.039,0.039,0.047]`. Dawn-amber `[0.788,0.541,0.235]` ONLY on exoneration/close moments (SIGNATURE_ERASE resolve, REC_LIGHT-on, NAME_WALL close).
- **Measured-fit MANDATORY** (Python `fit_size()` pre-fit + JSX `sourceRectAtTime(t,false).width` re-fit + quote-wrap; no advance-width estimation).
- **Two-step AE**: JSX builds `.aep` (`AfterFX -noui -r`) → assert `.aep` mtime > `.jsx` mtime → SEPARATE `aerender -project`. Output to a REPO path on C: (exFAT H: silently writes 0 mp4s).
- **No card asserts a contested figure** — money/years/stat carry "~" and match the hedged script. **No AE moment names or depicts the victim; none reproduces the Trump ad; no faces.** The DNA_LADDER and interrogation comps are abstract (no crime imagery).
- Final deck (both tiers) — id/layout/copy — must match CODEX_B exactly; `validate_centralpark_beats` cross-checks the DESIGN table against the CODEX_B deck, and `check_AE_layouts` asserts every layout is either one of the 6 proven OR one of the newly-implemented+dryrun-passed Tier-B layouts (0 phantom layouts).

---

## 4. IN-FILM FIGURE-BEAT SYSTEM (≥140 beats — the density engine)
Rendered inside the Remotion film via the real `FigureBeats.tsx` union. **Validate EVERY beat against the actual union** (timeline→events[] · bar→data[] · compbars→items[] · routemap/pindropmap→pins[] · kinetic→lines[] · mechanism→{closingdoor|gears|faultsplit} · votetally→majority+dissent · quote→quote+attribution · stat→value+label · brightline→mode). **dochighlight = 0 (BANNED — reads as a rendering bug; flagged 3×).** stub = 0.
- **≥140 beats, ≥2.5/min, variety ≥6 kinds**, distributed so no 30s window is figure-less. Heaviest in Act 2 (the mechanism of the false confession) and Act 5 (the DNA logic).
- **Signature figures:** a `timeline` of that night → 2002 (returns, extends, and finally resolves); `kinetic` name/age stacks (the five); a `mechanism` of the interrogation (pressure → yield); `compbars` of confession-count (5) vs DNA-match-count (0); a `votetally`/tally of the trial verdicts (verify split); a `stat` of the one-in-billions match; `quote` cards for the verified verbatim lines only. Abstract `pindropmap` of the park geography (abstracted, NO crime location detail).
- Figures use the cold-cyan system; the DNA/compbars beats are the ones that "ignite" in Act 5.

---

## 5. COMPOSITION & TIMING (60:00)
- `id="Ep50Centralpark"`, 1920×1080, fps 30, **hookSeconds = 8.0**, OPENING_SEC 3.5, ENDCARD_SEC 9.
- Narration ≈ 60.1 min (script v001 = 10,715 words @ calibrated pace). **durationInFrames = round(8·30) + round(3.5·30) + ceil(narrationSeconds·30) + round(9·30).** Provisional at 3,606s narration = 240 + 105 + 108,180 + 270 = **≈108,795 frames**. ★ FINAL value comes from the MEASURED TTS narration (forced-align), not this estimate — update SPEC + Root after the VO master exists.
- Body/captions/BGM VO OFF / AE film_offset all anchor at **11.5s** (hookSeconds 8.0 + OPENING 3.5). If hookSeconds is ever 0, everything desyncs 8s — assert it.
- **Chaptered YouTube timestamps** (per the retention de-risk): one per act, named to tease, published in the description.

---

## 6. GATES (nothing ships until all PASS — lessons are gates, not promises)
Preflight (before spend): `check_script_length` (60-min band, NOT the 2,141 12-min cap — the gate needs a --longform mode or an explicit cap ≈10,900), `check_centralpark_facts.py` (clone of check_strieff_facts: R-INNOCENCE [never imply the five were involved / Armstrong only as rejected], R-VICTIM [dignity, no depiction, no naming beyond the record], R-REYES [established facts only], R-NUM [hedged figures], R-FACE [no faces], R-DOCHL [dochighlight=0], R-QUOTE [verified verbatim + attribution]), `validate_centralpark_beats`, `check_centralpark_asset_manifest`, `check_AE_layouts` [only the 6 implemented; DATE_STAMP/SEAM_TRANSITION = FAIL].
Post-build (before final): `check_motion_density --ep PD-2026-050-centralpark`, `check_animation_mix --ep ...`, `check_caption_integrity`, `visual_asset_qc`, `check_asset_reuse`, `preflight_render_gate`.
Post-render (before "done"): **FULL 60-MINUTE eyeball, 3×** (structure / caption-text / audio-sync) — measured, not sampled from one frame. Then `check_final_acceptance 50`.

---

## 7. HANDOFF
The full `EP50_centralpark_DESIGN_and_CODEX_PROMPTS.v001.md` (0→~3,606s second-by-second timeline, all 7 acts storyboarded scene-by-scene, per-beat frames/easing/stagger/motion-blur, the full ~22-card AE deck table, the ≥140 figure-beat schedule, Composition block, gate list) is generated FROM this architecture + the locked script + structure + verified facts. CODEX_A (image/asset generation at 5× scale) and CODEX_B (build/render) inherit from it. A↔B connect only through `asset_manifest.v001.json`. This document is the intent; those are the execution.
