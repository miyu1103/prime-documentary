#!/usr/bin/env python
"""Stage episode footage by the archive ledger's TITLE, not by the filename's subtype label.

WHY THIS EXISTS (2026-07-30, EP51 visual QC): the factory shelf's filename labels are
pervasively wrong -- `AF-BG-23326__barbed_wire_fence_sky.mp4` is really "majestic texas
longhorns in rural pasture", `AF-BG-18181__evidence_bag.mp4` is a close-up of a child's face.
Every selector we had picked by that label, which is why serious documentaries kept getting
cartoon gravestones and pastel office desks (pd-factory-shelf-mislabeled). The ledger row,
however, carries the REAL human-written title. Selecting on the title -- and re-naming the
staged copy after it -- makes the mislabelling structurally unable to reach a film, and makes
the contact sheet readable, because the caption under each tile is now the truth.

    python scripts/stage_footage_by_title.py --slug willingham \
        --query "house fire" --query "prison cell" --per-query 4 [--dry-run]

Writes remotion/public/<slug>/factory/AR-<id>__<title-slug>.mp4 plus a staging receipt.
Read-only against the shelf: files are COPIED, never moved or edited.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_DIR = Path(r"E:\pd-archive\_ledger")
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv"}
OK_LICENSE = {"free_commercial", "pd", "cc0"}
# titles that read as stock-cheap or plainly wrong for a documentary, whatever they matched
TITLE_BLOCK = re.compile(
    r"\b(cartoon|3d render|3d animation|animated character|christmas|halloween|santa|"
    r"emoji|meme|logo|template|mockup|game|anime|toy car|funny)\b", re.I)
# Names left behind by YouTube-ripping sites. Hyphen, underscore and space all appear, because
# the identifier is slugified at different points by different tools.
RIP_SIGNATURE = re.compile(
    r"y[-_ ]?2mate|ytmp3|savefrom|ss[-_ ]?youtube|9convert|yt1s|snaptube|x2mate|"
    r"onlinevideoconverter|tubemate|4k[-_ ]?download|ytdlp|youtube[-_ ]?dl", re.I)


def slugify(text: str, limit: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return (s[:limit].rstrip("_")) or "untitled"


# --------------------------------------------------------------------------------------
# CROSS-EPISODE DE-DUP ON CONTENT (2026-08-12).  The id/name exclusion below is kept and
# still runs first, because it is free; this is the half that decides.
# --------------------------------------------------------------------------------------
def content_index(slug: str, enabled: bool = True):
    """The set of bytes already placed in ANOTHER episode's cut, or None when disabled.

    WHY (measured over all 46 film jsons, 2026-08-12). This function's absence is the single
    mechanical cause of the owner's longest-standing complaint, 「素材の被り」. The id-prefix
    exclusion further down asks whether `AR-11490316` has been used before. It cannot ask
    whether these BYTES have been used before, and the shelf has ingested the same source file
    more than once under different identifiers -- `AR-11490316__close_up_view_of_barbed_wire.mp4`
    on one row, `AF-BG-23315__barbed_wire_fence_sky.mp4` on another. Two different ids, two
    different filenames, one file.

        9,717 distinct cut files · 524 content groups shared by >=2 episodes · 1,272 incidents
        861 of the 1,272 (68%) share BYTES BUT NOT FILENAMES -- invisible to any name check
        29 of 43 episodes read red; one content group spans NINE episodes
        one pair carries labels for different subjects (scenic_sandy_pathway / white_picket_fence)
        for identical bytes, so the shelf label is provably wrong on at least one of them

    `check_arc_nonrepeat.py` was taught to decide on sha256 the same day, so the defect is now
    DETECTED at ship time. This stops it being CREATED. Both halves import the SAME
    `build_content_universe`, so the selector and the gate cannot disagree about what counts.

    FAIL-CLOSED. If the universe cannot be built, or is too small to be believable, harvesting
    stops rather than quietly running blind -- running blind is exactly what produced 1,272
    incidents. `--no-content-dedup` is the deliberate, printed way out.
    """
    if not enabled:
        print("[stage] !! --no-content-dedup: candidates are NOT compared against other "
              "episodes' bytes. Reuse created here will be caught only at the ship gate.")
        return None
    try:
        import check_arc_nonrepeat as arc  # local module, same scripts/ dir
        idx = arc.ContentIndex(arc.target_labels_for(slug))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(
            f"[stage] REFUSING TO RUN: cannot build the cross-episode content index ({exc!r}).\n"
            f"[stage] Staging without it re-creates the duplication it exists to prevent. Fix the "
            f"index, or pass --no-content-dedup and own the consequence.")
    if idx.files < arc.MIN_FINGERPRINTS:
        raise SystemExit(
            f"[stage] REFUSING TO RUN: the content universe holds {idx.files} file(s) from "
            f"{len(idx.episodes)} episode(s), below the {arc.MIN_FINGERPRINTS} floor. That is not "
            f"a comparison, it is a rubber stamp. Pass --no-content-dedup if this repo genuinely "
            f"has no prior episodes.")
    print(f"[stage] content index: {idx.files} file(s) cut into {len(idx.episodes)} other "
          f"episode(s), indexed by byte size -- a candidate is excluded when its BYTES already "
          f"appear there, whatever it is called")
    return idx


def _content_owners(idx, src: Path) -> list[str]:
    return idx.owners_of(src) if idx is not None else []


# --------------------------------------------------------------------------------------
# TITLE MATCHING.  A query term matches a WORD of the title, not a run of characters
# anywhere inside it.
# --------------------------------------------------------------------------------------
_WORD_RX = re.compile(r"[a-z0-9]+")
# The endings the ledger's own titles inflect with. A term matches a word that is the term
# itself, or the term plus exactly ONE of these. Nothing else. That one rule is the whole
# difference between reaching `car` in `cars` (wanted) and in `carpentry` (the accident).
_STEM_SUFFIXES = ("s", "es", "ed", "d", "ing")


def title_words(text: str) -> tuple[str, ...]:
    """A title as its words.

    Hyphens, slashes, commas and apostrophes are all separators, so `two-lane`, `two lane`
    and `two,lane` tokenise identically -- the ledger spells the same thing all three ways.
    """
    return tuple(_WORD_RX.findall(text.lower()))


def match_keys(words: tuple[str, ...]) -> frozenset[str]:
    """Every form a one-word query term may take and still legitimately match `words`.

    WHY THIS REPLACED `t in title.lower()` (EP68 pinto, 2026-08-11). The old test was a
    substring test with no word boundaries, so a term matched the INSIDE of an unrelated
    word and pulled the film's whole register off course. Measured on pinto's 807
    candidates: 100 of them, 12.4%, matched only inside a word --

        old car -> "people protesting and h(old)ing pla(car)ds"   <- the 2020 BLM footage
        arch    -> "people m(arch)ing on the street in protest"   <- the second BLM source
        trial   -> "indus(trial) worker cleaning factory shop floor"
        gas     -> "vibrant las ve(gas) nightlife"
        corn    -> "freshly popped pop(corn) at amusement park"

    Each word contributes itself plus its de-inflected stem, so `car` still reaches `cars`
    and `press` still reaches `pressing` -- the inflections this ledger genuinely relies on.
    Every key is a prefix of a real word in the title, so this set can only ever match a
    SUBSET of what the substring test matched: the fix can drop a hit, never invent one.
    """
    keys: set[str] = set()
    for w in words:
        keys.add(w)
        for suf in _STEM_SUFFIXES:
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                keys.add(w[: -len(suf)])
    return frozenset(keys)


def _word_matches(term: str, word: str) -> bool:
    return word == term or any(word == term + s for s in _STEM_SUFFIXES)


def query_terms(q: str) -> tuple[tuple[str, ...], ...]:
    """Split a query the way it has always been split, then tokenise each term.

    `old car`  -> (('old',), ('car',))    two terms, ANDed, order-free -- unchanged.
    `two-lane` -> (('two', 'lane'),)      ONE term of two words that must be ADJACENT, which
                                          is what a hyphen means. The substring test got that
                                          right by accident and lost it the moment the title
                                          spelled it `two lane`.
    """
    out: list[tuple[str, ...]] = []
    for tok in q.lower().split():
        seq = tuple(_WORD_RX.findall(tok))
        if seq:
            out.append(seq)
    return tuple(out)


def title_matches(terms: tuple[tuple[str, ...], ...], words: tuple[str, ...],
                  keys: frozenset[str]) -> bool:
    """Every term present as a whole word, or as an inflection of one. ANDed, as before."""
    for seq in terms:
        if len(seq) == 1:
            if seq[0] not in keys:
                return False
            continue
        n = len(seq)
        if not any(all(_word_matches(seq[j], words[i + j]) for j in range(n))
                   for i in range(len(words) - n + 1)):
            return False
    return True


# --------------------------------------------------------------------------------------
# FORBIDDEN SUBJECTS, applied at selection -- the filter the query file said existed.
# --------------------------------------------------------------------------------------
def forbidden_subjects_for(slug: str) -> frozenset[str]:
    """The episode's OWN `forbidden_subjects`, read from its episode_spec. Empty if none.

    `config/episode_footage_queries.v001.json` said of EP68's 124 terms: *"they are applied
    to candidate titles before staging"*. No code applied them, anywhere. 106 of pinto's 807
    candidates carried one as a whole word in their own ledger title -- drone 26, burning 14,
    beach 11, smoke 10, fire 5, police 4 -- and every one reached a human reviewer.
    `check_spec_satisfied.py` matches these word-wise against the STAGED filename, so a
    survivor here is an automatic build failure hours later; catching it at selection costs
    one set lookup per title.

    An episode with no spec, or a spec that does not validate, contributes no terms: this
    function never invents a constraint, it only enforces a declared one.
    """
    try:
        from check_episode_spec import load_and_validate
        spec, problems, _ = load_and_validate(slug)
    except Exception:  # noqa: BLE001
        return frozenset()
    if problems or not spec:
        return frozenset()
    return frozenset(str(w).lower().strip()
                     for w in (spec.get("forbidden_subjects") or []) if str(w).strip())


def forbidden_hit(forbidden: frozenset[str], words: tuple[str, ...],
                  keys: frozenset[str]) -> str:
    """The first forbidden subject this title carries AS A WORD, or ''.

    Word-wise, and through the same stems as the matcher, so a spec that forbids `drone`
    also catches `drones` and one that forbids `fire` also catches `fired` -- while
    `warehouse` keeps its `war` and `kidney` keeps its `kid`.
    """
    if not forbidden:
        return ""
    for w in words:
        if w in forbidden:
            return w
    for k in keys:
        if k in forbidden:
            return k
    # MULTI-WORD TERMS, added 2026-08-21. The three tests above are word-wise, so a forbidden
    # subject written as a PHRASE -- "hong kong", "concert crowd", "european street", "body bag" --
    # could never appear in `words` and could never fire. Measured across every episode_spec on
    # disk: 434 of 1,442 declared forbidden subjects, 30%, contained a space and were therefore
    # inert, and five episodes (weimer, correa, marmet, greene, memphis) had NO working term at
    # all. EP74 itaewon found it the only way it can be found -- by opening the candidate frames
    # and seeing Hong Kong aerials in a film that forbids Hong Kong by name.
    #
    # Matched against the token sequence with sentinels, so word boundaries still hold: a spec
    # that forbids "concert crowd" does not fire on "concerted".
    if any(" " in t for t in forbidden):
        joined = " " + " ".join(words) + " "
        for t in forbidden:
            if " " in t and f" {t} " in joined:
                return t
    return ""


def assert_queries_clean(queries: list[str], forbidden: frozenset[str], slug: str) -> None:
    """A query that ASKS FOR a forbidden subject is a config contradicting its own spec.

    19 of pinto's 465 shipped queries were themselves forbidden subjects -- `fire`, `smoke`,
    `crash`, `wreck`, `hourglass`, `car crash`, `bonfire`, `candle flame`, `soot` -- while
    the episode's spec forbids exactly those, and they harvested 106 banned clips. A
    contradiction between the query set and the spec cannot be settled by filtering
    afterwards: one of the two documents is wrong and a human has to say which. So it stops
    here, before a single row of the ledger is read.
    """
    bad: list[tuple[str, str]] = []
    for q in queries:
        for seq in query_terms(q):
            hit = forbidden_hit(forbidden, seq, match_keys(seq))
            if hit:
                bad.append((q, hit))
                break
    if not bad:
        return
    lines = "\n".join(f"    {q!r} asks for forbidden subject {w!r}" for q, w in bad[:25])
    more = f"\n    ... and {len(bad) - 25} more" if len(bad) > 25 else ""
    raise SystemExit(
        f"[stage] REFUSING TO RUN: {len(bad)} of {len(queries)} queries for {slug!r} ask for "
        f"a subject that episode's own episode_spec.v001.json forbids.\n{lines}{more}\n"
        f"[stage] Fix config/episode_footage_queries.v001.json or fix the spec. A query set "
        f"that contradicts the spec must not harvest -- do not weaken forbidden_subjects.")


def ledger_rows():
    for fn in sorted(os.listdir(LEDGER_DIR)):
        if not fn.endswith(".jsonl") or fn.startswith("rejects") or fn.endswith(
                ("_dedup_removed.jsonl", "_candidates.jsonl")):
            continue
        with open(LEDGER_DIR / fn, encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except Exception:
                    continue


def write_receipt(slug: str, rows: list[dict]) -> Path:
    """Merge these staging rows into runs/qc/<slug>_title_staging.v001.json, keyed by staged_as.

    MERGE, not overwrite. The receipt is the provenance of every clip in the pool -- ledger
    title, source and licence -- and `check_pool_frames.staging_rows`, `write_factory_clip_qc`
    and the visual QC all read it. Staging a top-up used to replace it with only the new rows,
    which left every clip staged earlier reported as `FILENAME ONLY -- no ledger row`.
    """
    out = ROOT / "runs" / "qc" / f"{slug}_title_staging.v001.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    have: dict[str, dict] = {}
    if out.is_file():
        try:
            for r in json.loads(out.read_text(encoding="utf-8")).get("staged") or []:
                if r.get("staged_as"):
                    have[str(r["staged_as"])] = r
        except Exception:  # noqa: BLE001
            have = {}
    for r in rows:
        have[str(r["staged_as"])] = r
    out.write_text(json.dumps({"slug": slug, "staged": list(have.values())},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def stage_from(slug: str, cand_path: Path, accepted_path: Path | None,
               dry_run: bool, dest_dir: Path | None = None,
               no_content_dedup: bool = False) -> int:
    """Copy ONLY the candidates a review accepted. No ledger scan, no selection, no judgement.

    This is the second half of the gated order (`prestage_footage_review.py`): the candidate
    list was produced by --emit-candidates, every candidate was filtered and looked at while
    it was still on the shelf, and what arrives here is the surviving subset. Staging is the
    LAST step, so the pool is clean by construction and `apply_clip_verdicts.py` has nothing
    to undo.
    """
    doc = json.loads(cand_path.read_text(encoding="utf-8"))
    rows = list(doc.get("candidates") if isinstance(doc, dict) else doc)
    if accepted_path:
        acc = json.loads(accepted_path.read_text(encoding="utf-8"))
        names = set(acc.get("accepted") if isinstance(acc, dict) else acc)
        rows = [r for r in rows if str(r.get("staged_as") or r.get("name")) in names]
        if len(names) != len(rows):
            missing = names - {str(r.get("staged_as") or r.get("name")) for r in rows}
            print(f"[stage] {len(missing)} accepted name(s) are not in the candidate list and "
                  f"will NOT be staged: {', '.join(sorted(missing)[:5])}")
    dest = dest_dir or (ROOT / "remotion" / "public" / slug / "factory")
    dest.mkdir(parents=True, exist_ok=True)
    # THE COPY IS THE LAST PLACE REUSE CAN BE STOPPED. A candidate list emitted before the
    # content check existed carries clips selected without it -- openfields' ten came through
    # exactly this path -- and a list can also be days old, by which time another episode may
    # have cut the same bytes. So the check runs here too, on the file that is about to be
    # copied, not only where the list was made.
    content = content_index(slug, not no_content_dedup)
    staged: list[dict] = []
    n_dupe = 0
    for r in rows:
        name = str(r.get("staged_as") or r["name"])
        src = Path(str(r["src"]))
        if (dest / name).is_file():
            continue
        if not src.is_file():
            print(f"[stage] source vanished, skipping: {src}")
            continue
        owners = _content_owners(content, src)
        if owners:
            n_dupe += 1
            print(f"[stage] REUSE, not copied: {name} is byte-identical to footage already cut "
                  f"into {', '.join(owners[:4])}")
            continue
        if not dry_run:
            shutil.copy2(src, dest / name)
        staged.append({"query": r.get("query"), "id": r.get("id"), "title": r.get("title"),
                       "source": r.get("source"), "license": r.get("license"),
                       "src": str(src), "staged_as": name})
    if content is not None:
        print(f"[stage] content de-dup: -{n_dupe} named clip(s) NOT copied because their bytes "
              f"are already cut into another episode ({content.hashed_files} file(s) hashed)")
        content.save()
    if staged and not dry_run:
        print(f"[stage] receipt {write_receipt(slug, staged)}")
    print(f"[stage] {len(staged)} accepted clip(s) {'would be ' if dry_run else ''}staged into "
          f"{dest} (of {len(rows)} named); pool now "
          f"{len(list(dest.glob('*.mp4')))} clip(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--query", action="append",
                    help="title terms, ANDed; repeat the flag for more queries")
    ap.add_argument("--emit-candidates",
                    help="run the selection and WRITE THE LIST, copying nothing. This is the "
                         "first step of the gated order: the clips are judged on the shelf "
                         "and only survivors are ever copied into the pool.")
    ap.add_argument("--stage-from",
                    help="a candidate list from --emit-candidates; copy from it instead of "
                         "searching the ledger again")
    ap.add_argument("--dest", help="staging destination (default "
                                    "remotion/public/<slug>/factory)")
    ap.add_argument("--accepted",
                    help="json {'accepted': [staged_as, ...]} -- with --stage-from, copy only "
                         "these. Without it, --stage-from copies the whole candidate list.")
    ap.add_argument("--per-query", type=int, default=4)
    ap.add_argument("--min-mb", type=float, default=1.0)
    ap.add_argument("--max-mb", type=float, default=120.0)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-content-dedup", action="store_true",
                    help="do NOT exclude candidates whose bytes are already cut into another "
                         "episode. Only for a repo with no prior episodes: without it, staging "
                         "re-creates the cross-episode footage reuse the ship gate now fails on.")
    a = ap.parse_args()

    if a.stage_from:
        return stage_from(a.slug, Path(a.stage_from),
                          Path(a.accepted) if a.accepted else None, a.dry_run,
                          Path(a.dest) if a.dest else None, a.no_content_dedup)
    if not a.query:
        print("[stage] --query is required unless --stage-from is given", file=sys.stderr)
        return 2
    dest = ROOT / "remotion" / "public" / a.slug / "factory"
    dest.mkdir(parents=True, exist_ok=True)
    have = {p.name for p in dest.glob("*.mp4")}
    have_ids = {n.split("__")[0] for n in have}

    # CROSS-EPISODE DE-DUP (EP51 acceptance, 2026-07-30: 143 of 263 cuts were clips this
    # episode shared with morton/flowers, i.e. the owner's 「素材の被り」 measured). The same
    # top-N title match was handed to every episode because staging looked only at ITS OWN
    # folder. Anything already staged for another episode is off the table here.
    # `factory*` on purpose: factory_rejected / factory_pruned_offtopic / factory_offtopic hold
    # clips a human already looked at and threw out. Globbing only `factory` re-staged them the
    # moment a pool was topped up (EP57 fieldtest, 2026-08-02) -- a rejected clip must stay dead
    # for every episode, not come back through the next query.
    for other in sorted((ROOT / "remotion" / "public").glob("*/factory*")):
        if other.parent.name == a.slug and other.name == "factory":
            continue
        for q in other.glob("*.mp4"):
            have_ids.add(q.name.split("__")[0])
    print(f"[stage] {len(have_ids)} clip id(s) already used by this or another episode -- excluded")

    # A CLIP REJECTED BEFORE THE COPY LEAVES NO FILE BEHIND. The glob above works because the
    # old order copied everything first, so a reject physically sat in factory_rejected/ and
    # was excluded from every later query by its presence there. Under the gated order
    # (prestage_footage_review.py) a rejected candidate is never copied at all, so nothing on
    # disk remembers it and the next episode's query surfaces it again -- the exact way
    # AR-10159563 came back within a day. The verdict files are the memory instead.
    verdict_ids = 0
    for vf in sorted((ROOT / "runs" / "qc").glob("*verdicts.v001.json")):
        try:
            v = json.loads(vf.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for name in list(v.get("rejected") or {}) + list(v.get("prestage_dropped") or {}):
            ident = str(name).split("__")[0].rsplit(".", 1)[0]
            if ident and ident not in have_ids:
                have_ids.add(ident)
                verdict_ids += 1
    print(f"[stage] {verdict_ids} further clip id(s) excluded because a recorded verdict "
          f"rejected them -- including clips that were judged and NEVER copied")

    rows = [r for r in ledger_rows()
            if Path(str(r.get("file_path", ""))).suffix.lower() in VIDEO_EXT
            and r.get("license_decision") in OK_LICENSE]
    print(f"[stage] ledger videos with a usable licence: {len(rows)}")

    # TOKENISE EVERY TITLE ONCE, not once per query. This episode ships 465 queries against
    # ~39k ledger rows: doing the regex inside the query loop would be 18M tokenisations and
    # would make the correctness fix cost more time than the substring test ever saved. The
    # per-row screens (block list, rip signature, forbidden subjects) are query-independent,
    # so they belong here too -- and each refusal is now reported once, not once per query.
    forbidden = forbidden_subjects_for(a.slug)
    assert_queries_clean(a.query, forbidden, a.slug)
    if forbidden:
        print(f"[stage] {len(forbidden)} forbidden_subject(s) declared by {a.slug}'s "
              f"episode_spec are being applied to candidate titles")
    else:
        print(f"[stage] !! {a.slug} declares no usable forbidden_subjects -- no subject screen")

    prepared: list[tuple[dict, str, tuple[str, ...], frozenset[str]]] = []
    n_block = n_rip = n_forbidden = 0
    forbidden_examples: list[str] = []
    for r in rows:
        title = str(r.get("title", "")).strip()
        if not title or TITLE_BLOCK.search(title):
            n_block += 1
            continue
        # A RIPPED UPLOAD ANNOUNCES ITSELF IN ITS OWN NAME. The signature lives in the
        # archive.org identifier, not the title, so TITLE_BLOCK never sees it -- and the
        # licence filter cannot help, because the tag is whatever the uploader typed.
        if RIP_SIGNATURE.search(f"{r.get('id', '')} {r.get('file_path', '')} {title}"):
            n_rip += 1
            print(f"  RIGHTS: refusing {title[:60]!r} -- its name says it was ripped from "
                  f"YouTube; a CC0 tag on archive.org is the uploader's word, not proof")
            continue
        words = title_words(title)
        keys = match_keys(words)
        banned = forbidden_hit(forbidden, words, keys)
        if banned:
            n_forbidden += 1
            if len(forbidden_examples) < 5:
                forbidden_examples.append(f"{banned}: {title[:52]}")
            continue
        prepared.append((r, title, words, keys))
    print(f"[stage] titles: -{n_block} blocked, -{n_rip} ripped-upload signature, "
          f"-{n_forbidden} carrying a forbidden_subject -> {len(prepared)} searchable")
    for ex in forbidden_examples:
        print(f"  FORBIDDEN: {ex}")

    content = content_index(a.slug, not a.no_content_dedup)
    staged, receipt = 0, []
    n_dupe = 0
    dupe_examples: list[str] = []
    for q in a.query:
        terms = query_terms(q)
        picked = 0
        for r, title, words, keys in prepared:
            if picked >= a.per_query:
                break
            if not title_matches(terms, words, keys):
                continue
            src = Path(str(r.get("file_path", "")))
            mb = float(r.get("bytes", 0)) / 1e6
            if not src.exists() or not (a.min_mb <= mb <= a.max_mb):
                continue
            ident = f"AR-{slugify(str(r.get('id', src.stem)), 24)}"
            if ident in have_ids:
                continue
            name = f"{ident}__{slugify(title)}{src.suffix.lower()}"
            if name in have:
                continue
            # THE NAME CHECKS ABOVE ARE THE FAST PATH; THIS ONE IS THE AUTHORITY.
            owners = _content_owners(content, src)
            if owners:
                n_dupe += 1
                if len(dupe_examples) < 8:
                    dupe_examples.append(f"{name} == bytes already cut into "
                                         f"{', '.join(owners[:3])}")
                continue
            receipt.append({"query": q, "id": ident, "title": title, "source": r.get("source"),
                            "license": r.get("license_decision"), "src": str(src),
                            "name": name, "staged_as": name})
            have.add(name); have_ids.add(ident); picked += 1; staged += 1
            if not a.dry_run and not a.emit_candidates:
                shutil.copy2(src, dest / name)
        print(f"  {q!r:38} -> {picked} clip(s)")

    if content is not None:
        print(f"[stage] content de-dup: -{n_dupe} candidate(s) rejected because their BYTES are "
              f"already cut into another episode ({content.checked} checked, "
              f"{content.size_hits} needed a hash, {content.hashed_files} file(s) actually read, "
              f"{content.hashed_bytes / 1e6:.0f} MB)")
        for ex in dupe_examples:
            print(f"  REUSE: {ex}")
        content.save()

    if a.emit_candidates:
        out = Path(a.emit_candidates)
        if not out.is_absolute():
            out = ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {"schema_version": "footage_candidates.v001", "slug": a.slug,
             "generated_at": datetime.now(timezone.utc).isoformat(),
             "per_query": a.per_query, "queries": len(a.query),
             "note": "Selected from the archive ledger and NOT COPIED. Each row's `src` is "
                     "where the clip lives on the shelf; `name` is what it would be staged "
                     "as. Judge it here, then copy only what survives.",
             "candidates": receipt}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[stage] {staged} candidate(s) selected and NOT staged -> {out}")
        return 0

    print(f"[stage] {staged} clip(s) {'would be ' if a.dry_run else ''}staged into {dest}")
    if not a.dry_run and receipt:
        print(f"[stage] receipt {write_receipt(a.slug, receipt)}")
    print("[stage] NEXT: build a labelled contact sheet and look at every tile before rendering.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
