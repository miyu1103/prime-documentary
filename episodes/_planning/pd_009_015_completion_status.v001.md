# PD 009-015 Completion Status v001

Generated: 2026-06-24T20:11:28+09:00

No paid API, upload, publish, or schedule action was performed by this status pass.

Owner review dashboard: `episodes/_planning/pd_014_015_owner_review.html`

Owner review launcher: `scripts/open_pd_014_015_review.ps1`

Owner action required: `episodes/_planning/pd_014_015_owner_action_required.v001.md`

Owner approval copy packet: `episodes/_planning/pd_014_015_owner_approval_packet.v001.md`

Publish readiness preflight: `episodes/_planning/pd_014_015_publish_readiness_preflight.v001.json` (public_release_allowed=False)

Owner approval apply helper: `scripts/prepare_lange_theranos_approvals.py`; dry-run: `episodes/_planning/pd_014_015_prepare_owner_approvals.dry_run.v001.json`

Owner approval input templates:
- `episodes/PD-2026-014-lange/approvals/OWNER_APPROVAL_INPUT.template.v001.txt`
- `episodes/PD-2026-015-theranos/approvals/OWNER_APPROVAL_INPUT.template.v001.txt`

After-owner-approval runbook: `episodes/_planning/pd_014_015_after_owner_approval_runbook.v001.md`

Safety script tests: `py -3.11 -m unittest tests.test_lange_theranos_safety_scripts -v`

9-15 readiness check: `episodes/_planning/pd_009_015_readiness_check.latest.md` (`REVIEW_READY_BLOCKED_BY_APPROVALS`)

| Episode | State | Approvals | Review Request | Risk Packet | Remaining Gate |
|---|---:|---|---|---|---|
| PD-2026-009-timbs | scheduled | APR-0001, APR-0002 | - | - | none_observed |
| PD-2026-010-kelo | scheduled | APR-0001, APR-0002 | - | - | none_observed |
| PD-2026-011-mahanoy | scheduled | APR-0001, APR-0002 | - | - | none_observed |
| PD-2026-012-arbitration | scheduled | APR-0001, APR-0002 | - | - | none_observed |
| PD-2026-013-king | scheduled | APR-0001, APR-0002 | - | - | none_observed |
| PD-2026-014-lange | edit_review | APR-0001 | episodes/PD-2026-014-lange/09_package/OWNER_REVIEW_REQUEST.v001.json | episodes/PD-2026-014-lange/09_package/prepublish_review_packet.v001.json | owner first-cut/title-thumbnail/final narration; publish approval not granted |
| PD-2026-015-theranos | edit_review | APR-0001 | episodes/PD-2026-015-theranos/09_package/OWNER_REVIEW_REQUEST.v001.json | episodes/PD-2026-015-theranos/09_package/legal_rights_review_packet.v001.json | owner first-cut/title-thumbnail/final narration; legal/rights review required; publish approval not granted |

## Practical Next Actions

1. Review 14 Lange exact video/title/thumbnail using `episodes/PD-2026-014-lange/09_package/OWNER_REVIEW_REQUEST.v001.md` and `prepublish_review_packet.v001.md`.
2. Review 15 Theranos exact video/title/thumbnail using `episodes/PD-2026-015-theranos/09_package/OWNER_REVIEW_REQUEST.v001.md` and `legal_rights_review_packet.v001.md`.
3. If approved, convert the corresponding `approval_drafts.v001.json` entries into real APR files only after explicit owner approval.
4. Do not publish or schedule Theranos until legal/rights review is recorded for the exact package hash.
5. Do not publish or schedule either 14 or 15 until the separate publish/schedule block includes the exact `final_delivery.v001.json` SHA-256.

## Publish/Schedule Hash Targets

- PD-2026-014-lange final delivery: `episodes/PD-2026-014-lange/09_package/final_delivery.v001.json`
- PD-2026-014-lange final delivery SHA-256: `sha256:3d38b5b56d9b97df568e5316814acc2526c3bfb9284f55efcf15b9c004eadc61`
- PD-2026-015-theranos final delivery: `episodes/PD-2026-015-theranos/09_package/final_delivery.v001.json`
- PD-2026-015-theranos final delivery SHA-256: `sha256:d08b2adc890efcceda39df51c8b06c0d3d130d7132759887d9d8be65a0756e62`

## Current Publish Blockers

### PD-2026-014-lange
- approval_present:first_cut:APR-0002: episodes/PD-2026-014-lange/approvals/APR-0002.json
- approval_present:title_thumbnail:APR-0003: episodes/PD-2026-014-lange/approvals/APR-0003.json
- approval_present:narration_release:APR-0004: episodes/PD-2026-014-lange/approvals/APR-0004.json
- approval_present:publish_schedule:APR-0005: episodes/PD-2026-014-lange/approvals/APR-0005.json

### PD-2026-015-theranos
- approval_present:first_cut:APR-0002: episodes/PD-2026-015-theranos/approvals/APR-0002.json
- approval_present:title_thumbnail:APR-0003: episodes/PD-2026-015-theranos/approvals/APR-0003.json
- approval_present:narration_release:APR-0004: episodes/PD-2026-015-theranos/approvals/APR-0004.json
- approval_present:legal_rights:APR-0005: episodes/PD-2026-015-theranos/approvals/APR-0005.json
- approval_present:publish_schedule:APR-0006: episodes/PD-2026-015-theranos/approvals/APR-0006.json
