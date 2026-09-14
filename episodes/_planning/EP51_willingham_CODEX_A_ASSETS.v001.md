# EP51 willingham — Codex Thread A "Asset Generation" handoff prompt v001 (20-min single-human suffering film)

> **This file is self-contained. You can start without reading any other file.**
> Do NOT read the DESIGN_ARCHITECTURE or CODEX_B docs — every number you need is transcribed here.
> Case: **Cameron Todd Willingham** — a father convicted of murdering his three daughters by arson and executed by Texas in 2004; the arson "science" was later invalidated. **He was NEVER legally exonerated.** Frame every reversal as a matter of the EVIDENCE / FIRE SCIENCE, never a court finding of innocence. **The children's deaths are NEVER depicted (maximum restraint).**

```
You are a production engineer for Prime Documentary (a YouTube documentary channel).
Repo:    C:\Users\aab15\Documents\prime-documentary
Python:  C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
Media:   H:\pd-media
Owner:   EP51 / Episode ID: PD-2026-051-willingham / slug: willingham
Composition id: Ep51Willingham (B registers it in Root.tsx; A stages only) / 1920x1080 / fps30 / ~20:24 (PROVISIONAL)
Case:    On Dec 23, 1991, a fire in a wood-frame house in Corsicana, Texas killed Cameron Todd Willingham's
         three young daughters (Amber, 2; twins Karmon and Kameron, 1). Willingham (b. 1968, then ~23) escaped
         and said he could not reach them. Investigators "read" the fire as arson via ~20 "indicators"
         (pour patterns, crazed glass, multiple origins, low/threshold burn, an accelerant trace at the doorway).
         A jailhouse informant (Johnny Webb) claimed a confession. Willingham REJECTED a plea (life for a guilty
         plea), was convicted (Aug 1992) and sentenced to death. On death row he maintained his innocence.
         Chemist Gerald Hurst reviewed the case and, DAYS BEFORE the execution, reported NO valid evidence of
         arson (flashover explains the "pour patterns"; crazed glass = water on hot glass; the doorway trace =
         a porch grill / lighter fluid). Clemency was denied. Executed Feb 17, 2004, Huntsville Unit, age 36.
         AFTER his death: the Texas Forensic Science Commission's expert Craig Beyler (2009) wrote "a finding of
         arson could not be sustained" and the fire marshal's testimony was "more characteristic of mystics or
         psychics"; Gov. Perry replaced 3 of 9 commissioners two days before the meeting, which was then canceled;
         the Innocence Project's 5 experts (48-page report) said "none of the scientific analysis used to convict
         Mr. Willingham was valid"; Webb later recanted and his charge had been reduced. He was NEVER exonerated.
         ★ THEME: a single human suffering narrative — how certainty, folklore-science, and timing killed a man.
         The fire itself and the deaths are CONTEXT, handled with maximum restraint (no depiction).
         ★ People rendered ANONYMIZED / NON-identifiable only. No likeness of any real person. The children are
           NEVER shown. No victim/child-death imagery. No readable fake documents. Clear, high-contrast image
           (no haze/fog/scanline wash). Footage/stills use bleed/parallax, NEVER depth-map displacement.
```

---

# 0. This thread's (A) responsibility, boundary, done-conditions

## 0.1 Responsibility (GPU-bound / eyeball-bound long jobs · 20-min scale)

Assemble every "picture" the film uses and write them into one manifest.

| # | Task | Output | Rough |
|---|---|---|---|
| A-1 | SDXL still batch (**150 unique body prompts × 1 image = 150**, variation 0) | `H:\pd-media\assets\ai\willingham\S<NNN>.png` | 4–6h (GPU) |
| A-1b | i2v seed images (**30 unique prompts × 1 = 30**, variation 0) | `H:\pd-media\assets\ai\willingham\M<NN>_src.png` | 1–1.5h (GPU) |
| A-2 | Still QC + eyeball (**all 180 images eyeballed**) | `05_visuals/still_qc.v001.json` + contact sheets | 2–3h |
| A-3 | ~~depth maps~~ **NOT NEEDED** — `treatment:"depth"` is BANNED this film (§5.5); body stills carry no `depth_path` | — | — |
| A-4 | factory real clip selection **165** + **full eyeball QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 3–4h (≥1.5h just eyeballing) |
| A-5 | i2v motion **30** (Wan 2.2 A14B → RIFE 48fps) | `H:\pd-media\assets\ai_video\willingham\M<NN>_rife.mp4` | 12–36h (GPU · overnight) |
| A-6 | overlay layer selection (particle/light/vfx) **20** | `05_stock/overlay_selection.v001.json` | 40m |
| A-7 | rights ledger + **boundary-contract manifest** | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30m |
| A-8 | staging to Remotion public | `remotion/public/willingham/{img,factory,motion,overlay}/` | 30m |

> **★★ Core premise (continued from EP42–50): 1 scene = 1 image, variation 0 ★★**
> **Generate each distinct still from a unique prompt, one image each** (150 body prompts = 150 lines, each 1 image).
> Run `generate_sdxl_4k.py` with **NO `--variants`**. **Do NOT use `--variants 3`. Do NOT make `_02`/`_03`.**
> **Total generated = still 150 + i2v seed 30 = 180 images (each once).** factory 165 is SELECTED from stock, not generated.
> **★ Confirm `shots=180`** in the `--only S001` log before the full run (150 body + 30 i2v seed = 180).
> ★ i2v 30 is an **overnight GPU job**. **Check machine state before starting** (heavy-job preflight). Run at night / in splits.

## 0.2 Boundary with thread B (build) = exactly one connecting file

```
episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json
   ↑ A produces (sole producer)          ↓ B consumes (sole consumer/validator)
```

**B reads no A intermediate except this file. A depends on no B output except this file.** counts / role enum / overlay count / also_thumb set are shared **byte-for-byte** between A(producer) and B(consumer/validator) (§4).

> ★★ **EP45 accident (avoid absolutely):** EP45 nearly shipped an asset_manifest with **only stills filled and factory/motion arrays empty**. **This film's `factory` array MUST materialize 165 entries, `motion` 30, `overlay` 20 — all with non-empty `public_path`** (§4.4/§4.5/§4.6 enumerate all of them; the build script consumes that enumeration and never writes empty arrays). EP38's empty-manifest accident is banned for the same reason.

### File ownership (breaking this breaks parallel work)

