# CODEX HANDOFF — EP24 "The Wiretap That Cracked Wall Street" (PD-2026-024-rajaratnam)

> The single MASTER DESIGN DOC Codex reads to BUILD the episode. Claude owns the LEFT side
> (topic / research / claims / script / annotated) — done and LOCKED. Codex owns the RIGHT side
> (scenes -> images -> narration -> music -> motion -> edit -> render -> thumbnails).
> Build the FIRST render to satisfy the whole acceptance table. NUMBERS, NOT ADJECTIVES.
> If two sources conflict: claims.v001.json wording locks win, then this doc, then the stricter reading — note it, ask nothing.
> Companion file = `episodes/_planning/codex_local_024_build.md` (the ordered deterministic build prompt). This doc is the spec; that file is the run order.

---

## 0. IDENTITY & STATE (source: episodes/PD-2026-024-rajaratnam/manifest.json)
- episode_id: **PD-2026-024-rajaratnam**  ·  topic_id: **TOP-20260630-024**  ·  slug: **rajaratnam**
- title_working: **"The Wiretap That Cracked Wall Street"**
- risk_class: **R2**  ·  production_tier: **A**  ·  autonomy_level: 3  ·  target_language: en
- duration profile: **mid** (target_duration_minutes = 30). Per manifest warning (ADR-0008): **narration band 24.0–32.4 min; finished-runtime band 27–33 min** (NOT the standard 11.5–12.5 gate).
- state: **script_verified**. validate_episode.py 24 = PASS (green at script stage).
- active_revisions (manifest): topic v001 / sources v001 / claims v001 / script v001 / script_qc v001 / annotated v001 / codex_image_prompts v001. **Build against v001 everywhere.**
- approvals: **APR-0001 = PENDING owner script gate.** Do NOT treat the script as owner-approved. APR-0001 must flip before publish.
- **PUBLISH is a SEPARATE gate** requiring **R2 legal review** (living convicted subject). Build to a finished, gate-passing file and STOP. Never publish/upload/schedule/set thumbnail live.
- Heavy media on `H:\pd-media\episodes\PD-2026-024-rajaratnam\` (NEVER commit). Repo: `C:\Users\aab15\Documents\prime-documentary`. Python: `./.venv/Scripts/python.exe`.
- Commit ONLY this episode's files. New immutable revisions only (vNNN); never overwrite an approved artifact (invariant 6).

## 1. EMOTIONAL SPINE & RE-HOOK
- **Thesis (annotated.thesis):** Everyone suspected the top of Wall Street was rigged by inside whispers, but the crime was invisible until investigators treated a billionaire like a mobster and recorded his phone; the wiretap turned a deniable whisper into the one piece of evidence a powerful man cannot argue with — his own voice.
- **The one human funnel = Raj Rajaratnam.** Every thread routes through him. Co-defendants are nodes that lead back to his telephone; never let a side character take the wheel.
- **Central question — opened in the first 8s, paid off in the coda:**
  - Opened (SPN-0005, cold open): *"What does it actually take to catch one of them? And what did the people chasing him have to become, to finally make it stick?"*
  - Paid off (SPN-0051, coda): *"It took the government deciding to treat a billionaire like a gangster. It took a judge's signature granting permission to listen. And in the end, it took the one piece of evidence that even the most powerful man in the room cannot argue with: himself."*
- **Re-hook every ~2–3 min** at chapter seams and inside long chapters: cut back to the grey room / the turning reel / the waveform motif so the "his own voice catches him" promise stays alive (motif appears SPN-0001, SPN-0004, SPN-0024 visual, SPN-0028, SPN-0035, SPN-0051). Retention engineered to stay flat-to-rising.
- **The "Like = the system finally caught one"** payoff is earned, not begged: CTA only lands after SPN-0053.
- **Money lines (pulled verbatim from script — protect these beats; let picture breathe under them):**
  1. *"How do you prove a whisper?"* (SPN-0009)
  2. *"The whisper had a waveform."* (SPN-0035)
  3. *"They were hiding in plain sight... protected by one simple and seemingly permanent fact. No one could hear them."* (SPN-0027)
  4. *"This was never the story of a single bad apple. It was the story of an orchard."* (SPN-0046)
  5. *"...the one piece of evidence that even the most powerful man in the room cannot argue with: himself."* (SPN-0051)

## 2. STRUCTURE & RUNTIME
Source: script.en.v001.md (narration master, [VO:] only) + script.annotated.v001.json (53 spans, SPN-0001..SPN-0053, 6 chapters).

| Block | Chapter id | Title | Script timecode | Spans | Register / color |
|---|---|---|---|---|---|
| HOOK (~0:00–0:08) | cold_open | flash-forward | inside 0:00–1:40 | first beat of SPN-0001 | grey, near silence, single reel turning |
| COLD OPEN | cold_open | (tease) | 0:00–1:40 | SPN-0001..0005 | grey + a thread of electric blue |
| OPENING (BrandOpening) | — | brand title | lands AFTER the 8s hook | — | gold sunrise + PD monogram |
| ACT 1 | the_edge | **THE EDGE** | 1:40–9:30 | SPN-0006..0017 | gold, warm, seductive (M1 rising, confident) |
| ACT 2 | the_whisper | **THE WHISPER NETWORK** | 9:30–16:30 | SPN-0018..0028 | warm interiors turning clinical (M2 intimate + cold thread) |
| ACT 3 | the_wire | **THE WIRE** | 16:30–23:30 | SPN-0029..0039 | cold blue surveillance (M3 low, patient, mechanical pulse) |
| ACT 4 | the_reckoning | **THE RECKONING** | 23:30–28:30 | SPN-0040..0049 | flat courtroom daylight (M4 spare, building to one resolved chord at the verdict) |
| ENDING + CTA | coda | resolution & CTA | 28:30–30:00 | SPN-0050..0053 | dusk cooling to blue (M5 = M1 theme returned, quieter) |

- **HOOK** = the first ~8s of SPN-0001 (the grey room, the thumb on PLAY) cut fast, THEN the gold **BrandOpening** lands (not at frame 0). **BrandEndcard** at tail under/after SPN-0053.
- **Dedicated Subscribe+Like CTA beat ~29:10–29:35** sits on SPN-0053 ("...subscribe to the channel, and hit the like button below..."). PD brand styling, NO real YouTube logo.
- **Narration length:** ~3,776 words. annotated `estimated_duration_seconds = 1510.4` (~25.2 min @150 wpm). Authoritative bands from manifest: **narration 24.0–32.4 min; finished runtime 27–33 min.** The edit (factory layer, transitions, breaths, hook + endcard) carries the finished cut into the 27–33 band; do NOT pad with dead air.
- **OP/ED canonical = `remotion/src/components/Bookends.tsx`** (`OPENING_SEC = 3.5`, `ENDCARD_SEC = 9`). **DO NOT FORK IT.** Drive EP24 through the existing premium-from-roughcut composition (register in `remotion/src/Root.tsx` if needed).

## 3. VOICE & MUSIC (numbers)
- **Narration = ElevenLabs master.** VOICE_ID **`nPczCjzI2devNBz1zQrb`**, model **`eleven_multilingual_v2`**, **stability 0.35**, **similarity_boost 0.80**, style 0, speaker_boost on. Speak ONLY `[VO:]` lines in order; ignore any "#"/`[CLM-xxxx]` markers; strip claim tags. **SAPI / Windows / local TTS FORBIDDEN in the final** (EP14 failure — never again). Idempotency key per chunk; if a chunk exists on disk, do NOT regenerate (no double billing).
- **Music = continuous library bed (Suno-origin assets, rights-tracked), ONE track per chapter** (6 cues): COLD OPEN = near-silence/single-reel texture; M1 rising confident (gold); M2 intimate with a cold thread; M3 low patient mechanical pulse; M4 spare building to one resolved chord at the verdict; M5 = M1 returned, quieter, resolved.
- **Ducking:** duck the bed under VO to an **audible floor ~ -22 LUFS** — the bed MUST stay audible under narration, **NEVER duck to silence**. **No silent stretch > 25s** anywhere. **Final integrated loudness -16..-12 LUFS.**
- One designed near-silence is allowed in the cold open ("Near silence. A single reel turning.") but it is a held texture, not dead air, and is < 25s.

## 4. CAPTIONS (numbers)
- **Force-aligned to the RENDERED ElevenLabs audio** (verbatim from what the narrator actually said — NOT pasted from the script file).
- **1 cue = 1 breath group** (split at the narrator's real breaths). **≤2 lines**, **≤42 chars/line**, duration **1.0–6.0s**, **≤17 cps**, **≥2-frame gaps** between cues.
- **Position: lower 10–15% (bottom-safe). NEVER centered or high.** Brand font, drop-shadow. **Coverage ≥95%** of runtime.

## 5. IMAGES — Codex generation only (SDXL NOT used this episode)
- **Generate every numbered MEGA-PROMPT in `episodes/PD-2026-024-rajaratnam/04_scenes/codex_image_prompts.v001.md`** (the per-scene image brief). NOTE: at handoff time that file may not yet be written — it is the authoritative per-scene image brief keyed to the 53 spans' `visual_intent`. If it is missing, STOP and report (do not invent random images); do not start the edit without it.
- **ONE masterpiece prompt per scene → exactly 1 image per prompt.** Regenerate ONLY failures (a still that violates a hard rule below). No bulk variant farming.
- **Output:** 16:9, **long edge ≥ 3840 px**.
- **Brand palette:** black / midnight-navy base + **electric-blue `#1F6BFF`** + **gold `#E5B53A`** + silver.
- **HARD image rules (reject + regenerate on any violation):**
  - **NO real-person likeness** (no Rajaratnam, Gupta, Goel, Kumar, Moffat, Chiesi, agents, judges — invariant 11).
  - **NO real logos / seals / landmarks / real company marks** (no Galleon, Intel, McKinsey, IBM, Goldman Sachs, SEC/FBI/court seals, no identifiable buildings).
  - **NO readable text in the image** (Remotion adds all text). No anatomy errors.
  - Symbolic reconstruction only; nothing may look like an authentic photograph or evidentiary record (invariant 11). Register every used still in the rights manifest (origin = Codex AI, AI-disclosed).
