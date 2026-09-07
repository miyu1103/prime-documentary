# EP51 — THE FIRE THAT NEVER WAS (Cameron Todd Willingham) — DESIGN ARCHITECTURE (v001)
### The creative + quality + guardrail spine for a 20-minute single-human suffering film. This is the SOURCE OF INTENT that CODEX_A (assets) and CODEX_B (build) both inherit. Where a later doc conflicts with this one on VISUAL INTENT or QUALITY BAR, this wins.

> episode_id `PD-2026-051-willingham` · slug `willingham` · EP51 · fps 30 · 1920×1080 · id `Ep51Willingham`
> Companions: `EP51_willingham_script.en.v001.md` (LOCKED narration, ~3,570 words) · `EP51_willingham_FACTS_LEDGER.v001.md` (the ONLY fact source · CONFIRMED facts + VERIFIED-VERBATIM quotes) · `EP51_willingham_CODEX_A_ASSETS.v001.md` (image/asset prompts) · `EP51_willingham_CODEX_B_BUILD.v001.md` (build/render).
> **This is a real, sensitive capital case.** Willingham was executed and **NEVER legally exonerated**. Every reversal is framed as a matter of the EVIDENCE / FIRE SCIENCE — never as a court finding of innocence. **Child deaths (his three daughters): MAXIMUM RESTRAINT — never depicted, never re-created.**

---

## 0. THE ONE TRUTH OF THIS EPISODE — and the burned lessons this doc pre-empts

**The subject is a MAN, not a doctrine.** Todd Willingham lost his three daughters in a house fire, was cast as a monster, was convicted on fire "science" that later turned out to be folklore, was warned-about by a qualified scientist *before* the execution, and was killed anyway — and then, after his death, the state's own experts said the arson finding could not be sustained. **The HARD FRAME: he was never legally exonerated.** The film dismantles the *evidence*; it never claims a court found him innocent. The honest hedge stays visible at the end.

This doc exists because EP48/49 shipped with defects the pipeline did not enforce. **The following are HARD RULES for EP51, stated once here and enforced downstream (CODEX_A §1/§5, CODEX_B §2/§5.9/§6/§7):**

1. **NO global haze/fog/mist/vignette wash, and NO scanline/CRT texture over the film.** The grade is minimal and neutral. Any milky "BodyGrade" screen-wash is **opacity ≤ 0.07** and there is **no DriftLight-style diagonal-line texture anywhere**. The frame stays **clear and high-contrast**. Local diegetic texture on a single beat is fine; a persistent every-frame veil is a FAILURE. (EP48/49 milky wash was rejected: "全体的に画像に曇りがかかってる…改善して".)
2. **Footage treatment uses `bleed`/parallax, NEVER `depth`.** Three.js depth-map displacement (`treatment:"depth"`) melts and warps subjects — banned for this film on both footage and stills. Still `treatment` cycle = `["bleed","scan","duotone","focus"]` (no `depth`). Because `depth` is banned, **body stills do NOT need depth maps** (the A-3 depth-map step is removed).
3. **Stock-first footage.** The real stock library (`H:\pd-media\assets\stock` · 74 clips + 155 stills · pexels/pixabay · commercial-OK) is woven into the footage lane at meaningful beats and **preferred over AI-i2v wherever a relevant real clip exists** (real footage also avoids i2v warping). EP48/49 left the downloaded library unused; EP51 must not.
4. **Humans allowed, but ANONYMIZED / NON-identifiable.** Anonymize-by-composition (from-behind / shadowed / hatted / hands-only / soft-focus) — this also prevents warping. **BANNED: real-person likeness** (Willingham, Stacy, Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, or any real person in this case); **victim depiction / child-death imagery** (the three daughters — maximum restraint, never shown); **readable fake documents.**
5. **Image-reuse discipline.** Enough DISTINCT source images that **average uses/source ≤ ~1.16** (EP49 was 1.8 and the owner flagged it). Intentional recurring motifs are fine; unmotivated repeats are not.
6. **AE hero cards: ONLY the 6 implemented layouts** — `ACT_TITLE_CARD` / `CENTER_STACK` / `MONEY_STACK` / `QUOTE_CARD` / `VOTE_SPLIT` / `SPLIT_COMPARE`. **`DATE_STAMP` / `SEAM_TRANSITION` CRASH the build (`else throw "unsupported layout"`) — BANNED / forbidden; do not emit, do not implement.** This film uses **no `VOTE_SPLIT`** (no verified jury/court vote split exists in the ledger — a `VOTE_SPLIT` pip count must exactly match a real court size, and none applies here) and **no `MONEY_STACK`** (there is no settlement/payout — he was executed, never exonerated).
7. **`numberticker` year figures: `group:false`** so a year renders `2004`, not `2,004`. Correctly-grouped magnitudes (e.g., 48 pages, 20 indicators) are small integers and need no grouping either way; there are no large grouped magnitudes in this film.
8. **Narration = ElevenLabs "Brian" (voice_id `nPczCjzI2devNBz1zQrb`), NEVER SAPI.**
9. **durationInFrames comes from the CaseFilm formula on MEASURED TTS.** TTS is not generated yet — the value below is ESTIMATED from word count and is **PROVISIONAL. It MUST be RE-LOCKED from measured TTS (forced-align) before final render (measured > estimated).**
10. **HOOK-AUDIO: Brian's VOICE leads from 0:00 (no silent runway).** Top videos open with voice/audio from frame 0. The stock CaseFilm ran ~11.5s of branded hook+music before Brian spoke — a silent runway, which is wrong here. **EP51's cold-open line plays from 0:00** over the single most intense visual (the anonymized firelit father held back from the burning house), with tense dramatized sound design under it. The branded opening element is KEPT but moved to a HOOK→OP interstitial. **Real-audio constraint: no real-person/archival audio — Brian narration + dramatized SFX/ambience only.** This requires a CaseFilm component change flagged at build time (CODEX_B §4.4/§5.1.1).