| Path | Owner | A's rights |
|---|---|---|
| `H:\pd-media\assets\ai\willingham\**` / `ai_video\willingham\**` | **A** | read/write |
| `episodes/PD-2026-051-willingham/05_visuals/**` / `05_stock/**` | **A** | read/write (`mkdir(parents=True, exist_ok=True)`) |
| `episodes/PD-2026-051-willingham/04_scenes/ai_prompts.v001.md` | **A** (input to `generate_sdxl_4k.py`) | read/write. B only reads |
| `remotion/public/willingham/{img,factory,motion,overlay}/**` | **A** | read/write |
| `episodes/PD-2026-051-willingham/{manifest.json,03_script,04_scenes/shotlist*,08_edit,09_package}/**` | **B** | **do not touch** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_willingham_film.py` | **B** | **do not touch** |
| `episodes/PD-2026-0{01..50}-*/**` and their assets | other agents | **never touch. read-only** |

## 0.3 Scripts A uses / creates

**★ Use existing scripts as-is (do not invent new ones):**

| Path | Role | Args |
|---|---|---|
| `scripts/generate_sdxl_4k.py` (**existing**) | §5 SDXL generation (reads `04_scenes/ai_prompts.v001.md` via `read_prompts()`) | `PD-2026-051-willingham` (no variants) / `51 --only S001` |
| `scripts/build_footage_contact_sheet.py` (**existing**) | §6/§7 full-eyeball contact sheets | `--ep PD-2026-051-willingham --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py` (**existing**) | §7 factory candidates | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-051-willingham --json` |
| `scripts/check_visual_asset_qc.py` (**existing**) | §0.4 factory full-eyeball gate | `--ep PD-2026-051-willingham` |

**★ Scripts A creates (clone the nearest existing one; confirm it exists with `ls scripts/` before cloning; create nothing else):**

| Path | Role | Clone base (confirm exists first) |
|---|---|---|
| `scripts/qc_willingham_stills.py` | §6 still QC + resolution check | `scripts/qc_centralpark_stills.py` (EP50) — else `qc_strieff_stills.py` |
| `scripts/select_willingham_factory.py` | §7 factory 165 selection · EP39–50 sha256 de-dup | `scripts/select_centralpark_factory.py` (EP50) |
| `scripts/comfy_wan_willingham.py` | §8 i2v 30 (Wan 2.2 A14B driver — swap paths + SHOTS only) | `scripts/comfy_wan_centralpark.py` (EP50) — else `comfy_wan_strieff.py` |
| `scripts/rife_willingham.py` | §8.4 RIFE 4x → 48fps | `scripts/rife_centralpark.py` — else `rife_strieff.py` |
| `scripts/build_willingham_asset_manifest.py` | §4 boundary-contract manifest + self-verify | `scripts/build_centralpark_asset_manifest.py` (EP50) |
| `scripts/stage_willingham_assets.py` | §10 staging | `scripts/stage_centralpark_assets.py` (EP50) |

> **Do NOT create a new SDXL generation script.** `generate_sdxl_4k.py` already exists. You only **write `ai_prompts.v001.md` in the §5.9 two-line format.** Do not invent scripts that don't exist.
> **The accuracy gate is `check_willingham_facts.py` (B clones `check_centralpark_facts.py`; same name across DESIGN/A/B).** Every string A writes (prompt / `tags` / `caption_hint` / `eyeballed_content` / `notes`) must satisfy §1.2's constraints and be phrased to pass `check_willingham_facts.py`.

## 0.4 Done-conditions (all green = done. One red = not done)

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] boundary-contract manifest passes self-verify
./.venv/Scripts/python.exe scripts/build_willingham_asset_manifest.py --verify
#   → exit 0. counts match §3/§4 locked values. all paths exist. zero sha256 dupes.
#   → ★ factory len==165 / motion len==30 / overlay len==20 non-empty & materialized (EP45-avoidance invariant)

# [A-DONE-2] non-repeat gate passes on asset counts
./.venv/Scripts/python.exe scripts/build_willingham_asset_manifest.py --reuse-feasibility
#   → still >=150 / motion >=30 / factory >=165 / distinct total >=345 / first-use >=0.70

# [A-DONE-3] still resolution gate (long edge >=3840)
./.venv/Scripts/python.exe scripts/qc_willingham_stills.py --check-resolution

# [A-DONE-4] factory visual QC gate (★ record of eyeballing all 165)
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-051-willingham
#   → exit 0 (factory_clip_qc.v001.json covers every staged clip reviewed:true)

# [A-DONE-5] zero asset overlap with EP39–EP50
./.venv/Scripts/python.exe scripts/select_willingham_factory.py --verify-no-prior-overlap
#   → duplicate sha256 = 0 (against all twelve of EP39–EP50)
```

---

# 1. ★★★ Top-priority absolute constraints (R1 + R2 + 7 accuracy constraints) ★★★

**Cameron Todd Willingham was executed in 2004 and was NEVER legally exonerated. No court vacated his conviction; the case is officially contested. Frame every reversal as a matter of the EVIDENCE / FIRE SCIENCE — never a court finding of innocence, never "exonerated." His three daughters (Amber, 2; twins Karmon and Kameron, 1) died in the fire; their deaths are NEVER depicted or re-created (maximum restraint) — name them once, with dignity, and keep the lens on the injustice and the science. "Monster" is the state's / Gov. Perry's framing, attributed and dismantled — never adopted in the narrator/visual voice except to take it apart. Living/real people (Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, Willingham himself) get NO likeness — but anonymized human presence IS wanted and woven through the film (from-behind/shadow/silhouette/hands, adults only; 15 of 30 motion beats + ~40 of 150 stills · §5.11), so the film does not read "empty/objects only." Numbers are hedged where the ledger hedges (soft-cite "roughly twenty" indicators). No fabricated quotes — only the three verified-verbatim lines (AE cards = B). Every real person gets R2 (no face/likeness — anonymized generic stand-ins only).**

## 1.1 R1/R2 (all generated visuals)

1. **R2: anonymized / non-identifiable people OK / real-person likeness NOT.** Anonymized generic people (resembling no real individual; faces turned/shadowed/hatted/hands-only/soft) — bodies/faces may appear (§5.11 H-series with dedicated `[HSTYLE]`/`[HNEG]`). But **NO likeness of any real person** = Willingham, Stacy, Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, or any real detective/judge/prosecutor/scientist. Where a real person is implied, keep the figure non-identifiable (from-behind / shadow / backlit silhouette / hatted / cropped below the eyes / soft focus). **The three daughters are NEVER shown — no child, no baby, no infant, no child's body, in any form (unbreakable).** The father in the yard is a firelit figure from behind — never Willingham's likeness, **never with children in frame.**
2. **Never reproduce readable text on a real document** — confession/autopsy/verdict/case-number/newspaper/date/ID rendered as atmosphere only ("blurred into an unreadable smear"). Dates (1968 / 1991 / 1992 / 2004 / 2009 / 2011), ages (2 / 1 / 23 / 36), the count "roughly twenty," "48 pages," "5 experts" are **not drawn into the image** — they come from AE/figures typography (= B).
3. **Never depict the victims, the deaths, the fire-with-people, or injury.** The house is shown only from OUTSIDE with an ember glow — no interior death, no bodies, no burned remains, no blood, no weapon, no re-enactment. **No children anywhere.**
4. AI images are disclosed in the description → set `ai_disclosure_required: true` on every still and every i2v in the manifest. While any generated visual is on screen, a bottom-right `AI-assisted visualization` runs (overlay applied by B).

## 1.2 ★ 7 accuracy constraints (apply to every string A writes: prompt · `tags` · `caption_hint` · `eyeballed_content` · `notes` · filenames. Violation = BLOCKER)

1. **R-INNOCENCE-FRAME:** Never claim or imply a court found him innocent; never write "exonerated," "cleared by a court," "conviction vacated," "proven innocent." Allowed: "the arson science was invalidated / discredited / could not be sustained," "no valid evidence of arson," "the fire was likely accidental," "there may have been no crime," "never legally exonerated," "the case remains contested." The reversal is about the EVIDENCE, not a verdict.
2. **R-CHILD (maximum restraint):** the three daughters' deaths are NEVER depicted or re-created. Do not write "dead child," "burned child," "children's bodies," "the girls dying," "child victim." Name-once-with-dignity happens in narration only (= B), never in an image.
3. **R-VICTIM-DIGNITY:** no graphic fire injury, no burned remains, no bodies, no sensational distress. Do not write "burned body," "corpse," "bleeding," "charred victim."
4. **R-LIVING (real people):** Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, Willingham as established public record only. No defamatory characterization; report allegations as allegations. Webb's account is unstable; Jackson's alleged misconduct is *reported/alleged* (a bar case was dismissed). Do not write "Perry is a murderer," "Webb the liar," "corrupt Jackson." "Monster" appears only as attributed framing to dismantle — never as the image's own claim about the man.
5. **R-FACE:** anonymized/non-identifiable people OK (§5.11). Zero real-person likeness — do not write "likeness of Willingham / Perry / Webb / Hurst / Beyler / a real detective/judge/prosecutor," "face of <those names>," "recognizable real person," "mugshot of a real person," "deepfake." Anonymized generic people ("anonymous / generic / non-identifiable person, face turned or in shadow, adults only") ARE allowed.
6. **R-DOCHL:** do NOT create or mention `dochighlight` (the black-bar/box/underline figure). Never write the string `dochighlight` in `tags`/`caption_hint`/`notes`/filenames (keep grep at 0). Owner flagged it 3× (EP40/41/42) as "looks like a bug."
7. **R-QUOTE:** no fabricated quotes. Verbatim lives only in AE (= B) and only the three verified lines. No readable quotes drawn into images.

## 1.3 Machine gate (inside `build_willingham_asset_manifest.py --verify`)

Any single hit across all string values in A's JSON → exit 1:

```python
import re
# Anonymized/non-identifiable people are allowed. Only real-person likeness FAILs.
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (willingham|todd|cameron|stacy|perry|webb|vasquez|fogg|hurst|beyler|gilbert|jackson)|"
    r"likeness of (willingham|todd|cameron|stacy|perry|webb|vasquez|fogg|hurst|beyler|gilbert|jackson)|"
    r"recognizable (real person|celebrity)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"\bexonerated\b|proven innocent|conviction vacated|cleared by a court|court found (him )?innocent|"
    r"dead (child|children|baby|infant|girl|daughter)|burned (child|children|body|girl|daughter)|"
    r"(children|girls|daughters|babies)('s)? (bodies|corpses|deaths on screen|dying)|child victim|"
    r"(burned|charred) (body|corpse|remains)|bleeding (victim|body)|"
    r"actual house fire with people|firefighters? faces|"
    r"dochighlight",
    re.IGNORECASE)
```

> `BANNED_ACCURACY` mechanizes constraints 1/2/3/6. **Allowed:** "no valid evidence of arson / the arson science was invalidated / could not be sustained / likely accidental / there may have been no crime / never legally exonerated / the case remains contested / flashover / crazed glass from water on hot glass" and **"anonymous / generic / non-identifiable person, face turned or in shadow, adults only."** Banned = claiming legal innocence/exoneration, any child/child-death imagery, victim/burned-body depiction, dochighlight, real-person likeness (anonymized generic people are OK).

---

# 2. Script word count & runtime locked values (basis for A's asset math)

**★ Script is LOCKED: `episodes/_planning/EP51_willingham_script.en.v001.md`. ★ TTS EXISTS and is MEASURED (audit 2026-07-28) — the block below is re-locked; the superseded provisional block is kept underneath for traceability.**

```
words_total          = 3,593 MEASURED (narration body; the "~3,570" estimate was low by 23)
narration_seconds    = 1208.845 MEASURED (ffprobe, vc_master_v001.mp3 · 218 chunks ·
                       1136.253s speech + 72.592s in-master gaps · real pace 189.7 wpm, not 178)
wpm_used             = 189.7 (MEASURED — do not re-derive anything from 178)
total_seconds        = narration 1208.845 + brand interstitial 3.5 + endcard 9.0 = 1221.367 = 20:21.4
durationInFrames     = 36,641 (RE-LOCKED · fps30 · = ceil(1208.845*30)=36266 + 105 + 270 · VO onset 0.0)
mean_shot            = 1208.845 / 395 = 3.060 s/cut · max_shot 7.0
speech ratio         = 1221.367 / 1136.253 = 1.0749 (∈ measured channel band 1.04–1.30 ✓)
visual acts          = 4 VISUAL acts over a 3-ACT SCRIPT (HOOK/OPENING are separate layers):
                       ACT_1 The Monster / ACT_2 The Trial / ACT_3 The Unraveling /
                       ACT_4 The Reckoning (the END payoff — NO script heading; see the note below)
```

> ★ **SUPERSEDED (do not use):** `total_seconds = hook 8.0 + OPENING 3.5 + narration ~1203.4 + endcard 9.0 = ~1223.9`; `durationInFrames = 36,717 (= 240 + 105 + 36102 + 270)`. That 4-term formula **prepends a 240-frame (8.0 s) SILENT HOOK RUNWAY**, which DESIGN §6 explicitly REPLACED with the HOOK-AUDIO / voice-leads-from-0 model. Building to 36,717 would put 8 seconds of voiceless film in front of the cold open — the exact defect the standard exists to prevent. **Use 36,641.**

> ★ **ACT-COUNT WARNING (audit 2026-07-28).** The SCRIPT has **three** acts (`ACT I` / `ACT II` / `ACT III` + `ENDING`). `ACT_4 "The Reckoning"` is a **VISUAL** act only: it is the post-execution stretch (Beyler / Forensic Science Commission / Innocence Project) that sits inside script **ACT III**, plus the ENDING. The measured narration has sections `HOOK / OP / ACT_1 / ACT_2 / ACT_3 / ENDING` and **no `ACT_4`**. Measured narration words per section: HOOK 108 · OP 97 · ACT_1 645 · ACT_2 853 · ACT_3 1,352 · ENDING 538 (= 3,593). Do NOT map `ACT_4` assets by script heading — map by the S-number ranges in §3.2 and the film clock.

**What this means for A:** > **total cuts ~395 / distinct 345 / first-use 87.3% = still 150 + factory 165 + motion 30.** (built up in §3; the "= still + factory + motion" sum is the DISTINCT count 345, same convention as EP52–EP55.)

> **Naming:** still asset IDs are **S001..S150** (1 prompt = 1 image). `covers_scene_id` points into the still ID space (S001..S150). The densest visual acts are ACT_3 (the reversal) and ACT_4 (the reckoning).

---

# 3. ★ Locked asset composition (procure exactly these)

## 3.1 Breakdown (★ procure at these values · do not change)

| Type | distinct | cuts covered | uses(cap) | how procured |
|---|---|---|---|---|
| **SDXL still (body)** | **150** | 170 cuts | 1.133 (≤2) | **150 unique prompts, 1 image each** (§5 · variation 0) |
| **factory real clips** | **165** | 165 cuts | **1 each (1)** | select from 11,000+ stock (§7) · full eyeball · zero sha256 overlap with EP39–50 |
| **i2v motion** | **30** | 60 cuts | 2 each (≤2) | 30 unique seed prompts → Wan (§8) |
| **total (cuts on screen)** | **345** | **395 cuts** | | |
| overlay layers (particle/light/vfx) | 20 | — | composited | **NOT counted in distinct** (§9) |

**SDXL generation batch (includes i2v seeds that never appear as a body cut):**

| Use | count | generation |
|---|---|---|
| body still (`role:"body"`) | **150** | 150 prompts × 1 image (variation 0) |
| i2v seed (`role:"i2v_source"`, separate asset from body) | **30** | 30 seed prompts × 1 image (variation 0) |
| **SDXL batch total** | **150 + 30 = 180 images (each once)** | **NO `--variants` (= 1 image)** |

> **Thumbnails are NOT newly generated.** After completion, reuse **exactly 4** body stills as `also_thumb:true` (§4.3a). **No `role=thumb` / `still_thumb`.**

> **★ Slideshow avoidance (EP40's biggest failure):** **still-cut 170 / (factory 165 + i2v 60)=video 225** gives **still-share 43.04% ≤45% · motion coverage 56.96% ≥45%** structurally (§3.3). **Do not grow stills and shrink factory.**

## 3.2 Per-act allocation of still 150 / factory 165 / i2v 30 (★ still is locked; factory/i2v per-act is a target; only totals are locked)

| Section | still (S# · locked) | factory (target) | i2v (locked total 30) | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING | **16** (S001–S016) | 10 | 3 (M01–M03) | S001 |
| ACT_1 "The Monster" | **30** (S017–S046) | 34 | 6 (M04–M09) | — |
| ACT_2 "The Trial" | **34** (S047–S080) | 30 | 6 (M10–M15) | S048 |
| ACT_3 "The Unraveling" (reversal · densest) | **32** (S081–S112) | 32 | 8 (M16–M23) | S081 |
| ACT_4 "The Reckoning" (END payoff) | **38** (S113–S150) | 33 | 7 (M24–M30) | S120 |
| connective (covers_scene_id:null) | — | 26 | — | — |
| **total** | **150** | **165** | **30** | **4** |

> **still per-act (16/30/34/32/38 = 150) is locked** (the §5.6 motif library is built to this split). Per-act factory/i2v splits are targets (only totals 165 / 30 are locked). Gates only check factory each-once total 165, motion each ≤2 total 60.

## 3.3 Full arithmetic (★ Codex recomputes and confirms)

```
[1] total cuts 395 = still 170 + factory 165 + i2v 60
[2] mean shot = narration 1208.845 (MEASURED) / 395 = 3.060 s/cut  ✓ (≤7.0)   [was 1203.4 → 3.046]
[3] still-share (check_animation_mix) = 170/395 = 43.04%  ✓ ≤45%
[4] motion coverage = (165+60)/395 = 225/395 = 56.96%     ✓ ≥45%
[5] per-asset cap: still 170/150=1.133(≤2) / factory 165/165=1.0(≤1) / motion 60/30=2.0(≤2)  ✓
[6] first-use share = 345/395 = 0.8734                    ✓ ≥0.70
[7] factory floor = 1208.845/30 = 40.3 → ≥41 clips. design 165 ✓ (protects still-share ≤0.45)
```

> **RE-CHECKED against MEASURED TTS (2026-07-28):** narration moved 1203.4 → 1208.845 (+5.4 s). Lines [1][3][4][5][6] are ratios of COUNTS and are unchanged; only [2] and [7] were re-derived. Ratios (still-share ≤0.45, first-use ≥0.70) hold; do NOT grow stills and shrink factory.

---

# 4. ★ Boundary contract: `asset_manifest.v001.json` (the one file linking A and B)

**Path:** `episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json`
**Schema version:** `willingham_assets.v1` (fixed string)
**Producer:** `scripts/build_willingham_asset_manifest.py` (**A implements. No one else writes this file**)
**★ A(producer) and B(consumer/validator) share counts / role enum / overlay count / also_thumb set byte-for-byte.** role enum = **`body | i2v_source | reject` only** (no `thumb`/`still_thumb`). Thumbnails = `also_thumb:true` body stills, **exactly 4**. overlay = **exactly 20**.

## 4.1 Schema (`willingham_assets.v1`)

```jsonc
{
  "schema_version": "willingham_assets.v1",
  "episode_id": "PD-2026-051-willingham",
  "slug": "willingham",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_willingham_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 150,         // ==150
    "still_i2v_source": 30,    // ==30
    "motion": 30,              // ==30
    "factory": 165,            // ==165
    "overlay": 20              // ==20 (not counted in distinct)
  },
  "stills":  [ /* §4.3: body 150 (WLM-S001..S150) + i2v_source 30 (WLM-MS01..MS30) */ ],
  "motion":  [ /* §4.5: WLM-M01..M30 all 30 · public_path required (★ non-empty) */ ],
  "factory": [ /* §4.4: 165 · public_path required (★ non-empty · EP45-avoidance core) */ ],
  "overlay": [ /* §4.6: 20 */ ]
}
```

### 4.1a stills[] entry shape (body example) — ★ NO depth_path (depth treatment banned)

```jsonc
{
  "asset_id": "WLM-S001",                 // body: ^WLM-S\d{3}$ (001..150) / i2v seed: ^WLM-MS\d{2}$
  "scene_id": "S001",                     // still ID space (§5.9 prompt line · S001..S150)
  "role": "body",                         // body|i2v_source|reject (1 image each)
  "also_thumb": false,                    // exactly 4 body stills true (§4.3a)
  "act": 0,                               // 0=HOOK/OPENING, 1..4=ACT_1..ACT_4
  "path": "H:/pd-media/assets/ai/willingham/S001.png",
  "public_path": "willingham/img/S001.png",   // role=="body" only, non-null
  "width": 3840, "height": 2160,          // long edge >=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 26.0,
  "tags": ["frame_house","ember_glow","from_the_yard","no_children","symbolic","no_face"],
  "caption_hint": "a wood-frame house at night seen only from the yard, an ember glow in its windows, no person and no child, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_child_or_victim": false,
         "has_human_body": false, "notes": ""}
         // reject triggers: has_readable_text OR has_identifiable_real_person OR has_child_or_victim.
         // has_human_body:true is NOT a reject (anonymized adults OK · H-series).
}
```
> **★ No `depth_path` field.** `treatment:"depth"` is banned this film (§5.5 / CODEX_B §5.2), so body stills need no depth map. `role=="body"` requires `public_path` only.

## 4.2 `--verify` invariants (BLOCKING · byte-identical to B's validator)

1. `schema_version=="willingham_assets.v1"` / `episode_id`/`slug` match / `is_stub==false`
2. `counts.*` equal each array's real length and the §4.1 values (body 150 / i2v_source 30 / motion 30 / factory 165 / overlay 20)
3. all `path`/`public_path` exist on disk
4. `sha256` unique across all arrays (zero dupes)
5. every `role!="reject"` still has `max(width,height)>=3840`
6. `role=="body"` has non-null `public_path` that exists. **No `depth_path` required or expected** (depth banned)
7. `qc.has_readable_text==true` OR `qc.has_identifiable_real_person==true` OR `qc.has_child_or_victim==true` ⇒ `role=="reject"`. **`qc.has_human_body==true` is NOT a reject** (anonymized adults OK). `has_child_or_victim` covers any child/baby/infant/victim/burned-body — always reject
8. `role=="i2v_source"` shares no `asset_id` with `role=="body"` (i2v_source = `^WLM-MS\d{2}$`)
9. all JSON strings match neither `BANNED_PORTRAIT` nor `BANNED_ACCURACY` (§1.3)
10. `factory[].license`/`overlay[].license` ∈ `ALLOWED_LICENSES` (§7.4)
11. `factory[].sha256` collides with none of EP39–EP50 (twelve episodes) staged assets (§7.7)
12. `factory[].eyeballed_content` non-empty
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` count is **exactly 4**, and its `scene_id` set exactly equals §4.3a's 4-set (**this set is an A↔B contract, byte-identical to CODEX_B**)
15. no `role` value `thumb`/`still_thumb` (enum = body|i2v_source|reject)
16. `overlay` length **exactly 20**
17. ★ `factory` length **==165** and every entry's `public_path` non-empty (EP45-avoidance)
18. ★ `motion` length **==30** and every entry's `public_path` non-empty (same)

`--reuse-feasibility` recomputes §3.3 [5][6][7]; any breach → exit 1.

## 4.3 `role` assignment (mechanical)

```
1. body 150 (S001..S150) = §5.9 150 prompts' output. 1 image each.
   ├─ ~110 symbolic objects: [STYLE]/[NEG] · qc.has_human_body:false
   └─ ~40 anonymized-human present (§5.6a S-numbers): [HSTYLE]/[HNEG] · qc.has_human_body:true / has_identifiable_real_person:false / has_child_or_victim:false
2. i2v_source 30 (MS01..MS30 / seed images M01_src..M30_src) = §8.1a's 30 seed prompts. 1 each. Never reassigned to body (invariant 8).
   └─ 15 human (H001–H015 · [HSTYLE]/[HNEG] · has_human_body:true) + 15 abstract ([STYLE]/[NEG])
3. also_thumb : body's §4.3a 4 stills set true (no extra generation · all 4 are OBJECT beats)
4. reject : QC failures (kept in manifest with qc.notes) → regen same prompt in §6.3
```

### 4.3a ★ also_thumb set (exactly 4 · byte-identical to CODEX_B)

```
{ WLM-S001 (the frame house, ember glow, from the yard — the cold-open),
  WLM-S048 (the two pillars — the fire and the informant),
  WLM-S081 (flashover — the reversal · the char re-lit cold),
  WLM-S120 (cold forensic science — the empty gurney / "could not be sustained") }
```
> Thumbnail concept (§11): a dramatized non-real face at dread, ember firelight, over a dark blurred wood-frame house — no real-person likeness, no children, ad-safe. This 4-set must carry the anchor motif at the named S# (§5.6 assigns them).

## 4.4 ★ `factory[]` all 165 entries (★ must materialize · public_path non-empty · EP45-avoidance core)

> `select_willingham_factory.py` consumes the table below with **public_path / act / covers_scene_id / subtype pre-assigned**, and fills `asset_id` (shelf id) / `path` (`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`) / `sha256` / `duration_sec` / `width` / `height` / `mean_luma` / `license` / `eyeballed_content` / `qc` at selection/eyeball time (§7). **Never write an empty array.** Each public_path = `willingham/factory/F0NN_<subtype>.mp4`. `type:"backgrounds"`, `kind:"video"`. `_02`/`_03` = "another clip on the same search theme" (different sha256, different clip — NOT a duplicate file).