- Visual vocabulary is already specified per span in `visual_intent` (grey interview room + recorder + PLAY; glowing night trading floor from above; reel-to-reel threading; gold web of nodes on a dark map; four empty chairs in four rooms; waveform freezing to ice labeled EXHIBIT; dawn street + unmarked cars; empty courtroom + jury box; money dissolving into court documents; the city skyline at night). Build to those.

## 6. ANIMATION / DYNAMISM (these failed before — enforce numerically)
- **NO static image, ever. NO frame held > 2s. NO naked hard cut.**
- **Every still gets Ken Burns ≥ 6% zoom OR parallax** (`Parallax.tsx` / `Motion.tsx`).
- **≥1 hero/organic motion shot per 60s** (SVD / 2.5D parallax + ink/particle overlay) on the marquee beats (grey room, reel turning, waveform→ice EXHIBIT, gold node web, verdict).
- **Designed transitions 0.3–0.5s crossfade/dissolve.** **OVERLAP Sequences by the transition length** so there is never a 1-frame black or jump.
- **Carry motion direction THROUGH the cut** — no velocity reset (the "kaku" stutter). **Trail motion blur** (`@remotion/motion-blur`) on fast moves.
- **Average shot ≤ ~6s**; the picture is always changing.
- **Factory shelf (221GB, commercial-OK) used abundantly:** **≥1 distinct factory clip per ~25–30s**; **factory layer across ≥40% of the timeline**; **every span carries ≥1 layer**; **no single clip reused > 3×.** Tool: `scripts/select_factory_assets.py --theme finance/legal/crime/tech/surveillance_tech` (use what fits Wall Street / wiretap / courtroom). Record license/source/hash per clip.

