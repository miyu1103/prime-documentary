# EP51 willingham — Codex Thread B "Build + Render" handoff prompt v001

> **This file is self-contained. You can start without reading any other file.** Numbers from DESIGN_ARCHITECTURE + FACTS_LEDGER are transcribed here.
> Thread A (asset generation) is FROZEN; the only connection is §3's one manifest file.
> **★ TTS is not generated yet.** `narrationSeconds`/`durationInFrames` below are PROVISIONAL estimates from word count and **MUST be re-locked from measured "Brian" TTS before final render (measured > estimated).**

```
You are a production engineer for Prime Documentary (a YouTube documentary channel).
Repo:    C:\Users\aab15\Documents\prime-documentary
Python:  C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
Media:   H:\pd-media
Owner:   EP51 / Episode ID: PD-2026-051-willingham / slug: willingham
Composition id (film): Ep51Willingham
Format: single-human 20-min film · ~36,477 frames (PROVISIONAL · fps30) · render minutes not hours
```

**Subject:** **Cameron Todd Willingham** — a father convicted of murdering his three daughters by arson (Corsicana, Texas; fire Dec 23, 1991) and **executed Feb 17, 2004**, on fire "science" (~20 "indicators") later invalidated by flashover science. He rejected a plea, maintained innocence to the end, and **was NEVER legally exonerated.** After his death the Texas Forensic Science Commission's expert (Beyler, 2009) and the Innocence Project's 5 experts said the arson finding could not be sustained / none of the analysis was valid. **HARD FRAME: dismantle the EVIDENCE, never claim a court found him innocent. The three daughters' deaths are NEVER depicted (maximum restraint). "Monster" appears only as attributed framing, to be dismantled.**

