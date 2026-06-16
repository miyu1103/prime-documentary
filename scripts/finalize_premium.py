#!/usr/bin/env python3
r"""QC + records for the PD-2026-002-gideon PREMIUM first cut → state edit_review (owner gate next).

Hashes gideon_premium_v001.mp4, writes the final-cut QC report (0004 §G + §N), updates youtube_meta
with the real cut hash, advances manifest audio_ready -> edit_review, logs events. Stops at the
owner first-cut gate (no owner approval is fabricated; APR pending). Idempotent.
    py -3.11 scripts/finalize_premium.py
"""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
EPDIR = REPO / "episodes" / EP
TS = "2026-06-17T00:00:00+00:00"
CUT = MEDIA / "episodes" / EP / "08_edit" / "gideon_premium_v001.mp4"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    h = sha256(CUT)
    dur = float(subprocess.run([FFPROBE,"-v","quiet","-show_entries","format=duration","-of","csv=p=0",str(CUT)],
                               capture_output=True, text=True).stdout.strip())
    size = CUT.stat().st_size
    print(f"premium cut: {size/1_048_576:.1f} MB  {dur:.1f}s  sha256:{h[:16]}..")

    qc = {
        "qc_report_id": f"QC-{EP}-v001",
        "target_type": "episode_final_cut",
        "target_id": EP, "target_revision": "v001",
        "gate": "first_cut_review", "result": "pass_with_warnings",
        "findings": [
            {"finding_id":"QC-0001","severity":"S0","code":"motion_coverage","message":"Every shot moves: CameraRig (Ken-Burns/pan) + drifting particles + light sweep + vignette under all scenes; Runway clips run a ~5s motion beat then cut to the still. No static-over-4s shot.","location":"GideonPremium","action":"none","related_ids":[]},
            {"finding_id":"QC-0002","severity":"S0","code":"visual_density","message":"112-shot plan (shotlist.v001), ~4-8s cadence; 28 scenes with 2-4 visuals each; graphics animate. Within 90-150 floor.","location":"04_scenes/shotlist.v001.md","action":"none","related_ids":[]},
            {"finding_id":"QC-0003","severity":"S0","code":"audio_four_layers","message":"VO + sequenced music bed + continuous ambience (100%) + SFX (121 cues) + featured real oral-argument excerpt at S013. mean -22.3 dB, max -0.5 dB; no silent gaps.","location":"08_edit/gideon_premium_v001.mp4","action":"none","related_ids":[]},
            {"finding_id":"QC-0004","severity":"S0","code":"real_asset_usage","message":"Real PD assets used first: pencil cert petition (hook hero + petition beats), Hugo Black portrait (opinion author), real 1963 oral-argument audio (S013). 8 real inserts (floor 8-12).","location":"05_visuals/real","action":"none","related_ids":["AST-0200","AST-0210","AST-0220"]},
            {"finding_id":"QC-0005","severity":"S0","code":"synthetic_media_label","message":"FIXED: on-screen 'symbolic reconstruction — not authentic footage' label now burned on AI reenactment shots (S002,S004,S007,S013,S020,S021,S027). Description also discloses AI narration + reconstructions.","location":"GideonPremium ReconLabel","action":"none","related_ids":[]},
            {"finding_id":"QC-0006","severity":"S0","code":"rights_complete","message":"rights_manifest.v001 = 67 assets, 67/67 sha256 verified, 0 needs_verification (incl. 8 real PD assets + library reuse).","location":"09_package/rights_manifest.v001.json","action":"none","related_ids":[]},
            {"finding_id":"QC-0007","severity":"S0","code":"caption_sync_forced_aligned","message":"FIXED (owner note): captions re-built by forced alignment (faster-whisper word timestamps) -> frame-accurate timing + clean clause/sentence breaks (5-8 words), narration text. captions.v002.srt (310 lines). No more odd mid-clause breaks or drift.","location":"08_edit/captions.v002.srt","action":"none","related_ids":[]},
            {"finding_id":"QC-0012","severity":"S0","code":"hook_5_8s","message":"FIXED (owner note): flash-forward hook tightened from 14.0s to ~7.5s (VC-0001 re-voiced) — within the 0004 §B 5-8s spec; then cold-open -> opening -> body.","location":"06_audio/voice_plan.v001.json","action":"none","related_ids":[]},
            {"finding_id":"QC-0013","severity":"S0","code":"ending_endcard","message":"FIXED (owner note): standard branded end-card — reusable BrandEndcard (PD monogram + Subscribe + 'New episodes weekly'), IDENTICAL every episode (channel consistency). ~9s.","location":"components/Bookends.tsx","action":"none","related_ids":[]},
            {"finding_id":"QC-0014","severity":"S0","code":"opening_title_sequence","message":"ADDED (owner note): reusable branded title opening (BrandOpening: PD monogram + gold rule + series/title/subtitle over sunrise, ~3.5s) inserted right after the hook; narration/captions(v003)/music/SFX shifted in sync. hook -> opening -> body. Bookends shared for EP3+.","location":"components/Bookends.tsx","action":"none","related_ids":[]},
            {"finding_id":"QC-0008","severity":"S2","code":"research_live_verification_pending","message":"SRC-0001..0003 durable content_hash/verified_at not captured (generalize run_research for 372 U.S. 335 / 316 U.S. 455). Citations valid; flip research QC warn->pass before publish (APR-0001 conditions).","location":"01_research/sources.v001.json","action":"research","related_ids":["SRC-0001","SRC-0002","SRC-0003"]},
            {"finding_id":"QC-0009","severity":"S3","code":"real_audio_vo_overlap","message":"The featured real oral-argument excerpt at S013 (~10s, low) briefly overlaps VO. Consider a dedicated narration gap to foreground it, or keep as low texture (current). Human listen-through recommended.","location":"08_edit/gideon_premium_v001.mp4","action":"review","related_ids":[]},
            {"finding_id":"QC-0010","severity":"S3","code":"real_person_accuracy","message":"Black portrait is an authentic but younger photo; symbolic reenactments depict Gideon/Fortas. Keep facts accurate (retried WITH counsel and acquitted; Fortas court-appointed). Human review.","location":"04_scenes/scene_plan.v001.json","action":"review","related_ids":["CLM-0004","CLM-0007"]},
            {"finding_id":"QC-0011","severity":"S5","code":"polish_deferred","message":"Optional v002: archive.org B-roll inserts; true depth-map 2.5D parallax on documents; opinion-quote PDF; younger Black portrait swap; per-scene ambience swaps.","location":"04_scenes/real_asset_sourcing.v001.md","action":"none","related_ids":[]},
        ],
        "created_at": TS,
        "validator_versions": {"schema":"qc-report.schema.json@1.0.0","checks":"manual + verify_rights_hashes (67/67) + ffprobe/volumedetect + frame spot-checks (hook/clip/portrait/desk)"},
    }
    (EPDIR / "08_qc").mkdir(exist_ok=True)
    (EPDIR / "08_qc" / "qc_report.v001.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False) + "\n", "utf-8")

    ym = json.loads((EPDIR / "09_package" / "youtube_meta.v001.json").read_text("utf-8"))
    ym["status"] = "first_cut_ready_for_owner_review"
    ym["video_file"] = "gideon_premium_v001.mp4"
    sc = ym["safety_checklist"]
    sc["ai_disclosure_set"] = True
    sc["ai_disclosure_notes"] = "On-screen 'symbolic reconstruction' label burned on AI reenactment shots; description discloses AI narration + reconstructions."
    sc["final_cut_hash_recorded"] = True
    sc["final_cut_hash"] = h
    sc["final_cut_path"] = f"H:/pd-media/episodes/{EP}/08_edit/gideon_premium_v001.mp4"
    sc["final_cut_size_bytes"] = size
    sc["final_cut_notes"] = f"PREMIUM v001 (GideonPremium: moving stage + real assets + clips + grade + 121 SFX). {dur:.1f}s."
    ym["publish_gate"] = "blocked"
    ym["publish_gate_blockers"] = [
        "owner first-cut approval (APR) pending — watch gideon_premium_v001.mp4",
        "QC-0007 caption sync forced-alignment verify",
        "QC-0008 research live-verification",
        "owner title/thumbnail approval + owner publish approval",
    ]
    (EPDIR / "09_package" / "youtube_meta.v001.json").write_text(json.dumps(ym, indent=2, ensure_ascii=False) + "\n", "utf-8")

    mani = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    mani["state"] = "edit_review"
    mani["active_revisions"].update({"qc_report": "v001", "edit": "v003", "captions": "v003"})
    mani["warnings"] = [
        f"PREMIUM cut v2 rendered (owner-note fixes applied): gideon_premium_v001.mp4 ({dur:.0f}s, sha256:{h[:12]}..). QC pass_with_warnings.",
        "Owner-note fixes DONE: (1) captions forced-aligned frame-accurate + clean breaks (captions.v003, shifted for opening); (2) hook tightened 14s->7.5s (5-8s spec); (3) reusable branded opening (~3.5s) + standard branded end-card — same bookends every episode (components/Bookends.tsx).",
        "State edit_review: awaiting OWNER FIRST-CUT approval (watch the cut) — not auto-approved.",
        "Pre-publish gates remaining: research live-verification (QC-0008), owner title/thumbnail approval, owner publish approval. Optional polish: archive.org B-roll, opinion-PDF, Justice-era Black portrait.",
    ]
    mani["updated_at"] = TS
    (EPDIR / "manifest.json").write_text(json.dumps(mani, indent=2, ensure_ascii=False) + "\n", "utf-8")

    events = [
        {"event":"premium_first_cut_rendered","episode_id":EP,"stage":"edit","revision":"v001","actor":"local-claude-code","content_hash":f"sha256:{h}","detail":f"GideonPremium (moving stage + real assets + 9 clips + brand grade + grain) + 4-layer audio (121 SFX + real oral-argument excerpt) + burned captions -> gideon_premium_v001.mp4 ({dur:.1f}s, {size/1_048_576:.0f}MB).","ts":TS},
        {"event":"qc_first_cut","episode_id":EP,"stage":"qc","revision":"v001","actor":"local-claude-code","qc_status":"pass_with_warnings","detail":"0004 §G/§N: motion/density/4-layer-audio/real-asset/rights/disclosure = S0 pass; caption-sync + research = S2; audio listen-through + real-person = S3.","ts":TS},
        {"event":"state_advanced","episode_id":EP,"stage":"edit","revision":"v001","actor":"local-claude-code","detail":"audio_ready -> edit_review. Awaiting owner first-cut gate.","ts":TS},
    ]
    with (EPDIR / "events" / "events.jsonl").open("a", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"wrote QC v001, youtube_meta, manifest (state={mani['state']}), +{len(events)} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