## 7. THUMBNAILS
- **≥3 variants**, rendered as Remotion `<Still>` at **1280×720**, backgrounds from Codex-generated stills (same R2 + no-likeness rules).
- **Loud:** UPPERCASE headline **≤ 3–4 words**, huge subject, very high contrast black/navy + gold `#E5B53A` or electric `#1F6BFF` accent, white/silver text, **legible at 320 px**. Title ≤ 60 chars. A/B title × thumb.
- **NO face / real logo / real landmark.** Background ideas: the grey room recorder, a reel-to-reel, a waveform turning to ice, a gold node-web tower.
- **Three concrete title-text concepts:**
  - A — **"CAUGHT ON TAPE"** (recorder / reel background)
  - B — **"THE $7B WIRE"** (gold node-web / glass tower)
  - C — **"HIS OWN VOICE"** (waveform freezing to ice / EXHIBIT)
- Pick a selected; DO NOT upload it (PD-001 owner gate).

## 8. R2 LEGAL & DIGNITY RULES (must hold in every caption / on-screen text / thumbnail / narration)
Source: claims.v001.json `allowed_wording` / `prohibited_wording`; manifest warnings.
- **Conviction & sentence = stated as FACT** (jury verdict May 11, 2011, guilty on all 14 counts = 5 conspiracy + 9 securities fraud; sentenced Oct 13, 2011 to 11 years). He did NOT plead guilty — he was convicted at trial and maintains innocence (CLM-0002/0003).
- **Underlying conduct framed as "the jury found / prosecutors proved / the government said / the government argued"** (CLM-0017, CLM-0018) — never as the narrator's own unattributed assertion.
- **Superlative attributed + time-bound:** "At the time, **prosecutors called it** the longest insider-trading sentence in American history" — never a flat, undated, permanent superlative (CLM-0004).
- **Profit hedged + anchored to the court forfeiture:** on screen use **"$53.8 million" / "more than fifty million dollars"** (the forfeiture). Never a single invented flat profit number; state the estimate gap as part of the story (CLM-0012). **Keep the SEC $92,805,705 civil penalty DISTINCT from the $53,816,434 criminal forfeiture + $10M fine.** Combined sanctions > $156.6M is presented as a sum, not one judgment (CLM-0005/0006/0007).
- **Wiretap "first" = "widely described as / according to the FBI and prosecutors"** — not absolute (CLM-0008). The 2nd Circuit upheld the wiretaps as lawful in 2013 (CLM-0009).
- **Rajat Gupta STRICTLY SEPARATE** (CLM-0011): different case, different jury, convicted June 2012, 2 years + $5M fine. Use ONLY to show the network reached the top. **NEVER merge Gupta's conduct or penalties with Rajaratnam's.** Tippers (Goel/Intel, Kumar/McKinsey, Moffat/IBM, Chiesi/New Castle) **charged SEPARATELY** (CLM-0010) — never merge any tipper's outcome with Rajaratnam's penalties; Goel and Kumar cooperated.
- **Memoir (CLM-0016) = grade C / conditional:** "Uneven Justice" (~2021) — **VERIFY title/date before voicing**; use only as "he says, to be fair," never to relitigate the verdict.
- **Any verbatim wiretap dialogue (CLM-0018) MUST be verified against the public trial record before voicing.** The script as written quotes no specific call — do not add one.
- **No real-person likeness or real logos/seals/landmarks in any generated image** (invariant 11).

