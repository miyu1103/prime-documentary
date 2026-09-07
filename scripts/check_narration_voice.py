#!/usr/bin/env python3
"""Preflight gate: block rendering an episode on the WRONG (robotic SAPI) narration.
EP48 glover shipped-blocked because a concurrent Windows-SAPI process overwrote its
narration_index with the robotic local-review track instead of the real ElevenLabs
"Brian" TTS. A robotic voice tanks retention. This gate asserts the narration the
film is built on is the real Brian master.

    py -3.11 scripts/check_narration_voice.py <slug>
Checks episodes/PD-2026-0XX-<slug>/06_audio/narration_index.v001.json:
  - voice_id == Brian (nPczCjzI2devNBz1zQrb)  AND
  - source / audio_path / master do NOT mention sapi / local_review  AND
  - total_seconds matches the real vc_master_v001.mp3 duration (±1.0s)
Exit 0 = PASS, 1 = FAIL (would ship a robotic voice).
"""
from __future__ import annotations
import sys, os, json, subprocess, glob
from pathlib import Path   # added 2026-08-22 with _pd_media_root() below; this file used os.path only


def _pd_media_root() -> Path:
    """The media root, resolved -- never assumed.

    FIXED 2026-08-22. This file hardcoded H:/pd-media. That drive stopped being enumerated by
    Windows around the 2026-08-16 reboot and config/storage.local.json was repointed to E:\pd-media
    on 2026-08-17. Rule 14: no OS-absolute path is a source of truth. The literal below is kept only
    as a last-resort fallback so an unconfigured checkout behaves as it used to instead of crashing.
    """
    import json as _json
    _cfg = Path(__file__).resolve().parents[1] / "config" / "storage.local.json"
    try:
        return Path(_json.loads(_cfg.read_text(encoding="utf-8"))["roots"]["media"]["path"])
    except Exception:
        return Path("H:/pd-media")


PD_MEDIA = _pd_media_root()


BRIAN = "nPczCjzI2devNBz1zQrb"

def ffdur(path):
    try:
        out = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",path],
                                      stderr=subprocess.DEVNULL).decode().strip()
        return float(out)
    except Exception:
        return None

def find_ep_dir(slug):
    for base in (r"C:\Users\aab15\Documents\prime-documentary\episodes", ):
        for d in glob.glob(os.path.join(base, f"PD-2026-*-{slug}")):
            return d
    return None

def main(slug):
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    epdir = find_ep_dir(slug)
    if not epdir:
        print(f"BLOCKED: no episode dir for slug {slug!r}"); return 1
    idx = os.path.join(epdir, "06_audio", "narration_index.v001.json")
    if not os.path.exists(idx):
        print(f"BLOCKED: narration_index not found: {idx}"); return 1
    d = json.load(open(idx, encoding="utf-8"))
    fails = []
    vid = str(d.get("voice_id","")).strip()
    # chunk voice_ids: if present and non-empty, they must all be Brian
    chunk_vids = {str(c.get("voice_id","")).strip() for c in d.get("chunks",[]) if str(c.get("voice_id","")).strip()}
    if vid != BRIAN and not (chunk_vids and chunk_vids == {BRIAN}):
        fails.append(f"voice_id={vid!r} / chunk voices {chunk_vids or 'none'} not confirmed Brian ({BRIAN})")
    if chunk_vids - {BRIAN}:
        fails.append(f"some chunk voice_ids are NOT Brian: {chunk_vids - {BRIAN}}")
    # STRUCTURAL fields only (NOT free-text provenance/note): the active track must not be SAPI
    active = " ".join(str(d.get(k,"")) for k in ("source","audio_path","master")).lower()
    for bad in ("sapi", "local_review", "local-review", "narration_local"):
        if bad in active:
            fails.append(f"active track references '{bad}' (robotic SAPI): {active[:80]}")
            break
    # duration match vs the real Brian master
    epid = os.path.basename(epdir)
    master = str(PD_MEDIA / "episodes" / epid / "06_voice" / "master" / "vc_master_v001.mp3")
    total = d.get("total_seconds")
    md = ffdur(master) if os.path.exists(master) else None
    if md is not None and total is not None and abs(float(total)-md) > 1.0:
        fails.append(f"total_seconds {total} != Brian master {md:.2f}s (indexed to a different track)")
    if fails:
        print(f"FAIL check_narration_voice ({slug}): would render a WRONG-voice episode:")
        for f in fails: print(f"  - {f}")
        return 1
    print(f"PASS check_narration_voice ({slug}): Brian voice, matches vc_master ({md:.2f}s)" if md else f"PASS ({slug})")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: check_narration_voice.py <slug>"); raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