```jsonc
// HOOK+OPENING (act 0) — 10
{ "public_path":"willingham/factory/F001_wood_frame_house_night.mp4", "act":0, "covers_scene_id":"S001", "subtype":"wood_frame_house_night" }
{ "public_path":"willingham/factory/F002_small_town_residential_street_night.mp4", "act":0, "covers_scene_id":"S005", "subtype":"small_town_residential_street_night" }
{ "public_path":"willingham/factory/F003_ember_glow_abstract_dark.mp4", "act":0, "covers_scene_id":null, "subtype":"ember_glow_abstract_dark" }
{ "public_path":"willingham/factory/F004_ash_falling_black_bg.mp4", "act":0, "covers_scene_id":null, "subtype":"ash_falling_black_bg" }
{ "public_path":"willingham/factory/F005_smoke_drift_dark.mp4", "act":0, "covers_scene_id":null, "subtype":"smoke_drift_dark" }
{ "public_path":"willingham/factory/F006_dark_porch_yard_night.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_porch_yard_night" }
{ "public_path":"willingham/factory/F007_texas_town_dusk_wide.mp4", "act":0, "covers_scene_id":null, "subtype":"texas_town_dusk_wide" }
{ "public_path":"willingham/factory/F008_night_sky_ember_haze_far.mp4", "act":0, "covers_scene_id":null, "subtype":"night_sky_ember_haze_far" }
{ "public_path":"willingham/factory/F009_wall_clock_dim_room.mp4", "act":0, "covers_scene_id":"S014", "subtype":"wall_clock_dim_room" }
{ "public_path":"willingham/factory/F010_dark_institutional_room_cold.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_institutional_room_cold" }
// ACT_1 THE MONSTER (act 1) — 34
{ "public_path":"willingham/factory/F011_charred_house_shell_exterior.mp4", "act":1, "covers_scene_id":"S017", "subtype":"charred_house_shell_exterior" }
{ "public_path":"willingham/factory/F012_burned_wood_char_texture.mp4", "act":1, "covers_scene_id":"S018", "subtype":"burned_wood_char_texture" }
{ "public_path":"willingham/factory/F013_fire_scene_aftermath_no_people.mp4", "act":1, "covers_scene_id":"S019", "subtype":"fire_scene_aftermath_no_people" }
{ "public_path":"willingham/factory/F014_corsicana_style_street_day.mp4", "act":1, "covers_scene_id":"S043", "subtype":"corsicana_style_street_day" }
{ "public_path":"willingham/factory/F015_frame_houses_row_day.mp4", "act":1, "covers_scene_id":null, "subtype":"frame_houses_row_day" }
{ "public_path":"willingham/factory/F016_front_yard_grass_dry.mp4", "act":1, "covers_scene_id":null, "subtype":"front_yard_grass_dry" }
{ "public_path":"willingham/factory/F017_cemetery_exterior_restrained.mp4", "act":1, "covers_scene_id":"S039", "subtype":"cemetery_exterior_restrained" }
{ "public_path":"willingham/factory/F018_small_town_church_exterior.mp4", "act":1, "covers_scene_id":null, "subtype":"small_town_church_exterior" }
{ "public_path":"willingham/factory/F019_dim_bedroom_wall_poster_shadow.mp4", "act":1, "covers_scene_id":"S031", "subtype":"dim_bedroom_wall_poster_shadow" }
{ "public_path":"willingham/factory/F020_kitchen_doorway_dim_abstract.mp4", "act":1, "covers_scene_id":null, "subtype":"kitchen_doorway_dim_abstract" }
{ "public_path":"willingham/factory/F021_town_dusk_streetlights.mp4", "act":1, "covers_scene_id":null, "subtype":"town_dusk_streetlights" }
{ "public_path":"willingham/factory/F022_ash_over_ruins_slow.mp4", "act":1, "covers_scene_id":null, "subtype":"ash_over_ruins_slow" }
{ "public_path":"willingham/factory/F023_charred_house_shell_exterior_02.mp4", "act":1, "covers_scene_id":null, "subtype":"charred_house_shell_exterior_02" }
{ "public_path":"willingham/factory/F024_burned_wood_char_texture_02.mp4", "act":1, "covers_scene_id":null, "subtype":"burned_wood_char_texture_02" }
{ "public_path":"willingham/factory/F025_fire_scene_aftermath_no_people_02.mp4", "act":1, "covers_scene_id":null, "subtype":"fire_scene_aftermath_no_people_02" }
{ "public_path":"willingham/factory/F026_corsicana_style_street_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"corsicana_style_street_day_02" }
{ "public_path":"willingham/factory/F027_frame_houses_row_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"frame_houses_row_day_02" }
{ "public_path":"willingham/factory/F028_front_yard_grass_dry_02.mp4", "act":1, "covers_scene_id":null, "subtype":"front_yard_grass_dry_02" }
{ "public_path":"willingham/factory/F029_cemetery_exterior_restrained_02.mp4", "act":1, "covers_scene_id":null, "subtype":"cemetery_exterior_restrained_02" }
{ "public_path":"willingham/factory/F030_small_town_church_exterior_02.mp4", "act":1, "covers_scene_id":null, "subtype":"small_town_church_exterior_02" }
{ "public_path":"willingham/factory/F031_dim_bedroom_wall_poster_shadow_02.mp4", "act":1, "covers_scene_id":null, "subtype":"dim_bedroom_wall_poster_shadow_02" }
{ "public_path":"willingham/factory/F032_kitchen_doorway_dim_abstract_02.mp4", "act":1, "covers_scene_id":null, "subtype":"kitchen_doorway_dim_abstract_02" }
{ "public_path":"willingham/factory/F033_town_dusk_streetlights_02.mp4", "act":1, "covers_scene_id":null, "subtype":"town_dusk_streetlights_02" }
{ "public_path":"willingham/factory/F034_ash_over_ruins_slow_02.mp4", "act":1, "covers_scene_id":null, "subtype":"ash_over_ruins_slow_02" }
{ "public_path":"willingham/factory/F035_charred_house_shell_exterior_03.mp4", "act":1, "covers_scene_id":null, "subtype":"charred_house_shell_exterior_03" }
{ "public_path":"willingham/factory/F036_burned_wood_char_texture_03.mp4", "act":1, "covers_scene_id":null, "subtype":"burned_wood_char_texture_03" }
{ "public_path":"willingham/factory/F037_corsicana_style_street_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"corsicana_style_street_day_03" }
{ "public_path":"willingham/factory/F038_frame_houses_row_day_03.mp4", "act":1, "covers_scene_id":null, "subtype":"frame_houses_row_day_03" }
{ "public_path":"willingham/factory/F039_front_yard_grass_dry_03.mp4", "act":1, "covers_scene_id":null, "subtype":"front_yard_grass_dry_03" }
{ "public_path":"willingham/factory/F040_town_dusk_streetlights_03.mp4", "act":1, "covers_scene_id":null, "subtype":"town_dusk_streetlights_03" }
{ "public_path":"willingham/factory/F041_ash_over_ruins_slow_03.mp4", "act":1, "covers_scene_id":null, "subtype":"ash_over_ruins_slow_03" }
{ "public_path":"willingham/factory/F042_smoke_drift_dark_02.mp4", "act":1, "covers_scene_id":null, "subtype":"smoke_drift_dark_02" }
{ "public_path":"willingham/factory/F043_fire_scene_aftermath_no_people_03.mp4", "act":1, "covers_scene_id":null, "subtype":"fire_scene_aftermath_no_people_03" }
{ "public_path":"willingham/factory/F044_dim_bedroom_wall_poster_shadow_03.mp4", "act":1, "covers_scene_id":null, "subtype":"dim_bedroom_wall_poster_shadow_03" }
// ACT_2 THE TRIAL (act 2) — 30
{ "public_path":"willingham/factory/F045_texas_county_courthouse_exterior.mp4", "act":2, "covers_scene_id":"S077", "subtype":"texas_county_courthouse_exterior" }
{ "public_path":"willingham/factory/F046_courtroom_interior_empty.mp4", "act":2, "covers_scene_id":"S073", "subtype":"courtroom_interior_empty" }
{ "public_path":"willingham/factory/F047_county_jail_exterior_day.mp4", "act":2, "covers_scene_id":"S063", "subtype":"county_jail_exterior_day" }
{ "public_path":"willingham/factory/F048_jail_corridor_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"jail_corridor_cold" }
{ "public_path":"willingham/factory/F049_witness_stand_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty" }
{ "public_path":"willingham/factory/F050_judges_bench_empty.mp4", "act":2, "covers_scene_id":null, "subtype":"judges_bench_empty" }
{ "public_path":"willingham/factory/F051_char_pattern_floor_ember.mp4", "act":2, "covers_scene_id":"S053", "subtype":"char_pattern_floor_ember" }
{ "public_path":"willingham/factory/F052_crazed_glass_crack_texture.mp4", "act":2, "covers_scene_id":"S055", "subtype":"crazed_glass_crack_texture" }
{ "public_path":"willingham/factory/F053_door_threshold_burn_abstract.mp4", "act":2, "covers_scene_id":null, "subtype":"door_threshold_burn_abstract" }
{ "public_path":"willingham/factory/F054_liquid_pour_dark_abstract.mp4", "act":2, "covers_scene_id":null, "subtype":"liquid_pour_dark_abstract" }
{ "public_path":"willingham/factory/F055_jail_bars_shadow_cold.mp4", "act":2, "covers_scene_id":null, "subtype":"jail_bars_shadow_cold" }
{ "public_path":"willingham/factory/F056_courthouse_corridor_long.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_corridor_long" }
{ "public_path":"willingham/factory/F057_gavel_bench_still.mp4", "act":2, "covers_scene_id":null, "subtype":"gavel_bench_still" }
{ "public_path":"willingham/factory/F058_texas_county_courthouse_exterior_02.mp4", "act":2, "covers_scene_id":null, "subtype":"texas_county_courthouse_exterior_02" }
{ "public_path":"willingham/factory/F059_courtroom_interior_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_interior_empty_02" }
{ "public_path":"willingham/factory/F060_county_jail_exterior_day_02.mp4", "act":2, "covers_scene_id":null, "subtype":"county_jail_exterior_day_02" }
{ "public_path":"willingham/factory/F061_jail_corridor_cold_02.mp4", "act":2, "covers_scene_id":null, "subtype":"jail_corridor_cold_02" }
{ "public_path":"willingham/factory/F062_char_pattern_floor_ember_02.mp4", "act":2, "covers_scene_id":null, "subtype":"char_pattern_floor_ember_02" }
{ "public_path":"willingham/factory/F063_crazed_glass_crack_texture_02.mp4", "act":2, "covers_scene_id":null, "subtype":"crazed_glass_crack_texture_02" }
{ "public_path":"willingham/factory/F064_door_threshold_burn_abstract_02.mp4", "act":2, "covers_scene_id":null, "subtype":"door_threshold_burn_abstract_02" }
{ "public_path":"willingham/factory/F065_courthouse_corridor_long_02.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_corridor_long_02" }
{ "public_path":"willingham/factory/F066_witness_stand_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"witness_stand_empty_02" }
{ "public_path":"willingham/factory/F067_texas_county_courthouse_exterior_03.mp4", "act":2, "covers_scene_id":null, "subtype":"texas_county_courthouse_exterior_03" }
{ "public_path":"willingham/factory/F068_courtroom_interior_empty_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courtroom_interior_empty_03" }
{ "public_path":"willingham/factory/F069_county_jail_exterior_day_03.mp4", "act":2, "covers_scene_id":null, "subtype":"county_jail_exterior_day_03" }
{ "public_path":"willingham/factory/F070_char_pattern_floor_ember_03.mp4", "act":2, "covers_scene_id":null, "subtype":"char_pattern_floor_ember_03" }
{ "public_path":"willingham/factory/F071_crazed_glass_crack_texture_03.mp4", "act":2, "covers_scene_id":null, "subtype":"crazed_glass_crack_texture_03" }
{ "public_path":"willingham/factory/F072_jail_corridor_cold_03.mp4", "act":2, "covers_scene_id":null, "subtype":"jail_corridor_cold_03" }
{ "public_path":"willingham/factory/F073_courthouse_corridor_long_03.mp4", "act":2, "covers_scene_id":null, "subtype":"courthouse_corridor_long_03" }
{ "public_path":"willingham/factory/F074_gavel_bench_still_02.mp4", "act":2, "covers_scene_id":null, "subtype":"gavel_bench_still_02" }
// ACT_3 THE UNRAVELING (act 3) — 32
{ "public_path":"willingham/factory/F075_fire_science_lab_flame_test.mp4", "act":3, "covers_scene_id":"S093", "subtype":"fire_science_lab_flame_test" }
{ "public_path":"willingham/factory/F076_documents_files_unreadable.mp4", "act":3, "covers_scene_id":"S103", "subtype":"documents_files_unreadable" }
{ "public_path":"willingham/factory/F077_letters_envelopes_desk.mp4", "act":3, "covers_scene_id":"S099", "subtype":"letters_envelopes_desk" }
{ "public_path":"willingham/factory/F078_death_row_institution_exterior.mp4", "act":3, "covers_scene_id":"S107", "subtype":"death_row_institution_exterior" }
{ "public_path":"willingham/factory/F079_prison_corridor_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_cold" }
{ "public_path":"willingham/factory/F080_bare_chamber_cold_abstract.mp4", "act":3, "covers_scene_id":"S107", "subtype":"bare_chamber_cold_abstract" }
{ "public_path":"willingham/factory/F081_incandescent_room_glow_abstract.mp4", "act":3, "covers_scene_id":"S081", "subtype":"incandescent_room_glow_abstract" }
{ "public_path":"willingham/factory/F082_ember_to_cold_transition_abstract.mp4", "act":3, "covers_scene_id":null, "subtype":"ember_to_cold_transition_abstract" }
{ "public_path":"willingham/factory/F083_lab_bench_beakers_cold.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_beakers_cold" }
{ "public_path":"willingham/factory/F084_hose_water_on_glass_abstract.mp4", "act":3, "covers_scene_id":"S089", "subtype":"hose_water_on_glass_abstract" }
{ "public_path":"willingham/factory/F085_dusk_sky_cold_clear.mp4", "act":3, "covers_scene_id":null, "subtype":"dusk_sky_cold_clear" }
{ "public_path":"willingham/factory/F086_desk_paper_slides_in_abstract.mp4", "act":3, "covers_scene_id":"S103", "subtype":"desk_paper_slides_in_abstract" }
{ "public_path":"willingham/factory/F087_fire_science_lab_flame_test_02.mp4", "act":3, "covers_scene_id":null, "subtype":"fire_science_lab_flame_test_02" }
{ "public_path":"willingham/factory/F088_documents_files_unreadable_02.mp4", "act":3, "covers_scene_id":null, "subtype":"documents_files_unreadable_02" }
{ "public_path":"willingham/factory/F089_letters_envelopes_desk_02.mp4", "act":3, "covers_scene_id":null, "subtype":"letters_envelopes_desk_02" }
{ "public_path":"willingham/factory/F090_death_row_institution_exterior_02.mp4", "act":3, "covers_scene_id":null, "subtype":"death_row_institution_exterior_02" }
{ "public_path":"willingham/factory/F091_prison_corridor_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_cold_02" }
{ "public_path":"willingham/factory/F092_bare_chamber_cold_abstract_02.mp4", "act":3, "covers_scene_id":null, "subtype":"bare_chamber_cold_abstract_02" }
{ "public_path":"willingham/factory/F093_incandescent_room_glow_abstract_02.mp4", "act":3, "covers_scene_id":null, "subtype":"incandescent_room_glow_abstract_02" }
{ "public_path":"willingham/factory/F094_lab_bench_beakers_cold_02.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_beakers_cold_02" }
{ "public_path":"willingham/factory/F095_dusk_sky_cold_clear_02.mp4", "act":3, "covers_scene_id":null, "subtype":"dusk_sky_cold_clear_02" }
{ "public_path":"willingham/factory/F096_fire_science_lab_flame_test_03.mp4", "act":3, "covers_scene_id":null, "subtype":"fire_science_lab_flame_test_03" }
{ "public_path":"willingham/factory/F097_documents_files_unreadable_03.mp4", "act":3, "covers_scene_id":null, "subtype":"documents_files_unreadable_03" }
{ "public_path":"willingham/factory/F098_letters_envelopes_desk_03.mp4", "act":3, "covers_scene_id":null, "subtype":"letters_envelopes_desk_03" }
{ "public_path":"willingham/factory/F099_death_row_institution_exterior_03.mp4", "act":3, "covers_scene_id":null, "subtype":"death_row_institution_exterior_03" }
{ "public_path":"willingham/factory/F100_prison_corridor_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"prison_corridor_cold_03" }
{ "public_path":"willingham/factory/F101_incandescent_room_glow_abstract_03.mp4", "act":3, "covers_scene_id":null, "subtype":"incandescent_room_glow_abstract_03" }
{ "public_path":"willingham/factory/F102_ember_to_cold_transition_abstract_02.mp4", "act":3, "covers_scene_id":null, "subtype":"ember_to_cold_transition_abstract_02" }
{ "public_path":"willingham/factory/F103_lab_bench_beakers_cold_03.mp4", "act":3, "covers_scene_id":null, "subtype":"lab_bench_beakers_cold_03" }
{ "public_path":"willingham/factory/F104_hose_water_on_glass_abstract_02.mp4", "act":3, "covers_scene_id":null, "subtype":"hose_water_on_glass_abstract_02" }
{ "public_path":"willingham/factory/F105_dusk_sky_cold_clear_03.mp4", "act":3, "covers_scene_id":null, "subtype":"dusk_sky_cold_clear_03" }
{ "public_path":"willingham/factory/F106_bare_chamber_cold_abstract_03.mp4", "act":3, "covers_scene_id":null, "subtype":"bare_chamber_cold_abstract_03" }
// ACT_4 THE RECKONING (act 4) — 33
{ "public_path":"willingham/factory/F107_state_official_building_exterior.mp4", "act":4, "covers_scene_id":"S121", "subtype":"state_official_building_exterior" }
{ "public_path":"willingham/factory/F108_empty_conference_room_cold.mp4", "act":4, "covers_scene_id":"S121", "subtype":"empty_conference_room_cold" }
{ "public_path":"willingham/factory/F109_report_pages_unreadable.mp4", "act":4, "covers_scene_id":"S127", "subtype":"report_pages_unreadable" }
{ "public_path":"willingham/factory/F110_newsprint_texture_unreadable.mp4", "act":4, "covers_scene_id":null, "subtype":"newsprint_texture_unreadable" }
{ "public_path":"willingham/factory/F111_dawn_texas_plains_cold.mp4", "act":4, "covers_scene_id":"S143", "subtype":"dawn_texas_plains_cold" }
{ "public_path":"willingham/factory/F112_quiet_cemetery_wide_restrained.mp4", "act":4, "covers_scene_id":null, "subtype":"quiet_cemetery_wide_restrained" }
{ "public_path":"willingham/factory/F113_empty_chair_cold_room.mp4", "act":4, "covers_scene_id":"S147", "subtype":"empty_chair_cold_room" }
{ "public_path":"willingham/factory/F114_balance_scale_still_abstract.mp4", "act":4, "covers_scene_id":"S135", "subtype":"balance_scale_still_abstract" }
{ "public_path":"willingham/factory/F115_cold_clear_daylight_window.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_clear_daylight_window" }
{ "public_path":"willingham/factory/F116_empty_yard_cold_dawn.mp4", "act":4, "covers_scene_id":"S143", "subtype":"empty_yard_cold_dawn" }
{ "public_path":"willingham/factory/F117_state_official_building_exterior_02.mp4", "act":4, "covers_scene_id":null, "subtype":"state_official_building_exterior_02" }
{ "public_path":"willingham/factory/F118_empty_conference_room_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_conference_room_cold_02" }
{ "public_path":"willingham/factory/F119_report_pages_unreadable_02.mp4", "act":4, "covers_scene_id":null, "subtype":"report_pages_unreadable_02" }
{ "public_path":"willingham/factory/F120_newsprint_texture_unreadable_02.mp4", "act":4, "covers_scene_id":null, "subtype":"newsprint_texture_unreadable_02" }
{ "public_path":"willingham/factory/F121_dawn_texas_plains_cold_02.mp4", "act":4, "covers_scene_id":null, "subtype":"dawn_texas_plains_cold_02" }
{ "public_path":"willingham/factory/F122_quiet_cemetery_wide_restrained_02.mp4", "act":4, "covers_scene_id":null, "subtype":"quiet_cemetery_wide_restrained_02" }
{ "public_path":"willingham/factory/F123_empty_chair_cold_room_02.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_chair_cold_room_02" }
{ "public_path":"willingham/factory/F124_balance_scale_still_abstract_02.mp4", "act":4, "covers_scene_id":null, "subtype":"balance_scale_still_abstract_02" }
{ "public_path":"willingham/factory/F125_cold_clear_daylight_window_02.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_clear_daylight_window_02" }
{ "public_path":"willingham/factory/F126_empty_yard_cold_dawn_02.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_yard_cold_dawn_02" }
{ "public_path":"willingham/factory/F127_state_official_building_exterior_03.mp4", "act":4, "covers_scene_id":null, "subtype":"state_official_building_exterior_03" }
{ "public_path":"willingham/factory/F128_empty_conference_room_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_conference_room_cold_03" }
{ "public_path":"willingham/factory/F129_report_pages_unreadable_03.mp4", "act":4, "covers_scene_id":null, "subtype":"report_pages_unreadable_03" }
{ "public_path":"willingham/factory/F130_dawn_texas_plains_cold_03.mp4", "act":4, "covers_scene_id":null, "subtype":"dawn_texas_plains_cold_03" }
{ "public_path":"willingham/factory/F131_quiet_cemetery_wide_restrained_03.mp4", "act":4, "covers_scene_id":null, "subtype":"quiet_cemetery_wide_restrained_03" }
{ "public_path":"willingham/factory/F132_empty_chair_cold_room_03.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_chair_cold_room_03" }
{ "public_path":"willingham/factory/F133_cold_clear_daylight_window_03.mp4", "act":4, "covers_scene_id":null, "subtype":"cold_clear_daylight_window_03" }
{ "public_path":"willingham/factory/F134_empty_yard_cold_dawn_03.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_yard_cold_dawn_03" }
{ "public_path":"willingham/factory/F135_balance_scale_still_abstract_03.mp4", "act":4, "covers_scene_id":null, "subtype":"balance_scale_still_abstract_03" }
{ "public_path":"willingham/factory/F136_newsprint_texture_unreadable_03.mp4", "act":4, "covers_scene_id":null, "subtype":"newsprint_texture_unreadable_03" }
{ "public_path":"willingham/factory/F137_report_pages_unreadable_04.mp4", "act":4, "covers_scene_id":null, "subtype":"report_pages_unreadable_04" }
{ "public_path":"willingham/factory/F138_dawn_texas_plains_cold_04.mp4", "act":4, "covers_scene_id":null, "subtype":"dawn_texas_plains_cold_04" }
{ "public_path":"willingham/factory/F139_empty_chair_cold_room_04.mp4", "act":4, "covers_scene_id":null, "subtype":"empty_chair_cold_room_04" }
// CONNECTIVE (covers_scene_id:null) — 26
{ "public_path":"willingham/factory/F140_abstract_loop_dark_drift.mp4", "act":0, "covers_scene_id":null, "subtype":"abstract_loop_dark_drift" }
{ "public_path":"willingham/factory/F141_ash_drift_slow_black.mp4", "act":0, "covers_scene_id":null, "subtype":"ash_drift_slow_black" }
{ "public_path":"willingham/factory/F142_sky_gradient_dusk.mp4", "act":0, "covers_scene_id":null, "subtype":"sky_gradient_dusk" }
{ "public_path":"willingham/factory/F143_texture_pan_charred_wood.mp4", "act":0, "covers_scene_id":null, "subtype":"texture_pan_charred_wood" }
{ "public_path":"willingham/factory/F144_cold_light_slow_move.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_light_slow_move" }
{ "public_path":"willingham/factory/F145_ember_sparks_rising_dark.mp4", "act":0, "covers_scene_id":null, "subtype":"ember_sparks_rising_dark" }
{ "public_path":"willingham/factory/F146_two_lane_road_texas_far.mp4", "act":0, "covers_scene_id":null, "subtype":"two_lane_road_texas_far" }
{ "public_path":"willingham/factory/F147_plains_grass_wind_cold.mp4", "act":0, "covers_scene_id":null, "subtype":"plains_grass_wind_cold" }
{ "public_path":"willingham/factory/F148_night_window_dim_glow.mp4", "act":0, "covers_scene_id":null, "subtype":"night_window_dim_glow" }
{ "public_path":"willingham/factory/F149_abstract_loop_dark_drift_02.mp4", "act":0, "covers_scene_id":null, "subtype":"abstract_loop_dark_drift_02" }
{ "public_path":"willingham/factory/F150_ash_drift_slow_black_02.mp4", "act":0, "covers_scene_id":null, "subtype":"ash_drift_slow_black_02" }
{ "public_path":"willingham/factory/F151_sky_gradient_dusk_02.mp4", "act":0, "covers_scene_id":null, "subtype":"sky_gradient_dusk_02" }
{ "public_path":"willingham/factory/F152_texture_pan_charred_wood_02.mp4", "act":0, "covers_scene_id":null, "subtype":"texture_pan_charred_wood_02" }
{ "public_path":"willingham/factory/F153_cold_light_slow_move_02.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_light_slow_move_02" }
{ "public_path":"willingham/factory/F154_ember_sparks_rising_dark_02.mp4", "act":0, "covers_scene_id":null, "subtype":"ember_sparks_rising_dark_02" }
{ "public_path":"willingham/factory/F155_two_lane_road_texas_far_02.mp4", "act":0, "covers_scene_id":null, "subtype":"two_lane_road_texas_far_02" }
{ "public_path":"willingham/factory/F156_plains_grass_wind_cold_02.mp4", "act":0, "covers_scene_id":null, "subtype":"plains_grass_wind_cold_02" }
{ "public_path":"willingham/factory/F157_night_window_dim_glow_02.mp4", "act":0, "covers_scene_id":null, "subtype":"night_window_dim_glow_02" }
{ "public_path":"willingham/factory/F158_abstract_loop_dark_drift_03.mp4", "act":0, "covers_scene_id":null, "subtype":"abstract_loop_dark_drift_03" }
{ "public_path":"willingham/factory/F159_ash_drift_slow_black_03.mp4", "act":0, "covers_scene_id":null, "subtype":"ash_drift_slow_black_03" }
{ "public_path":"willingham/factory/F160_sky_gradient_dusk_03.mp4", "act":0, "covers_scene_id":null, "subtype":"sky_gradient_dusk_03" }
{ "public_path":"willingham/factory/F161_texture_pan_charred_wood_03.mp4", "act":0, "covers_scene_id":null, "subtype":"texture_pan_charred_wood_03" }
{ "public_path":"willingham/factory/F162_cold_light_slow_move_03.mp4", "act":0, "covers_scene_id":null, "subtype":"cold_light_slow_move_03" }
{ "public_path":"willingham/factory/F163_ember_sparks_rising_dark_03.mp4", "act":0, "covers_scene_id":null, "subtype":"ember_sparks_rising_dark_03" }
{ "public_path":"willingham/factory/F164_plains_grass_wind_cold_03.mp4", "act":0, "covers_scene_id":null, "subtype":"plains_grass_wind_cold_03" }
{ "public_path":"willingham/factory/F165_night_window_dim_glow_03.mp4", "act":0, "covers_scene_id":null, "subtype":"night_window_dim_glow_03" }
```
> **Count check: 10 + 34 + 30 + 32 + 33 + 26 = 165 ✓.** subtype `_02`/`_03`/`_04` = distinct clips on the same theme (different sha256), never the same file twice. **No `dark cell interior with a body`, no `actual fire with people`, no `firefighter/juror/mourner faces`, no readable newsprint.**