If any one of these fails, the episode is not done — regardless of how good the rest looks.

---

## 1. THE QUALITY BAR (what "past-best" means, operationally)

1. **Restraint that is also dense.** Tone is quiet — no flashing, no melodrama, no sensationalizing of the deaths. Motion is relentless — something is always animating with intent. Restraint governs COLOR, PACING, COPY; density governs how many beats carry real motion. A still, silent hold of 4+ seconds is a FAILURE unless it is a deliberate, earned breath (max 2 in the whole film, each ≤2.5s).
2. **Every cut earns its place.** ~395 cuts across ~20 min. mean_shot ≈ 3.05s, max 7.0s. No cut is a filler slide. still-share ≤ 0.45. first-use ≥ 0.70.
3. **Premium motion density (HARD, per the premium-animation mandate).** ≥ 58 in-film FigureBeats (≥2.5/min; design 2.89/min), variety ≥ 6 kinds, plus ~17 AE hero cards composited on top. `check_motion_density` + `check_animation_mix` must PASS before any render is called final.
4. **Zero legibility/quality defects.** No garbled captions, no clipped AE text (measured-fit mandatory), no black frames, no desync (**VO onset at 0:00 exactly — voice leads the hook**), no silent runway, no dochighlight (reads as a bug — BANNED), no unsupported AE layout (crashes — BANNED), no year comma-grouping ("2,004").
5. **Truth, on a real capital case.** Every on-screen number, name, date, and quote traces to `FACTS_LEDGER` at high confidence, or it is hedged in copy or cut. **No likeness of any real person. The children's deaths are never depicted. He is never called "exonerated." "Monster" appears only as the state/Perry framing, to be dismantled.**

---

## 2. VISUAL LANGUAGE (the elevated system — a thermal inversion)

The whole film is shot in one palette and one grammar. The thesis is encoded in the color: **the WARM color is the LIE and the COLD color is the TRUTH — and, unlike a redemption film, the cold truth never turns warm, because it arrived too late.**

