from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import request


ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path("H:/pd-media")
A1111 = "http://127.0.0.1:7860/sdapi/v1"
MODEL = "juggernautXL_ragnarokBy.safetensors [dd08fa32f9]"
NEG = (
    "text, letters, words, typography, watermark, logo, brand mark, signature, "
    "identifiable real person, celebrity likeness, public figure likeness, judge likeness, "
    "deepfake, portrait of real person, distorted anatomy, extra fingers, bad hands, low resolution, "
    "blurry, cartoon, illustration, flat lighting, oversaturated, cheap CGI"
)


EPISODES: dict[str, dict[str, Any]] = {
    "lange": {
        "episode_id": "PD-2026-014-lange",
        "risk_class": "R2",
        "selected_background": "THUMB-01.png",
        "render": MEDIA / "episodes/PD-2026-014-lange/08_edit/renders/lange_premium_review_proxy_v001.mp4",
        "captions": ROOT / "episodes/PD-2026-014-lange/08_edit/captions.review_proxy.v001.srt",
        "qc": ROOT / "episodes/PD-2026-014-lange/08_edit/renders/premium_qc/lange_review_proxy_v001.qc.json",
        "title": "Can a Cop Follow You Into Your Own Home?",
        "description": (
            "A police officer follows a man into his garage. The Supreme Court has to decide whether "
            "misdemeanor flight automatically lets police cross the home's threshold without a warrant.\n\n"
            "This review package uses local review-proxy narration. It is for owner review and production "
            "handoff, not public upload.\n\n"
            "Visual note: this video uses licensed stock/factory media, AI-generated symbolic reconstructions, "
            "and motion design. No real-person likeness is intended.\n"
        ),
        "chapters": [
            ("00:00", "A foot under the garage door"),
            ("00:32", "Opening: the home threshold"),
            ("01:20", "Hot pursuit and misdemeanors"),
            ("03:20", "What the Court rejects"),
            ("05:45", "The emergency exception"),
            ("08:20", "Why the line matters"),
            ("10:05", "Next: fraud and proof"),
        ],
        "tags": [
            "Lange v California",
            "Fourth Amendment",
            "hot pursuit",
            "warrantless entry",
            "Supreme Court",
            "constitutional law",
            "home privacy",
            "Prime Documentary",
        ],
        "thumbnail_titles": [
            {"id": "A", "title": "FOLLOWED INTO YOUR HOME?", "youtube_title": "Can a Cop Follow You Into Your Own Home?"},
            {"id": "B", "title": "GARAGE DOOR. NO WARRANT?", "youtube_title": "He Ran Into His Garage. The Officer Stuck His Foot Under the Door."},
            {"id": "C", "title": "WHEN CAN POLICE ENTER?", "youtube_title": "When Can Police Enter Your Home Without a Warrant?"},
        ],
        "prompts": {
            "THUMB-01.png": "Tense hero, a foot wedged under a descending garage door with bright light spilling through the gap, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-02.png": "A police silhouette with no face standing at a glowing warm front door at night, looming shadow, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-03.png": "A single house glowing like a fortress under a vast dark sky with cold blue police light approaching, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-04.png": "Dramatic close view of a front door with a glowing red threshold line and a boot about to cross it, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-05.png": "Hot pursuit silhouette chasing a faceless fleeing figure toward a home at night, cinematic motion, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-06.png": "A warrant scroll and emergency red glow shown as two symbolic keys before a locked front door, conceptual legal threshold, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
        },
    },
    "theranos": {
        "episode_id": "PD-2026-015-theranos",
        "risk_class": "R3",
        "selected_background": "THUMB-02.png",
        "render": MEDIA / "episodes/PD-2026-015-theranos/08_edit/renders/theranos_premium_review_proxy_v003.mp4",
        "captions": ROOT / "episodes/PD-2026-015-theranos/08_edit/captions.review_proxy.v001.srt",
        "qc": ROOT / "episodes/PD-2026-015-theranos/08_edit/renders/premium_qc/theranos_review_proxy_v003.qc.json",
        "title": "When Does a Bold Promise Become a Crime?",
        "description": (
            "Theranos promised a blood-testing revolution. The legal question is narrower and harder: "
            "when does a bold business promise become criminal fraud?\n\n"
            "This review package uses local review-proxy narration. It is for owner review and production "
            "handoff, not public upload. Because this episode concerns living convicted people, legal/rights "
            "review remains required before any public release.\n\n"
            "Visual note: this video uses licensed stock/factory media, AI-generated symbolic reconstructions, "
            "and motion design. No real-person likeness of Elizabeth Holmes, Ramesh Balwani, or any other "
            "real person is intended.\n"
        ),
        "chapters": [
            ("00:00", "A dream becomes evidence"),
            ("00:35", "Opening: promise or crime"),
            ("01:25", "The blood-testing pitch"),
            ("03:05", "What investors heard"),
            ("05:25", "The trial line"),
            ("07:45", "The split verdict"),
            ("09:50", "The final question"),
        ],
        "tags": [
            "Theranos",
            "Elizabeth Holmes",
            "corporate fraud",
            "startup fraud",
            "wire fraud",
            "investor fraud",
            "true crime documentary",
            "Prime Documentary",
        ],
        "thumbnail_titles": [
            {"id": "A", "title": "$9B MACHINE. EMPTY INSIDE?", "youtube_title": "The $9 Billion Blood-Testing Machine That Never Worked"},
            {"id": "B", "title": "DREAM OR CRIME?", "youtube_title": "When Does a Bold Promise Become a Crime?"},
            {"id": "C", "title": "THE MACHINE WAS A LIE?", "youtube_title": "She Was Called the Next Steve Jobs — Until the Machine Was a Lie"},
        ],
        "prompts": {
            "THUMB-01.png": "Hero macro, a single luminous blood drop suspended above a sleek hollow black device, electric-blue rim light, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-02.png": "A sleek glowing black-box blood-testing machine cracked open to reveal it is completely hollow inside, dramatic, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-03.png": "A faceless anonymous founder silhouette with no likeness and no visible face holding up a single vial of blood, backlit and ominous, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-04.png": "A single blood drop refracting a crumbling abstract empire of light, conceptual collapse, no legible text, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-05.png": "A magazine-cover-shaped frame holding a faceless silhouette and one vial of blood, fallen icon, no text, no likeness, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
            "THUMB-06.png": "A solemn empty federal courtroom with a single spotlight on one vial of blood resting on the witness stand, strong empty negative space on one side for title overlay, single powerful focal subject, deep navy and black palette with electric-blue and gold rim light, photorealistic, volumetric light, shallow depth of field, cinematic documentary key art, 16:9",
        },
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def post_a1111(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    req = request.Request(
        f"{A1111}/{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=2400) as res:
        return json.loads(res.read().decode("utf-8"))


def ensure_thumb_images(slug: str, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    out_dir = MEDIA / "assets/ai/thumbs" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    generated: list[dict[str, Any]] = []
    for index, (name, body) in enumerate(cfg["prompts"].items(), start=1):
        out = out_dir / name
        if not out.exists() or out.stat().st_size < 100_000:
            prompt = (
                body
                + ", ultra high resolution, masterpiece quality, hyper-detailed, razor-sharp focus, "
                + "dramatic cinematic key-art lighting, bold high-contrast composition, scroll-stopping YouTube documentary thumbnail background"
            )
            payload = {
                "prompt": prompt,
                "negative_prompt": NEG,
                "width": 1344,
                "height": 768,
                "steps": 34,
                "cfg_scale": 5.5,
                "sampler_name": "DPM++ 2M Karras",
                "seed": 814000 + index * 101 + (7000 if slug == "theranos" else 0),
                "batch_size": 1,
                "n_iter": 1,
                "override_settings": {"sd_model_checkpoint": MODEL},
                "override_settings_restore_afterwards": True,
            }
            data = post_a1111("txt2img", payload)
            out.write_bytes(base64.b64decode(data["images"][0].split(",", 1)[-1]))
        generated.append({"id": out.stem, "file": str(out).replace("\\", "/"), "sha256": sha256(out)})
    write_json(out_dir / "_thumb_generation_manifest.v001.json", {
        "episode_id": cfg["episode_id"],
        "slug": slug,
        "revision": "v001",
        "generated_at": now_iso(),
        "generator": "local A1111 SDXL",
        "model": MODEL,
        "external_upload": False,
        "paid_api": False,
        "assets": generated,
    })
    return generated


def run(cmd: list[str | Path], cwd: Path) -> None:
    args = [str(x) for x in cmd]
    if args and args[0] == "npm":
        args[0] = "npm.cmd"
    subprocess.run(args, cwd=cwd, check=True)


def render_thumbnail_candidates(slug: str, cfg: dict[str, Any], thumb_assets: list[dict[str, Any]]) -> dict[str, Any]:
    ep = cfg["episode_id"]
    epdir = ROOT / "episodes" / ep
    pkg = epdir / "09_package"
    thumb_dir = epdir / "10_thumbnail"
    remotion_thumbs = ROOT / "remotion/public" / slug / "thumbs"
    source_thumbs = MEDIA / "assets/ai/thumbs" / slug
    pkg.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)
    remotion_thumbs.mkdir(parents=True, exist_ok=True)

    for src in sorted(source_thumbs.glob("THUMB-*.png")):
        shutil.copy2(src, remotion_thumbs / src.name)

    selected_background = cfg["selected_background"]
    rendered = []
    for option in cfg["thumbnail_titles"]:
        out = thumb_dir / f"thumbnail.{slug}_option_{option['id']}.v001.png"
        props = {
            "title": option["title"],
            "backgroundSrc": f"{slug}/thumbs/{selected_background}",
            "variant": "left",
        }
        props_path = thumb_dir / f"thumbnail.{slug}_option_{option['id']}.props.json"
        props_path.write_text(json.dumps(props, indent=2) + "\n", encoding="utf-8")
        run(["npm", "run", "still", "--", "ThumbnailFrame", out, f"--props={props_path}", "--overwrite"], ROOT / "remotion")
        rendered.append({**option, "file": str(out.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(out)})

    selected = rendered[1] if slug == "theranos" else rendered[0]
    selected_path = pkg / "thumbnail.selected.v001.png"
    shutil.copy2(ROOT / selected["file"], selected_path)

    meta = {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "slug": slug,
        "revision": "v001",
        "generated_at": now_iso(),
        "status": "selected_review_package_candidate",
        "selection": {
            "selected_id": selected["id"],
            "selected_title": selected["youtube_title"],
            "selected_thumbnail_text": selected["title"],
            "selected_file": str(selected_path.relative_to(ROOT)).replace("\\", "/"),
            "selected_sha256": sha256(selected_path),
            "selected_background": selected_background,
            "reason": "Best current combination of story clarity, mobile legibility, rights safety, and brand fit.",
        },
        "background_options": thumb_assets,
        "title_options": rendered,
        "rights_gate": {
            "real_person_likeness": False,
            "judge_likeness": False,
            "deepfake": False,
            "symbolic_ai_reconstruction": True,
            "commercial_use_ok": True,
            "theranos_specific": "No likeness of Elizabeth Holmes or Ramesh Balwani." if slug == "theranos" else None,
        },
    }
    write_json(pkg / "title_thumbnail_candidates.v001.json", meta)
    return meta


def ffprobe(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-show_streams", "-of", "json", str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    return json.loads(result.stdout)


def make_rights(cfg: dict[str, Any], thumb_meta: dict[str, Any]) -> dict[str, Any]:
    slug = cfg["episode_id"].split("-")[-1]
    stock = ROOT / "episodes" / cfg["episode_id"] / "05_stock/usable_assets.v001.json"
    stock_assets = []
    if stock.exists():
        stock_assets = json.loads(stock.read_text("utf-8")).get("assets", [])
    ai_public_dir = ROOT / "remotion/public" / slug
    ai_assets = [
        {"file": str(p.relative_to(ROOT)).replace("\\", "/"), "sha256": f"sha256:{sha256(p)}"}
        for p in sorted(ai_public_dir.glob("SPN-*.png"))
    ]
    thumb_public_dir = ROOT / "remotion/public" / slug / "thumbs"

    verifiable_assets: list[dict[str, Any]] = []

    def verifier_path(uri: str) -> Path:
        if uri.startswith("artifact://"):
            return MEDIA / uri[len("artifact://") :]
        return ROOT / uri

    for index, item in enumerate(ai_assets, start=1):
        verifiable_assets.append(
            {
                "asset_id": f"{slug}-ai-scene-{index:03d}",
                "asset_type": "ai_image",
                "file": item["file"],
                "content_hash": item["sha256"],
                "license": "generated",
                "source_tool": "local_sdxl_or_project_generated",
                "disclosure_required": True,
            }
        )
    for item in stock_assets:
        declared = item.get("sha256") or item.get("content_hash")
        file_uri = item["file"]
        if str(file_uri).startswith("assets/stock/"):
            public_candidate = ROOT / "remotion/public" / slug / Path(str(file_uri)).name
            if public_candidate.exists():
                file_uri = str(public_candidate.relative_to(ROOT)).replace("\\", "/")
                declared = f"sha256:{sha256(public_candidate)}"
        if not verifier_path(str(file_uri)).exists():
            continue
        verifiable_assets.append(
            {
                "asset_id": item.get("asset_id", f"{slug}-stock-{len(verifiable_assets) + 1:03d}"),
                "asset_type": item.get("asset_type", "stock"),
                "file": file_uri,
                "content_hash": declared,
                "license": item.get("license", "Pexels/Pixabay License"),
                "source_tool": item.get("source", "stock"),
                "disclosure_required": False,
            }
        )
    for p in sorted(thumb_public_dir.glob("THUMB-*.png")):
        verifiable_assets.append(
            {
                "asset_id": f"{slug}-{p.stem.lower()}",
                "asset_type": "thumbnail_background",
                "file": str(p.relative_to(ROOT)).replace("\\", "/"),
                "content_hash": f"sha256:{sha256(p)}",
                "license": "generated",
                "source_tool": "local_sdxl_a1111",
                "disclosure_required": True,
            }
        )
    selected_thumb = ROOT / thumb_meta["selection"]["selected_file"]
    if selected_thumb.exists():
        verifiable_assets.append(
            {
                "asset_id": f"{slug}-thumbnail-selected-v001",
                "asset_type": "thumbnail_composite",
                "file": str(selected_thumb.relative_to(ROOT)).replace("\\", "/"),
                "content_hash": f"sha256:{sha256(selected_thumb)}",
                "license": "generated_composite",
                "source_tool": "remotion",
                "disclosure_required": True,
            }
        )
    if cfg["render"].exists():
        verifiable_assets.append(
            {
                "asset_id": f"{slug}-review-video-v001",
                "asset_type": "review_proxy_video",
                "file": f"artifact://episodes/{cfg['episode_id']}/08_edit/renders/{cfg['render'].name}",
                "content_hash": f"sha256:{sha256(cfg['render'])}",
                "license": "project_assembly",
                "source_tool": "remotion_ffmpeg",
                "disclosure_required": True,
            }
        )
    review_audio = MEDIA / "episodes" / cfg["episode_id"] / "07_audio/review_proxy_mix_v001.mp3"
    if review_audio.exists():
        verifiable_assets.append(
            {
                "asset_id": f"{slug}-review-proxy-audio-v001",
                "asset_type": "review_proxy_audio",
                "file": f"artifact://episodes/{cfg['episode_id']}/07_audio/review_proxy_mix_v001.mp3",
                "content_hash": f"sha256:{sha256(review_audio)}",
                "license": "local_review_proxy",
                "source_tool": "windows_sapi_local",
                "disclosure_required": False,
            }
        )
    return {
        "schema_version": "1.0.0",
        "episode_id": cfg["episode_id"],
        "revision": "v001",
        "generated_at": now_iso(),
        "status": "review_proxy_rights_registered",
        "commercial_use_ok_for_review_package": True,
        "public_release_gate": "owner approval plus final narration/legal review required",
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "contains_real_person_likeness": False,
        "contains_logo_or_brand_mark": False,
        "assets": verifiable_assets,
        "ai_scene_assets": ai_assets,
        "stock_assets": stock_assets,
        "thumbnail": thumb_meta["selection"],
        "narration": {
            "kind": "local_review_proxy",
            "path": str((MEDIA / "episodes" / cfg["episode_id"] / "07_audio/review_proxy_mix_v001.mp3")).replace("\\", "/"),
            "public_release_allowed": False,
            "note": "Windows local review-proxy voice only; master narration still requires approved voice path.",
        },
        "risk_notes": [
            "Lange framing must remain misdemeanor-flight/home-entry, not DUI as the legal question."
            if cfg["episode_id"].endswith("lange")
            else "Theranos is R3: living-person legal/rights review required before publish; visuals must stay symbolic and avoid Holmes/Balwani likeness.",
        ],
    }


def package_episode(slug: str, cfg: dict[str, Any], thumb_meta: dict[str, Any]) -> None:
    ep = cfg["episode_id"]
    epdir = ROOT / "episodes" / ep
    pkg = epdir / "09_package"
    manifest_path = epdir / "manifest.json"
    events_path = epdir / "events/events.jsonl"
    pkg.mkdir(parents=True, exist_ok=True)

    probe = ffprobe(cfg["render"])
    video_sha = sha256(cfg["render"])
    thumb_sha = thumb_meta["selection"]["selected_sha256"]
    created = now_iso()

    (pkg / "title.v001.txt").write_text(cfg["title"] + "\n", encoding="utf-8")
    (pkg / "description.v001.md").write_text(cfg["description"], encoding="utf-8")
    write_json(pkg / "chapters.v001.json", [{"time": t, "title": title} for t, title in cfg["chapters"]])
    write_json(pkg / "tags.v001.json", {"episode_id": ep, "revision": "v001", "tags": cfg["tags"]})
    write_json(pkg / "rights_manifest.v001.json", make_rights(cfg, thumb_meta))

    youtube_meta = {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "revision": "v001",
        "status": "review_proxy_package_ready_owner_review_required",
        "title": cfg["title"],
        "description": cfg["description"],
        "chapters": [{"time": t, "title": title} for t, title in cfg["chapters"]],
        "tags": cfg["tags"],
        "categoryId": "27",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
        "thumbnail": thumb_meta["selection"]["selected_file"],
        "selected_thumbnail_sha256": f"sha256:{thumb_sha}" if thumb_sha and not str(thumb_sha).startswith("sha256:") else thumb_sha,
        "video_actual_path": str(cfg["render"]).replace("\\", "/"),
        "video_sha256": f"sha256:{video_sha}" if video_sha else None,
        "captions_sidecar": str(cfg["captions"].relative_to(ROOT)).replace("\\", "/") if cfg["captions"].exists() else None,
        "captions_burned_in": True,
        "synthetic_content_disclosure_required": True,
        "contains_ai_symbolic_reconstruction": True,
        "privacy_status_target": "private",
        "upload_performed": False,
        "publish_performed": False,
        "schedule_performed": False,
        "publish_gate": "closed",
        "blocking_requirements": [
            "owner first-cut approval for the exact review/final cut",
            "master narration replacement or explicit approval to use review-proxy audio",
            "title/thumbnail approval",
            "publish approval",
            "R3 legal/rights review before public release" if slug == "theranos" else "standard rights/publish preflight before public release",
        ],
        "created_at": created,
    }
    write_json(pkg / "youtube_meta.v001.json", youtube_meta)

    final_delivery = {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "revision": "v001",
        "status": "review_proxy_ready_owner_review_required",
        "generated_at": created,
        "review_video": str(cfg["render"]).replace("\\", "/"),
        "review_video_exists": cfg["render"].exists(),
        "review_video_sha256": f"sha256:{video_sha}" if video_sha else None,
        "ffprobe": probe,
        "selected_thumbnail": thumb_meta["selection"]["selected_file"],
        "captions": youtube_meta["captions_sidecar"],
        "youtube_meta": f"episodes/{ep}/09_package/youtube_meta.v001.json",
        "rights_manifest": f"episodes/{ep}/09_package/rights_manifest.v001.json",
        "qc": str(cfg["qc"].relative_to(ROOT)).replace("\\", "/") if cfg["qc"].exists() else None,
        "external_side_effects": {"upload": False, "publish": False, "paid_api": False},
        "owner_stop_point": "Review package is ready. Upload/publish not performed.",
    }
    write_json(pkg / "final_delivery.v001.json", final_delivery)

    manifest = json.loads(manifest_path.read_text("utf-8"))
    manifest["state"] = "edit_review"
    manifest["updated_at"] = created
    manifest.setdefault("active_revisions", {}).update(
        {
            "shotlist": "v001",
            "usable_assets": "v001",
            "review_proxy_audio": "v001",
            "review_proxy_captions": "v001",
            "review_proxy_qc": "v001",
            "thumbnail_candidates": "v001",
            "youtube_meta": "v001",
            "rights_manifest": "v001",
            "final_delivery": "v001",
        }
    )
    warnings = manifest.setdefault("warnings", [])
    note = "Review-proxy package prepared; public upload/schedule still blocked by owner approval and final narration/legal gates."
    if note not in warnings:
        warnings.append(note)
    write_json(manifest_path, manifest)

    events_path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event": "review_proxy_package_ready_owner_stop",
        "episode_id": ep,
        "stage": "edit_review",
        "revision": "v001",
        "actor": "codex",
        "detail": "Review-proxy video, thumbnail candidate, rights manifest, youtube metadata draft, and final_delivery prepared. Upload/publish not performed.",
        "video": str(cfg["render"]).replace("\\", "/"),
        "video_sha256": f"sha256:{video_sha}" if video_sha else None,
        "ts": created,
    }
    prior = events_path.read_text("utf-8") if events_path.exists() else ""
    if event["video_sha256"] not in prior or "review_proxy_package_ready_owner_stop" not in prior:
        events_path.open("a", encoding="utf-8").write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    for slug, cfg in EPISODES.items():
        print(f"== {slug} thumbnails ==")
        thumb_assets = ensure_thumb_images(slug, cfg)
        thumb_meta = render_thumbnail_candidates(slug, cfg, thumb_assets)
        package_episode(slug, cfg, thumb_meta)
        print(f"packaged {cfg['episode_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
