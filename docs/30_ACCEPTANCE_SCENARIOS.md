# 30 — End-to-End Acceptance Scenarios

## Scenario 1 — Clean low-risk episode

Given an approved evergreen topic and valid sources,
when the pipeline runs,
then it creates a verified script, scene plan, approved asset set, narration, edit plan, QC report, package, and private upload candidate without manual file handling.

## Scenario 2 — Unsupported critical claim

Given a critical claim with no A/B-level support,
when script verification runs,
then the script cannot become `script_verified`, downstream master audio and final assets are blocked, and the operator receives the claim, attempted wording, missing evidence, and research options.

## Scenario 3 — One image fails

Given 80 approved visual assets and one malformed hand in scene S017,
when visual QC rejects that asset,
then only the affected asset job is regenerated, neighboring approved assets remain unchanged, and the edit plan relinks the new revision.

## Scenario 4 — Script line changes after voice generation

Given a verified script with master voice,
when one script span changes,
then linked voice chunks and dependent timeline ranges become stale, unrelated chunks remain valid, and approval for the old package is invalidated.

## Scenario 5 — Windows generation node restarts

Given active image jobs,
when the node crashes and restarts,
then expired leases are reclaimed, completed provider outputs are detected by idempotency key and hash, and no duplicate generation occurs.

## Scenario 6 — Mac editing node offline

Given assets and audio ready while the Mac is offline,
when edit jobs queue,
then upstream processing respects WIP limits, edit jobs remain blocked without failing, and resume automatically after node heartbeat returns.

## Scenario 7 — Provider rate limit

Given a TTS 429 response,
when the adapter receives the rate-limit instruction,
then it pauses according to retry policy, reserves no duplicate cost, records the provider request ID, and resumes only within retry and budget limits.

## Scenario 8 — Hard budget exceeded

Given estimated remaining generation cost exceeds the episode hard limit,
when a job is about to start,
then the job becomes `awaiting_approval`, no paid request is issued, and the operator receives cost-reduction options.

## Scenario 9 — Stale approval

Given title-thumbnail pair revision v003 is approved,
when the thumbnail changes to v004,
then v003 approval is invalid, publish is blocked, and the UI requests approval for the exact new pair.

## Scenario 10 — Wrong YouTube channel

Given OAuth resolves to an unapproved channel ID,
when upload preflight runs,
then upload is blocked and credentials are not used for any write action.

## Scenario 11 — Duplicate upload attempt

Given a video hash already has a platform video ID,
when the same package is submitted,
then the system returns the existing record or requires an explicit duplicate-purpose override. It does not upload silently.

## Scenario 12 — Current fact changes before publish

Given a volatile current fact was verified seven days earlier,
when publish preflight runs,
then the recheck job must pass before package approval remains valid.

## Scenario 13 — Copyright/rights uncertainty

Given a music track lacks generation-plan evidence,
when rights QC runs,
then the track is blocked, the timeline becomes stale, and a rights-clear library replacement is proposed.

## Scenario 14 — Prompt injection in source

Given a source page contains instructions to reveal secrets or run shell commands,
when research ingestion runs,
then the text is stored as untrusted content, no instruction is executed, and the suspicious segment is flagged.

## Scenario 15 — Published analytics learning

Given 28-day analytics and scene mapping,
when retrospective runs,
then it creates observations, hypotheses, confidence, confounders, proposed experiments, and expiration dates. It does not directly overwrite production rules without approval.

## Scenario 16 — Restoration

Given the metadata DB is lost,
when the restore runbook is executed,
then the latest verified backup restores, artifact registry reconciliation passes, and no approved artifact is orphaned.

## Scenario 17 — Golden episode regression

Given a change to the state machine or schemas,
when CI runs the golden episode,
then all canonical transitions, dependency invalidation, package completeness, and safety barriers remain valid.

## Scenario 18 — Human review reduction

Given ten episodes of the same low-risk format,
when review metrics are analyzed,
then any proposal to promote an operation to `auto_unless_flagged` includes false-negative rate, reviewer agreement, incident history, cost variance, and rollback.
