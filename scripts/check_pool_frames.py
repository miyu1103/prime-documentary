#!/usr/bin/env python
"""Look at every staged clip ACROSS ITS OWN LENGTH, before the build -- not once at t=1s.

WHY THIS FILE EXISTS (EP62 greene, 2026-08-10/11)
-------------------------------------------------
greene was staged, QC'd, built, rendered, muxed and graded. Pre-flight was green, the
60-second probe was green, the post-render gate was green, forty acceptance checks were
green, and the pool's own visual QC was green. Then somebody read the 78 SHIPPED-FRAME
contact sheets -- 1,556 frames, every tile with a person, document, vehicle or text
reopened and magnified -- and found two clips that cannot ship in a film about 1975
Louisville:

  * AR-8847832, filed `person_holding_papers`: a MODERN US ELECTION BALLOT reading
    "United States President and Vice President / VOTE FOR ONE". Used twice; the second
    use sits under the narration "the only evidence anybody brought".
  * AR-28450296, filed `playground`: a modern European park with a Range Rover Evoque
    (2011+) on an EU plate. Used twice; the first inside the opening minute.

Both are in config/footage_blocklist.v001.json now. That is the symptom.

THE STRUCTURAL FAULT is that the only review able to find those runs AFTER the render.
`check_shipped_frames.py` samples four points per cut out of the finished master; the
pool-stage review (`build_footage_contact_sheet.py`, whose `load_frame` hard-codes
`ffmpeg -ss 1`) shows ONE frame at t=1s per clip. So a defect that costs a four-hour
re-render was only discoverable once the four hours had been spent.

WHAT ACTUALLY WENT WRONG, MEASURED RATHER THAN ASSUMED (2026-08-11)
--------------------------------------------------------------------
The first version of this file said the pool sheet missed the ballot because the ballot
appears at 0:04 and the sheet looks at 1s. THAT IS NOT TRUE, and it was worth an hour to
find out. Both clips were pulled out of greene/factory_pruned_offtopic and re-measured:

  * AR-8847832 is 27.4s long. The ballots are on the table AT t=1.0s, legible in the 960px
    frame -- "United States President and Vice President / VOTE FOR ONE". The t=1s frame
    the old sheet took CONTAINED THE DEFECT.
  * AR-28450296 is 5.1s long. Modern cars are parked behind the swings in every single
    sampled frame, including the first.

So the sampling point was never the reason either one survived. Three other things were:

  1. TILE RESOLUTION. `build_sheet` draws a 360px-wide tile. A sheet of 8pt ballot text and
     a car eighty feet behind a tree are both unresolvable at that size. THE SHEET IS AN
     INDEX, NOT THE EVIDENCE. The evidence is the 960px jpg per sample under frames/, and a
     review that never opens one has not looked. This file prints that path every run.
  2. THE VERDICT WAS RECORDED PER SHEET, NOT PER CLIP. `reviewed_sheets` means "somebody
     opened sheet 03", and that cleared twenty clips at once. Nobody ever had to say
     anything about AR-8847832 specifically.
  3. NOTHING BOUND THE REVIEW TO THE POOL. Clips restaged after a review inherited it.

Sampling across the clip is still worth doing -- it is what catches the EP61 motorbike at
56% of its cut and the EP62 i2v inventions in the last 1-3 seconds, and it gives a reviewer
several framings of the same clip instead of one. But it is the SMALLEST of the four fixes
here, and this file would be lying if it claimed otherwise. The per-clip verdict and the
pool binding are the load-bearing ones.

This moves the whole review to the pool, where acting on it costs nothing.

WHY A NEW FILE AND NOT AN EXTENSION (CLAUDE.md invariant 14)
-------------------------------------------------------------
Three existing tools were read first and none can carry this:

  * `build_footage_contact_sheet.py` tiles, but its unit is ONE frame per file and its
    seek is the constant that caused the defect. Its `build_sheet()` IS the tiler used
    below -- imported, not copied.
  * `check_shipped_frames.py` has exactly the right sampling shape, but its unit is a CUT
    IN A FILM TIMELINE: it selects a delivered master, walks `film.json`, and binds its
    verdict to `render_sha256`. At pool stage there is no film and no master. Its
    `extract()`, `measure()` and `_rel()` are imported here, and the sheet/verdict/receipt
    shape below is deliberately the same one so the two reviews read alike.
  * `check_pool_faces.py` already samples 8 frames per pool clip -- but it feeds a
    haarcascade, produces no sheets and records no verdict. It answers "is there a face",
    not "what is in this clip".

WHAT IS SAMPLED
---------------
Per clip: n = clamp(MIN_SAMPLES, ceil(duration / SECONDS_PER_SAMPLE), MAX_SAMPLES) frames
at (i+0.5)/n of the clip's OWN probed duration. SECONDS_PER_SAMPLE is 4.0 because a cut in
this channel's films is 3.1-4.6s (`target_cut_sec`), so one sample per 4s of source means
no window the length of a cut goes entirely unseen. A 6-second clip gets 6 frames, a
30-second clip gets 8, a 10-minute clip gets 12 (and 12 frames of a 10-minute clip is
thin -- the receipt says so per clip, in `seconds_per_sample`).

WHAT IS RECORDED
----------------
`runs/qc/<slug>_pool_frames.v001.json` -- the receipt this tool writes: every clip, every
sampled timecode, which sheet each tile is on, the mechanical flags, the pool's id hash,
and the verdict.

`runs/qc/<slug>_clip_verdicts.v001.json` -- the file the REVIEWER writes, which already
exists and which `write_factory_clip_qc.py`, `apply_clip_verdicts.py` and
`check_episode_inputs.py` already read. This adds one key to it rather than inventing a
second verdict file:

    {"rejected": {"<clip>.mp4": "why", ...},            <- unchanged, existing contract
     "pool_frame_review": {
        "reviewer": "...",
        "reviewed_at": "2026-08-11",
        "pool_id_sha256": "<the hash this script prints>",
        "reviewed_clips": ["<clip>.mp4", ...],
        "accepted":       ["<clip>.mp4", ...]}}

A clip's verdict is `reject` when it is in `rejected`, `accept` when it is in
`pool_frame_review.accepted`, and MISSING otherwise. Missing is a build-blocking failure.

HOW THE BINDING WORKS, AND WHY IT IS NOT JUST AN EQUALITY TEST
---------------------------------------------------------------
`pool_id_sha256` is sha256 of the sorted clip filenames joined by newlines -- the pool's
equivalent of the acceptance receipt's `video_sha256`. Three outcomes:

  exact   the hash matches the pool on disk. Bound.
  subset  it does not match, but every clip now in the pool is named in `reviewed_clips`.
          This is the NORMAL state after `apply_clip_verdicts.py` moves the rejects out:
          clips were REMOVED, and every clip that remains was still looked at. Allowed,
          and reported as a subset so nobody reads it as an exact binding.
  FAIL    a clip is in the pool that is not in `reviewed_clips`. A clip added after the
          review invalidates the review, because nobody has seen it. A reviewed-then-
          restaged pool is exactly how the greene defect comes back.

THE ERA/SETTING PROMPT IS A PROMPT. IT IS NOT A DETECTOR.
----------------------------------------------------------
`episode_spec.v001.json` may declare `era_setting` (place, country, years). When it does,
this file matches the clip's filename and its ledger title against a table of things that
date or place a shot -- modern vehicles, mobile phones, computer screens, non-matching
countries, legible signage and legible political text -- and PRINTS THEM FOR A HUMAN TO
OPEN. It is not evidence and it is not a pass:

  * On the actual greene ballot clip, `AR-8847832__person_holding_papers`, the table fires
    only `legible_text` (on the word "papers"). Nothing in it says "ballot". It would have
    put the clip on the triage list; it would NOT have said what was wrong.
  * On the actual greene Evoque clip, `AR-28450296__playground`, THE TABLE FIRES NOTHING
    AT ALL. A filename is not evidence of content -- that is the whole lesson of this file,
    and of the shelf, where `empty_parking_garage.mp4` is an icicle.

So: a clip with no prompt is not a clean clip. The sheets are the check.

    py -3.11 scripts/check_pool_frames.py --slug openfields
    py -3.11 scripts/check_pool_frames.py --slug openfields --sheets-only
    py -3.11 scripts/check_pool_frames.py --slug openfields --state        # no ffmpeg
    py -3.11 scripts/check_pool_frames.py --pool-dir <dir> --verdicts <json> --slug demo

Exit 0 only when every clip in the pool carries a verdict bound to THIS pool. Exit 1
otherwise. Read-only apart from runs/qc/. No network, no GPU, no render.

`preflight_render_gate.py` and `check_episode_inputs.py` call `evaluate(epdir)` /
`pool_state(...)` below; those are cheap and never run ffmpeg.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pd_footage_blocklist                                        # noqa: E402  (the ONE reader)
from build_footage_contact_sheet import COLS, ROWS, build_sheet   # noqa: E402
from check_episode_spec import load_and_validate                   # noqa: E402
from check_shipped_frames import _rel, extract, measure            # noqa: E402
from check_spec_satisfied import _hits, _words                     # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "runs" / "qc"
TILES_PER_SHEET = COLS * ROWS          # 20, whatever build_footage_contact_sheet tiles

VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv")

# One sample per this many seconds of source. A cut in this channel's films is 3.1-4.6s
# (episode_spec target_cut_sec), so at 4.0 no window the length of a cut is entirely unseen.
SECONDS_PER_SAMPLE = 4.0
MIN_SAMPLES = 6                        # even a 3-second clip gets six looks; frames are cheap
MAX_SAMPLES = 12                       # a 10-minute archive reel would otherwise produce 150

NEAR_BLACK_MEAN = 12.0                 # same numbers check_shipped_frames uses on the master
BLOWN_OUT_MEAN = 240.0
BLOWN_OUT_FRAC = 0.70

REVIEW_KEY = "pool_frame_review"


# --------------------------------------------------------------------------------------
# the era/setting prompt table.  READ THE DOCSTRING BEFORE TRUSTING ANY OF THIS.
# (category, plausible_from, keywords)
#   plausible_from = the earliest year the thing could honestly appear. The prompt fires
#                    when the episode's era ENDS before that year.
#   None           = the shot dates itself whatever the year, so it always prompts when an
#                    era is declared at all (a street scene contains whatever cars were on
#                    the road; a document on screen is legible and therefore datable).
# --------------------------------------------------------------------------------------
ERA_PROMPTS: tuple[tuple[str, int | None, tuple[str, ...]], ...] = (
    ("modern_vehicle", 1985, (
        "suv", "crossover", "minivan", "evoque", "range rover", "tesla", "prius",
        "hybrid car", "electric car", "electric vehicle", "ev charging", "charging station",
        "modern car", "sports car", "hatchback", "motorhome", "rv")),
    ("vehicles_date_the_shot", None, (
        "traffic", "highway", "motorway", "freeway", "interstate", "road", "roads",
        "street", "car", "cars", "driving", "drive", "parking", "car park", "intersection",
        "crosswalk", "roundabout", "bus", "truck", "van", "motorcycle", "scooter",
        "bicycle", "bike", "commute", "commuter")),
    ("mobile_phone", 1990, (
        "phone", "smartphone", "iphone", "android", "cell phone", "cellphone",
        "mobile phone", "texting", "text message", "selfie", "tablet", "touchscreen",
        "earbuds", "smartwatch", "qr code", "scanning phone")),
    ("computer_screen", 1980, (
        "computer", "laptop", "monitor", "keyboard", "coding", "code", "software",
        "website", "internet", "online", "email", "server", "data center", "hologram",
        "lcd", "led screen", "digital display", "spreadsheet", "cursor", "database",
        "typing on keyboard", "video call", "webcam")),
    ("political_text", None, (
        "ballot", "ballots", "vote", "votes", "voting", "voter", "election", "elections",
        "president", "presidential", "campaign", "poll", "polls", "polling", "referendum",
        "candidate", "senate", "congress", "parliament", "protest", "placard", "rally",
        "petition")),
    ("legible_text", None, (
        "sign", "signs", "signage", "billboard", "poster", "banner", "newspaper",
        "magazine", "document", "documents", "paper", "papers", "letter", "letters",
        "book", "books", "form", "forms", "certificate", "contract", "notice", "label",
        "menu", "receipt", "licence", "license", "number plate", "headline", "printed",
        "writing", "handwriting", "text", "map", "chart", "screen")),
)

# Place markers. These fire only when the spec declares a country/place and the marker is
# NOT part of that declaration -- EP67 is Dublin, CALIFORNIA, and "dublin" must not fire on
# its own episode.
PLACE_PROMPTS: tuple[str, ...] = (
    "europe", "european", "eu", "euro", "uk", "britain", "british", "england", "london",
    "scotland", "wales", "ireland", "dublin", "france", "french", "paris", "germany",
    "german", "berlin", "munich", "italy", "italian", "rome", "milan", "spain", "spanish",
    "madrid", "barcelona", "portugal", "lisbon", "netherlands", "amsterdam", "belgium",
    "brussels", "poland", "warsaw", "prague", "czech", "austria", "vienna", "hungary",
    "budapest", "sweden", "stockholm", "norway", "oslo", "denmark", "copenhagen",
    "finland", "helsinki", "greece", "athens", "turkey", "istanbul", "russia", "moscow",
    "ukraine", "kyiv", "china", "chinese", "beijing", "shanghai", "shenzhen", "japan",
    "japanese", "tokyo", "korea", "seoul", "india", "indian", "delhi", "mumbai",
    "thailand", "bangkok", "vietnam", "indonesia", "jakarta", "philippines", "australia",
    "sydney", "melbourne", "new zealand", "canada", "toronto", "vancouver", "montreal",
    "mexico", "brazil", "argentina", "chile", "colombia", "africa", "nigeria", "kenya",
    "egypt", "cairo", "morocco", "dubai", "uae", "qatar", "saudi", "israel", "tel aviv",
)


# --------------------------------------------------------------------------------------
# pool enumeration + binding
# --------------------------------------------------------------------------------------
def pool_clips(pool: Path) -> list[Path]:
    """Every video physically staged in the pool. The DIRECTORY is the ground truth.

    Not film.json (stale by design at this stage), not the staging receipt (a record of an
    intent), not the ledger. `check_visual_asset_qc.py` settled this after EP36 and this
    follows it.
    """
    if not pool.is_dir():
        return []
    return sorted(p for p in pool.iterdir()
                  if p.is_file() and p.suffix.lower() in VIDEO_EXT)


def pool_id_hash(names: list[str]) -> str:
    """sha256 over the sorted clip filenames -- the pool's `video_sha256`.

    Deliberately over NAMES, not bytes: hashing 338 video files costs minutes and would be
    re-paid on every gate run, and the failure being guarded against is "a clip was added
    or swapped after the review", which the name list already answers. A clip whose BYTES
    change under a stable name is caught separately, by the per-clip (size, mtime) cache
    below, which re-extracts its frames.
    """
    return hashlib.sha256("\n".join(sorted(names)).encode("utf-8")).hexdigest()


def load_verdicts(path: Path) -> tuple[dict, str]:
    if not path.is_file():
        return {}, f"no {_rel(path)}"
    try:
        return json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:  # noqa: BLE001
        return {}, f"{_rel(path)} is unreadable ({exc})"


def pool_state(pool: Path, verdicts_path: Path, spec: dict | None = None) -> dict:
    """Is every clip in this pool covered by a verdict bound to THIS pool? Cheap, no ffmpeg.

    This is the gate. `check_episode_inputs.py` calls it directly and
    `preflight_render_gate.py` reaches it through `evaluate()`. It reads a directory listing
    and one json; it never decodes video, so it is safe to run in a pre-flight.

    Returns {ok, skipped, reason, problems, ...counts}. `ok` is False for every state that
    must stop a build; `skipped` is True only when there is genuinely nothing to judge.
    """
    clips = pool_clips(pool)
    names = [p.name for p in clips]
    out: dict = {
        "check": "pool_frame_review",
        "pool": _rel(pool),
        "pool_clips": len(names),
        "pool_id_sha256": pool_id_hash(names) if names else "",
        "verdicts_file": _rel(verdicts_path),
        "problems": [],
        "skipped": False,
        "ok": True,
        "reason": "",
    }
    if not names:
        out["skipped"] = True
        out["reason"] = f"no clips staged in {_rel(pool)} -- nothing to review yet"
        return out

    # THE BLOCKLIST, READ AT THE POOL (added 2026-08-11).
    # config/footage_blocklist.v001.json is consulted when CANDIDATES are filtered
    # (prestage_footage_review.filter_blocklist) and again when the film is emitted
    # (build_case_film_generic, which refuses on a blocked cut). Between those two moments sits
    # the staged pool, and nothing looked at it: a clip withdrawn AFTER staging simply stayed on
    # disk. Measured on 2026-08-11, four clips withdrawn hours earlier were still physically in
    # remotion/public/correa/factory, in the directory the next rebuild draws from.
    #
    # It runs BEFORE every early return in this function, including the
    # footage_review_required=false one. A rights hazard is not waived by an episode deciding it
    # does not need a frame review; that decision is about whether somebody looks, and this is
    # about a clip somebody already looked at and withdrew.
    #
    # Same reader as the other three tools, so the four can never disagree about a match
    # (CLAUDE.md invariant 14). This is a directory listing against a json -- no video is read.
    slug_for_block = pool.parent.name if pool.parent.name else ""
    blocked_rows = pd_footage_blocklist.load_blocked(slug_for_block or None)
    on_list = sorted((n, pd_footage_blocklist.reason_for(n, blocked_rows)) for n in names
                     if pd_footage_blocklist.reason_for(n, blocked_rows))
    out["blocklisted_still_staged"] = len(on_list)
    if on_list:
        out["ok"] = False
        out["problems"].append(
            f"{len(on_list)} clip(s) in {_rel(pool)} are on config/footage_blocklist.v001.json "
            f"and must not be in the pool the builder draws from: "
            + "; ".join(f"{n} ({why})" for n, why in on_list[:4])
            + (f" ... (+{len(on_list) - 4})" if len(on_list) > 4 else "")
            + ". Run `py -3.11 scripts/prune_pool_by_blocklist.py --slug "
              f"{slug_for_block or '<slug>'}`. Withdrawing a clip on the list and leaving the "
              "file on disk is not withdrawing it.")

    # The episode's own contract decides whether this applies. Every episode from EP54 on
    # declares true; an episode that declares false has made a recorded decision, and this
    # is not the place to override it. It is printed either way.
    if spec is not None and spec.get("footage_review_required") is False and not on_list:
        out["skipped"] = True
        out["reason"] = (f"{len(names)} clip(s) staged, but this episode declares "
                         f"footage_review_required=false -- NOT REVIEWED, by its own spec. "
                         f"None of them is on the footage blocklist, which is checked either "
                         f"way.")
        return out

    data, read_err = load_verdicts(verdicts_path)
    if read_err and not data:
        out["ok"] = False
        out["problems"].append(
            f"{read_err}: {len(names)} clip(s) are staged and NOT ONE carries a pool-frame "
            f"verdict. Run `py -3.11 scripts/check_pool_frames.py --slug <slug>`, read the "
            f"sheets, then record {REVIEW_KEY} in {_rel(verdicts_path)}.")
        out["reason"] = " | ".join(out["problems"])
        return out

    rejected = dict(data.get("rejected") or {})
    review = data.get(REVIEW_KEY) or {}
    accepted = {str(x) for x in (review.get("accepted") or [])}
    reviewed = {str(x) for x in (review.get("reviewed_clips") or [])} or (accepted | set(rejected))
    declared_hash = str(review.get("pool_id_sha256") or "")

    out["reviewer"] = review.get("reviewer")
    out["reviewed_at"] = review.get("reviewed_at")
    out["declared_pool_id_sha256"] = declared_hash
    out["accepted"] = len(accepted & set(names))
    out["rejected_named"] = len(rejected)

    if not review:
        out["ok"] = False
        n_sheet = len(data.get("reviewed_sheets") or [])
        out["problems"].append(
            f"{len(names)} clip(s) are staged and {_rel(verdicts_path)} carries no "
            f"'{REVIEW_KEY}' block, so no clip has been looked at ACROSS ITS OWN LENGTH"
            + (f" (it does record {n_sheet} reviewed contact sheet(s), but a sheet tick "
               f"clears 20 clips at once -- that is how EP62 greene cleared the clip that put "
               f"a modern US election ballot into a 1975 film)" if n_sheet else "")
            + f". Run `py -3.11 scripts/check_pool_frames.py --slug <slug>`.")
        out["reason"] = " | ".join(out["problems"])
        return out

    # --- binding ------------------------------------------------------------------------
    added = sorted(set(names) - reviewed)
    if declared_hash and declared_hash == out["pool_id_sha256"]:
        out["binding"] = "exact"
    elif not added:
        removed = len(reviewed - set(names))
        out["binding"] = "subset"
        out["binding_note"] = (
            f"the review names pool_id_sha256={declared_hash[:16] or '(none)'} and the pool "
            f"now hashes to {out['pool_id_sha256'][:16]}; {removed} clip(s) have been REMOVED "
            f"since and none added, so every clip still staged was seen. Not an exact binding.")
    else:
        out["binding"] = "broken"
        out["ok"] = False
        out["problems"].append(
            f"{len(added)} clip(s) were STAGED AFTER the review and nobody has seen them: "
            + ", ".join(added[:5]) + (f" ... (+{len(added) - 5})" if len(added) > 5 else "")
            + f". The review is bound to pool_id_sha256={declared_hash[:16] or '(none)'}; this "
            f"pool hashes to {out['pool_id_sha256'][:16]}. Re-run check_pool_frames.py and "
            f"re-read the new clips' sheets -- a reviewed-then-restaged pool is exactly how "
            f"the EP62 ballot comes back.")

    # --- per-clip coverage ---------------------------------------------------------------
    no_verdict = [n for n in names if n not in accepted and n not in rejected]
    if no_verdict:
        out["ok"] = False
        out["problems"].append(
            f"{len(no_verdict)} of {len(names)} staged clip(s) carry no per-clip verdict "
            f"(neither accepted nor rejected): "
            + ", ".join(no_verdict[:5])
            + (f" ... (+{len(no_verdict) - 5})" if len(no_verdict) > 5 else ""))
    out["no_verdict"] = len(no_verdict)

    # A recorded rejection that is still on disk is a verdict that was never acted on --
    # `apply_clip_verdicts.py` exists precisely because recording is not applying. The build
    # draws from this directory.
    still_staged = sorted(n for n in names if n in rejected)
    if still_staged:
        out["ok"] = False
        out["problems"].append(
            f"{len(still_staged)} clip(s) REJECTED at review are still in {_rel(pool)}: "
            + ", ".join(still_staged[:5])
            + (f" ... (+{len(still_staged) - 5})" if len(still_staged) > 5 else "")
            + f". Run `py -3.11 scripts/apply_clip_verdicts.py --slug <slug>`.")
    out["rejected_still_staged"] = len(still_staged)

    if out["ok"]:
        out["reason"] = (
            f"{len(names)} staged clip(s), every one carrying a per-clip verdict read from "
            f"frames sampled across its own duration; binding={out['binding']}"
            + (f" ({out['binding_note']})" if out.get("binding_note") else "")
            + f". Reviewer: {review.get('reviewer') or 'unnamed'} "
              f"{review.get('reviewed_at') or ''}".rstrip()
            + ", and none of them is on the footage blocklist"
            + ". This says who looked, not that the pool is clean.")
    else:
        out["reason"] = " | ".join(out["problems"])
    return out


def evaluate(epdir: Path) -> dict:
    """The `preflight_render_gate._run_ext_gate` contract: {ok, hard, reason, skipped}.

    Never raises, never calls sys.exit, never runs ffmpeg -- a pre-flight must not decode
    338 videos, and a gate that crashes is a gate that gets removed.
    """
    epdir = Path(epdir)
    slug = epdir.name.split("-")[-1]
    spec, problems, _ = load_and_validate(slug)
    st = pool_state(ROOT / "remotion" / "public" / slug / "factory",
                    QC / f"{slug}_clip_verdicts.v001.json",
                    spec if not problems else None)
    return {"check": "pool_frame_review", "ok": bool(st["ok"]), "hard": True,
            "skipped": bool(st["skipped"]), "reason": st["reason"], "detail": st}


# --------------------------------------------------------------------------------------
# sampling
# --------------------------------------------------------------------------------------
def sample_times(duration: float) -> list[float]:
    """The timecodes to pull out of ONE clip. See the module docstring for the arithmetic."""
    if duration <= 0:
        return [0.0]
    n = max(MIN_SAMPLES, min(MAX_SAMPLES, int(math.ceil(duration / SECONDS_PER_SAMPLE))))
    return [round(duration * (i + 0.5) / n, 3) for i in range(n)]


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)], capture_output=True, text=True)
    try:
        return float((r.stdout or "0").strip())
    except ValueError:
        return 0.0


def clip_id(name: str) -> str:
    """`AR-8847832__person_holding_papers.mp4` -> `AR-8847832`. The id the reviewer cites."""
    stem = Path(name).stem
    return stem.split("__", 1)[0] if "__" in stem else stem[:28]


# --------------------------------------------------------------------------------------
# metadata: what the shelf CLAIMS this clip is
# --------------------------------------------------------------------------------------
def staging_rows(slug: str) -> dict[str, dict]:
    """clip filename -> the staging receipt's row (ledger title, source, licence).

    `stage_footage_by_title.py` selects on the archive ledger's human-written TITLE, so this
    is better evidence than the filename -- and it is what `write_factory_clip_qc.py`
    already treats as the clip's provenance.
    """
    p = QC / f"{slug}_title_staging.v001.json"
    if not p.is_file():
        return {}
    try:
        rows = json.loads(p.read_text(encoding="utf-8")).get("staged") or []
    except Exception:  # noqa: BLE001
        return {}
    return {str(r.get("staged_as")): r for r in rows if r.get("staged_as")}


def episode_stock_rows(slug: str) -> dict[str, dict]:
    """clip id -> the EPISODE's own stock ledger row (05_stock/stock_ledger.v001.json).

    THE THIRD PLACE A POOL CLIP CAN COME FROM, and until 2026-08-22 this tool knew about only
    two. `staging_rows()` covers what `stage_footage_by_title.py` pulled off the archive shelf,
    and `shelf_index()` covers the shelf itself. Neither covers footage HARVESTED FOR THIS
    EPISODE by `fetch_stock.py`, which writes its rights record to the episode's own
    `05_stock/stock_ledger.v001.json` -- source, licence, author, source_url, query, sha256.

    Measured on 2026-08-22: 99 of EP72's 159 pool clips and 113 of EP73's 150 came back
    "FILENAME ONLY -- no ledger row" (62 % and 75 %). Every one of them had a full rights record
    sitting in the episode ledger the whole time. EP75 reported the same symptom.

    A clip reported as unbacked when it is fully documented is worse than useless: it trains the
    reviewer to ignore the field, and the field is what a rights challenge would be answered
    with.
    """
    epdir = next((p for p in sorted((ROOT / "episodes").glob(f"PD-*-{slug}"))), None)
    if epdir is None:
        return {}
    p = epdir / "05_stock" / "stock_ledger.v001.json"
    if not p.is_file():
        return {}
    try:
        assets = json.loads(p.read_text(encoding="utf-8")).get("assets") or []
    except Exception:  # noqa: BLE001
        return {}
    out: dict[str, dict] = {}
    for a in assets:
        aid = str(a.get("asset_id") or "")
        if not aid:
            continue
        row = {
            "title": a.get("depicts") or a.get("query") or "",
            "source": a.get("source"),
            "license": a.get("license"),
            "author": a.get("author"),
            "source_url": a.get("source_url"),
            "sha256": a.get("sha256"),
        }
        # the merge step names these AR-<asset_id>__<title-slug>.mp4, so key on both forms
        out[aid.lower()] = row
        out[f"ar-{aid}".lower()] = row
    return out


def shelf_index(ids: set[str]) -> dict[str, dict]:
    """Ledger records for clip ids the staging receipt did not cover.

    Uses `shelf.shelf_rows()` -- the ONE definition of what the shelf holds -- with
    include_factory left at its default True. Three tools in this repo pass
    include_factory=False and thereby hide the 88,740-item factory shelf, which is 58% of
    stock; a pool clip drawn from it would then resolve to no metadata at all and be
    reported as unbacked when it is not.

    Only called when something is actually unresolved, because it streams ~300 MB of jsonl.
    """
    if not ids:
        return {}
    try:
        from shelf import shelf_rows
    except Exception:  # noqa: BLE001
        return {}
    want = {i.lower() for i in ids}
    out: dict[str, dict] = {}
    try:
        for rec in shelf_rows():
            rid = str(rec.get("id") or "").lower()
            mid = str(rec.get("manifest_id") or "").lower()
            for key in (rid, mid):
                if key and key in want and key not in out:
                    out[key] = rec
            if len(out) == len(want):
                break
    except Exception:  # noqa: BLE001
        pass
    return out


# --------------------------------------------------------------------------------------
# the era/setting prompt
# --------------------------------------------------------------------------------------
def era_of(spec: dict | None) -> dict | None:
    era = (spec or {}).get("era_setting")
    return era if isinstance(era, dict) else None


def era_prompts(haystack: str, era: dict | None) -> list[str]:
    """Words in this clip's filename/title that a reviewer should go and LOOK at.

    NOT a detector. See the module docstring: on the real greene Evoque clip this returns
    an empty list, and an empty list means nothing.
    """
    if not era:
        return []
    years = era.get("years") or []
    end_year = int(years[1]) if len(years) >= 2 else None
    hits: list[str] = []
    for category, plausible_from, words in ERA_PROMPTS:
        if plausible_from is not None and (end_year is None or end_year >= plausible_from):
            continue
        found = [w for w in words if _hits(w, haystack)]
        if found:
            hits.append(f"{category}:{'/'.join(sorted(set(found))[:3])}")
    declared = _words(f"{era.get('place', '')} {era.get('country', '')}")
    foreign = [w for w in PLACE_PROMPTS if _hits(w, haystack) and not _hits(w, declared)]
    if foreign:
        hits.append(f"setting_mismatch:{'/'.join(sorted(set(foreign))[:3])}")
    return hits


# --------------------------------------------------------------------------------------
# WHAT MUST BE MAGNIFIED, whatever the era.  A tile is 360px wide and the EP62 ballot was
# legible only in the 960px frame, so a clip that can carry a person, a document, a
# vehicle, a screen or text has to be opened at full size and not judged off the sheet.
# This fires with NO era declared and for every era: it is not asking "is this in period",
# it is asking "could this frame contain something a thumbnail cannot resolve".
# Word lists are the ERA_PROMPTS ones, reused rather than restated, plus people.
# --------------------------------------------------------------------------------------
_ERA_WORDS: dict[str, tuple[str, ...]] = {cat: words for cat, _yr, words in ERA_PROMPTS}

PERSON_WORDS: tuple[str, ...] = (
    "man", "men", "woman", "women", "person", "people", "boy", "girl", "child", "children",
    "kid", "kids", "baby", "teen", "guy", "lady", "couple", "family", "crowd", "group",
    "face", "faces", "portrait", "hand", "hands", "worker", "workers", "farmer", "hiker",
    "walker", "walking", "standing", "sitting", "runner", "student", "officer", "police",
    "soldier", "doctor", "nurse", "driver", "passenger", "shopper", "silhouette",
)

LOOK_CLOSER: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("person", PERSON_WORDS),
    ("document_or_text", _ERA_WORDS["legible_text"] + _ERA_WORDS["political_text"]),
    ("vehicle", _ERA_WORDS["vehicles_date_the_shot"] + _ERA_WORDS["modern_vehicle"]),
    ("screen", _ERA_WORDS["computer_screen"] + _ERA_WORDS["mobile_phone"]),
)


def look_closer(haystack: str) -> list[str]:
    """Categories in this clip's name/title that CANNOT be judged from a 360px tile.

    Era-independent, unlike `era_prompts`: EP66 openfields runs to 2026, so every dated
    ERA_PROMPTS category is in period there and the era table stays silent on a clip full
    of number plates. The magnification question is a different question from the period
    question, and this is the one that decides whether a full-size frame gets opened.

    Still a prompt and still not a detector -- it reads words, and the EP62 Evoque clip is
    called `playground`. `faces_in_frames` below is the only part of this file that looks
    at pixels.
    """
    return [cat for cat, words in LOOK_CLOSER if any(_hits(w, haystack) for w in words)]


def faces_in_frames(frames: list[Path]) -> list[dict]:
    """Faces/upper bodies found IN THE PIXELS of frames already extracted. No extra ffmpeg.

    The detector is `check_pool_faces.faces_in` with its calibrated floor -- imported, not
    restated, because that floor was set against a known positive (the EP65 marmet subject,
    0.132% of frame) and a second copy of it would drift. What this adds is WHEN: the frames
    are spread across the clip's own duration, so the four EP64 memphis clips whose face only
    appears late are found at the point they appear rather than missed at t=1s.

    Returns [] when OpenCV is missing -- and the caller must say so, because "I could not
    look" is not "there is nothing there".
    """
    try:
        import cv2
        from check_pool_faces import MIN_FACE_SHARE, faces_in
    except Exception:  # noqa: BLE001
        return []
    hits: list[dict] = []
    for fp in frames:
        img = cv2.imread(str(fp))
        if img is None:
            continue
        fh, fw = img.shape[0], img.shape[1]
        for (kind, x, y, w, h) in faces_in(img):
            share = (w * h) / float(fw * fh)
            if share >= MIN_FACE_SHARE:
                hits.append({"frame": fp.name, "kind": kind, "face_share": round(share, 5)})
    return sorted(hits, key=lambda d: -d["face_share"])[:8]


# --------------------------------------------------------------------------------------
# extraction
# --------------------------------------------------------------------------------------
def cache_state(items) -> dict[str, str]:
    """{clip name: "size:mtime"} for the BYTES a review's frames were taken from.

    Accepts plain Paths (pool mode, where the name IS the file) or (name, source_path) pairs
    (candidate mode, where the clip is not in the pool yet and the name it will be staged
    under is not the name it carries on the shelf).
    """
    out: dict[str, str] = {}
    for it in items:
        name, p = (it.name, it) if isinstance(it, Path) else (str(it[0]), Path(it[1]))
        try:
            st = p.stat()
        except OSError:
            continue
        out[name] = f"{st.st_size}:{int(st.st_mtime)}"
    return out


def main() -> int:  # noqa: C901
    # --samples-min/--samples-max/--seconds-per-sample rebind these so a cheap first pass over
    # hundreds of candidates is possible; sample_times() reads them, and every receipt records
    # the values that were actually in force.
    global SECONDS_PER_SAMPLE, MIN_SAMPLES, MAX_SAMPLES
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pool-dir", help="override remotion/public/<slug>/factory")
    ap.add_argument("--verdicts", help="override runs/qc/<slug>_clip_verdicts.v001.json")
    ap.add_argument("--out-dir", help="frames and sheets (default runs/qc/pool_frames/<slug>)")
    ap.add_argument("--state", action="store_true",
                    help="report the gate state only -- extracts nothing, runs no ffmpeg. "
                         "This is exactly what the pre-flight sees.")
    ap.add_argument("--sheets-only", action="store_true",
                    help="extract and tile, then stop. Never passes, by design.")
    ap.add_argument("--force", action="store_true", help="re-extract frames already on disk")
    ap.add_argument("--jobs", type=int, default=4, help="parallel ffmpeg/ffprobe (default 4)")
    ap.add_argument("--limit", type=int, help="only the first N clips (fixtures/demos)")
    ap.add_argument("--candidates",
                    help="json {'candidates':[{'name': staged_as, 'src': archive path, "
                         "'title': ..., 'source': ..., 'license': ...}]} -- sample clips AT "
                         "THEIR ARCHIVE LOCATION, before anything is copied into the pool. "
                         "The pool is not read and not written; the caller "
                         "(prestage_footage_review.py) owns the accept/reject decision.")
    ap.add_argument("--seconds-per-sample", type=float, default=SECONDS_PER_SAMPLE,
                    help=f"one sample per this many seconds of source (default "
                         f"{SECONDS_PER_SAMPLE:g}; a cut in this channel is 3.1-4.6s)")
    ap.add_argument("--samples-min", type=int, default=MIN_SAMPLES,
                    help=f"floor on samples per clip (default {MIN_SAMPLES}). A cheaper first "
                         f"pass over hundreds of candidates can lower this; the receipt "
                         f"records what was actually taken, per clip.")
    ap.add_argument("--samples-max", type=int, default=MAX_SAMPLES,
                    help=f"ceiling on samples per clip (default {MAX_SAMPLES})")
    ap.add_argument("--faces", action="store_true",
                    help="run check_pool_faces' calibrated detector over the frames that were "
                         "extracted anyway (no extra ffmpeg). Pixel evidence, unlike every "
                         "other flag in this file, which reads words.")
    a = ap.parse_args()

    SECONDS_PER_SAMPLE, MIN_SAMPLES, MAX_SAMPLES = (
        a.seconds_per_sample, a.samples_min, a.samples_max)
    slug = a.slug

    pool = Path(a.pool_dir) if a.pool_dir else ROOT / "remotion" / "public" / slug / "factory"
    if not pool.is_absolute():
        pool = ROOT / pool
    verdicts_path = (Path(a.verdicts) if a.verdicts
                     else QC / f"{slug}_clip_verdicts.v001.json")
    if not verdicts_path.is_absolute():
        verdicts_path = ROOT / verdicts_path

    spec, spec_problems, _epdir = load_and_validate(slug)
    era = era_of(spec)

    st = pool_state(pool, verdicts_path, spec if not spec_problems else None)
    print(f"[pool-frames] {slug}: {st['pool_clips']} clip(s) in {st['pool']}")
    print(f"[pool-frames] pool_id_sha256={st['pool_id_sha256']}")
    if spec_problems:
        print(f"[pool-frames] NOTE: no usable episode spec ({spec_problems[0]}) -- no era/"
              f"setting prompt is possible, and footage_review_required is unknown")
    elif era:
        yrs = era.get("years") or []
        print(f"[pool-frames] era_setting: {era.get('place')} "
              f"({era.get('country') or '?'}) "
              f"{yrs[0] if yrs else '?'}-{yrs[1] if len(yrs) > 1 else '?'}")
    else:
        print(f"[pool-frames] !! this episode declares NO era_setting. The EP62 ballot and "
              f"the EP62 Evoque were forbidden by nothing because nobody had written down "
              f"that greene is 1975, Louisville, USA. Add era_setting to "
              f"episodes/PD-*-{slug}/episode_spec.v001.json.")

    if a.state:
        for p in st["problems"]:
            print(f"[pool-frames]   - {p}")
        print(f"[pool-frames] state: {'SKIP' if st['skipped'] else ('OK' if st['ok'] else 'BLOCK')}"
              f" -- {st['reason']}")
        return 0 if (st["ok"] or st["skipped"]) else 1

    # CANDIDATE MODE. The clips being judged are not in the pool and must not be: the whole
    # point is that the copy has not happened yet. `clips` becomes a list of NAME-ONLY Paths
    # (the name the clip would be staged under) and `_src` resolves each to where it really
    # lives on the shelf. Everything downstream -- probe, extract, sheet, receipt -- is the
    # same code the staged pool goes through.
    cand_rows: list[dict] = []
    src_of: dict[str, Path] = {}
    if a.candidates:
        cpath = Path(a.candidates)
        if not cpath.is_absolute():
            cpath = ROOT / cpath
        doc = json.loads(cpath.read_text(encoding="utf-8"))
        cand_rows = list(doc.get("candidates") if isinstance(doc, dict) else doc)
        src_of = {str(r["name"]): Path(str(r["src"])) for r in cand_rows}
        clips = [Path(str(r["name"])) for r in cand_rows]
        print(f"[pool-frames] CANDIDATE MODE: {len(clips)} clip(s) sampled AT THEIR ARCHIVE "
              f"LOCATION, before anything is copied into {_rel(pool)}. This run stages "
              f"nothing and writes no verdict; prestage_footage_review.py owns both.")
    else:
        clips = pool_clips(pool)
    if a.limit:
        clips = clips[:a.limit]
    if not clips:
        print(f"[pool-frames] {slug}: nothing to sample")
        return 0

    def _src(name: str) -> Path:
        return src_of.get(name) or (pool / name)

    cand_names = set(src_of)
    out_dir = (Path(a.out_dir) if a.out_dir
               else QC / ("prestage_frames" if a.candidates else "pool_frames") / slug)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    # A cached frame is only evidence about the bytes it came from. Keyed per clip on
    # (size, mtime) so a re-staged clip under the same name cannot inherit the old review's
    # pictures -- the pool-stage form of the render_sha256 cache marker in
    # check_shipped_frames.py, which exists because EP35 shipped a probe receipt taken from
    # a different render.
    marker = frames_dir / "_clips.json"
    prev = json.loads(marker.read_text(encoding="utf-8")) if marker.is_file() else {}
    now = cache_state([(c.name, _src(c.name)) for c in clips])
    changed = [n for n, v in now.items() if prev.get(n) and prev[n] != v]
    for n in changed:
        for f in frames_dir.glob(f"{clip_id(n)}__*.jpg"):
            f.unlink()
    if changed:
        print(f"[pool-frames] {len(changed)} clip(s) changed on disk since the last run -- "
              f"their cached frames were discarded")

    # ---- probe -------------------------------------------------------------------------
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        durations = list(ex.map(probe_duration, [_src(c.name) for c in clips]))

    staged = staging_rows(slug)
    # A candidate carries its own ledger row (title, source, licence) from the selector that
    # proposed it -- there is no staging receipt yet, because nothing has been staged.
    for r in cand_rows:
        staged.setdefault(str(r["name"]), r)
    unresolved = {clip_id(c.name) for c in clips if c.name not in staged}
    epstock = episode_stock_rows(slug)
    from_ep = {i for i in unresolved if i.lower() in epstock}
    shelf = shelf_index(unresolved - from_ep)
    if unresolved:
        print(f"[pool-frames] {len(unresolved)} clip(s) have no staging-receipt row; "
              f"{len(from_ep)} resolved from the episode's own 05_stock ledger, "
              f"{len(shelf)} from the shelf ledger, "
              f"{len(unresolved) - len(from_ep) - len(shelf)} have NO provenance beyond a filename")

    rows: list[dict] = []
    samples: list[dict] = []
    for c, dur in zip(clips, durations):
        cid = clip_id(c.name)
        row = staged.get(c.name) or epstock.get(cid.lower()) or shelf.get(cid.lower()) or {}
        title = str(row.get("title") or "")
        hay = _words(f"{c.name} {title}")
        prompts = era_prompts(hay, era)
        closer = look_closer(hay)
        times = sample_times(dur)
        rows.append({
            "clip": c.name, "clip_id": cid,
            "src": _rel(_src(c.name)),
            "duration_s": round(dur, 3),
            "samples": len(times),
            "seconds_per_sample": round(dur / len(times), 2) if times else None,
            "ledger_title": title or None,
            "source": row.get("source"),
            "license": row.get("license") or row.get("license_decision"),
            "provenance": ("candidate list (ledger row, not yet staged)" if c.name in cand_names
                           else "staging receipt" if c.name in staged
                           else "episode 05_stock ledger" if cid.lower() in epstock
                           else "shelf ledger" if cid.lower() in shelf
                           else "FILENAME ONLY -- no ledger row"),
            "era_prompts": prompts,
            "look_closer": closer,
        })
        for i, t in enumerate(times):
            samples.append({
                "clip": c.name, "clip_id": cid, "index": i,
                "t_clip_s": t, "duration_s": round(dur, 3),
                "ledger_title": title or None, "era_prompts": prompts,
                "look_closer": closer,
                "frame": str(frames_dir / f"{cid}__{i:02d}_t{t:08.2f}s.jpg"),
            })

    total_frames = len(samples)
    print(f"[pool-frames] sampling {total_frames} frame(s) from {len(clips)} clip(s): "
          f"n = clamp({MIN_SAMPLES}, ceil(duration/{SECONDS_PER_SAMPLE:g}s), {MAX_SAMPLES}) "
          f"at (i+0.5)/n of each clip's OWN duration "
          f"(the old pool sheet took one frame, at t=1s)")

    # ---- extract -----------------------------------------------------------------------
    def _one(s: dict) -> bool:
        fp = Path(s["frame"])
        if fp.is_file() and not a.force:
            return True
        # `is not None`, NOT truthiness: extract() returns the time it actually landed on
        # (check_shipped_frames, 2026-08-12), and a legitimate t=0.0 is falsy.
        return extract(_src(s["clip"]), s["t_clip_s"], fp) is not None

    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        got = list(ex.map(_one, samples))
    missing = 0
    for s, ok in zip(samples, got):
        if not ok:
            s["extract_failed"] = True
            missing += 1
        else:
            try:
                s.update(measure(Path(s["frame"])))
            except Exception as exc:  # noqa: BLE001
                s["extract_failed"] = True
                s["measure_error"] = str(exc)[:120]
                missing += 1
    marker.write_text(json.dumps(now, indent=0) + "\n", encoding="utf-8")
    if missing:
        print(f"[pool-frames] {missing} frame(s) could not be extracted -- those seconds of "
              f"those clips have NOT been seen")

    # ---- faces, IN THE PIXELS ----------------------------------------------------------
    # The only part of this file that is evidence rather than a reading order. Runs over the
    # frames already on disk, so it costs no ffmpeg. Because those frames are spread across
    # each clip's own duration it answers "a face appears at 0:19" -- the four EP64 memphis
    # clips whose only face arrives late in the clip, and the withdrawn AR-10159563 with a
    # real identifiable woman in it, are that shape.
    faces_by_clip: dict[str, list[dict]] = {}
    if a.faces:
        try:
            import cv2  # noqa: F401
        except Exception:  # noqa: BLE001
            print("[pool-frames] REFUSED --faces: OpenCV is not importable, so NO clip was "
                  "checked for people. 'I could not look' is not 'there is nothing there'.")
        else:
            by_clip: dict[str, list[Path]] = {}
            for s in samples:
                if not s.get("extract_failed"):
                    by_clip.setdefault(s["clip"], []).append(Path(s["frame"]))
            with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
                for name, hits in zip(by_clip, ex.map(faces_in_frames, by_clip.values())):
                    if hits:
                        faces_by_clip[name] = hits
            frames_with = {h["frame"] for hits in faces_by_clip.values() for h in hits}
            for s in samples:
                if Path(s["frame"]).name in frames_with:
                    s["face_detected"] = True
            for r in rows:
                if r["clip"] in faces_by_clip:
                    r["faces"] = faces_by_clip[r["clip"]]
            rate = len(faces_by_clip) / max(1, len(rows))
            print(f"[pool-frames] faces: the haarcascade fired on {len(faces_by_clip)} of "
                  f"{len(rows)} clip(s) ({rate:.0%}).")
            # Deliberately NOT folded into look_closer. Measured on the EP66 candidate set on
            # 2026-08-11: it fired on 17 of 17 clips, including `time_lapse_of_moving_clouds`
            # eight times, and on the known positive -- AR-10159563, the withdrawn clip with a
            # real identifiable woman -- it fires ONLY through the upper-body cascade, with no
            # frontal detection at all. So it cannot be filtered on and it cannot be ranked on:
            # at 100% it is not a reading order either. It stays because it costs no ffmpeg and
            # it does fire on the real case, and because a per-clip record of where a body-like
            # shape was found is worth having next to the frames. It is not a person detector.
            if rate > 0.5:
                print(f"[pool-frames] TREAT THAT AS NOISE, NOT AS A FINDING: at {rate:.0%} it "
                      f"discriminates nothing. It fires on tree canopy and cloud texture, and "
                      f"on the one clip in this archive KNOWN to carry a real identifiable "
                      f"person it fires only as `upper-body`. Read the frames.")

    # ---- mechanical flags (cheap, and not the point) -----------------------------------
    for s in samples:
        flags: list[str] = []
        if s.get("extract_failed"):
            flags.append("extract_failed")
        else:
            if s.get("mean_luma", 255) < NEAR_BLACK_MEAN:
                flags.append("near_black")
            if s.get("mean_luma", 0) > BLOWN_OUT_MEAN or s.get("frac_white", 0) > BLOWN_OUT_FRAC:
                flags.append("blown_out")
        if s.get("face_detected"):
            flags.append("face")
        flags.extend(s["era_prompts"])
        flags.extend(f"look:{c}" for c in s.get("look_closer") or [])
        s["flags"] = flags

    # ---- sheets ------------------------------------------------------------------------
    what_pool = "CANDIDATES, NOT YET STAGED" if a.candidates else "STAGED POOL"
    sheets: list[dict] = []
    tiles = [s for s in samples if not s.get("extract_failed")]
    for n in range(0, len(tiles), TILES_PER_SHEET):
        chunk = tiles[n:n + TILES_PER_SHEET]
        idx = n // TILES_PER_SHEET + 1
        out = out_dir / (f"{slug}_prestage_frames_{idx:02d}.png" if a.candidates
                         else f"{slug}_pool_frames_{idx:02d}.png")
        labels: dict[str, str] = {}
        paths: list[Path] = []
        for s in chunk:
            p = Path(s["frame"])
            paths.append(p)
            # `off_label` makes build_sheet draw the second line in warning colour.
            lead = "off_label " if s["flags"] else ""
            what = s["ledger_title"] or Path(s["clip"]).stem.split("__", 1)[-1].replace("_", " ")
            labels[str(p)] = (f"{lead}{s['t_clip_s']:.1f}/{s['duration_s']:.1f}s  {what}")
            s["sheet"] = _rel(out)
        build_sheet(paths, out,
                    f"{slug} — {what_pool}, sampled across each clip  (sheet {idx}, "
                    f"{chunk[0]['clip_id']}–{chunk[-1]['clip_id']})", labels)
        sheets.append({"sheet": _rel(out), "tiles": len(chunk),
                       "from_clip": chunk[0]["clip"], "to_clip": chunk[-1]["clip"]})
    print(f"[pool-frames] {len(sheets)} labelled contact sheet(s) in {_rel(out_dir)}")
    print(f"[pool-frames] THE SHEET IS AN INDEX, NOT THE EVIDENCE. A tile is 360px wide; the "
          f"ballot that shipped in EP62 is unreadable at that size and the parked cars behind "
          f"the EP62 playground are a smudge. The evidence is the {total_frames} full-size "
          f"frame(s) in {_rel(frames_dir)} -- open the tiles you are judging.")

    # ---- receipt -----------------------------------------------------------------------
    prompted = [r for r in rows if r["era_prompts"]]
    by_cat: dict[str, int] = {}
    for r in prompted:
        for h in r["era_prompts"]:
            by_cat[h.split(":")[0]] = by_cat.get(h.split(":")[0], 0) + 1
    look_counts: dict[str, int] = {}
    for r in rows:
        for cat in r.get("look_closer") or []:
            look_counts[cat] = look_counts.get(cat, 0) + 1

    receipt = {
        "schema_version": "pool_frames.v001",
        "mode": "candidates" if a.candidates else "pool",
        "slug": slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pool": _rel(pool),
        "pool_clips": len(clips),
        "pool_id_sha256": pool_id_hash([c.name for c in pool_clips(pool)]),
        "sampling": {
            "seconds_per_sample": SECONDS_PER_SAMPLE,
            "min_samples": MIN_SAMPLES,
            "max_samples": MAX_SAMPLES,
            "rule": "n = clamp(min, ceil(duration/seconds_per_sample), max); "
                    "t_i = duration*(i+0.5)/n",
            "frames": total_frames,
            "frames_failed": missing,
        },
        "era_setting": era,
        "era_prompt_is_not_a_detector": (
            "The era_prompts below match this clip's FILENAME and ledger TITLE against a "
            "word table. They are a reading order for a human, not a finding. On the real "
            "EP62 clip that put a modern US election ballot into a 1975 film "
            "(AR-8847832__person_holding_papers) this table fires only `legible_text` on the "
            "word `papers`; on the real EP62 clip that put a 2011 Range Rover Evoque on an EU "
            "plate into it (AR-28450296__playground) IT FIRES NOTHING AT ALL. A clip with no "
            "prompt has not been cleared by anything. THE SHEETS ARE THE CHECK."),
        "era_prompt_counts": by_cat,
        "look_closer_counts": look_counts,
        "look_closer_means_open_the_full_frame": (
            "A tile is 360px wide. Every clip whose look_closer is non-empty can be carrying "
            "a person, a document, a vehicle, a screen or legible text, none of which survive "
            "that size -- the EP62 ballot was legible at t=1.0s in the 960px frame and "
            "invisible in the tile. Open runs/qc/.../frames/<clip_id>__*.jpg for these. "
            "`person_pixels` is the only entry here that came from pixels; the rest are words."),
        "faces_detected_in_clips": sorted(faces_by_clip),
        "clips": rows,
        "samples": samples,
        "sheets": sheets,
        "gate_state": pool_state(pool, verdicts_path, spec if not spec_problems else None),
    }

    state = receipt["gate_state"]
    verdict = "PASS"
    reasons: list[str] = []
    if not sheets:
        verdict = "FAIL"
        reasons.append("no contact sheet was produced -- there is no evidence to read")
    if missing:
        verdict = "FAIL"
        reasons.append(f"{missing} sampled frame(s) could not be extracted -- "
                       f"that part of those clips has not been seen")
    if a.candidates:
        verdict = "CANDIDATES_SAMPLED" if verdict == "PASS" else verdict
        reasons.append(
            "--candidates: these clips were sampled where they live on the shelf and NOTHING "
            "was staged. This mode records no verdict and binds no pool -- it produces the "
            "evidence that the accept/reject decision is made on, and the caller writes that "
            "decision and copies only what it accepted.")
    elif a.sheets_only:
        verdict = "UNREVIEWED" if verdict == "PASS" else verdict
        reasons.append("--sheets-only: the evidence was produced and nothing was read. "
                       "This mode never passes, by design.")
    elif not state["ok"] and not state["skipped"]:
        verdict = "UNREVIEWED" if verdict == "PASS" else verdict
        reasons.extend(state["problems"])
    receipt["verdict"] = verdict
    receipt["verdict_reasons"] = reasons

    QC.mkdir(parents=True, exist_ok=True)
    receipt_path = QC / (f"{slug}_prestage_frames.v001.json" if a.candidates
                         else f"{slug}_pool_frames.v001.json")
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")

    flagged = sum(1 for s in samples if s.get("flags"))
    print(f"[pool-frames] mechanical + era prompts: {flagged} tile(s) marked across "
          f"{len(prompted)} clip(s) {by_cat or '{}'}")
    for r in prompted[:12]:
        print(f"    {r['clip'][:64]:64s} {','.join(r['era_prompts'])}")
    if len(prompted) > 12:
        print(f"    ... and {len(prompted) - 12} more (all of them are in {receipt_path.name})")
    print("[pool-frames] THE PROMPTS ABOVE ARE A READING ORDER, NOT A FINDING. A filename is "
          "not evidence of content: the EP62 Evoque clip is called `playground` and matches "
          "nothing in the table. A clip with no prompt has been cleared by NOBODY.")
    print(f"[pool-frames] receipt -> {_rel(receipt_path)}")

    magnify = [r for r in rows if r.get("look_closer")]
    if magnify:
        print(f"[pool-frames] OPEN THE FULL-SIZE FRAME for {len(magnify)} of {len(rows)} clip(s) "
              f"{look_counts} -- a person, a document, a vehicle, a screen or text cannot be "
              f"judged in a 360px tile:")
        for r in magnify[:15]:
            print(f"    {r['clip'][:58]:58s} {','.join(r['look_closer'])}"
                  + (f"  faces@{','.join(str(h['frame'].split('_t')[-1][:6]) for h in r.get('faces', [])[:3])}"
                     if r.get("faces") else ""))
        if len(magnify) > 15:
            print(f"    ... and {len(magnify) - 15} more (all of them are in "
                  f"{receipt_path.name} under clips[].look_closer)")
        print(f"    frames: {_rel(frames_dir)}/<clip_id>__*.jpg")

    if a.candidates:
        print(f"[pool-frames] {slug}: {len(clips)} CANDIDATE(S) SAMPLED AT SOURCE, "
              f"{total_frames} frame(s), nothing copied. No verdict was recorded here and no "
              f"pool was bound: this run produced the evidence, and prestage_footage_review.py "
              f"records the decision and stages only what was accepted.")
        return 0 if verdict == "CANDIDATES_SAMPLED" else 1
    if verdict == "PASS":
        print(f"[pool-frames] {slug}: PASS -- {len(clips)} clip(s), {total_frames} frame(s) "
              f"sampled, every clip carrying a per-clip verdict bound to this pool "
              f"({state.get('binding')}). That is a statement about who looked and at what; "
              f"it is not a statement that the pool is clean.")
        return 0
    print(f"[pool-frames] {slug}: NOT A PASS")
    for r in reasons:
        print(f"  - {r}")
    print(f"  Open the sheets in {_rel(out_dir)}, then add to {_rel(verdicts_path)}:")
    print(f'    "{REVIEW_KEY}": {{"reviewer": "...", "reviewed_at": '
          f'"{datetime.now().strftime("%Y-%m-%d")}", "pool_id_sha256": '
          f'"{receipt["pool_id_sha256"]}", "reviewed_clips": [...], "accepted": [...]}}')
    print(f"  and put anything you are rejecting under the existing top-level \"rejected\".")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
