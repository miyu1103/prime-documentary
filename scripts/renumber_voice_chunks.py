#!/usr/bin/env python3
"""Renumber already-paid ElevenLabs chunk files when a script gains lines in the MIDDLE.

`gen_narration_case.py` numbers chunks positionally (`VC-0001`, `VC-0002`, ...) and keys its
idempotency on `VC-NNNN.mp3` plus the sidecar's `text_sha256`. That is exactly right for a
re-run of an unchanged script and exactly wrong for an insertion: put one new sentence into
ACT_2 and every later chunk finds a file whose recorded sha no longer matches its text, so
the runner regenerates all of them. On EP67 ramirez that is $7.72 of audio the account has
already bought, to add $0.74 of new audio.

This moves the paid files to the positions the new script gives them FIRST, so the runner's
own sha check then skips them and spends only on what is genuinely new. It is the EP66 route,
written down.

    py -3.11 scripts/renumber_voice_chunks.py --ep PD-2026-067-ramirez \
        --old-script episodes/_planning/EP67_ramirez_script.en.v001.md \
        --new-script episodes/_planning/EP67_ramirez_script.en.v002.md          # dry run
    ... --apply                                                                  # do it

Refuses, before touching anything, if:
  * a chunk of the OLD script has no counterpart in the new one (the change was not a pure
    insertion, so some paid audio would be orphaned -- pass --allow-loss to accept that),
  * a mapped old chunk has no mp3 on disk,
  * two old chunks would land on the same new id.
Renames go through a staging directory, so an interrupted run cannot leave one file written
over another. Each sidecar is rewritten with its new chunk_id and a recomputed
idempotency_key (which is keyed on the chunk id), and keeps a `renumbered_from` record.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gen_narration_case import (  # noqa: E402
    EPISODES, MODEL, VOICE_ID, append_event, build_chunks, idempotency_key, media_root,
)


def draft_dir(ep: str) -> Path:
    return media_root() / "episodes" / ep / "06_voice" / "draft"


def align(old: list[dict], new: list[dict]) -> dict[str, str]:
    """old chunk_id -> new chunk_id, by matching text sha in order.

    SequenceMatcher rather than a dict so repeated sentences keep their order instead of
    collapsing onto one another.
    """
    a = [c["text_sha256"] for c in old]
    b = [c["text_sha256"] for c in new]
    out: dict[str, str] = {}
    for i, j, n in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(n):
            out[old[i + k]["chunk_id"]] = new[j + k]["chunk_id"]
    return out


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ep", required=True, choices=sorted(EPISODES))
    ap.add_argument("--old-script", required=True, help="the revision the paid files were generated from")
    ap.add_argument("--new-script", required=True, help="the revision that will be generated next")
    ap.add_argument("--apply", action="store_true", help="without this, nothing is moved")
    ap.add_argument("--allow-loss", action="store_true",
                    help="proceed even though some paid chunks have no place in the new script")
    a = ap.parse_args(argv)

    old = build_chunks(a.ep, Path(a.old_script).read_text("utf-8"))
    new = build_chunks(a.ep, Path(a.new_script).read_text("utf-8"))
    mapping = align(old, new)

    lost = [c for c in old if c["chunk_id"] not in mapping]
    print(f"old {len(old)} chunks -> new {len(new)} chunks; {len(mapping)} carried over, "
          f"{len(lost)} lost, {len(new) - len(mapping)} to be generated")
    for c in lost:
        print(f"  LOST {c['chunk_id']} {c['section']} | {c['spoken_text'][:90]}")
    if lost and not a.allow_loss:
        print("REFUSING: not a pure insertion. Re-check the edit, or pass --allow-loss.",
              file=sys.stderr)
        return 1

    dd = draft_dir(a.ep)
    if not dd.is_dir():
        print(f"REFUSING: no draft dir {dd}", file=sys.stderr)
        return 1

    missing = [o for o in mapping if not (dd / f"{o}.mp3").is_file()]
    if missing:
        print(f"REFUSING: {len(missing)} mapped chunk(s) have no mp3, first {missing[:5]}",
              file=sys.stderr)
        return 1
    targets: dict[str, str] = {}
    for o, n in mapping.items():
        if n in targets:
            print(f"REFUSING: {o} and {targets[n]} both map to {n}", file=sys.stderr)
            return 1
        targets[n] = o

    moves = {o: n for o, n in mapping.items() if o != n}
    todo = sorted({c["chunk_id"] for c in new} - set(mapping.values()))
    print(f"renames needed: {len(moves)}  (identity: {len(mapping) - len(moves)})")
    for o, n in list(sorted(moves.items()))[:5]:
        print(f"  {o} -> {n}")
    if len(moves) > 5:
        print(f"  ... and {len(moves) - 5} more")
    print(f"to generate after this: {len(todo)}  {todo[:6]}{' ...' if len(todo) > 6 else ''}")

    if not a.apply:
        print("\nDRY RUN -- nothing moved. Re-run with --apply.")
        return 0

    new_by_id = {c["chunk_id"]: c for c in new}
    stage = dd / "_renumber_stage"
    stage.mkdir(exist_ok=True)
    staged: list[tuple[Path, Path, str, str]] = []
    for o, n in sorted(moves.items()):
        for ext in (".mp3", ".json"):
            src = dd / f"{o}{ext}"
            if src.is_file():
                dst = stage / f"{n}{ext}"
                src.rename(dst)
                staged.append((dst, dd / f"{n}{ext}", o, n))
    for dst, final, o, n in staged:
        if final.exists():
            final.unlink()
        dst.rename(final)
    try:
        stage.rmdir()
    except OSError:
        pass

    # Sidecars carry the chunk id, and idempotency_key is derived from it.
    rewritten = 0
    for o, n in sorted(mapping.items()):
        side = dd / f"{n}.json"
        if not side.is_file():
            continue
        d = json.loads(side.read_text("utf-8"))
        if d.get("chunk_id") == n:
            continue
        d["renumbered_from"] = d.get("chunk_id")
        d["chunk_id"] = n
        d["section"] = new_by_id[n]["section"]
        d["idempotency_key"] = idempotency_key(a.ep, new_by_id[n]["spoken_text"], n)
        d["renumbered_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        side.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", "utf-8")
        rewritten += 1

    # Post-condition: every carried-over chunk's file now sits at its new id with the sha the
    # new script expects, which is precisely what makes the runner skip it.
    bad = []
    for c in new:
        side = dd / f"{c['chunk_id']}.json"
        if not side.is_file():
            continue
        d = json.loads(side.read_text("utf-8"))
        if d.get("text_sha256") != c["text_sha256"]:
            bad.append(c["chunk_id"])
    if bad:
        print(f"POST-CHECK FAILED: {len(bad)} sidecar sha mismatch(es), first {bad[:5]}",
              file=sys.stderr)
        return 1

    # The concat working dir holds decoded WAVs named by the OLD ids; concat_master rewrites
    # every one it needs, but a stale file under a reused name is not worth the argument.
    wav = dd / "_wav"
    removed = 0
    if wav.is_dir():
        for p in wav.glob("VC-*.wav"):
            p.unlink()
            removed += 1

    append_event(a.ep, {
        "event": "voice_chunks_renumbered",
        "episode_id": a.ep, "stage": "audio_generating",
        "old_script": a.old_script, "new_script": a.new_script,
        "chunks_old": len(old), "chunks_new": len(new),
        "renamed": len(moves), "sidecars_rewritten": rewritten,
        "lost": [c["chunk_id"] for c in lost],
        "pending_generation": todo,
        "stale_wavs_removed": removed,
        "model_id": MODEL, "voice_id": VOICE_ID,
        "cost_avoided_note": "renaming is free; only `pending_generation` is billed",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    print(f"\nrenamed {len(moves)} file pair(s), rewrote {rewritten} sidecar(s), "
          f"removed {removed} stale wav(s). POST-CHECK OK.")
    print(f"now run: py -3.11 scripts/gen_narration_case.py --ep {a.ep}   "
          f"(it will generate {len(todo)} chunk(s) and skip {len(mapping)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