## 4.5 ★ `motion[]` all 30 entries (★ must materialize · public_path non-empty)

> Each is an i2v result. `public_path` = `willingham/motion/M<NN>_rife.mp4` (ends `.mp4`, contains `_rife`). `source_scene_id` points at the i2v seed (`WLM-MS<NN>`). Per-act pre-assigned (HOOK 3 / ACT_1 6 / ACT_2 6 / ACT_3 8 / ACT_4 7 = 30). **★ 15 of the 30 are the anonymized H-series human beats** (§5.11 · owner directive: more human presence, less "empty/lonely, objects-only"): M02, M04, M05, M08, M09, M11, M12, M14, M15, M17, M20, M21, M23, M25, M26. The other 15 are abstract/symbolic (pure science + objects). **All human beats: from-behind / shadow / silhouette / hands, adults only, no likeness, no child, no body, no readable text.**

```jsonc
{ "public_path":"willingham/motion/M01_rife.mp4", "act":0, "source_scene_id":"WLM-MS01", "storyboard":"a wood-frame house at night, ember glow rising in the windows, seen from the yard, no person, no child", "human":false }
{ "public_path":"willingham/motion/M02_rife.mp4", "act":0, "source_scene_id":"WLM-MS02", "storyboard":"H001: a firelit anonymous figure in a dark yard seen from behind, held back from an ember glow, no face, no child in frame", "human":true }
{ "public_path":"willingham/motion/M03_rife.mp4", "act":0, "source_scene_id":"WLM-MS03", "storyboard":"a wall clock in a dim room, the hands almost still, the gap between truth and timing, no person", "human":false }
{ "public_path":"willingham/motion/M04_rife.mp4", "act":1, "source_scene_id":"WLM-MS04", "storyboard":"H002: a small knot of anonymous neighbors and townsfolk gathered outside the burned wood-frame house at dawn, seen from behind in silhouette, no faces, no bodies on the ground, no child", "human":true }
{ "public_path":"willingham/motion/M05_rife.mp4", "act":1, "source_scene_id":"WLM-MS05", "storyboard":"H003: anonymous fire investigators walking a burned interior shell from behind with flashlights, no faces, no bodies, no child", "human":true }
{ "public_path":"willingham/motion/M06_rife.mp4", "act":1, "source_scene_id":"WLM-MS06", "storyboard":"an abstract char pattern on a scorched floor lit ember-orange, the fire read as a language, no readable text", "human":false }
{ "public_path":"willingham/motion/M07_rife.mp4", "act":1, "source_scene_id":"WLM-MS07", "storyboard":"a dim bedroom wall of heavy-metal posters and skulls thrown to shadow, the town's projection of evil, no readable text, no face", "human":false }
{ "public_path":"willingham/motion/M08_rife.mp4", "act":1, "source_scene_id":"WLM-MS08", "storyboard":"H004: anonymous mourners at a graveside seen from behind, restrained and dignified, no coffin visible, no bodies, no child", "human":true }
{ "public_path":"willingham/motion/M09_rife.mp4", "act":1, "source_scene_id":"WLM-MS09", "storyboard":"H005: a small-town crowd of anonymous onlookers on a dusk street seen from behind, faces away, the town deciding who to hate, no faces, no child", "human":true }
{ "public_path":"willingham/motion/M10_rife.mp4", "act":2, "source_scene_id":"WLM-MS10", "storyboard":"crazed spider-web cracks spreading across a pane of glass lit ember-orange, called proof of unnatural heat, no readable text", "human":false }
{ "public_path":"willingham/motion/M11_rife.mp4", "act":2, "source_scene_id":"WLM-MS11", "storyboard":"H006: an anonymous investigator on a witness stand in cold shadow, seen from behind and side, gesturing toward an unreadable fire diagram, no face, no readable text", "human":true }
{ "public_path":"willingham/motion/M12_rife.mp4", "act":2, "source_scene_id":"WLM-MS12", "storyboard":"H007: a jury box of shadowed anonymous figures seen from behind and an empty podium, no faces, no readable text", "human":true }
{ "public_path":"willingham/motion/M13_rife.mp4", "act":2, "source_scene_id":"WLM-MS13", "storyboard":"a puddle-shaped pour pattern of char on a floor lit ember-orange, sworn to be poured accelerant, abstract, no readable text", "human":false }
{ "public_path":"willingham/motion/M14_rife.mp4", "act":2, "source_scene_id":"WLM-MS14", "storyboard":"H008: an anonymous figure behind jail bars in cold shadow and a pair of hands, an informant telling a story, no face, no readable text", "human":true }
{ "public_path":"willingham/motion/M15_rife.mp4", "act":2, "source_scene_id":"WLM-MS15", "storyboard":"H009: a courtroom gallery of anonymous figures seen from behind and a judge's silhouette at the bench, cold light, no faces, no readable text", "human":true }
{ "public_path":"willingham/motion/M16_rife.mp4", "act":3, "source_scene_id":"WLM-MS16", "storyboard":"a closed room's air going incandescent, everything about to ignite at once, flashover, abstract, no person", "human":false }
{ "public_path":"willingham/motion/M17_rife.mp4", "act":3, "source_scene_id":"WLM-MS17", "storyboard":"H010: an anonymous hand writing a letter at a desk under a warm lamp, seen over the shoulder, an outsider with nothing to gain, no face, no readable text", "human":true }
{ "public_path":"willingham/motion/M18_rife.mp4", "act":3, "source_scene_id":"WLM-MS18", "storyboard":"the same char pattern on a floor re-lit in cold forensic teal instead of ember, an ordinary fire not a poured one, no readable text", "human":false }
{ "public_path":"willingham/motion/M19_rife.mp4", "act":3, "source_scene_id":"WLM-MS19", "storyboard":"cold water hitting hot glass and crazing it, the cracks caused by the firehose not the arson, cold teal, no readable text", "human":false }
{ "public_path":"willingham/motion/M20_rife.mp4", "act":3, "source_scene_id":"WLM-MS20", "storyboard":"H011: a scientist's anonymous hands over a fire-science file and diagrams under cold light, seen over the shoulder, reading the evidence one more time, no face, files blurred unreadable", "human":true }
{ "public_path":"willingham/motion/M21_rife.mp4", "act":3, "source_scene_id":"WLM-MS21", "storyboard":"H012: an official's anonymous hands receiving a document at a desk and setting it aside under cold light, a written warning passed by, no face, pages blurred unreadable", "human":true }
{ "public_path":"willingham/motion/M22_rife.mp4", "act":3, "source_scene_id":"WLM-MS22", "storyboard":"an empty gurney with straps in a bare cold chamber, no person and no body, the room that waited, no readable text", "human":false }
{ "public_path":"willingham/motion/M23_rife.mp4", "act":3, "source_scene_id":"WLM-MS23", "storyboard":"H013: anonymous witnesses seen only from behind facing a dark viewing-room glass, and a guard's back in a cold corridor, adults only, NO body and NO execution shown, no faces, no readable text", "human":true }
{ "public_path":"willingham/motion/M24_rife.mp4", "act":4, "source_scene_id":"WLM-MS24", "storyboard":"the two dark columns of the pillars crumbling and falling in cold light, after the execution, no person, no readable text", "human":false }
{ "public_path":"willingham/motion/M25_rife.mp4", "act":4, "source_scene_id":"WLM-MS25", "storyboard":"H014: anonymous commission officials seated from behind at a long table in cold light with three chairs turned away and vacated, no faces, no readable text", "human":true }
{ "public_path":"willingham/motion/M26_rife.mp4", "act":4, "source_scene_id":"WLM-MS26", "storyboard":"H015: a lone anonymous man seen from behind at a cold fence or bare wall, the man who insisted to the end, no face, adult only, no readable text", "human":true }
{ "public_path":"willingham/motion/M27_rife.mp4", "act":4, "source_scene_id":"WLM-MS27", "storyboard":"a balance scale righting itself in cold forensic teal, the evidence re-weighed too late, no person, no readable text", "human":false }
{ "public_path":"willingham/motion/M28_rife.mp4", "act":4, "source_scene_id":"WLM-MS28", "storyboard":"a cold clear dawn over open Texas plains, no warmth, the truth that came too late, no person", "human":false }
{ "public_path":"willingham/motion/M29_rife.mp4", "act":4, "source_scene_id":"WLM-MS29", "storyboard":"an empty dark yard at cold dawn, the yard from the first minute to the last, no person, no child, no readable text", "human":false }
{ "public_path":"willingham/motion/M30_rife.mp4", "act":4, "source_scene_id":"WLM-MS30", "storyboard":"a wall clock in cold light, the hands past the moment that mattered, too late, no person, no readable text", "human":false }
```
> **Count check: 30 ✓. Human beats = 15** (M02/M04/M05/M08/M09/M11/M12/M14/M15/M17/M20/M21/M23/M25/M26) · per act HOOK 1 / ACT_1 4 / ACT_2 4 / ACT_3 4 / ACT_4 2 ✓. Abstract = 15. **All human beats anonymized, no likeness, no child, no body, no readable text.** The displaced object motifs (refrigerator, two pillars, gavel, doors, report-fan) still live in the body-still lane (§5.6).

