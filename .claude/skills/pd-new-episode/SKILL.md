---
name: pd-new-episode
description: Creates a new Prime Documentary episode workspace, IDs, manifest, topic brief, initial approvals and folder structure. Use when beginning a new video.
---

# Create New PD Episode

## Inputs

- subject or topic candidate
- optional angle
- target duration
- production tier
- target publish window
- risk notes

## Procedure

1. Read `docs/03_TOPIC_AND_PORTFOLIO_SYSTEM.md`, `docs/10_DATA_MODEL_AND_STATE_MACHINE.md`, and `docs/19_FOLDER_NAMING_AND_ARTIFACT_SPEC.md`.
2. Check semantic duplicates against existing topics and episodes.
3. Generate a topic ID and a provisional episode ID.
4. Create a structured topic brief with central question, viewer promise, surprise, stakes, audience, differentiation, feasibility, risk and score.
5. If below the configured threshold, mark `needs_reframe` instead of forcing approval.
6. Create the episode folder from the standard layout.
7. Create `manifest.json`, `events.jsonl`, initial topic artifact and approval request.
8. Validate all generated JSON against schemas.
9. Produce a concise review summary.

## Safety

- Do not overwrite an existing episode ID.
- Do not mark a topic approved without an approval record or an explicit auto-approval policy.
- Do not start paid provider jobs.

## Output

- New episode path
- IDs
- Topic score and recommendation
- Approval needed
- Next runnable stage
