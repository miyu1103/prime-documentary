"""EP38 kidsforcash — build the YouTube publish package (owner GO 2026-07-19).

Writes youtube_meta.v001.json + final_delivery.v001.json + approvals/APR-0001.json,
all bound to the exact v004_ae render + CTR thumbnail sha256. Deterministic (no
wall-clock in the artifacts). Owner accepted the 3 deviations (runtime_band,
sound_layers, preflight_receipt) after watching the cut.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
EP = "PD-2026-038-kidsforcash"
PKG = ROOT / "episodes" / EP / "09_package"
APPROVALS = ROOT / "episodes" / EP / "approvals"

VIDEO = "episodes/PD-2026-038-kidsforcash/08_edit/kidsforcash_final_bgm.v004_ae.mp4"
VIDEO_SHA = "sha256:d83b2023b91212ae2bf41601b629783ab054fe036bb33f0ef7262a688e4c2e78"
THUMB = "09_package/thumbnail.selected.v002.png"
THUMB_SHA = "sha256:c9eeacfaa609dd2ce0eca2ecb75b6790ce25cfbe5139194fef15a9d1367788a1"
CHANNEL = "UCuQPtAz1rca9eJ4xhvX0yKA"

PUBLISH_AT_UTC = "2026-07-23T03:00:00Z"
PUBLISH_AT_LOCAL = "2026-07-23T12:00:00+09:00"

TITLE = "The Judges Were Paid to Send Children to Jail — The Kids for Cash Scandal"

DESCRIPTION = """In Luzerne County, Pennsylvania, a courtroom that was supposed to protect children became a pipeline to a private jail. For years, Judge Mark Ciavarella sent kids away for the smallest things — a schoolyard fight, a prank web page, twenty dollars of stolen makeup — often in hearings that lasted about ninety seconds, with no lawyer in the room.

What the children and their families didn't know: the judge and a colleague, Michael Conahan, were being paid millions by the people who owned the for-profit detention centers. Half the children who came before Ciavarella were locked up — compared with about eight in a hundred statewide.

This is the story of how it happened, how a small nonprofit and a grieving mother finally forced it into the light, and what it cost everyone involved — including the more than 2,000 convictions a court would eventually throw out.

— CHAPTERS —
0:00 A ninety-second hearing
(chapters finalized before publish)

— NOTE ON IMAGERY —
This film contains AI-assisted symbolic reconstructions. No real footage of the children or private hearings exists; dramatized and generated visuals are used to illustrate documented events and are labeled on-screen as symbolic reconstruction.

— SOURCES —
Interbranch Commission on Juvenile Justice report (2010); U.S. v. Ciavarella court records; Juvenile Law Center filings; Pennsylvania Supreme Court orders vacating adjudications.

If stories like this matter to you, subscribe — one true story of power and the law, every week.
#KidsForCash #JuvenileJustice #TrueCrime"""

TAGS = [
    "kids for cash", "kids for cash scandal", "luzerne county", "mark ciavarella",
    "michael conahan", "juvenile justice", "judicial corruption", "for-profit prison",
    "juvenile detention", "juvenile law center", "sandy fonzo", "pennsylvania",
    "wrongful conviction", "true crime documentary", "corruption documentary",
    "prime documentary", "know your rights", "right to a lawyer",
]

DEVIATIONS = [
    {"gate": "runtime_band", "value": "9.40min vs band 11.5-12.5min",
     "reason": "owner-accepted shorter cut (like EP34); pacing deliberate"},
    {"gate": "sound_layers", "value": "3-layer VO+music+ambience -14 LUFS (no dense SFX bed)",
     "reason": "owner is SFX-sensitive (EP32 rejected noisy SFX); mix approved on watch 2026-07-19"},
    {"gate": "preflight_receipt", "value": "receipt exists but verdict=BLOCK",
     "reason": "EP38 built ad-hoc; lacks remotion_plan/scene_plan/asset_selection provenance files; render itself verified"},
]


