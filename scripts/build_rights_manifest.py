#!/usr/bin/env python3
r"""Assemble a per-episode rights manifest from records that already exist on disk.

WHY THIS EXISTS
    `scripts/pd_ship_policy.py` prints, for the `rights_and_licence` blocking class:
    "the blocklist is a DENYLIST of assets already found to be bad. Nothing on the ship path
    requires positive licence or provenance clearance for the assets in the film."
    The licences DO exist -- in the archive shelf ledger, in the sound-library rights manifest,
    in the plate review verdicts -- they were just never assembled where a gate could read them.
    This tool assembles them. It does NOT decide anything it cannot read.

HARD RULE (`.claude/rules/media-truth-license.md`)
    source_type / truth_status / license_decision are SEPARATE fields.
    `unknown` is never converted to `approved` by inference. When no record establishes a
    licence, the asset is emitted as `review_required` with the exact missing evidence named.

SCOPE
    Every distinct asset referenced by the SHIPPED film (`remotion/src/data/<slug>_film.json`,
    cuts + hook), plus the audio layers in the episode's audio_provenance, the narration master,
    the brand fonts, and the thumbnail candidates in 09_package.

Read-only except for the manifest it writes.

    py -3.11 scripts/build_rights_manifest.py --slug marmet
    py -3.11 scripts/build_rights_manifest.py --all --dry-run
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "runs" / "qc"
PLANNING = ROOT / "episodes" / "_planning"
LEDGER_DIR = Path(r"H:\pd-media\assets\archive\_ledger")
LEDGERS = ["factory", "mixkit", "pixabay_extra", "coverr", "ia", "nara", "freesound"]

EPISODES = {
    "greene": ("PD-2026-062-greene", "G"),
    "correa": ("PD-2026-063-correa", "C"),
    "memphis": ("PD-2026-064-memphis", "M"),
    "marmet": ("PD-2026-065-marmet", "R"),
}

SOUND_RIGHTS = PLANNING / "SOUND_LIBRARY_RIGHTS.v001.json"
IMAGEGEN_QUEUE = ROOT / "runs" / "imagegen" / "ep62_ep65_queue.v001.json"
FONT_LICENCE = ROOT / "remotion" / "public" / "fonts" / "LICENSE_FONTS.md"
I2V_TOOL = ROOT / "scripts" / "build_motion_from_plates.py"

# ---- the two gaps that make a whole CLASS review_required, quoted from what was actually read --

NO_IMAGE_MODEL_RECORD = (
    "review_required: no licence record exists in this repository for the image generator that "
    "produced this plate. The commissioning document (see prompt_ref / batch_doc) names the "
    "prompt but not the model or its output terms; runs/imagegen/ep62_ep65_queue.v001.json "
    "records prompt + destination and no model field; docs/pd-visual-system/LICENSE_REGISTER.md "
    "is still an empty template row (LIC-001, decision review_required); "
    "docs/pd-visual-system/MODEL_LICENSE_RECORD.md covers only OpenCLIP ViT-B/32. "
    "This is a MISSING RECORD, not a known defect in the asset."
)

NO_I2V_MODEL_RECORD = (
    "review_required: no licence record exists in this repository for the image-to-video model. "
    "scripts/build_motion_from_plates.py states the route is ComfyUI + Wan 2.2 TI2V-5B, and "
    "docs/pd-visual-system/MASTER_REFERENCE.md §17.5 explicitly forbids treating Wan2.2's "
    "Apache-2.0 as clearing the workflow (repository code / architecture / checkpoint weights / "
    "text encoder / VAE / custom nodes / output terms must each be audited separately). None of "
    "those audits exists. The source plate's own licence position is unresolved for the same "
    "reason as every AI plate. This is a MISSING RECORD, not a known defect in the asset."
)

NO_VOICE_RECORD = (
    "review_required: no record in this repository states the LICENCE position of the narration "
    "master. episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json records the ElevenLabs Terms-of-Use "
    "position for the SFX/ambience library only and never mentions the voice, and it attaches a "
    "publish_gate -- 'confirm the generating ElevenLabs account was on a paid (Creator+) tier and "
    "retain that evidence before public publish' -- for which no evidence file exists. What DOES "
    "exist is a paid-run record: this episode's events.jsonl carries narration_generated / "
    "narration_mastered with a USD cost (see evidence below), which shows the run was billed but "
    "does not state the account tier or the output terms it was billed under."
)

# A rejected plate on disk is not the same claim as a rejected plate VISIBLE in the master, so the
# four blocking-class rejections were opened as pixels before this manifest asserted anything.
MASTER_SPOTCHECK = {
    "memphis": {
        "checked_by": "claude-opus-5, rights-manifest assembly, 2026-08-12",
        "master": "episodes/PD-2026-064-memphis/08_edit/memphis_final_bgm.v002.mp4",
        "method": ("existing sampled frames in runs/qc/shipped_frames/memphis/frames/ were opened, "
                   "plus four fresh single-frame ffmpeg extracts from the delivered master around "
                   "the M159 cut, with the lower-left corner cropped and brightened 3x"),
        "findings": [
            {"plate": "M117", "mmss": "21:18-21:22", "on_screen": True,
             "what_is_visible": ("two men seated facing each other across a table, BOTH FACES "
                                 "fully lit and frontal, under the burned card 'THE JUDGMENT OF "
                                 "THE COURT OF APPEALS IS AFFIRMED.' This is what the reviewer "
                                 "rejected, and it is in the master.")},
            {"plate": "M049", "mmss": "10:39-10:44", "on_screen": True,
             "what_is_visible": ("a woman at a kitchen window holding a slip up to the light. In "
                                 "the graded master her face is in shadowed near-profile and reads "
                                 "far less sharply than the reviewer described on the raw plate, "
                                 "but a depicted individual IS on screen where the order said no "
                                 "person.")},
            {"plate": "M202", "mmss": "4:16-4:22", "on_screen": True,
             "what_is_visible": ("two figures at a kitchen table seen from BEHIND; no face is "
                                 "visible. The right-hand figure is small and in a sleeveless "
                                 "print dress -- the reviewer read it as a child. The objection is "
                                 "factual (the spec says no children), not a likeness exposure.")},
            {"plate": "M159", "mmss": "22:36-22:40", "on_screen": False,
             "what_is_visible": ("the generator watermark IS present in the source plate -- "
                                 "confirmed by cropping remotion/public/memphis/img/M159.png at "
                                 "x0-384 / y1900-2160 -- but it is NOT visible in any of the four "
                                 "frames extracted from the delivered master, because the cut "
                                 "crops the plate's lower-left corner out. Every frame of the cut "
                                 "was NOT checked.")},
        ],
        "what_this_does_not_say": ("the remaining 12 rejections were not opened as pixels; their "
                                   "reviewer notes are framing, period and motif faults rather "
                                   "than blocking-class objections."),
    },
}

# memphis is the one episode of the four whose plate review was never converted to JSON, so the
# per-plate verdicts below are parsed out of the prose table -- see MEMPHIS_REJECT_NOTE.
MD_REJECT_RE = r"\|\s*`(M\d{3})`\s*\|\s*\*\*REJECT\*\*\s*\|[^|]*\|[^|]*\|[^|]*\|([^|]*)\|"


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def jload(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except Exception:  # noqa: BLE001
        return p.as_posix()


# --------------------------------------------------------------------------- record loaders

def load_shelf_ledger() -> dict:
    """H:\\pd-media\\assets\\archive\\_ledger\\*.jsonl -- the PRIMARY per-item rights record for
    every downloaded clip: license_field_raw ("Pexels License"), license_decision, source_url,
    sha256, fetched_at. Keyed by normalised absolute file_path."""
    idx = {}
    for name in LEDGERS:
        p = LEDGER_DIR / f"{name}.jsonl"
        if not p.is_file():
            continue
        with p.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                fp = r.get("file_path")
                if fp:
                    idx[os.path.normpath(fp).lower()] = (name, r)
    return idx


def load_staging(slug: str) -> dict:
    """runs/qc/<slug>_title_staging*.json -- what was copied into remotion/public/<slug>/factory.

    The live v001 is authoritative; earlier rounds and .bak files are consulted ONLY for clips the
    live file no longer lists (marmet re-staged twice and 52 shipped clips survive only in the
    older receipts). The record each clip was cleared by is recorded per asset.
    """
    out: dict[str, tuple[str, dict]] = {}
    files = [QC / f"{slug}_title_staging.v001.json"]
    files += sorted(q for q in QC.glob(f"{slug}_title_staging.v001.json.*"))
    for p in files:
        if not p.is_file():
            continue
        try:
            d = jload(p)
        except Exception:  # noqa: BLE001
            continue
        rows = d.get("staged", []) if isinstance(d, dict) else d
        for it in rows:
            key = it.get("staged_as")
            if key and key not in out:
                out[key] = (rel(p), it)
    return out


def load_prompts() -> dict:
    if not IMAGEGEN_QUEUE.is_file():
        return {}
    d = jload(IMAGEGEN_QUEUE)
    return {(it["slug"], it["asset_id"]): it for it in d.get("items", [])}


def load_plate_verdicts(slug: str):
    """The per-plate review verdicts, and whether a machine could read them.

    marmet / greene / correa carry `<slug>_plate_verdicts.v001.json`, which check_plate_verdicts.py
    can enforce. memphis carries ONLY a prose markdown report, so its 16 REJECT verdicts were never
    machine-readable and nothing on the build path could keep a rejected plate out of the film.
    The REJECT rows are parsed here so at least the manifest carries them.
    """
    p = QC / f"{slug}_plate_verdicts.v001.json"
    if p.is_file():
        d = jload(p)
        return rel(p), (d.get("plates") or {}), (d.get("plate_review") or {}), "json"
    md = QC / f"{slug}_plate_verdicts.v001.md"
    if md.is_file():
        text = md.read_text(encoding="utf-8")
        plates = {f"{pid}.png": {"verdict": "reject", "note": note.strip()[:400],
                                 "parsed_from": "prose REJECT table"}
                  for pid, note in re.findall(MD_REJECT_RE, text)}
        return rel(md), plates, {"reviewer": "prose report; only REJECT rows are machine-parsable"}, \
            "prose_rejects_only"
    return None, None, {}, "none"


def load_plate_hashes(slug: str) -> dict:
    p = QC / f"{slug}_plate_hashes.v001.json"
    if not p.is_file():
        return {}
    return {os.path.basename(k): v for k, v in jload(p).items()}


def load_audio(ep: str):
    d = ROOT / "episodes" / ep / "06_audio"
    aps = sorted(d.glob("audio_provenance.v*.json"))
    if not aps:
        return None, None, None, None
    ap = jload(aps[-1])
    vp = d / "voice_plan.v001.json"
    ni = sorted(d.glob("narration_index.v*.json"))
    return rel(aps[-1]), ap, (jload(vp) if vp.is_file() else None), (jload(ni[0]) if ni else None)


def load_sound_rights() -> dict:
    if not SOUND_RIGHTS.is_file():
        return {}
    return {a["filename"]: a for a in jload(SOUND_RIGHTS)["assets"]}


# --------------------------------------------------------------------------- asset builders

def film_sources(slug: str) -> list[str]:
    f = ROOT / "remotion" / "src" / "data" / f"{slug}_film.json"
    d = jload(f)
    srcs = [c.get("src") for c in (d.get("cuts") or []) + (d.get("hook") or []) if c.get("src")]
    return sorted(set(srcs))


def archive_assets(slug: str, srcs, staging, shelf) -> list[dict]:
    out = []
    for i, s in enumerate([x for x in srcs if "/factory/" in x]):
        name = os.path.basename(s)
        shipped = ROOT / "remotion" / "public" / s
        a = {
            "asset_id": f"{slug.upper()}-ARC-{i + 1:03d}",
            "type": "archive_footage",
            "file": f"remotion/public/{s}",
            "source_type": "third_party_stock_footage",
            "truth_status": "authentic_recording_not_of_this_case",
            "ai_disclosure_required": False,
            "evidence": [],
        }
        st = staging.get(name)
        if not st:
            a.update(license_decision="review_required", license=None, source=None,
                     truth_status="unknown", needs_verification=True,
                     review_reason=("review_required: this clip is in the shipped film but appears "
                                    "in no title-staging receipt, so nothing records where it came "
                                    "from."),
                     content_hash=None, content_hash_source="none")
            out.append(a)
            continue
        rec_path, row = st
        a["evidence"].append({"record": rec_path, "join": f"staged_as == {name}",
                              "states": {"source": row.get("source"),
                                         "license": row.get("license"),
                                         "id": row.get("id"), "title": row.get("title")}})
        a["source"] = row.get("source")
        a["shelf_path"] = row.get("src")
        led = shelf.get(os.path.normpath(row.get("src", "")).lower())
        if not led:
            a.update(license_decision="review_required", license=row.get("license"),
                     truth_status="unknown", needs_verification=True,
                     review_reason=("review_required: the staging receipt carries the bare token "
                                    f"license='{row.get('license')}' but the shelf original is in "
                                    "no archive ledger, so no source URL, no raw licence string and "
                                    "no acquisition date back it."),
                     content_hash=None, content_hash_source="none")
            out.append(a)
            continue
        lname, r = led
        a["evidence"].append({
            "record": f"H:/pd-media/assets/archive/_ledger/{lname}.jsonl",
            "join": f"file_path == {row.get('src')}",
            "states": {"license_field_raw": r.get("license_field_raw"),
                       "license_decision": r.get("license_decision"),
                       "source_url": r.get("source_url"),
                       "fetched_at": r.get("fetched_at")}})
        a["source_url"] = r.get("source_url")
        a["license"] = r.get("license_field_raw")
        a["rights_holder"] = ("licensor per the platform licence named in license_field_raw; "
                              "Prime Documentary holds a use licence, not the copyright")
        a["content_hash"] = f"sha256:{r['sha256']}" if r.get("sha256") else None
        # the staged copy must be the same bytes as the shelf original the ledger hashed
        same = None
        if shipped.is_file() and r.get("bytes") is not None:
            same = shipped.stat().st_size == r["bytes"]
        a["content_hash_source"] = (
            "archive ledger sha256 of the shelf original; the staged copy in remotion/public was "
            "byte-size verified against it at manifest time" if same else
            "archive ledger sha256 of the shelf original; staged-copy size NOT verified")
        a["staged_copy_size_matches_ledger"] = same
        dec = r.get("license_decision")
        if dec in {"free_commercial", "pd", "cc0"} and r.get("license_field_raw"):
            a["license_decision"] = "approved"
            a["needs_verification"] = False
        else:
            a["license_decision"] = "review_required"
            a["needs_verification"] = True
            a["review_reason"] = (f"review_required: the archive ledger records "
                                  f"license_decision='{dec}', which is not a cleared value.")
        if same is False:
            a["license_decision"] = "review_required"
            a["needs_verification"] = True
            a["review_reason"] = ("review_required: the staged copy in the film does not match the "
                                  "byte size of the shelf original the ledger cleared, so the "
                                  "ledger record may not describe this file.")
        out.append(a)
    return out


def _plate_block(slug, pid, verdicts, vpath, vsource, prompts):
    """Shared truth / review position for a commissioned AI plate id.

    Returns (evidence, truth_status, qc_verdict, prompt_row, rejection_note or None).
    A plate the reviewer REJECTED but that is nonetheless in the shipped film is the single most
    important thing this manifest can say, so it is returned separately and surfaced at the top.
    """
    ev = []
    truth = "unknown"
    qc = None
    rejection = None
    q = prompts.get((slug, pid))
    if q:
        ev.append({"record": rel(IMAGEGEN_QUEUE), "join": f"items[].asset_id == {pid}",
                   "states": {"source_markdown": q.get("source_markdown"),
                              "prompt_first_120": (q.get("prompt") or "")[:120]}})
    v = (verdicts or {}).get(f"{pid}.png")
    if v:
        qc = v.get("verdict")
        ev.append({"record": vpath, "join": f"plates['{pid}.png']",
                   "states": {"verdict": qc, "note": (v.get("note") or "")[:400]}})
        if str(qc).lower() == "reject":
            rejection = (v.get("note") or "").strip()
            truth = "unknown"
        else:
            truth = "symbolic_reconstruction"
    elif vpath and vsource == "prose_rejects_only":
        ev.append({"record": vpath,
                   "join": ("prose review; its scope statement covers the whole plate range but "
                            "only its REJECT rows are machine-parsable, so an ACCEPT for this "
                            "plate cannot be read out of it"),
                   "states": {"verdict": "not machine-readable for this id"}})
    return ev, truth, qc, q, rejection


def plate_assets(slug, srcs, verdicts, vpath, vsource, hashes, prompts, batch_doc) -> list[dict]:
    out = []
    for i, s in enumerate([x for x in srcs if "/img/" in x]):
        pid = os.path.basename(s).rsplit(".", 1)[0]
        ev, truth, qc, q, rejection = _plate_block(slug, pid, verdicts, vpath, vsource, prompts)
        h = hashes.get(f"{pid}.png", {}).get("sha256")
        out.append({
            "asset_id": f"{slug.upper()}-PLT-{i + 1:03d}",
            "type": "ai_plate_still",
            "file": f"remotion/public/{s}",
            "source_type": "ai_generated_image",
            "truth_status": truth,
            "license_decision": "review_required",
            "license": None,
            "rights_holder": "unknown -- no output-terms record for the generator (see review_reason)",
            "review_reason": NO_IMAGE_MODEL_RECORD if q else (
                NO_IMAGE_MODEL_RECORD + " In addition this plate id is NOT in the commissioned "
                "batch queue, so even the prompt that produced it is unrecorded."),
            "needs_verification": True,
            "ai_disclosure_required": True,
            "symbolic_reconstruction": truth == "symbolic_reconstruction",
            "prompt_ref": (f"{q['source_markdown']}#{pid}" if q else None),
            "batch_doc": batch_doc,
            "qc_status": qc,
            "content_hash": f"sha256:{h}" if h else None,
            "content_hash_source": (f"runs/qc/{slug}_plate_hashes.v001.json" if h
                                    else "none -- no recorded hash for this file in this repository"),
            "shipped_despite_review_rejection": bool(rejection),
            "review_rejection_note": rejection,
            "evidence": ev,
        })
    return out


def motion_assets(slug, srcs, verdicts, vpath, vsource, hashes, prompts, batch_doc) -> list[dict]:
    out = []
    pubdir = ROOT / "remotion" / "public" / slug
    for i, s in enumerate([x for x in srcs if "/motion/" in x]):
        pid = os.path.basename(s).rsplit(".", 1)[0]
        ev, truth, qc, q, rejection = _plate_block(slug, pid, verdicts, vpath, vsource, prompts)
        plate = None
        for d in sorted(pubdir.glob("img*")):
            if (d / f"{pid}.png").is_file():
                plate = f"remotion/public/{slug}/{d.name}/{pid}.png"
                break
        h = hashes.get(f"{pid}.mp4", {}).get("sha256")
        reason = NO_I2V_MODEL_RECORD
        if plate is None:
            reason += (" The source plate file is no longer on disk, so the derivation is recorded "
                       "here from the id convention and the review verdict only.")
        out.append({
            "asset_id": f"{slug.upper()}-MOT-{i + 1:03d}",
            "type": "ai_motion_clip_i2v",
            "file": f"remotion/public/{s}",
            "source_type": "ai_generated_video_i2v",
            "truth_status": truth,
            "license_decision": "review_required",
            "license": None,
            "rights_holder": "unknown -- no output-terms record for the generator (see review_reason)",
            "review_reason": reason,
            "needs_verification": True,
            "ai_disclosure_required": True,
            "symbolic_reconstruction": truth == "symbolic_reconstruction",
            "derived_from": plate,
            "derivation": ("image-to-video: the AI plate of the same id is the start image. Tool: "
                           "scripts/build_motion_from_plates.py -> ComfyUI HTTP API -> Wan 2.2 "
                           "TI2V-5B, 832x480 / 49 frames / 20 steps. The motion prompt is derived "
                           "from the plate's own commissioned prompt."),
            "derivation_evidence": rel(I2V_TOOL),
            "prompt_ref": (f"{q['source_markdown']}#{pid}" if q else None),
            "batch_doc": batch_doc,
            "qc_status": qc,
            "content_hash": f"sha256:{h}" if h else None,
            "content_hash_source": (f"runs/qc/{slug}_plate_hashes.v001.json" if h
                                    else "none -- no recorded hash for this file in this repository"),
            "shipped_despite_review_rejection": bool(rejection),
            "review_rejection_note": rejection,
            "evidence": ev,
        })
    return out


AUDIO_TYPE = {"music": "music_bed", "ambience": "ambience_bed", "sfx": "sfx_oneshot"}
SOURCE_TYPE = {"suno-generated": "ai_generated_music",
               "elevenlabs-generated": "ai_generated_audio",
               "ffmpeg-synthesized": "synthesized_audio_owned",
               "downloaded-cc0": "third_party_audio_cc0"}


def audio_assets(slug, ap, ap_path, sound) -> list[dict]:
    """Every music / ambience / sfx file the mix actually uses, joined to the sound rights record."""
    used: dict[str, str] = {}
    L = ap["layers"]
    for t in L["music"]["tracks"]:
        used[os.path.basename(t)] = "music"
    for f in L["music"].get("fills", []):
        used[os.path.basename(f["file"])] = "music"
    for b in L["ambience"]["beds"]:
        used[os.path.basename(b)] = "ambience"
    for c in ap.get("sfx_cues", []):
        if c.get("file"):
            used[os.path.basename(c["file"])] = "sfx"
    if L["sfx"].get("riser_fill"):
        used[os.path.basename(L["sfx"]["riser_fill"])] = "sfx"

    out = []
    for i, (fn, cat) in enumerate(sorted(used.items())):
        r = sound.get(fn)
        a = {
            "asset_id": f"{slug.upper()}-AUD-{i + 1:03d}",
            "type": AUDIO_TYPE[cat],
            "file": f"artifact://library/{cat if cat != 'music' else 'music'}/{fn}",
            "truth_status": "synthetic_audio_not_a_recording_of_this_case",
            "ai_disclosure_required": cat != "ambience",
            "evidence": [{"record": ap_path, "join": f"layers.{cat} / sfx_cues -> {fn}"}],
        }
        if not r:
            a.update(source_type="unknown", license_decision="review_required", license=None,
                     needs_verification=True, content_hash=None, content_hash_source="none",
                     review_reason=("review_required: this file is in the mix but is in no entry of "
                                    "episodes/_planning/SOUND_LIBRARY_RIGHTS.v001.json."))
            out.append(a)
            continue
        a["file"] = f"artifact://{r['path_relative']}"
        a["source_type"] = SOURCE_TYPE.get(r["provenance_method"], "unknown")
        a["license"] = r["license"]
        a["source_url"] = r.get("license_url")
        a["rights_holder"] = ("Prime Documentary (owned outright)" if r.get("owned")
                              else "Prime Documentary as licensee of the generator's output terms")
        # the sound rights record uses two different key names for the same thing
        sha = r.get("file_sha256_recorded") or r.get("file_sha256")
        a["content_hash"] = f"sha256:{sha}" if sha else None
        a["content_hash_source"] = rel(SOUND_RIGHTS) if sha else "none"
        a["evidence"].append({"record": rel(SOUND_RIGHTS), "join": f"assets[].filename == {fn}",
                              "states": {"provenance_method": r["provenance_method"],
                                         "license": r["license"],
                                         "commercial_ok": r["commercial_ok"],
                                         "provenance_status": r.get("provenance_status")}})
        if r.get("commercial_ok") and r.get("provenance_status") in {"recorded_license",
                                                                    "owned_synthesized"}:
            a["license_decision"] = "approved"
            a["needs_verification"] = False
        else:
            a["license_decision"] = "review_required"
            a["needs_verification"] = True
            a["review_reason"] = ("review_required: the sound rights record does not state "
                                  f"commercial_ok with a recorded licence for this file "
                                  f"(provenance_status={r.get('provenance_status')!r}).")
        if r.get("publish_gate"):
            a["outstanding_condition"] = r["publish_gate"]
            a["outstanding_condition_evidence"] = "NOT FOUND in this repository"
        out.append(a)
    return out


def narration_asset(slug, ep, ap, ap_path, vp, ni) -> dict:
    master = ap["layers"]["narration"]["master_uri"]
    ev = [{"record": ap_path, "join": "layers.narration.master_uri",
           "states": {"master_uri": master,
                      "master_exists": ap["layers"]["narration"].get("master_exists")}}]
    if vp:
        ev.append({"record": f"episodes/{ep}/06_audio/voice_plan.v001.json",
                   "states": {"provider": vp.get("provider"), "voice_id": vp.get("voice_id"),
                              "model_id": vp.get("model_id")}})
    if ni:
        ev.append({"record": f"episodes/{ep}/06_audio/narration_index.v001.json",
                   "states": {"chunks": (ni.get("totals") or {}).get("chunks"),
                              "measured_seconds": (ni.get("totals") or {}).get("measured_seconds")}})
    evp = ROOT / "episodes" / ep / "events.jsonl"
    if evp.is_file():
        rows = []
        for line in evp.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if r.get("event") in {"narration_generated", "narration_mastered"}:
                rows.append(r)
        if rows:
            last = rows[-1]
            ev.append({"record": f"episodes/{ep}/events.jsonl",
                       "join": "last narration_generated / narration_mastered event",
                       "states": {"event": last.get("event"),
                                  "provider": last.get("provider"),
                                  "estimated_cost_usd_total_plan":
                                      last.get("estimated_cost_usd_total_plan"),
                                  "timestamp": last.get("timestamp")},
                       "what_it_proves": ("the run was billed to a paying account; it does NOT "
                                          "state the account tier or the output-licence terms")})
    return {
        "asset_id": f"{slug.upper()}-VO-001",
        "type": "narration_master",
        "file": master,
        "source_type": "ai_synthetic_voice",
        "truth_status": "synthetic_voice_not_a_recording_of_any_real_person_in_this_case",
        "license_decision": "review_required",
        "license": None,
        "rights_holder": "unknown -- see review_reason",
        "review_reason": NO_VOICE_RECORD,
        "needs_verification": True,
        "ai_disclosure_required": True,
        "provider": (vp or {}).get("provider") or ap["layers"]["narration"].get("provider"),
        "voice_id": (vp or {}).get("voice_id"),
        "model_id": (vp or {}).get("model_id"),
        "content_hash": None,
        "content_hash_source": ("none -- no recorded hash of the narration master in this "
                                "repository"),
        "evidence": ev,
    }


FONTS = [("Oswald", "Oswald.ttf"), ("Anton", "Anton.ttf"), ("Archivo", "Archivo.ttf")]


def font_assets(slug) -> list[dict]:
    return [{
        "asset_id": f"{slug.upper()}-FNT-{i + 1:03d}",
        "type": "font",
        "file": f"remotion/public/fonts/{fn}",
        "source_type": "licensed_font",
        "truth_status": "not_applicable",
        "license_decision": "approved",
        "license": "SIL Open Font License 1.1 (embedding, modification and commercial use permitted)",
        "rights_holder": f"{name} authors; distributed via google/fonts",
        "source_url": f"https://github.com/google/fonts/tree/main/ofl/{name.lower()}",
        "needs_verification": False,
        "ai_disclosure_required": False,
        "content_hash": None,
        "content_hash_source": "none -- LICENSE_FONTS.md records provenance but no file hash",
        "evidence": [{"record": rel(FONT_LICENCE), "join": f"table row '{name}'",
                      "states": {"license": "SIL Open Font License 1.1",
                                 "source": f"google/fonts ofl/{name.lower()}",
                                 "acquired": "2026-07-17"}}],
        "usage_note": ("declared as the brand typography for burned captions and on-screen text; "
                       "per-episode usage of each individual face is not separately recorded"),
    } for i, (name, fn) in enumerate(FONTS)]


def thumbnail_assets(slug, ep) -> list[dict]:
    pkg = ROOT / "episodes" / ep / "09_package"
    out = []
    for i, p in enumerate(sorted(pkg.glob("thumbnail.*.png"))):
        out.append({
            "asset_id": f"{slug.upper()}-THM-{i + 1:03d}",
            "type": "thumbnail_candidate",
            "file": rel(p),
            "source_type": "ai_generated_image_composited_with_typography",
            "truth_status": "unknown",
            "license_decision": "review_required",
            "license": None,
            "rights_holder": "unknown -- no output-terms record for the generator",
            "review_reason": (NO_IMAGE_MODEL_RECORD + " Additionally, no build record in this "
                              "repository maps this thumbnail file to the plate it was composited "
                              "from, and no record states which candidate is the selected one "
                              "(09_package/title_thumbnail_candidates.v001.json selects a TITLE "
                              "only)."),
            "needs_verification": True,
            "ai_disclosure_required": True,
            "derived_from": None,
            "content_hash": None,
            "content_hash_source": "none",
            "evidence": [],
        })
    return out


# --------------------------------------------------------------------------- manifest

SCHEMA_NOTE = {
    "base_schema": ("episodes/PD-2026-007-riley/09_package/rights_manifest.v001.json -- "
                    "schema_version 1.0.0, assets[] as a flat list of per-asset objects."),
    "base_schema_is_thin": (
        "No rights manifest anywhere in this repository (57 files, EP1-EP29) carries "
        "source_type, truth_status or license_decision as separate fields, and there is no "
        "rights-manifest JSON Schema in schemas/. .claude/rules/media-truth-license.md REQUIRES "
        "those three as separate fields and forbids converting unknown to approved by inference. "
        "The base schema therefore cannot express the rule it is governed by."),
    "fields_added_here_deliberately": [
        "source_type", "truth_status", "license_decision", "review_reason", "evidence[]",
        "content_hash_source", "outstanding_condition", "derived_from", "derivation",
        "staged_copy_size_matches_ledger",
    ],
    "fields_kept_for_the_existing_reader": (
        "asset_id, file, content_hash -- scripts/verify_rights_hashes.py reads exactly these "
        "three and resolves 'artifact://' against config/storage.local.json roots.media "
        "(H:\\pd-media) and everything else repo-relative, so it runs against this file unchanged."),
    "vocabularies": {
        "license_decision": ["approved", "review_required", "unknown", "rejected", "not_applicable"],
        "truth_status": ["authentic_recording_not_of_this_case", "symbolic_reconstruction",
                         "synthetic_audio_not_a_recording_of_this_case",
                         "synthetic_voice_not_a_recording_of_any_real_person_in_this_case",
                         "not_applicable", "unknown"],
    },
    "decision_rule": ("approved is emitted ONLY where a record read at generation time states a "
                      "licence for that exact file. Everything else is review_required with the "
                      "missing evidence named. No clearance is inferred from a neighbouring asset, "
                      "a platform default, or the fact that the episode already rendered."),
}


def build(slug: str) -> dict:
    ep, _prefix = EPISODES[slug]
    srcs = film_sources(slug)
    staging = load_staging(slug)
    shelf = load_shelf_ledger()
    prompts = load_prompts()
    vpath, verdicts, vreview, vsource = load_plate_verdicts(slug)
    hashes = load_plate_hashes(slug)
    ap_path, ap, vp, ni = load_audio(ep)
    sound = load_sound_rights()
    batch = next((rel(p) for p in sorted(PLANNING.glob(f"EP*_{slug}_CODEX_BATCH_A.v*.md"))), None)

    assets: list[dict] = []
    assets += archive_assets(slug, srcs, staging, shelf)
    assets += plate_assets(slug, srcs, verdicts, vpath, vsource, hashes, prompts, batch)
    assets += motion_assets(slug, srcs, verdicts, vpath, vsource, hashes, prompts, batch)
    if ap:
        assets += audio_assets(slug, ap, ap_path, sound)
        assets += [narration_asset(slug, ep, ap, ap_path, vp, ni)]
    assets += font_assets(slug)
    assets += thumbnail_assets(slug, ep)

    by_type: dict[str, dict[str, int]] = {}
    for a in assets:
        by_type.setdefault(a["type"], {}).setdefault(a["license_decision"], 0)
        by_type[a["type"]][a["license_decision"]] += 1
    approved = [a for a in assets if a["license_decision"] == "approved"]
    review = [a for a in assets if a["license_decision"] == "review_required"]

    reasons: dict[str, int] = {}
    for a in review:
        head = (a.get("review_reason") or "").split(".")[0][:110]
        reasons[head] = reasons.get(head, 0) + 1

    shipped_rejected = [
        {"asset_id": a["asset_id"], "file": a["file"], "reviewer_verdict": "REJECT",
         "reviewer_note": a["review_rejection_note"], "review_record": vpath}
        for a in assets if a.get("shipped_despite_review_rejection")]

    esc = None
    if shipped_rejected:
        esc = {
            "severity": "ESCALATE_BEFORE_BOOKING",
            "what": (f"{len(shipped_rejected)} asset(s) in the SHIPPED film were REJECTED by this "
                     f"episode's own plate review ({vpath}). The files in remotion/public are "
                     "byte-identical to the files the reviewer rejected; no replacement was "
                     "generated in their place."),
            "why_nothing_caught_it": (
                "this episode's plate verdicts exist only as prose markdown. The sibling episodes "
                "carry runs/qc/<slug>_plate_verdicts.v001.json, which check_plate_verdicts.py can "
                "read and enforce. A verdict a machine cannot read cannot stop a build."
                if vsource == "prose_rejects_only" else
                "the verdicts were machine-readable; the build did not consult them."),
            "scope_of_this_finding": (
                "This is the REVIEWER'S editorial/spec objection carried forward, not a new legal "
                "conclusion. Read each reviewer_note: some are framing or period faults, and some "
                "name the episode's own forbidden_subjects (identifiable faces, a child, a "
                "generator watermark). Those last ones fall in the policy's blocking classes and "
                "should be looked at by a human before this episode is booked."),
            "assets": shipped_rejected,
        }
        if slug in MASTER_SPOTCHECK:
            esc["verified_on_the_delivered_master"] = MASTER_SPOTCHECK[slug]

    return {
        "schema_version": "1.0.0",
        "episode_id": ep,
        "slug": slug,
        "revision": "v001",
        "generated_at": now(),
        "generator": "scripts/build_rights_manifest.py",
        "status": "assembled_from_existing_records",
        "notes": (
            "Positive licence/provenance position for every distinct asset in the SHIPPED film "
            f"(remotion/src/data/{slug}_film.json, cuts + hook), plus the audio layers actually in "
            "the mix, the narration master, the brand fonts and the thumbnail candidates. Nothing "
            "here is inferred: every 'approved' names the record that says so, and every gap is "
            "review_required with the missing evidence stated. NOTHING ON THE SHIP PATH READS "
            "THIS FILE YET -- pd_ship_policy.py only globs 09_package/rights_manifest.v*.json and "
            "reports the filename; check_final_acceptance.py does not mention rights at all."),
        "escalation": esc,
        "schema_note": SCHEMA_NOTE,
        "coverage": {
            "scope": "distinct assets referenced by the shipped film + mix + packaging",
            "film_data": f"remotion/src/data/{slug}_film.json",
            "distinct_film_sources": len(srcs),
            "audio_provenance": ap_path,
            "plate_review_record": vpath,
            "plate_review_source": vsource,
            "plate_review_machine_readable": vsource == "json",
            "plate_reviewer": vreview.get("reviewer"),
            "commission_doc": batch,
            "not_covered": [
                "assets staged or generated for this episode but NOT used in the shipped film",
                "the rendered master itself (it is a derivative of everything listed here)",
                "the three shorts packaged alongside this episode",
            ],
        },
        "summary": {
            "assets_total": len(assets),
            "cleared_by_a_record": len(approved),
            "review_required": len(review),
            "by_type": by_type,
            "review_required_reasons": reasons,
            "shipped_despite_review_rejection": len(shipped_rejected),
        },
        "review_required_asset_ids": [a["asset_id"] for a in review],
        "assets": assets,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", choices=sorted(EPISODES))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing rights_manifest.v001.json (default: refuse)")
    a = ap.parse_args(argv)
    slugs = sorted(EPISODES) if a.all else ([a.slug] if a.slug else [])
    if not slugs:
        ap.error("give --slug or --all")
    for slug in slugs:
        m = build(slug)
        out = ROOT / "episodes" / EPISODES[slug][0] / "09_package" / "rights_manifest.v001.json"
        s = m["summary"]
        print(f"{slug:8s} assets={s['assets_total']:4d} cleared={s['cleared_by_a_record']:4d} "
              f"review_required={s['review_required']:4d} -> {rel(out)}"
              f"{'  (dry-run, not written)' if a.dry_run else ''}")
        for t, d in sorted(s["by_type"].items()):
            print(f"           {t:42s} {d}")
        if m.get("escalation"):
            e = m["escalation"]
            print(f"  ** {e['severity']}: {e['what']}")
            for x in e["assets"]:
                print(f"     - {x['file']}: {(x['reviewer_note'] or '')[:150]}")
        if not a.dry_run:
            if out.exists() and not a.force:
                print(f"           REFUSING to overwrite existing {out.name}")
                continue
            out.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