## 9. ACCEPTANCE GATES ("DONE" = machine gates, not opinion)
- At script stage: `./.venv/Scripts/python.exe scripts/validate_episode.py 24` = **PASS** (already green).
- "Done" for the build = the independent gate exits 0:
  ```
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 24 --json
  ```
  must **exit 0** (hard rows: narration provider contains "eleven"; captions coverage ≥95% + breath-group + ≤17 cps + 0 format violations; BGM bed present, no silent stretch >25s, audible floor under VO; loudness -16..-12 LUFS; motion = 0 static spans / 0 freeze >2s / transitions present; images all long-edge ≥3840 + 0 face/logo/landmark/text violations; factory density ≥ runtime/30s; structure hook(~8s)/opening/body/ending + CTA in last 30s; OP after hook / ED at tail; ≥3 thumbnails @1280×720 + selected; 0 black frames).
- Also run: `./.venv/Scripts/python.exe scripts/check_runtime_band.py` on the rendered file → **27–33 min**. If `scripts/check_dynamics.py` exists in this repo, run it too (motion/dynamism gate) and drive it to exit 0; if it is absent, the motion rows inside `check_final_acceptance.py` are authoritative — do not skip the motion measurement.
- **Build LOOPS until green:** build → run gate → read JSON → FIX the cause → re-run. **No mid-build approvals.** Do not declare success until the real file passes; self-reported "looks good" is rejected. Any row the gate lists as manual, measure yourself against the stated number and record it.
- **PUBLISH = owner gate after R2 legal review** (+ confirm APR-0001 flipped, verify memoir title/date, verify any wiretap quote). First-cut → title/thumbnail → pre-publish legal review → scheduling are owner gates, in order. **Commit ONLY this episode's files.**

---
*Build to all of the above. The companion run order is `episodes/_planning/codex_local_024_build.md`. Numbers, not adjectives. Loop until the gate exits 0, then STOP for the owner.*