- **Primary accent — EMBER-ORANGE `#C25A2E`** = RGB (194,90,46) = normalized **[0.761, 0.353, 0.180]**. This is the fire, the "reading" of the char, the certainty of the town, the heat of the accusation, the "monster." It dominates the HOOK and Acts I–II. It is the color of everyone being *sure*.
- **Truth note — FORENSIC COLD `#7FA8B0`** = RGB (127,168,176) = **[0.498, 0.659, 0.690]**. A muted daylight teal-grey. This is clear-eyed fire science: Hurst's reading, flashover understood, Beyler, the Innocence Project. It is used SPARINGLY until Act III, then it re-reads the same char patterns the ember lit — and it **stays cold at the end**. There is no warm exoneration payoff, because there was no exoneration. The cold is the point.
- **INK base `#0B0A09`** (soot-black). **BONE-white `#ECE7DF`** for type.
- **People — anonymized, non-identifiable, and PRESENT (owner directive: the film must NOT read "empty/lonely, objects only").** Anonymized human figures are woven through the film wherever the narration has people — the town/onlookers, neighbors, mourners, investigators on the stand, the jury, the informant, the courtroom gallery, guards, execution witnesses (backs only), officials, experts — all from-behind / shadow / silhouette / hatted / hands-only / soft-focus (CODEX_A §5.11). **Target presence: 15 of the 30 motion beats + ~40 of the 150 body stills (~27%) carry anonymized humans** (converted within the locked lanes, not appended). **BANNED (absolute): any likeness of a real person in this case; any depiction of the three daughters or their deaths; any child/baby/infant in any form; any victim/burned-body/violence; any readable fake document.** The father in the yard is a firelit figure from behind — never Willingham's likeness, and never with children in frame. Execution beats show witnesses' backs / an empty gurney — never a body, never the act.
- **Recurring motifs (build a vocabulary, then pay it off):**
  - **The frame house on West 11th Street** — a wood-frame house rendered from OUTSIDE, ember glow through the windows, never the interior, never the children. Establishes in the cold-open, echoes, and is finally re-read as *an ordinary house that got big enough to flash over*.
  - **The yard** — an anonymous figure (from behind, firelit) held back from the glow. The father who couldn't reach them. Returns at the end ("from the first minute in the yard to the last minute on the gurney").
  - **The "read" fire / the language of char** — floor char, "pour patterns," crazed glass, threshold burn: shown as abstract forensic textures, ember-lit as "proof of arson" in Acts I–II, then RE-LIT cold in Act III as artifacts of an ordinary fire. **This re-reading is the film's visual thesis.**
  - **Flashover** — a closed room's air going incandescent, everything igniting at once; then the SAME char pattern resolves in cold `#7FA8B0` = "not a poured liquid — an ordinary fire that got big enough." The reversal, made visible.
  - **The two pillars** — two columns: THE FIRE and THE INFORMANT. Both crumble in Act III/IV — *after* the execution.
  - **The gurney / the chamber** — an empty gurney with straps in a bare chamber. **NEVER a body.** The execution rendered as an empty, waiting, unbearable room.
  - **The warning that arrived in time** — a document (unreadable smear) sliding onto a desk / into an inbox and being passed by. Hurst's report. Cold. The "dozen doors marked exit" the system walked past.
  - **The clock / the gap** — the space between the truth and the timing. "Just never in time."
  - **The letters** — an outsider (Gilbert) writing to a death-row prisoner; envelopes, a hand, a stamp. Nothing to gain.
- **Type & motion grammar:** all reveals use `overflow:hidden` + translateY mask lifts; easing is spring OR `Easing.out(Easing.cubic)` — NEVER linear; multi-element reveals STAGGER 2–4 frames; fast moves get `@remotion/motion-blur` Trail; opacity is NEVER used alone (always paired with translateY/scale).
- **Clear image, no wash (HARD — this doc wins).** No global haze/fog/mist/vignette-wash and no global scanline/CRT texture. Any grade is minimal, neutral, within the ember/cold system, **wash opacity ≤ 0.07**. Enforcement: **CODEX_B §5.9**.
- **Footage: `bleed`/parallax, NEVER `depth`.** Depth-map displacement melts subjects (banned — CODEX_B §5.2/§5.3, CODEX_A §5.5).
- **Real stock footage, woven at meaningful beats.** `H:\pd-media\assets\stock` (74 clips + 155 stills) is preferred over AI-i2v wherever a relevant real clip exists (small-town/night-street/courthouse/prison-adjacent/lab/dawn/ember-and-ash matched to the story). AI-i2v is reserved for abstract/symbolic beats (flashover, char re-reading, the gurney, the two pillars) where restraint/no-depiction means real footage cannot be used. Build spec: **CODEX_B §5.8** + sourcing in **CODEX_A §7.4a**.

