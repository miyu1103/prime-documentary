# Prime Documentary — Takeover Audit (Evidence-Based)

- Date: 2026-06-13
- Operator: Claude Code
- Mode: read-first takeover per `BOOTSTRAP_PROMPT.txt`
- Scope: the materialized blueprint repository at project root

This report precedes implementation. It is evidence-based and cites file paths.
The first vertical slice that follows this audit is described in
`docs/VERTICAL_SLICE_MVP.md`.

---

## A. Repository map

### What exists (executable)

- `src/pd_factory/` — small reference core, all imported and tested:
  - `domain.py` — `EpisodeState` (28 states), `JobState`, `RiskClass`, `Severity`, `RevisionRef`, `StateEvent`.
  - `state_machine.py` — canonical episode transitions + narrow operational loops.
  - `artifact_uri.py` — `artifact://` logical URIs with path-escape rejection.
  - `idempotency.py` — order-independent canonical idempotency keys.
  - `budget.py` — soft/hard budget ledger with reserve/commit.
  - `approval.py` — exact-revision + exact-hash approval validity.
  - `schema_validation.py` — Draft 2020-12 JSON Schema validation.
  - `cli.py` — `transitions`, `validate` subcommands.
- `scripts/validate_all_v2.py` — whole-package validator (JSON/YAML/Python/pytest). **Runs green.**
- `scripts/` — `build_status_report.py`, `create_episode.py`, `validate_examples.py`, `build_v2_package.py`, `check_secrets.py`, `guard_destructive.py`, `validate_manifest.py`.
- `tests/` — 9 unit tests over the core. **All pass.**

### What is documentation only

- `docs/00..41` (42 specs), `contracts/01..11`, `architecture/adrs/0001..0010`,
  `decisions/0001`, `backlog/EPIC-01..08`, `prompts/01..12`, `templates/`,
  `.claude/skills/` (22), `.claude/agents/` (11), `hooks/` (3 example hooks).
- The two master documents (`PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md`,
  `PD_CLAUDE_CODE_MASTER_BLUEPRINT.md`) are **concatenations** of the same source
  files, not independent sources of truth.

### What is duplicated

- `PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md` and `PD_CLAUDE_CODE_MASTER_BLUEPRINT.md`
  embed `CLAUDE.md`, `VERSION.md`, `START_HERE.md`, `decisions/`, and `docs/` verbatim.
  Risk: edits to the canonical files will drift from the bundled mega-docs.
- `PACKAGE_MANIFEST.md` vs `PACKAGE_MANIFEST_V2.md`; `VALIDATION_REPORT.md` vs
  `VALIDATION_REPORT_V2.md` (V1 artifacts retained alongside V2).

### What is obsolete or inconsistent

- **G1 (state-enum mismatch).** `src/pd_factory/domain.py::EpisodeState` defines 28
  states (incl. `pre_research`, `thesis_ready`, `script_review`, `audio_*`,
  `finalizing`, `uploading`, `analytics_active`). `schemas/episode-manifest.schema.json`
  and `schemas/common.schema.json` `state` enums define a **condensed 21-state** set
  that omits several of those and adds `voice_ready`/`music_ready`. The manifest schema
  is the contract for on-disk manifests; the code state machine is richer. These two
  must be reconciled. Until then, on-disk `manifest.state` must use the schema enum.
- **G2 (sources schema shape).** `examples/episode/01_research/sources.v001.json` is a
  JSON **array**, but `schemas/source.schema.json` validates a **single** source object.
  Array files must be validated per-item, not whole-file.

### What is missing (the real gap)

- **No orchestration.** There is no module that takes a topic and produces the
  downstream artifact chain. The core proves *properties* (transitions, idempotency,
  budgets, approvals) but nothing *runs the pipeline*.
- No artifact repository (immutable revisioned writes, overwrite protection, manifest
  registration, event log).
- No resume / partial-rerun / downstream-invalidation logic.
- No per-stage schema-validated generators.

---

## B. Current capability matrix

Legend: not_started / spec_only / partial / testable / production_ready / ext_blocked

| Stage | Status | Evidence |
|---|---|---|
| Demand sensing | spec_only | `docs/02`, `docs/03` |
| Topic / scoring | testable (data) | `schemas/topic.schema.json`, `examples/episode/00_topic/topic.v001.json` |
| Research plan | spec_only → **(this slice: testable)** | `schemas/research-plan.schema.json` |
| Source registry | spec_only → **(this slice: testable)** | `schemas/source.schema.json` |
| Claim ledger | spec_only → **(this slice: testable)** | `schemas/claim-ledger.schema.json` |
| Thesis / outline | spec_only → **(this slice: testable)** | `schemas/thesis.schema.json` |
| Script (annotated) | spec_only → **(this slice: testable)** | `schemas/script-annotated.schema.json` |
| Scene plan | spec_only → **(this slice: testable)** | `schemas/scene-plan.schema.json` |
| Asset plan | spec_only → **(this slice: testable)** | `schemas/asset-plan.schema.json` |
| Visual generation (SDXL) | ext_blocked | RTX 4090 / ComfyUI, no adapter yet |
| Voice plan / narration | spec_only (plan) → **(this slice: draft plan)** | `schemas/voice-plan.schema.json` |
| Music | ext_blocked | `architecture/adrs/0006-library-first-music.md` |
| Edit plan / DaVinci | spec_only (plan) → **(this slice: plan)** | `schemas/edit-plan.schema.json` |
| QC report | spec_only → **(this slice: testable)** | `schemas/qc-report.schema.json` |
| Package / publish | spec_only, gated | `schemas/publish-package-v2.schema.json`, `hooks/require_publish_approval.py` |
| Analytics / learning | spec_only | `schemas/analytics-snapshot.json`, `docs/22` |

