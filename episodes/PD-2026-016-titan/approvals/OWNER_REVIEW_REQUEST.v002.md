# OWNER RE-APPROVAL REQUEST — PD-2026-016-titan script v002

- **Requested:** 2026-06-27 by local-claude-code
- **Why a new approval is needed:** APR-0001 is bound to the **v001** annotated content hash (`sha256:e2e109f574c41a64170dc0a848eabcb2cb70056f3855365f2b86f0f98c2594b9`). The two corrections below change content, so v001 approval no longer covers it (rules/12). **This is a request, not an approval.**
- **Basis:** `01_research/fact_recheck.v001.md` (2026-06-27 independent web re-verification of all 14 claims).

## What changed (v001 → v002) — exactly two edits

### 1. Quote fidelity (script) — SPN-0004 / `script.en` line 22
The cold-open / title quote is now verbatim to the 2022 David Pogue (CBS) on-record wording.

- **Before:** "He said: at some point, safety **is just** pure waste."
- **After:**  "He said: at some point, safety **just is** pure waste."
- Title card "Pure Waste" unchanged. No other span changed.

### 2. Evidence-ledger correction (research) — CLM-0005 / SRC-0005
Corrected a viewport-vs-hull conflation. The ~1,300 m rating was the **acrylic viewport**, not the carbon-fiber hull (the hull concern was carbon-fiber flaws + lack of non-destructive testing).

- **Script impact: NONE.** No script span ever asserted the 1,300 m number; the script's wording (lines 78, 113, 123) was already accurate and attributed. This is a ledger-accuracy fix only.

## Revisions in this bundle
| Artifact | New revision | Note |
|---|---|---|
| `03_script/script.annotated.v002.json` | v002 | **content_hash to bind: `sha256:843c8f36fd660eea176c5d32d9965322da13e97fcaaca4f11056536064d94920`** |
| `03_script/script.en.v002.md` | v002 | quote word-order only |
| `01_research/claims.v002.json` | v002 | CLM-0005 corrected |
| `01_research/sources.v002.json` | v002 | SRC-0005 aligned |

v001 artifacts are retained immutable. Manifest approved pointers and APR-0001 are unchanged until you sign off below.

## What is NOT changed
- Thesis, structure, all dignity guardrails, every other claim and span, all shotlist/asset mappings, all 76 hero images. No paid API, upload, render, or publish action was taken.

## Standing gates still required regardless of this approval
First-cut · title/thumbnail · **final same-day pre-publish fact re-check** · public scheduling (per APR-0001 conditions, R2).

---

## Owner decision (fill in)

```
decision:            approved | rejected | changes_requested
decided_by:          owner
decided_at:          <ISO-8601>
binds_to_hash:       sha256:843c8f36fd660eea176c5d32d9965322da13e97fcaaca4f11056536064d94920
notes:               <optional>
```

On `approved`, the next mechanical steps (I will do them on your go): write `approvals/APR-0002.json`, set `manifest.active_revisions.{script,script_qc,claims,sources}` to v002, mark the v002 annotated artifact `approved`, and log the event. Nothing publishes.