## 4.6 `overlay[]` 20 entries (NOT counted in distinct · 12 particle / 6 light / 2 vfx) — ★ NO scanline/CRT

| type | count | use |
|---|---|---|
| `particle_assets` | **12** | ash drift · ember spark rising · dark room dust · archive dust. Black-bg drift, `screen` blend |
| `light_assets` | **6** | ember-orange glow edge · cold forensic shaft · cold clear daylight (**NO tv/scanline glow**) |
| `vfx_overlays` | **2** | fine film grain only (**NO scanline, NO CRT, NO vignette-wash**) |
| **total** | **20** | |

`public_path` = `willingham/overlay/{P##|L##|V##}_<slug>.mp4`, contains `/overlay/`, never `/factory/`. **Not in `cuts[].src`.** Per-beat sparse accents only — never a full-timeline persistent layer (§CODEX_B 5.9). **Do not select any scanline/CRT/tv-glow or full-frame vignette-wash clip** (task rule #1 bans them). Ember-orange lights are for accusation/fire beats; cold lights for science beats; do not use other-episode colors.

---

# 5. A-1: SDXL still batch (150 × 1 image · variation 0) — ★ motif-library method

## 5.1 Environment (★ use existing `generate_sdxl_4k.py`)

```
API:   http://127.0.0.1:7860 (local AUTOMATIC1111 · no cost)
Model: juggernautXL_ragnarokBy (generate_sdxl_4k.py auto set_model)
Prompts: episodes/PD-2026-051-willingham/04_scenes/ai_prompts.v001.md   ← A writes in §5.9 format
Output: H:\pd-media\assets\ai\willingham\S<NNN>.png (+ auto-copy to remotion/public/willingham/)
2-stage: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160 (long edge ≥3840 · idempotent skip)
```

**Local GPU generation is free.** Forbidden = ElevenLabs TTS / paid image APIs / uploads only (§12).

## 5.2 ★ How to write 150 = the "motif library" template method

Systematize the 150 unique prompts by act × motif. Each motif gets (a) a **locked distinct count**, (b) an **S# range**, (c) a **literal example prompt** (positive + `Avoid:[NEG]`). **Your job: using each motif's example as a base, write the assigned number of unique prompts, varying subject/angle/light/scale/object-state one image at a time** (no mass-produced identical compositions — 1 image = 1 unique prompt). **Confirm the motif totals sum to each act's locked still count (§3.2) and the grand total is 150.**

> ★ **1 scene = 1 image, variants 0.** Do not use `--variants 3`. Repetition is avoided by 150 distinct subjects. Append §5.3 `[STYLE]` in full to each positive; append §5.4 `[NEG]` in full after `Avoid:`. **All body 150 (this §5.2/§5.6 symbolic stills) are face-free / person-free / symbolic / unreadable / no victim / no child / no fire-with-people** (★ anonymized *people* appear only in the §5.11 H-series i2v seeds, never in body 150).

## 5.3 Common style `[STYLE]` (append in full to the ~110 SYMBOLIC body stills + the 15 abstract i2v seeds · byte-identical in DESIGN §2)

> **★ Scope:** `[STYLE]`/§5.4 `[NEG]` (which suppress people) apply to the **~110 object-only body stills + 15 abstract i2v seeds.** The **~40 human-present body stills (§5.11/§5.6a) and the 15 human i2v seeds (§5.11) use `[HSTYLE]`/`[HNEG]`** instead (anonymized bodies allowed).

```
, cinematic still, somber documentary grade, an ember-orange firelight as the recurring warm note of false certainty, a muted forensic cold-teal as the note of clear science, soot-black institutional gravity, a wood-frame house seen only from outside with an ember glow in the windows never any interior and never any child, abstract char patterns and crazed glass as forensic motifs, an empty gurney and a bare chamber never a body, letters and files blurred into unreadable smears, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, backs and hands and objects only, clear and high-contrast with no haze or fog or scanline
```

> **EP39–EP50 color words (include not one):** electric blue (39) / suburban demolition (40) / sodium prison gold (41) / warrant-blue·ankle monitor (42) / porch-amber·ambulance (43) / teal-green hospital (44) / warm-tungsten kitchen·crimson (45) / forest-green (46) / civil-violet·pickup (47) / EP48 glover / somber-plum·Utah night lot (49) / **cold steel-cyan #2F9FC4 (50 centralpark)**. **EP51 = ember-orange `#C25A2E` + forensic cold `#7FA8B0` (INK `#0B0A09`, type `#ECE7DF`).**

## 5.4 Common negative `[NEG]` (append in full after every `Avoid:` · A/B identical · byte-identical in DESIGN §2)

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible confession, legible autopsy, legible verdict, legible newspaper, legible case citation, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, Cameron Todd Willingham, Rick Perry, Johnny Webb, Gerald Hurst, Craig Beyler, the three daughters, children, child, baby, infant, toddler, kid, dead child, injured child, child's body, victim of a fire, burned body, corpse, human remains, blood, gore, injury, weapon, sexual content, nudity, crime scene re-enactment, actual house fire with people, firefighter faces, courtroom faces, glorified execution, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, haze, fog, mist, vignette wash, scanline, CRT texture, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan
```

> The NEG hard-suppresses **any child/baby/infant**, victim/burned-body/gore, readable documents, real-person likeness, actual-fire-with-people, other-episode colors, and haze/scanline (task rules #1/#4). This NEG suppresses `human face / portrait / identifiable face`, so it is used ONLY on the **~110 symbolic body stills + 15 abstract i2v seeds**. **All human beats (the ~40 human-present body stills + the 15 human i2v seeds · §5.11) use `[HNEG]` instead** (anonymized bodies allowed; real-likeness/child/victim/readable-text still banned).

## 5.5 Absolute prompt rules (apply to all 150)

- **Two body-still sub-lanes (owner directive · §5.11):** ~110 stills stay **symbolic objects, no people** (`[STYLE]`/`[NEG]`); **~40 stills (§5.6a) carry anonymized human presence** (a back / hands / a silhouette, `[HSTYLE]`/`[HNEG]`) where the beat has people. The 15 abstract i2v seeds keep `[STYLE]`/`[NEG]`; the 15 human i2v seeds use `[HSTYLE]`/`[HNEG]`. **Anonymized/non-identifiable people are resembling no real individual, adults only. No real-person likeness ever. The children are NEVER shown, in any lane.**
- **No readable text.** Confessions/autopsies/verdicts/newspapers/citations/IDs/dates as atmosphere only ("blurred into an unreadable smear"). Do not draw dates/ages/counts/quotes/logos.
- **No victim, no death, no fire-with-people, no interior of the burning house.** The house is exterior-only with an ember glow. No injury/blood/weapon/re-enactment. **No child/baby/infant anywhere.**
- **Frame the science and the injustice, never legal innocence.** Never draw "exonerated." "Monster" imagery (posters/tattoos) is the town's *projection*, shown to be dismantled — never the image's own claim.
- **ember `#C25A2E` = the false certainty / fire / accusation; cold `#7FA8B0` = the clear science, from Act III on.** No warm/gold exoneration payoff (the cold stays cold).
- **`treatment:"depth"` is banned** → do not describe strong foreground/background separation that a depth-map would displace; keep compositions parallax-safe (`bleed`).
- **Do NOT create or write `dochighlight` (constraint 6).**

## 5.6 ★ Motif library (per act · locked distinct counts · S# ranges · literal example prompts)

> Each motif block header = `motif — count — S# range`. The example S# lines MUST be made with that content; fill the rest of the count with variations of that motif. Expand `[STYLE]`/`[NEG]` in full per §5.3/§5.4 on every line.

### ACT 0 — HOOK + OPENING (16 · S001–S016)
- **frame_house_yard — 6 — S001–S006** (S001 also_thumb · the cold-open · the worst concrete moment, restrained)
```
- `S001.png`
A wood-frame house at night seen only from the front yard, a low ember-orange glow behind its windows, dry grass and a dark porch in the foreground, no person and no child, the house where it began, no readable text [STYLE] Avoid: [NEG]
- `S003.png`
A dark residential yard at night lit by a distant ember-orange glow from a frame house, an empty patch of grass where a man once collapsed, no person, no child, no readable text [STYLE] Avoid: [NEG]
```
- **ember_open_loop — 4 — S007–S010** (ember abstract · ash · the certainty)
```
- `S007.png`
An abstract field of ember-orange embers and falling ash against soot-black, the heat of a certainty about to take hold, no people, no readable text [STYLE] Avoid: [NEG]
```
- **name_dates_abstract — 3 — S011–S013** (title underlay · 1968–2004 · ember field, no drawn numerals)
- **clock_gap — 3 — S014–S016** (a clock · the gap between truth and timing · no numerals)
```
- `S014.png`
A plain wall clock with an unreadable blank face in a dim room, the hands almost still, the gap between the truth and the timing, no numerals, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 1 — THE MONSTER (30 · S017–S046)
- **burned_shell — 8 — S017–S024** (charred house shell · exterior/abstract · no bodies · no child)
```
- `S017.png`
The blackened shell of a burned wood-frame house at dawn seen from outside, charred studs and a collapsed roofline, cold grey smoke lifting, no people, no bodies, no child, no readable text [STYLE] Avoid: [NEG]
```
- **the_read_char — 6 — S025–S030** (floor char · "read like a language" · ember)
```
- `S025.png`
An abstract dark char pattern spread across a scorched wooden floor lit ember-orange, a fire being read like a language, irregular scorch shapes and nothing legible, no person, no readable text [STYLE] Avoid: [NEG]
```
- **monster_projection — 8 — S031–S038** (metal posters · skull/serpent tattoo abstract · satanic-panic texture · the town's projection, dismantled)
```
- `S031.png`
A dim bedroom wall of heavy-metal band posters and skull imagery thrown into deep shadow, the ornaments a frightened town read as proof of evil, symbolic and unreadable, no person, no face, no readable text [STYLE] Avoid: [NEG]
```
- **funeral_refrigerator — 4 — S039–S042** (graveside restrained · refrigerator-by-doorway silhouette · the ordinary explanation)
```
- `S039.png`
A small-town graveside seen from a respectful distance at dusk, bare ground and a low headstone in cold light, dignified and restrained, no coffin, no people, no child, no readable text [STYLE] Avoid: [NEG]
```
- **town_certainty — 4 — S043–S046** (small town at dusk · the machine of certainty building)

### ACT 2 — THE TRIAL (34 · S047–S080)
- **two_pillars — 6 — S047–S052** (S048 also_thumb · two columns: the fire and the informant)
```
- `S048.png`
Two dark stone columns standing in ember-orange light against soot-black, one column of char and one of shadow, the two pillars a death sentence rested on, symbolic, no person, no readable text [STYLE] Avoid: [NEG]
```
- **arson_indicators — 10 — S053–S062** (pour patterns · crazed glass · multiple origins · threshold burn · accelerant trace · ember, "proof")
```
- `S053.png`
A puddle-shaped pour pattern of char burned into a floor, lit hard ember-orange, sworn by investigators to be the footprint of a poured accelerant, abstract and severe, no person, no readable text [STYLE] Avoid: [NEG]
- `S055.png`
A pane of glass covered in fine crazed spider-web cracks lit ember-orange, testified to be the signature of an unnaturally hot fire, a forensic close-up with nothing legible, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_informant — 6 — S063–S068** (jailhouse informant silhouette · a deal · an unstable story · no likeness)
```
- `S063.png`
A single dark silhouette behind cold jail bars, an informant with a story to trade, seen only as a shadow with no face, a story that would not stay put, no readable text [STYLE] Avoid: [NEG]
```
- **the_plea — 4 — S069–S072** (offered life · said no · a needle refused · an unsigned page)
```
- `S069.png`
A blank statement page and a pen lying untouched under cold light, an offer of life refused rather than signed, the writing an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
```
- **psychiatrist_prophecy — 4 — S073–S076** (future-dangerousness · the sociopath verdict · a courtroom-science prophecy, abstract)
- **convicted_death — 4 — S077–S080** (a gavel · a death sentence · August 1992 · no numerals)
```
- `S077.png`
A judge's gavel resting on a bench in cold hard light, the moment a capital sentence was handed down, austere and final, no person, no numerals, no readable text [STYLE] Avoid: [NEG]
```

### ACT 3 — THE UNRAVELING (32 · S081–S112 · the reversal · visual climax)
- **flashover_reversal — 8 — S081–S088** (S081 also_thumb · flashover · the char re-lit cold)
```
- `S081.png`
A closed room whose air has gone incandescent, every surface glowing at the instant of flashover, then the same scorch pattern resolving in cold forensic teal instead of ember, an ordinary fire that got big enough, abstract, no person, no readable text [STYLE] Avoid: [NEG]
```
- **crazed_glass_reversal — 4 — S089–S092** (glass re-read cold · water on hot glass)
```
- `S089.png`
Cold water from a firehose striking hot glass and crazing it into spider-web cracks, the very act of putting the fire out making the evidence, rendered in cold forensic teal, no person, no readable text [STYLE] Avoid: [NEG]
```
- **hurst_reads — 6 — S093–S098** (a file read cold · the threshold trace explained: a porch grill / lighter fluid)
```
- `S093.png`
A small porch grill and a can of lighter fluid on a dark porch under cold light, the innocent explanation for a trace at the threshold, plain and undramatic, no person, no readable text [STYLE] Avoid: [NEG]
```
- **gilbert_letters — 4 — S099–S102** (envelopes · a stamp · an outsider with nothing to gain)
```
- `S099.png`
A small stack of handwritten envelopes and a single stamp on a plain desk under a warm lamp, letters between a playwright and a death-row prisoner, the writing an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_warning_ignored — 4 — S103–S106** (the report to the Board / a governor's desk · passed by · cold)
```
- `S103.png`
A single document lying on an official's empty desk under cold light, a written warning that arrived in time and was set aside, the pages blurred into an unreadable smear, no person, no readable text [STYLE] Avoid: [NEG]
```
- **execution_chamber — 6 — S107–S112** (the empty gurney/straps in a bare chamber · NO body · Huntsville-adjacent exterior · still insisting)
```
- `S107.png`
An empty gurney with restraint straps in a bare cold chamber, one shaft of cold light across it, no person and no body, the room that waited, austere and unbearable, no readable text [STYLE] Avoid: [NEG]
```

### ACT 4 — THE RECKONING (38 · S113–S150 · the END payoff · the cold stays cold)
- **beyler_cold_science — 8 — S113–S120** (S120 also_thumb · cold forensic clarity · "could not be sustained" · mystics-vs-science inversion)
```
- `S120.png`
A cold forensic teal light falling across an empty gurney and a closed file, the clear-eyed science that arrived after the man was gone, austere and cold with no warmth allowed, no person, no readable text [STYLE] Avoid: [NEG]
- `S113.png`
A cold laboratory bench of instruments and a single flame test in muted forensic teal, the discipline that reads a fire correctly, clear and high-contrast, no person, no readable text [STYLE] Avoid: [NEG]
```
- **commission_replaced — 6 — S121–S126** (an official body · three empty seats · a canceled meeting · 9 chairs, 3 removed · abstract)
```
- `S121.png`
An empty official conference room in cold light with nine chairs around a long table and three of them turned away and vacated, a review stopped before it could speak, symbolic, no person, no readable text [STYLE] Avoid: [NEG]
```
- **innocence_project — 4 — S127–S130** (48 pages fanning · five experts · "none valid")
```
- `S127.png`
A thick report fanned open in cold light, dozens of pages each an unreadable blur, the independent finding that none of it held, no person, no readable text [STYLE] Avoid: [NEG]
```
- **webb_recants — 4 — S131–S134** (the informant's story taken back · a charge quietly reduced · no likeness)
- **pillars_fallen — 4 — S135–S138** (both columns down · after the execution)
```
- `S135.png`
Two dark columns fallen and broken across cold ground in muted forensic teal, the fire and the informant both collapsed after the man was already dead, symbolic, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_hedge — 4 — S139–S142** (never exonerated · the case still contested · an open, cold question)
- **the_yard_return — 4 — S143–S146** (the yard again · first minute to the last · cold)
```
- `S143.png`
The same dark residential yard now at cold clear dawn with no ember and no glow, the place where a father screamed from the first minute, empty and quiet, no person, no child, no readable text [STYLE] Avoid: [NEG]
```
- **the_thesis_close — 4 — S147–S150** (a machine fed folklore · a warning that should have been enough · restraint returns)

## 5.7 Per-act motif count check (★ Codex sums after writing)

```
ACT0 : 6+4+3+3 = 16
ACT1 : 8+6+8+4+4 = 30
ACT2 : 6+10+6+4+4+4 = 34
ACT3 : 8+4+6+4+4+6 = 32
ACT4 : 8+6+4+4+4+4+4+4 = 38
TOTAL: 16+30+34+32+38 = 150 ✓
```
> Confirm S001..S150 is a gap-free run of 150 lines, and `shots=180` (150 body + 30 i2v seed) in the `--only S001` log.
> **★ Of the 150: ~110 are symbolic objects (`[STYLE]`/`[NEG]`) and ~40 carry anonymized human presence (`[HSTYLE]`/`[HNEG]`, S-numbers in §5.6a).** The count is 150 either way — the ~40 are the SAME stills written with people. Confirm the §5.6a 40-set S-numbers each use `[HSTYLE]`/`[HNEG]` and the rest use `[STYLE]`/`[NEG]`.

## 5.8 Meta JSON

`generate_sdxl_4k.py` writes no per-image meta. A records `sha256`/`phash`/`mean_luma`/`long_edge` into `still_qc.v001.json` during QC (§6.2) via `qc_willingham_stills.py`.

## 5.9 Parser contract (`read_prompts()` reads only this two-line form)

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **Line 1:** `` - `S001.png` `` (backtick-wrapped, ends right after `.png`)
- **Line 2:** positive → `Avoid:` → negative
- `ai_prompts.v001.md` holds **body 150 lines (S001..S150) + i2v seed 30 lines (M01_src..M30_src, §8.1a) = 180 entries.** All 1-image.

## 5.10 Generation command (★ no `--variants`)

```bash
# First 1 image to confirm parsed line count (★ shots=180 or the format is broken)
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 51 --only S001
#   → log "episode=... shots=180 ... -> N images"; shots must be 180 (150 body + 30 i2v seed)

# All 180 (body 150 + i2v seed 30 · idempotent · long-edge>=3840 existing skipped)
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-051-willingham
#   → S001.png ... S150.png / M01_src.png ... M30_src.png (each 1 image · no _02/_03)
```
> Regen a QC-failed scene with `--only S037` (same prompt, new seed, 1 image). **Do not lower the bar or pad with variants.**

## 5.11 ★ Human images (anonymized dramatized stand-ins) — HUMAN-FIGURE prompts (owner directive: humans allowed but anonymized so the film isn't empty)

> **Owner directive:** anonymized human figures ARE allowed (dramatized stand-ins resembling no real individual). **No likeness of any real person** (Willingham, Stacy, Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, or any real detective/judge/prosecutor/scientist). Where a real person is implied, keep the face non-identifiable (from-behind / profile-in-shadow / backlit silhouette / hatted / cropped below the eyes / soft focus). **The three daughters / victim / child-death are NEVER depicted (unbreakable). Adults only in the human lane.** The father in the yard shows coercion/grief/injustice — never guilt, never a likeness, never a child in frame.

### ★ lane definition — TWO human sub-lanes (owner directive: MORE human presence · the film must NOT read "empty/lonely, objects only")

> **Owner directive (revised):** EP48/49 leaned too hard on symbolic objects and read "empty/lonely." **Put anonymized human presence back in — in BOTH the motion lane and the still lane** — wherever the narration naturally has people (the town/onlookers, neighbors, mourners, investigators on the stand, the jury, the informant, the courtroom gallery, guards, execution witnesses, officials, experts). All from-behind / shadow / silhouette / hands, **adults only, no likeness, no child, no body, no readable text.** **Counts are NOT increased — presence is CONVERTED within the locked lanes** (fewer object-only beats, more human-present beats; totals unchanged).

**Lane 1 — MOTION human beats: H001–H015 (= 15 of the 30 i2v seeds).**
- **role = `i2v_source`** (never body). **15 of the 30 i2v seeds are human beats**; the other **15 are abstract/symbolic**. Per-act i2v seed counts (§3.2/§4.5: HOOK 3 / ACT_1 6 / ACT_2 6 / ACT_3 8 / ACT_4 7) are unchanged; the human seeds sit *inside* them as HOOK×1 · ACT_1×4 · ACT_2×4 · ACT_3×4 · ACT_4×2 = **15**.
- **asset_id occupies the i2v seed ID space (`^WLM-MS\d{2}$`)** — H001–H015 label 15 of those 30 seeds; seed files follow `M<NN>_src.png` (§8.1a; H↔M map below). **`public_path==null`** (seeds never appear as a body cut). Each is Wan-motion-ized → a motion clip → up to 2 of the 60 motion cuts.

**Lane 2 — STILL human presence: ~40 of the 150 body stills (~27%).**
- **role = `body`** (normal body still). **Of the 150 body stills, ~40 include anonymized human presence** (a back / hands / a silhouetted figure) instead of pure objects, where it strengthens the beat; the other **~110 stay symbolic objects**. **The still count is unchanged (still_body 150)** — these are the SAME 150 stills, just ~40 of them now carry a person. The 40 human-present S-numbers are listed in §5.6a.
- Human-present body stills use the **`[HSTYLE]`/`[HNEG]`** below (NOT the §5.3 `[STYLE]`/§5.4 `[NEG]`, which suppress people). Symbolic body stills keep `[STYLE]`/`[NEG]`.

**Shared for BOTH lanes:**
- **QC flags:** `has_human_body:true` (allowed) · `has_identifiable_real_person:false` (required) · `has_child_or_victim:false` (required) · `has_readable_text:false` (required). §6.1/§8.5 eyeball confirms "no real likeness / no child / no victim / no readable text / face non-identifiable / adults only."
- **★ locked counts unchanged:** still_body **150** (= ~110 symbolic + ~40 human-present) / still_i2v_source **30** (= abstract 15 + human 15) / motion **30** / factory **165** / overlay **20**; cuts **170/165/60 = 395**; still-share **0.4304**; first-use **0.8734**; `ai_prompts.v001.md` stays **180 entries** (`shots=180`). **Nothing is appended — presence is converted in place.**

**Common style `[HSTYLE]` (append in full · anonymized / non-identifiable / photoreal · adults only):**
```
, cinematic photoreal still, documentary reenactment stand-in, generic anonymized people who resemble no real individual, faces kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, hatted, cropped below the eyes, or thrown soft in shallow focus, an ember-orange firelight as the recurring warm note, a muted forensic cold-teal for the science beats, soot-black institutional gravity, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents or signage, clear and high-contrast with no haze or scanline, adults only never children
```
**Common negative `[HNEG]` (append after `Avoid:` · ★ anonymized bodies allowed; real-likeness / child / victim / readable text still banned):**
```
recognizable real person, likeness of a specific person, Cameron Todd Willingham, Stacy Willingham, Rick Perry, Johnny Webb, Manuel Vasquez, Douglas Fogg, Gerald Hurst, Craig Beyler, Elizabeth Gilbert, John Jackson, any real detective or judge or prosecutor or scientist, celebrity, mugshot, deepfake, the three daughters, children, child, baby, infant, toddler, kid, a child's body, dead or injured child, victim depiction, burned body, corpse, blood, gore, injury, weapon, sexual content, nudity, crime scene re-enactment, a menacing or guilty framing of the father, glorified execution, text, words, letters, numbers, readable document, legible confession, license plate, haze, fog, mist, scanline, CRT texture, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, cartoon, illustration, anime, 3d render, low quality, blurry, deformed, extra limbs
```

### The 15 MOTION human beats (H001–H015 · each a poised-still i2v seed · motion added by Wan · §8)
```
- `H001` (= i2v seed for M02 · HOOK)
A firelit anonymous man seen from behind in a dark yard, held back from an ember-orange glow, shoulders heaving, no face and no child in frame, a father who could not reach them, poised and still before he moves [HSTYLE] Avoid: [HNEG]
- `H002` (= i2v seed for M04 · ACT_1)
A small knot of anonymous neighbors and townsfolk gathered on the street outside a burned wood-frame house at dawn, seen from behind in silhouette, watching the ruin, no faces, no bodies on the ground, no child, poised and still [HSTYLE] Avoid: [HNEG]
- `H003` (= i2v seed for M05 · ACT_1)
Two anonymous fire investigators walking through the blackened interior shell of a burned house, seen from behind with flashlight beams, no faces, no bodies, no child, reading the ruin, poised and still [HSTYLE] Avoid: [HNEG]
- `H004` (= i2v seed for M08 · ACT_1)
A small group of anonymous mourners standing at a graveside seen from behind in cold dusk light, heads bowed, restrained and dignified, no coffin visible, no bodies, no child, poised and still [HSTYLE] Avoid: [HNEG]
- `H005` (= i2v seed for M09 · ACT_1)
A small-town crowd of anonymous onlookers on a dusk street, seen from behind with faces turned away, a community deciding whom to hate, no faces, no child, poised and still [HSTYLE] Avoid: [HNEG]
- `H006` (= i2v seed for M11 · ACT_2)
An anonymous investigator on a witness stand in cold institutional shadow, seen from behind and three-quarter, one arm raised toward an unreadable fire diagram, no face, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H007` (= i2v seed for M12 · ACT_2)
A jury box of anonymous jurors in cold light, faces shadowed and soft-focus, seen from behind toward an empty podium, non-identifiable, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H008` (= i2v seed for M14 · ACT_2)
An anonymous man behind cold jail bars seen only as a shadow, and a pair of hands gesturing a story across a table, an informant with something to gain, no face, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H009` (= i2v seed for M15 · ACT_2)
A courtroom gallery of anonymous figures seen from behind in cold light, and a judge's silhouette at the bench beyond, no faces, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H010` (= i2v seed for M17 · ACT_3)
A single anonymous hand writing a letter at a plain desk under a warm lamp, seen over the shoulder so no face reads, an outsider with nothing to gain, the writing an unreadable smear, poised and still [HSTYLE] Avoid: [HNEG]
- `H011` (= i2v seed for M20 · ACT_3)
A scientist's anonymous hands over a fire-science file and diagrams under cold forensic light, seen over the shoulder so no face reads, testing every indicator one more time, the papers blurred illegible, poised and still [HSTYLE] Avoid: [HNEG]
- `H012` (= i2v seed for M21 · ACT_3)
An official's anonymous hands receiving a document at a desk and setting it aside under cold light, seen over the shoulder so no face reads, a written warning passed by, the pages an unreadable smear, poised and still [HSTYLE] Avoid: [HNEG]
- `H013` (= i2v seed for M23 · ACT_3)
Anonymous witnesses seen only from behind facing a dark viewing-room glass, and a guard's back in a cold corridor, adults only, NO body and NO execution shown, no faces, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H014` (= i2v seed for M25 · ACT_4)
Anonymous commission officials seated from behind at a long table in cold light, three chairs turned away and vacated, no faces, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
- `H015` (= i2v seed for M26 · ACT_4)
A lone anonymous man seen from behind against a cold bare wall, adult only, still and composed, the man who insisted he was innocent to the very end, no face, no readable text, poised and still [HSTYLE] Avoid: [HNEG]
```
> **★ H↔M map (15):** H001→M02(HOOK) · H002→M04, H003→M05, H004→M08, H005→M09 (ACT_1) · H006→M11, H007→M12, H008→M14, H009→M15 (ACT_2) · H010→M17, H011→M20, H012→M21, H013→M23 (ACT_3) · H014→M25, H015→M26 (ACT_4). In `ai_prompts.v001.md`, write these as the corresponding `M<NN>_src.png` lines (do NOT add new lines — `shots=180` stays). §8.5 eyeballs "no real likeness / no child / no victim / face non-identifiable / adults only."

### The ~40 STILL human beats (anonymized presence in body stills · S-numbers · use `[HSTYLE]`/`[HNEG]`)

> These S-numbers are the SAME body stills as §5.6 (still count stays 150) — but their content includes an anonymized human presence (a back / hands / a silhouetted figure) instead of a pure object, because the beat has people. **Write these lines with `[HSTYLE]`/`[HNEG]` (not `[STYLE]`/`[NEG]`).** QC flags `has_human_body:true` / `has_identifiable_real_person:false` / `has_child_or_victim:false` / `has_readable_text:false`. All from-behind/shadow/silhouette/hands, adults only, no likeness, no child, no body, no readable text.

| act | human-present S-numbers (≈40 total) | count | what the person is |
|---|---|---|---|
| HOOK/OP | S002, S006 | 2 | the firelit father from behind in the yard (no child) |
| ACT_1 | S021, S022, S027, S035, S036, S040, S041, S044, S045, S046 | 10 | neighbors/onlookers at the shell · an investigator's back reading char · the man cast-as-monster from behind before the poster wall · mourners from behind at the graveside · townsfolk deciding whom to hate |
| ACT_2 | S060, S063, S064, S065, S070, S071, S074, S075, S079, S080 | 10 | an investigator on the stand · the informant silhouette behind bars + hands · a figure refusing the plea (hands pushing a page away) · a psychiatrist silhouette / jurors from behind · the defendant from behind at the table · the gallery from behind |
| ACT_3 | S095, S096, S097, S100, S101, S105, S110, S111, S112 | 9 | a scientist's back/hands at a lab bench and over the file (Hurst) · a hand writing letters (Gilbert) · official hands setting the report aside · guards' backs in a cold corridor · witnesses' backs at a dark viewing glass (NO body) · the man from behind, seated, still |
| ACT_4 | S113, S114, S122, S123, S128, S129, S131, S132, S145 | 9 | experts examining at a bench from behind · commission officials seated from behind (three seats vacated) · experts poring over the report · the informant taking his story back (silhouette) · a lone figure in the yard from behind at dawn |
| **total** | | **40** | ~27% of the 150 body stills |

**Example human-present still prompts (write the rest of the 40 in this form):**
```
- `S044.png`
A small-town crowd of anonymous onlookers on a dusk street seen from behind, faces turned away, a community that had already decided whom to hate, ember-orange streetlight, no faces, no readable text, no child [HSTYLE] Avoid: [HNEG]
- `S079.png`
A young man's anonymous back and shoulders seated small at a defense table beside an adult lawyer's shoulder, seen from behind so no face reads, dwarfed by a cold courtroom, no readable text, no child [HSTYLE] Avoid: [HNEG]
- `S122.png`
Anonymous officials seated from behind at a long conference table in cold light, three chairs turned away and empty, a review being taken apart, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S112.png`
A lone anonymous man seen from behind seated still in a bare cold cell, adult only, composed, the man who insisted to the end, no face, no gurney, no body, no readable text [HSTYLE] Avoid: [HNEG]
```
> **★ The remaining ~110 body stills stay symbolic objects** (`[STYLE]`/`[NEG]`, `has_human_body:false`). The §5.6 motif examples that are objects (house, char, glass, gurney, pillars, dawn) stay object-only. **also_thumb 4 (S001/S048/S081/S120) are all object beats — keep them object-only.** The daughters / any child are NEVER present, in either lane (unbreakable).

---

# 6. A-2/A-3: still QC / eyeball (★ NO depth-map step)

## 6.1 Machine QC (all 180 = body 150 + i2v seed 30 · `qc_willingham_stills.py`)

| # | check | pass | on fail |
|---|---|---|---|
| Q1 | resolution | `max(w,h)>=3840` | reject |
| Q2 | size/openable | `>1024 bytes` and PIL-openable | reject |
| Q3 | mean luma | `24.0<=mean_luma<=225.0` (near-black + ember → many dark frames; watch black-crush) | reject |
| Q4 | near-dup | all-pairs phash; `>=0.90` similar → reject one. **Variation 0, so collisions are rare. Watch: frame_house (S001/S003), char (S025/S053/S062-family), crazed glass (S055/S089), gurney (S107/S120), pillars (S048/S135), clock (S014/M03), dawn yard (S143/M29).** | reject one + revise prompt |
| Q5 | text intrusion | **eyeball.** readable letters/dates(1991/2004/2009)/ages/counts/newspaper/logo present? (R1 · constraint 2) | `has_readable_text=true`→reject |
| Q6 | real-person likeness | **eyeball.** a face resembling Willingham/Perry/Webb/Hurst/Beyler/a real detective/judge? (anonymized generic faces = OK) | `has_identifiable_real_person=true`→reject |
| Q7 | child / victim / fire-with-people | **eyeball.** ANY child/baby/infant, any victim/burned-body/gore, any interior death, any actual fire with people present? | `has_child_or_victim=true`→**reject (unbreakable)** |

**Q5/Q6/Q7 are eyeball, not machine. Eyeball all 180:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-051-willingham --media image
#   → runs/qc/willingham_footage_contact_NN.png (20/sheet · ~9 sheets). Open every sheet, look at each image.
```
> **EP38/EP39-50 lesson: don't trust filenames or prompts. Look at the output.** SDXL will happily draw readable text, real-looking faces, and — critically — **children**. **★ Expectation:** the ~40 human-present body stills (§5.6a) and the 15 human motion beats (§5.11) SHOULD contain anonymized adults — that is intended, NOT a reject. The eyeball checks **likeness (does the face resemble a REAL person → reject) and child/victim (any child/baby/body → reject)**, not mere presence. **Confirm by eye: human stills show adults only, faces non-identifiable (from-behind/shadow/soft) and resembling no real person; S001/S003 (frame house) show no child and no interior; execution beats (S107–S112, M22/M23) show NO body on the gurney and NO execution act; every image in BOTH lanes is free of any child/baby and of any real-person likeness.** Any child, any real-likeness → reject, no exceptions.

## 6.2 Output

```
episodes/PD-2026-051-willingham/05_visuals/still_qc.v001.json   # all 180 rows (rejects kept)
```

## 6.3 When accepted < (body 150 / i2v 30)

```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 51 --only S037   # failed scene, same prompt, new seed, 1 image
./.venv/Scripts/python.exe scripts/qc_willingham_stills.py
```
Repeat until accepted body >= 150 and i2v_source >= 30. **Do not lower the bar or pad.**

## 6.4 depth map — ★ SKIP (not needed)

`treatment:"depth"` is banned this film (§5.5 / CODEX_B §5.2/§5.3), so **A generates NO depth maps** and body stills carry no `depth_path`. This removes the EP50 A-3 step entirely.

---

# 7. A-4: factory real clip selection 165 + full eyeball QC

## 7.1 Inventory

```
H:\pd-media\assets\factory\   flat layout
  backgrounds/     11,000+ (.mp4)  ← ★ main (small-town Texas streets/houses/yards · charred wood & fire-aftermath
                                       textures with NO people · county courthouse/courtroom/jail exteriors & interiors ·
                                       fire-science lab / flame tests / beakers · documents & letters (unreadable) ·
                                       death-row-adjacent institutional exteriors/corridors (non-sensational) ·
                                       bare cold chambers · ash/ember/smoke abstracts · dawn Texas plains/sky · connective)
  light_assets/    …            overlay layers (ember glow · cold forensic shaft · cold daylight)
  particle_assets/ …            overlay layers (ash · ember spark · dust)
  vfx_overlays/    …            overlay layers (fine grain only — NO scanline/CRT)
  texture_assets/  …            charred wood / paper / stone textures
File-name convention: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext> (TYPECODE = BG|LIGHT|LOOP|PART|TEX|VFX)
Shelf registry: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json (open with encoding="utf-8")
```

## 7.2 Selection rules

- **`kind=="video"` only.** No still factory.
- **exactly 165.**
- **each used once** (`MAX_USES_FACTORY=1`).
- Per-act allocation (§4.4): HOOK+OP 10 / ACT_1 34 / ACT_2 30 / ACT_3 32 / ACT_4 33 + connective 26 = 165.
- **Do not pick EP39–EP50 imagery (§7.7 separation words).** EP51 = small-town Texas · charred wood / ember / ash / smoke (NO people, NO actual fire-with-people) · county courthouse/courtroom/jail · fire-science lab · documents/letters (unreadable) · death-row-adjacent institutional · bare cold chamber · dawn plains. **Do NOT pick: any clip with a child/baby, any victim/injury/burned-body/gore, any real person's identifiable face (news footage of Perry/Webb/etc.), any actual house-fire-with-people, hospital/clinical (EP44), Utah night lot (EP49), steel-cyan interrogation (EP50).**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query courthouse --limit 40 --exclude-used --ep PD-2026-051-willingham --json
```
`--exclude-used` uses the same fingerprint set as the ship gate `arc_nonrepeat`. **Always include it.**

## 7.3 Representative covered scenes (`covers_scene_id` → still ID space, pre-assigned in §4.4)

| covers (example) | content | `--query` | act |
|---|---|---|---|
| S001/S005 | frame house / small-town street night | `wood_frame_house_night` / `residential_street_night` | 0 |
| S017/S018/S043 | charred shell / char texture / Texas town | `burned_house` / `charred_wood` / `small_town_street` | 1 |
| S053/S063/S073/S077 | char floor / jail / courtroom / courthouse | `arson_char` / `county_jail` / `empty_courtroom` / `courthouse_exterior` | 2 |
| S081/S089/S093/S103/S107 | flashover / glass / lab / files / chamber | `fire_lab` / `documents` / `prison_corridor` / `bare_chamber` | 3 |
| S121/S127/S143/S147 | official building / report / dawn plains / empty chair | `government_building` / `dawn_plains` / `cold_daylight` | 4 |

Remaining are connective (`covers_scene_id:null`). **Don't over-weight dark clips** (dark ≤ ~1/3 = ~55 clips; mix in courthouse daylight, dawn plains, cold daylight).

## 7.4 Licenses (`ALLOWED_LICENSES` — pick nothing else)

```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ Use the real stock library (kill the EP48/49 burned lesson = zero real footage) ★★★

> **Owner directive (EP48/49 retro):** "せっかくたくさんダウンロードしたんだから意味のある所に使ってほしい." EP48/49 shipped AI-still + AI-i2v only and used none of the downloaded stock. EP51 kills this.

- **Stock library:** `H:\pd-media\assets\stock` (manifest `H:\pd-media\assets\stock\STOCK_MANIFEST.json` · **74 videos + 155 stills** · pexels/pixabay · **commercial-OK** = already in `ALLOWED_LICENSES`).
- **Sourcing (★ counts fixed — factory 165 unchanged; widen the source pool inside the lane):**
  1. Read `STOCK_MANIFEST.json`; **prefer stock video clips that match a §7.3 category (courthouse/small-town/night-street/jail/prison-adjacent/lab/documents/dawn) and pass §7.5 eyeball + R-FACE/R-CHILD (no face, no child, no victim, no readable text).** Target: adopt as many of the 74 stock videos as pass QC (no padding, no irrelevant inserts).
  2. Fill the rest of the 165 from `H:\pd-media\assets\factory`.
  3. Record each factory entry's origin (`stock` vs `factory`) in `05_stock/stock_ledger.v001.json` (§10.2) and `factory_selection.v001.json` (§7.6).
  4. **Do NOT mix the 155 stock stills into the body-still (AI 150) lane** (body is 1-scene-1-AI-prompt). If used at all, only face-free/text-free/child-free ones, as factory/scenery.
- **★ R-FACE/R-CHILD absolute:** any clip with a real person's identifiable face, a child/baby, or a victim/burned-body — **not used, even from stock.** Zero sha256 overlap with EP39–50 (§7.7) applies to stock too.
- **★ Color-match is B's job:** pexels/pixabay color variance is graded by B to the ember/cold system (CODEX_B §5.8(d) · **no milky wash**). A stages as-is (§10.1 libx264 conform).

## 7.5 ★★★ factory filenames and subtypes are NOT trustworthy ★★★

> **Real accidents, not hypotheticals.** EP36: `city_surveillance_camera_dome` was a cathedral. EP38: a cow tagged `documents_on_desk`. `subtype` = "the search term it came from," not a content guarantee.

**Every selected clip of the 165 goes through:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-051-willingham --media video --dir "<staging folder of the 165>"
#   → runs/qc/willingham_footage_contact_NN.png (filename label per tile · ~9 sheets)
```
2. **Open the contact sheets and look at all 165, one at a time.**
3. Write the **`eyeballed_content`** (one English sentence of what you actually saw — not a filename paraphrase) into the manifest. If it disagrees with `subtype`, set `label_matches_content:false` and **drop it** (replace).
4. Confirm real cinematic B-roll (no anime/CG smell), on-theme, no watermark, **no identifiable real person (R-FACE), no child/baby (R-CHILD), no victim/injury/gore.**
5. **★ constraints 2/3 eyeball:** avoid clips with people; where present, only from-behind/distant/face-off. **No child/baby anywhere. No victim/injury/burned-body/gore. No news footage with real faces (Perry/Webb/etc.). No actual house-fire-with-people. No hospital/clinical (EP44), Texas pickup two-lane (EP47), Utah lot (EP49), steel-cyan interrogation (EP50).**
6. Write `05_visuals/factory_clip_qc.v001.json` atomically (idempotent).

Thresholds (`check_visual_asset_qc.py`): `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`.
> **EP51 is soot-black + ember-heavy → dark side is the main risk.** Keep dark clips ≤ ~55 (1/3); mix in courthouse daylight, dawn plains, cold daylight. **A 1-frame ambiguous clip → play it in VLC/ffplay.**

## 7.6 Output

```
episodes/PD-2026-051-willingham/05_stock/factory_selection.v001.json   # selection reasons + act assignment
episodes/PD-2026-051-willingham/05_visuals/factory_clip_qc.v001.json   # reviewed manifest the gate reads
```

## 7.7 Zero overlap with EP39–EP50 (BLOCKING)

```bash
./.venv/Scripts/python.exe scripts/select_willingham_factory.py --verify-no-prior-overlap
```
Open `episodes/PD-2026-039-*/` … `PD-2026-050-*/` `05_stock/stock_ledger*.json` (and any `asset_manifest*.json`) **read-only**; confirm the `sha256` intersection with EP51's 165 is **empty**. One hit → exit 1. **Read-only; never write/move/delete EP39–50 files.**

**Separation lanes (color/subject):** EP41 gold (prison) / EP42 blue (ankle monitor) / EP43 amber (porch/ambulance) / EP44 teal (hospital) / EP45 crimson (kitchen) / EP46 green / EP47 civil-violet (Texas pickup) / EP48 glover / EP49 somber-plum (Utah night lot) / **EP50 steel-cyan (interrogation)**. **EP51 = ember-orange `#C25A2E` + forensic cold `#7FA8B0` (INK `#0B0A09`).** Pick none of the other episodes' imagery/color/subjects.

---

# 8. A-5: i2v motion 30 (Wan 2.2 A14B → RIFE 48fps)

## 8.1 The 30 i2v (moving-because-meaningful pictures · 1 seed prompt each · variation 0)

Seed images use the same `generate_sdxl_4k.py` (no variants) as `M<NN>_src.png` (add the §8.1a 30 lines to `ai_prompts.v001.md`). **Reserved as `role:"i2v_source"`, never reassigned to body** (§4.2 inv. 8). i2v_source asset_id = `WLM-MS01..MS30`; motion output = `WLM-M01..M30`. Per-act pre-assigned (§4.5): HOOK 3 / ACT_1 6 / ACT_2 6 / ACT_3 8 / ACT_4 7 = 30.
> **★ 15 of the 30 are the §5.11 anonymized human beats** (M02/M04/M05/M08/M09/M11/M12/M14/M15/M17/M20/M21/M23/M25/M26). The other 15 are abstract/symbolic. Human seeds use §5.11's `[HSTYLE]`/`[HNEG]` (poised-still); abstract seeds use §5.3 `[STYLE]` / §5.4 `[NEG]`.

### 8.1a i2v seed prompts (★ append these 30 lines to `ai_prompts.v001.md` · 1 image each · poised-still source)

> Each is the "poised, still, about to move" version of the §4.5 storyboard. The **15 human lines** (M02/M04/M05/M08/M09/M11/M12/M14/M15/M17/M20/M21/M23/M25/M26) are the §5.11 H-prompts (H001–H015) with `[HSTYLE]`/`[HNEG]`. The **15 abstract lines** end with `[STYLE]` + `Avoid:` `[NEG]`. All face-free (or anonymized), symbolic, unreadable, no child. Representative abstract examples:

```
- `M01_src.png`
A wood-frame house at night, an ember-orange glow rising in its windows seen from the yard, held motionless and poised before the light grows, no person, no child, no readable text [STYLE] Avoid: [NEG]
- `M11_src.png`
Two dark columns standing in ember-orange light, the fire and the informant held still and poised, symbolic and severe, no person, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`
A closed room's air held an instant before flashover, every surface poised to ignite at once, abstract, no person, no readable text [STYLE] Avoid: [NEG]
- `M18_src.png`
A scorch pattern on a floor held poised to resolve from ember-orange into cold forensic teal, an ordinary fire not a poured one, no person, no readable text [STYLE] Avoid: [NEG]
- `M22_src.png`
An empty gurney with restraint straps in a bare cold chamber, held still and poised under one shaft of cold light, no person and no body, no readable text [STYLE] Avoid: [NEG]
- `M28_src.png`
A cold clear dawn over open Texas plains held poised and still, no warmth, no person, no readable text [STYLE] Avoid: [NEG]
```
> **The 15 human seeds are written from §5.11 (H001–H015) as the corresponding `M<NN>_src.png` lines** (no new lines added; `shots=180`). Fill the remaining 15 abstract seeds from §4.5 storyboards in the same format, M01_src..M30_src gap-free.

## 8.2 Wan 2.2 A14B settings (★ known-good · DO NOT change · clone `comfy_wan_centralpark.py`, swap paths + SHOTS only)

```python
HOST = "http://127.0.0.1:8188"                              # local ComfyUI
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★ 2.1 (NOT 2.2 · silent quality loss otherwise)
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41        # 4090 full-load ceiling @720p
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★ SHIFT 5.0 (8.0 is a silent 5B carry-over bug)
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\willingham      # reads seed images M<NN>_src.png
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\willingham
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, text, watermark, identifiable face, real person likeness, child, baby, infant, dead child, victim, burned body, corpse, assault, gore, blood"
```

**Gates:** `dry_validate` (length=5 single POST to catch wiring cheaply) / `assert_loaded_completely` / `assert_frame_math`. Wire the `--run` path only.

## 8.3 Run (get 1 through first · ★ 30 clips is overnight)

```bash
py -3.11 scripts/comfy_wan_willingham.py --build            # graph only (no GPU)
py -3.11 scripts/comfy_wan_willingham.py --run --shot M01   # 1 real run, eyeball
py -3.11 scripts/comfy_wan_willingham.py --run-all          # remaining 29 (idempotent · skip existing)
```
~24–73 GPU-min each · 30 clips ≈ 12–36h = **overnight**. Poll `/queue` `/history` every 30s. **Run at night in splits. Check machine state before starting.**

## 8.4 RIFE to 48fps (`rife_willingham.py` · same steps as `rife_centralpark.py`)

```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / model rife-v4.6
```
1. Drop the first **5 frames** of each Wan output (length=5 validate probe · `DROP_VALIDATE=5`)
2. Rename the remaining 41 to `f0001.png`… → RIFE 2x **twice** (=4x) → **164 frames**
3. 164/48fps = **3.417s** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` → `M<NN>_rife.mp4`
4. Frame-count check `n2 >= 4*n0 - 8` else record `SHORT?` and reject

## 8.5 i2v QC

- No face/body-warping and **no child/baby, no victim, no burned-body/gore** generated (NEG suppresses but **eyeball every clip** · constraints 2/3/5)
- No morphing/flicker/warp → regen with a new seed
- Human beats (all 15: M02/M04/M05/M08/M09/M11/M12/M14/M15/M17/M20/M21/M23/M25/M26): **face stays non-identifiable** (from-behind/shadow/soft) and resembles no real person; **adult only, no child in frame**; M23 shows witnesses' backs only (NO body, NO execution)
- Abstract beats: no readable numbers/text; flashover (M16/M18) and glass (M19) read as the reversal; gurney (M22) has no body
- 3.417s each → B cuts at 3.0–3.4s (30 clips × 2 = 60 cuts)

---

# 9. A-6: overlay layers (NOT counted in distinct · exactly 20) — ★ NO scanline/CRT

See §4.6 table (12 particle / 6 light / 2 vfx). **Rules:** overlays are NOT in `check_asset_reuse` distinct → placed in `remotion/public/willingham/overlay/`, **never in `centralpark_film.json`... i.e. never in `willingham_film.json`'s `cuts[].src`.** Pick black-bg loopable clips, write `blend_hint`. Ember-orange lights = accusation/fire beats; cold lights = science beats. **Do NOT pick any scanline/CRT/tv-glow or full-frame vignette-wash clip** (task rule #1). B tints toward ember/cold; A picks no other-episode color. §7.5 eyeball QC covers all 20.

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --kind video --query ash_particles --limit 30 --exclude-used --ep PD-2026-051-willingham --json
```

---

# 10. A-7/A-8: staging and manifest output

## 10.1 Staging to Remotion public (`scripts/stage_willingham_assets.py`)

```
remotion/public/willingham/img/     ← role=body stills 150 (★ NO _depth.png — depth banned)
remotion/public/willingham/factory/ ← selected factory .mp4 165 (F001..F165 names · §4.4)
remotion/public/willingham/motion/  ← i2v M<NN>_rife.mp4 30
remotion/public/willingham/overlay/ ← overlay layers 20 (P/L/V names · §4.6)
```
- `public_path` matches manifest (§4.4/§4.5/§4.6) and real files
- factory videos conformed to **30fps** on copy (`libx264 crf 16 preset medium -an`)
- i2v left at 48fps
- skip copy if sha256 already matches (idempotent)
- **★ No depth maps** (depth treatment banned)

**★ Naming (`check_asset_reuse.kind_of()` classifies by path string):**
- factory `public_path` under `willingham/factory/` (contains `/factory`)
- i2v `public_path` ends `.mp4` and contains `_rife`
- still `public_path` is `.png`, contains neither `/factory` nor `ai_video` nor `_rife`
- overlay under `willingham/overlay/`, never in `cuts[].src`

## 10.2 Rights ledger `05_stock/stock_ledger.v001.json`

Every still/i2v/factory/overlay one row: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`.

## 10.3 Boundary-contract manifest output

```bash
./.venv/Scripts/python.exe scripts/build_willingham_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_willingham_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_willingham_asset_manifest.py --reuse-feasibility
```
Three exit-0 = "the manifest is real." **★ Confirm factory 165 / motion 30 / overlay 20 non-empty & materialized (invariants 16/17/18).** Do not edit B's files to signal anything.

---

# 11. Thumbnail concept (CTR_PLAYBOOK §4A — emotive face · A stages source art; B builds the 3 thumbnails)

> Per CTR §4A, the channel default is a single **AI-generated, NON-real, dramatized** human face at peak emotion. **This is our likeness firewall — style it clearly illustrative/semi-painterly so it never reads as a photo of the real Willingham. No real-person likeness, no child, ad-safe.** A supplies the source still concept below; B composites text + 3 variants (`WillinghamThumbnails.tsx`).

**Thumbnail source concept (a dramatized non-real face):**
```
A single dramatized, semi-painterly, NON-real man's face at peak dread and grief, firelit ember-orange on one side and cold on the other, eyes looking slightly OFF-camera (the wronged party), face occupying 55–65% of frame height pushed to the right third, a dark blurred wood-frame house with an ember glow behind him, warm skin against a cool desaturated background, cinematic documentary render, resembling no real person, no child, no readable text
```
- Second focal object (lower-left): a single struck match / an ember, OR an empty gurney strap — one saturated ember detail in an otherwise desaturated frame.
- **Text (2–4 words, red urgency bar OR yellow stroked caps, ALL CAPS heavy condensed sans, black stroke, never over the eyes):**
  - "NO ARSON. NO CRIME." · "EXECUTED FOR AN ACCIDENT" · "THE FIRE WAS A LIE"
- **Title options (front-load the shock word; 3rd-person case-film grammar per CTR §3):**
  1. **"Texas Executed Him for Arson That Never Happened"**
  2. **"They Killed Him for a Fire — Then Proved It Was an Accident"**
  3. **"A Scientist Warned Texas Before the Execution. They Killed Him Anyway."**

> The 4 `also_thumb` body stills (§4.3a: S001 frame-house, S048 pillars, S081 flashover, S120 cold-gurney) are the FALLBACK/no-face B-side (CTR §4B) if the face variant is not chosen. The face art above is generated as a dedicated thumbnail source, NOT counted in the 150 body stills (B renders it in `WillinghamThumbnails.tsx`).

---

# 12. Absolute do-nots

- **Never touch EP39–EP50 files** (read-only). Separate lanes (§7.7). EP51 accent = ember-orange `#C25A2E` + forensic cold `#7FA8B0` (INK `#0B0A09`).
- **Never touch thread-B files** (`remotion/src/**`, `scripts/ae/**`, `scripts/build_willingham_film.py`, `manifest.json`, `04_scenes/shotlist*`, `figures`). **A DOES write `04_scenes/ai_prompts.v001.md`** (§5.9/§8.1a); B only reads it.
- **Don't hunt for graphic/transition/typography stock.** Thin/empty categories are B's to build.
- **Don't launch charged jobs** (ElevenLabs TTS / paid image APIs / uploads). Local A1111/ComfyUI/RIFE = GPU only, no cost.
- **Don't overwrite/re-render shipped mp4s.**
- **★ Never create a real-person likeness anywhere** (Willingham, Stacy, Perry, Webb, Vasquez, Fogg, Hurst, Beyler, Gilbert, Jackson, any real detective/judge/prosecutor/scientist). Anonymized generic adults (H-series, resembling no one real) are OK.
- **★ Never depict the three daughters, any child, any victim/death, any actual fire-with-people, any burned body, any interior of the burning house.** Maximum restraint, unbreakable.
- **★ Never claim/imply legal innocence or "exonerated."** The reversal is about the evidence/fire-science; the case is contested; he was never legally exonerated.
- **Never draw readable text** (confession/autopsy/verdict/newspaper/date/count/logo). Atmosphere only, unreadable smear.
- **Never write `dochighlight`** anywhere (tags/caption_hint/notes/filename · grep must be 0).
- **★ Never make `_02`/`_03` variants / never `--variants 3`.** 1 scene = 1 image. (factory subtype `_02`/`_03` = distinct clips, different concept — don't confuse.)
- **★ Never leave factory 165 / motion 30 / overlay 20 empty or stub** (EP45/EP38 accident · materialize §4.4/§4.5/§4.6 · public_path non-empty).
- **★ Never add haze/fog/vignette-wash or scanline/CRT to any image or overlay** (task rule #1). Clear, high-contrast. No `depth` treatment / depth maps (task rule #2).
- **Don't decide counts "roughly."** Use §3's locked values (still 150 / factory 165 / i2v 30 / distinct 345 / first-use 0.8734 / still-share 0.4304 / overlay 20) and the §3.3 arithmetic. If it doesn't add up, suspect this doc and report — don't improvise.
- **★ Don't trust filenames/subtypes/prompts to be "fine."** EP36 passed a cathedral, EP38 a cow. **Look at the actual output / clip** — constraints 2/3/5 and the child/victim ban are eyeball-only.

---

# 13. What to include in the completion report

```
1. accepted still count & breakdown (body 150 [~110 symbolic + ~40 human-present, §5.6a] / i2v_source 30 / also_thumb 4 [§4.3a set] / reject N)
1b. ★ HUMAN-PRESENCE count: 15 of 30 motion beats (H001–H015) + ~40 of 150 body stills = ~55 human-present beats
    (all anonymized / from-behind/shadow/hands / adults only / no likeness / no child / no body). Confirm the film no
    longer reads "empty/objects only."
2. factory 165 list (asset_id / subtype / eyeballed_content), how many dropped for subtype-mismatch, and the
   "no readable text / no logo / no real face / no child / no victim / no gore / no fire-with-people" confirmation
3. EP39–EP50 (twelve) zero-overlap result
4. i2v 30 frames / duration_sec and any SHORT?
5. overlay 20 list (confirm NO scanline/CRT/vignette-wash)
6. §0.4 [A-DONE-1]..[A-DONE-5] exit codes (paste as-is) + factory 165/motion 30/overlay 20 materialized non-empty
7. §3.3 arithmetic [1]..[7] recomputed
8. asset_manifest.v001.json counts block (still_body 150 / still_i2v_source 30 / motion 30 / factory 165 / overlay 20)
9. constraint self-attestation: no real-person likeness (eyeballed) · NO child/victim/death imagery anywhere ·
   no "exonerated"/legal-innocence claim · "monster" only as dismantled framing · no readable text · no dochighlight ·
   no fabricated/readable quotes · no haze/scanline · no depth maps · variation 0 · A↔B same schema
   [schema willingham_assets.v1 / role enum body|i2v_source|reject / counts / also_thumb 4 / overlay 20]
```

**"I think it worked" is not done. The gate returns exit 0, then it's done. Rewriting a QC threshold to pass is forbidden.**

---

## 5.13 ★EMOTIVE FACES — VISIBLE faces (ADDED per owner 2026-07-25)

The generated set hid faces (turned-away/shadow/hands-only) and reads as "almost no faces." The owner wants VISIBLE, emotive human faces woven in — faces drive retention + CTR. Generate this F-series (visible faces) IN ADDITION to the existing anonymized figures.

**Two lanes, both = ANONYMIZED, NON-REAL people resembling NO real individual:**
- **(a) generic-photoreal** — faces of roles NOT tied to a specific real person (jurors, townsfolk, adult mourners, reporters, guards, a generic scientist). A visible emotive face here implies no real person → photoreal is fine.
- **(b) dramatized-illustrative** — for any beat adjacent to a central real figure (an anguished everyman): render in a clearly ILLUSTRATIVE, semi-painterly, non-photographic cinematic style so it NEVER reads as a photograph of a real person; never captioned/named as the real person.

**HARD BANS (unbreakable, same as the rest of the doc):** NO likeness of Willingham/Stacy/Perry/Webb/Vasquez/Fogg/Hurst/Beyler/Gilbert/Jackson or any real official; **NO children/babies/infants in any form (the daughters NEVER)**; NO victim/burned-body; no readable text. QC flags: `has_human_body:true`, `has_identifiable_real_person:false`, `has_identifiable_face:false` (non-real face), `has_child_or_victim:false`, `has_readable_text:false`.

**★ FACE (data-driven, per owner choice A · 2026-07-25 thumbnail research):** every F-image shows a CLEARLY-VISIBLE, instantly-readable emotive face — prominent by **LIGHT + EXPRESSION, not by raw size** (in-lane data: a huge face-filling head correlates with FLOPS/clickbait; a composed face in a dark cinematic scene correlates with winners). Face a strong **medium-close-up at ~30–45% of frame height, eyes on the upper third, front or slight three-quarter view looking near camera**, one strong unmistakable emotion, dramatic key + rim light on the face against a **DARK, moody, restrained-saturation** background. NOT a 60%+ face-filling head, NOT turned away, NOT lost in shadow, NOT hands-only. (Bans hold: no real-person likeness, no victim/burned-body, no child in any form.)

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable {EXPRESSION}, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, ember-vs-cold-forensic palette, ultra-detailed skin and eyes, high contrast, {photoreal | clearly illustrative semi-painterly non-photographic}, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Willingham, Todd, Stacy, Perry, Webb, Hurst, Beyler, Gilbert, Jackson, recognizable real person, mugshot, deepfake, child, baby, infant, toddler, victim, burned body, corpse, injury, readable text, document, caption`

Files `F001.png … F012.png` (`public_path` per your still convention). Suggested beats (act-mapped):
- **F001** (b · ACT1/OPEN) anguished illustrative everyman's face in low ember light, grief + disbelief — the human cost. NOT a likeness.
- **F002** (a · ACT2) a juror's drawn, uneasy face in courtroom shadow — the weight of a death verdict.
- **F003** (a · ACT1) two or three townsfolk faces, hard and certain — the community that decided whom to hate.
- **F004** (a · ACT1) an adult mourner's grief-worn face at a graveside, restrained — no coffin, no child.
- **F005** (a · ACT2) a jailhouse informant's shifty, calculating face in cold shadow — generic.
- **F006** (a · ACT3) a fire scientist's focused, troubled face reading a file under cold forensic light — generic, not Hurst/Beyler.
- **F007** (b · ACT2-3) an illustrative face behind glass/bars, resigned — the man insisting he tried to save them. NOT a likeness.
- **F008** (a · ACT3-4) a reporter's intent face, the story breaking.
- **F009** (b · ACT4) an illustrative face at the end, calm and unresolved — the injustice that outlived him. NOT a likeness.
- **F010** (a · ACT4) a commission official's grave face delivering a finding — generic.
- **F011** (a · ACT2) a defense figure's weary, determined face — generic.
- **F012** (a · ACT1) a first-responder/onlooker's shocked adult face by firelight — no bodies, no child.

Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/victim/text) before adding to the manifest.