---

## C. Risk audit

- **Secrets / credentials:** none committed. `scripts/check_secrets.py` exists;
  validator reports "no obvious secrets." `.gitignore` excludes `.env`, `secrets/`,
  `credentials/`. ✅
- **Destructive operations:** `hooks/block_dangerous_commands.py`,
  `scripts/guard_destructive.py` present (defense exists). No destructive code paths
  in the core. ✅
- **Paid API calls:** none implemented; idempotency + budget primitives exist and must
  gate any future external call (invariant 5). ⚠️ enforced only when callers use them.
- **Public upload / publishing:** none implemented; `hooks/require_publish_approval.py`
  enforces approval intent. Slice does **no** upload. ✅
- **Rights / provenance:** `artifactRef.rights_status` exists in schema; example sources
  carry `rights_note`. Generators must not fabricate rights as "clear". ⚠️
- **Prompt injection:** invariant 10 (research text is untrusted). No web ingestion yet,
  so no live exposure. To enforce when `docs/28` ingestion lands. ⚠️
- **Data loss / stale artifacts:** no overwrite protection existed before this slice
  (invariant 6). Addressed by the new immutable artifact repository.
- **Windows/Mac paths:** logical `artifact://` URIs (ADR 0007) mitigate; core uses
  `PurePosixPath`. ✅ for logical layer.
- **Non-idempotent operations:** the new pipeline keys every stage (invariant 8).

---

## D. Architecture gap analysis (current vs target)

Target (`docs/02_END_TO_END_PIPELINE.md`, `docs/10_DATA_MODEL_AND_STATE_MACHINE.md`):
artifacts flow `topic → research → claims → thesis → script → scenes → assets →
narration → edit → QC`, each immutable, revisioned, provenance-bearing, resumable,
partially re-runnable, with a change to claims invalidating dependents (invariant 12).

Current vs target:

1. Domain properties exist and are tested, but **nothing composes them into a run**
   (`src/pd_factory/` has no pipeline). → Add `pipeline.py` + `episode_repo.py` +
   `generators.py`.
2. Immutability/provenance are stated invariants but **not enforced on disk**. → Add
   immutable revisioned writes + provenance sidecars + manifest registration.
3. Downstream invalidation (invariant 12) is **not implemented**. → Implement via
   idempotency keys that include upstream input revisions, so a changed upstream
   revision forces dependents to recompute.
4. State enum contract conflict (G1) must be respected: on-disk state uses the
   **schema** enum.

---

## E. Recommended first vertical slice

The smallest slice that proves the architecture (not a toy):

`approved topic → research_plan → sources → claim_ledger → thesis → annotated_script
→ scene_plan → asset_plan → draft_voice_plan → edit_plan → qc_report`

- No public upload. No uncontrolled paid calls. No LLM/network — deterministic stub
  generators derived from the topic's own fields (no invented facts; placeholders are
  explicitly flagged, and the final QC report marks the episode not-publishable until
  real research replaces placeholders).
- Must demonstrate: immutable revisioned artifacts, provenance + hashes, schema
  validation per stage, idempotent resume, partial rerun with downstream
  invalidation, manifest + event-log updates, and overwrite protection.

Implemented in this PR. See `docs/VERTICAL_SLICE_MVP.md`.

---

## F. Implementation plan (phases)

1. **Foundation (this PR):** `episode_repo.py`, `generators.py`, `pipeline.py`, CLI
   `run`/`status`, tests, `runs/` ignored. Outcome: chain runs, resumes, partial-reruns,
   validates. Rollback: revert PR; reference core untouched in behavior.
2. **First episode vertical slice (this PR):** demo via `make demo` into `runs/`.
3. **Local SDXL integration:** behind `providers/` adapter; preflight capability check;
   asset_plan → real candidates; QC `assets` gate. Risk: GPU env, ext_blocked.
4. **Master narration + music library:** ElevenLabs adapter w/ idempotency+budget;
   library-first music (ADR 0006). Risk: billing, rights.
5. **DaVinci assembly:** edit_plan → Resolve scripting; assembly-before-finish (ADR 0005).
6. **Approval + private upload:** `approval.py` gates; `require_publish_approval` hook;
   private-upload-first (ADR 0008).
7. **Production Level 3:** WIP limits, job store, observability, retries.
8. **Selective Level 4:** earned by measured performance (governance `docs/39`).

Each later phase keeps provider payloads behind adapters (invariant 9) and must not be
treated as done merely because the blueprint validates (per `VALIDATION_REPORT_V2.md`).
