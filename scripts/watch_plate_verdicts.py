#!/usr/bin/env python3
r"""Verdict AI plates AS THEY LAND, so the review finishes when the generation finishes.

WHY THIS EXISTS
---------------
Today a batch is generated (152 plates for EP67, 123 for EP68, 133 for EP69) and THEN
somebody reviews it. The review's wall clock is added on top of the generation's. Reviewed
as they land, it is not: the last plate is verdicted minutes after it is written, and the
episode is already unblocked when the generator stops.

So this watches `E:\pd-media\assets\ai\<slug>\` on an interval, measures every new or
CHANGED `.png` the moment it settles, builds the review packet a content reviewer actually
needs (native-resolution crops, the callback pair side by side, the plate's own order text),
and appends the reviewer's verdict incrementally to the one file the pre-build gate reads.

WHAT THE MECHANICAL PASS CAN MEASURE, AND WHAT IT CANNOT
--------------------------------------------------------
This is the whole point of the tool, so it is the first thing in the docstring and it is
printed in every receipt. A green mechanical line IS NOT AN APPROVAL.

  CAN:  does it decode; width/height/aspect; bytes; mean luma; contrast (sd); crushed and
        blown fractions; subject-region luma (the `check_thumb_subject_luma` box, floor 60);
        the whole-frame floors the ship gate uses (mean >= 33, contrast >= 40, from
        `check_final_acceptance`); for a THUMB plate the clear upper region
        (`check_thumb_headline_band.measure`); a perceptual hash and therefore the nearest
        already-measured plate in the same episode; and the era/place PROMPTS that
        `check_pool_frames` derives from `episode_spec.era_setting`.

  CANNOT: whether the picture is the thing that was ordered. Whether a callback matches its
        pair. Whether any text is legible. Whether fingers are countable. Whether a face
        resembles a real person. Whether it is dull.

        Every one of those is a CONTENT verdict, and this tool never issues one. It moves a
        plate to `awaiting_content_verdict` and hands over a packet. Only `--record`, with a
        named reviewer, writes `accept` or `reject`.

        The only verdict the machine writes by itself is a rejection for a defect that is
        not a matter of opinion: the file does not decode, or it is the wrong size/aspect.

WHY THE PACKET IS CROPS AND NOT THE PLATE
------------------------------------------
Measured on real EP66 plates in the last day:

  * `L146` and `L173` carried a manufacturer wordmark about 53x12 px on the tailgate of a
    3840x2160 plate. Invisible until 4x. `L096` carried a licence plate with five or six
    glyphs, invisible until 14x. A reviewer handed a 1600px proxy CANNOT see these. So when
    the plate's own order text names a surface that must be bare -- a tailgate, a grille, a
    placard, a document, a screen -- the packet carries the whole plate as a grid of 1:1
    NATIVE crops (3840x2160 -> 3x3 tiles of 1280x720), and the trigger words are printed
    beside them so the reviewer knows what to hunt for.
  * `L236` came back with fused fingers twice. Where the order names hands, the same 1:1
    grid is emitted and `hands` is named as the trigger.
  * `L170` came back a round pole three times where the film needs the squared one from
    `L075`, 26 minutes earlier. A pair mismatch is invisible to ANY single-plate check. The
    order records the reference for each callback in the plate's own block, this reads it,
    and the packet carries BOTH IMAGES IN ONE FRAME, labelled.
  * `L209` was ordered as a plain olive box and delivered a consumer camera. Nothing
    mechanical sees that. It goes to the reviewer with its order text quoted.
  * EP65's first four thumbnails passed every machine floor and were rejected by the owner
    as dull. Which is why a clean mechanical line reads `awaiting_content_verdict`, never
    `accept`.

THE CROP TRIGGERS ARE A PROMPT, NOT A DETECTOR
-----------------------------------------------
They fire on the WORDS IN THE ORDER, not on pixels. There is no tailgate detector here and
there is no glyph detector here -- an MSER glyph-row detector was built during the EP66
review and thrown away because its top-ranked plate out of 260 was a patch of flattened
grass at 11,571 candidate glyph boxes (`runs/qc/openfields_plate_verdicts.v001.md`, Method).
A plate that fires no trigger is not a clean plate; it is a plate whose ORDER did not name a
bare surface. That is said in every packet.

WHAT IS WRITTEN, AND WHERE
--------------------------
`runs/qc/<slug>_plate_watch.v001.json`   the watcher's own receipt and measurement cache.
                                         Keyed by filename; carries the sha256 of the BYTES,
                                         the mechanical numbers, the plate's order text, its
                                         crop triggers and its packet paths. This file is a
                                         cache and a record; it is NOT a verdict.

`runs/qc/<slug>_plate_verdicts.v001.json`  THE VERDICT FILE. IT IS NOT THIS TOOL'S FILE.

  `scripts/check_plate_verdicts.py` -- the blocking pre-build gate, wired into
  `check_episode_inputs.py` and `preflight_render_gate.py` -- owns it: the schema, the plate
  set, which directory counts as the plate directory, the id-list binding and the
  invalidation. This watcher IMPORTS every one of those and re-implements none of them, so
  there is exactly one answer to "does this plate have a verdict":

    {"schema_version": "plate_verdicts.v001",
     "slug": "openfields",
     "plate_review": {"reviewer": "...", "reviewed_at": "2026-08-11",
                      "plate_dir": "E:/pd-media/assets/ai/openfields",
                      "plate_id_sha256": "<sha256 of the sorted id list>",
                      "reviewed_ids": ["L070.png", ...]},
     "plates": {"L070.png": {"verdict": "accept", "sha256": "<of the bytes>", "note": "..."},
                "L146.png": {"verdict": "reject", "sha256": "...", "note": "tailgate wordmark"}}}

  `accept` and `reject` are resolved; EVERYTHING ELSE -- `flag`, `pending`, blank, absent --
  is `unresolved` and blocks. `flag` is not a pass, and this tool never writes one.

  The plate set is the gate's: declared `mandatory_stills` UNION every non-depth `.png` in the
  plate directory. Note what that means on EP66 -- the set is 260, not the 191 the QC document
  counted, because the 69 abandoned batch-A plates are physically on the shelf and
  `build_case_film_generic` builds its still pool from the DIRECTORY. They are measured,
  packeted and put in a worklist like everything else. That is the gate's definition and this
  file does not get a second opinion about it.

  REGENERATION INVALIDATION IS `check_plate_verdicts.scaffold()`, called once per pass. It
  stamps every id with its current sha256, keeps a verdict whose picture is unchanged, and
  RESETS to `unresolved` any whose picture has moved. There is no copy of that logic in this
  file, so a plate regenerated while the watcher is stopped is invalidated just the same, by
  the gate, on the next run of either tool.

`runs/qc/<slug>_plate_watch/`            the review packets: `<ID>/full.jpg`, `<ID>/zoom_*.jpg`
                                         (1:1 native), `<ID>/pair_<REF>.jpg`, and
                                         `batch_NNNN.md`, the worklist for a small batch.
                                         `runs/` is git-ignored, so these are free.

POLL DESIGN
-----------
No filesystem-event library. Each pass lists the directory and stats every `.png`. A file is
processed when it has SETTLED, which means all three of:

  1. `mtime` is at least `--settle-sec` (default 3.0) in the past;
  2. its `(size, mtime)` are identical to what the PREVIOUS pass saw, unless this is the
     first pass for that file in this process (`--once` has no previous pass, so it leans on
     1 and 3);
  3. PIL can `load()` it end to end. A half-written PNG raises, and that alone rejects a file
     that passed 1 and 2 because the writer stalled.

A file that fails 1 or 2 is `unsettled` and is simply looked at again next pass. A file that
is old and still will not decode is `undecodable`, which IS a machine rejection.

IDEMPOTENT AND RESUMABLE
------------------------
The receipt is the cache. A plate whose `(size, mtime)` are unchanged is not re-measured and
not re-packeted -- a second `--once` over 260 plates takes 0.0s and creates no new worklist.
A plate whose bytes changed is re-measured, its packet is rebuilt, and the scaffold resets its
verdict, which is printed. Kill the watcher and re-run it and it picks up where it stopped.

USAGE
-----
  py -3.11 scripts/watch_plate_verdicts.py --slug openfields --once
  py -3.11 scripts/watch_plate_verdicts.py --slug ramirez            # poll until Ctrl-C
  py -3.11 scripts/watch_plate_verdicts.py --slug ramirez --interval 30 --batch 8
  py -3.11 scripts/watch_plate_verdicts.py --slug openfields --once --only L146,L096,L170
  py -3.11 scripts/watch_plate_verdicts.py --slug openfields --state      # no decoding

  py -3.11 scripts/watch_plate_verdicts.py --slug openfields --record \
      --reviewer "claude/plate-watch" \
      --accept L070,L071,L072 \
      --reject "L146=wordmark 53x12 native px on the tailgate, the defect it was re-ordered to remove"
  py -3.11 scripts/watch_plate_verdicts.py --slug openfields --record --reviewer X --from-json v.json

Exit code is `check_plate_verdicts.plate_state()`'s answer, not this file's opinion: 0 only
when every plate in the gate's set carries a RESOLVED verdict bound to the bytes on disk.
Exit 1 otherwise -- including when plates are merely awaiting a content verdict, which is the
honest state of a directory nobody has looked at yet. Reads the plate directory; writes only
under `runs/qc/`. No network, no GPU, no ffmpeg, no render.

MEASURED, FIRST RUN, 2026-08-11
-------------------------------
EP66 openfields, 260 plates, 84s: no hard rejection, 260 awaiting content verdict, 33
worklists, 1,179 native 1:1 tiles, 9 callback-pair images. Against the two existing human
verdict documents it contradicted nothing: of the 184 plates a human ACCEPTED whose bytes are
still the ones that were judged, it emitted a prompt on 14 and a rejection on none.

EP67 ramirez, the live batch, 96 plates: 80 MACHINE-REJECTED at 1672x941 against the order's
own "Long edge >= 3840", printed twice in `EP67_ramirez_CODEX_BATCH_A.v002.md`. That is what
this tool is for, and it is also the reason the resolution rule is the CONTRACT and not the
batch's modal size -- the mode here is the defect, and a mode rule rejected the 16 good plates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_footage_contact_sheet import _font                       # noqa: E402
from check_episode_spec import load_and_validate                    # noqa: E402
from check_pool_frames import era_of, era_prompts                   # noqa: E402
# THE VERDICT FILE IS check_plate_verdicts.py'S. Its schema, its plate set, its plate-dir
# resolution, its invalidation. Nothing about the contract is re-implemented here -- this file
# only fills the document in. See the module docstring.
from check_plate_verdicts import (                                  # noqa: E402
    MIN_LONG_EDGE, PLATES_KEY, _norm_verdict, declared_ids, load_verdicts, plate_state,
    plates_on_disk, resolve_plate_dir, scaffold,
)
from check_shipped_frames import _rel                               # noqa: E402
from check_spec_satisfied import _hits, _words                      # noqa: E402
from check_thumb_headline_band import measure as band_measure       # noqa: E402
from check_thumb_subject_luma import SUBJ_X0, SUBJ_X1, SUBJ_Y0, SUBJ_Y1  # noqa: E402

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "runs" / "qc"
PLANNING = ROOT / "episodes" / "_planning"

# --- floors, every one of them lifted from a gate that already exists -------------------
# THUMBNAIL ONLY. Measured: applied to body plates these flag 82 of EP66's 184 accepted
# plates, because this film's own STYLE block orders low contrast. See mechanical_flags().
MIN_MEAN_LUMA = 33.0        # check_final_acceptance.THUMB_MIN_MEAN_LUMA
MIN_CONTRAST_STD = 40.0     # check_final_acceptance.THUMB_MIN_CONTRAST_STD
MIN_SUBJECT_LUMA = 60.0     # check_thumb_subject_luma.SUBJECT_MIN_LUMA
# UNIVERSAL -- these are about a broken image, not about taste.
NEAR_BLACK_MEAN = 12.0      # check_pool_frames / check_shipped_frames
BLOWN_OUT_MEAN = 240.0      # check_shipped_frames
BLOWN_OUT_FRAC = 0.70       # check_shipped_frames
CRUSHED_LEVEL = 2.0         # a pixel at or below this is crushed black
BLOWN_LEVEL = 253.0
ASPECT_TOL = 0.005          # 16:9 within half a percent
# MIN_LONG_EDGE is IMPORTED from check_plate_verdicts above, not defined here (2026-08-11).
# It used to be its own `= 3840` in this file, and this file is a WATCHER: it runs when somebody
# starts one, and on EP67 nobody started one until plate 104 of 104, by which time 88 plates were
# 1672x941. The number now lives in the gate that BLOCKS the build, where it is resolved from the
# episode's own order (check_plate_verdicts.order_pixel_contract) and falls back to
# check_final_acceptance.IMG_MIN_LONG_EDGE. One definition, in the place that can stop something.
# outlier prompts, relative to the batch's own distribution -- never a floor
OUTLIER_PCT = 2.0
MIN_FOR_OUTLIERS = 24       # below this, a percentile of the batch means nothing

# --- measurement frame ------------------------------------------------------------------
# 1280x720, the same reduction check_thumb_headline_band uses, so its numbers and these are
# in one frame. The EP66 v001 verdict table quoted a 1920x1080 reduction; the two agree to
# well under a level on every plate, and mixing frames is how two tables stop being
# comparable, so one frame is picked and named.
REF_W, REF_H = 1280, 720

# --- near duplicate ----------------------------------------------------------------------
DHASH_SIDE = 16             # 16x17 grid -> 256 bits. Threshold is the batch's own
                            # distribution, not a constant -- see refresh_nearest().

# --- packet --------------------------------------------------------------------------------
PROXY_W = 1600              # the "read the whole picture" image
CROP_W, CROP_H = 1280, 720  # one native 1:1 tile; 3840x2160 is exactly 3x3 of these
PAIR_W = 1200               # per side of a callback pair
JPEG_Q = 92

ID_IN_TEXT = re.compile(r"\b([A-Z]{1,3}\d{2,4})\b")


# =========================================================================================
# the crop triggers.  READ THE DOCSTRING. THESE FIRE ON THE ORDER'S WORDS, NOT ON PIXELS.
# =========================================================================================
CROP_TRIGGERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("bareness_ordered", (
        # the order itself saying a surface must carry nothing. If this fires, the order
        # already believes there is something to get wrong here.
        "bare", "blank", "unmarked", "featureless", "no lettering", "no letter", "no text",
        "no wordmark", "no badge", "no emblem", "no nameplate", "no name plate", "no logo",
        "no insignia", "no characters", "no numerals", "no digits", "no writing", "no print",
        "no marks", "no mark of any kind", "not one readable character", "never legible",
        "completely bare", "plain and unmarked", "no signage")),
    ("vehicle_surfaces", (
        "pickup", "truck", "car", "saloon", "sedan", "van", "vehicle", "tailgate", "grille",
        "grill", "bumper", "bonnet", "hood", "wheel", "wheels", "cab", "crew cab",
        "number plate", "numberplate", "licence plate", "license plate", "registration plate",
        "tractor", "trailer", "windscreen", "windshield")),
    ("hands", (
        "hand", "hands", "finger", "fingers", "fingertip", "fingertips", "palm", "palms",
        "thumb", "thumbs", "knuckle", "knuckles", "fist", "grip", "gripping", "clasped",
        "interlaced", "interlocked", "holding", "held in", "resting on the")),
    ("faces", (
        # NOT the bare words "face" / "mouth": on this subject matter they are the face of a
        # placard, the flat face of a squared post and the mouth of a farm track. Measured on
        # EP66: bare "face" fired on L170, L172 and L175, none of which contains a person.
        "facial", "portrait", "head and shoulders", "eyes", "profile", "expression", "gaze",
        "looking at the camera", "weathered face", "his face", "her face", "their face",
        "the face of a", "no smile", "likeness")),
    ("sign_faces", (
        "placard", "sign", "signs", "signage", "board", "notice", "poster", "banner",
        "plaque", "label", "nameplate", "name plate", "blaze", "marker", "stencil",
        "billboard", "headline")),
    ("documents", (
        "paper", "papers", "document", "documents", "sheet", "sheets", "letter", "letters",
        "form", "forms", "report", "file", "folder", "envelope", "card", "ledger", "book",
        "page", "pages", "certificate", "contract", "receipt", "map", "chart", "newspaper")),
    ("screens", (
        "screen", "screens", "monitor", "display", "laptop", "computer", "phone", "tablet",
        "terminal", "panel", "gauge", "dial", "meter", "readout", "keypad")),
    ("device_objects", (
        # not bare "camera": in every one of these orders it is the camera POSITION
        # ("seen from the camera", "camera at chest height"), not an object in the frame.
        "box", "canister", "trail camera", "compact camera", "lens", "viewfinder", "case",
        "housing", "unit", "instrument", "device", "padlock", "hasp", "badge", "emblem",
        "logo", "seal", "stamp", "dial", "shutter")),
)


# =========================================================================================
# small helpers
# =========================================================================================
def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _atomic_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _load_json(path: Path) -> tuple[dict, str]:
    if not path.is_file():
        return {}, ""
    try:
        return json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:  # noqa: BLE001
        return {}, f"{_rel(path)} is unreadable ({exc})"


def _pid(name: str) -> str:
    """`L170.png` -> `L170`. Plate id without the extension, uppercased."""
    return Path(name).stem.upper()


# =========================================================================================
# the plate directory.  `check_plate_verdicts.resolve_plate_dir` decides which one -- render
# truth (`remotion/public/<slug>/img`) once plates are staged, the Codex delivery directory
# before that -- and this watcher must watch the SAME one the gate reads, or the two will
# disagree about which pictures exist.
# =========================================================================================
def watch_dir(slug: str, override: str | None = None) -> tuple[Path, str]:
    if override:
        return Path(override), "explicit --plate-dir"
    return resolve_plate_dir(slug)


# =========================================================================================
# the order.  This is where the reference plate for a callback, and the surfaces that must
# be bare, actually come from -- they are written down, so they are read rather than guessed.
# =========================================================================================
def order_files(slug: str) -> list[Path]:
    """Every `EP##_<slug>_CODEX_BATCH_*.md`, oldest batch first, newest version last.

    Sorted so that a later batch overwrites an earlier one for the same id: batch C re-ordered
    21 of batch B's plates in place, and the live contract for those 21 is C.
    """
    return sorted(PLANNING.glob(f"EP*_{slug}_CODEX_BATCH_*.md"))


def paste_files(slug: str) -> list[Path]:
    """The `CODEX_PASTE` texts, which carry the FULL prompt.

    EP66 wrote every prompt into the order markdown as a bullet. EP68 and EP69 write a TABLE
    into the markdown with the prompt truncated at about 160 characters and an ellipsis, and
    put the full text only in the paste files (`■ R001.png` then the prompt). A truncated
    prompt would silently lose the trigger words at the end of the sentence -- which on EP68's
    `R002` is `no character can be made out`, the whole point of the plate -- so the paste
    files are read too.
    """
    out: list[Path] = []
    for p in sorted(PLANNING.glob(f"EP*_{slug}_CODEX_PASTE*")):
        if p.is_dir():
            out.extend(sorted(p.glob("*.txt")))
        elif p.suffix.lower() == ".txt":
            out.append(p)
    return out


def _batch_key(p: Path) -> tuple[str, int, str]:
    """Sort key that interleaves each batch's markdown with its own paste text.

    `..._CODEX_BATCH_C.v001.md` and `..._CODEX_PASTE_C/batch_03.txt` are the SAME order; the
    paste must not be applied after a LATER batch's markdown. Key = (batch letter, md-before-
    paste, filename). A paste directory with no letter (`..._CODEX_PASTE`) is batch A.
    """
    s = p.as_posix()
    m = re.search(r"CODEX_(BATCH|PASTE)_?([A-Z])?\b", s)
    kind, letter = (m.group(1), m.group(2) or "A") if m else ("PASTE", "A")
    return (letter, 0 if kind == "BATCH" else 1, s)


def parse_orders(slug: str) -> tuple[dict[str, dict], list[str]]:
    """id -> {order, section, heading, why, prompt, refs, thumb}. Later batches win.

    The anchor is the one thing every batch writes the same way: a line that is exactly
    ``- `L170.png` `` followed by the prompt paragraph. Around it:

      * `section`  the nearest preceding `###` heading (batch B groups plates under
                   `### THUMB（6枚）`; that is how a THUMB plate is identified).
      * `heading`  a `###` heading that names THIS plate (batch C gives every re-ordered
                   plate its own).
      * `why`      the lines between that own-heading and the bullet -- in batch C this is
                   `**作り直す理由:**`, which is where the callback's reference plate is named.
      * `refs`     OTHER plate ids appearing in this plate's OWN heading, its `why`, or its
                   prompt. Deliberately NOT the nearest section heading: batch B's section
                   headings are followed by a table listing every id in the section, and
                   reading that as a reference would make every plate a reference to its
                   four neighbours. Batch C's per-plate blocks are clean, and they are the
                   ones that record the callbacks.
    """
    out: dict[str, dict] = {}
    notes: list[str] = []

    def _put(pid: str, rec: dict) -> bool:
        """Later source wins -- except a TRUNCATED prompt never overwrites a full one."""
        prev = out.get(pid)
        if prev and rec.get("truncated") and not prev.get("truncated") and prev.get("prompt"):
            prev.update({k: v for k, v in rec.items()
                         if k not in ("prompt", "truncated") and v})
            return False
        if prev:
            for k in ("section", "heading", "why", "refs", "thumb"):
                if not rec.get(k) and prev.get(k):
                    rec[k] = prev[k]
        out[pid] = rec
        return True

    sources = sorted(order_files(slug) + paste_files(slug), key=_batch_key)

    # Which id prefixes are real for this episode. Taken only from the forms that carry the
    # FILENAME (``- `L070.png` `` / ``■ R001.png``), because those cannot be anything but a
    # plate. A markdown table row cannot: EP66's batch A carries a QC-criteria table whose
    # first column is `Q10`, `Q11`, and reading those as plates put two plates in the order
    # that have never existed. Prefix, not id, so a table-only episode still parses.
    known_prefixes: set[str] = set()
    for f in sources:
        for m in re.finditer(r"(?:^-\s+`|^■\s*)([A-Za-z]{1,3})\d{2,4}\.png",
                             f.read_text(encoding="utf-8", errors="replace"), re.M):
            known_prefixes.add(m.group(1).upper())

    for f in sources:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        # Ids this file states properly. A table row for one of them is NOT its prompt: batch
        # B's section tables carry the SCRIPT LINE a plate lands on, and its §0.6 table pairs
        # the callbacks, both in a two-column shape indistinguishable from a prompt row. Read
        # as prompts they inflated batch B from 191 plates to 288.
        proper = {m.group(1).upper() for m in
                  (re.match(r"^(?:-\s+`|■\s*)([A-Za-z]{1,3}\d{2,4})\.png", ln) for ln in lines)
                  if m}
        section = ""
        own_heading = ""
        since_heading: list[str] = []
        n_in_file = 0
        for i, raw in enumerate(lines):
            line = raw.rstrip()

            m_head = re.match(r"^#{2,4}\s+(.*)$", line)
            if m_head:
                text = m_head.group(1)
                ids = ID_IN_TEXT.findall(re.sub(r"`", " ", text.replace(".png", "")))
                # a heading that names exactly one plate is that plate's own heading
                own_heading = text if len(set(ids)) == 1 else ""
                if not own_heading:
                    section = text
                since_heading = []
                continue

            # three prompt forms, all of them live in this repo right now:
            #   EP66 markdown : ``- `L070.png` `` then the prompt on the next line
            #   EP68/69 paste : ``■ R001.png``   then the prompt on the next line
            #   EP68/69 table : ``| R001 | prompt... | no | HOOK 0:00 |`` (TRUNCATED)
            m_b = re.match(r"^(?:-\s+`|■\s*)([A-Za-z]{1,3}\d{2,4})\.png`?\s*$", line)
            m_t = re.match(r"^\|\s*`?([A-Za-z]{1,3}\d{2,4})`?\s*\|\s*(.+?)\s*\|", line)
            if not m_b and not m_t:
                since_heading.append(line)
                continue

            if m_b:
                pid = m_b.group(1).upper()
                body: list[str] = []
                for j in range(i + 1, len(lines)):
                    nxt = lines[j].rstrip()
                    if not nxt:
                        if body:
                            break
                        continue
                    if re.match(r"^(-\s+`|■|#{2,4}\s|\*\*|>|\||---|─)", nxt):
                        break
                    body.append(nxt)
                prompt = " ".join(body).strip()
            else:
                pid = m_t.group(1).upper()
                prompt = m_t.group(2).strip()
                prefix = re.match(r"[A-Z]+", pid).group(0)
                if (pid in proper or len(prompt) < 40
                        or (known_prefixes and prefix not in known_prefixes)):
                    since_heading.append(line)      # a legend row, a count, a QC criterion
                    continue
            if not prompt:
                since_heading.append(line)
                continue
            truncated = bool(re.search(r"(…|\.\.\.)\s*$", prompt))

            own = own_heading if pid in own_heading.replace(".png", "") else ""
            # `why` -- and therefore the reference ids in it -- is read ONLY out of a block
            # that this plate owns. Batch B puts a table of five ids under each section
            # heading, and reading that as context would make every plate a reference to its
            # four neighbours (measured: L070 came back citing L071-L074).
            why = " ".join(x for x in since_heading if x.strip()) if own else ""
            # Only ids with a prefix this episode actually uses. Batch C's own re-order note
            # for L099 opens "Q11 CARD BACKGROUND", and `Q11` is a QC criterion, not a plate.
            cand = {r.upper() for r in ID_IN_TEXT.findall(f"{own} {why} {prompt}")} - {pid}
            refs = sorted(r for r in cand
                          if not known_prefixes
                          or re.match(r"[A-Z]+", r).group(0) in known_prefixes)
            n_in_file += _put(pid, {
                "order": _rel(f),
                "section": section,
                "heading": own,
                "why": why[:600],
                "prompt": prompt,
                "truncated": truncated,
                "refs": refs,
                "thumb": ("THUMB" in section.upper()) or ("THUMB" in own.upper()),
            })
            since_heading = []
        if n_in_file:
            notes.append(f"{_rel(f)}: {n_in_file} plate prompt(s)")
    if len(notes) > 6:               # 50 paste batches is not a useful thing to print
        notes = [f"{len(notes)} order/paste file(s) under episodes/_planning/, "
                 f"{len(out)} distinct plate id(s); newest: "
                 + ", ".join(_rel(p) for p in sources[-2:])]
    return out, notes


def crop_triggers(prompt: str) -> list[str]:
    """Which trigger categories this plate's ORDER fires, and on which words.

    A PROMPT for the reviewer. There is no detector behind any of it -- see the docstring.
    An empty list means the ORDER named nothing that must be bare. It does not mean the plate
    is clean.
    """
    hay = _words(prompt)
    hits: list[str] = []
    for cat, words in CROP_TRIGGERS:
        found = sorted({w for w in words if _hits(w, hay)})
        if found:
            hits.append(f"{cat}:{'/'.join(found[:4])}")
    return hits


# =========================================================================================
# mechanical measurement
# =========================================================================================
def _dhash(grey: np.ndarray) -> str:
    """256-bit difference hash from the reduced luma. Cheap, and stable under a re-encode."""
    im = Image.fromarray(grey.astype(np.uint8)).resize((DHASH_SIDE + 1, DHASH_SIDE),
                                                       Image.LANCZOS)
    a = np.asarray(im, dtype=np.int16)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return f"{v:064x}"


def measure_plate(path: Path, is_thumb: bool) -> dict:
    """Everything the pixels can say. Never a content judgement.

    Raises on a truncated/undecodable file; the caller turns that into a state, because
    "cannot decode yet" and "will never decode" are different answers and only mtime age
    separates them.
    """
    im = Image.open(path)
    im.load()                      # force the full decode: a half-written PNG raises HERE
    im = im.convert("RGB")
    w, h = im.size
    red = im.resize((REF_W, REF_H), Image.LANCZOS)
    a = np.asarray(red, dtype=np.float64)
    g = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]

    x0, x1 = int(SUBJ_X0 * REF_W), int(SUBJ_X1 * REF_W)
    y0, y1 = int(SUBJ_Y0 * REF_H), int(SUBJ_Y1 * REF_H)
    box = g[y0:y1, x0:x1]

    out = {
        "width": w,
        "height": h,
        "aspect": round(w / h, 4) if h else 0.0,
        "mean_luma": round(float(g.mean()), 1),
        "contrast_sd": round(float(g.std()), 1),
        "subject_luma": round(float(box.mean()), 1) if box.size else 0.0,
        "p1": round(float(np.percentile(g, 1)), 1),
        "p99": round(float(np.percentile(g, 99)), 1),
        "crushed_pct": round(float((g <= CRUSHED_LEVEL).mean() * 100.0), 2),
        "blown_pct": round(float((g >= BLOWN_LEVEL).mean() * 100.0), 2),
        "dhash": _dhash(g),
        "measured_in": f"{REF_W}x{REF_H} Lanczos reduction",
    }
    if is_thumb:
        try:
            out["headline_band"] = band_measure(path)
        except Exception as exc:  # noqa: BLE001
            out["headline_band"] = {"error": f"{type(exc).__name__}: {exc}"}
    return out


def refresh_nearest(plates: dict) -> dict:
    """Recompute every plate's nearest neighbour and its near-duplicate PROMPT.

    Recomputed over the whole set on every pass, not incrementally, because the relation is
    symmetric and a plate measured at 09:00 has to learn about its twin measured at 11:00.
    260 plates is 67k 256-bit comparisons -- about 70 ms.

    THE THRESHOLD IS THE BATCH'S OWN DISTRIBUTION, not a constant. Measured on EP66's 260
    plates the nearest-neighbour distance runs from 35 to a median of 88 bits, and the two
    tightest pairs in the whole episode are `L075`~`L170` (35) and `L096`~`L173` (40) -- which
    are two of the three DESIGNED callbacks, i.e. the tool ranks the intended repeats top.
    Any fixed threshold either misses those or, set low enough to be "safe", fires never: at
    the 12/256 this file first used, nothing fired at all.

    This is a diversity prompt (`footage_diversity`: the owner's standing note that plates and
    clips repeat too much), NEVER a rejection, and it is explicitly NOT a pair verifier. The
    other two designed callbacks, `L074`~`L172` (115) and `L082`~`L175` (113), sit near the
    median and were both judged to HOLD by eye. A perceptual hash sees layout and tone; it
    does not see whether the post is squared.
    """
    ids = [n for n, v in plates.items() if (v.get("mechanical") or {}).get("dhash")]
    if len(ids) < 2:
        return {}
    hs = {n: int(plates[n]["mechanical"]["dhash"], 16) for n in ids}
    near: dict[str, tuple[str, int]] = {}
    for a in ids:
        ha = hs[a]
        best, bid = 1 << 30, ""
        for b in ids:
            if b == a:
                continue
            d = bin(ha ^ hs[b]).count("1")
            if d < best:
                best, bid = d, b
        near[a] = (bid, best)
    dists = sorted(d for _, d in near.values())
    cut = (dists[max(0, min(len(dists) - 1,
                            int(round((OUTLIER_PCT / 100.0) * (len(dists) - 1)))))]
           if len(dists) >= MIN_FOR_OUTLIERS else -1)
    for a in ids:
        bid, d = near[a]
        plates[a]["nearest"] = {"id": _pid(bid), "hamming": d}
        soft = [f for f in (plates[a].get("flags_soft") or [])
                if not f.startswith("NEAR-DUPLICATE")]
        if cut >= 0 and d <= cut:
            expected = _pid(bid) in (plates[a].get("refs") or [])
            soft.append(
                f"NEAR-DUPLICATE PROMPT (not a floor, and not a pair check): closest plate in "
                f"this episode is {_pid(bid)} at {d}/256 bits, inside the tightest "
                f"{OUTLIER_PCT:g}% of this batch's {len(dists)} nearest-neighbour distances "
                f"(<= {cut}). "
                + ("The order names it as this plate's reference, so a repeat is INTENDED -- "
                   "look at whether it is the SAME frame, which no hash can tell you."
                   if expected else
                   "The order does NOT name it as a reference. Two plates this alike is the "
                   "footage_diversity problem, on the still side."))
        plates[a]["flags_soft"] = soft
    return {"n": len(dists), "min": dists[0], "median": dists[len(dists) // 2], "cut": cut}


def batch_percentiles(mechs: list[dict]) -> dict:
    """The batch's OWN distribution on each measure. Used for outlier prompts, not for floors.

    Needs enough plates to mean anything; under MIN_FOR_OUTLIERS it returns {} and no outlier
    prompt is issued at all, which is the correct answer for the first eight plates of a run.
    """
    if len(mechs) < MIN_FOR_OUTLIERS:
        return {}
    out: dict = {}
    for key, lo in (("mean_luma", True), ("contrast_sd", True), ("subject_luma", True),
                    ("crushed_pct", False)):
        xs = sorted(m[key] for m in mechs if key in m)
        if not xs:
            continue
        i = max(0, min(len(xs) - 1, int(round((OUTLIER_PCT / 100.0) * (len(xs) - 1)))))
        j = len(xs) - 1 - i
        out[key] = xs[i] if lo else xs[j]
    out["_n"] = len(mechs)
    return out


def mechanical_flags(m: dict, expect_wh: tuple[int, int] | None, is_thumb: bool,
                     pct: dict | None = None) -> dict:
    """Split the numbers into HARD (a machine may reject) and SOFT (a reviewer must look).

    HARD is deliberately tiny: the file does not decode, or it is not the size and shape the
    rest of the batch is. Nobody's opinion changes either.

    SOFT is where the discipline is, and the first version of this function got it wrong in a
    way worth recording. It applied `check_final_acceptance`'s THUMB floors -- contrast >= 40,
    subject luma >= 60 -- to every plate. Run against EP66 it flagged 82 of the 184 plates a
    human had already ACCEPTED. Those floors are not wrong; they are floors for a THUMBNAIL,
    which has to punch at 320px in a feed. A body plate in this film is ordered "low contrast
    but never crushed" IN ITS OWN STYLE BLOCK, and the accepted set runs down to contrast 24.1
    (`L147`), subject luma 41.9 (`L209`) and mean 43.8. A gate whose floor is tighter than the
    work its own episode already accepted is not measuring quality, it is manufacturing
    failures, and it gets switched off. So:

      THUMB plates    get the thumbnail contract, cited: mean >= 33 and contrast >= 40
                      (`check_final_acceptance`), subject >= 60
                      (`check_thumb_subject_luma`), and the clear upper region
                      (`check_thumb_headline_band`).
      EVERY plate     gets the two universal ones, which are about a broken image rather than
                      a taste: near-black (`check_pool_frames.NEAR_BLACK_MEAN`, 12.0) and
                      blown out (mean >= 240, or 70% of pixels pinned at the top).
      BODY plates     get NO luma or contrast floor. Their numbers are printed in the packet
                      and the reviewer reads them. What they get instead is an OUTLIER prompt:
                      bottom/top 2% OF THIS BATCH'S OWN DISTRIBUTION. That is a comparison
                      against the episode rather than against a constant, it costs nothing
                      when the batch is uniform, and it says "open this one first" rather than
                      "this one is bad".
    """
    hard: list[str] = []
    soft: list[str] = []
    if max(m["width"], m["height"]) < MIN_LONG_EDGE:
        hard.append(f"long edge {max(m['width'], m['height'])} < {MIN_LONG_EDGE} "
                    f"(PD_ONE_PASS_PRODUCTION_SPEC.v2 row 5; the order repeats it)")
    if abs(m["aspect"] - 16 / 9) > ASPECT_TOL * (16 / 9):
        hard.append(f"aspect {m['aspect']:.4f} is not 16:9")
    # The batch's modal size is a PROMPT, never a rejection, and the reason is measured: on
    # EP67 ramirez, 74 of the 90 plates delivered so far are 1672x941 and only 16 are the
    # contracted 3840x2160. A "differs from the mode" rule rejects THE SIXTEEN CORRECT PLATES.
    # The mode is whatever the generator happened to do most often; it is not the contract.
    if expect_wh and (m["width"], m["height"]) != expect_wh:
        soft.append(f"size {m['width']}x{m['height']} differs from the batch's most common "
                    f"{expect_wh[0]}x{expect_wh[1]} -- worth knowing which of the two is right")

    # universal: a broken image, not a matter of taste
    if m["mean_luma"] < NEAR_BLACK_MEAN:
        soft.append(f"NEAR BLACK: mean luma {m['mean_luma']} < {NEAR_BLACK_MEAN:g} "
                    f"(check_pool_frames.NEAR_BLACK_MEAN)")
    if m["mean_luma"] >= BLOWN_OUT_MEAN or m["blown_pct"] >= BLOWN_OUT_FRAC * 100:
        soft.append(f"BLOWN OUT: mean {m['mean_luma']}, {m['blown_pct']}% of pixels pinned "
                    f"(check_shipped_frames floors)")

    if is_thumb:
        if m["mean_luma"] < MIN_MEAN_LUMA:
            soft.append(f"THUMB mean luma {m['mean_luma']} < {MIN_MEAN_LUMA:g} "
                        f"(check_final_acceptance.THUMB_MIN_MEAN_LUMA)")
        if m["contrast_sd"] < MIN_CONTRAST_STD:
            soft.append(f"THUMB contrast {m['contrast_sd']} < {MIN_CONTRAST_STD:g} "
                        f"(check_final_acceptance.THUMB_MIN_CONTRAST_STD)")
        if m["subject_luma"] < MIN_SUBJECT_LUMA:
            soft.append(f"THUMB subject luma {m['subject_luma']} < {MIN_SUBJECT_LUMA:g} "
                        f"(check_thumb_subject_luma.SUBJECT_MIN_LUMA)")
        hb = m.get("headline_band") or {}
        if hb.get("error"):
            soft.append(f"headline band unmeasurable: {hb['error']}")
        elif not hb.get("ok"):
            soft.append(
                f"THUMB headline band: clear_rows {hb.get('clear_rows')} (floor 174), "
                f"non_sky {hb.get('non_sky_pct')}% (<=1.0), edge {hb.get('edge_pct')}% "
                f"(<=1.0) -- check_thumb_headline_band. If clear_rows is 0 with edge 0.00 "
                f"and a high band mean, suspect the LENS VIGNETTE and re-measure with "
                f"--inset-pct 6: that is exactly what EP66's L256 turned out to be, and it "
                f"was accepted on the substance")
    elif pct:
        for key, label, low in (("mean_luma", "mean luma", True),
                                ("contrast_sd", "contrast", True),
                                ("subject_luma", "subject luma", True),
                                ("crushed_pct", "crushed-black %", False)):
            if key not in pct:
                continue
            if (m[key] <= pct[key]) if low else (m[key] >= pct[key]):
                soft.append(
                    f"OUTLIER (not a floor): {label} {m[key]} is in the "
                    f"{'bottom' if low else 'top'} {OUTLIER_PCT:g}% of this batch's own "
                    f"{pct['_n']} measured plates ({'<=' if low else '>='} {pct[key]}). "
                    f"Open it early.")
    return {"hard": hard, "soft": soft}


# =========================================================================================
# review packet
# =========================================================================================
def _save_jpg(im: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path, "JPEG", quality=JPEG_Q, optimize=True)


def _label(im: Image.Image, text: str) -> Image.Image:
    """A caption bar under an image. A crop with no label is a crop nobody can act on."""
    f = _font(22)
    bar = 34
    out = Image.new("RGB", (im.width, im.height + bar), (16, 16, 20))
    out.paste(im.convert("RGB"), (0, 0))
    ImageDraw.Draw(out).text((8, im.height + 6), text[:220], fill=(225, 225, 232), font=f)
    return out


def build_packet(path: Path, pid: str, out_dir: Path, triggers: list[str],
                 refs: list[Path], zoom: bool) -> dict:
    """The files a content reviewer opens. Returns their repo-relative paths."""
    d = out_dir / pid
    d.mkdir(parents=True, exist_ok=True)
    im = Image.open(path)
    im.load()
    im = im.convert("RGB")
    made: dict = {"full": "", "zooms": [], "pairs": []}

    prox = im.resize((PROXY_W, max(1, round(PROXY_W * im.height / im.width))), Image.LANCZOS)
    p_full = d / "full.jpg"
    _save_jpg(_label(prox, f"{pid}  full frame, {im.width}x{im.height} shown at {PROXY_W}px "
                           f"-- a 53x12px wordmark is NOT visible here"), p_full)
    made["full"] = _rel(p_full)

    if zoom and triggers:
        # The whole plate at 1:1, tiled. No localisation is attempted, because none is
        # possible: there is no tailgate detector here. 3840x2160 -> exactly 3x3.
        cols = max(1, math.ceil(im.width / CROP_W))
        rows = max(1, math.ceil(im.height / CROP_H))
        for r in range(rows):
            for c in range(cols):
                l = min(c * CROP_W, max(0, im.width - CROP_W))
                t = min(r * CROP_H, max(0, im.height - CROP_H))
                tile = im.crop((l, t, min(l + CROP_W, im.width), min(t + CROP_H, im.height)))
                p = d / f"zoom_r{r + 1}c{c + 1}.jpg"
                _save_jpg(_label(tile, f"{pid}  1:1 NATIVE  tile r{r + 1}c{c + 1} of "
                                       f"{rows}x{cols}  at ({l},{t})  |  look for: "
                                       f"{', '.join(triggers)[:150]}"), p)
                made["zooms"].append(_rel(p))

    for ref in refs:
        try:
            rim = Image.open(ref)
            rim.load()
            rim = rim.convert("RGB")
        except Exception:  # noqa: BLE001
            continue
        hh = max(1, round(PAIR_W * im.height / im.width))
        rh = max(1, round(PAIR_W * rim.height / rim.width))
        H = max(hh, rh)
        canvas = Image.new("RGB", (PAIR_W * 2 + 12, H), (16, 16, 20))
        canvas.paste(rim.resize((PAIR_W, rh), Image.LANCZOS), (0, 0))
        canvas.paste(im.resize((PAIR_W, hh), Image.LANCZOS), (PAIR_W + 12, 0))
        p = d / f"pair_{_pid(ref.name)}.jpg"
        _save_jpg(_label(canvas, f"LEFT = {_pid(ref.name)} (the reference the order names)   "
                                 f"RIGHT = {pid} (the callback).  Same object? Same post? "
                                 f"Same framing? No machine can answer this."), p)
        made["pairs"].append(_rel(p))
    return made


# =========================================================================================
# the verdict file.  IT IS `check_plate_verdicts.py`'S FILE AND ITS SCHEMA.
#
# That gate landed while this was being written and is wired into `check_episode_inputs.py`
# and `preflight_render_gate.py`. It owns: the schema, the plate set (declared
# `mandatory_stills` UNION every non-depth png on disk), which directory counts, the id-list
# binding, and the invalidation. Every one of those is IMPORTED, not re-implemented, so the
# two files cannot drift into two answers:
#
#   scaffold()      stamps every id with its current sha256, PRESERVES a verdict whose sha is
#                   unchanged and RESETS one whose picture has changed. This watcher calls it
#                   once per pass, which is the whole regeneration-invalidates mechanism --
#                   there is no second copy of it here.
#   plate_state()   the gate's own answer, printed in this tool's receipt so the operator sees
#                   the same verdict the build will see.
#   _norm_verdict() accept / reject / everything-else-is-unresolved. `flag` BLOCKS.
#
# What this file adds is only the two things the gate deliberately does not do: it measures
# the pixels, and it puts the picture in front of a reviewer.
# =========================================================================================
def verdict_path(slug: str, override: str | None = None) -> Path:
    return Path(override) if override else QC / f"{slug}_plate_verdicts.v001.json"


def read_plates(vpath: Path) -> dict:
    """The `plates` map, or {}. Never invents one -- `scaffold()` creates the file."""
    data, err = load_verdicts(vpath)
    if err and "no " not in err:
        raise SystemExit(f"REFUSING TO WRITE: {err}. Fix or move it; overwriting a verdict "
                         f"file that failed to parse would silently discard verdicts.")
    got = data.get(PLATES_KEY)
    return got if isinstance(got, dict) else {}


def write_plates(vpath: Path, plates: dict) -> None:
    """Put a mutated `plates` map back, leaving every other key exactly as it was."""
    data, err = load_verdicts(vpath)
    if err and "no " not in err:
        raise SystemExit(f"REFUSING TO WRITE: {err}")
    data[PLATES_KEY] = plates
    _atomic_json(vpath, data)


def verdict_counts(vpath: Path) -> dict:
    plates = read_plates(vpath)
    out = {"accept": 0, "reject": 0, "unresolved": 0}
    for v in plates.values():
        out[_norm_verdict((v or {}).get("verdict"))] += 1
    return out



# receipt (the watcher's cache)
# =========================================================================================
def receipt_path(slug: str) -> Path:
    return QC / f"{slug}_plate_watch.v001.json"


def packet_dir(slug: str) -> Path:
    return QC / f"{slug}_plate_watch"


# =========================================================================================
# one pass
# =========================================================================================
def do_pass(cfg: dict, rec: dict, first: bool) -> dict:
    slug = cfg["slug"]
    pdir: Path = cfg["pdir"]
    orders: dict = cfg["orders"]
    spec = cfg["spec"]
    declared: set[str] = cfg["declared"]
    era = era_of(spec)
    only: set[str] | None = cfg["only"]

    seen = plates_on_disk(pdir)
    if only:
        seen = [p for p in seen if _pid(p.name) in only]
    obs = rec.setdefault("observations", {})
    plates = rec.setdefault("plates", {})
    now = time.time()

    # ---- what has settled, what has changed -------------------------------------------
    todo: list[Path] = []
    unsettled: list[str] = []
    for p in seen:
        try:
            st = p.stat()
        except OSError:
            continue
        key = f"{st.st_size}:{int(st.st_mtime)}"
        prev = obs.get(p.name)
        obs[p.name] = key
        age = now - st.st_mtime
        if age < cfg["settle_sec"] or (prev is not None and prev != key):
            unsettled.append(p.name)
            continue
        cached = plates.get(p.name)
        if cached and cached.get("stat_key") == key and cached.get("state") != "unsettled":
            continue
        todo.append(p)

    # ---- measure -----------------------------------------------------------------------
    def _one(p: Path) -> tuple[str, dict]:
        pid = _pid(p.name)
        o = orders.get(pid) or {}
        is_thumb = bool(o.get("thumb"))
        try:
            m = measure_plate(p, is_thumb)
        except Exception as exc:  # noqa: BLE001
            return p.name, {"state": "undecodable", "error": f"{type(exc).__name__}: {exc}"}
        return p.name, {"state": "measured", "mechanical": m,
                        "sha256": _sha256(p), "bytes": p.stat().st_size}

    results: dict[str, dict] = {}
    if todo:
        with ThreadPoolExecutor(max_workers=cfg["workers"]) as ex:
            for name, r in ex.map(_one, todo):
                results[name] = r

    # The batch's own modal resolution, over everything measured so far plus this pass, so a
    # lone 1024x1024 plate stands out without anybody having to declare a number the order
    # never wrote down. Computed AFTER measuring, so the very first pass is not exempt.
    sizes: dict[tuple[int, int], int] = {}
    for src in (plates.values(), results.values()):
        for v in src:
            m = v.get("mechanical") or {}
            if m.get("width"):
                sizes[(m["width"], m["height"])] = sizes.get((m["width"], m["height"]), 0) + 1
    expect_wh = max(sizes, key=sizes.get) if sizes else None

    # The batch's own distribution, over every BODY plate measured so far plus this pass.
    # Thumbnails are excluded because they are deliberately lit two stops harder and would
    # drag the percentile off the population it is meant to describe.
    body_mechs: list[dict] = []
    for name, v in plates.items():
        if v.get("mechanical") and not v.get("thumb"):
            body_mechs.append(v["mechanical"])
    for name, v in results.items():
        o = orders.get(_pid(name)) or {}
        if v.get("mechanical") and not o.get("thumb"):
            body_mechs.append(v["mechanical"])
    pct = batch_percentiles(body_mechs)

    newly, broke = [], []

    for p in todo:
        r = results.get(p.name) or {}
        pid = _pid(p.name)
        o = orders.get(pid) or {}
        st = p.stat()
        key = f"{st.st_size}:{int(st.st_mtime)}"
        if r.get("state") == "undecodable":
            age = now - st.st_mtime
            if age < max(cfg["settle_sec"] * 4, 12.0):
                unsettled.append(p.name)          # probably still being written
                plates[p.name] = {"state": "unsettled", "stat_key": key}
                continue
            plates[p.name] = {"state": "undecodable", "stat_key": key,
                              "error": r.get("error", ""), "declared": p.name in declared,
                              "flags_hard": ["does not decode"], "flags_soft": []}
            broke.append(p.name)
            continue

        prev = plates.get(p.name) or {}
        prev_sha = prev.get("sha256")
        sha = r["sha256"]

        m = r["mechanical"]
        is_thumb = bool(o.get("thumb"))
        fl = mechanical_flags(m, expect_wh, is_thumb, pct)

        trig = crop_triggers(o.get("prompt", "")) if o else []
        eprompts = era_prompts(_words(o.get("prompt", "")), era) if o else []

        # --- packet ---------------------------------------------------------------------
        refs = []
        for rid in (o.get("refs") or []):
            rp = pdir / f"{rid}.png"
            if rp.is_file():
                refs.append(rp)
        packet = build_packet(p, pid, cfg["packets"], trig, refs,
                              zoom=cfg["zoom"]) if cfg["packet"] else {}

        plates[p.name] = {
            "state": "awaiting_content_verdict" if not fl["hard"] else "machine_rejected",
            "stat_key": key,
            "sha256": sha,
            "bytes": r["bytes"],
            "declared": p.name in declared,
            "ordered": bool(o),
            "order": o.get("order", ""),
            "section": o.get("section", ""),
            "thumb": is_thumb,
            "refs": o.get("refs") or [],
            "prompt": o.get("prompt", ""),
            "why_reordered": o.get("why", ""),
            "crop_triggers": trig,
            "era_prompts": eprompts,
            "nearest": None,                     # filled by refresh_nearest() below
            "mechanical": m,
            "flags_hard": fl["hard"],
            "flags_soft": fl["soft"],
            "packet": packet,
            "measured_at": _now(),
            "batch": None,
            "regenerated": bool(prev_sha and prev_sha != sha),
        }
        newly.append(p.name)

    near_stats = refresh_nearest(plates) if newly else (rec.get("nearest_stats") or {})

    # ---- hand the set to the gate's own scaffold ------------------------------------------
    # This is the ONLY place a verdict is invalidated, and it is not this file's code. The
    # scaffold stamps every id in the gate's plate set with its current sha256, keeps a verdict
    # whose picture is unchanged, and RESETS to `unresolved` any whose picture has moved. A
    # regenerated plate therefore loses its verdict without this watcher having to remember
    # anything, and it loses it in the same way whether the watcher is running or not.
    sc = scaffold(slug, spec, pdir, cfg["vpath"], reviewer="")
    cleared = [f"{n} (regenerated -> reset to unresolved)" for n in sc["reset"]]

    # ---- the one verdict a machine is allowed to write on its own --------------------------
    # Not "this plate is bad". Only "this file is not a usable 16:9 plate at all", which is not
    # a matter of opinion. Everything else stays `unresolved` and waits for a person.
    vplates = read_plates(cfg["vpath"])
    wrote_machine = 0
    for name, v in plates.items():
        if not v.get("flags_hard") or name not in vplates:
            continue
        cur = vplates[name]
        note = "MECHANICAL: " + "; ".join(v["flags_hard"])
        if _norm_verdict(cur.get("verdict")) != "reject" or cur.get("note") != note:
            vplates[name] = {"verdict": "reject", "sha256": v.get("sha256", ""), "note": note}
            wrote_machine += 1
    if wrote_machine:
        write_plates(cfg["vpath"], vplates)

    # ---- batch whatever is still unresolved -----------------------------------------------
    counts = verdict_counts(cfg["vpath"])
    unresolved = {n for n, v in read_plates(cfg["vpath"]).items()
                  if _norm_verdict((v or {}).get("verdict")) == "unresolved"}
    awaiting = sorted(n for n in unresolved
                      if n in plates and plates[n].get("state") == "awaiting_content_verdict"
                      and (plates[n].get("declared") or not cfg["declared_only"]))
    unbatched = [n for n in awaiting if not plates[n].get("batch")]
    made_batches: list[str] = []
    while unbatched:
        chunk, unbatched = unbatched[:cfg["batch"]], unbatched[cfg["batch"]:]
        rec["batch_seq"] = int(rec.get("batch_seq", 0)) + 1
        bname = f"batch_{rec['batch_seq']:04d}"
        for n in chunk:
            plates[n]["batch"] = bname
        if cfg["packet"]:
            write_batch_md(cfg, plates, chunk, bname)
        made_batches.append(bname)

    # ---- persist ---------------------------------------------------------------------------
    rec["slug"] = slug
    rec["plate_dir"] = _rel(pdir)
    rec["verdicts_file"] = _rel(cfg["vpath"])
    rec["expect_wh"] = list(expect_wh) if expect_wh else None
    rec["batch_percentiles"] = pct
    rec["nearest_stats"] = near_stats
    rec["updated_at"] = _now()
    rec["orders"] = cfg["order_notes"]
    rec["boundary"] = (
        "MECHANICAL ONLY. This receipt cannot say whether a plate is the picture that was "
        "ordered, whether a callback matches its pair, whether any text is legible, whether "
        "fingers are countable, whether a face resembles a real person, or whether it is "
        "dull. Those are content verdicts and only --record writes them.")
    _atomic_json(cfg["rpath"], rec)

    return {
        "seen": len(seen),
        "newly": len(newly),
        "awaiting": len(awaiting),
        "unresolved": counts["unresolved"],
        "accepted": counts["accept"],
        "rejected": counts["reject"],
        "cleared": cleared,
        "broke": broke,
        "unsettled": sorted(set(unsettled)),
        "batches": made_batches,
    }


def write_batch_md(cfg: dict, plates: dict, chunk: list[str], bname: str) -> None:
    """The worklist a content reviewer works from. Small, self-contained, and honest."""
    slug = cfg["slug"]
    out = cfg["packets"] / f"{bname}.md"
    L: list[str] = []
    L.append(f"# {slug} — plate content review, `{bname}` ({len(chunk)} plate(s))")
    L.append("")
    L.append(f"Written {_now()} by `scripts/watch_plate_verdicts.py`. "
             f"Plates: `{_rel(cfg['pdir'])}`.")
    L.append("")
    L.append("**The machine has measured these and has NOT judged them.** It cannot tell you "
             "whether the picture is the thing that was ordered, whether a callback matches "
             "its pair, whether any text is legible, whether fingers are countable, whether a "
             "face resembles a real person, or whether it is dull. Open the files listed "
             "under each plate and answer those yourself.")
    L.append("")
    L.append("Record the answer with:")
    L.append("")
    L.append("```")
    L.append(f"py -3.11 scripts/watch_plate_verdicts.py --slug {slug} --record \\")
    L.append("    --reviewer \"<who>\" \\")
    L.append("    --accept " + ",".join(_pid(n) for n in chunk[:3]) + " \\")
    L.append("    --reject \"<ID>=<what you saw, at what magnification>\"")
    L.append("```")
    L.append("")
    for n in chunk:
        v = plates[n]
        pid = _pid(n)
        m = v.get("mechanical") or {}
        L.append(f"## `{pid}`  —  {v.get('section') or '(no section)'}"
                 + ("  **THUMB**" if v.get("thumb") else "")
                 + ("  **declared in mandatory_stills**" if v.get("declared") else
                    "  *(not declared in mandatory_stills — but it is on disk, so the gate "
                    "still wants a verdict: the still pool is built from the directory)*"))
        L.append("")
        if v.get("prompt"):
            L.append(f"**Ordered** ({v.get('order')}): {v['prompt']}")
        else:
            L.append("**No order text found for this id.** It was not commissioned by any "
                     "`CODEX_BATCH` file in `episodes/_planning/`. Judge it against the spec, "
                     "or leave it out of the film.")
        L.append("")
        if v.get("why_reordered"):
            L.append(f"**Why it was re-ordered:** {v['why_reordered']}")
            L.append("")
        L.append(f"- mechanical: {m.get('width')}x{m.get('height')}, mean {m.get('mean_luma')}, "
                 f"contrast {m.get('contrast_sd')}, subject {m.get('subject_luma')}, "
                 f"crushed {m.get('crushed_pct')}%, p1 {m.get('p1')} "
                 f"(measured on a {m.get('measured_in')})")
        if v.get("thumb") and m.get("headline_band"):
            hb = m["headline_band"]
            L.append(f"- headline band: clear_rows {hb.get('clear_rows')} (floor 174), "
                     f"non_sky {hb.get('non_sky_pct')}%, edge {hb.get('edge_pct')}%, "
                     f"first_row {hb.get('first_row')} — "
                     f"{'PASS' if hb.get('ok') else 'FAIL'}")
        for f in v.get("flags_soft") or []:
            L.append(f"- **flag** {f}")
        for f in v.get("flags_hard") or []:
            L.append(f"- **MACHINE REJECT** {f}")
        if v.get("era_prompts"):
            L.append(f"- era/place prompt (from `episode_spec.era_setting`, a prompt and not "
                     f"a detector): {', '.join(v['era_prompts'])}")
        L.append("")
        pk = v.get("packet") or {}
        if pk.get("full"):
            L.append(f"- whole frame: `{pk['full']}`")
        if pk.get("pairs"):
            L.append(f"- **CALLBACK PAIR — the order names {', '.join(v.get('refs') or [])} as "
                     f"this plate's reference. Judge them together, not separately:**")
            for q in pk["pairs"]:
                L.append(f"    - `{q}`")
        if pk.get("zooms"):
            L.append(f"- **1:1 NATIVE crops ({len(pk['zooms'])} tiles) — the order names "
                     f"{', '.join(v.get('crop_triggers') or [])}. "
                     f"EP66's `L146` wordmark was 53x12px and invisible until 4x; `L096`'s "
                     f"licence plate needed 14x. Read the tiles, not the proxy:**")
            for q in pk["zooms"]:
                L.append(f"    - `{q}`")
        elif v.get("declared"):
            L.append("- no 1:1 crops: this plate's ORDER named no surface that must be bare. "
                     "That is a fact about the order, not a finding about the plate.")
        L.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


# =========================================================================================
# --record
# =========================================================================================
def do_record(cfg: dict, reviewer: str, accepts: list[str], rejects: dict[str, str]) -> int:
    """Write content verdicts into `check_plate_verdicts.py`'s file, in its schema.

    Every verdict is bound to the sha256 THIS TOOL MEASURED, not to whatever is on disk at the
    moment of recording -- if the plate has been rewritten between the reviewer opening the
    packet and typing the command, the scaffold on the next pass resets it, which is correct:
    they judged a picture that is no longer there.
    """
    rec, err = _load_json(cfg["rpath"])
    if err or not rec:
        print(f"no measurement receipt at {_rel(cfg['rpath'])} -- run a pass first, so a "
              f"verdict is bound to bytes somebody measured.")
        return 2
    plates = rec.get("plates") or {}
    if not (cfg["vpath"]).is_file():
        scaffold(cfg["slug"], cfg["spec"], cfg["pdir"], cfg["vpath"], reviewer=reviewer)
    vplates = read_plates(cfg["vpath"])

    def _resolve(tok: str) -> str | None:
        n = tok if tok.lower().endswith(".png") else f"{tok}.png"
        for cand in (n, n.upper(), f"{tok.upper()}.png"):
            if cand in plates:
                return cand
        return None

    bad, wrote = [], 0
    for tok in accepts:
        n = _resolve(tok)
        if not n:
            bad.append(f"{tok}: not measured -- run a pass first")
            continue
        v = plates[n]
        if v.get("flags_hard"):
            bad.append(f"{tok}: machine-rejected ({'; '.join(v['flags_hard'])}) -- fix the "
                       f"file, do not accept over it")
            continue
        vplates[n] = {"verdict": "accept", "sha256": v["sha256"],
                      "note": f"content verdict by {reviewer} {_now()}"}
        wrote += 1
    for tok, why in rejects.items():
        n = _resolve(tok)
        if not n:
            bad.append(f"{tok}: not measured -- run a pass first")
            continue
        if not why.strip():
            bad.append(f"{tok}: a rejection with no reason is not a verdict")
            continue
        vplates[n] = {"verdict": "reject", "sha256": plates[n]["sha256"],
                      "note": f"{why.strip()} [{reviewer} {_now()}]"}
        wrote += 1

    write_plates(cfg["vpath"], vplates)
    if wrote:                   # a run that recorded nothing does not get to claim the file
        # re-stamp reviewer / reviewed_at / the id-list binding through the gate's own scaffold
        scaffold(cfg["slug"], cfg["spec"], cfg["pdir"], cfg["vpath"], reviewer=reviewer)
    c = verdict_counts(cfg["vpath"])
    print(f"recorded {wrote} verdict(s) into {_rel(cfg['vpath'])} as `{reviewer}` "
          f"-- now accept {c['accept']}, reject {c['reject']}, unresolved {c['unresolved']}")
    for b in bad:
        print(f"  NOT recorded -- {b}")
    return 1 if bad else 0


# =========================================================================================
# main
# =========================================================================================
def _parse_rejects(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for it in items or []:
        if "=" not in it:
            raise SystemExit(f"--reject needs ID=reason, got {it!r}")
        k, v = it.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--plate-dir", default=None,
                    help="override check_plate_verdicts.resolve_plate_dir() "
                         "(remotion/public/<slug>/img once staged, else "
                         "E:/pd-media/assets/ai/<slug>)")
    ap.add_argument("--verdicts", default=None, help="override the verdict file path")
    ap.add_argument("--receipt", default=None,
                    help="override runs/qc/<slug>_plate_watch.v001.json (use with --plate-dir "
                         "to exercise the tool without touching the episode's own receipt)")
    ap.add_argument("--packets", default=None,
                    help="override runs/qc/<slug>_plate_watch/")
    ap.add_argument("--once", action="store_true", help="one pass over what is on disk, exit")
    ap.add_argument("--state", action="store_true", help="print the gate state only, no decode")
    ap.add_argument("--interval", type=float, default=20.0, help="seconds between passes")
    ap.add_argument("--settle-sec", type=float, default=3.0,
                    help="a file younger than this is assumed to be still being written")
    ap.add_argument("--batch", type=int, default=8, help="plates per content-review worklist")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", default=None, help="comma-separated ids, e.g. L146,L096")
    ap.add_argument("--no-packet", action="store_true", help="measure only, write no images")
    ap.add_argument("--no-zoom", action="store_true", help="packet without the 1:1 crops")
    ap.add_argument("--declared-only", action="store_true",
                    help="build worklists only for plates the spec DECLARES in "
                         "mandatory_stills. Default is everything on disk, which is also the "
                         "gate's plate set: build_case_film_generic draws its still pool from "
                         "the directory, so an undeclared plate that is staged can still reach "
                         "a cut")
    ap.add_argument("--max-passes", type=int, default=0, help="0 = until Ctrl-C")
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--reviewer", default="")
    ap.add_argument("--accept", action="append", default=[])
    ap.add_argument("--reject", action="append", default=[])
    ap.add_argument("--from-json", default=None,
                    help='bulk verdicts: {"accept":[...], "reject":{"ID":"reason"}}')
    args = ap.parse_args()

    slug = args.slug
    pdir, which_dir = watch_dir(slug, args.plate_dir)
    spec, sproblems, _ = load_and_validate(slug)
    if sproblems:
        print(f"NOTE: episode_spec for {slug} did not validate ({len(sproblems)} problem(s)); "
              f"era prompts and the declared plate set are degraded.")
        spec = spec or {}
    orders, order_notes = parse_orders(slug)
    declared = set(declared_ids(spec))

    cfg = {
        "slug": slug,
        "pdir": pdir,
        "spec": spec,
        "orders": orders,
        "order_notes": order_notes,
        "declared": declared,
        "declared_only": args.declared_only,
        "vpath": verdict_path(slug, args.verdicts),
        "rpath": Path(args.receipt) if args.receipt else receipt_path(slug),
        "packets": Path(args.packets) if args.packets else packet_dir(slug),
        "settle_sec": args.settle_sec,
        "batch": max(1, args.batch),
        "workers": max(1, args.workers),
        "packet": not args.no_packet,
        "zoom": not args.no_zoom,
        "only": ({t.strip().upper() for t in args.only.split(",") if t.strip()}
                 if args.only else None),
    }

    if args.record:
        if not args.reviewer.strip():
            raise SystemExit("--record needs --reviewer: an unattributed verdict is not one")
        acc = [t.strip() for a in args.accept for t in a.split(",") if t.strip()]
        rej = _parse_rejects(args.reject)
        if args.from_json:
            blob = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
            acc += [str(x) for x in (blob.get("accept") or [])]
            rej.update({str(k): str(v) for k, v in (blob.get("reject") or {}).items()})
        return do_record(cfg, args.reviewer.strip(), acc, rej)

    if args.state:
        st = plate_state(slug, spec, pdir, cfg["vpath"])
        print(json.dumps(st, indent=2, ensure_ascii=False))
        return 0 if st["ok"] else 1

    print(f"watching {_rel(pdir)}  [{which_dir}]")
    print(f"  orders   : {'; '.join(order_notes) or 'NONE FOUND'}")
    print(f"  declared : {len(declared)} id(s) in episode_spec.mandatory_stills; "
          f"{len(plates_on_disk(pdir))} png(s) on disk. The GATE's plate set is the union, "
          f"and it is check_plate_verdicts.py's definition, not this file's.")
    print(f"  verdicts : {_rel(cfg['vpath'])}  (schema: check_plate_verdicts.py)")
    print(f"  packets  : {_rel(cfg['packets'])}")
    print("  the mechanical pass CANNOT judge content. A green line here is not an approval.")

    rec, err = _load_json(cfg["rpath"])
    if err:
        raise SystemExit(err)

    n = 0
    try:
        while True:
            n += 1
            t0 = time.time()
            r = do_pass(cfg, rec, first=(n == 1))
            stamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{stamp}] pass {n:<4} seen {r['seen']:<5} measured +{r['newly']:<4} "
                  f"awaiting {r['awaiting']:<5} unresolved {r['unresolved']:<5} "
                  f"accepted {r['accepted']:<5} "
                  f"rejected {r['rejected']:<4} reset {len(r['cleared']):<3} "
                  f"unsettled {len(r['unsettled']):<3} ({time.time() - t0:.1f}s)")
            for c in r["cleared"]:
                print(f"           VERDICT CLEARED  {c}")
            for b in r["broke"]:
                print(f"           MACHINE REJECT  {b} does not decode")
            for b in r["batches"]:
                print(f"           review worklist -> {_rel(cfg['packets'] / (b + '.md'))}")
            if args.once or (args.max_passes and n >= args.max_passes):
                break
            time.sleep(max(1.0, args.interval))
    except KeyboardInterrupt:
        print("\nstopped.")

    st = plate_state(slug, spec, pdir, cfg["vpath"])
    print()
    print(f"gate state (check_plate_verdicts.plate_state): "
          f"{'OK' if st['ok'] else 'BLOCKED'} -- {st['reason'][:400]}")
    return 0 if st["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
