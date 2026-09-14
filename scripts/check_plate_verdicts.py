#!/usr/bin/env python
"""Every GENERATED PLATE carries its own verdict, bound to the picture that was judged.

WHY THIS FILE EXISTS (EP66 openfields -> EP67/68/69, 2026-08-11)
-----------------------------------------------------------------
Measured on 2026-08-11, the two halves of this channel's visual supply were not guarded alike:

    check_pool_frames    wired into check_episode_inputs.py + preflight_render_gate.py  BLOCKS
    check_plate_qc       does not exist
    check_pool_faces     wired into: NOTHING
    qc_delivered_plates  wired into: NOTHING

ARCHIVE FOOTAGE HAD A BLOCKING PRE-BUILD GATE. GENERATED PLATES HAD NONE. Every EP66 plate
defect came through that hole and every one was found only because somebody was asked to look:

  * L170 a ROUND POLE where the callback to L075 needed a squared timber post
  * L146 a manufacturer WORDMARK on a tailgate that survived two [NEG] bans
  * L236 FUSED FINGERS on the raised hand -- the same defect it had been re-ordered to fix
  * a licence plate, and 21 further plates that had to be re-ordered as batch C

"Somebody was asked to look" is not a gate. It is a habit, and habits are not on the path.
This puts the same question on the path, at the stage where acting on it costs one image
instead of a four-hour re-render.

WHAT IT IS NOT
--------------
IT DOES NOT LOOK AT A PICTURE. Not one pixel of any plate is judged here. There is no vision
model, no OCR, no glyph detector, no hand-anatomy check and no subject-match check in this
file, and there will not be one -- EP66's own review recorded an MSER "glyph row" detector
being built and thrown away because its top-ranked plate out of 260 was a patch of grass.

This file is a FILING CLERK with a lock on the door. It answers exactly four questions:

    does every plate in the set have a verdict?
    is that verdict about the picture that is on disk right now?
    is any verdict still unresolved?
    is the plate the SIZE the episode's own order asked for?  (added 2026-08-11)

The fourth reads thirty-three bytes of the PNG header -- the IHDR, which carries width and
height. That is a fact about the file, not a judgement about the picture, and it is the one
number a reviewer cannot see by looking. EP67 delivered 88 of its first 104 plates at 1672x941
against an order that says "Long edge >= 3840" twice; the only thing that measured it before
the render was a watcher somebody happened to start at plate 104. See order_pixel_contract.

Every content judgement -- does this match its beat, is that a wordmark, are those five
fingers, is the upper 40% clean -- is supplied by a human or a vision pass, and this file
cannot tell a careful one from a careless one. A green result here means SOMEBODY SIGNED FOR
EVERY PLATE. It does not mean the plates are good, and nothing it prints will say they are.

WHY A NEW FILE AND NOT AN EXTENSION (CLAUDE.md invariant 14)
---------------------------------------------------------------
Four existing tools were read first. None can carry this, and the reasons are not stylistic:

  * `check_plate_qc.py` DOES NOT EXIST. It is named in the work order; it is not on disk.
    Measured with `ls scripts/ | grep plate`. There was nothing to extend.
  * `qc_delivered_plates.py` is 9:16 SHORTS ONLY: `W, H = 135, 240`, it resolves its plate set
    out of `episodes/_planning/short_designs/*.json` by `short_id`, and its bands are the telop
    and caption bands of a vertical Short. It measures pixels and records NO verdict, has no
    `evaluate()`, and knows nothing of `mandatory_stills`. A long-form episode has none of the
    inputs it reads.
  * `check_pool_faces.py` scans ARCHIVE CLIPS with haarcascades and says so in its own scope
    note: "Scope is deliberately archive footage only ... Generated plates and the i2v motion
    built from them may show people ... so scanning them would produce noise, not safety."
    It records no verdict and binds nothing.
  * `check_visual_asset_qc.py` is the closest, and it was the real candidate. Its still lane
    already enumerates `remotion/public/<slug>/img/*.png` and it is already wired into both
    preflight and `check_final_acceptance`. It was rejected for three measured reasons:
      (a) its still lane is explicitly statistics-only -- "cheap, objective pixel stats -- no
          content judgement" -- median luma and a phash variety score. There is no per-still
          verdict anywhere in it to extend;
      (b) its per-item verdict pattern lives in the FACTORY lane, and that lane's manifest is
          written by `write_factory_clip_qc.py` from `reviewed_sheets`. That is the exact
          mechanism `check_pool_frames` was written to supersede: a sheet tick clearing twenty
          items at once. Extending the pattern would import the defect;
      (c) it never reads `episode_spec.v001.json`, so it cannot know the declared plate set,
          and it has no binding of any kind. Both would have to be built regardless.
    So the extension would have been a new subsystem wearing another file's name, and it would
    have changed the meaning of a gate that `check_final_acceptance` runs over the whole
    back-catalogue.

  What IS reused rather than re-implemented: the binding primitive itself. `pool_id_sha256` is
  imported from `check_pool_frames` (`pool_id_hash`) and not copied, so the two gates can never
  disagree about what "a hash of the id list" means. `_rel` comes from `check_shipped_frames`
  and the spec loader from `check_episode_spec`, as in `check_pool_frames`.

  The shape below is deliberately `check_pool_frames`'s shape -- `plate_state()` / `evaluate()`,
  the same verdict vocabulary, the same exact/subset/broken binding, the same refusal to claim
  cleanliness -- so the footage review and the plate review read alike.

THE PLATE SET
-------------
The union of two sources, because either alone leaves a hole:

  1. the episode's DECLARED `mandatory_stills` (the contract: `check_spec_satisfied` requires
     every one of these to appear in a cut), and
  2. every non-depth `.png` physically in the plate directory, because
     `build_case_film_generic` draws its still pool from the staged directory -- an undeclared
     headroom plate that is staged DOES become a cut, and would otherwise be unreviewed.

A declared id with no file on disk is still in the set and still needs a verdict. An
undelivered plate is not a reviewed plate.

TWO BINDINGS, AND WHY THE ID-LIST HASH IS NOT ENOUGH HERE
------------------------------------------------------------
`check_pool_frames` binds a pool of CLIPS by `sha256` over the sorted filenames, because the
failure it guards is "a clip was added or swapped after the review", and a swap arrives under
a new name from the shelf.

A PLATE IS REGENERATED UNDER ITS OWN ID. `L170.png` re-ordered in batch C is still
`L170.png` -- the id list does not move a bit, so an id-list hash alone would carry the old
verdict onto a new picture. That is the single most likely way an EP66 defect returns. So:

  plate_id_sha256   sha256 of the sorted id list  -- exactly `check_pool_frames.pool_id_hash`,
                    catches ids ADDED or REMOVED since the review
  per-plate sha256  sha256 of the file's bytes    -- catches a plate REGENERATED under its own
                    id. A verdict that records no sha256 cannot be shown to describe the file
                    on disk and is refused, not assumed.

Hashing is cached in `runs/qc/<slug>_plate_hashes.v001.json` keyed by (size, mtime_ns), so the
first run reads the plates once and every later run is a directory listing plus a stat. No
decode, no ffmpeg, no GPU, no network.

THE VERDICT FILE
----------------
`runs/qc/<slug>_plate_verdicts.v001.json` -- written by `--scaffold`, filled in by the
reviewer:

    {"schema_version": "plate_verdicts.v001",
     "slug": "openfields",
     "plate_review": {"reviewer": "...", "reviewed_at": "2026-08-11",
                      "plate_dir": "H:/pd-media/assets/ai/openfields",
                      "plate_id_sha256": "<the hash this script prints>",
                      "reviewed_ids": ["L070.png", ...]},
     "plates": {"L070.png": {"verdict": "accept", "sha256": "...", "note": "..."},
                "L146.png": {"verdict": "reject", "sha256": "...", "note": "tailgate wordmark"},
                "L259.png": {"verdict": "flag",   "sha256": "...", "note": "hair in the band"}}}

    accept                          resolved; the plate may ship
    reject                          resolved; the plate must NOT be declared and must NOT be
                                    staged. Left in either place, it fails.
    flag / unresolved / pending /
    revise / todo / "" / missing    UNRESOLVED -- blocks. `flag` is not a pass: EP66's L259 was
                                    a FLAG and its hair crosses the headline band.

`--scaffold` re-stamps the file: a plate whose sha256 has changed since it was judged is RESET
to `unresolved` and named on stdout. That is the invalidation, and it is mechanical rather
than remembered.

    py -3.11 scripts/check_plate_verdicts.py --slug openfields --scaffold --reviewer "name"
    py -3.11 scripts/check_plate_verdicts.py --slug openfields
    py -3.11 scripts/check_plate_verdicts.py --slug openfields --json runs/qc/x.json
    py -3.11 scripts/check_plate_verdicts.py --plate-dir <dir> --verdicts <json> --slug demo

Exit 0 only when every plate in the set carries a resolved verdict bound to the picture on
disk. Exit 1 otherwise. Read-only apart from runs/qc/.

`preflight_render_gate.py` calls `evaluate(epdir)` and `check_episode_inputs.py` calls
`plate_state(...)`; both go through the hash cache and neither decodes an image.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_episode_spec import load_and_validate          # noqa: E402
from check_final_acceptance import IMG_MIN_LONG_EDGE      # noqa: E402  (the ship-gate floor)
from check_pool_frames import pool_id_hash                # noqa: E402  (the ONE id-list hash)
from check_shipped_frames import _rel                     # noqa: E402


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


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "runs" / "qc"

# Where Codex delivers plates. Overridable for a fixture or a moved drive; there is no shared
# constant for this in the repo (eleven scripts hard-code the same string), so it is named once
# here and taken from the environment when set.
AI_DELIVERY_ROOT = Path(os.environ.get("PD_AI_PLATES_ROOT", str(PD_MEDIA / "assets" / "ai")))

REVIEW_KEY = "plate_review"
PLATES_KEY = "plates"

ACCEPT_WORDS = {"accept", "accepted", "ok", "pass", "keep", "approved"}
REJECT_WORDS = {"reject", "rejected", "kill", "regenerate", "reorder", "re-order"}
# Everything else -- flag, pending, revise, todo, blank, absent -- is UNRESOLVED and blocks.


# --------------------------------------------------------------------------------------
# the plate set
# --------------------------------------------------------------------------------------
def declared_ids(spec: dict | None) -> list[str]:
    """The episode's contract: `mandatory_stills`. `check_spec_satisfied` requires each of
    these to land in a cut, so each of them is a picture the audience will see."""
    vals = (spec or {}).get("mandatory_stills") or []
    return sorted({str(v) for v in vals if str(v).strip()})


def plates_on_disk(plate_dir: Path) -> list[Path]:
    """Every non-depth PNG physically in the plate directory.

    The DIRECTORY is ground truth, as `check_pool_frames.pool_clips` settled for the pool:
    not film.json, not the order document, not the delivery receipt. `*_depth.png` are
    depth maps generated from a plate, not plates.
    """
    if not plate_dir.is_dir():
        return []
    return sorted(p for p in plate_dir.iterdir()
                  if p.is_file() and p.suffix.lower() == ".png"
                  and not p.name.endswith("_depth.png"))


def _find_as_motion(plate_dir: Path, pid: str) -> Path | None:
    """The same plate after i2v: <plate_dir>/../motion/<stem>.<video ext>.

    A plate driven to motion LEAVES img/ and lands in motion/ as an mp4 -- the same picture in a
    different container. check_spec_satisfied.py already matches on the stem for exactly this
    reason ("a plate given motion arrives as G045.mp4"). Without this the gate reported 126 of
    EP65 marmet's 196 accepted plates as missing files and blocked the build over pictures that
    are present and on screen. Returns None when the picture is in neither place, which stays a
    hard failure.
    """
    stem = Path(pid).stem
    for d in (plate_dir.parent / "motion", plate_dir.parent / "video"):
        if not d.is_dir():
            continue
        for ext in (".mp4", ".mov", ".webm"):
            q = d / f"{stem}{ext}"
            if q.is_file():
                return q
    return None


def _find_still_after_motion(plate_dir: Path, pid: str) -> Path | None:
    """The judged STILL, after the finisher has moved it out of img/.

    A plate converted to i2v leaves img/ and the finisher retires the source PNG to
    img_unused/. The verdict's sha256 is the PNG's, so it can only be checked against the
    PNG -- hashing the .mp4 instead reported all 60 of EP76 morandi's converted plates as
    REGENERATED. Returns None when no still survives, in which case the bytes simply go
    unverified rather than being reported as a change nobody made.
    """
    name = Path(pid).name
    for d in (plate_dir.parent / f"{plate_dir.name}_unused",
              plate_dir.parent / "img_unused",
              plate_dir.parent / "img"):
        q = d / name
        if q.is_file():
            return q
    return None


def resolve_plate_dir(slug: str) -> tuple[Path, str]:
    """Render truth first, delivery second. Returns (dir, which).

    `remotion/public/<slug>/img` is what the render reads, so once plates are staged that is
    the set that matters. Before staging, the plates only exist where Codex saved them.
    """
    staged = ROOT / "remotion" / "public" / slug / "img"
    if plates_on_disk(staged):
        return staged, "render-truth (remotion/public/<slug>/img)"
    return AI_DELIVERY_ROOT / slug, "delivery (Codex save directory)"


# --------------------------------------------------------------------------------------
# the size the EPISODE'S OWN ORDER asked for
# --------------------------------------------------------------------------------------
# WHY THIS IS HERE AND NOT ONLY IN A WATCHER (2026-08-11)
# `EP67_ramirez_CODEX_BATCH_A.v002.md` states "Long edge >= 3840" twice, at line 77 and line
# 147. Eighty-eight of the first hundred and four delivered plates were 1672x941. Nothing
# refused them: the only pre-render reader of a plate's pixel size was
# `scripts/watch_plate_verdicts.py`, and a watcher runs when somebody starts one -- it was
# started at plate 104. `check_final_acceptance.check_image_resolution` measures it too, but
# after the render. This gate is already on the path that blocks a build
# (`preflight_render_gate` -> `evaluate`, `check_episode_inputs` -> `plate_state`), it already
# stats and hashes every plate, and acting here costs one image instead of a four-hour render.
#
# THE FLOOR IS NOT A CONSTANT IN THIS FILE. It is read from the episode's own image order --
# the document Codex was actually handed, and the only place an episode can ask for something
# other than the channel default. `IMG_MIN_LONG_EDGE` is imported from
# `check_final_acceptance`, never retyped, and is used ONLY when the order states no number of
# its own; whichever was used is printed. Two copies of one number is exactly how
# `watch_plate_verdicts.MIN_LONG_EDGE` and `preflight_render_gate.MIN_LONG_EDGE_PX` came to be
# three copies of it.
#
# THIS STILL LOOKS AT NO PIXEL. Thirty-three bytes of the PNG header are read; the IHDR
# carries width and height. No image library is imported, nothing is decoded, and a plate that
# is 3840x2160 and completely wrong for its beat passes this exactly as easily as a right one.

MIN_LONG_EDGE = IMG_MIN_LONG_EDGE     # channel default; watch_plate_verdicts imports this name
ASPECT_TOLERANCE = 0.01               # 3840x2160 is 1.7778; 0.01 admits nothing PD has shipped
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# The three ways this channel's orders have written the requirement, in English and Japanese.
# Measured against every EP*_CODEX_* order on disk before being written.
_RE_ORDER_LONG_EDGE = re.compile(
    r"long\s*edge\s*(?:is\s*)?(?:>=|\u2265|>|at\s*least|of\s*at\s*least)?\s*(\d{3,5})"
    r"|(\d{3,5})\s*(?:px\s*)?long\s*edge"
    r"|\u9577\u8fba\s*(\d{3,5})\s*px\s*\u4ee5\u4e0a", re.I)
_RE_ORDER_16_9 = re.compile(r"\b16\s*[:x\u00d7]\s*9\b")


def order_documents(slug: str) -> list[Path]:
    """The episode's own image orders. `check_design_doc.discover` resolves the same set."""
    return sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_CODEX_*.md"))