---

## 3. ANIMATION INTENT PER ACT (motion as dramaturgy)

Motion tracks the story's emotional pressure. Density stays high; its CHARACTER changes.

- **HOOK + COLD OPEN (VOICE FROM 0:00 · no silent runway):** Brian's cold-open line plays from frame 0 — *"On the day before Christmas Eve, 1991, a man ran out of a burning house in Corsicana, Texas…"* — over the single most intense visual (an ember glow on a wood-frame house; a firelit figure in the yard, held back, anonymized, from behind, no children). Tense dramatized sound design under it (low sub pulse, distant fire-roar/crackle, a muffled impact on "hold him back") — Brian + SFX only, no real audio, no music melody. Lands on OST: **THERE MAY HAVE BEEN NO CRIME.** The branded gold sting follows as a HOOK→OP interstitial. Absolute restraint on the image; maximum grip on the audio.
- **OPENING:** the name, the dates 1968–2004, and the open loop — "the gap between the truth and the timing." Ember, quiet.
- **ACT I — THE MONSTER:** how a grieving father was cast as guilty. Observational, ember-lit. The town's certainty builds as a *machine* (`mechanism:gears`). The metal posters / tattoos / satanic-panic framing are shown as the town's projection, never adopted. The one spike: "the fire, they said, could be read" — the hinge. OST: **THE FIRE, THEY SAID, COULD BE READ.**
- **ACT II — THE TRIAL:** the two pillars. Pillar 1 = the ~20 arson "indicators" (Vasquez + Fogg) shown as convincing, ember-lit forensic textures. Pillar 2 = the informant (Johnny Webb). The rejected plea ("he said no") lands as the most human beat. The future-dangerousness psychiatrist. Convicted, sentenced to death, August 1992. OST: **TWO PILLARS: THE FIRE, AND THE INFORMANT.**
- **ACT III — THE UNRAVELING:** the reversal, and the failure to stop it. Gilbert (letters), then Hurst. **The visual climax:** each indicator re-lit cold — pour patterns → flashover; crazed glass → water on hot glass; threshold trace → the porch grill. "No valid evidence of arson." The report reaches the Board and the governor; clemency denied; **executed Feb 17, 2004, Huntsville; still insisting he was innocent; age 36.** The appeals walked past every door. Motion cold and clarifying, then unbearably still at the gurney. OST: **A STATE EXPERT: "A FINDING OF ARSON COULD NOT BE SUSTAINED."**
- **ACT IV — THE RECKONING (the END payoff):** after his death, the state proved him right. Beyler (2009): the two verified-verbatim lines. Perry replaces 3 of 9 commissioners two days before the meeting; the new chair cancels it; Perry calls him "a monster." Innocence Project: 5 experts, 48 pages, "none of it valid." Webb recants; his charge had been reduced. Both pillars fallen — after the execution. Then the honest hedge: **never legally exonerated**, the case is contested, Stacy said guilty — *but* the science, before and after, agrees. The thesis and the CTA. The cold never warms. OST: **HE SAID IT FROM THE FIRST MINUTE TO THE LAST.**

---

## 4. AE HERO PROGRAM — go heavy, but ONLY on the 6 proven layouts (no bespoke Tier-B)

AE carries the film's biggest beats as bespoke After Effects cards composited on top of the Remotion film. **~17 AE moments, ALL on the six proven layouts.** Time/effort is authorized, but this film does NOT invent new layouts (unlike EP50) — the six proven builders are enough for a 20-min film and they never crash.

