"""
scripts/gen_sfx.py
Role: audio-director
Generate SFX and ambience using ElevenLabs Sound Generation API.

Output:
  H:\pd-media\library\sfx\       SFX-0001 … SFX-0016  (one-shots)
  H:\pd-media\library\ambience\  SFX-0017 … SFX-0022  (loopable beds)

Registry:
  H:\pd-media\library\sfx_registry.v001.json

Idempotency: SHA-256 of (prompt + str(duration_seconds)).
If registry entry with same content_hash and file exist → skip.

ElevenLabs rights:
  Sound effects generated via ElevenLabs API are licensed for commercial use
  under the ElevenLabs Terms of Service (Creator License, or higher plan).
  https://elevenlabs.io/terms-of-use  — verified 2026-06
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── Paths ──────────────────────────────────────────────────────────────────
ENV_PATH      = pathlib.Path(r"C:\Users\aab15\Documents\prime-documentary\.env")
LIB_SFX       = pathlib.Path(r"H:\pd-media\library\sfx")
LIB_AMB       = pathlib.Path(r"H:\pd-media\library\ambience")
REGISTRY_PATH = pathlib.Path(r"H:\pd-media\library\sfx_registry.v001.json")
EVENTS_JSONL  = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\events.jsonl"
)
EL_SFX_URL    = "https://api.elevenlabs.io/v1/sound-generation"

# ── SFX definitions ────────────────────────────────────────────────────────
# (id, filename_stem, category, function, prompt, duration_seconds, loopable)
SFX_DEFS: list[tuple[str, str, str, str, str, float, bool]] = [
    # --- one-shots: SFX-0001–SFX-0016 ---
    (
        "SFX-0001", "sfx_whoosh_short", "sfx", "transition_cut",
        "Quick short whoosh, fast air swoosh, 0.4 seconds, cinematic documentary transition",
        0.8, False,
    ),
    (
        "SFX-0002", "sfx_whoosh_medium", "sfx", "transition_cut",
        "Medium cinematic whoosh transition, air rush, clean punchy sound, documentary style",
        1.2, False,
    ),
    (
        "SFX-0003", "sfx_ui_tick", "sfx", "ui_feedback",
        "Soft minimal UI tick click, gentle interface beep, very quiet and clean",
        0.5, False,
    ),
    (
        "SFX-0004", "sfx_soft_impact", "sfx", "chapter_hit",
        "Soft cinematic low-frequency thud impact, subtle documentary hit, controlled weight",
        0.8, False,
    ),
    (
        "SFX-0005", "sfx_paper_rustle", "sfx", "document_handling",
        "Paper rustling, crisp document pages being moved, office sound",
        1.0, False,
    ),
    (
        "SFX-0006", "sfx_gavel_knock", "sfx", "courtroom",
        "Wooden gavel knock on block, single strike, courtroom, subtle and dignified, not cartoonish",
        1.0, False,
    ),
    (
        "SFX-0007", "sfx_camera_shutter", "sfx", "still_photo",
        "Single DSLR camera mechanical shutter click for photograph, clean and crisp",
        0.5, False,
    ),
    (
        "SFX-0008", "sfx_low_boom", "sfx", "chapter_card",
        "Low cinematic bass boom, chapter card title hit, restrained documentary weight",
        1.5, False,
    ),
    (
        "SFX-0009", "sfx_riser_2s", "sfx", "reveal_buildup",
        "Cinematic tension riser 2 seconds, rising frequency swell building into reveal, documentary",
        2.5, False,
    ),
    (
        "SFX-0010", "sfx_data_blip", "sfx", "diagram",
        "Subtle electronic data blip, minimal digital interface sound for diagram animation",
        0.5, False,
    ),
    (
        "SFX-0011", "sfx_page_turn", "sfx", "document_handling",
        "Single document page turn, paper flip, clean book page sound",
        0.6, False,
    ),
    (
        "SFX-0012", "sfx_clock_tick_loop", "sfx", "time_indicator",
        "Mechanical clock ticking steady tick-tock rhythm, 3 seconds seamlessly loopable",
        3.0, True,
    ),
    (
        "SFX-0013", "sfx_stamp_seal", "sfx", "official_action",
        "Rubber stamp pressed firmly on paper, official seal sound, single clean impact",
        0.7, False,
    ),
    (
        "SFX-0014", "sfx_binder_lock", "sfx", "document_handling",
        "Metal binder rings closing, folder latch click, quiet clean office sound",
        0.6, False,
    ),
    (
        "SFX-0015", "sfx_dust_swell", "sfx", "atmosphere",
        "Light air dust swell, gentle atmospheric breath exhale, subliminal texture",
        1.5, False,
    ),
    (
        "SFX-0016", "sfx_sub_drop", "sfx", "hook_end",
        "Soft sub-bass drop, cinematic hook ending weight, low frequency rumble fade",
        2.0, False,
    ),
    # --- loopable ambience: SFX-0017–SFX-0022 ---
    (
        "SFX-0017", "amb_courtroom_room_tone", "ambience", "room_tone",
        (
            "Neutral courtroom room tone, very quiet institutional space, "
            "subtle air conditioning hum, no voices, 22 seconds seamlessly loopable"
        ),
        22.0, True,
    ),
    (
        "SFX-0018", "amb_tension_drone", "ambience", "tension_bed",
        (
            "Low cinematic tension drone, subtle anxious atmosphere, "
            "documentary style, no rhythm, no melody, dark sustained tone, 22 seconds loopable"
        ),
        22.0, True,
    ),
    (
        "SFX-0019", "amb_empty_hallway", "ambience", "location_texture",
        (
            "Empty government hallway ambience, institutional building, "
            "distant sound, subtle echo, 22 seconds loopable"
        ),
        22.0, True,
    ),
    (
        "SFX-0020", "amb_office_hum", "ambience", "neutral_bed",
        (
            "Neutral office ambient hum, fluorescent light buzz, "
            "air handling unit white noise, 22 seconds loopable"
        ),
        22.0, True,
    ),
    (
        "SFX-0021", "amb_night_window", "ambience", "location_texture",
        (
            "Night urban ambience heard through window, distant city low hum, "
            "very subtle outdoor night sound, 22 seconds loopable"
        ),
        22.0, True,
    ),
    (
        "SFX-0022", "amb_institutional_drone", "ambience", "neutral_bed",
        (
            "Institutional government building low subliminal drone, "
            "almost inaudible, texture glue, no rhythm, 22 seconds loopable"
        ),
        22.0, True,
    ),
]


def _load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _content_hash(prompt: str, duration: float) -> str:
    payload = f"{prompt}|{duration:.3f}"
    return hashlib.sha256(payload.encode()).hexdigest()


def _load_registry() -> list[dict]:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return []


def _save_registry(entries: list[dict]) -> None:
    tmp = REGISTRY_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(REGISTRY_PATH)


def _append_event(event: dict) -> None:
    EVENTS_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with EVENTS_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _generate(api_key: str, prompt: str, duration: float, retries: int = 3) -> bytes:
    payload = json.dumps(
        {"text": prompt, "duration_seconds": duration, "prompt_influence": 0.3}
    ).encode()
    req = urllib.request.Request(
        EL_SFX_URL,
        data=payload,
        method="POST",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read(300).decode("utf-8", errors="replace")
            if e.code == 429 or e.code >= 500:
                wait = 5 * attempt
                print(f"  HTTP {e.code} attempt {attempt}/{retries}, retry in {wait}s: {body[:120]}")
                time.sleep(wait)
                continue
            raise RuntimeError(f"ElevenLabs HTTP {e.code}: {body}") from e
    raise RuntimeError(f"All {retries} attempts failed")


def main(dry_run: bool = False) -> None:
    env = _load_env()
    api_key = env.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set in .env")

    registry = _load_registry()
    existing_hashes = {e["content_hash"] for e in registry}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    generated = []
    skipped = []
    failed = []

    for sfx_id, stem, category, function, prompt, duration, loopable in SFX_DEFS:
        out_dir = LIB_AMB if category == "ambience" else LIB_SFX
        out_path = out_dir / f"{stem}.mp3"
        h = _content_hash(prompt, duration)

        if h in existing_hashes and out_path.exists():
            print(f"  SKIP {sfx_id} {stem} (already registered)")
            skipped.append(sfx_id)
            continue

        print(f"  GEN  {sfx_id} {stem} ({duration}s) {'[DRY]' if dry_run else ''}")
        if dry_run:
            continue

        try:
            audio = _generate(api_key, prompt, duration)
            tmp = out_path.with_suffix(".partial")
            tmp.write_bytes(audio)
            tmp.replace(out_path)

            # Compute file hash for provenance
            file_hash = hashlib.sha256(out_path.read_bytes()).hexdigest()
            file_dur = len(audio) / (192_000 / 8)  # rough estimate from 192kbps

            entry = {
                "id": sfx_id,
                "category": category,
                "function": function,
                "filename": out_path.name,
                "path_relative": f"library/{category}/{out_path.name}",
                "duration_sec": round(file_dur, 2),
                "duration_target_sec": duration,
                "loopable": loopable,
                "source": "ElevenLabs",
                "el_endpoint": "sound-generation",
                "el_prompt": prompt,
                "rights_basis": (
                    "ElevenLabs Creator License — commercial use permitted "
                    "per Terms of Service https://elevenlabs.io/terms-of-use"
                ),
                "content_hash": h,
                "file_sha256": file_hash,
                "verified_at": now,
            }
            registry.append(entry)
            existing_hashes.add(h)
            _save_registry(registry)
            generated.append(sfx_id)
            print(f"    ✓ {out_path.name}  {len(audio)/1024:.0f} KB")
            time.sleep(0.5)  # polite rate limiting

        except Exception as e:
            print(f"    ✗ {sfx_id} FAILED: {e}")
            failed.append(sfx_id)

    if not dry_run and generated:
        _append_event({
            "event": "sfx_generated",
            "episode_id": "library",
            "generated": generated,
            "skipped": skipped,
            "failed": failed,
            "registry": str(REGISTRY_PATH),
            "timestamp": now,
        })

    print(f"\n{'='*50}")
    print(f"Generated : {len(generated)}")
    print(f"Skipped   : {len(skipped)}")
    print(f"Failed    : {len(failed)}")
    if failed:
        print(f"Failed IDs: {failed}")
    print(f"Registry  : {REGISTRY_PATH}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    main(dry_run=args.dry_run)