def order_pixel_contract(slug: str) -> dict:
    """What the orders demand of every delivered plate, in pixels.

    STRICTEST WINS. When two orders state different minima the larger binds, because a plate
    must satisfy every order that governs it and taking the smaller could only ever weaken the
    gate. Absurd matches are ignored: a number outside 1000-16000 is prose, not a contract.
    """
    stated: list[tuple[int, str]] = []
    wants_169 = ""
    for p in order_documents(slug):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in _RE_ORDER_LONG_EDGE.finditer(text):
            val = next((int(g) for g in m.groups() if g), 0)
            if 1000 <= val <= 16000:
                stated.append((val, p.name))
        if not wants_169 and _RE_ORDER_16_9.search(text):
            wants_169 = p.name
    if stated:
        val, where = max(stated)
        source = (f"the episode's own order ({where}, +{len(stated) - 1} more statement(s))"
                  if len(stated) > 1 else f"the episode's own order ({where})")
    else:
        val, source = MIN_LONG_EDGE, (
            f"the channel default check_final_acceptance.IMG_MIN_LONG_EDGE -- "
            f"{len(order_documents(slug))} order document(s) state no long edge of their own")
    return {"min_long_edge": val, "source": source,
            "require_16_9": bool(wants_169), "aspect_source": wants_169}


