# PD 014-015 Owner Action Required v001

Current status: all local review preparation is complete; public release remains blocked by missing owner approvals.

Use the full review dashboard first:
`episodes/_planning/pd_014_015_owner_review.html`

Local launcher from repo root:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\open_pd_014_015_review.ps1
```

Optional local input templates:
- `episodes/PD-2026-014-lange/approvals/OWNER_APPROVAL_INPUT.template.v001.txt`
- `episodes/PD-2026-015-theranos/approvals/OWNER_APPROVAL_INPUT.template.v001.txt`

Only copy approved blocks into `OWNER_APPROVAL_INPUT.v001.txt` after the owner has actually approved the exact hashes.

## Fastest Path

If 14 Lange is approved as-is, send these three approvals back unchanged:

```text
APPROVED: PD-2026-014-lange first-cut review v001.
Video: H:/pd-media/episodes/PD-2026-014-lange/08_edit/renders/lange_premium_review_proxy_v001.mp4
Video SHA-256: sha256:0698e4294d536506c7eac40b693e911d548d23e24706d607f12f91c38d49022b
Scope: first-cut review approval only. No upload, schedule, public release, or paid narration.
```

```text
APPROVED: PD-2026-014-lange title/thumbnail v001.
Title: Can a Cop Follow You Into Your Own Home?
Thumbnail: episodes/PD-2026-014-lange/09_package/thumbnail.selected.v001.png
Thumbnail SHA-256: sha256:dae3f3a81eeb0253b077bbab5f581fc56e95d7eae9174fb8e84b18f73c6c6e97
Scope: title/thumbnail approval only. No upload, schedule, public release, or paid narration.
```

```text
APPROVED: PD-2026-014-lange may use the local review-proxy narration for release if all other gates pass.
Audio: H:/pd-media/episodes/PD-2026-014-lange/07_audio/review_proxy_mix_v001.mp3
Scope: narration decision only. No upload, schedule, or public release.
```

If 15 Theranos is approved as-is, send these four approvals back unchanged:

```text
APPROVED: PD-2026-015-theranos first-cut review v001.
Video: H:/pd-media/episodes/PD-2026-015-theranos/08_edit/renders/theranos_premium_review_proxy_v003.mp4
Video SHA-256: sha256:fa119c6af8c3f37c55f23f2885d34250f65c0b0ee2f87f73ca1cccb2ce873df9
Scope: first-cut review approval only. No upload, schedule, public release, or paid narration.
```

```text
APPROVED: PD-2026-015-theranos title/thumbnail v001.
Title: When Does a Bold Promise Become a Crime?
Thumbnail: episodes/PD-2026-015-theranos/09_package/thumbnail.selected.v001.png
Thumbnail SHA-256: sha256:f0d14264ffaf47aaa601ce7ad7eff5106dc828e30a3da8da17c31c3eca603963
Scope: title/thumbnail approval only. No upload, schedule, public release, or paid narration.
```

```text
APPROVED: PD-2026-015-theranos may use the local review-proxy narration for release if all other gates pass.
Audio: H:/pd-media/episodes/PD-2026-015-theranos/07_audio/review_proxy_mix_v001.mp3
Scope: narration decision only. No upload, schedule, or public release.
```

```text
APPROVED: PD-2026-015-theranos legal/rights review v001 for the exact package hashes in legal_rights_review_packet.v001.md.
Scope: public-release risk gate only. This does not authorize upload or schedule by itself.
Conditions: keep living-person framing record-based and neutral; no Holmes/Balwani likeness; no Theranos logo/brand mark; final delivery hash must still be checked before publish.
```

## Publish Approval Comes Later

After the approvals above are applied and preflight passes up to publish gate, send separate publish/schedule approval for each exact final delivery hash.

Lange publish/schedule approval block, only after all earlier Lange gates pass:

```text
APPROVED: PD-2026-014-lange publish/schedule for the exact final delivery hash below.
Final delivery: episodes/PD-2026-014-lange/09_package/final_delivery.v001.json
Final delivery SHA-256: sha256:3d38b5b56d9b97df568e5316814acc2526c3bfb9284f55efcf15b9c004eadc61
Initial upload must be private.
Public schedule target: 2026-06-29T12:00:00+09:00 / 2026-06-29T03:00:00Z.
Synthetic media disclosure must be set where supported.
```

Theranos publish/schedule approval block, only after all earlier Theranos gates pass, including legal/rights:

```text
APPROVED: PD-2026-015-theranos publish/schedule for the exact final delivery hash below.
Final delivery: episodes/PD-2026-015-theranos/09_package/final_delivery.v001.json
Final delivery SHA-256: sha256:d08b2adc890efcceda39df51c8b06c0d3d130d7132759887d9d8be65a0756e62
Initial upload must be private.
Public schedule target: 2026-06-30T12:00:00+09:00 / 2026-06-30T03:00:00Z.
Synthetic media disclosure must be set where supported.
```
