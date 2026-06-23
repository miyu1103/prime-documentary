# PD-2026-016-titan — "Pure Waste" (first PD feature, ~58 min)

OceanGate's Titan submersible: how a culture that treated safety certification as optional ignored years of explicit warnings and dived to the wreck of the Titanic. The U.S. Coast Guard later found the loss **preventable**.

- **State:** `script_verified` (validator PASS) · **Risk:** R2 · **Tier:** A · **Lang:** EN narration
- **Thesis:** Why intelligent people believe the rule-breaking visionary until physics forecloses the choice. The ocean is the one investor that always does its own due diligence.
- **Moral center / dignity guardrail:** Suleman Dawood (19). No schadenfreude; no graphic implosion; cause attributed to the USCG Board; no real-person likeness.

## Left process (Claude) — DONE
- `00_topic/topic.v001.json` · `01_research/{sources,claims}.v001.json` (10 sources / 14 claims, web-verified 2026-06-24)
- `03_script/script.en.v001.md` (6,266 words, FK 5.6, 0 filler) · `script.annotated.v001.json` (107 spans) · `script_qc.v001.json`
- `04_scenes/{shotlist.v001.json, ai_prompts.v001.md (76 hero prompts), design_bible.v001.md}`
- `manifest.json` · `approvals/APR-0001.json` (owner content sign-off) · `events/events.jsonl`
- Infra: `decisions/0003-feature-duration-profile.md` + `scripts/validate_episode.py` feature band.

## Right process (Codex) — NEXT
See `CODEX_HANDOFF.v001.md`. Images (SDXL :7860) → factory b-roll → code-graphics → Remotion `TitanFeature` → audio 4-layer → libx264 render.

## Verify
`./.venv/Scripts/python.exe scripts/validate_episode.py 16` → PASS

## Remaining human gates
first-cut · title/thumbnail · **pre-publish fact re-check** · public scheduling. ElevenLabs master narration = cost gate (owner GO).
