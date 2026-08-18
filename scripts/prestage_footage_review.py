#!/usr/bin/env python
"""Judge candidate footage ON THE SHELF, and copy only what survives.

WHY THIS FILE EXISTS (owner, 2026-08-11)
-----------------------------------------
    「DL素材も使う前に君がちゃんとチェックすれば、組み立て後に騒がなくて済むんじゃない？」

The order of operations was backwards. Today `stage_episode_footage.py` copies every clip the
queries matched into `remotion/public/<slug>/factory`, somebody reviews the pool later, and
`apply_clip_verdicts.py` moves the rejects back out. Measured:

  * EP64 memphis staged 624 clips and accepted 145.
  * EP62 greene staged 242 and accepted 74.
  * EP66 openfields had 135 REJECTED clips still physically in its pool, because step three had
    never been run -- and the film builder draws from that directory.

Every one of those is the same fault: the copy happens before the judgement, so the pool is
dirty by default and stays dirty until somebody remembers to clean it. This inverts it. The
verdict happens first, at the clip's archive location, and only accepted clips are ever copied.
`apply_clip_verdicts.py` then has nothing to undo, and `check_pool_frames`'s pool binding is
satisfied the moment staging completes rather than after a second review round.

THE ORDER, CHEAPEST FIRST
--------------------------
The expensive look is only spent on survivors.

    0  select            stage_footage_by_title.py --emit-candidates   (ledger, no copy)
    1  junk words        the UNIVERSAL_JUNK table in stage_episode_footage.py
    2  blocklist         pd_footage_blocklist, on the CANDIDATE, not only on the pool
    3  shape             scan_video_shape, MEASURED ON THE FILE
    4  cross-episode     check_cross_episode_reuse, on the content hash, in process
    5  content look      check_pool_frames.py --candidates: 6-12 frames across each clip's own
                         duration, tiled, plus a pixel face pass
    6  decide            a human reads the frames and names what to reject
    7  stage             stage_footage_by_title.py --stage-from --accepted

Steps 1-4 are seconds for the whole list. Step 5 is the only expensive one and it never runs on
a clip that steps 1-4 already killed. Frames are cached BY CONTENT HASH under
`runs/qc/prestage_frames/_bycontent/`, so a clip that appears as a candidate for a second
episode is never sampled twice.

TWO BUGS THIS RESPECTS
-----------------------
  * `check_cross_episode_reuse.py --check <glob>` reported a clean "0 already used" that was a
    lie -- unexpanded the pattern is one missing file, and expanded past ~500 files the command
    line exceeds the OS limit and the script never runs. Fixed there (in-process globbing, a
    non-zero exit when anything went unchecked, and `--check-list`); this file does not use the
    command line at all, it imports `key_of` and hashes in process.
  * `AR-10159563`, the withdrawn clip carrying a real identifiable woman, RE-STAGED ITSELF
    within a day off a generic query, because the blocklist was only ever applied to a pool
    after the copy. Step 2 runs on candidates.

WHAT THE CONTENT LOOK IS FOR, AND WHAT IT IS NOT
-------------------------------------------------
All of these were found on real clips in the last day, and none of them is machine-detectable:

  * EP62 greene (1975 Louisville): a modern US election ballot filed as `person_holding_papers`;
    a Range Rover Evoque on an EU plate filed as `playground`; legible Breaking Bad shot-list
    cards filed as `small_pieces_of_paper_falling_on_the_floor`.
  * EP63 correa (1991 Puerto Rico): present-day Seoul, Lotte World Tower and Hangul signage,
    filed as `motoring_road_car_traffic_vehicle_driving_roadwa`.
  * EP64 memphis: four clips where a face only appears LATE in the clip; a dog-food advert; two
    clips recorded as "a pale rotary wall phone" that are a shocking-pink prop on gold glitter.

Two lessons shape step 5. A FILENAME IS NOT EVIDENCE OF CONTENT -- every one of those clips is
filed under a name that describes something else. And THE TILE IS AN INDEX, NOT THE EVIDENCE --
the EP62 ballot is legible at t=1.0s in the 960px frame and invisible in the 360px tile. So
anything whose name or title can carry a person, a document, a vehicle, a screen or text is
listed for magnification, the episode's `era_setting` prompts on period and place, and a
haarcascade pass runs over the frames that were extracted anyway.

THOSE PROMPTS ARE PROMPTS, NOT DETECTORS. They read words. On the real EP62 Evoque clip the era
table fires nothing at all. A candidate with no prompt has been cleared by nobody; the frames
are the check, and only the `person_pixels` flag comes from pixels.

    py -3.11 scripts/prestage_footage_review.py --slug openfields
    py -3.11 scripts/prestage_footage_review.py --slug openfields --decide rejects.json --stage
    py -3.11 scripts/prestage_footage_review.py --slug openfields --candidates <list> --dry-run

Exit 0 when the run reached its stated end (phase 1 always exits 1: nothing has been read yet).
No network, no GPU, no render. The only writes are runs/qc/ and, with --stage, the pool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pd_footage_blocklist                                          # noqa: E402
from check_cross_episode_reuse import INDEX as REUSE_INDEX           # noqa: E402
from check_cross_episode_reuse import key_of                         # noqa: E402
from check_pool_frames import REVIEW_KEY, era_prompts                # noqa: E402
from check_pool_frames import pool_id_hash, pool_state               # noqa: E402
from check_episode_spec import load_and_validate                     # noqa: E402
from check_shipped_frames import _rel                                # noqa: E402
from check_spec_satisfied import _words as spec_words                # noqa: E402
from stage_footage_by_title import assert_queries_clean, forbidden_hit  # noqa: E402
from stage_footage_by_title import forbidden_subjects_for            # noqa: E402
from stage_footage_by_title import match_keys, title_words           # noqa: E402
from scan_video_shape import OUT as SHAPE_SCAN                       # noqa: E402
from scan_video_shape import cropbox, probe, verdict as shape_verdict  # noqa: E402
from stage_episode_footage import QUERIES, UNIVERSAL_JUNK            # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
QC = ROOT / "runs" / "qc"
FRAME_CACHE = QC / "prestage_frames" / "_bycontent"


# --------------------------------------------------------------------------------------
# step 0: the candidate list
# --------------------------------------------------------------------------------------
def emit_candidates(slug: str, per_query: int, out: Path) -> list[dict]:
    """Ask the existing selector for the list it WOULD copy, without copying it.

    Same selector, same ledger, same exclusions -- `stage_footage_by_title.py` is the one
    definition of what this episode's queries match, and re-deriving it here would be a second
    implementation of the only part of staging that has any judgement in it (invariant 14).
    """
    spec = json.loads(QUERIES.read_text(encoding="utf-8"))["episodes"].get(slug)
    if not spec:
        raise SystemExit(f"[prestage] no query set for {slug} in {QUERIES.name}")
    # A QUERY SET THAT CONTRADICTS ITS OWN SPEC MUST NOT HARVEST. 19 of EP68's 465 queries
    # asked for `fire`, `smoke`, `crash`, `wreck`, `hourglass` -- all five of which the same
    # episode's episode_spec forbids -- and they harvested 106 banned clips. Checked at the
    # moment the config is read, not after 800 candidates exist.
    assert_queries_clean(list(spec["queries"]), forbidden_subjects_for(slug), slug)
    cmd = [sys.executable, str(ROOT / "scripts" / "stage_footage_by_title.py"),
           "--slug", slug, "--per-query", str(per_query),
           "--emit-candidates", str(out)]
    for q in spec["queries"]:
        cmd += ["--query", q]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in (r.stdout or "").splitlines():
        if line.startswith("[stage]") or line.startswith("  RIGHTS"):
            print(f"  {line}")
    if r.returncode != 0 or not out.is_file():
        raise SystemExit(f"[prestage] candidate selection failed: {(r.stderr or '')[:400]}")
    return list(json.loads(out.read_text(encoding="utf-8"))["candidates"])


# --------------------------------------------------------------------------------------
# steps 1-4: the mechanical filters.  Cheapest first; each one shrinks what step 5 pays for.
# --------------------------------------------------------------------------------------
def filter_junk(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    keep, drop = [], []
    for r in rows:
        m = UNIVERSAL_JUNK.search(r["name"])
        (drop if m else keep).append(r)
        if m:
            r["drop_reason"] = f"universal junk word {m.group(0)!r} -- foreign to every " \
                               f"episode in this catalogue"
            r["dropped_by"] = "junk_words"
    return keep, drop


def filter_blocklist(rows: list[dict], slug: str) -> tuple[list[dict], list[dict]]:
    """The blocklist, applied to CANDIDATES.

    `prune_pool_by_blocklist.py` only ever sees a pool, i.e. clips that have already been
    copied, and a blocked clip that is never staged is never pruned. AR-10159563 -- withdrawn
    because it carries a real identifiable woman -- came back within a day off a generic query
    for exactly that reason. Matching uses `pd_footage_blocklist.identifiers`, so both the name
    the clip would be staged under and the name it has on the shelf are tried.
    """
    blocked = pd_footage_blocklist.load_blocked(slug)
    keep, drop = [], []
    for r in rows:
        why = (pd_footage_blocklist.reason_for(r["name"], blocked)
               or pd_footage_blocklist.reason_for(Path(str(r["src"])).name, blocked)
               or pd_footage_blocklist.reason_for(str(r.get("id") or ""), blocked))
        if why:
            r["drop_reason"] = f"footage blocklist: {why}"
            r["dropped_by"] = "blocklist"
            drop.append(r)
        else:
            keep.append(r)
    return keep, drop


def filter_forbidden(rows: list[dict], forbidden: frozenset[str]
                     ) -> tuple[list[dict], list[dict]]:
    """The episode's own `forbidden_subjects`, applied to the CANDIDATE's title and name.

    `config/episode_footage_queries.v001.json` claimed, in EP68's own note, that the spec's
    124 forbidden terms "are applied to candidate titles before staging". Nothing applied
    them. This file ran four mechanical filters -- junk_words, blocklist, shape,
    cross_episode_reuse -- and none of them read `forbidden_subjects`; the spec was loaded
    only to print an era banner. 106 of pinto's 807 candidates carried a forbidden term as a
    whole word in their own ledger title (drone 26, burning 14, beach 11, smoke 10, fire 5,
    police 4) and all of them went to the 12 reviewers.

    `check_spec_satisfied.py` matches these word-wise against the STAGED filename, so any
    survivor is an automatic build failure after the render. Catching it here costs one set
    lookup, before the ffprobe and before a frame is decoded.

    Matching is `stage_footage_by_title.forbidden_hit` -- imported, not restated, so the
    selector and this filter can never drift apart (invariant 14).
    """
    if not forbidden:
        return rows, []
    keep, drop = [], []
    for r in rows:
        words = title_words(f"{r.get('title') or ''} {r.get('name') or ''}")
        hit = forbidden_hit(forbidden, words, match_keys(words))
        if hit:
            r["drop_reason"] = (f"episode_spec forbidden_subject {hit!r} in this clip's own "
                                f"title -- check_spec_satisfied would fail the build on it")
            r["dropped_by"] = "forbidden_subjects"
            drop.append(r)
        else:
            keep.append(r)
    return keep, drop


# A CANDIDATE THE PIPELINE HAS ALREADY CONVICTED DOES NOT GO ON A BALLOT.
DECISIVE_FLAGS = ("setting_mismatch:", "mobile_phone:")


def filter_decisive(rows: list[dict], era: dict | None) -> tuple[list[dict], list[dict]]:
    """Place and period contradictions the era table already found. Not every flagged tile.

    `setting_mismatch:*` says the clip's own title names a country the episode does not run
    in; `mobile_phone:*` says it names a device that did not exist in the episode's years.
    Unlike `look:*` -- which only ever meant "a 360px tile cannot settle this, open the full
    frame" -- these are a finding. 18 of EP68's 216 presented candidates carried one
    (Toronto, Vancouver, Bangkok, Tokyo, Kazan, Sicily, an Indian railway station, a broken
    iPhone, a smartphone close-up) and the 12 reviewers accepted 0 of the 18.

    DO NOT EXTEND THIS TO EVERY FLAGGED TILE. The `off_label` prefix `check_pool_frames`
    draws on a sheet fires on ANY flag, including the entirely benign `look:vehicle` (482
    samples on EP68) and `look:person` (382). 130 of the 216 carried that prefix, and cutting
    on it would have deleted the vehicle register a film about the Ford Pinto is made of.

    Runs BEFORE the content look, not after it. `era_prompts` reads only the clip's filename
    and ledger title -- it is a pure function of text that `check_pool_frames` happens to
    call after sampling -- so evaluating it here also saves the ffmpeg cost of sampling 18
    clips nobody was ever going to accept, and keeps them off the contact sheet entirely.

    These are PROMPTS READING WORDS, not detectors. A clip with no flag has been cleared by
    nobody; that is what the human review of the survivors is for.
    """
    if not era:
        return rows, []
    keep, drop = [], []
    for r in rows:
        hay = spec_words(f"{r.get('name') or ''} {r.get('title') or ''}")
        found = [f for f in era_prompts(hay, era) if f.startswith(DECISIVE_FLAGS)]
        if found:
            r["drop_reason"] = (f"the era table already found a place/period contradiction "
                                f"in this clip's own title: {', '.join(found)}")
            r["dropped_by"] = "decisive_contradiction"
            drop.append(r)
        else:
            keep.append(r)
    return keep, drop


def load_shape_cache() -> dict[str, dict]:
    """Previously measured dimensions, KEYED BY ABSOLUTE PATH.

    Not by clip id. `video_resolution.json` is keyed by id and the same id exists in more than
    one source, so it answers about a different file than the one being staged; two of the
    sub-HD clips that reached EP64 were cleared by it. This file is written by
    `scan_video_shape.py`, one record per path, and anything not in it is measured now.
    """
    out: dict[str, dict] = {}
    if SHAPE_SCAN.is_file():
        for line in SHAPE_SCAN.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if rec.get("path"):
                out[rec["path"]] = rec
    return out


def filter_shape(rows: list[dict], jobs: int, timeout: int = 30
                 ) -> tuple[list[dict], list[dict], int]:
    """Portrait, pillarboxed or sub-HD clips cannot be used in a 1920x1080 film.

    Measured on the file with `scan_video_shape`'s own probe/cropdetect/verdict, and new
    measurements are appended to its JSONL so the next episode does not pay for them again.
    """
    from concurrent.futures import ThreadPoolExecutor

    cache = load_shape_cache()
    todo = [r for r in rows if str(Path(str(r["src"])).resolve()) not in cache
            and str(r["src"]) not in cache]
    fresh: list[dict] = []

    def work(r: dict) -> dict:
        p = Path(str(r["src"]))
        rec = {"path": str(p), "name": p.name}
        rec.update(probe(p, timeout))
        if rec.get("width", 0) >= rec.get("height", 1) > 0:
            cb = cropbox(p, timeout * 2)
            if cb:
                rec["crop"] = list(cb)
        return rec

    if todo:
        with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
            for rec in ex.map(work, todo):
                cache[rec["path"]] = rec
                fresh.append(rec)
        SHAPE_SCAN.parent.mkdir(parents=True, exist_ok=True)
        with SHAPE_SCAN.open("a", encoding="utf-8") as fh:
            for rec in fresh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    keep, drop = [], []
    for r in rows:
        rec = cache.get(str(r["src"])) or cache.get(str(Path(str(r["src"])).resolve())) or {}
        v = shape_verdict(rec, 0.08) if rec else "unreadable"
        r["shape"] = {"verdict": v, "width": rec.get("width"), "height": rec.get("height")}
        if v == "ok":
            keep.append(r)
        else:
            r["drop_reason"] = (f"shape={v} ({rec.get('width')}x{rec.get('height')}) -- "
                                f"not usable in a 1920x1080 film")
            r["dropped_by"] = "shape"
            drop.append(r)
    return keep, drop, len(fresh)


def filter_reuse(rows: list[dict], slug: str, jobs: int) -> tuple[list[dict], list[dict]]:
    """Content already burned into another episode's film.

    In process, on `(size, sha1 of the first 256 KB)` -- the same key
    `check_cross_episode_reuse.py` indexes with, imported rather than restated. Nothing is
    passed on a command line, so the argument-limit failure that made that tool report a clean
    "0 already used" cannot happen here.
    """
    from concurrent.futures import ThreadPoolExecutor

    if not REUSE_INDEX.is_file():
        print(f"  [reuse] NO INDEX at {_rel(REUSE_INDEX)} -- nothing was checked for reuse. "
              f"Run `py -3.11 scripts/check_cross_episode_reuse.py --build` first.")
        return rows, []
    idx = json.loads(REUSE_INDEX.read_text(encoding="utf-8"))["index"]
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        keys = list(ex.map(key_of, [Path(str(r["src"])) for r in rows]))
    keep, drop = [], []
    for r, k in zip(rows, keys):
        row = idx.get(k or "")
        # the episode's own earlier staging is not "reuse" -- it is this pool
        eps = [e for e in (row or {}).get("episodes", []) if e != slug]
        if row and eps:
            r["drop_reason"] = (f"same content already staged in {', '.join(sorted(eps))} "
                                f"(as {row.get('example_name', '')[:48]})")
            r["dropped_by"] = "cross_episode_reuse"
            drop.append(r)
        else:
            r["content_key"] = k
            keep.append(r)
    return keep, drop


# --------------------------------------------------------------------------------------
# step 5: the content look.  check_pool_frames does the sampling; this warms and saves its
# frame cache so the same content is never decoded twice across episodes.
# --------------------------------------------------------------------------------------
def cache_dir_for(key: str) -> Path:
    return FRAME_CACHE / hashlib.sha1(key.encode("utf-8")).hexdigest()[:20]


def warm_frame_cache(rows: list[dict], frames_dir: Path) -> int:
    hits = 0
    frames_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        key = r.get("content_key")
        if not key:
            continue
        meta = cache_dir_for(key) / "meta.json"
        if not meta.is_file():
            continue
        cid = str(r["name"]).split("__", 1)[0]
        try:
            names = json.loads(meta.read_text(encoding="utf-8"))["frames"]
        except Exception:  # noqa: BLE001
            continue
        for fn in names:
            src = meta.parent / fn
            dst = frames_dir / f"{cid}__{fn}"
            if src.is_file() and not dst.is_file():
                shutil.copy2(src, dst)
        hits += 1
    return hits


def save_frame_cache(receipt: dict, rows: list[dict]) -> int:
    keys = {str(r["name"]): r.get("content_key") for r in rows}
    by_clip: dict[str, list[Path]] = {}
    for s in receipt.get("samples", []):
        if not s.get("extract_failed"):
            by_clip.setdefault(s["clip"], []).append(Path(s["frame"]))
    saved = 0
    for clip, frames in by_clip.items():
        key = keys.get(clip)
        if not key:
            continue
        d = cache_dir_for(key)
        if (d / "meta.json").is_file():
            continue
        d.mkdir(parents=True, exist_ok=True)
        cid = clip.split("__", 1)[0]
        names = []
        for fp in frames:
            short = fp.name[len(cid) + 2:] if fp.name.startswith(f"{cid}__") else fp.name
            if fp.is_file():
                shutil.copy2(fp, d / short)
                names.append(short)
        (d / "meta.json").write_text(
            json.dumps({"content_key": key, "frames": names,
                        "first_seen_as": clip}, indent=1), encoding="utf-8")
        saved += 1
    return saved


def content_look(slug: str, rows: list[dict], out_dir: Path, pool: Path, jobs: int,
                 samples_min: int, samples_max: int, faces: bool = True) -> dict:
    """Sample every survivor AT ITS ARCHIVE LOCATION, using the existing sampler."""
    # A DIFFERENT FILE from the emitted candidate list. Writing the survivors back over
    # `<slug>_prestage_candidates.v001.json` destroyed the record of what had been dropped, and
    # a second run then reported "0 dropped" off its own output.
    cand = QC / f"{slug}_prestage_survivors.v001.json"
    cand.parent.mkdir(parents=True, exist_ok=True)
    cand.write_text(json.dumps({"candidates": rows}, ensure_ascii=False, indent=1),
                    encoding="utf-8")
    warmed = warm_frame_cache(rows, out_dir / "frames")
    if warmed:
        print(f"  [frames] {warmed} candidate(s) already had frames cached by content hash "
              f"-- those clips are not decoded again")
    cmd = [sys.executable, str(ROOT / "scripts" / "check_pool_frames.py"),
           "--slug", slug, "--candidates", str(cand), "--out-dir", str(out_dir),
           "--pool-dir", str(pool),
           "--jobs", str(jobs),
           "--samples-min", str(samples_min), "--samples-max", str(samples_max)]
    if faces:
        cmd.append("--faces")
    r = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace")
    receipt_p = QC / f"{slug}_prestage_frames.v001.json"
    if r.returncode != 0 or not receipt_p.is_file():
        raise SystemExit(f"[prestage] the content look did not complete (exit {r.returncode})")
    receipt = json.loads(receipt_p.read_text(encoding="utf-8"))
    saved = save_frame_cache(receipt, rows)
    if saved:
        print(f"  [frames] cached {saved} clip(s) of frames by content hash under "
              f"{_rel(FRAME_CACHE)} -- a later episode gets them free")
    return receipt


# --------------------------------------------------------------------------------------
# step 6/7: record the decision, then stage the survivors
# --------------------------------------------------------------------------------------
def record_and_stage(slug: str, pool: Path, verdicts_path: Path, plan: dict,
                     decisions: dict, cand_file: Path, dry_run: bool) -> dict:
    presented = [c["clip"] for c in plan["presented"]]
    rejected_now = {str(k): str(v) for k, v in (decisions.get("reject") or {}).items()}
    unknown = sorted(set(rejected_now) - set(presented))
    if unknown:
        raise SystemExit(f"[prestage] {len(unknown)} rejected name(s) were never presented: "
                         + ", ".join(unknown[:5]))
    accepted = [c for c in presented if c not in rejected_now]

    if not dry_run:
        acc = QC / f"{slug}_prestage_accepted.v001.json"
        acc.write_text(json.dumps({"accepted": accepted}, indent=1), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "stage_footage_by_title.py"),
             "--slug", slug, "--stage-from", str(cand_file), "--accepted", str(acc),
             "--dest", str(pool)],
            text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise SystemExit("[prestage] staging failed; nothing was recorded")

    doc: dict = {}
    if verdicts_path.is_file():
        doc = json.loads(verdicts_path.read_text(encoding="utf-8"))
    doc.setdefault("slug", slug)

    # Content rejections join the existing `rejected` contract: they are visual QC verdicts and
    # every later stage already reads that key. Mechanical drops are a different kind of fact --
    # nobody looked at them -- so they are recorded separately and are not claimed as a review.
    rejected = dict(doc.get("rejected") or {})
    rejected.update({k: f"prestage content review: {v}" for k, v in rejected_now.items()})
    doc["rejected"] = rejected
    dropped = dict(doc.get("prestage_dropped") or {})
    for row in plan["dropped"]:
        dropped[row["name"]] = f"{row['dropped_by']}: {row['drop_reason']}"
    doc["prestage_dropped"] = dropped

    review = dict(doc.get(REVIEW_KEY) or {})
    reviewed = sorted(set(review.get("reviewed_clips") or []) | set(presented))
    acc_all = sorted((set(review.get("accepted") or []) | set(accepted)) - set(rejected))
    names = sorted(p.name for p in pool.glob("*.mp4")) if pool.is_dir() else []
    review.update({
        "reviewer": decisions.get("reviewer") or review.get("reviewer") or "unnamed",
        "reviewed_at": decisions.get("reviewed_at") or datetime.now().strftime("%Y-%m-%d"),
        "pool_id_sha256": pool_id_hash(names),
        "reviewed_clips": reviewed,
        "accepted": acc_all,
        "note": ("Recorded by prestage_footage_review.py: every clip named here was sampled "
                 "across its own duration WHILE STILL ON THE SHELF, and only the accepted ones "
                 "were then copied. The pool hash is taken after that copy, so the binding is "
                 "exact at the moment staging completes."),
    })
    doc[REVIEW_KEY] = review
    if not dry_run:
        verdicts_path.parent.mkdir(parents=True, exist_ok=True)
        verdicts_path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                 encoding="utf-8")
    return {"accepted": accepted, "rejected": rejected_now, "pool_clips": len(names)}


# --------------------------------------------------------------------------------------
def main() -> int:  # noqa: C901
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--per-query", type=int, default=6)
    ap.add_argument("--candidates", help="reuse a candidate list instead of re-selecting")
    ap.add_argument("--pool-dir", help="where accepted clips are staged "
                                       "(default remotion/public/<slug>/factory)")
    ap.add_argument("--verdicts", help="default runs/qc/<slug>_clip_verdicts.v001.json")
    ap.add_argument("--out-dir", help="frames and sheets "
                                      "(default runs/qc/prestage_frames/<slug>)")
    ap.add_argument("--decide", help="json {'reject': {'<clip>.mp4': 'why'}, 'reviewer': '...'} "
                                     "-- everything presented and not named here is accepted")
    ap.add_argument("--stage", action="store_true",
                    help="with --decide, copy the accepted clips into the pool")
    ap.add_argument("--samples-min", type=int, default=6)
    ap.add_argument("--samples-max", type=int, default=12)
    ap.add_argument("--no-faces", action="store_true",
                    help="skip the haarcascade pass. Measured 2026-08-11 on 17 EP66 "
                         "candidates: sampling costs 0.84s/clip and the face pass adds "
                         "1.5s/clip on top -- and it fired on 17 of 17, so it discriminated "
                         "nothing. Worth dropping on a large list.")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    slug = a.slug

    pool = Path(a.pool_dir) if a.pool_dir else ROOT / "remotion" / "public" / slug / "factory"
    if not pool.is_absolute():
        pool = ROOT / pool
    verdicts_path = (Path(a.verdicts) if a.verdicts
                     else QC / f"{slug}_clip_verdicts.v001.json")
    if not verdicts_path.is_absolute():
        verdicts_path = ROOT / verdicts_path
    out_dir = Path(a.out_dir) if a.out_dir else QC / "prestage_frames" / slug
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    plan_path = QC / f"{slug}_prestage.v001.json"
    cand_file = QC / f"{slug}_prestage_candidates.v001.json"

    spec, spec_problems, _ = load_and_validate(slug)
    era = (spec or {}).get("era_setting") if not spec_problems else None

    # ---------------- phase 2: a decision exists ----------------------------------------
    if a.decide:
        if not plan_path.is_file():
            raise SystemExit(f"[prestage] no plan at {_rel(plan_path)} -- run phase 1 first")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        decisions = json.loads(Path(a.decide).read_text(encoding="utf-8"))
        if not a.stage and not a.dry_run:
            raise SystemExit("[prestage] --decide needs --stage (or --dry-run): recording a "
                             "verdict without staging leaves the pool and the record apart, "
                             "which is the failure this file exists to remove")
        res = record_and_stage(slug, pool, verdicts_path, plan, decisions,
                               cand_file, a.dry_run)
        print(f"[prestage] {slug}: {len(res['accepted'])} accepted and "
              f"{'would be ' if a.dry_run else ''}staged, {len(res['rejected'])} rejected at "
              f"the content look, {len(plan['dropped'])} dropped mechanically before it. "
              f"Pool now {res['pool_clips']} clip(s).")
        st = pool_state(pool, verdicts_path, spec if not spec_problems else None)
        print(f"[prestage] check_pool_frames state: "
              f"{'SKIP' if st['skipped'] else ('OK' if st['ok'] else 'BLOCK')} "
              f"binding={st.get('binding')} -- {st['reason'][:400]}")
        print(f"[prestage] apply_clip_verdicts.py has nothing to undo: no rejected clip was "
              f"ever copied into {_rel(pool)}.")
        return 0 if (st["ok"] or st["skipped"]) else 1

    # ---------------- phase 1: judge the candidates -------------------------------------
    t0 = datetime.now(timezone.utc)
    print(f"[prestage] {slug}: judging candidates BEFORE the copy. Pool is {_rel(pool)} "
          f"({len(list(pool.glob('*.mp4'))) if pool.is_dir() else 0} clip(s) already there).")
    if era:
        yrs = era.get("years") or []
        print(f"[prestage] era_setting: {era.get('place')} ({era.get('country') or '?'}) "
              f"{yrs[0] if yrs else '?'}-{yrs[1] if len(yrs) > 1 else '?'}")
    else:
        print(f"[prestage] !! no era_setting declared -- no period or place prompt is possible")

    if a.candidates:
        src = Path(a.candidates)
        if not src.is_absolute():
            src = ROOT / src
        doc = json.loads(src.read_text(encoding="utf-8"))
        rows = list(doc.get("candidates") if isinstance(doc, dict) else doc)
        print(f"[prestage] 0. candidates: {len(rows)} from {_rel(src)} (not re-selected)")
    else:
        rows = emit_candidates(slug, a.per_query, cand_file)
        print(f"[prestage] 0. candidates: {len(rows)} selected, NONE COPIED")
    n_in = len(rows)
    for r in rows:
        r.setdefault("name", r.get("staged_as"))

    timings: dict[str, float] = {}

    def tick(label: str, t: datetime) -> None:
        timings[label] = round((datetime.now(timezone.utc) - t).total_seconds(), 1)

    t = datetime.now(timezone.utc)
    rows, d_junk = filter_junk(rows)
    tick("junk_words", t)
    print(f"[prestage] 1. junk words:        -{len(d_junk):4d}  -> {len(rows)} left")

    t = datetime.now(timezone.utc)
    rows, d_block = filter_blocklist(rows, slug)
    tick("blocklist", t)
    print(f"[prestage] 2. blocklist:         -{len(d_block):4d}  -> {len(rows)} left"
          + (f"   {', '.join(r['name'][:36] for r in d_block[:3])}" if d_block else ""))

    # 2b/2c BEFORE the ffprobe and before any frame is decoded. Both are pure text tests on
    # the candidate's own ledger title, so every clip they remove is a clip the expensive
    # steps below -- and the human reading the contact sheet -- never has to pay for.
    forbidden = forbidden_subjects_for(slug)
    t = datetime.now(timezone.utc)
    rows, d_forb = filter_forbidden(rows, forbidden)
    tick("forbidden_subjects", t)
    print(f"[prestage] 2b. forbidden_subjects: -{len(d_forb):4d}  -> {len(rows)} left"
          f"   ({len(forbidden)} term(s) declared by episode_spec)"
          + (f"   {', '.join(sorted({r['drop_reason'].split(chr(39))[1] for r in d_forb}))}"
             if d_forb else ""))

    t = datetime.now(timezone.utc)
    rows, d_dec = filter_decisive(rows, era)
    tick("decisive_contradiction", t)
    print(f"[prestage] 2c. place/period:      -{len(d_dec):4d}  -> {len(rows)} left"
          f"   (setting_mismatch / mobile_phone only -- look:vehicle and look:person are NOT "
          f"a finding and are kept)")

    t = datetime.now(timezone.utc)
    rows, d_shape, measured = filter_shape(rows, a.jobs)
    tick("shape", t)
    print(f"[prestage] 3. shape (measured):  -{len(d_shape):4d}  -> {len(rows)} left"
          f"   ({measured} newly probed, rest from {_rel(SHAPE_SCAN)})")

    t = datetime.now(timezone.utc)
    rows, d_reuse = filter_reuse(rows, slug, a.jobs)
    tick("cross_episode_reuse", t)
    print(f"[prestage] 4. cross-episode:     -{len(d_reuse):4d}  -> {len(rows)} left")

    dropped = d_junk + d_block + d_forb + d_dec + d_shape + d_reuse
    mech_s = sum(timings.values())
    print(f"[prestage] mechanical filters removed {len(dropped)} of {n_in} candidate(s) in "
          f"{mech_s:.1f}s. The content look now runs on {len(rows)}, not {n_in}.")

    if not rows:
        print("[prestage] nothing survived the mechanical filters -- nothing to look at")
        receipt: dict = {"clips": [], "samples": [], "sheets": []}
    else:
        t = datetime.now(timezone.utc)
        receipt = content_look(slug, rows, out_dir, pool, a.jobs, a.samples_min,
                               a.samples_max, faces=not a.no_faces)
        tick("content_look", t)

    by_clip = {c["clip"]: c for c in receipt.get("clips", [])}
    presented = []
    for r in rows:
        c = by_clip.get(r["name"], {})
        presented.append({
            "clip": r["name"], "src": str(r["src"]), "title": r.get("title"),
            "duration_s": c.get("duration_s"), "samples": c.get("samples"),
            "era_prompts": c.get("era_prompts") or [],
            "look_closer": c.get("look_closer") or [],
            "faces": c.get("faces") or [],
        })

    plan = {
        "schema_version": "prestage_footage_review.v001",
        "slug": slug,
        "generated_at": t0.isoformat(),
        "pool": _rel(pool),
        "order": ["select", "junk_words", "blocklist", "forbidden_subjects",
                  "decisive_contradiction", "shape", "cross_episode_reuse",
                  "content_look", "decide", "stage"],
        "candidates_in": n_in,
        "dropped_by": {"junk_words": len(d_junk), "blocklist": len(d_block),
                       "forbidden_subjects": len(d_forb),
                       "decisive_contradiction": len(d_dec),
                       "shape": len(d_shape), "cross_episode_reuse": len(d_reuse)},
        "presented_for_content_verdict": len(presented),
        "seconds": timings,
        "frames_receipt": _rel(QC / f"{slug}_prestage_frames.v001.json"),
        "sheets": receipt.get("sheets", []),
        "frames_dir": _rel(out_dir / "frames"),
        "prompts_are_not_detectors": (
            "era_prompts and look_closer read this clip's FILENAME and ledger TITLE against "
            "word tables. They are a reading order, not a finding: on the real EP62 clip that "
            "put a 2011 Range Rover Evoque on an EU plate into a 1975 film the era table fires "
            "NOTHING, and that clip is called `playground`. `person_pixels` and `faces` are the "
            "only entries here that came from pixels, and a haarcascade both misses and "
            "invents. A candidate with no prompt has been cleared by nobody."),
        "dropped": [{"name": r["name"], "src": str(r["src"]),
                     "dropped_by": r["dropped_by"], "drop_reason": r["drop_reason"]}
                    for r in dropped],
        "presented": presented,
    }
    QC.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n",
                         encoding="utf-8")

    print(f"[prestage] plan -> {_rel(plan_path)}")
    print(f"[prestage] {slug}: {n_in} candidate(s) in, {len(dropped)} dropped mechanically, "
          f"{len(presented)} presented for a content verdict, 0 staged so far.")
    print(f"[prestage] NEXT: read {len(receipt.get('sheets', []))} sheet(s) in {_rel(out_dir)}, "
          f"OPEN THE FULL-SIZE FRAME in {_rel(out_dir / 'frames')} for every clip with a "
          f"look_closer entry, then:")
    print(f'    echo \'{{"reviewer": "...", "reject": {{"<clip>.mp4": "why"}}}}\' > rejects.json')
    print(f"    py -3.11 scripts/prestage_footage_review.py --slug {slug} "
          f"--decide rejects.json --stage")
    print(f"[prestage] nothing has been copied into {_rel(pool)}. That is the point: the "
          f"judgement happens while the clips are still on the shelf, so a reject costs a line "
          f"in a json instead of a copy, a review round and a move back out.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
