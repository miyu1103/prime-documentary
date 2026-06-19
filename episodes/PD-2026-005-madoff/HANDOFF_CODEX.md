# HANDOFF → Codex (local executor) — PD-2026-005-madoff

You are the **local executor** (Codex on the owner's Windows/Mac nodes). Claude has done the design (topic, research, script, scene/visual/audio/edit specs). Your job is to **execute the generation and assembly** from these specs and stop at the human gates. Do not redesign; if a spec is ambiguous or a fact is unverified, stop and ask.

## 0. State & what's already approved
- Episode state: `scene_planned` → ready for asset generation. Manifest is the source of truth.
- Approved: topic v002 (APR-0002), **final script v001 (APR-0003)**.
- Risk: R1 (Madoff deceased, pleaded guilty). Still faceless / no real-person likeness / **no pink**.

## 1. HARD safety constraints (do not violate)
1. **No pink** anywhere. All people are anonymous silhouettes — **no real-person likeness**, no deepfakes (invariant 11).
2. Generated visuals are symbolic reconstruction, **never** presented as authentic footage. Keep the cold-open + description disclaimer ("Dramatized symbolic reconstruction. Not financial or legal advice.").
3. Every on-screen factual number must carry a **citation lower-third linked to its claim_id** (see claims.v001).
4. **Paid generation only after SCRIPT LOCK + explicit owner go** (ElevenLabs master, Runway). Drafts/dry-runs first. Use idempotency keys; log provider request IDs; never silently double-bill (rules/11).
5. **Publish = upload PRIVATE first**; public scheduling needs the exact-revision **publish approval** gate. Channel/destination allowlist only.
6. Keep media off the git repo (logical URIs); repo holds specs/manifest/approvals only (rules/14).

## 2. Resolve BEFORE script lock (research follow-ups)
From `01_research/qc.v001.json` — confirm against primary sources, then lock script:
- SEC OIG report (OIG-509): exact Markopolos submission count/dates + the 2005 memo title (CLM-0005/0011).
- Trustee/DOJ: latest recovery totals + official $65B vs $17.5B definitions (CLM-0004/0009).
- 1–3 named institutional victims, neutral framing (CLM-0008); exact 11-count wording (CLM-0001).
- If any changes the wording of an adjudicated fact → create script v002 (invalidates dependent assets).

## 3. Execution tasks (in order)

### T1 — Images (SDXL, local) → `05_visuals/`
- Spec: `04_scenes/sdxl_prompts.v001.md` (H01–H26) + `04_scenes/visual_bible.v001.json`.
- Model RealVisXL/JuggernautXL; lock one model/VAE + seed family; shared NEGATIVE (incl `pink`).
- Generate 3–4 candidates/shot + 2–4 coverage angles each → upscale R-ESRGAN 4x → 1080p.
- Output to `05_visuals/candidates/` then `05_visuals/approved/`. Record content_hash + provenance.
- Selection: composition, seed consistency, no breakage, scene-intent, must read as symbolic.

### T2 — Motion graphics (Remotion) → tier-K renders
- Spec: `04_scenes/remotion_plan.v001.json` (G01–G12): THE LINE refrain, Ponzi loop, $65B→$17.5B morph, warning-years timeline, citation lower-thirds, open captions, cards.
- Data-driven; exact numbers from claims.v001; **no pink**; cold accent only for THE LINE.

### T3 — Motion beats (Runway, budget-capped) → optional
- Spec: `04_scenes/runway_shots.v001.md` (RW1–RW5). Stay within monthly credits; if near cap, drop RW4 → Remotion parallax. Paid → dry-run then owner go. Log IDs.

### T4 — Narration (ElevenLabs) → `06_voice/`
- Spec: `06_audio/voice_plan.v001.json` (VC-0001…0023, pronunciation dict, silence beats).
- **Draft pass first** for timing; **master only after script lock + owner go**. Chunk-level so one fix = one re-render.

### T5 — Music/SFX/mix → `07_music/` + mix
- Spec: `06_audio/audio_cue_sheet.v001.md` (M1–M6 arc, 100% ambience, 60–100 SFX, silence beats). Library assets only (record reuse + rights). Target −14 LUFS, TP ≤ −1 dB, VO ducking.

### T6 — Assembly & render (Remotion + FFmpeg) → `08_edit/`
- Spec: `08_edit/edit_plan.v001.json` (assembly_order 1–9). Force-align captions to the voice master.
- Output `08_edit/renders/review.proxy.v001.mp4`. Run the `qc_before_first_cut` checklist.
- **STOP → human gate: first-cut approval** (record APR, exact render hash).

### T7 — Package (after first-cut approval)
- Title + thumbnail per `visual_bible` thumbnail_concept ("TOO PERFECT TO BE REAL" / empty-vault alt), curiosity-gap, no face, no pink, ≤4 words. **STOP → human gate: title+thumbnail approval.**
- Description (with disclaimer + "not financial/legal advice"), chapters from section markers, subtitles, **rights_manifest** (every asset: rights_basis/source/verified_at), final QC.

### T8 — Publish (after publish approval)
- Upload **PRIVATE** first to the allowlisted channel. Public scheduling only on the exact-revision **publish approval** gate. Then state → published; write analytics hooks.

## 4. After each task
- Update `manifest.json` (active_revisions + state), append `events.jsonl`, commit to the working branch. Never overwrite an approved artifact — new revision only (rules/05, rules/12).

## 5. Human gates (do NOT cross without a recorded approval)
final script ✅ (done) → **first cut** → **title+thumbnail** → **publish (private→public)**.

---
Design inputs index: `00_topic/topic.v002.json`, `01_research/*`, `03_script/script.en.v001.md`, `04_scenes/{scene_plan,visual_bible,sdxl_prompts,remotion_plan,runway_shots}.v001`, `06_audio/{voice_plan,audio_cue_sheet}.v001`, `08_edit/edit_plan.v001.json`.
