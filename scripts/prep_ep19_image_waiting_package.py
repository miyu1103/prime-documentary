#!/usr/bin/env python3
"""Prepare EP19 packaging/QC artifacts that do not require finished hero images.

No paid calls, no upload, no render. This writes owner/operator-facing handoff
files so the final image insertion run is deterministic once EP19-IMG-001..092
exist in the selected folder.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-019-varsityblues"
EPDIR = ROOT / "episodes" / EP
MEDIA = Path("H:/pd-media")
EP_MEDIA = MEDIA / "episodes" / EP
SELECTED = EP_MEDIA / "05_visuals" / "selected"
PKG = EPDIR / "09_package"
STOCK = EPDIR / "05_stock"
EDIT = EPDIR / "08_edit"
AUDIO = EPDIR / "06_audio"
EVENTS = EPDIR / "events" / "events.jsonl"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def sha256(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def append_event(kind: str, payload: dict[str, Any]) -> None:
    EVENTS.parent.mkdir(exist_ok=True)
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": now(), "event": kind, "payload": payload}, ensure_ascii=False) + "\n")


def image_slot_template() -> list[dict[str, Any]]:
    slots = []
    for i in range(1, 93):
        path = SELECTED / f"EP19-IMG-{i:03d}.png"
        slots.append(
            {
                "image_id": f"EP19-IMG-{i:03d}",
                "expected_path": str(path).replace("\\", "/"),
                "exists_now": path.exists(),
                "required_long_edge_px": 3840,
                "required_aspect": "16:9",
                "r3_rules": [
                    "no real-person likeness",
                    "no real university logo/crest/mascot",
                    "no real landmark",
                    "no readable institutional marks",
                    "symbolic reconstruction only",
                ],
            }
        )
    return slots


def write_image_waiting_packet() -> None:
    slots = image_slot_template()
    present = sum(1 for slot in slots if slot["exists_now"])
    (EDIT / "image_insertion_manifest.template.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "status": "waiting_for_hero_images",
                "expected_count": 92,
                "present_now": present,
                "selected_dir": str(SELECTED).replace("\\", "/"),
                "slots": slots,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_rights_manifest() -> None:
    assets: list[dict[str, Any]] = []
    voice_meta = load_json(AUDIO / "voice_master.v001.json", {})
    audio_delivery = load_json(PKG / "audio_delivery.v001.json", {})
    for key, kind in [("voice_master", "elevenlabs_narration_master"), ("audio_mix", "audio_mix_with_library_bgm")]:
        path = Path(str(audio_delivery.get(key, "")).replace("/", "\\"))
        if path.exists():
            assets.append(
                {
                    "asset_id": f"EP19-{kind}",
                    "asset_type": kind,
                    "path": str(path).replace("\\", "/"),
                    "origin": "ElevenLabs narration and Prime Documentary internal music/SFX library mix",
                    "license": "internal production use; no upload performed",
                    "provider": voice_meta.get("provider", "elevenlabs") if "narration" in kind else "prime_documentary_library",
                    "ai_disclosure": "ElevenLabs voice synthesis" if "narration" in kind else "Suno-origin library bed reused in mix",
                    "sha256": sha256(path),
                }
            )
    factory = load_json(STOCK / "factory_ledger.v001.json", {}).get("assets", [])
    for item in factory:
        assets.append(
            {
                "asset_id": item["id"],
                "asset_type": "factory_broll",
                "path": item["remotion_src"],
                "source_path": item["source_path"],
                "origin": "Prime Documentary asset factory stock shelf",
                "license": item.get("license"),
                "source_url": item.get("source_url"),
                "sha256": item.get("sha256"),
            }
        )
    assets.append(
        {
            "asset_id": "EP19-HERO-IMAGES-PENDING",
            "asset_type": "hero_stills_pending",
            "path": str(SELECTED / "EP19-IMG-###.png").replace("\\", "/"),
            "origin": "pending generated symbolic hero stills",
            "license": "pending",
            "ai_disclosure": True,
            "status": "pending_image_completion",
        }
    )
    PKG.mkdir(exist_ok=True)
    (PKG / "rights_manifest.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "status": "audio_and_factory_ready_images_pending",
                "owner_r3_legal_review_required": True,
                "assets": assets,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def run_acceptance_snapshot() -> dict[str, Any]:
    result = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "scripts/check_final_acceptance.py", "19", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        data = json.loads(result.stdout)
    except Exception:
        data = {"status": "ERROR", "stdout": result.stdout, "stderr": result.stderr}
    (PKG / "pre_image_acceptance_snapshot.v001.json").write_text(
        json.dumps(
            {
                "episode_id": EP,
                "revision": "v001",
                "expected_status": "FAIL_until_images_thumbnails_and_final_render_exist",
                "exit_code": result.returncode,
                "snapshot": data,
                "created_at": now(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return data


def write_resume_runbook(snapshot: dict[str, Any]) -> None:
    missing = []
    for row in snapshot.get("results", []):
        if row.get("hard") and not row.get("ok"):
            missing.append(f"- {row.get('check')}: {row.get('reason')}")
    text = f"""# EP19 Image-Waiting Handoff v001

Status: audio/factory/Remotion scaffold ready; hero images, thumbnails, final render pending.

Ready now:
- ElevenLabs master voice: `H:/pd-media/episodes/{EP}/06_audio/master_elevenlabs_v001/voice_master.v001.wav`
- Final audio mix: `H:/pd-media/episodes/{EP}/08_edit/varsityblues_final_mix.v001.wav`
- Captions: `episodes/{EP}/08_edit/captions.v001.srt`
- Factory b-roll ledger: `episodes/{EP}/05_stock/factory_ledger.v001.json`
- Remotion composition: `VarsityBluesPremium`

When images are ready:
1. Place all files as `H:/pd-media/episodes/{EP}/05_visuals/selected/EP19-IMG-001.png` through `EP19-IMG-092.png`.
2. Confirm every used still is 16:9 and long edge >= 3840 px.
3. Run:

```powershell
cd C:\\Users\\aab15\\Documents\\prime-documentary
.\\.venv\\Scripts\\python.exe scripts\\build_ep19_varsityblues_final.py
.\\.venv\\Scripts\\python.exe scripts\\check_final_acceptance.py 19 --json
```

Current independent gate blockers:
{chr(10).join(missing) if missing else "- none"}

Do not publish/upload. R3 legal and rights owner gate remains required after final render.
"""
    (PKG / "IMAGE_WAITING_HANDOFF.v001.md").write_text(text, encoding="utf-8")


def main() -> int:
    PKG.mkdir(exist_ok=True)
    EDIT.mkdir(exist_ok=True)
    write_image_waiting_packet()
    write_rights_manifest()
    snapshot = run_acceptance_snapshot()
    write_resume_runbook(snapshot)
    append_event(
        "image_waiting_package_prepared",
        {
            "revision": "v001",
            "handoff": f"episodes/{EP}/09_package/IMAGE_WAITING_HANDOFF.v001.md",
            "rights_manifest": f"episodes/{EP}/09_package/rights_manifest.v001.json",
            "image_slots": 92,
            "final_render_pending": True,
        },
    )
    print("EP19 image-waiting package prepared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