> **★ Narration voice = ElevenLabs "Brian" (voice_id `nPczCjzI2devNBz1zQrb`). NEVER SAPI.** (§4.)
> **★ Accuracy = 7 constraints (§2 · `check_willingham_facts.py`):** R-INNOCENCE-FRAME (never "exonerated"/legal-innocence; reversals are about the evidence; Armstrong-style contrarian views only as rejected) · R-CHILD (the daughters' deaths never depicted; named once with dignity) · R-VICTIM-DIGNITY · R-LIVING (Perry/Webb/Jackson/Vasquez/Fogg/Hurst/Beyler/Gilbert only as the public record supports) · R-NUM (hedged: "roughly twenty" indicators) · R-DOCHL (`dochighlight`=0) · R-QUOTE (only the 3 verified-verbatim lines + attribution) · R-FACE (no real-person likeness; anonymized humans OK).

---

# 0. This thread's responsibility, boundary, done-conditions

## 0.1 Responsibility (B) — code-bound. You can write all of it.

| # | Task | Output |
|---|---|---|
| B-1 | episode dir + `manifest.json` | `episodes/PD-2026-051-willingham/**` |
| B-2 | manifest **consumer** validator | `scripts/check_willingham_asset_manifest.py` (clone `check_centralpark_asset_manifest.py`) |
| B-3 | fact ledger WLM-IDs + 7-constraint gate (BLOCKING) | `scripts/check_willingham_facts.py` (clone `check_centralpark_facts.py`) |
| B-4 | `willingham_film.json` builder (manifest→395 cuts + 58 figures + captions · real assets only) | `scripts/build_willingham_film.py` (clone `build_centralpark_film.py`) |
| B-5 | beats validator (AE 17 ↔ figures 58 non-overlap · year group:false · layout allowlist) | `scripts/validate_willingham_beats.py` (clone `validate_centralpark_beats.py`) |
| B-6 | AE layout allowlist gate (**6 proven only**) | `scripts/check_AE_layouts.py` (**exists from EP50** — reuse; else clone its spec §7.7) |
| B-7 | syntactic caption generator (from measured narration_index) | `scripts/gen_captions_willingham.py` (clone `gen_captions_centralpark.py`) |
| B-8 | After Effects card builder (**6 proven layouts ONLY**) + compositor | `scripts/ae/build_willingham_hero_cards.py` (**clone the CLEAN 6-layout base `build_cleveland_hero_cards.py` — NOT centralpark, see §7.1**) / `scripts/ae/composite_willingham_hero.py` (clone `composite_centralpark_hero.py`) |
| B-9 | BGM + **cold-open sound-design** mix (base mp4 · **VOICE from 0:00** · §4.5) | `scripts/build_willingham_bgm_real.py` (clone `build_centralpark_bgm_real.py`, retarget offsets per §4.5) |
| B-10 | film composition registration `Ep51Willingham` | `remotion/src/Root.tsx` |
| B-11 | OP bumper `OpeningWillingham` (fps60/1920x1080/180f) | `remotion/src/compositions/OpeningWillingham.tsx` |
| B-12 | thumbnails (3 · CTR §4A emotive-face + §4B no-face) | `remotion/src/compositions/WillinghamThumbnails.tsx` |
| B-13 | film render → BGM/SFX → AE composite → all gates → **FULL 20-min eyeball 3×** | `episodes/PD-2026-051-willingham/08_edit/**` |

> **★ Real assets only. No stub/placeholder code paths** (`grep -riE 'stub|placeholder' scripts/*willingham*.py` = 0). AE `--dryrun` single-comp renders are a legitimate verification step, not placeholders.

## 0.2 Boundary with thread A (FROZEN) — one connecting file

```
episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json
   ↑ A produces (sole producer · FROZEN)        ↓ B consumes (sole consumer/validator)
```
**B reads no A intermediate except this file.** counts / role enum / overlay count / also_thumb set are shared byte-for-byte (§3).

### 0.2.1 File ownership

| Path | Owner | B rights |
|---|---|---|
| `episodes/PD-2026-051-willingham/{manifest.json,00_topic,01_research,03_script,04_scenes,06_audio,08_edit,09_package,approvals,events}/**` | **B** | read/write |
| `remotion/src/**` `remotion/props/**` | **B** | read/write |
| `scripts/*willingham*.py` / `scripts/ae/*willingham*.py` | **B** | create new |
| `episodes/PD-2026-051-willingham/05_visuals/**` `05_stock/**` | **A** | **read-only** |
| `H:\pd-media\assets\ai\willingham\**` / `ai_video\willingham\**` | **A** | **read-only** |
| `remotion/public/willingham/{img,factory,motion,overlay}/**` | **A** | **read-only** (B builds `public_slim` in §12) |
| `EP51_willingham_*` planning docs / `script.en.v001.md` / `FACTS_LEDGER` | upstream | **read-only** (★ SPEC/Root durationInFrames updated after measured TTS = §5.1.1 — the one exception) |
| `episodes/PD-2026-0{01..50}-*/**` / `scripts/*{other slug}*.py` | other agents | **never touch (read-only). separate lanes** |

## 0.3 Scripts B creates (clone the base; change paths/constants only; don't modify the base)

| Path | Role | Clone base (confirm exists) |
|---|---|---|
| `scripts/check_willingham_asset_manifest.py` | §3.3 consumer validator | `scripts/check_centralpark_asset_manifest.py` |
| `scripts/check_willingham_facts.py` | §2 7-constraint + ledger (BLOCKING) | `scripts/check_centralpark_facts.py` |
| `scripts/build_willingham_film.py` | §5 film.json (real assets · factory/motion full-load · year group:false · **no depth** · **voice-from-0**) | `scripts/build_centralpark_film.py` |
| `scripts/validate_willingham_beats.py` | §7.6 (AE↔figures / layout allowlist / year group:false) | `scripts/validate_centralpark_beats.py` |
| `scripts/gen_captions_willingham.py` | §8 caption generator | `scripts/gen_captions_centralpark.py` |
| `scripts/ae/build_willingham_hero_cards.py` | §7 AE cards (**6 proven layouts ONLY**) | **`scripts/ae/build_cleveland_hero_cards.py`** (clean 6-layout base · §7.1) |
| `scripts/ae/composite_willingham_hero.py` | §7.9 compositor | `scripts/ae/composite_centralpark_hero.py` |
| `scripts/build_willingham_bgm_real.py` | §4.5/§7.9 base mp4 (BGM + cold-open SFX · voice-from-0) | `scripts/build_centralpark_bgm_real.py` |

> **★ AE builder cloning (CRITICAL):** clone from **`build_cleveland_hero_cards.py`** (the clean base with EXACTLY the 6 proven layouts `buildActTitle`/`buildCenter`(CENTER_STACK+MONEY_STACK)/`buildQuote`/`buildVote`/`buildCompare` and `else throw "unsupported layout"`), **NOT** from `build_centralpark_hero_cards.py` (which added 8 bespoke Tier-B layouts — EP51 uses none of them). Change `ACCENT=[0.698,0.227,0.282]` → ember `[0.761,0.353,0.180]`, add the cold note `[0.498,0.659,0.690]`, retarget paths. **Do not add any new layout. Do not implement DATE_STAMP/SEAM_TRANSITION.**
> **`build_willingham_film.py` constants:** `SLUG="willingham"`, `EP="PD-2026-051-willingham"`, `DEFAULT_OUT=remotion/src/data/willingham_film.json`, `PUB_FILM=remotion/public/willingham/film_data.v001.json`, `expected={"still":170,"factory":165,"motion":60}` (distinct still150/factory165/motion30). **Logic (`public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions`) unchanged EXCEPT the voice-from-0 offset model in §4.5/§5.1.1 and dropping the depth path (§5.2).**

## 0.4 Done-conditions (all green on real assets = done). Commands in §10/§13. Summary:
1. Consumer validator PASSES against A's FROZEN manifest (§3.3)
2. Captions generated from measured narration at syntactic boundaries; `check_caption_breaks`/`check_caption_integrity` PASS (§8)
3. film.json built from the real manifest (footage mixed · factory165/motion30 full-load · dochighlight 0 · year group:false · **no depth treatment** · **voice-from-0 hook**) (§5)
4. **All gates PASS** (§10 · script_length ~3,570-word band · animation_mix · check_year_grouping · check_AE_layouts (6 proven only) · check_willingham_facts)
5. AE 17 cards (6 proven layouts) built → two-step aerender → composite (§7)
6. Film render (`--public-dir=public_slim --concurrency=4`) → BGM + cold-open SFX → AE composite → `check_final_acceptance 51`
7. **Full 20-min 3× eyeball** (§13.1)

**Script is LOCKED** (`EP51_willingham_script.en.v001.md` · ~3,570 words). Copy byte-for-byte to `03_script/script.en.v001.md` (no reformatting — that re-triggers the AI-smell and re-computes the length gate).

---

# 0.5 ★★★ EP38–50 failures — prevented structurally ★★★

1. **Slideshow (EP45 death)** — 100% stills FAIL `check_animation_mix`; EP45 got empty `factory[]`/`motion[]`. → `build_willingham_film.py` asserts `public_items(manifest,"factory")`==165 and `public_items(manifest,"motion")`==30 at startup; 0 or wrong count → exit 1. cuts carry factory165 + motion60 from the start; still-share (cut) = **0.4304** (cap 0.45).
2. **AE cards don't count toward density** — `check_motion_density` counts `graphics+figures+heroCuts` only; AE is post-composited. → §6 places **58 `figures[]`** (`graphics[]=[]`). AE is separate.
3. **FigureSpec `kind` = lowercase real values only** — capitalized names silently vanish. **`dochighlight` is in the union but is used 0×** (R-DOCHL). `comparebars`→`compbars`, `VoteTally`→`votetally` (unused). (§6.2)
4. **Never burn a number not in the ledger** — EP40's fake $580,000. → §2 WLM-ID ledger holds only verified values; `check_willingham_facts.py` cross-checks every number in film.json/AE/thumbs/props. Hedged values FAIL if asserted.
5. **YEAR comma-grouping bug (EP46/47 "2,001")** — set `group:false` on every figure/AE numeric that shows a YEAR (1968/1991/1992/2004/2009/2011). `check_year_grouping.py` enforces (§9). (This film has no large grouped magnitudes — 48/20/5/9/3/12/2 are small integers.)
6. **Captions = script verbatim** — from measured narration_index, syntactic boundaries. (§8)
7. **phantom-layout crash (EP48/49)** — the AE JSX ends `else throw "unsupported layout"`. **`DATE_STAMP`/`SEAM_TRANSITION` are unimplemented = BANNED** (date cards = `CENTER_STACK`). **EP51 uses ONLY the 6 proven layouts and implements no new ones** (§7).
8. **(NEW, EP51) Silent runway** — the CaseFilm hook ran ~11.5s of music/SFX before Brian's voice. **EP51 leads with Brian's cold-open line from 0:00** (§4.5). Requires the CaseFilm anchor change flagged in §4.5/§5.1.1.

---

# 1. Files to read before writing (don't guess)

| Path | Why |
|---|---|
| `scripts/build_centralpark_film.py` | **Clone base.** `public_items()`/`repeated()`/`take()`/`allocate`/`build_figures`/`build_captions`. ★ Read `public_items(manifest,"factory")`(165)/`(...,"motion")`(30) (EP45 empty-array = slideshow). ★ Note where narration onset/section-offset is applied (§4.5 changes it to 0:00). ★ Note the still `depth` treatment + `depthSrcOf()` (EP51 removes it — §5.2). |
| `scripts/ae/build_cleveland_hero_cards.py` | **Clone base (clean 6-layout FIXED version).** `fit_size()`/`count_keys()`/DECK/REPO-path output/JSX-saves-.aep-then-separate-aerender/`buildActTitle`/`buildCenter`/`buildQuote`/`buildVote`/`buildCompare`/`else throw "unsupported layout"`/`render/_build_ok.txt`. **Add NOTHING; retarget only.** |
| `scripts/ae/composite_centralpark_hero.py` | **Clone base.** SKIP-4 conditions + ffmpeg overlay/blend + `film_offset_sec`. |
| `scripts/gen_captions_centralpark.py` | **Clone base.** `internal_split()`/`chunk_sentence()`/`NO_DANGLE_END`. |
| `scripts/build_centralpark_bgm_real.py` | **Clone base.** narration+BGM mix → base mp4 (**retarget to voice-from-0 + cold-open SFX** = §4.5). |
| `scripts/check_centralpark_facts.py` | **Clone base (accuracy gate).** Structural exclusions (asset_manifest out of R-NUM, geometry keys, `kind!="acttitle"`). (§2.3) |
| `scripts/check_year_grouping.py` | Existing gate. Year `group:false` logic + CLI/exit. (§9) |
| `scripts/check_AE_layouts.py` | Existing (EP50). Allowlist gate; EP51 allowlist = the 6 proven ONLY. (§7.7) |
| `remotion/src/components/CaseFilm.tsx` | `FilmData` type / `caseFilmDurationInFrames` / `depthSrcOf()`. **★ voice-from-0 hook needs a component change here** (§4.5/§5.1.1). |
| `remotion/src/components/FigureBeats.tsx` | The real lowercase `kind` values (§6.2). `numberticker` has `group?:boolean`; `mechanism` = `{closingdoor|gears|faultsplit}`; `compbars`=`items[]`; `timeline`=`events[]`; `stat`=`{value;label;...}`; `pindropmap`=`pins[]`. **`dochighlight` in union but unused.** |
| `remotion/src/components/Bookends.tsx` | `BrandOpening` / `BrandEndcard` / `OPENING_SEC` / `ENDCARD_SEC`. **★ voice-from-0 makes BrandOpening a HOOK/OP interstitial** (§4.5). |
| gate scripts (`check_asset_reuse`/`check_motion_density`/`check_animation_mix`/`check_caption_breaks`/`check_caption_integrity`/`check_script_length`/`check_visual_asset_qc`/`preflight_render_gate`/`check_final_acceptance`) | actual pass logic (§10). |
| `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx` | §11 OP canonical implementation. |

---

# 2. ★ EP51 accuracy: 7 constraints + fact-lock (`scripts/check_willingham_facts.py` · BLOCKING)

> Checks every string and number in `willingham_film.json` figures/captions, AE beats, thumbnails, props, pinned comment, `03_script/script.en.v001.md`, `09_package/*`, and (if present) manifest tags/caption_hint/qc.notes. **Accuracy gate = this one script.** Output `09_package/facts_lock.v001.json`. **`pass:true` required before `check_final_acceptance`.** Missing target files → log in `skipped[]` (don't silently pass).

## 2.1 The 7 constraints (all outputs · violation = BLOCKER)

| # | constraint | allowed | forbidden |
|---|---|---|---|
| **R-INNOCENCE-FRAME** | dismantle the EVIDENCE, never claim legal innocence | "the arson science was invalidated / could not be sustained", "no valid evidence of arson", "the fire was likely accidental", "there may have been no crime", "never legally exonerated", "the case remains contested" | **"exonerated", "proven innocent", "conviction vacated/overturned", "cleared", "a court found him innocent"** (this case has NONE of those) |
| **R-CHILD** | the three daughters' deaths NEVER depicted; named once with dignity in narration only | "his three daughters — Amber, two, and her one-year-old twin sisters — died in the fire" (narration, once, clinical) | any image/label depicting/recreating the children or their deaths; "dead/burned children", "the girls dying", "child victim" as screen copy |
| **R-VICTIM-DIGNITY** | dignity; no graphic injury | clinical fact | burned-body/gore/graphic-injury copy or imagery |
| **R-LIVING** | Perry/Webb/Vasquez/Fogg/Hurst/Beyler/Gilbert/Jackson as public record supports | Beyler wrote…, Hurst reported…, Perry publicly called him "a monster" (attributed), Webb later recanted (reported); Webb's charge was reduced after he testified (reported) | asserting crimes not in the record; "Jackson committed misconduct" as fact (bar case dismissed — "reportedly/alleged" only); defaming any living person |
| **R-NUM** | numbers = ledger-matched; hedged stays hedged | §2.2 allowed set only; "roughly twenty" indicators; "about twelve years"; years `group:false` | any out-of-ledger number; "exactly twenty indicators"; asserting a settlement/payout (there is none) |
| **R-DOCHL** | no dochighlight | intent via `kinetic`/`stat`/`highlightring`/`spotlight` | `figures[].kind`/beats/layout name containing `dochighlight` |
| **R-QUOTE** | only verified-verbatim + attribution | the 3 APPROVED_QUOTES (§2.2) + non-empty attribution; Perry "a monster" as attributed framing; Webb line only with "reportedly"/attribution | any other quoted line; a quote without attribution; the disputed profane last words (never quote) |
| **R-FACE** | anonymized humans OK; no real-person likeness | anonymized generic adults (from-behind/shadow/soft); symbolic objects; `AI-assisted visualization` bottom-right | likeness/face of Willingham/Stacy/Perry/Webb/Vasquez/Fogg/Hurst/Beyler/Gilbert/Jackson/any real person; mugshot of a real person; deepfake; **any child/victim/burned-body imagery** |

**★ Forbidden strings (`check_willingham_facts.py`, case-insensitive substring, 1 hit = FAIL):**
`exonerated` / `proven innocent` / `conviction (was )?(vacated|overturned)` / `cleared of` / `court found him innocent` (R-INNOCENCE-FRAME) — **note:** the narration does say "never been exonerated" and "never legally exonerated" in *negated* form; the gate must allow `never (been )?(legally )?exonerated` and only FAIL a *positive* claim of exoneration. Also `dead child`/`burned child`/`children's bodies`/`child victim` (R-CHILD); `exactly twenty` (R-NUM). **Do not add bare `attacked`/`confession`/`fire`/`monster` as forbidden words** — they occur in legitimate narration/attributed context (the script uses "a monster" attributed to the town/Perry, and dismantles it). Context is caught by the payload rules below.

## 2.2 Fact ledger WLM-IDs (`03_script/willingham_facts.v001.json` · schema `willingham_facts.v1` · B transcribes from `EP51_willingham_FACTS_LEDGER.v001.md`)

Each WLM-ID `{claim, value, unit, verified, confidence:"high|medium", screen_phrasing, attribution, quote}`. Only ledger-backed values `verified:true`. `confidence:medium` shows only with its hedge phrasing.

| WLM-ID | screen point | conf | on-screen handling |
|---|---|---|---|
| WLM01 | fire **December 23, 1991**, Corsicana, Texas | high | year **group:false** |
| WLM02 | three daughters died — Amber (2), twins Karmon & Kameron (1) | high · ⚠ | **named once, narration only, NO depiction (R-CHILD)**; ages 2/1 |
| WLM03 | wife Stacy not home (buying Christmas presents) | high | plain |
| WLM04 | Willingham b. **1968**, ~**23** at the fire, escaped, minor injuries | high | year group:false; age 23 |
| WLM05 | demeanor read as suspicious (too calm; the car) | high | **attributed to witnesses/investigators** |
| WLM06 | "monster" narrative: metal posters (Iron Maiden/Led Zeppelin), skull/serpent tattoos, satanic-panic | high | **attributed to the town/state, to dismantle** |
| WLM07 | Gov. Perry publicly called him **"a monster"** | high | **attributed quote** (R-QUOTE, safe) |
| WLM08 | investigators **Vasquez** (deputy state fire marshal) + **Fogg** (asst. fire chief) | high | plain |
| WLM09 | **"roughly twenty" arson "indicators"**: pour patterns, crazed glass, multiple origins, low/threshold burn, accelerant trace at the doorway | high | **soft-cite "~20" (R-NUM hedged)** |
| WLM10 | charged Jan 1992; tried **August 1992**; convicted; sentenced to death Oct 1992 | high | year group:false |
| WLM11 | jailhouse informant **Johnny Webb** claimed a confession; later **recanted**; favorable treatment / reduced charge (reported) | high (recant/charge reduced reported) | **hedged/attributed** ("later recanted", "his charge was reduced after he testified") |
| WLM12 | future-dangerousness psychiatrist (sociopath; the profession later expelled him) | medium | **"a psychiatrist… his profession later expelled him" (attributed to reporting)** |
| WLM13 | funeral-as-performance; refrigerator-by-a-doorway (ordinary explanation); Stacy initially defended him | medium | attributed / hedged |
| WLM14 | **offered life for a guilty plea — REJECTED, maintained innocence** | high | load-bearing, plain |
| WLM15 | prosecutor John Jackson (a bar case was later dismissed) | high (no misconduct asserted) | **"reporting alleged / it emerged that" only** |
| WLM16 | **Elizabeth Gilbert**, a playwright, befriended him and helped investigate | high | plain |
| WLM17 | **Gerald Hurst**, Cambridge-trained chemist; days before the execution (early **2004**) reported **no valid evidence of arson**; consistent with an accidental fire | high | plain; year group:false |
| WLM18 | **FLASHOVER**: "pour patterns" = flashover artifacts; crazed glass = water on hot glass; multiple origins/low burn consistent with flashover; threshold trace = porch grill/lighter fluid | high | the reversal (SPLIT_COMPARE) |
| WLM19 | report reached the **Board of Pardons and Paroles** + **Gov. Perry's office**; **clemency denied**; courts did not halt | high | plain |
| WLM20 | **executed by lethal injection, February 17, 2004, Huntsville Unit**; maintained innocence; age **36** | high | year group:false; age 36; **do NOT quote the disputed last words** |
| WLM21 | Texas Forensic Science Commission → **Craig Beyler**; report (**2009**): "a finding of arson could not be sustained" + "hardly consistent with a scientific mind-set and is more characteristic of mystics or psychics" | high | year group:false; **VERBATIM (QUOTE_CARD)** |
| WLM22 | Perry replaced **3 of 9** commissioners (incl. chair Sam Bassett) **two days** before a scheduled 2009 meeting; new chair canceled it; Perry denied interfering | high | 9/3/2 plain; year group:false |
| WLM23 | Innocence Project **5** fire scientists; **48**-page report: "none of the scientific analysis used to convict Mr. Willingham was valid" | high | 5/48 plain; **VERBATIM (QUOTE_CARD)** |
| WLM24 | Commission final report **2011** + addendum; did not (and by law could not) declare innocence | high | year group:false |
| WLM25 | **NEVER legally exonerated**; no court vacated the conviction; the case is contested | high · HARD | the honest hedge (CENTER_STACK) |
| WLM26 | Webb recantation motion (reported): "Mr. Willingham is innocent of all charges" | medium | **"reportedly" + attribution only** |
| WLM27 | theme/CTA: a scientist's warning should stop an execution | high | close line |

> **Allowed number set (R-NUM · narrative figure/AE/thumb/props only):** years `{1968, 1991, 1992, 2004, 2009, 2011}` (**all group:false**); ages `{1, 2, 23, 36}`; `3` (daughters); `~20` (indicators · hedged "roughly twenty"); `12` (years on death row · "about twelve"); `48` (pages); `5` (independent experts); `9` (commissioners) + `3` (replaced); `2` (days before the meeting). **No money/settlement number exists — asserting one = FAIL.** narration verbatim (script.md) is R-NUM-exempt (caption verbatim).

**VERIFIED-VERBATIM (`APPROVED_QUOTES`, the ONLY quotes allowed in quote marks):**
1. **"a finding of arson could not be sustained."** — Craig Beyler, 2009 (Texas Forensic Science Commission)
2. **"hardly consistent with a scientific mind-set and is more characteristic of mystics or psychics."** — Beyler
3. **"none of the scientific analysis used to convict Mr. Willingham was valid."** — Innocence Project (5 experts · 48 pages)
(Attributed framing allowed: Perry — "a monster." Reported: Webb — "Mr. Willingham is innocent of all charges" only with "reportedly".)

## 2.3 `check_willingham_facts.py` checks (exit 0=PASS / 1=FAIL / 2=schema)

- Keep the clone's structural exclusions (asset_manifest out of R-NUM; geometry/index keys skipped; context rules fire when `kind!="acttitle"`).
- Target files: `03_script/script.en.v001.md`, `03_script/willingham_facts.v*.json`, `08_edit/ae_hero/beats.json`, `09_package/*.json|*.txt`, `05_visuals/asset_manifest*.json` (R-NUM excluded), `remotion/src/data/willingham_film.json`, `remotion/props/willingham*.json`.
- **R-INNOCENCE-FRAME (BLOCKING):** any positive claim of exoneration/legal innocence FAILs; the negated forms (`never …exonerated`, `no court …vacated`) are ALLOWED. Any "Armstrong-style" contrarian view must be framed as rejected/contested if present.
- **R-CHILD (BLOCKING):** any figure/AE/thumb string depicting or re-creating the children/their deaths FAILs. The single dignified naming lives in the caption verbatim only.
- **R-LIVING (BLOCKING):** `Jackson` payload with an asserted crime (no "reportedly/alleged") FAILs; `Webb` recant only with hedge; `Perry` "monster" only as attributed.
- **R-NUM:** figure/AE/thumb/props numbers ∈ §2.2 set; hedged values without a hedge word FAIL; any settlement/money number FAILs.
- **R-DOCHL (BLOCKING):** `dochighlight` anywhere = FAIL.
- **R-QUOTE (BLOCKING):** quoted strings ∈ APPROVED_QUOTES + non-empty attribution; else FAIL.
- **R-FACE:** manifest items with `has_readable_text|has_identifiable_real_person|has_child_or_victim`==true must be `role=="reject"`; positive real-likeness prompt language FAILs; `AI-assisted visualization` / AI-disclosure line missing FAILs.
- **R-DATE:** never swap Dec 23 1991 (fire) / Feb 17 2004 (execution) / 2009 (Beyler) / 2011 (final report). Years all `group:false`.

**Output:** `09_package/facts_lock.v001.json` `{"pass":bool,"violations":[...],"skipped":[...]}`. **CLI:** `--json`.

---

# 3. ★ Boundary contract: `asset_manifest.v001.json` (from A · FROZEN)

## 3.1 Schema (A produces · B reads · A↔B byte-identical)
Schema `willingham_assets.v1` (else **exit 2**). counts: **still_body 150 / still_i2v_source 30 / motion 30 / factory 165 / overlay 20.** Thumbnails have no own classification — **4** body stills carry `also_thumb:true`. `role` enum (3): `body|i2v_source|reject`.
- `stills[]`: `asset_id`/`scene_id`/`role`/`also_thumb`/`act`(0..4)/`public_path`(`willingham/img/S###.png`)/`width>=3840`/`sha256`/`tags`/`caption_hint`/`qc{...}`. **★ NO `depth_path`** (depth banned — §5.2). i2v seeds `role=="i2v_source"`, `public_path==null`.
- `motion[]`: **30**. `public_path` ends `.mp4`, contains `_rife`. `build_willingham_film` full-loads via `public_items(manifest,"motion")` (0 or ≠30 → exit 1).
- `factory[]`: **165**. `public_path` contains `/factory/`. `eyeballed_content` non-empty, `qc.label_matches_content==true`. full-loaded (0 or ≠165 → exit 1).
- `overlay[]`: **20**. Not in `cuts[].src`. `public_path` contains `/overlay/`, not `/factory/`.

## 3.2 What B builds from it

| manifest | use | count |
|---|---|---|
| `stills[role="body"]` 150 | **still cuts 170** (`kind:"img"` · `treatment` cycle **`["bleed","scan","duotone","focus"]` — NO depth** · ≤2 each) | still distinct150/cuts170 |
| body `also_thumb==true` 4 | thumbnail backgrounds (§12 · 4 IDs · A↔B identical) | — |
| `stills[role="i2v_source"]` 30 | **not shown as cuts** (Wan-motion-ized by A) | — |
| `motion` 30 | **i2v cuts 60** (`kind:"footage"` · ≤2 each) | motion distinct30/cuts60 |
| `factory` 165 | **real-footage cuts 165** (`kind:"footage"` · 1 each) | factory distinct165/cuts165 |
| `overlay` 20 | **not in `cuts[].src`** (§5.5) | — |

**Total 170 + 60 + 165 = 395 cuts / distinct 150+30+165 = 345 / first-use 345/395 = 0.8734 ✓ (≥0.70) / still-share 170/395 = 0.4304 ✓ (≤0.45).**

## 3.3 `scripts/check_willingham_asset_manifest.py` (consumer validator · BLOCKING)
```bash
$PY scripts/check_willingham_asset_manifest.py --assets <path> [--json]
```
1 violation → exit 1; `schema_version` diff → exit 2. Checks: schema/episode/slug/`is_stub==false`; counts == locked (still_body150/i2v_source30/motion30/factory165/overlay20); role ∈ {body,i2v_source,reject}; `role=="body"` `public_path` exists (**no depth_path required — depth banned**); `role!="reject"` long-edge≥3840; motion path `.mp4`+`_rife`; factory path `/factory/`; overlay `/overlay/` non-`/factory/` and len==20; sha256 unique within set; factory `eyeballed_content` non-empty + `label_matches_content`; **`has_readable_text|has_identifiable_real_person|has_child_or_victim`==true ⇒ role=="reject"** (`has_human_body` is NOT a reject); `also_thumb`==4 and scene_id set == §12; no `thumb`/`still_thumb` role; **★ factory len==165 & motion len==30 non-empty** (EP45 direct guard).

---

# 4. narration_index (TTS = charged; B does NOT run it) — consume the MEASURED version

## 4.1 Why
`build_willingham_film.py` derives runtime/windows/captions from narration_index. **No seconds hard-coded in code.** The sole truth is narration_index.

## 4.2 ★ Narration voice + the charged job (B does not launch it)
**Voice = ElevenLabs "Brian" · voice_id `nPczCjzI2devNBz1zQrb`. NEVER SAPI** (SAPI = the robotic-narration defect). A separate charged step runs Brian TTS → faster-whisper → `06_audio/narration_index.v001.json` (measured word times · `is_stub:false` · `measure_vo_wpm` band 168–190). **B consumes the JSON only.** The script stays byte-identical.

## 4.3 Schema (`willingham_narration.v1`)
```jsonc
{ "schema_version":"willingham_narration.v1", "episode_id":"PD-2026-051-willingham", "is_stub":false,
  "total_seconds": 1203.4,            // ★ PROVISIONAL. FINAL = forced-align measured
  "chunks":[ {"section":"HOOK","start":0.0,"end":5.5,"text":"..."} ] }
```
**section values (6, fixed):** `HOOK` / `OP` / `ACT_1` / `ACT_2` / `ACT_3` / `ACT_4`. `section_windows()` gives act boundaries. **HOOK = the cold-open paragraph** (§4.5 — plays from 0:00).

## 4.4 ★★★ HOOK-AUDIO STANDARD — VOICE LEADS FROM 0:00 (owner directive · evidence-based) ★★★

> **Owner directive:** top-performing videos open with audio/voice from frame 0. The CaseFilm default (branded hook+opening for ~11.5s with music/SFX but Brian's VOICE starting only at 11.5s) is a **silent runway** and is wrong here. **EP51's hook must lead with Brian's most gripping cold-open line from 0:00**, over the single most intense visual, with tense dramatized sound design under it. Keep the branded opening element, but the VOICE leads.

**New EP51 hook/bookend standard (baked into the build):**

1. **VOICE from 0:00.** Brian delivers the **cold-open line from frame 0** — no silent/music-only build-up. The HOOK narration section starts at absolute **0.0s** (not 11.5s).
   - **First line (Brian, from 0:00):** *"On the day before Christmas Eve, 1991, a man ran out of a burning house in Corsicana, Texas, and collapsed in the front yard, screaming that his three little girls were still inside."* (script COLD OPEN, verbatim). It continues through the cold-open paragraph and lands on the OST beat **"THERE MAY HAVE BEEN NO CRIME."**
   - **Over the single most intense visual (from 0:00):** the anonymized **firelit father held back from the burning wood-frame house** — motion clip **M02 (H001)** + still **S001** (frame house, ember glow, from the yard). **No children in frame, no interior, no likeness** (R-CHILD/R-FACE). Drop the viewer straight into the highlight scene WITH sound.
   - **Sound design under the VO (dramatized SFX/ambience ONLY — NO real audio):** a low sub-bass pulse (~40–60 Hz, slow), distant fire-roar/crackle ambience, a muffled body-impact whump on "hold him back," a thin high room-tone rising toward the OST line; all ducked ~6 dB under Brian so the voice is always clear. **No music melody yet — tension, not score.**
2. **Branded opening element KEPT, but moved.** `BrandOpening` (the ~3.5s gold sting) plays **after the cold-open line lands** (at the HOOK→OP boundary) as a short interstitial, then narration resumes with the OPENING section ("His name was Cameron Todd Willingham…"). It no longer precedes the voice. `BRAND_OPENING_SEC = 3.5`.
3. **Real-audio constraint (HARD):** these are real cases — **no real-person audio** (no archival clips, no real 911 calls, no real courtroom audio). Use **Brian narration + dramatized SFX/ambience only** throughout.
4. **Anchor model (film clock, absolute):**
   - COLD OPEN (HOOK narration): `0.0 → hookNarrSeconds` (measured; provisional ~37s).
   - BrandOpening interstitial: `hookNarrSeconds → hookNarrSeconds + 3.5`.
   - OP + ACT_1..ACT_4 narration: resume at `hookNarrSeconds + 3.5`; i.e. every post-HOOK narration time from narration_index is shifted `+3.5s` on the film clock (the brand interstitial is the only non-narration gap).
   - Endcard: `+9s` at the end.
5. **★ CaseFilm component change REQUIRED at build time (FLAG):** the stock `CaseFilm.tsx` assumes VO onset at `hookSeconds + OPENING_SEC` (11.5s) with a pre-narration hook montage. EP51 needs: **(a)** narration/captions/BGM VO-onset anchored at **0.0s**; **(b)** the hook visual montage running SIMULTANEOUSLY with the cold-open VO (from 0:00), not before it; **(c)** `BrandOpening` rendered as a HOOK→OP interstitial at `film_offset = hookNarrSeconds`; **(d)** `durationInFrames` per §5.1.1. Implement this as a small variant/prop on `CaseFilm.tsx` (e.g. `hookVoiceLeads:true` + `brandInterstitialSec:3.5`) — **do not fork the whole component; add the branch.** Assert the new onset (0.0) at build.

## 4.5 note
The old `hookSeconds=8.0` silent block is removed. The hook is now the cold-open VO window (measured). Do not re-introduce a silent pre-roll.

---

# 5. `willingham_film.json` (clone of `build_centralpark_film.py` · real assets only)

## 5.1 `FilmData`
```ts
export type Cut = {start:number; dur:number; kind:'img'|'footage'; src:string; treatment:string; seed:string};
export type FilmData = { fps:number; narration:string; narrationSeconds:number;
  hookVoiceLeads:boolean; brandInterstitialSec:number; hookLine:string;
  cuts:Cut[]; captions:{start:number;end:number;text:string}[];
  graphics:{start:number;end:number;lines:string[]}[]; // required. EP51 = []
  figures?:FigureSpec[]; heroCuts?:{start:number;dur:number;src:string}[]; };
```
- `fps=30`. `narration="willingham/narration.mp3"`.
- **★ `hookVoiceLeads=true` · `brandInterstitialSec=3.5`** (§4.4 · VO from 0:00).
- **`hookLine` (EP51-specific · from the cold open · R-INNOCENCE-FRAME/R-CHILD safe):**
  ```
  "A father ran from a burning house screaming for his daughters. Texas killed him for it — then found there may have been no crime."
  ```
- **still `treatment` cycle = `["bleed","scan","duotone","focus"]` (NO `depth`)** — §5.2.

### 5.1.1 ★ durationInFrames (voice-from-0 · 3-term · PROVISIONAL)
```
willinghamDurationInFrames(fps=30)
  = ceil(narrationSeconds*fps)          // cold-open leads at 0 → narration spans the film · 1203.4*30 = 36,102
  + round(brandInterstitialSec*fps)     // 3.5*30 = 105 (HOOK→OP brand sting)
  + round(ENDCARD_SEC*fps)              // 9.0*30 = 270
  = 36,102 + 105 + 270 = 36,477 frames = ~20:16 (PROVISIONAL)
```
> **★ `narrationSeconds=1203.4` and `durationInFrames=36,477` are PROVISIONAL** (3,570 words / 178 wpm). **FINAL from measured "Brian" TTS forced-align.** After the VO master exists, put `narration_index.total_seconds` into `narrationSeconds`, recompute with the same function, and **update `Root.tsx` (and, if a SPEC json is later created, its runtime_plan) to the measured value** (the only write-back exception). **measured > estimated.** No `total_seconds/fps` upper-bound assert (warn if measured deviates >±3% from estimate). **The old 4-term formula (hook 8.0 + opening 3.5 + narr + endcard = 240+105+36102+270) is REPLACED** — the 240-frame silent hook is gone (§4.4).

## 5.2 ★ NO depth treatment (task rule #2 · depth melts subjects)
`treatment:"depth"` (Three.js depth-map displacement) warps/melts subjects — **BANNED** on stills and footage this film. **Cut `treatment` cycle = `["bleed","scan","duotone","focus"]`** (parallax/bleed, not depth). **Drop `depthSrcOf()` and all `_depth.png` handling** from the clone (A generates no depth maps; the manifest has no `depth_path`). Any `treatment=="depth"` in film.json = build error.

## 5.3 Cut construction (mechanical from §3 manifest · slideshow-avoidance first)
```
total 395 = factory 165 (footage) + motion 60 (footage) + still 170 (img)
[A] first-use  345/395 = 0.8734  ✓ ≥0.70
[B] per-asset  factory 165/165=1.00 ✓≤1 · motion 60/30=2.00 ✓≤2 · still 170/150=1.13 ✓≤2
[C] anim_mix   still-share(cut) 170/395 = 0.4304 ✓≤0.45 · motion-cov (165+60)/395 = 0.5696 ✓≥0.45
[D] mean shot  1203.4/395 = 3.046 s/cut ✓≤7.0 (max)
[E] factory floor 1203.4/30 = 40.1 → ≥41 · design 165 ✓
```
- allocate per `section_windows()` (factory:motion:still per act; densest ACT_3/ACT_4). factory each once; motion/still ≤2 (`repeated(pool,need,cap,key)`).
- no same asset consecutive; still `treatment` cycles `["bleed","scan","duotone","focus"]` (no 3-in-a-row same); still `dur` systematically shorter than footage; motion `dur` 3.0–3.4s.
- **AE card windows (§7.2) must have underlying cuts** (no hole if a card SKIPs).
- **★ real-footage priority & semantic mapping (§5.8).**
- **★ if manifest < still150/factory165/motion30, don't build — bounce to A** (never grow stills to shrink factory). Snap boundaries to the `QUANT` grid.

## 5.4 `figures[]` and `captions[]`
`figures[]` = §6 (**58** · floor 51 · `graphics[]=[]` · dochighlight 0 · year group:false). `captions[]` = every narration_index chunk verbatim (SRT too), **shifted by the §4.4 offset model (0:00 cold-open, +3.5 after HOOK)**.

## 5.5 overlay — not in `cuts[].src`. Held under an `overlays` key (CaseFilm ignores unknown keys) or a dedicated `screen`/`multiply` layer. **Per-beat sparse accents only — never a full-timeline persistent layer (§5.9).**

## 5.6 Builder outputs
`remotion/src/data/willingham_film.json` · `remotion/public/willingham/film_data.v001.json` · `04_scenes/willingham_build_manifest.v001.json` · `04_scenes/willingham_beatsheet.v001.json` (**NOT `premium_` — `check_motion_density`/`check_animation_mix` auto-detect `premium_beatsheet.v*.json` and would override film.json**) · `08_edit/captions.final.v001.srt`.

## 5.7 CLI
```bash
$PY scripts/build_willingham_film.py \
  --assets episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json \
  --narr   episodes/PD-2026-051-willingham/06_audio/narration_index.v001.json \
  --out    remotion/src/data/willingham_film.json
```
Real assets only. `is_stub==true` → exit 1. **`public_items(...,"factory")` 0 or ≠165, `(...,"motion")` 0 or ≠30 → exit 1.**

## 5.8 ★ Stock-first footage (kill EP48/49 = zero real footage)
Real stock (`H:\pd-media\assets\stock` · 74 videos + 155 stills · pexels/pixabay · commercial-OK) is woven by A into the `factory[]` lane (CODEX_A §7.4a). B allocates assuming stock-derived clips are in `factory[]`. **(a) semantic mapping (required):** footage cut content matches the beat — small-town/night-street/house → the fire & the town (ACT_1); courthouse/jail/courtroom → the trial (ACT_2); lab/documents/letters/prison-adjacent/chamber → the unraveling (ACT_3); official-building/report/dawn-plains/empty-chair → the reckoning (ACT_4). `allocate()` prefers footage whose `covers_scene_id`/`eyeballed_content` matches the beat category; **never force an irrelevant clip.** **(b) real > AI-i2v:** where a relevant real clip exists, use it; reserve the 30 AI-i2v for abstract/symbolic beats (flashover, char re-read cold, the two pillars, the gurney, the report) where restraint/no-depiction blocks real footage. **(c) real screen-time target:** factory 165 / (165+60) = **73.3%** of footage is real — don't fall below (don't divert factory→still). **(d) color-match:** grade footage to the ember/cold system (ember `#C25A2E` / cold `#7FA8B0` / INK `#0B0A09`) minimally + neutrally at conform or as a footage `treatment` — **no milky wash** (§5.9), no other-episode color.

## 5.9 ★ NO full-frame haze/fog/vignette-wash · NO scanline/CRT (task rule #1 · EP48/49 rejected wash)
> **Owner:** "全体的に画像に曇りがかかってる…改善して." EP48/49 shipped a milky low-contrast wash + diagonal scanline every frame and were rejected.
1. **No full-timeline wash:** no haze/fog/mist/曇り/vignette-wash layer across the film; **no full-frame scanline/CRT/diagonal-line texture** (no DriftLight-style diagonal line texture anywhere). Frame stays **clear, high-contrast.**
2. **Grade minimal + neutral:** any `BodyGrade`-style screen-wash has **opacity ≤ 0.07**; ember/cold palette unification only; no low-contrast milky veil.
3. **overlay = per-beat sparse accents** (§5.5): the 20 overlays (ash/ember/dust/light/grain) sit on specific cuts via `screen`/`multiply` — never a persistent full-timeline layer. **No scanline/CRT overlay exists in the set (A excluded them · CODEX_A §4.6/§9).**
4. **still `treatment` "scan"** stays a subtle local texture — never a full-frame scanline veil / global contrast drop.
5. **AE card internal grade** (§7.4) is per-card + minimal/neutral — never milky.
6. **composite injects no full-frame haze/blur/scanline** (§7.9).
> **Verify at §13.1 eyeball (pass 1): every frame clear & high-contrast, no wash, no scanline, no depth-warping.** DESIGN §2 governs "clear/high-contrast" — a wash violates VISUAL INTENT.

---

# 6. Remotion `figures[]` (58 · floor 51 · `graphics[]=[]` · dochighlight 0 · year group:false)

## 6.1 Density arithmetic (`check_motion_density` · AE 17 not counted)
```
body-minutes = 1203.4/60 = 20.06 · floor(2.5/min) = ceil(20.06*2.5) = 51
design 58 → 58/20.06 = 2.89/min ✓≥2.5 · coverage 58*6.0s=348 / 1203.4 = 0.289 ✓≥0.25 · variety 11 ✓≥6
dochighlight 0 · stub 0 · quote 0 · votetally 0 · no figure-less 30s window
```
Each figure dur 5.2–6.5s.

## 6.2 `FigureSpec.kind` = real lowercase values only · `dochighlight` unused
Capitalized names silently vanish. `comparebars`→`compbars`, `VoteTally`→`votetally`. **`dochighlight` in the union but used 0× (R-DOCHL). quote/votetally unused** (verbatim → AE QUOTE_CARDs; no verified vote exists).

| kind | count | payload (real union) | use |
|---|---:|---|---|
| `lowerthird` | 15 | `{primary; secondary?; accent?}` | `AI-assisted visualization`×2 · place/date/name/hedged labels (Corsicana · Dec 23 1991 · CAMERON TODD WILLINGHAM 1968–2004 · Huntsville Unit · Vasquez/Fogg · "roughly twenty indicators") |
| `kinetic` | 9 | `{lines[]; emphasisWords?}` | "READ LIKE A LANGUAGE" · "THE FIRE, THEY SAID, COULD BE READ" · "HE SAID NO" · "NO CRIME AT ALL" · "JUST NEVER IN TIME" · second-person close (emphasisWords 1–2) |
| `mechanism` | 6 | `{mechanism:'closingdoor'\|'gears'\|'faultsplit'}` | gears = the machine of certainty (town→jury→governor) · closingdoor = the dozen doors marked exit · faultsplit = the two pillars / the reading splitting from the truth |
| `compbars` | 5 | `{items:[{label; value; accent?}]}` | TWO PILLARS → both fall · ~20 INDICATORS → 0 VALID · confession claim vs the physical evidence (neutral) |
| `timeline` | 4 | `{events:[{year; text}]}` | 1991 fire → 1992 trial → 2004 execution → 2009 Beyler (returns/extends; year literals, **not "1,991"**) |
| `stat` | 6 | `{value; label; ...}` | 3 (daughters · dignity) · ~20 (indicators · hedged) · 12 (years on death row) · 36 (age) · 48 (pages) · 5 (experts) |
| `numberticker` | 3 | `{value; label?; group?}` | year tickers 1991 / 2004 / 2009 (**group:false**) |
| `arrow` | 3 | `{from?; to?; label?}` | the report → the governor's desk → past it · the "read" fire → arson |
| `highlightring` | 3 | `{cx?; cy?; r?; label?}` | the doorway accelerant trace (innocent: the porch grill) · the one warning in the record |
| `pindropmap` | 2 | `{pins:[{x; y; label?}]}` | Corsicana abstracted (**NO crime-location detail**) |
| `spotlight` | 2 | `{cx?; cy?; r?; dim?}` | single light on the empty gurney / the yard (restraint) |
| **total** | **58** | | **variety 11 · dochighlight 0 · quote 0 · votetally 0** |

> **★ Year group:false** on every `numberticker`/`stat`/`lowerthird` that shows a YEAR (1968/1991/1992/2004/2009/2011). `timeline` `events[].year` = literal strings (never "1,991"). No large grouped magnitudes exist. `check_year_grouping.py` enforces (§9).

## 6.3 Per-act placement
| act | figures | main kinds |
|---|---:|---|
| HOOK/OP | 4 | lowerthird(disclosure) · kinetic · spotlight · pindropmap |
| ACT_1 The Monster | 13 | kinetic · mechanism(gears) · stat · lowerthird · compbars · highlightring · timeline |
| ACT_2 The Trial | 13 | compbars · mechanism(faultsplit) · stat · kinetic · lowerthird · arrow · numberticker |
| ACT_3 The Unraveling | 14 | compbars(reversal) · mechanism(closingdoor) · timeline · stat · kinetic · arrow · highlightring · lowerthird · spotlight |
| ACT_4 The Reckoning | 14 | numberticker · stat · compbars · lowerthird · kinetic · timeline · mechanism · pindropmap |
| **total** | **58** | variety 11 |

## 6.4 Anchors: `(anchor_sec, payload)` ascending; `build_figures()` clamps `end=min(anchor+FIG_DUR, next-FIG_GAP, total-0.5)`; `FIG_DUR=6.0/FIG_MIN_DUR=3.0/FIG_GAP=0.4`. **Anchors relative to narration_index section windows (no hard seconds)** — and on the §4.4 film clock (VO from 0:00, +3.5 after HOOK).

## 6.5 Rules
1. **No overlap with the 17 AE moments** (§7.2) — `validate_willingham_beats` checks.
2. No same `kind` consecutive; lowerthird 15/58=25.9% (no single-kind dominance).
3. dur 5.2–6.5s.
4. All strings pass §2 (R-INNOCENCE-FRAME/R-CHILD/R-LIVING/R-NUM/R-DOCHL/R-QUOTE/R-FACE).
5. No out-of-ledger number; hedged stays hedged; **years group:false**.
6. `emphasisWords` 1–2 words; **no `dochighlight`.**

---

# 7. After Effects — 17 cards on the SIX PROVEN LAYOUTS ONLY (no bespoke Tier-B)

> AE carries the payoff (the three verbatim findings) composited on top via ffmpeg (not counted in density). **17 moments, ALL on `ACT_TITLE_CARD`/`CENTER_STACK`/`MONEY_STACK`/`QUOTE_CARD`/`VOTE_SPLIT`/`SPLIT_COMPARE`. EP51 uses ACT_TITLE_CARD×5 / CENTER_STACK×6 / SPLIT_COMPARE×3 / QUOTE_CARD×3 — no MONEY_STACK (no money in this story), no VOTE_SPLIT (no verified court/jury vote split), no DATE_STAMP/SEAM_TRANSITION (crash).**

## 7.1 Positioning + common rules
Clone **`build_cleveland_hero_cards.py`** (clean 6-layout FIXED base) — **do not clone centralpark** (it has Tier-B). Keep `buildActTitle`/`buildCenter`(CENTER_STACK+MONEY_STACK)/`buildQuote`/`buildVote`/`buildCompare`, `fit_size()`/`count_keys()`, REPO-path output, two-step render, `render/_build_ok.txt`, and **`else throw "unsupported layout"`**. **Add no builder.**

**★ AE color constants (0..1 float · ember/cold lane · NOT other-episode colors):**
```python
ACCENT = [0.761, 0.353, 0.180]  # #C25A2E ember-orange (fire / accusation / trial cards)
COLD   = [0.498, 0.659, 0.690]  # #7FA8B0 forensic cold (SCIENCE cards: both SPLIT_COMPARE right panes, Hurst, all 3 QUOTE_CARDs, the hedge)
INK    = [0.043, 0.039, 0.035]  # #0B0A09 soot-black root
BONE   = [0.925, 0.906, 0.875]  # #ECE7DF type
SILVER = [0.784, 0.804, 0.839]  # #C8CDD6 disclosure text
```
> Replace the clone's `ACCENT=[0.698,0.227,0.282]` (crimson) with ember. **No warm/gold dawn payoff — the cold stays cold** (the science arrived too late; there is no exoneration).
> **measured-fit MANDATORY:** `fit_size()` pre-fit + JSX `sourceRectAtTime(t,false).width` re-fit + quote-wrap (no advance-width estimation = EP40 clipping).
> **Every moment burns `AI-assisted visualization` bottom-right** (Oswald 20px/SILVER/op70/`[W-32,H-28]`), ≥56px above the caption band.
> **★ No moment depicts the children/deaths, a real-person likeness, or a readable fake document. No card asserts a hedged figure without its hedge. Year cards group:false.**

## 7.2 AE deck (contract · id/layout/WLM-id/anchor byte-match `validate_willingham_beats` + DESIGN §4)

> **anchors = film-clock seconds (absolute; VO leads from 0:00; +3.5s brand interstitial applied after HOOK — §4.4). DATE_STAMP/SEAM_TRANSITION not emitted. No VOTE_SPLIT, no MONEY_STACK.**

| id | layout | main copy | anchor(s) | dur | WLM | accent |
|---|---|---|---:|---:|---|---|
| t-a1 | ACT_TITLE_CARD | ACT I / THE MONSTER · CORSICANA, 1991 | 88.0 | 5.0 | WLM01 | ember |
| c-fire | CENTER_STACK | DECEMBER 23, 1991 / THREE DAUGHTERS DIED IN THE FIRE | 120.0 | 6.0 | WLM01/WLM02 | ember |
| t-a2 | ACT_TITLE_CARD | ACT II / THE TRIAL · 1992 | 296.0 | 5.0 | WLM10 | ember |
| cmp-pillars | SPLIT_COMPARE | THE CASE / "THE FIRE" ↔ "THE INFORMANT" / "TWO PILLARS" | 330.0 | 6.5 | WLM09/WLM11 | ember↔ember |
| c-indicators | CENTER_STACK | THE FIRE, THEY SAID, COULD BE READ / ROUGHLY TWENTY "INDICATORS" | 390.0 | 6.0 | WLM09 hedged | ember |
| c-plea | CENTER_STACK | OFFERED LIFE FOR A GUILTY PLEA / HE SAID NO | 470.0 | 6.0 | WLM14 | ember |
| t-a3 | ACT_TITLE_CARD | ACT III / THE UNRAVELING | 560.0 | 5.0 | — | cold |
| cmp-flashover | SPLIT_COMPARE | THE POUR PATTERNS / "PROOF OF ARSON" ↔ "PROOF OF FLASHOVER" | 645.0 | 6.5 | WLM18 | ember↔cold |
| cmp-glass | SPLIT_COMPARE | THE CRAZED GLASS / "UNNATURAL HEAT" ↔ "WATER ON HOT GLASS" | 690.0 | 6.5 | WLM18 | ember↔cold |
| c-hurst | CENTER_STACK | DAYS BEFORE THE EXECUTION / NO VALID EVIDENCE OF ARSON | 725.0 | 6.0 | WLM17 | cold |
| c-executed | CENTER_STACK | FEBRUARY 17, 2004 / EXECUTED — STILL INSISTING HE WAS INNOCENT | 800.0 | 6.0 | WLM20 | cold |
| t-a4 | ACT_TITLE_CARD | ACT IV / THE RECKONING | 830.0 | 5.0 | — | cold |
| q-beyler | QUOTE_CARD | "A FINDING OF ARSON COULD NOT BE SUSTAINED." / CRAIG BEYLER · 2009 | 900.0 | 6.5 | WLM21 high | cold |
| q-mystics | QUOTE_CARD | "…MORE CHARACTERISTIC OF MYSTICS OR PSYCHICS." / TEXAS FORENSIC SCIENCE COMMISSION | 935.0 | 6.5 | WLM21 high | cold |
| q-none | QUOTE_CARD | "NONE OF THE SCIENTIFIC ANALYSIS … WAS VALID." / INNOCENCE PROJECT · 5 EXPERTS · 48 PAGES | 1015.0 | 6.5 | WLM23 high | cold |
| c-neverexonerated | CENTER_STACK | NEVER LEGALLY EXONERATED / THE CASE REMAINS CONTESTED | 1090.0 | 6.0 | WLM25 | cold |
| t-end | ACT_TITLE_CARD | THE FIRE THAT NEVER WAS | 1175.0 | 5.0 | WLM27 | cold/bone |

> **17 cards: ACT_TITLE×5 · CENTER_STACK×6 · SPLIT_COMPARE×3 · QUOTE_CARD×3.** All 3 QUOTE_CARDs are APPROVED_QUOTES (§2.2). SPLIT_COMPARE right pane = COLD (the science); left = ember (the false reading). Anchors monotonic; **no AE↔AE and no AE↔figures overlap** (`validate_willingham_beats`). **No card names/depicts the children, the deaths, a real-person likeness; SPLIT_COMPARE panes are abstract textures (char/glass), no crime imagery.**

## 7.3 Card choreography (reuse the 6 clean builders; ember→cold on the science cards)
- **ACT_TITLE_CARD** — kicker + title mask-lift (`translateY 110%→0`, `Easing.out(cubic)`, stagger 3f), accent underline `scaleX 0→1` wipe. t-a3/t-a4/t-end use COLD.
- **CENTER_STACK** — headline + subhead mask-lift, motion-blur on the fast lift; date cards (c-fire/c-executed) here (NOT DATE_STAMP); years group:false.
- **SPLIT_COMPARE** — left pane ember ("PROOF OF ARSON"/"UNNATURAL HEAT"/"THE FIRE"), right pane COLD ("PROOF OF FLASHOVER"/"WATER ON HOT GLASS"/"THE INFORMANT"); center divider wipe; each pane's copy is a separate layer (no `\n`).
- **QUOTE_CARD** — quote wrap via measured-fit; attribution mask-lifts under it; COLD accent; the three findings are the emotional peak. Quote text = APPROVED_QUOTES byte-for-byte.
> All easing spring or `Easing.out(cubic)` (no linear); opacity always paired with translateY/scale; `motionBlur` on moving layers individually; Python precomputes display strings (JSX does no arithmetic).

## 7.4 JSX dispatch — clone's `build(spec)` unchanged; **keep `else throw "unsupported layout"`**. Common stack (bottom→top): black bg → symbolic still (optional) → grade wash (INK/MULTIPLY, **minimal/neutral, ≤0.07-equivalent, never milky** — §5.9) → feathered vignette → glow (ember; cold on science cards) → light sweep (`"ADBE Rotate Z"`=18, motionBlur) → main layers (per-layer motionBlur) → `AI-assisted visualization` → 4f head/tail black dip. **No full-frame wash added to the base — §5.9.**

## 7.5 No new layouts
EP51 implements no Tier-B. **The allowlist is exactly the 6 proven.** `check_AE_layouts` (§7.7) FAILs any other layout, including `DATE_STAMP`/`SEAM_TRANSITION`.

## 7.6 `validate_willingham_beats.py` (BLOCKING · clone `validate_centralpark_beats.py`)
1. `beats[].start` ascending, non-overlapping. 2. all start/end inside the narration span (not on the endcard). 3. `layout` ∈ the 6 proven (DATE_STAMP/SEAM_TRANSITION/VOTE_SPLIT/MONEY_STACK → FAIL for EP51). 4. `still` non-null exists + long-edge≥3840. 5. all strings pass §2. 6. `verified:false` values only on `required:false` cards. 7. **no AE↔figures(§6) time overlap.** 8. no `\n` in caption/label. 9. `AI-assisted visualization` layer present (static check). 10. no `dochighlight`/fabricated quote. 11. **id/layout/WLM-id/anchor byte-match §7.2 (and DESIGN §4).** 12. year cards group:false; AE total = 17.

## 7.7 `check_AE_layouts.py` (BLOCKING · exists from EP50)
```bash
$PY scripts/check_AE_layouts.py --ep PD-2026-051-willingham [--json]
```
**allowlist = EXACTLY** `{ACT_TITLE_CARD, CENTER_STACK, MONEY_STACK, QUOTE_CARD, VOTE_SPLIT, SPLIT_COMPARE}`. Every `beats.json` `layout` ∈ allowlist; anything else (incl. `DATE_STAMP`/`SEAM_TRANSITION`) → FAIL. **EP51 adds no Tier-B**, so no dryrun/allowlist-extension step is needed.

## 7.8 Machine traps (clone = FIXED · omit none)
Same as the EP50 clone base: spatial-ease dim (Position isSpatial=1); RS `"最良設定"` / OM localized name with try/catch; TextDocument `\n` forbidden (multi-value = separate layers; SPLIT_COMPARE left/right); measured width `sourceRectAtTime`; em-dash = `-`; `app.newProject()` hangs headless (defensively delete same-named `WILLINGHAM_` comps); `_build_ok.txt` poll ≥300s (17 short cards); JSX saves `.aep` then `app.quit()`; per-layer `motionBlur=true`; 2D rotate = `"ADBE Rotate Z"`; set both `inPoint`/`outPoint`; `conformFrameRate=30`; AfterFX path `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\AfterFX.exe`; `gpuAccelType=SOFTWARE`; strict font resolve; **build fonts in Python literal, not via PowerShell regex** (`\b` backspace bug); `sys.stdout.reconfigure(encoding="utf-8")`; **two-step: JSX writes `.aep` (`-noui -r`) → assert `.aep` mtime > `.jsx` → separate `aerender` to a REPO path on C:** (H: exFAT writes 0 mp4s).

## 7.9 Execution (two-step · 17 comps) + BGM/SFX + composite
```bash
# stage 1: build 17-card JSX + AfterFX saves .aep (no mp4 yet)
$PY scripts/ae/build_willingham_hero_cards.py
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.exe" -noui \
  -r ".../episodes/PD-2026-051-willingham/08_edit/ae_hero/willingham_hero.jsx"
# wait render/_build_ok.txt (≥300s) → assert .aep mtime > .jsx mtime
# stage 2: aerender each of 17 comps to REPO path
"C:/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project ".../08_edit/ae_hero/willingham_hero.aep" -comp "<id>" -output ".../render/<id>.mp4"
# stage 3: base mp4 (Brian narration + BGM + cold-open SFX · VOICE from 0:00 · §4.5) → AE composite
$PY scripts/build_willingham_bgm_real.py        # voice-from-0 + cold-open sound design
$PY scripts/ae/composite_willingham_hero.py
```

**Compositor (`composite_willingham_hero.py` = `composite_centralpark_hero.py` clone):**
- `BASE = 08_edit/willingham_final_bgm.v001.mp4` (from `build_willingham_bgm_real.py`) / `OUT = 08_edit/willingham_final_bgm.v002_ae.mp4` (**never overwrite v001**).
- **Keep all 4 SKIP conditions:** (1) `render/<id>.mp4` missing (2) res≠1920×1080 (3) measured dur `< dur-0.3` (4) `film_offset_sec + beat.end > base_dur`. **Print SKIP count to stderr.**
- ffmpeg `overlay=0:0:eof_action=pass:enable='between(t,start,end)'` (`blend` only if screen/multiply) / `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p -colorspace bt709 -c:a copy`. **Anchors are film-clock absolute (§4.4)** — apply the per-beat offset the clone uses; with voice-from-0 the base clock starts at the cold open (0:00), so AE anchors map directly to base time (the +3.5 brand offset is already in the section windows for post-HOOK cards).
- **★ inject NO full-frame haze/blur/scanline (§5.9).** Footage color-match (§5.8(d)) is applied upstream; composite adds no global grade.
- confirm `probe_dur(OUT)` within 0.5s of base.

**BGM + cold-open SFX (`build_willingham_bgm_real.py` = `build_centralpark_bgm_real.py` clone · voice-from-0):**
- **VOICE from 0:00** (§4.4): Brian's cold-open line starts at frame 0. **No silent runway.** Final mp4 -14.0 LUFS (-16…-12) · true peak ≤-1.0 dBTP · VO -18.0 · BGM(under VO) -22.0 / (no VO) -17.0 · ambient -30.0 · ducking 5.0 dB / attack120ms / release450ms.
- **Cold-open sound design (0:00–~10s, dramatized ONLY, no real audio):** low sub pulse (~40–60 Hz), distant fire-roar/crackle ambience, a muffled impact whump on "hold him back," a rising thin room-tone into the OST line — all ducked ~6 dB under Brian. **Tension, not melody.**
- **Real-audio constraint (HARD):** no real-person/archival audio anywhere — Brian narration + dramatized SFX/ambience only.
- Chapter BGM: 1 track/act (ember-tension in ACT_1/2; a cold clarifying shift at the flashover reversal in ACT_3; a bare, unresolved cold at the execution and through ACT_4 — **the cold never warms**, no triumphant resolution). Longest silence <25s (`bgm_present`); no digital-silence gaps. **Do not place a caption cue in an intentional breath.**

---

# 8. Captions (`gen_captions_willingham.py` = `gen_captions_centralpark.py` clone)
- Copy `internal_split()`/`chunk_sentence()`/`from fix_caption_dangling import NO_DANGLE_END, wrap as safe_wrap` unchanged.
- Input = narration_index chunks (`--narr`). Caption text = script verbatim, split at syntactic boundaries. **Timing from narration_index start/end, shifted by the §4.4 model (cold open at 0:00; +3.5 after HOOK).**
- `ABBR` includes `U.S.`/`Mr.`/`Mrs.`/`Dr.`/`No.`/`Dec.`/`Feb.` so `Dec. 23, 1991`/`Feb. 17, 2004` don't break a sentence.
- Pass `check_caption_breaks.py` (A end-function-word 0 / B orphan 0 / C hard-split 0 — **don't loosen thresholds**) + `check_caption_integrity`.
- **R-FORBID applies to captions** (script verbatim passes — §2.1 note: don't add bare `attacked`/`confession`/`monster`/`fire`).
```bash
$PY scripts/gen_captions_willingham.py --narr episodes/PD-2026-051-willingham/06_audio/narration_index.v001.json
$PY scripts/check_caption_breaks.py episodes/PD-2026-051-willingham/08_edit/captions.final.v001.srt
```

---

# 9. ★ Year group:false gate (`scripts/check_year_grouping.py` · exists · BLOCKING)
```bash
$PY scripts/check_year_grouping.py --ep PD-2026-051-willingham [--json]
```
- Every `numberticker`/`stat`/`lowerthird` and AE numeric showing a YEAR (1968/1991/1992/2004/2009/2011) must carry `group:false` — else FAIL (the "1,991"/"2,004" bug · EP46/47). `timeline` `events[].year` are literal strings (never "1,991").
- **This film has no large grouped magnitudes** (48/20/12/9/5/3/2 are small integers rendered plainly). Do not `group:false` those (harmless) — the gate only enforces years.
- Scans figures[] and beats.json.

---

# 10. All gates (after build · before render preflight · before "done")
```bash
cd C:\Users\aab15\Documents\prime-documentary ; PY=./.venv/Scripts/python.exe

# --- Preflight (before spend/render) ---
$PY scripts/check_script_length.py episodes/PD-2026-051-willingham/03_script/script.en.v001.md --cap 3700 --json
#    → ~3,570 words within the 20-min band (the 12-min 2,141 cap does NOT apply — pass --cap 3700)
$PY scripts/check_willingham_facts.py --json
$PY scripts/validate_willingham_beats.py
$PY scripts/check_willingham_asset_manifest.py --assets episodes/PD-2026-051-willingham/05_visuals/asset_manifest.v001.json
$PY scripts/check_AE_layouts.py --ep PD-2026-051-willingham
$PY scripts/check_year_grouping.py --ep PD-2026-051-willingham

# --- Post-build (before final) ---
$PY scripts/check_asset_reuse.py     remotion/src/data/willingham_film.json   # factory≤1/motion≤2/still≤2 · first-use≥0.70 (design 0.8734)
$PY scripts/check_motion_density.py  --ep PD-2026-051-willingham              # ≥51 beats/≥2.5min/variety≥6/dochighlight=0 (design 58/2.89/11)
$PY scripts/check_animation_mix.py   --ep PD-2026-051-willingham              # still-share≤0.45 (design 0.4304)/motion-cov≥0.45 (0.5696)
$PY scripts/check_caption_breaks.py  episodes/PD-2026-051-willingham/08_edit/captions.final.v001.srt
$PY scripts/check_caption_integrity.py --ep PD-2026-051-willingham            # narration match ≥99%/coverage≥95%/CPS≤17/drift≤120ms
$PY scripts/check_visual_asset_qc.py --ep PD-2026-051-willingham              # all still/factory/motion eyeball QC · black-frame 0 · R-FACE/R-CHILD
$PY scripts/preflight_render_gate.py --ep PD-2026-051-willingham              # machine state · public_slim disk · durationInFrames assert · VO onset 0.0

# --- Render → BGM/SFX → AE composite (§12) → final acceptance ---
$PY scripts/check_final_acceptance.py 51 \
  --render episodes/PD-2026-051-willingham/08_edit/willingham_final_bgm.v002_ae.mp4 --emit-receipt
```
> **Gate input convention:** density/mix/year/AE_layouts/caption_integrity/visual_qc/preflight take `--ep PD-2026-051-willingham`; asset_reuse takes the film.json positional; caption_breaks the srt positional; script_length the script positional. **beatsheet must NOT be `premium_` (§5.6).** All exit 0 before `package_ready`.

| gate | EP51 target |
|---|---|
| `check_script_length` | ~3,570 words ∈ 20-min band (not the 2,141 cap) |
| `check_willingham_facts` | violations 0 (7 constraints · no "exonerated" · no child depiction · hedged intact) |
| `check_asset_reuse` | factory≤1/motion≤2/still≤2 · first-use **0.8734** |
| `check_motion_density` | **58** beats / **2.89**/min / variety **11** (floor 51/2.5/6 · dochighlight 0) |
| `check_animation_mix` | still-share **0.4304** (cap 0.45) / motion-cov **0.5696** (floor 0.45) |
| `check_AE_layouts` | all ∈ 6 proven · DATE_STAMP/SEAM_TRANSITION/VOTE_SPLIT/MONEY_STACK 0 |
| `check_year_grouping` | years group:false ("1,991" 0) |
| `validate_willingham_beats` | AE 17 ↔ figures 58 non-overlap · id/layout/WLM/anchor match |
| captions | end-func-word 0/orphan 0/hard 0 · match ≥99% · CPS≤17 |
| runtime | ~20:16 (PROVISIONAL 36,477f · **FINAL from measured Brian TTS**) |

---

# 11. OP bumper `OpeningWillingham` (independent · fps60/1920x1080/180f)
The film's own OP is `Bookends.tsx` `BrandOpening` (now a HOOK→OP interstitial · §4.4 · no fork). `OpeningWillingham` is a standalone title bumper (`out/willingham_opening.mp4`, for Shorts/trailer, not burned into the film).
- Composition `id="OpeningWillingham"` / 1920×1080 / fps60 / 180f (3.0s) / `remotion/src/compositions/OpeningWillingham.tsx`.
- Dependency `@remotion/motion-blur` (`cd remotion && npm i @remotion/motion-blur` if missing). `remotion.config.ts` = canonical (png/h264 libx264/CRF16/yuv420p/bt709/aac320k/all-core/angle) — confirm, don't edit.
- Second-based (fps60 · no hard frame counts · all `Math.round(fps*sec)`) · zero linear easing · no opacity-alone (pair translateY/scale) · 2–4f stagger · fast moves `Trail` motion-blur · text `overflow:hidden`+translateY mask-lift · ≥3 layers behind the title (gradient/grid/glow).
- props `{ title; subtitle; accent; hasLogo }`. `remotion/props/willingham.json` = `{ "title":"THE FIRE THAT NEVER WAS", "subtitle":"THEY EXECUTED HIM FOR ARSON. THERE WAS NO ARSON.", "accent":"#C25A2E", "hasLogo":true }`.
- **accent must be `#C25A2E`** (other-episode color = BLOCKER); root bg INK `#0B0A09`. title/subtitle are §2-checked (R-INNOCENCE-FRAME: "no arson" is about the evidence, allowed; no "exonerated").
```bash
cd remotion && npm run studio      # scrub OpeningWillingham 0→180f
npx remotion render OpeningWillingham out/willingham_opening.mp4 --props=./props/willingham.json
```

---

# 12. staging & render
```bash
# public/willingham → public_slim/willingham (img/factory/motion/overlay/audio · ★ NO _depth.png — none exist)
$PY scripts/stage_centralpark_assets.py --ep PD-2026-051-willingham 2>/dev/null || {
    mkdir -p remotion/public_slim/willingham
    cp -r remotion/public/willingham/{img,factory,motion,overlay,audio} remotion/public_slim/willingham/ 2>/dev/null
    cp remotion/public/willingham/narration.mp3 remotion/public_slim/willingham/ 2>/dev/null
}
#   ★ confirm every src willingham_film.json references exists in public_slim (0-missing). No depth maps to check.
#   ★ prune public_slim to EP51 only (avoid C: ENOSPC). Check machine state first.
cd remotion
npx remotion render Ep51Willingham out/willingham.mp4 --public-dir=public_slim --concurrency=4
cd ..
```
Root.tsx registration:
```tsx
import willinghamFilm from './data/willingham_film.json';
<Composition id="Ep51Willingham" component={CaseFilm}
  durationInFrames={willinghamDurationInFrames(willinghamFilm as unknown as FilmData, BRAND.video.fps)}
  fps={BRAND.video.fps} width={BRAND.video.width} height={BRAND.video.height}
  defaultProps={{ data: willinghamFilm as unknown as FilmData, seriesLabel: 'PRIME DOCUMENTARY',
    title: 'The Fire That Never Was', subtitle: '...' }}/>
```
> id exactly `Ep51Willingham`. **Assert `hookVoiceLeads==true` and VO onset 0.0** (§4.4). durationInFrames recomputed by the 3-term function → **36,477 (provisional)**, re-locked from measured TTS. `cd remotion && npx tsc --noEmit` green. Confirm no existing `willingham` string collision before adding.

---

# 13. Acceptance (confirm exit 0 yourself before reporting done)
Run every §10 gate to exit 0, then `check_final_acceptance.py 51 --render .../willingham_final_bgm.v002_ae.mp4 --emit-receipt` PASS.

## 13.1 ★ FULL 20-min 3× eyeball (no 1-frame judgment = EP39-41/EP47 harm)
Watch `willingham_final_bgm.v002_ae.mp4` **0→end, 3 passes** (measured across the WHOLE ~20 min, not 1 frame):
- **Pass 1 structure/cuts:** no slideshow (no still runs; footage majority = EP45 death avoided); 4-act structure; **★ the HOOK leads with Brian's VOICE from 0:00 over the father-in-the-yard visual with tense SFX — NO silent runway (§4.4)**; all 17 AE cards burned in; **real stock at meaningful beats (§5.8) & real ≥73%**; footage + AI still read as one ember/cold palette; **★ anonymized human presence is VISIBLE throughout (15 motion beats + ~40 human-present stills = the town/jury/investigators/mourners/officials/witnesses, from-behind/shadow/hands) — the film must NOT read "empty/lonely, objects only" (owner directive), while showing NO real-person likeness, NO child, NO body**; **★ every frame clear & high-contrast — no full-frame haze/fog/scanline, no depth-warping (§5.9/§5.2).**
- **Pass 2 caption-text:** every caption matches the script; no end-function-word/orphan/hard split; **years not comma-grouped (1991/2004/2009 — inspect every numberticker/stat/year card, EP47 "2,001" guard).**
- **Pass 3 audio-sync:** **VO onset = 0:00 exactly** (cold-open line from frame 0); brand interstitial ~3.5s after the HOOK; endcard 9s; **dramatized SFX/ambience only, NO real-person audio**; BGM ducking; no drift (base ≤0.5s).
- **Every pass, confirm:**
  - each AE card once: cmp-flashover / cmp-glass ember→cold reversal · the 3 QUOTE_CARDs verbatim + attribution · c-neverexonerated present · no MONEY_STACK/VOTE_SPLIT/DATE_STAMP.
  - **R-INNOCENCE-FRAME:** nothing on screen/caption claims a court found him innocent or says "exonerated" (except the negated "never exonerated"); the reversal is about the evidence.
  - **R-CHILD (unbreakable):** the three daughters / any child / any death imagery appear **nowhere**; named once with dignity in the caption only.
  - **R-VICTIM/R-LIVING/R-REYES-equivalent:** no graphic injury; living people only as the record supports; "monster" only as attributed & dismantled.
  - **R-FACE:** anonymized humans OK, but **no face/likeness resembling Willingham/Perry/Webb/Hurst/Beyler/a real official**; no readable fake document.
  - **R-DOCHL:** no dochighlight (black bar/box/underline) anywhere.
  - **R-QUOTE:** quote marks only around the 3 verified lines + attribution.
  - `AI-assisted visualization` bottom-right whenever a generated visual/AE card shows (incl. the 17 cards).
  - accent = ember `#C25A2E` + forensic cold `#7FA8B0` (no other-episode color); the cold never warms into a triumphant/gold payoff (there was no exoneration).

---

# 14. Absolute do-nots
- **Never touch EP1–50 files/assets/`scripts/*{other slug}*.py`** (read-only). Separate lanes. accent = ember `#C25A2E` + forensic cold `#7FA8B0` only.
- **Never write A's owned files** (`05_visuals/`, `05_stock/`, `remotion/public/willingham/`, `H:\...\ai\willingham\`). B provenance → `04_scenes/`.
- **Never launch charged jobs** (TTS / paid image API / uploads). Consume the measured "Brian" narration_index only.
- **Never overwrite shipped mp4s** (AE output = `v002_ae`; base = `v001`).
- **Never burn a number not in the §2 ledger.** Hedged (≈20 indicators, ≈12 years, WLM12/13/26) never asserted without hedge. **No settlement/money number exists — never invent one.**
- **Never guess `FigureSpec.kind`** (§6.2 lowercase real values; `comparebars`→`compbars`). **No `dochighlight`. quote/votetally unused.**
- **★ Never emit/implement DATE_STAMP/SEAM_TRANSITION/VOTE_SPLIT/MONEY_STACK** (crash / no verified vote / no money). Use ONLY the 6 proven layouts; add no new layout.
- **★ Never comma-group years** (1991/2004/2009 → group:false; §9).
- **★ `build_willingham_film.py` full-loads `factory[]`(165)/`motion[]`(30); empty/wrong → exit 1** (EP45 slideshow guard).
- **★ Never use `treatment:"depth"` / depth maps** (melts subjects — task rule #2; cut cycle `["bleed","scan","duotone","focus"]`).
- **★ Never add a full-frame haze/fog/vignette-wash or scanline/CRT** (task rule #1; wash opacity ≤0.07; overlays are per-beat only).
- **★ Never re-introduce a silent hook runway** (§4.4 · voice from 0:00; keep the brand sting as a HOOK→OP interstitial). **Never use real-person/archival audio** (Brian + dramatized SFX only).
- **★ Never claim legal innocence/"exonerated"; never depict the children or their deaths; never create a real-person likeness; "monster" only as attributed framing to dismantle.**
- **★ AE two-step render (AfterFX saves .aep → separate aerender → REPO path on C:)**; assert `.aep` mtime > `.jsx`.
- **Never change the spec numbers** (395 cuts / still150/factory165/motion30 / distinct345 / first-use0.8734 / still-share0.4304 / figures58(floor51) / AE 17 (6 proven) / narrationSeconds1203.4 provisional / durationInFrames36,477 provisional) — durationInFrames/narrationSeconds updated **only from measured TTS** (§5.1.1).
- **composition id = `Ep51Willingham`**; typecheck green. **No PowerShell-generated regex/escapes** (`\b` backspace harm).
```
