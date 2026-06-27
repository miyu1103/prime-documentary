# EP17 「ONECOIN / NOTHING」 — CODEX MEGA-PROMPT (assets → finished cut)

> Paste everything below the line into Codex as one task. Self-contained, grounded in real repo paths, bound to the production contract, stops at every human/cost gate.

---

## ROLE & MISSION
You are **Codex**, right-process engineer for **PD-2026-017-onecoin** — "**Nothing**", a **~30-minute mid-feature** (auteur short film) on OneCoin / Ruja Ignatova, the "Missing Cryptoqueen". Claude (left process) has finished: verified script, annotated script, shotlist, the SDXL prompt pack, **and the 18 MAX-quality hero stills (already generated, reviewed, and upscaled to 4032×2304)**. **Your job:** turn the verified design into a finished, reviewable cut — factory b-roll → code graphics → Remotion composition → 4-layer audio → quality-first libx264 render → package draft — **without crossing any approval, cost, or publish gate.**

Repo `C:\Users\aab15\Documents\prime-documentary`. Python `./.venv/Scripts/python.exe`. Media on `H:\pd-media\` (never commit). Mirror existing per-episode conventions (`build_kelo_audio_v001.py`, `build_kelo_package_v001.py`, `TheranosPremium.tsx`/`KingPremium.tsx` fed by `remotion/src/data/<slug>_roughcut.ts` + `<slug>_captions.ts`, registered in `remotion/src/Root.tsx`). Do not duplicate an existing path (CLAUDE.md invariant 14).

## THE BINDING CONTRACT (read first, obey)
**`docs/PD_ONE_PASS_PRODUCTION_SPEC.v1.md`** is the production contract. **"Done" ≠ validator pass. Done = `./.venv/Scripts/python.exe scripts/check_final_acceptance.py 17` exits 0 (all hard gates) + manual rows 5/7/12/13.** You may NOT hand-write your own QC (the EP14 failure). Every recurring defect (BGM/voice/captions/quality/asset-use/motion/hook/structure/thumbnail) is pre-specified there with a gate.

## ABSOLUTE NON-NEGOTIABLES (R3 — read approvals + claims + fact_recheck)
1. **Ruja Ignatova is CHARGED, NOT CONVICTED.** Every wrongdoing reference stays "alleged/charged/accused/the U.S. indictment" — NEVER "guilty/convicted". The narration already complies; do not add any line that asserts her guilt. (Convicted associates — Greenwood/Scott/Ignatov — may be stated plainly.)
2. **No real-person likeness/deepfake** of Ignatova or anyone (invariant 11). All visuals symbolic. The wanted-poster beat = a **Remotion graphic** (a stylized female silhouette + text "WANTED · RUJA IGNATOVA · UP TO $5,000,000 · VANISHED"), NOT a real face. Hero still T-IMG-013 is a dark backdrop only.
3. **Dignity:** victims are the **moral center** — no schadenfreude, no mocking believers. Living victims/whistleblowers (Jen McAdam, the Norwegian developer) via documented statements only; no invented dialogue.
4. **No brand markings** (OneCoin logo etc.); symbolic coin only. All AI/stock disclosed, never "the authentic record."
5. **Cost gate:** **ElevenLabs master narration requires owner GO** before spend. Until then use free SAPI/local draft for timing only. No paid API without idempotency key + budget check (soft $150/hard $300).
6. **Never publish/upload/schedule/change channel settings/delete approved artifacts.** Stop at every human gate and report.
7. **Immutability:** never overwrite an approved artifact; new `vNNN` (invariant 6). ID+revision+sha256+provenance on every artifact. Resumable/idempotent jobs.
8. **Source of truth = `manifest.json`** → `active_revisions`. Build against the approved script (v001).

## INPUTS (read in order)
1. `manifest.json` (state=`assets_ready`, target_duration_minutes=30, R3).
2. `03_script/script.en.v001.md` — narration master ([VO:] = the spoken truth). 5 chapters: **cold_open → the_promise (gold) → the_crack (white) → the_void (black) → coda**.
3. `03_script/script.annotated.v001.json` — 48 spans, claim_ids, visual_intent. sha in manifest + shotlist `source_annotated_sha256`.
4. `04_scenes/shotlist.v001.json` — 48 shots, 1:1 with spans: `suggested_asset_type` (ai_image / motion_graphic), `asset_ref` (T-IMG-* or MG-*), `motion`, `search_keywords`.
5. `04_scenes/ai_prompts.v001.md` — the hero pack (already generated).
6. `04_scenes/design_bible.v001.md` — the auteur treatment (§2 form, §3 signature devices, §5 audio, §6 dignity, §7 acceptance) + `04_scenes/thumb_prompts.v001.md`.
7. `05_stock/usable_assets.v001.json` — **19 hero stills, 4032×2304, on `H:\pd-media\episodes\PD-2026-017-onecoin\05_stock\hero\_final\`** (T-IMG-001_v2, _v3, 002–016, AUX2 [+AUX1 spare]).
8. `01_research/{claims,sources}.v001.json` + `01_research/fact_recheck.v001.md` — honor every R3 attribution; verify ★ verbatim before locking narration.

## THE AUTEUR FORM (preserve — this is why it wins)
- **The film enacts the con: seduce → believe → nothing.** Color arc is load-bearing: **gold (promise) → cold white (crack) → black (void)**, coda in white airport light. Grade each chapter to its color.
- **Second-person** narration; do not undercut it.
- **Recurring motif = the empty ledger** (MG-LEDGER) and the coin-with-a-hole (T-IMG-003). Bring them back.
- **The silence beat:** at the void reveal (the `[VO:] ...` span in `the_void`), **cut ALL audio + hold on black** for the designed beat (MG-BLACK). Preserve exactly.
- **Unresolved ending:** the coda does not resolve. Do not add hopeful music swells.

## CURRENT STATE (done — do NOT redo)
Hero stills generated, reviewed, upscaled (≥3840), registered. **Start at Step 1 (factory b-roll) + Step 2 (code graphics) + the Remotion composition.**

---

# PIPELINE (QC-gate each step; append an event to `events/events.jsonl`; update manifest)

## STEP 1 — Factory b-roll (the establish / "間" layer) → `remotion/public/onecoin/factory/`
Pull commercial-OK clips per the motifs (use `scripts/select_factory_assets.py --help`):
```
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme finance_money            --kind video   # gold, cash, wealth (PROMISE)
./.venv/Scripts/python.exe scripts/select_factory_assets.py --query "stage crowd spotlight"   --kind video   # arenas, audiences
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme surveillance_tech         --kind video   # servers, data, world map (CRACK)
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme atmosphere_symbolic                      # empty chair, clock, candle, padlock (VOID)
./.venv/Scripts/python.exe scripts/select_factory_assets.py --query "airport night runway"     --kind video   # the vanishing (coda)
```
Record license/source/hash for every clip. **Spec row 7: ≥1 distinct factory clip per ~45 s; every span carries ≥1 layer; no clip reused >3×.**

## STEP 2 — Code graphics (Remotion, NOT SDXL) — the `motion_graphic` shots in the shotlist
- **MG-LEDGER** (central motif): a ledger whose rows should fill but stay blank; a chain of links that dissolves into nothing. Recurs across chapters.
- **MG-TREE**: an MLM referral tree of glowing nodes multiplying into a pyramid, then going dark all at once.
- **MG-BARS**: "raised" (a gold bar filling to >$4B) vs "real value" (a bar that never leaves zero).
- **MG-BLACK**: the held-black silence beat at the void reveal (all layers cut).
- **Wanted-poster graphic** (the `the_void` poster beat): stylized **female** silhouette (NO real likeness) + text "WANTED · RUJA IGNATOVA · FBI TEN MOST WANTED · UP TO $5,000,000 · VANISHED 2017"; over/with backdrop T-IMG-013.
Dates/figures must match `claims.v001.json` and be R3-attributed.

## STEP 3 — Remotion composition `OneCoinPremium`
- Create `remotion/src/compositions/OneCoinPremium.tsx` (extend `RoughCut.tsx`/`CasePremiumFromRoughCut.tsx`/`TheranosPremium.tsx`); feed from `remotion/src/data/onecoin_roughcut.ts` (extend to all **48 spans**, grouped by `chapter_id`, color per chapter) + `remotion/src/data/onecoin_captions.ts` (Step 4). Register in `remotion/src/Root.tsx` (`id="OneCoinPremium"`, `durationInFrames` from `oneCoinPremiumDurationInFrames(fps)`); fps per `BRAND.video.fps`; ~30 min ≈ **~54,000 frames @30fps**.
- **Spec row 8 — motion mandatory, no static**: every hero still gets MovingImage (Ken Burns ≥6% / parallax via `Parallax.tsx`/`Motion.tsx`) per the shotlist `motion`; factory = MovingVideo; T-IMG-014 ink as overlay. No frame motionless >2 s (except the designed black beat). Use the 19 stills + factory across all 48 spans so **every span has a moving picture**.
- Keep chapters independently renderable (per-chapter render in Step 6).

## STEP 4 — Audio (4 layers; narration master = tempo) → `scripts/build_onecoin_audio_v001.py`
- **Narration (EN):** chunk `[VO:]` spans → `06_audio/narration_index.v001.json`. SAPI/local **draft first** for timing. **STOP, request owner GO before the ElevenLabs master.** On GO: `VOICE_ID=nPczCjzI2devNBz1zQrb`, `model=eleven_multilingual_v2`, stability≈0.35, similarity≈0.80, with an idempotency key + char/cost tracking → `06_audio/voice_master.v001.*`. (Spec row 2 — never ship SAPI.)
- **Captions:** forced-align to the rendered master (gen_captions_forced.py / align_*) → `08_edit/captions.v001.srt` + `remotion/src/data/onecoin_captions.ts`. **Spec rows 3–4: text matches the audio ≥99%; ≤2 lines, ≤42 chars/line, clean breaks.**
- **Music (Suno-origin, ingested as assets, rights-tracked):** M1 awe/seduction (gold) → M2 low unease (crack) → M3 hollow drone collapsing to silence (void) → Coda single piano note + silence. The roar→static→one-voice→silence "curdle" at the cold-open and the void.
- **Ambience/SFX:** arena roar, crowd murmur, notification chimes (referral payouts), keyboard, rising-number tick, **static** at the void, **total silence cut** at the implosion-of-belief beat.
- Mix → `remotion/public/onecoin/audio/onecoin_final_mix_v001.wav` (+hash); QC → `08_edit/audio_mix.v001.qc.json`. **Spec row 1: continuous ducked bed, no silence >25 s (except the beat).**

## STEP 5 — Thumbnails (≥3, before package) → Remotion `<Still>` 1280×720 per `thumb_prompts.v001.md`
Concepts A "THERE WAS NO COIN / AND MILLIONS BELIEVED" (T-IMG-003), B "SHE VANISHED / STILL ON THE FBI'S LIST" (T-IMG-012/013-graphic), C "$4 BILLION. GONE." (T-IMG-002). Gold/electric accent, ≤4-word UPPERCASE headline, legible at 320 px. **No real face; no "GUILTY" for Ignatova.** Manual upload (PD-001). (Spec rows 11–13.)

## STEP 6 — Render (quality-first; NOT NVENC)
`npx remotion render OneCoinPremium` **per chapter** (5) → FFmpeg concat → `-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p`; audio `-c:a aac -b:a 192k`; 1920×1080. Output → `H:\pd-media\episodes\PD-2026-017-onecoin\07_edit\v001.mp4` (+sha in manifest). Resumable per chapter. (Spec row 6.)

## STEP 7 — Package draft (DO NOT PUBLISH) → `scripts/build_onecoin_package_v001.py`
Title (candidates in thumb_prompts; working "Nothing — The Woman Who Sold a Coin That Did Not Exist"), description, chapters, tags, subtitles, `rights_manifest.v001.json`, `youtube_meta.v001.json`, `OWNER_REVIEW_REQUEST` for first-cut.

---

# ACCEPTANCE GATE (a step is done only when measured on the real file)
`./.venv/Scripts/python.exe scripts/check_final_acceptance.py 17` → **exit 0** (hard: voice master / captions coverage+format / runtime band **27–33 min** / resolution / no black / **motion (no static)** / bgm bed / thumbnail). Then measure manual **rows 5 (source stills ≥3840 — already ✓), 7 (factory density), 12–13 (thumbnail/title)**. Independent measurement — never self-attested (CLAUDE.md invariant 13, rule 17).

# HARD STOPS — pause and report; do not proceed past:
1. **ElevenLabs master narration** (cost GO).
2. **First-cut review.**
3. **Title/thumbnail approval.**
4. **Pre-publish LEGAL REVIEW + same-day fact re-check (R3)** — `fact_recheck.v001.md`: verify ★ verbatim DOJ/FBI quotes; confirm every Ignatova line is "alleged"; no real likeness anywhere.
5. **Public scheduling** — only after an APR bound to the exact revision/hash.

# REPORT (every stop; CLAUDE.md §12): Result · Files changed · Behavior · Verification + exact results (check_final_acceptance output, measured runtime, QC json) · Data impact · External side effects & cost · Limitations/risks · Rollback · Next action. State the active script revision. Media on `H:\`, off git.

**Begin with a short PLAN (Japanese ok) of Steps 1–3 and the files you will create — then execute. Do not skip the gates.**
