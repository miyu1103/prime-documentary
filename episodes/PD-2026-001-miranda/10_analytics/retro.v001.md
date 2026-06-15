# Retro — PD-2026-001-miranda (v001)

First episode **shipped and published** — the hardest milestone is cleared. This retro captures what
slowed us down and what drifted, so episode 2 is **higher quality in less time**. Feeds the learning
loop (CLAUDE.md §1; decisions/0006 §I).

## What shipped
- Public on YouTube (owner-approved cut). Narration (Brian), 21 music + 22 SFX library, real images
  wired into 14 scenes, thumbnail (concept A + Midjourney bg), youtube_meta v002, APR-0002 (title +
  thumbnail). ~9:53.

## 課題 (issues this time)

### 1. Provenance / state drift (biggest process gap)
- `manifest.json` is **stuck at `scene_planned`** with only `APR-0001`, although audio, edit (v013),
  package, **APR-0002**, and **publish** all happened. The manifest is supposed to be the state
  source of truth (CLAUDE.md §5/§9) — it no longer reflects reality.
- `events.jsonl` is **incomplete/sloppy**: late events have no `ts`/`stage` ("? | ?"); missing
  `edit_assembly`, `first_cut_approved`, `publish_approved`, `uploaded`, `published`.
- **`APR-0003` (first-cut) was never recorded** — the owner approved the cut verbally, but no
  approval artifact/hash was written. Publish happened without a recorded first-cut/publish approval.
- → Hurts reproducibility, audit trail, and the learning loop (we can't cleanly attribute results).

### 2. Safety/quality gates effectively bypassed under time pressure
- **No `rights_manifest.v00x.json` exists** — yet the publish-gate (decision §N) requires a complete
  rights manifest (per-asset `rights_basis`/`source`/`verified_at`) before publish. It was skipped.
- **Research QC warn unresolved**: `SRC-0001 live content not captured (no durable hash); recheck
  before publish` is still open in the (stale) manifest.
- **No final-cut QC re-run**: the only `qc_report` is `v001` from the scene-plan stage
  (`pass_with_warnings`); the assembled video was not QC'd against the §9 checklist as a recorded gate.
- Risk is low (PD-only assets, AI disclosure shown), but the **discipline drifted** — exactly what the
  constitution guards against.

### 3. Production time-sinks
- **Assembly iterated v010 → v013** (subtitle sync, BGM fix, image-wiring, tpad/preset fixes) =
  the main time drain — built then re-fixed instead of locked-first.
- **Coded-animatic "しょぼい" detour**: time spent polishing placeholder SVG motion before pivoting
  to real assets. The animatic is only a timing proxy, not the deliverable.
- **Strategy interleaved with production**: a large, valuable design sprint (decisions 0004–0006) ran
  *during* production = context-switching.

## 改善策 (episode 2: quality up, time down)

### Process
1. **Drive transitions through the state machine** (`pd-run-pipeline` / `pd-resume`), keeping
   `manifest.json` + `events.jsonl` in sync at every stage: entry conditions → artifact rev → gate
   pass → **APR at each gate (exact hash)** → event. No ad-hoc stage jumps.
2. **Do not bypass publish gates.** Complete `rights_manifest.v001.json`, resolve research QC, run a
   **final-cut QC** against decision §N — all green — *before* publish. The publish-preflight hook
   must actually block.
3. **Lock structure + storyboard + asset list BEFORE assembling** (0004 §A) → one assembly pass, not
   thirteen. This is the single biggest time saver.

### Quality (per 0004/0005/0006)
4. **Reuse the libraries** (music/SFX/ambience, Remotion components, ThumbConcept, Pino) — ep2
   doesn't rebuild them.
5. **Skip the coded-animatic-as-deliverable**: go straight to real assets (Midjourney + PD footage →
   `ClipProof`) per the standard; coded art is fallback only.
6. **Hit the abundance floors** (0004 §E2): ≥8–12 real inserts, ≥6–10 motion clips, 60–100+ SFX,
   100% ambience, 90–150 shots, flash-forward 5–8s hook.
7. **Separate strategy from production**: design is locked (0001–0006). Ep2 = pure execution.

### Speed
8. **Batch the automatable steps** (narration, SFX, music-select, assembly) and stop only at the four
   human gates (script, first-cut, title/thumbnail, publish).
9. **Buffer**: aim to keep a finished episode in reserve so cadence never breaks (0006 §F).

## EP1 cleanup (retroactive — make the record honest)
Now that it's public, reconcile the trail so the learning loop has clean data:
- Write `rights_manifest.v001.json` (every shipped asset + `rights_basis`/`source`/`verified_at`).
- Record `APR-0003` (first-cut, owner-approved, exact final-cut hash) + a `publish` approval/record.
- Advance `manifest.json` state → `published` (+ `published_at`, video id) and append the missing
  `events.jsonl` entries (edit_assembly, first_cut_approved, publish_approved, published).
- Resolve or explicitly accept the `SRC-0001` research warn with a note.

## Targets for ep2
- **Time:** materially less than ep1 (factory + libraries already built; one assembly pass).
- **Quality:** meets all 0004 floors; flash-forward hook; richer real-asset + motion + sound.
- **Discipline:** manifest/events/approvals stay in sync; publish only on an all-green preflight.