def png_dims(path: Path) -> tuple[int, int] | None:
    """(width, height) out of the PNG IHDR, or None when the file is not a readable PNG.

    Thirty-three bytes. No decode, no PIL, no judgement about what the picture contains.
    """
    try:
        with path.open("rb") as fh:
            head = fh.read(33)
    except OSError:
        return None
    if len(head) < 33 or head[:8] != PNG_SIGNATURE or head[12:16] != b"IHDR":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return (w, h) if (w and h) else None


def plate_pixels(slug: str, on_disk: dict) -> tuple[dict, list[str]]:
    """Measure every staged PNG against the order. Returns (counts, problems)."""
    contract = order_pixel_contract(slug)
    small: list[str] = []
    shape: list[str] = []
    unreadable: list[str] = []
    for pid, p in sorted(on_disk.items()):
        if Path(p).suffix.lower() != ".png":
            continue          # a plate driven to i2v arrives as .mp4; its source PNG was measured
        dim = png_dims(Path(p))
        if dim is None:
            unreadable.append(pid)
            continue
        w, h = dim
        if max(w, h) < contract["min_long_edge"]:
            small.append(f"{pid}={w}x{h}")
        elif contract["require_16_9"] and abs(max(w, h) / min(w, h) - 16 / 9) > ASPECT_TOLERANCE:
            shape.append(f"{pid}={w}x{h}")
    problems: list[str] = []
    if small:
        problems.append(
            f"{len(small)} plate(s) are BELOW the {contract['min_long_edge']}px long edge this "
            f"episode's own order demands ({contract['source']}): "
            + ", ".join(small[:6]) + (f" ... (+{len(small) - 6})" if len(small) > 6 else "")
            + ". EP67 delivered 88 plates at 1672x941 against an order that says 3840 twice, "
              "and nothing refused them until a watcher was started at plate 104. Re-order at "
              "the stated size; do not upscale a delivered plate to satisfy the number.")
    if shape:
        problems.append(
            f"{len(shape)} plate(s) are not 16:9, which {contract['aspect_source']} requires: "
            + ", ".join(shape[:6]) + (f" ... (+{len(shape) - 6})" if len(shape) > 6 else ""))
    if unreadable:
        problems.append(
            f"{len(unreadable)} file(s) carry a .png name but no readable PNG header, so their "
            f"size cannot be measured: "
            + ", ".join(unreadable[:6])
            + (f" ... (+{len(unreadable) - 6})" if len(unreadable) > 6 else ""))
    return ({"min_long_edge": contract["min_long_edge"],
             "min_long_edge_source": contract["source"],
             "require_16_9": contract["require_16_9"],
             "undersized": len(small), "wrong_aspect": len(shape),
             "unreadable_png": len(unreadable)}, problems)