def main():
    PKG.mkdir(parents=True, exist_ok=True)
    APPROVALS.mkdir(parents=True, exist_ok=True)

    meta = {
        "schema_version": "1.1.0", "episode_id": EP, "revision": "v004_ae",
        "status": "ready_to_schedule",
        "title": TITLE,
        "title_options": [
            TITLE,
            "Two Judges. A Private Jail. Thousands of Children Sold for Cash.",
            "They Jailed Kids for Cash — and Almost Got Away With It",
        ],
        "description": DESCRIPTION,
        "description_first_two_lines": DESCRIPTION.split("\n\n")[0][:200],
        "tags": TAGS,
        "category": "News & Politics", "category_id": "25",
        "default_language": "en", "default_audio_language": "en",
        "made_for_kids": False,
        "privacy_status": "private",
        "scheduling": {"mode": "scheduled", "publishAt": PUBLISH_AT_UTC,
                       "scheduled_at_local": PUBLISH_AT_LOCAL},
        "video": VIDEO, "video_sha256": VIDEO_SHA,
        "thumbnail": THUMB, "thumbnail_sha256": THUMB_SHA, "selected_thumbnail": "thumbnail.selected.v002.png",
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "altered_or_synthetic_content": True,
        "playlist": "Prime Documentary — Landmark Rights Cases",
        "pre_publish_checks": {"acceptance": "FAIL (3 owner-accepted deviations)",
                               "quality_gates_pass": ["arc_nonrepeat", "footage_utilization",
                                   "caption_integrity", "motion_density", "visual_asset_qc",
                                   "loudness", "thumbnail_visibility", "probe_receipt"],
                               "captions_srt": "08_edit/captions.final.v001.srt"},
    }
    (PKG / "youtube_meta.v001.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    delivery = {
        "schema_version": "1.0.0", "episode_id": EP, "revision": "v004_ae",
        "canonical_final": VIDEO, "canonical_final_sha256": VIDEO_SHA,
        "thumbnail": THUMB, "thumbnail_sha256": THUMB_SHA,
        "acceptance": {"result": "FAIL", "pass_count": 37, "hard_fail_count": 3,
                       "hard_failures": ["runtime_band", "sound_layers", "preflight_receipt"]},
        "owner_deviation_required": True, "deviations": DEVIATIONS,
        "notes": "AE hero beats + unique-sourced factory clips + namespaced stills + caption gate fix. "
                 "All output-quality gates green; 3 deviations owner-accepted.",
    }
    (PKG / "final_delivery.v001.json").write_text(json.dumps(delivery, ensure_ascii=False, indent=2), encoding="utf-8")

    apr = {
        "schema_version": "1.0.0", "id": "APR-0001", "episode_id": EP,
        "type": "publish", "decision": "approved",
        "approver": "owner", "approved_via": "chat instruction",
        "owner_instruction": "YouTubeに予約投稿して / ok. サムネはCTR意識して (2026-07-19)",
        "scope": "schedule PRIVATE upload with publishAt (auto-publish at scheduled time)",
        "video": VIDEO, "video_sha256": VIDEO_SHA,
        "thumbnail_sha256": THUMB_SHA,
        "channel_id": CHANNEL,
        "publishAt": PUBLISH_AT_UTC, "scheduled_at_local": PUBLISH_AT_LOCAL,
        "deviations_accepted": ["runtime_band", "sound_layers", "preflight_receipt"],
        "conditions": "approval valid ONLY for this exact video_sha256; any re-render voids it",
    }
    (APPROVALS / "APR-0001.json").write_text(json.dumps(apr, ensure_ascii=False, indent=2), encoding="utf-8")

    print("[pkg] wrote youtube_meta.v001.json, final_delivery.v001.json, approvals/APR-0001.json")
    print(f"[pkg] title: {TITLE}")
    print(f"[pkg] schedule: {PUBLISH_AT_LOCAL}  privacy: private(scheduled)")
    print(f"[pkg] video_sha bound: {VIDEO_SHA[:23]}…  thumb: thumbnail.selected.v002.png")


if __name__ == "__main__":
    main()
