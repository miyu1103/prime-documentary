#!/usr/bin/env python3
r"""Finalize PD-2026-002-gideon to package_ready (just before publish/upload).

Owner authorized everything ("すべて承認しますので投稿できる手前まで進めてください", 2026-06-16),
so this records the first-cut and title/thumbnail approvals, writes the final-cut QC report,
advances the manifest audio_ready -> package_ready, updates youtube_meta with the real final-cut
+ thumbnail hashes, and logs events. It does NOT cross the publish/upload boundary.

Deterministic + idempotent. Hashes are computed from the real rendered files.
    py -3.11 scripts/finalize_gideon.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
EPDIR = REPO / "episodes" / EP
TS = "2026-06-16T06:00:00+00:00"

CUT = MEDIA / "episodes" / EP / "08_edit" / "gideon_v001.mp4"
THUMB2 = REPO / "remotion/out/thumb_gideon_concept2.png"
THUMB3 = REPO / "remotion/out/thumb_gideon_concept3.png"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def probe_dur(p: Path) -> float:
    import subprocess
    r = subprocess.run([r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe",
                        "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def main() -> int:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for p in (CUT, THUMB2, THUMB3):
        if not p.exists():
            raise FileNotFoundError(p)
    cut_hash, cut_dur, cut_size = sha256(CUT), probe_dur(CUT), CUT.stat().st_size
    t2_hash, t3_hash = sha256(THUMB2), sha256(THUMB3)
    print(f"final cut: {cut_size/1_048_576:.1f} MB  {cut_dur:.1f}s  sha256:{cut_hash[:16]}..")

    # ── 1. final-cut QC report ───────────────────────────────────────────────────────────────
    qc = {
        "qc_report_id": f"QC-{EP}-v001",
        "target_type": "episode_final_cut",
        "target_id": EP,
        "target_revision": "v001",
        "gate": "final_cut_review",
        "result": "pass_with_warnings",
        "findings": [
            {"finding_id": "QC-0001", "severity": "S0", "code": "scene_coverage",
             "message": "All 28 scenes (S001-S028) render on the narration timeline; animatic length 694.4s == narration master; no orphan scenes; within 12-min format.",
             "location": "04_scenes/scene_plan.v001.json, 08_edit/timing.v001.json", "action": "none", "related_ids": []},
            {"finding_id": "QC-0002", "severity": "S0", "code": "promise_payoff",
             "message": "Cold-open hook (no lawyer; 9-0) is paid off: ruling 9-0/Black at S015, Betts overruled S018, double-win S020-S027. Title/thumbnail match content (no clickbait).",
             "location": "08_edit/gideon_v001.mp4", "action": "none", "related_ids": ["S001", "S015", "S018"]},
            {"finding_id": "QC-0003", "severity": "S0", "code": "rights_manifest_complete",
             "message": "rights_manifest.v001 = 59 assets, all licensed + hashed; verify_rights_hashes.py reports 59/59 OK, 0 needs_verification (incl. library-reuse music/sfx/ambience and narration master).",
             "location": "09_package/rights_manifest.v001.json", "action": "none", "related_ids": []},
            {"finding_id": "QC-0004", "severity": "S0", "code": "captions_present",
             "message": "captions.v001.srt burned (narration-timed). Video 1920x1080 h264 + mono aac; audio mean -22.8 dB, max -1.0 dB (not silent, not clipping).",
             "location": "08_edit/captions.v001.srt", "action": "none", "related_ids": []},
            {"finding_id": "QC-0005", "severity": "S2", "code": "synthetic_media_label_missing",
             "message": "Description carries the AI/synthetic-media disclosure, but reenactment scenes do not yet burn an on-screen 'symbolic reconstruction — not authentic footage' label (EP1 carried one). Add the on-screen label to S002/S004/S007/S009/S013/S020/S021/S027 before publish (invariant 11).",
             "location": "remotion (SceneVisual reenactment)", "action": "repair",
             "related_ids": ["S002", "S004", "S007", "S009", "S013", "S020", "S021", "S027"]},
            {"finding_id": "QC-0006", "severity": "S2", "code": "research_live_verification_pending",
             "message": "SRC-0001..0003 durable content_hash/verified_at not captured (generalize run_research for 372 U.S. 335 / 316 U.S. 455). Citations are valid; flip research QC warn->pass before publish (carried from APR-0001 conditions).",
             "location": "01_research/sources.v001.json", "action": "research", "related_ids": ["SRC-0001", "SRC-0002", "SRC-0003"]},
            {"finding_id": "QC-0007", "severity": "S2", "code": "real_person_review_required",
             "message": "Clarence Earl Gideon, Abe Fortas, Hugo Black depicted symbolically (faces hidden / silhouette). Human review: must keep facts accurate (Gideon retried WITH counsel and acquitted; Fortas court-appointed) and not present AI visuals as authentic records.",
             "location": "04_scenes/scene_plan.v001.json", "action": "review", "related_ids": ["CLM-0004", "CLM-0006", "CLM-0007"]},
            {"finding_id": "QC-0008", "severity": "S3", "code": "audio_human_listen_through",
             "message": "Audio is layered (narration + 9-region music bed + subliminal ambience, never-silent). A human listen-through for ducking/levels/region crossfades is recommended before publish; loudnorm to -14 LUFS optional.",
             "location": "08_edit/gideon_v001.mp4", "action": "review", "related_ids": []},
            {"finding_id": "QC-0009", "severity": "S5", "code": "polish_pass_deferred",
             "message": "v002 polish (non-blocking): SFX one-shots + per-scene ambience swaps from audio_cue_sheet.v001.md; Runway motion clips (9 routed) as B-roll inserts; 4 library SFX gaps (pencil-scratch/cell-door/stone/heartbeat) use documented nearest substitutes.",
             "location": "06_audio/audio_cue_sheet.v001.md", "action": "none", "related_ids": []},
        ],
        "created_at": TS,
        "validator_versions": {"schema": "qc-report.schema.json@1.0.0",
                               "checks": "manual + verify_rights_hashes.py + ffprobe/volumedetect + frame spot-checks (S001/S008/S015/S024)"},
    }
    (EPDIR / "08_qc").mkdir(exist_ok=True)
    (EPDIR / "08_qc" / "qc_report.v001.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")

    # ── 2. approvals (owner authorized everything up to just-before-publish) ──────────────────
    def approval(aid, ttype, tid, notes, conditions, ev):
        return {
            "schema_version": "1.0.0", "approval_id": aid, "episode_id": EP,
            "target_type": ttype, "target_id": tid, "target_revision": "v001",
            "decision": "approved_with_conditions" if conditions else "approved",
            "requested_at": TS, "requested_by": "local-claude-code",
            "decided_at": TS, "decided_by": "owner",
            "notes": notes, "conditions": conditions, "expires_at": None,
            "evidence_snapshot_ref": ev,
        }

    apr2 = approval(
        "APR-0002", "edit", "gideon_v001.mp4",
        ("Owner approved the first cut (blanket 'すべて承認' / proceed-to-just-before-publish, 2026-06-16). "
         f"Bound to final-cut content_hash sha256:{cut_hash} ({cut_dur:.1f}s). Re-approval required if the cut is re-rendered."),
        ["Burn on-screen 'symbolic reconstruction' label on reenactment scenes before public publish (QC-0005).",
         "Human audio listen-through + optional loudnorm -14 LUFS before publish (QC-0008)."],
        f"artifact://episodes/{EP}/08_edit/gideon_v001.mp4")
    apr3 = approval(
        "APR-0003", "package", "title_thumbnail",
        ("Owner approved title + A/B thumbnails (blanket approval, 2026-06-16). "
         f"Title 'He Had No Lawyer — So He Beat the Supreme Court'. Thumbnails rendered: "
         f"concept2 sha256:{t2_hash[:16]}.., concept3 sha256:{t3_hash[:16]}.. (1280x720 brand component)."),
        ["Run YouTube Studio Test & Compare A/B (concept2 vs concept3); keep the winner."],
        "artifact://episodes/PD-2026-002-gideon/09_package/packaging_concept.v001.md")
    for apr in (apr2, apr3):
        (EPDIR / "approvals" / f"{apr['approval_id']}.json").write_text(
            json.dumps(apr, indent=2, ensure_ascii=False) + "\n", "utf-8")

    # ── 3. update youtube_meta with real final-cut + thumbnail hashes ─────────────────────────
    ym = json.loads((EPDIR / "09_package" / "youtube_meta.v001.json").read_text("utf-8"))
    ym["status"] = "package_ready_pending_publish"
    ym["video_file"] = "gideon_v001.mp4"
    ym["first_cut_approved"] = True
    ym["first_cut_approval_ref"] = "APR-0002"
    ym["title_thumbnail_approved"] = True
    ym["title_thumbnail_approval_ref"] = "APR-0003"
    ym["thumbnail_ab_set"][0]["rendered_file"] = "remotion/out/thumb_gideon_concept2.png"
    ym["thumbnail_ab_set"][0]["rendered_hash"] = f"sha256:{t2_hash}"
    ym["thumbnail_ab_set"][0]["status"] = "rendered_approved"
    ym["thumbnail_ab_set"][1]["rendered_file"] = "remotion/out/thumb_gideon_concept3.png"
    ym["thumbnail_ab_set"][1]["rendered_hash"] = f"sha256:{t3_hash}"
    ym["thumbnail_ab_set"][1]["status"] = "rendered_approved"
    sc = ym["safety_checklist"]
    sc["final_cut_hash_recorded"] = True
    sc["final_cut_hash"] = cut_hash
    sc["final_cut_path"] = f"H:/pd-media/episodes/{EP}/08_edit/gideon_v001.mp4"
    sc["final_cut_size_bytes"] = cut_size
    sc["final_cut_notes"] = f"v001 GideonAnimatic (stills+Ken Burns) + layered audio + burned SRT. {cut_dur:.1f}s."
    sc["ai_disclosure_set"] = False  # honest: on-screen reconstruction label still pending (QC-0005)
    sc["ai_disclosure_notes"] = "Description discloses AI narration + symbolic reconstructions; on-screen reconstruction LABEL on reenactment scenes still pending before publish (QC-0005)."
    ym["publish_gate"] = "blocked"
    ym["publish_gate_blockers"] = [
        "QC-0005: burn on-screen 'symbolic reconstruction' label on reenactment scenes",
        "QC-0006: capture research durable content hashes (live-verification)",
        "QC-0008: human audio listen-through",
        "owner publish approval (APR-0004) + upload not yet performed",
    ]
    ym["pending_approvals_required"] = [
        "APR-0004: owner PUBLISH approval for gideon_v001.mp4 (final pre-upload gate)"]
    (EPDIR / "09_package" / "youtube_meta.v001.json").write_text(json.dumps(ym, indent=2, ensure_ascii=False) + "\n", "utf-8")

    # ── 4. advance manifest -> package_ready ──────────────────────────────────────────────────
    mani = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    mani["state"] = "package_ready"
    mani["active_revisions"].update({
        "audio_cue_sheet": "v001", "qc_report": "v001", "youtube_meta": "v001", "edit": "v001",
    })
    for a in ("APR-0002", "APR-0003"):
        if a not in mani["approvals"]:
            mani["approvals"].append(a)
    mani["warnings"] = [
        "package_ready: first cut rendered (gideon_v001.mp4, 694.4s) + QC pass_with_warnings + rights complete (59/59). Owner-approved first-cut (APR-0002) + title/thumbnail (APR-0003).",
        "PRE-PUBLISH GATES (not crossed): on-screen reconstruction label (QC-0005); research live-verification (QC-0006); human audio listen-through (QC-0008); owner publish approval APR-0004 + upload.",
    ]
    mani["blockers"] = []
    mani["updated_at"] = TS
    (EPDIR / "manifest.json").write_text(json.dumps(mani, indent=2, ensure_ascii=False) + "\n", "utf-8")

    # ── 5. append events ──────────────────────────────────────────────────────────────────────
    events = [
        {"event": "audio_cue_sheet_authored", "episode_id": EP, "stage": "audio", "revision": "v001",
         "actor": "local-claude-code", "detail": "SFX/ambience/music cue sheet bound to real library IDs; expansion->strain = library reuse MUS-0007 (owner-approved).", "ts": TS},
        {"event": "rights_manifest_completed", "episode_id": EP, "stage": "package", "revision": "v001",
         "actor": "local-claude-code", "detail": "59 assets, all hashed+verified (59/59 OK); narration master hash + library-reuse lines added.", "ts": TS},
        {"event": "first_cut_rendered", "episode_id": EP, "stage": "edit", "revision": "v001",
         "actor": "local-claude-code", "content_hash": f"sha256:{cut_hash}",
         "detail": f"GideonAnimatic (Remotion stills+Ken Burns, 20832f) + layered audio + burned SRT -> gideon_v001.mp4 ({cut_dur:.1f}s, {cut_size/1_048_576:.0f}MB).", "ts": TS},
        {"event": "first_cut_approved", "episode_id": EP, "stage": "edit", "revision": "v001",
         "actor": "local-claude-code", "approval_id": "APR-0002", "decided_by": "owner", "content_hash": f"sha256:{cut_hash}", "detail": "Owner blanket-approved first cut. State -> edit_review.", "ts": TS},
        {"event": "title_thumbnail_approved", "episode_id": EP, "stage": "package", "revision": "v001",
         "actor": "local-claude-code", "approval_id": "APR-0003", "decided_by": "owner", "detail": "Title + A/B thumbnails (concept2/concept3) rendered + approved.", "ts": TS},
        {"event": "qc_final_cut", "episode_id": EP, "stage": "qc", "revision": "v001",
         "actor": "local-claude-code", "qc_status": "pass_with_warnings", "detail": "Final-cut QC: 4xS0 pass, 3xS2 + 1xS3 pre-publish, 1xS5 deferred.", "ts": TS},
        {"event": "state_advanced", "episode_id": EP, "stage": "package", "revision": "v001",
         "actor": "local-claude-code", "detail": "audio_ready -> package_ready (just before publish). Publish/upload NOT performed (awaits APR-0004 + pre-publish gates).", "ts": TS},
    ]
    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"wrote QC, APR-0002/0003, youtube_meta, manifest (state={mani['state']}), +{len(events)} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
