# EP29 hinton — PUBLISH READINESS (target 2026-07-14)

## Ready ✅ (Claude, 2026-07-05)
- **Final video**: `remotion/out/hinton_final.v001.bgm.mp4` — 11.6 min, 1080p, ElevenLabs VO forward, ducked BGM.
- **Acceptance**: `09_package/acceptance_receipt.v001.json` — **STATUS PASS, 0 hard failures**, `video_sha256` matches the file.
- **Thumbnail**: `09_package/thumbnail.selected.png` (A, 派手 grade) + 3 variants in `10_thumbnail/`.
- **Metadata**: `09_package/youtube_meta.v001.json` — title/desc/tags/category, `privacy=private`, disclosure flags, `proposed_publish_at=2026-07-14T12:00:00+09:00`.

## Gates remaining 🔒 (HUMAN — Claude will not cross these)
1. **R2 legal/rights review** signed off — `LEGAL_REVIEW_PACKET.v001.md`.
2. **Owner approvals**: first-cut, title+thumbnail, and explicit publish approval.
3. Set `youtube_meta.v001.json` → `publish_approved: true` (+ approval id).

## Then — schedule 7/14 (run only after the gates above)
Mirror `scripts/upload_schedule_arbitration_v001.py` for hinton (private upload + `publishAt`
2026-07-14, `containsSyntheticMedia=true`, `madeForKids=false`), gated on the green receipt:
```
# 1) dry-run first (no external writes)
py -3.11 scripts/upload_schedule_hinton_v001.py --dry-run
# 2) real: private upload + schedule 2026-07-14, verified against acceptance_receipt sha
py -3.11 scripts/upload_schedule_hinton_v001.py
```
The uploader must (a) confirm the file sha == `acceptance_receipt.video_sha256`, (b) upload
**private**, (c) set `publishAt` = the approved slot, (d) verify privacy/publishAt read back, and
(e) record the approval id. **Immediate public publish is not used — YouTube holds it private
until 2026-07-14, and only after the legal gate is signed.**

> Claude has prepared this to the gate. It has **not** uploaded, scheduled, or made anything public.
> Confirm the legal review + approvals, then the schedule step is one command.