- **Layouts used:** `ACT_TITLE_CARD` (×5) · `CENTER_STACK` (×6) · `SPLIT_COMPARE` (×3) · `QUOTE_CARD` (×3) = **17**. **No `MONEY_STACK`, no `VOTE_SPLIT`; `DATE_STAMP` and `SEAM_TRANSITION` are BANNED — do not emit, do not implement (unimplemented layout = build crash).** Date cards are `CENTER_STACK`.
- **The three QUOTE_CARDs are the spine of the payoff** — all three are VERIFIED-VERBATIM in the ledger:
  1. **"A FINDING OF ARSON COULD NOT BE SUSTAINED."** — Craig Beyler, 2009 (Texas Forensic Science Commission).
  2. **"...MORE CHARACTERISTIC OF MYSTICS OR PSYCHICS."** — Beyler, on the fire marshal's testimony.
  3. **"NONE OF THE SCIENTIFIC ANALYSIS USED TO CONVICT MR. WILLINGHAM WAS VALID."** — Innocence Project · 5 fire experts · 48 pages.
- **There are THREE SPLIT_COMPAREs — one framing card + the two reversal cards** (audit 2026-07-28 clarification; CODEX_B §7.2 is authoritative and lists all three). Framing: `cmp-pillars` THE CASE "THE FIRE" ↔ "THE INFORMANT" (ember ↔ ember, no cold pane). **The two reversal cards carry the science:** `cmp-flashover` POUR PATTERNS "PROOF OF ARSON" ↔ "PROOF OF FLASHOVER"; `cmp-glass` CRAZED GLASS "UNNATURAL HEAT" ↔ "WATER ON HOT GLASS". The cold accent applies to the RIGHT pane of those **two** reversal cards only.
- **Colour rules:** `ACCENT` = ember `[0.761, 0.353, 0.180]` for accusation/fire/trial cards; the cold note `[0.498, 0.659, 0.690]` for the SCIENCE cards (both SPLIT_COMPAREs' right pane, the Hurst card, all three QUOTE_CARDs, the "never exonerated" hedge). **No warm/gold dawn payoff — the cold stays cold.**
- **Rules for the whole AE program:** measured-fit MANDATORY (`fit_size()` pre-fit + JSX `sourceRectAtTime` re-fit + quote-wrap); two-step AE (JSX builds `.aep`, assert `.aep` mtime > `.jsx`, separate `aerender`, output to a REPO path on C:); every card burns `AI-assisted visualization` bottom-right; **no card depicts the children, the deaths, a real-person likeness, or a readable fake document; no card asserts a contested figure without a hedge; year cards `group:false`.** Deck contract: **CODEX_B §7.2**; `validate_willingham_beats` + `check_AE_layouts` assert every layout is one of the six proven (`DATE_STAMP`/`SEAM_TRANSITION` = FAIL).

---

## 5. IN-FILM FIGURE-BEAT SYSTEM (≥58 beats — the density engine)

Rendered inside the Remotion film via the real `FigureBeats.tsx` union. **Validate EVERY beat against the actual union** (timeline→events[] · compbars→items[] · kinetic→lines[] · mechanism→{closingdoor|gears|faultsplit} · stat→value+label · numberticker→value+group? · arrow→from/to · highlightring · pindropmap→pins[] · spotlight · lowerthird · acttitle). **dochighlight = 0 (BANNED — reads as a rendering bug, flagged 3×). votetally = 0 (no verified vote). quote figures = 0 (verbatim lives in AE QUOTE_CARDs). stub = 0.**
- **≥58 beats, ≥2.5/min (design 2.89 provisional → **2.85** at the re-locked 20:21.4 runtime), variety ≥6 kinds**, distributed so no 30s window is figure-less. Heaviest in VISUAL ACT III (the reversal) and VISUAL ACT IV (the reckoning).
  > ★ **ACT-COUNT NOTE (audit 2026-07-28 — read this before mapping anything by act name).** The **SCRIPT has THREE acts** (`## ACT I` / `## ACT II` / `## ACT III` + `## ENDING`); the **FILM has FOUR visual acts**. "ACT IV — THE RECKONING" is a *visual* act with no corresponding script heading: it is the post-execution stretch (Beyler / Texas Forensic Science Commission / Innocence Project) that lives inside script **ACT III**, followed by the ENDING. The narration runner therefore emits sections `HOOK/OP/ACT_1/ACT_2/ACT_3/ENDING` only — **there is no `ACT_4` narration section and there never will be**; the measured voice_plan confirms 218 chunks across exactly those six sections with zero orphan prose. Anything that maps by act NAME (CODEX_A §3.2's `ACT_4 "The Reckoning"` still block S113–S150, CODEX_B §7.2's `t-a4` ACT_TITLE_CARD at t=830.0 s, chapter markers, `validate_willingham_beats`) must use the VISUAL act index, not the script heading, and must not expect an `ACT_4` narration section. `gen_narration_case.py` cannot regenerate EP51 as registered: its default `SECTION_ORDER` requires `ACT_4`, so EP51 would be REFUSED (a safe failure, not a silent drop) — a 3-act `sections` list must be declared in that runner's registry if EP51 is ever re-voiced.
- **Signature figures:** a `timeline` 1991 → 1992 → 2004 → 2009 (returns, extends, resolves); `mechanism:gears` for the machine of certainty; `mechanism:closingdoor` for the "dozen doors marked exit"; `mechanism:faultsplit` for the two pillars splitting from the truth; `compbars` TWO PILLARS → 0 and ~20 INDICATORS → 0 VALID; `stat` for 3 (daughters, dignity), ~20 (indicators, hedged), 12 (years on death row), 36 (age), 48 (pages), 5 (independent experts); `arrow` for the report → the governor's desk → past it; `highlightring` on the doorway accelerant trace (innocent: the porch grill); `pindropmap` of Corsicana abstracted (**NO crime-location detail**); `spotlight` on the empty gurney and the figure in the yard.
- Figures use the ember/cold system; the flashover/pillars beats are the ones that flip from ember to cold in Act III.

---

## 6. COMPOSITION & TIMING (20:00 · PROVISIONAL — RE-LOCK FROM TTS)

- `id="Ep51Willingham"`, 1920×1080, fps 30, **VOICE leads from 0:00** (`hookVoiceLeads=true`), `brandInterstitialSec` 3.5 (HOOK→OP gold sting), ENDCARD_SEC 9.
- **narrationSeconds is ESTIMATED, not measured.** Script body = **~3,570 words**; at **178 wpm → 20.06 min → narrationSeconds ≈ 1203.4s (PROVISIONAL)**.
- **durationInFrames = ceil(narrationSeconds·30) + round(3.5·30) + round(9·30)** = ceil(1203.4·30=36102) + 105 + 270 = **36,477 frames ≈ 20:16 (PROVISIONAL)**. (The old 4-term formula with a 240-frame silent hook is REPLACED — the silent runway is gone; the cold-open narration leads at 0:00.)
  > ★ **FINAL value comes from MEASURED "Brian" TTS (forced-align), not this estimate.** Once the VO master exists, the builder puts `narration_index.total_seconds` into `narrationSeconds`, recomputes durationInFrames with the same 3-term function, and updates the Root registration. **measured > estimated.**
- **Anchor model (voice-from-0):** cold-open narration (HOOK section) at **0:00 → hookNarrSeconds**; the branded gold sting as a **HOOK→OP interstitial** at `[hookNarrSeconds, hookNarrSeconds+3.5]`; OP + acts resume at `hookNarrSeconds+3.5` (post-HOOK narration shifted +3.5s on the film clock); endcard +9s. Captions/BGM/SFX/AE all anchor to this clock. **Assert VO onset = 0.0** (not 11.5). CaseFilm component change flagged in CODEX_B §4.4/§5.1.1.
- **Cut budget (PROVISIONAL, scales with measured TTS):** total **395 cuts** = still **170** (img) + factory **165** (footage) + motion **60** (footage). distinct **345** = still **150** + factory **165** + motion **30**. still-share 170/395 = **0.4304** (≤0.45); motion-cov 225/395 = **0.5696** (≥0.45); mean_shot 1203.4/395 = **3.046s** (≤7.0); first-use 345/395 = **0.8734** (≥0.70); per-asset caps still 1.13 / factory 1.00 / motion 2.00.
- **Chaptered YouTube timestamps:** one per act, named to tease, published in the description.

### ★ MEASURED-VO RE-LOCK (audit 2026-07-28) — these values SUPERSEDE the PROVISIONAL figures above
The ElevenLabs "Brian" master EXISTS and was measured with ffprobe. The re-lock this section mandates had **not** been performed; it is performed here.
- Master `H:\pd-media\episodes\PD-2026-051-willingham\06_voice\master\vc_master_v001.mp3` = **1,208.845 s** (218 chunks · 3,593 narration words · 1,136.253 s of speech + 72.592 s of in-master gaps · measured pace **189.7 wpm**, not the 178 wpm estimate).
- **narrationSeconds = 1,208.845** (was 1,203.4 provisional; drift only **+5.4 s** — EP51 is the one episode where Brian ran FASTER than model, because this script is shorter and less dense than the 30-min slate).
- **durationInFrames RE-LOCKED = ceil(1208.845·30) + 105 + 270 = 36266 + 105 + 270 = 36,641** (was 36,477) → total **1,221.367 s = 20:21.4**.
- Speech ratio 1221.367 / 1136.253 = **1.0749** ∈ the measured channel band 1.04–1.30 ✓. Inside a 19:00–21:00 (1140–1260 s) 20-min band ✓.
- Cut-budget re-derive: mean_shot = 1208.845 / 395 = **3.060 s/cut** (≤7.0 ✓); factory floor = 1208.845/30 = 40.3 → ≥41 (design 165 ✓). All ratio gates (still-share 0.4304, motion-cov 0.5696, first-use 0.8734) are ratios of counts and are UNCHANGED.
- ★ **RUNTIME-BAND DEVIATION (owner decision required before ship):** 1,221 s is deliberately OUTSIDE the channel's 1740–1860 s 30-min standard. `check_final_acceptance` will hard-fail `runtime_band`; that is the single owner-approved deviation class, but it needs an explicit APR for EP51 — it must not be waved through as "the usual runtime_band fail".

---

## 7. GATES (nothing ships until all PASS — lessons are gates, not promises)

Preflight (before spend): `check_script_length` (20-min band, ~3,570 words · cap the 12-min 2,141 rule does NOT apply — pass an explicit ~3,700 cap), `check_willingham_facts.py` (R-INNOCENCE-FRAME [never claim a court found him innocent / never say "exonerated" / "monster" only as attributed framing], R-CHILD [the daughters' deaths never depicted, named once with dignity], R-VICTIM-DIGNITY, R-LIVING [Perry/Webb/Jackson/Vasquez/Fogg/Hurst/Beyler/Gilbert only as the public record supports], R-NUM [hedged figures: "roughly twenty" indicators], R-FACE [no real-person likeness; anonymized humans OK], R-DOCHL [dochighlight=0], R-QUOTE [only the 3 verified-verbatim lines + attribution]), `validate_willingham_beats`, `check_willingham_asset_manifest`, `check_AE_layouts` [only the 6 implemented; DATE_STAMP/SEAM_TRANSITION = FAIL].
Post-build (before final): `check_asset_reuse`, `check_motion_density --ep PD-2026-051-willingham`, `check_animation_mix`, `check_caption_breaks`, `check_caption_integrity`, `check_visual_asset_qc`, `check_year_grouping`, `preflight_render_gate`.
Post-render (before "done"): **FULL 20-MINUTE eyeball, 3×** (structure/caption-text/audio-sync) — measured, not sampled from one frame; confirm the HOOK leads with Brian's VOICE from 0:00 (no silent runway) over the father-in-the-yard visual + tense SFX, no real-person audio, no full-frame haze/scanline, no depth-warping, the children never appear, no real-person likeness, no "exonerated" claim, years not comma-grouped. Then `check_final_acceptance 51`.

---

## 8. HANDOFF

CODEX_A (image/asset generation) and CODEX_B (build/render) inherit from this architecture + the locked script + the FACTS_LEDGER. **A ↔ B connect only through `episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json`.** This document is the intent; those are the execution. All second/frame counts here are PROVISIONAL and RE-LOCK from measured "Brian" TTS before final render.
