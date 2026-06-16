#!/usr/bin/env python3
r"""Prepare PD-2026-002-gideon for upload: recompute chapters for the final timeline, select the
click thumbnail, record owner approvals (APR-0002/0003/0004), update youtube_meta + manifest.

Owner explicitly approved the cut + title/thumbnail + posting (2026-06-17). Visibility stays PRIVATE
(public is a separate step). Recomputes chapter timestamps from the FINAL timing (hook shortened +
opening inserted) so the published description is correct. Idempotent.
    py -3.11 scripts/prep_publish_gideon.py
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MEDIA = Path(json.loads((REPO / "config/storage.local.json").read_text("utf-8"))["roots"]["media"]["path"])
EP = "PD-2026-002-gideon"
EPDIR = REPO / "episodes" / EP
TS = "2026-06-17T00:00:00+00:00"
OPENING_SEC = 3.5
CUT = MEDIA / "episodes" / EP / "08_edit" / "gideon_premium_v001.mp4"
THUMB = REPO / "remotion" / "out" / "thumb_click_a.png"

# chapter -> scene (output time = scene start, +OPENING_SEC for everything after the hook)
CHAPTERS = [
    ("S001", "The prisoner who beat the Court"),
    ("S003", "The right that's younger than you think"),
    ("S004", "On trial with no lawyer"),
    ("S009", "The letter — and the wall called Betts v. Brady"),
    ("S015", "Nine to nothing"),
    ("S019", "The law changed — but not his fate yet"),
    ("S023", "The right vs. the reality (public defenders)"),
    ("S026", "A pencil, a letter — a rule for everyone"),
]


def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    tm = json.loads((EPDIR / "08_edit/timing.v001.json").read_text("utf-8"))
    start = {s["scene_id"]: s["start"] for s in tm["scenes"]}
    cut_hash, thumb_hash = sha256(CUT), sha256(THUMB)

    chapters = []
    for i, (sid, title) in enumerate(CHAPTERS):
        out_t = 0 if sid == "S001" else round(start[sid] + OPENING_SEC, 3)
        chapters.append({"index": i + 1, "timestamp": mmss(out_t), "timestamp_sec": int(out_t), "title": title})

    ym = json.loads((EPDIR / "09_package/youtube_meta.v001.json").read_text("utf-8"))
    # rebuild the description's chapter block with the corrected timestamps
    desc = ym["description"]
    chap_lines = "\n".join(f"{c['timestamp']} {c['title']}" for c in chapters)
    import re
    desc = re.sub(r"⏱ Chapters\n(?:.*\n)*?(?=\n📚)", "⏱ Chapters\n" + chap_lines + "\n", desc)
    ym["description"] = desc
    ym["chapters"] = chapters
    ym["video_file"] = "gideon_premium_v001.mp4"
    ym["status"] = "approved_private_upload"
    ym["visibility"] = "private"
    ym["publish_approved"] = False  # public flip is the separate final step
    ym["first_cut_approved"] = True
    ym["first_cut_approval_ref"] = "APR-0002"
    ym["title_thumbnail_approved"] = True
    ym["title_thumbnail_approval_ref"] = "APR-0003"
    ym["thumbnail"] = {
        "selected": "click_a",
        "file": "remotion/out/thumb_click_a.png",
        "content_hash": f"sha256:{thumb_hash}",
        "props_ref": "remotion/thumb_gideon_click_a.json",
        "ab_alt": "remotion/out/thumb_click_b.png",
    }
    sc = ym["safety_checklist"]
    sc["final_cut_hash"] = cut_hash
    sc["final_cut_path"] = f"H:/pd-media/episodes/{EP}/08_edit/gideon_premium_v001.mp4"
    sc["final_cut_size_bytes"] = CUT.stat().st_size
    sc["title_thumbnail_content_match"] = True
    ym["publish_gate"] = "private_upload_ready"
    ym["publish_gate_blockers"] = ["public flip pending owner go (recommend research SRC live-verification first, QC-0008)"]
    (EPDIR / "09_package/youtube_meta.v001.json").write_text(json.dumps(ym, indent=2, ensure_ascii=False) + "\n", "utf-8")

    # approvals (owner explicitly approved: "最高、投稿しよう", 2026-06-17)
    def apr(aid, ttype, tid, decision, notes, ev):
        return {"schema_version": "1.0.0", "approval_id": aid, "episode_id": EP, "target_type": ttype,
                "target_id": tid, "target_revision": "v001", "decision": decision, "requested_at": TS,
                "requested_by": "local-claude-code", "decided_at": TS, "decided_by": "owner",
                "notes": notes, "conditions": [], "expires_at": None, "evidence_snapshot_ref": ev}
    aprs = {
        "APR-0002": apr("APR-0002", "edit", "gideon_premium_v001.mp4", "approved",
            f"Owner approved final cut ('めちゃくちゃよかった。最高', 2026-06-17). Bound to sha256:{cut_hash}.",
            f"artifact://episodes/{EP}/08_edit/gideon_premium_v001.mp4"),
        "APR-0003": apr("APR-0003", "package", "title_thumbnail", "approved",
            f"Owner approved title + click thumbnail (thumb_click_a 'NO LAWYER. HE STILL WON.', sha256:{thumb_hash[:16]}..).",
            "artifact://episodes/PD-2026-002-gideon/09_package/packaging_concept.v001.md"),
        "APR-0004": apr("APR-0004", "publish", "gideon_premium_v001.mp4", "approved",
            f"Owner authorized posting ('投稿しよう', 2026-06-17). Upload is PRIVATE first per decisions §11; "
            f"public scheduling is a separate owner action. Bound to sha256:{cut_hash}.",
            f"artifact://episodes/{EP}/08_edit/gideon_premium_v001.mp4"),
    }
    for aid, data in aprs.items():
        (EPDIR / "approvals" / f"{aid}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", "utf-8")

    mani = json.loads((EPDIR / "manifest.json").read_text("utf-8"))
    mani["state"] = "package_ready"
    for a in ("APR-0002", "APR-0003", "APR-0004"):
        if a not in mani["approvals"]:
            mani["approvals"].append(a)
    mani["updated_at"] = TS
    (EPDIR / "manifest.json").write_text(json.dumps(mani, indent=2, ensure_ascii=False) + "\n", "utf-8")

    print(f"cut sha256:{cut_hash}")
    print("chapters:")
    for c in chapters:
        print(f"  {c['timestamp']:>5}  {c['title']}")
    print("wrote youtube_meta + APR-0002/0003/0004 + manifest (package_ready)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