# --------------------------------------------------------------------------------------
# content identity
# --------------------------------------------------------------------------------------
def _cache_path(slug: str) -> Path:
    return QC / f"{slug}_plate_hashes.v001.json"


def _load_cache(slug: str) -> dict:
    p = _cache_path(slug)
    if not p.is_file():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _save_cache(slug: str, cache: dict) -> None:
    try:
        QC.mkdir(parents=True, exist_ok=True)
        _cache_path(slug).write_text(json.dumps(cache, indent=1) + "\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass          # a cache that cannot be written is slow, never wrong


def file_sha256(path: Path, cache: dict) -> str:
    """sha256 of the file, cached on (size, mtime_ns).

    A regenerated plate lands with a new mtime, so the cache misses and the file is re-read.
    A plate that has only been COPIED (H: -> public/img) keeps its bytes, so the digest
    matches in both locations and a review made against the delivery directory still binds
    after staging.
    """
    try:
        st = path.stat()
    except OSError:
        return ""
    key = str(path)
    stamp = f"{st.st_size}:{st.st_mtime_ns}"
    hit = cache.get(key)
    if isinstance(hit, dict) and hit.get("stamp") == stamp and hit.get("sha256"):
        return str(hit["sha256"])
    h = hashlib.sha256()
    try:
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        return ""
    digest = h.hexdigest()
    cache[key] = {"stamp": stamp, "sha256": digest}
    return digest


# --------------------------------------------------------------------------------------
# the gate
# --------------------------------------------------------------------------------------
def _norm_verdict(raw) -> str:
    v = str(raw or "").strip().lower().replace("*", "").replace("`", "")
    if v in ACCEPT_WORDS:
        return "accept"
    if v in REJECT_WORDS:
        return "reject"
    return "unresolved"


def load_verdicts(path: Path) -> tuple[dict, str]:
    if not path.is_file():
        return {}, f"no {_rel(path)}"
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {}, f"{_rel(path)} is unreadable ({exc})"
    return (d if isinstance(d, dict) else {}), ("" if isinstance(d, dict) else
                                                f"{_rel(path)} is not a JSON object")


def plate_state(slug: str, spec: dict | None, plate_dir: Path | None = None,
                verdicts_path: Path | None = None) -> dict:
    """Does every plate in this set carry a resolved verdict bound to the picture on disk?

    This is the gate. `check_episode_inputs.py` calls it directly, `preflight_render_gate.py`
    reaches it through `evaluate()`. Directory listing, one json, and a cached digest per
    plate -- no image is decoded.

    Returns {ok, skipped, reason, problems, ...counts}. `ok` is False for every state that
    must stop a build; `skipped` is True only when there is genuinely nothing to judge.
    """
    which = "explicit --plate-dir"
    if plate_dir is None:
        plate_dir, which = resolve_plate_dir(slug)
    if verdicts_path is None:
        verdicts_path = QC / f"{slug}_plate_verdicts.v001.json"

    declared = declared_ids(spec)
    on_disk = {p.name: p for p in plates_on_disk(plate_dir)}
    ids = sorted(set(declared) | set(on_disk))

    out: dict = {
        "check": "plate_review",
        "slug": slug,
        "plate_dir": _rel(plate_dir),
        "plate_dir_kind": which,
        "declared": len(declared),
        "on_disk": len(on_disk),
        "plates": len(ids),
        "plate_id_sha256": pool_id_hash(ids) if ids else "",
        "verdicts_file": _rel(verdicts_path),
        "problems": [],
        "skipped": False,
        "ok": True,
        "reason": "",
    }
    if not ids:
        out["skipped"] = True
        out["reason"] = (f"no plates declared in mandatory_stills and none on disk under "
                         f"{_rel(plate_dir)} -- nothing to review yet")
        return out

    data, read_err = load_verdicts(verdicts_path)
    if read_err and not data:
        # A human-readable review may exist and still be unreadable by a machine. Say which,
        # rather than reporting "no review".
        md = QC / f"{slug}_plate_verdicts.v001.md"
        hint = (f" (there IS a prose review at {_rel(md)}, which no gate can read -- convert it "
                f"with --ingest-md)" if md.is_file() else "")
        out["ok"] = False
        out["problems"].append(
            f"{read_err}: {len(ids)} plate(s) are in this episode's plate set and NOT ONE "
            f"carries a per-plate verdict{hint}. Run `py -3.11 scripts/check_plate_verdicts.py "
            f"--slug {slug} --scaffold --reviewer <name>`, open every plate, then record a "
            f"verdict for each.")
        out["reason"] = out["problems"][0]
        return out

    review = data.get(REVIEW_KEY) or {}
    entries = data.get(PLATES_KEY) or {}
    if not isinstance(entries, dict):
        entries = {}
    out["reviewer"] = review.get("reviewer")
    out["reviewed_at"] = review.get("reviewed_at")

    if not review and not entries:
        out["ok"] = False
        out["problems"].append(
            f"{_rel(verdicts_path)} carries neither a '{REVIEW_KEY}' block nor a '{PLATES_KEY}' "
            f"map, so no plate has been looked at individually. A per-BATCH sign-off clears "
            f"eight plates at once; that is how EP66's round pole, tailgate wordmark and fused "
            f"fingers all reached a re-order.")
        out["reason"] = out["problems"][0]
        return out

    reviewed = {str(x) for x in (review.get("reviewed_ids") or [])} or set(entries)
    declared_hash = str(review.get("plate_id_sha256") or "")
    out["declared_plate_id_sha256"] = declared_hash

    # --- binding 1: the id list -----------------------------------------------------------
    added = sorted(set(ids) - reviewed)
    if declared_hash and declared_hash == out["plate_id_sha256"]:
        out["binding"] = "exact"
    elif not added:
        removed = len(reviewed - set(ids))
        out["binding"] = "subset"
        out["binding_note"] = (
            f"the review names plate_id_sha256={declared_hash[:16] or '(none)'} and this set "
            f"hashes to {out['plate_id_sha256'][:16]}; {removed} id(s) have been REMOVED since "
            f"and none added, so every plate still in the set was seen. Not an exact binding.")
    else:
        out["binding"] = "broken"
        out["ok"] = False
        out["problems"].append(
            f"{len(added)} plate(s) entered the set AFTER the review and nobody has seen them: "
            + ", ".join(added[:5]) + (f" ... (+{len(added) - 5})" if len(added) > 5 else "")
            + f". The review is bound to plate_id_sha256={declared_hash[:16] or '(none)'}; this "
            f"set hashes to {out['plate_id_sha256'][:16]}. Re-run --scaffold and judge the new "
            f"ids.")

    # --- per-plate coverage, resolution and content binding -------------------------------
    cache = _load_cache(slug)
    no_verdict: list[str] = []
    unresolved: list[str] = []
    unbound: list[str] = []
    regenerated: list[str] = []
    rejected: list[str] = []
    accepted: list[str] = []
    missing_file: list[str] = []

    for pid in ids:
        e = entries.get(pid)
        if not isinstance(e, dict):
            no_verdict.append(pid)
            continue
        v = _norm_verdict(e.get("verdict"))
        if v == "unresolved":
            unresolved.append(f"{pid} [{str(e.get('verdict') or 'blank').strip()}]")
            continue
        if v == "reject":
            rejected.append(pid)
        else:
            accepted.append(pid)
        # content binding applies to any plate that is still on disk; a rejected plate that has
        # already been deleted has nothing to bind to.
        p = on_disk.get(pid)
        if p is None:
            # A plate driven to i2v LEAVES img/ and lands in motion/ as <id>.mp4 -- the same
            # picture in a different container. check_spec_satisfied.py already matches on the
            # stem for exactly this reason ("a plate given motion arrives as G045.mp4"). Without
            # this, EP65 marmet reported 126 of its 196 accepted plates as missing files and the
            # build was blocked over pictures that are present and on screen.
            p = _find_as_motion(plate_dir, pid)
            if p is None:
                if v == "accept":
                    missing_file.append(pid)
                continue
            on_disk[pid] = p
            # ...but the .mp4 IS A DIFFERENT FILE, so its sha256 can never match the verdict,
            # which was bound to the PNG. Hashing it reported all 60 of EP76 morandi's
            # i2v-converted plates as REGENERATED (2026-08-25) and sent the build to re-review
            # 60 pictures that had not changed. The still is the thing that was judged: hash it
            # where it now lives (img_unused/ after the finisher retires it), and only say
            # nothing about the bytes when the still is genuinely gone.
            still = _find_still_after_motion(plate_dir, pid)
            if still is None:
                continue
            p = still
        want = str(e.get("sha256") or "").strip().lower()
        if not want:
            unbound.append(pid)
            continue
        got = file_sha256(p, cache)
        if got and got != want:
            regenerated.append(pid)
    _save_cache(slug, cache)

    out.update({"accepted": len(accepted), "rejected": len(rejected),
                "no_verdict": len(no_verdict), "unresolved": len(unresolved),
                "unbound": len(unbound), "regenerated": len(regenerated)})

    def _list(xs: list[str], n: int = 5) -> str:
        return ", ".join(xs[:n]) + (f" ... (+{len(xs) - n})" if len(xs) > n else "")

    if no_verdict:
        out["ok"] = False
        out["problems"].append(
            f"{len(no_verdict)} of {len(ids)} plate(s) carry NO per-plate verdict: "
            f"{_list(no_verdict)}")
    if unresolved:
        out["ok"] = False
        out["problems"].append(
            f"{len(unresolved)} plate(s) carry an UNRESOLVED verdict -- flag/pending is not a "
            f"pass, EP66's L259 was a FLAG and its hair crosses the headline band: "
            f"{_list(unresolved)}")
    if unbound:
        out["ok"] = False
        out["problems"].append(
            f"{len(unbound)} plate(s) have a verdict that records no sha256, so it cannot be "
            f"shown to describe the file now on disk -- a plate regenerated under its own id "
            f"would keep the old verdict: {_list(unbound)}. Re-run --scaffold.")
    if regenerated:
        out["ok"] = False
        out["problems"].append(
            f"{len(regenerated)} plate(s) have been REGENERATED since they were judged (the "
            f"file's sha256 no longer matches the verdict): {_list(regenerated)}. The verdict "
            f"describes a picture that no longer exists. Re-run --scaffold, which resets these "
            f"to unresolved, and look at them again.")
    if missing_file:
        out["ok"] = False
        out["problems"].append(
            f"{len(missing_file)} plate(s) are marked accept but have no file in "
            f"{_rel(plate_dir)}: {_list(missing_file)}")

    # --- the size the order asked for ------------------------------------------------------
    # Independent of any verdict: a reviewer signing "accept" on a thumbnail-sized plate is
    # exactly the EP67 failure, and the number is not something a person eyeballs.
    px, px_problems = plate_pixels(slug, on_disk)
    out.update(px)
    if px_problems:
        out["ok"] = False
        out["problems"] += px_problems

    # A recorded rejection is not an applied one. `check_spec_satisfied` requires every
    # mandatory_stills id to appear in a cut, and the still pool is drawn from the staged
    # directory, so a rejected plate in either place still reaches the audience.
    still_declared = sorted(p for p in rejected if p in set(declared))
    if still_declared:
        out["ok"] = False
        out["problems"].append(
            f"{len(still_declared)} plate(s) REJECTED at review are still declared in "
            f"mandatory_stills, so the film will place them as cuts: {_list(still_declared)}. "
            f"Regenerate them under the same id, or drop the id from the spec.")
    staged_img = ROOT / "remotion" / "public" / slug / "img"
    still_staged = sorted(p for p in rejected if (staged_img / p).is_file())
    if still_staged:
        out["ok"] = False
        out["problems"].append(
            f"{len(still_staged)} plate(s) REJECTED at review are still staged in "
            f"remotion/public/{slug}/img, which is the still pool the builder draws from: "
            f"{_list(still_staged)}")

    if out["ok"]:
        out["reason"] = (
            f"{len(ids)} plate(s) in the set ({len(declared)} declared, {len(on_disk)} on disk), "
            f"every one carrying a resolved per-plate verdict whose sha256 matches the file now "
            f"on disk; binding={out['binding']}"
            + (f" ({out['binding_note']})" if out.get("binding_note") else "")
            + f". Reviewer: {review.get('reviewer') or 'unnamed'} "
              f"{review.get('reviewed_at') or ''}".rstrip()
            + ". THIS SAYS SOMEBODY SIGNED FOR EVERY PLATE. It does not say the plates are "
              "good: no pixel was examined here, and every content judgement came from that "
              "reviewer.")
    else:
        out["reason"] = " | ".join(out["problems"])
    return out


def evaluate(epdir: Path) -> dict:
    """The `preflight_render_gate._run_ext_gate` contract: {ok, hard, reason, skipped}.

    Never raises, never calls sys.exit, never decodes an image.
    """
    epdir = Path(epdir)
    slug = epdir.name.split("-")[-1]
    spec, problems, _ = load_and_validate(slug)
    if problems:
        # Fail closed rather than judging against an unknown contract. An unreadable spec means
        # the declared plate set is unknown, and "unknown" is not "empty".
        return {"check": "plate_review", "ok": False, "hard": True, "skipped": False,
                "reason": (f"the episode spec could not be validated, so the declared plate set "
                           f"is unknown: {problems[0]}"),
                "detail": {"spec_problems": problems}}
    st = plate_state(slug, spec)
    return {"check": "plate_review", "ok": bool(st["ok"]), "hard": True,
            "skipped": bool(st["skipped"]), "reason": st["reason"], "detail": st}


# --------------------------------------------------------------------------------------
# scaffolding the verdict file
# --------------------------------------------------------------------------------------
def scaffold(slug: str, spec: dict | None, plate_dir: Path, verdicts_path: Path,
             reviewer: str) -> dict:
    """Write/refresh the verdict file: every id present, current sha256 stamped.

    Existing verdicts are PRESERVED where the sha256 is unchanged and RESET to `unresolved`
    where the picture has changed. That reset is the whole invalidation mechanism, and it is
    mechanical rather than remembered.
    """
    declared = declared_ids(spec)
    on_disk = {p.name: p for p in plates_on_disk(plate_dir)}
    ids = sorted(set(declared) | set(on_disk))

    prev, _ = load_verdicts(verdicts_path)
    prev_plates = prev.get(PLATES_KEY) if isinstance(prev.get(PLATES_KEY), dict) else {}

    cache = _load_cache(slug)
    plates: dict[str, dict] = {}
    reset, kept, fresh, bound = [], [], [], []
    for pid in ids:
        p = on_disk.get(pid)
        if p is None:
            # Same resolution as plate_state(): a plate driven to i2v LEAVES img/ and lands in
            # motion/ as <id>.mp4. Without this, scaffold stamped no sha256 for every such plate
            # and then RESET it as "the picture changed" -- EP65 marmet, 149 of 233 plates, a
            # loop no reviewer could ever close because the next scaffold reset them again.
            p = _find_as_motion(plate_dir, pid)
        sha = file_sha256(p, cache) if p is not None else ""
        old = prev_plates.get(pid) if isinstance(prev_plates.get(pid), dict) else None
        if old is None:
            plates[pid] = {"verdict": "unresolved", "sha256": sha, "note": ""}
            fresh.append(pid)
        elif str(old.get("sha256") or "") == sha and sha:
            plates[pid] = {"verdict": str(old.get("verdict") or "unresolved"),
                           "sha256": sha, "note": str(old.get("note") or "")}
            kept.append(pid)
        elif not str(old.get("sha256") or "").strip():
            # NEVER BOUND, which is not the same fact as CHANGED. --ingest-md converts a prose
            # review by scaffolding first and then writing verdict+note only, so every verdict it
            # imports arrives with an empty sha256. Calling that "the picture changed" resets the
            # whole imported review the moment it is bound, and the next scaffold resets it again
            # -- a loop no reviewer can close, and the printed reason is a claim the tool cannot
            # support. Stamp the hash, keep the verdict, and say in the note that the binding was
            # made after the fact so it is never mistaken for one the reviewer signed.
            plates[pid] = {"verdict": str(old.get("verdict") or "unresolved"), "sha256": sha,
                           "note": (str(old.get("note") or "") + " [sha256 bound retroactively: "
                                    "this verdict was imported without one]").strip()}
            bound.append(pid)
        else:
            plates[pid] = {"verdict": "unresolved", "sha256": sha,
                           "note": (f"RESET: the picture changed since it was judged as "
                                    f"'{old.get('verdict')}'. " + str(old.get("note") or "")).strip()}
            reset.append(pid)
    _save_cache(slug, cache)

    payload = {
        "schema_version": "plate_verdicts.v001",
        "slug": slug,
        REVIEW_KEY: {
            "reviewer": reviewer or (prev.get(REVIEW_KEY) or {}).get("reviewer") or "",
            "reviewed_at": date.today().isoformat(),
            "plate_dir": str(plate_dir),
            "plate_id_sha256": pool_id_hash(ids) if ids else "",
            "reviewed_ids": ids,
        },
        PLATES_KEY: plates,
    }
    verdicts_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = verdicts_path.with_suffix(verdicts_path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(verdicts_path)
    return {"ids": len(ids), "new": fresh, "kept": kept, "reset": reset, "bound": bound,
            "path": verdicts_path}


# --------------------------------------------------------------------------------------
# converting a prose review that already exists
# --------------------------------------------------------------------------------------
_ID_RE = re.compile(r"^[A-Z]{1,2}\d{2,4}(?:\.png)?$")
# Deliberately NARROW. "PASS" and "OK" are not in this set: EP66's own batchC document carries a
# per-plate MEASUREMENT table with a PASS column, and admitting "pass" made that row outvote the
# FLAG the reviewer had actually written for L259. A converter may only ever recognise the words
# a reviewer uses to render a verdict.
_MD_ACCEPT = {"accept", "accepted"}
_MD_REJECT = {"reject", "rejected"}
_MD_UNRESOLVED = {"flag", "flagged", "pending", "revise", "todo", "unresolved"}


def _cell(text: str) -> str:
    return text.replace("**", "").replace("`", "").strip()


def ingest_md(md_path: Path) -> tuple[dict[str, tuple[str, str]], list[str], list[str]]:
    """Parse a markdown verdict table into {id: (verdict, note)}. STRICT by design.

    A converter that guesses can only ever fail in the dangerous direction -- turning a human's
    FLAG into an ACCEPT. So a row is used only when its first cell is an id and EXACTLY ONE of
    its remaining cells is, on its own, one of the known verdict words. Anything else is
    reported as ambiguous and the whole conversion refuses.
    """
    out: dict[str, tuple[str, str]] = {}
    ambiguous: list[str] = []
    skipped: list[str] = []
    for raw in md_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [_cell(c) for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        pid = cells[0]
        if not _ID_RE.match(pid):
            continue
        pid = pid if pid.endswith(".png") else pid + ".png"
        hits = [c.lower() for c in cells[1:]
                if c.lower() in (_MD_ACCEPT | _MD_REJECT | _MD_UNRESOLVED)]
        if not hits:
            # A row whose first cell is an id but which renders no verdict -- a measurement
            # table, a description table, an index. Skipped rather than flagged: a plate that
            # ends with no verdict is caught downstream by the coverage check, so ignoring the
            # row fails closed. Counted so the operator can see how many were passed over.
            skipped.append(pid)
            continue
        if len(hits) != 1:
            ambiguous.append(f"{pid}: {len(hits)} conflicting verdict words in one row")
            continue
        word = hits[0]
        verdict = ("accept" if word in _MD_ACCEPT else
                   "reject" if word in _MD_REJECT else "unresolved")
        note = next((c for c in reversed(cells[1:]) if len(c) > 12), "")[:400]
        if pid in out and out[pid][0] != verdict:
            ambiguous.append(f"{pid}: two rows disagree ({out[pid][0]} vs {verdict})")
            continue
        out[pid] = (verdict, note)
    return out, ambiguous, sorted(set(skipped) - set(out))


# --------------------------------------------------------------------------------------
def _print(st: dict) -> None:
    print("=" * 92)
    print(f"PLATE REVIEW  {st['slug']}")
    print(f"  plate dir     {st['plate_dir']}   [{st['plate_dir_kind']}]")
    print(f"  plate set     {st['plates']}  ({st['declared']} declared in mandatory_stills, "
          f"{st['on_disk']} png on disk)")
    print(f"  plate_id_sha256 {st['plate_id_sha256'][:32]}")
    print(f"  verdicts      {st['verdicts_file']}")
    if st.get("binding"):
        print(f"  binding       {st['binding']}")
    if "min_long_edge" in st:
        print(f"  min long edge {st['min_long_edge']}  ({st.get('min_long_edge_source', '')})")
    for k in ("accepted", "rejected", "no_verdict", "unresolved", "unbound", "regenerated",
              "undersized", "wrong_aspect", "unreadable_png"):
        if k in st:
            print(f"  {k:13s} {st[k]}")
    print("-" * 92)
    if st["skipped"]:
        print(f"SKIPPED: {st['reason']}")
    elif st["ok"]:
        print("PASS")
        print(f"  {st['reason']}")
    else:
        print(f"REFUSED -- {len(st['problems'])} problem(s):")
        for p in st["problems"]:
            print(f"  - {p}")
    print("-" * 92)
    print("WHAT THIS CHECK CANNOT DO: it never looks at a picture. Width and height come out")
    print("of the PNG header; no pixel of any plate is examined here -- no vision model, no")
    print("OCR, no glyph detector, no hand check, no")
    print("subject-match check. It proves only that a verdict exists for every plate, that it")
    print("is bound to the bytes on disk, and that none is unresolved. Whether a plate is")
    print("actually right is a judgement a human or a vision pass made, and a careless one")
    print("passes this gate exactly as easily as a careful one.")
    print("=" * 92)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--plate-dir", help="override the plate directory (fixture / moved drive)")
    ap.add_argument("--verdicts", help="override runs/qc/<slug>_plate_verdicts.v001.json")
    ap.add_argument("--scaffold", action="store_true",
                    help="write/refresh the verdict file; resets any plate whose picture changed")
    ap.add_argument("--reviewer", default="", help="name recorded by --scaffold")
    ap.add_argument("--ingest-md", help="convert an existing markdown verdict table first")
    ap.add_argument("--json", dest="json_out")
    a = ap.parse_args()

    spec, problems, _ = load_and_validate(a.slug)
    if problems:
        print(f"[plate-review] spec problem(s) for {a.slug}:")
        for p in problems:
            print(f"  - {p}")
        if not a.plate_dir:
            # Without a spec there is no declared set. A fixture run may still proceed on the
            # directory alone; a real episode may not.
            return 1
        spec = None

    plate_dir = Path(a.plate_dir) if a.plate_dir else resolve_plate_dir(a.slug)[0]
    verdicts_path = Path(a.verdicts) if a.verdicts else QC / f"{a.slug}_plate_verdicts.v001.json"

    if a.ingest_md:
        parsed, ambiguous, ignored = ingest_md(Path(a.ingest_md))
        print(f"[plate-review] {Path(a.ingest_md).name}: parsed {len(parsed)} verdict row(s), "
              f"{len(ambiguous)} ambiguous, {len(ignored)} id row(s) with no verdict word "
              f"(ignored -- a plate left without a verdict blocks anyway)")
        for x in ambiguous[:10]:
            print(f"  ? {x}")
        if ambiguous:
            print("[plate-review] REFUSED to convert: an ambiguous row could only ever be "
                  "resolved in the dangerous direction. Fix the table or write the JSON.")
            return 2
        res = scaffold(a.slug, spec, plate_dir, verdicts_path, a.reviewer or "ingest-md")
        data = json.loads(verdicts_path.read_text(encoding="utf-8"))
        applied = 0
        for pid, (verdict, note) in parsed.items():
            if pid in data[PLATES_KEY]:
                data[PLATES_KEY][pid]["verdict"] = verdict
                data[PLATES_KEY][pid]["note"] = note
                applied += 1
        verdicts_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                                 encoding="utf-8")
        print(f"[plate-review] applied {applied} of {len(parsed)} parsed verdict(s) onto "
              f"{res['ids']} scaffolded plate(s) -> {_rel(verdicts_path)}")
        print("[plate-review] a converted verdict is only as good as the table it came from, "
              "and FLAG was converted to UNRESOLVED, not to a pass.")

    elif a.scaffold:
        res = scaffold(a.slug, spec, plate_dir, verdicts_path, a.reviewer)
        print(f"[plate-review] {res['ids']} plate(s) -> {_rel(res['path'])}")
        print(f"  new {len(res['new'])}   kept {len(res['kept'])}   "
              f"bound (had no sha256) {len(res.get('bound') or [])}   "
              f"RESET (picture changed) {len(res['reset'])}")
        for pid in res["reset"][:20]:
            print(f"    reset: {pid}")
        if not a.reviewer:
            print("  no --reviewer recorded; write one in before signing anything off")

    st = plate_state(a.slug, spec, plate_dir if a.plate_dir else None,
                     verdicts_path if a.verdicts else None)
    _print(st)
    if a.json_out:
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
        print(f"report -> {a.json_out}")
    return 0 if (st["ok"] or st["skipped"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
