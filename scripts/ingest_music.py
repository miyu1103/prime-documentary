"""
scripts/ingest_music.py
Role: audio-director
Ingest Suno-generated music from downloads/music/ into library/music/[category]/.

Suno Commercial License:
  Paid subscribers (Pro / Premier) may use Suno-generated audio commercially.
  Terms: https://suno.com/terms  (Section 4 — Output License)
  rights_basis: "suno_commercial" (verified 2026-06)

Registry: H:\pd-media\library\music_registry.v001.json
Idempotency: content_hash (SHA-256 of file bytes) — skip if already registered.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
from datetime import datetime, timezone

MUSIC_DL    = pathlib.Path(r"H:\pd-media\downloads\music")
LIB_MUSIC   = pathlib.Path(r"H:\pd-media\library\music")
REGISTRY    = pathlib.Path(r"H:\pd-media\library\music_registry.v001.json")
EVENTS      = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\events.jsonl"
)
FFPROBE     = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

RIGHTS_BASIS = (
    "Suno Commercial License — paid subscriber, commercial use permitted "
    "per Suno Terms of Service https://suno.com/terms (Section 4, Output License). "
    "Verified 2026-06."
)

# ── Track catalog ──────────────────────────────────────────────────────────
# (filename_stem, category, mood, function, bpm, energy, loopable, suno_prompt)
TRACKS: list[tuple[str, str, str, str, int | None, int, bool, str]] = [
    # hook (energy 3–4, 70–85 BPM)
    (
        "mus_20260614_hook_glass_air_bed_v1",
        "hook", "tense_sparse", "cold_open_underscore", 78, 3, False,
        "Cold-open underscore, sparse piano + low sub pulse, single rising synth swell, "
        "tense but restrained, no melody, leaves space for a spoken question, 70–85 BPM, "
        "cinematic documentary.",
    ),
    (
        "mus_20260614_hook_glass_air_bed_v2",
        "hook", "tense_sparse", "cold_open_underscore", 78, 4, False,
        "Cold-open underscore, sparse piano + low sub pulse, single rising synth swell, "
        "tense but restrained, no melody, leaves space for a spoken question, 70–85 BPM, "
        "cinematic documentary.",
    ),
    # opening (energy 3, 90 BPM)
    (
        "mus_20260614_opening_measured_arpeggio_v1",
        "opening", "confident_clear", "title_sequence", 90, 3, False,
        "Title-sequence underscore, measured piano arpeggio + warm low strings, "
        "confident and clear, sense of 'we will explain', 90 BPM, builds slightly then settles, "
        "instrumental.",
    ),
    (
        "mus_20260614_opening_measured_arpeggio_v2",
        "opening", "confident_clear", "title_sequence", 90, 3, False,
        "Title-sequence underscore, measured piano arpeggio + warm low strings, "
        "confident and clear, sense of 'we will explain', 90 BPM, builds slightly then settles, "
        "instrumental.",
    ),
    # explainer_bed (energy 2, 85 BPM, loopable)
    (
        "mus_20260614_explainer_bed_soft_explainer_v1",
        "explainer_bed", "neutral_unobtrusive", "narration_bed", 85, 2, True,
        "Neutral explainer bed, soft sustained pads + gentle pulse, unobtrusive, "
        "sits under narration, no strong melody, 85 BPM, fully loopable, long and even.",
    ),
    (
        "mus_20260614_explainer_bed_soft_explainer_v2",
        "explainer_bed", "neutral_unobtrusive", "narration_bed", 85, 2, True,
        "Neutral explainer bed, soft sustained pads + gentle pulse, unobtrusive, "
        "sits under narration, no strong melody, 85 BPM, fully loopable, long and even.",
    ),
    # tension_build (energy 4, 95 BPM)
    (
        "mus_20260614_tension_build_courtroom_horizon_v1",
        "tension_build", "slow_crescendo", "stakes_escalation", 95, 4, False,
        "Slow-building tension, layered strings + rising arpeggio + soft timpani, "
        "courtroom stakes, controlled crescendo, 95 BPM, no big payoff (the reveal handles that).",
    ),
    (
        "mus_20260614_tension_build_courtroom_horizon_v2",
        "tension_build", "slow_crescendo", "stakes_escalation", 95, 4, False,
        "Slow-building tension, layered strings + rising arpeggio + soft timpani, "
        "courtroom stakes, controlled crescendo, 95 BPM, no big payoff (the reveal handles that).",
    ),
    # somber (energy 2, 65 BPM)
    (
        "mus_20260614_somber_ledger_of_ash_v1",
        "somber", "dignified_sparse", "human_cost", 65, 2, False,
        "Somber reflective underscore, lone piano + cello, dignified not maudlin, "
        "for a human-cost moment, 65 BPM, sparse.",
    ),
    (
        "mus_20260614_somber_ledger_of_ash_v2",
        "somber", "dignified_sparse", "human_cost", 65, 2, False,
        "Somber reflective underscore, lone piano + cello, dignified not maudlin, "
        "for a human-cost moment, 65 BPM, sparse.",
    ),
    # reveal (energy 4–5, 90 BPM)
    (
        "mus_20260614_reveal_hidden_system_clicks_v1",
        "reveal", "harmonic_resolution", "reveal_sting", 90, 4, False,
        "Reveal sting + bed, a clear harmonic resolution, warm brass-pad swell + "
        "bright but tasteful synth, the 'hidden system clicks' moment, 90 BPM, "
        "8–12s usable sting plus a sustained tail.",
    ),
    (
        "mus_20260614_reveal_hidden_system_clicks_v2",
        "reveal", "harmonic_resolution", "reveal_sting", 90, 5, False,
        "Reveal sting + bed, a clear harmonic resolution, warm brass-pad swell + "
        "bright but tasteful synth, the 'hidden system clicks' moment, 90 BPM, "
        "8–12s usable sting plus a sustained tail.",
    ),
    (
        "mus_20260614_reveal_verdict_at_dawn_v1",
        "reveal", "warm_brass_swell", "reveal_bed", 90, 4, False,
        "Reveal sting + bed, warm brass-pad swell, hopeful resolution, "
        "verdict moment underscore, 90 BPM, sustained tail.",
    ),
    (
        "mus_20260614_reveal_verdict_at_dawn_v2",
        "reveal", "warm_brass_swell", "reveal_bed", 90, 4, False,
        "Reveal sting + bed, warm brass-pad swell, hopeful resolution, "
        "verdict moment underscore, 90 BPM, sustained tail.",
    ),
    (
        "mus_20260614_reveal_verdict_at_dawn_v3",
        "reveal", "warm_brass_swell", "reveal_bed", 90, 5, False,
        "Reveal sting + bed, warm brass-pad swell, hopeful resolution, "
        "verdict moment underscore, 90 BPM, sustained tail.",
    ),
    # outro (energy 3, 92 BPM)
    (
        "mus_20260614_outro_last_frame_v1",
        "outro", "hopeful_resolved", "end_card", 92, 3, False,
        "End-card underscore, hopeful resolved chords, piano + strings + soft pulse, "
        "subscribe/next-episode CTA feel, 92 BPM, clean ending, instrumental.",
    ),
    (
        "mus_20260614_outro_last_frame_v2",
        "outro", "hopeful_resolved", "end_card", 92, 3, False,
        "End-card underscore, hopeful resolved chords, piano + strings + soft pulse, "
        "subscribe/next-episode CTA feel, 92 BPM, clean ending, instrumental.",
    ),
    # ambience (energy 1, no BPM, loopable)
    (
        "mus_20260614_ambience_empty_hall_v1",
        "ambience", "subliminal_drone", "glue_texture", None, 1, True,
        "Neutral room-tone / texture bed, very low drone + faint noise, almost subliminal, "
        "to glue cuts, no rhythm, fully loopable.",
    ),
    (
        "mus_20260614_ambience_empty_hall_v2",
        "ambience", "subliminal_drone", "glue_texture", None, 1, True,
        "Neutral room-tone / texture bed, very low drone + faint noise, almost subliminal, "
        "to glue cuts, no rhythm, fully loopable.",
    ),
    (
        "mus_20260614_ambience_paper_trail_static_v1",
        "ambience", "paper_texture", "document_glue", None, 1, True,
        "Ambient paper and static texture, archival feel, very quiet, "
        "document-handling atmosphere, fully loopable.",
    ),
    (
        "mus_20260614_ambience_paper_trail_static_v2",
        "ambience", "paper_texture", "document_glue", None, 1, True,
        "Ambient paper and static texture, archival feel, very quiet, "
        "document-handling atmosphere, fully loopable.",
    ),
]


def _probe_duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return round(float(r.stdout.strip()), 3)


def _file_hash(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_registry() -> list[dict]:
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return []


def _save_registry(entries: list[dict]) -> None:
    tmp = REGISTRY.with_suffix(".tmp")
    tmp.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(REGISTRY)


def _append_event(event: dict) -> None:
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> None:
    registry = _load_registry()
    existing_hashes = {e["content_hash"] for e in registry}
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    ingested: list[str] = []
    skipped:  list[str] = []
    by_category: dict[str, int] = {}
    track_num = len(registry) + 1

    for stem, category, mood, function, bpm, energy, loopable, suno_prompt in TRACKS:
        src = MUSIC_DL / f"{stem}.mp3"
        if not src.exists():
            print(f"  MISSING {src.name}")
            continue

        h = _file_hash(src)
        if h in existing_hashes:
            print(f"  SKIP {stem} (already registered)")
            skipped.append(stem)
            continue

        dst_dir = LIB_MUSIC / category
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / f"{stem}.mp3"

        shutil.copy2(src, dst)
        dur = _probe_duration(dst)

        track_id = f"MUS-{track_num:04d}"
        entry = {
            "track_id":    track_id,
            "category":    category,
            "mood":        mood,
            "function":    function,
            "bpm":         bpm,
            "energy":      energy,
            "duration_sec": dur,
            "loopable":    loopable,
            "suno_prompt": suno_prompt,
            "filename":    dst.name,
            "path_relative": f"library/music/{category}/{dst.name}",
            "source":      "Suno",
            "rights_basis": RIGHTS_BASIS,
            "content_hash": h,
            "backup_required": True,
            "verified_at": now,
        }
        registry.append(entry)
        existing_hashes.add(h)
        _save_registry(registry)

        by_category[category] = by_category.get(category, 0) + 1
        ingested.append(track_id)
        print(f"  OK {track_id}  [{category}]  {stem}  {dur:.1f}s")
        track_num += 1

    if ingested:
        _append_event({
            "event":       "music_ingested",
            "episode_id":  "library",
            "ingested":    ingested,
            "skipped":     skipped,
            "by_category": by_category,
            "registry":    str(REGISTRY),
            "timestamp":   now,
        })

    print(f"\n{'='*56}")
    print(f"Ingested : {len(ingested)}")
    print(f"Skipped  : {len(skipped)}")
    print(f"By category:")
    for cat, cnt in sorted(by_category.items()):
        print(f"  {cat:20s} {cnt}")
    print(f"\nRegistry : {REGISTRY}")
    print(f"\nSuno rights note:")
    print(f"  Commercial use permitted for paid subscribers.")
    print(f"  backup_required=True: do not keep masters on SSD only.")


if __name__ == "__main__":
    main()
