#!/usr/bin/env python3
r"""Independent SFX-manifest gate — proves the sound design is a RICH, MEANINGFUL, REAL palette,
not a few whoosh variants (or a machine-gun tick-bed), and not a list of fabricated names pointing
at files that do not exist.

Owner reject (EP32, 2026-07-06): "意味のない効果音がうざい / ピコピコ鳴ってて耳障り / 種類も
少なくてしょぼい". The audio builder had answered the old raw-onset floor by injecting a 326-hit
tick/blip filler "transient bed" on a fixed cadence PURELY to game the number. check_final_acceptance
already stopped counting raw transients and instead counts distinct MEANINGFUL SFX *files*. This gate
goes one level deeper and measures the REAL INTENT the file count only approximates:

  1. DISTINCT MEANINGFUL BASE SFX >= MIN_DISTINCT_BASE. We collapse variant/size/version tokens
     (whoosh_v2_long, whoosh_v2_short, whoosh_medium, whoosh_short  -> one base "whoosh") so that
     shipping ten flavours of the same whoosh does NOT read as a rich palette. Distinct file paths
     can be inflated by variants; distinct *base families* cannot. A genuine Kurzgesagt/Veritasium
     level mix has >= 12 different KINDS of sound (whoosh, boom, riser, page_turn, stamp, gavel,
     lock, ...), not 12 spellings of two sounds. A file whose name reduces to NOTHING semantic
     ('(unidentified)') is junk and never counts toward the 12.
  2. EVERY counted SFX carries a REAL SEMANTIC MEANING TAG. The old check accepted ANY non-empty
     string (phrase="x" passed) — theater. A cue is meaningful only when its phrase / trigger /
     explicit intent field names a real narrative sound intent drawn from ALLOWED_INTENTS
     (impact / transition / reveal / ui / tension / ambient-accent / whoosh / boom / riser / tick /
     page_turn / gavel / lock ...). "x", "a sound", "" -> NOT meaningful -> untagged -> the gate FAILS.
  3. EVERY counted SFX must be a REAL FILE, not a fabricated name. Each cue's file is cross-checked
     against (a) an actual file on disk (resolved via library_root / the episode dir) OR
     (b) an INDEPENDENT provenance attestation — a real absolute path or sha for that basename found
     somewhere OTHER than the cue's own `file` string (e.g. the rendered ffmpeg `-i` input list).
     A name with no backing file counts for NOTHING and FAILS the gate (unbacked_count).
  4. FILLER / tick-bed cues are EXCLUDED before counting (source = transient_bed / onset_filler /
     a fixed-cadence bed, or the provenance's declared transient_bed file). They can neither help
     (excluded from the distinct count) nor be laundered into "meaning".
  5. The ENDING chapter must declare a REAL, QUIET ambience bed. A missing chapter, a missing or
     empty ambience_bed (roar-by-omission), OR a roar / broadband / noise-tagged bed all FAIL: the
     film must resolve into a settled room tone under the CTA, never a blast of broadband roar and
     never nothing at all.

It reads the highest-revision 06_audio/audio_provenance.v*.json (its `sfx_cues` list is the source
of truth; `layers.sfx` / `density_gate` are used for reporting). It NEVER trusts a single summary
integer it cannot re-derive: the distinct-base count is recomputed from the actual (real, meaningful)
cue files here, so a wrong/optimistic `distinct_files` cannot slip a thin or fabricated palette past.

If the provenance is absent (e.g. the mix lives only on the H: media SSD and was not synced into the
repo), the gate SKIPS honestly (ok=True, hard=False, skipped=True) rather than faking green or
crashing the caller.

Usage:
  py -3.11 scripts/verify_sfx_manifest.py --ep PD-2026-031-unlock
  py -3.11 scripts/verify_sfx_manifest.py --ep PD-2026-032-carsearch --json out.json
  py -3.11 scripts/verify_sfx_manifest.py --ep PD-2026-032-carsearch --dry-run
  py -3.11 scripts/verify_sfx_manifest.py --selftest        # RED fixture + real-episode numbers

Exit code 0 = PASS (or dry-run, or honest SKIP), 1 = FAIL (or CLI usage error). Read-only: it never
writes into the episode. check_final_acceptance can `import verify_sfx_manifest; evaluate(epdir)`;
the returned dict shape ({"check","ok","hard","reason", ...}) is that contract.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterator, Optional

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EP = "PD-2026-031-unlock"

# --- thresholds (kept in sync with check_final_acceptance.SOUND_PROV_MIN_SFX_FILES = 12) ----------
# The gate measures a DEEPER quantity (distinct base families, not file paths), so 12 here is a
# strictly-no-weaker bar: you cannot satisfy it with 12 variants of one sound.
MIN_DISTINCT_BASE = 12

# Cue `source` values that mark a filler / cadence bed rather than a designed, meaningful hit. These
# are removed BEFORE any counting so a padded tick-bed can neither inflate distinctness nor meaning.
FILLER_SOURCES = {
    "transient_bed", "transient_filler", "onset_filler", "onset_bed", "density_filler",
    "density_bed", "filler", "tick_bed", "cadence_bed", "cadence_filler", "pad",
}
# Cue `timing` values that indicate a mechanical fixed cadence (the gaming pattern), also excluded.
FILLER_TIMINGS = {"fixed_cadence", "cadence", "grid", "metronome"}

# Ending ambience must not be a roar / broadband wash. Matched against the ending bed's base tokens.
ENDING_BED_BAD_TAGS = {
    "roar", "broadband", "noise", "whitenoise", "pinknoise", "static", "blast", "crowd_roar",
    "crowd", "cheer", "applause", "explosion", "wash",
}

# --- ALLOWED narrative sound-intent vocabulary (hole #1) ------------------------------------------
# A cue's meaning tag must name a REAL narrative sound intent, not any string. Category-level intents
# (the reviewer's examples) PLUS the concrete designed-sound / onomatopoeia families that ARE the
# intent. Matched token-wise (singular/plural) against phrase + trigger + any explicit intent field.
ALLOWED_INTENTS = {
    # category-level intents
    "impact", "transition", "reveal", "ui", "tension", "ambient", "accent", "ambience",
    "emphasis", "punctuation", "stinger", "foley", "cut", "swell", "riser", "rise",
    # concrete designed-sound families / onomatopoeia (the intent itself)
    "whoosh", "woosh", "boom", "drone", "hum", "turn", "page", "stamp", "seal", "tear",
    "rip", "clink", "clank", "clang", "blip", "beep", "bleep", "tick", "tock", "drop",
    "sub", "thud", "click", "clack", "clunk", "lock", "latch", "unlock", "pop", "knock",
    "gavel", "footstep", "step", "pass", "passby", "whir", "data", "chime", "ding", "buzz",
    "rustle", "paper", "slam", "hit", "punch", "pull", "check", "drag", "scrape", "ratchet",
    "zip", "flip", "snap", "crack", "pulse", "pluck", "shimmer", "glitch", "sweep",
}


# Variant / size / version / count tokens stripped when reducing a file name to its base family.
# (Semantic words like whoosh, boom, riser, stamp, gavel, lock survive.)
_VARIANT_TOKENS = {
    "sfx", "v1", "v2", "v3", "v4",
    "long", "short", "shorter", "med", "medium", "mid", "big", "small", "tiny",
    "hi", "high", "lo", "low", "deep", "tight", "wide", "soft", "hard", "light", "heavy",
    "loud", "quiet", "up", "down", "in", "out", "a", "b", "alt", "var", "loop", "oneshot",
    "l", "r", "left", "right", "stereo", "mono", "dry", "wet",
}
_DUR_TOKEN = re.compile(r"^\d+(?:s|ms|sec)?$")   # 2s, 3s, 500ms, 07, ...
_AUDIO_EXT = r"(?:mp3|wav|flac|ogg|aif|aiff|m4a)"
# A real audio file referenced as part of a PATH (preceded by a separator) — used for attestation.
_PATH_AUDIO = re.compile(r"[\\/]([^\\/\"'\s]+\." + _AUDIO_EXT + r")", re.IGNORECASE)


def norm_token(tok: str) -> str:
    """Lowercase alphanumeric core of a token."""
    return re.sub(r"[^a-z0-9]", "", tok.lower())


def base_family(file_ref: str) -> str:
    """Reduce an SFX file reference to its BASE sound family.

    'sfx/sfx_whoosh_v2_long.mp3'   -> 'whoosh'
    'sfx_whoosh_medium.mp3'        -> 'whoosh'
    'sfx/sfx_low_boom.mp3'         -> 'boom'
    'sfx/sfx_page_turn.mp3'        -> 'page_turn'
    'sfx/sfx_binder_lock.mp3'      -> 'binder_lock'
    Empty string if nothing semantic remains (treated as unidentifiable filler).
    """
    stem = Path(str(file_ref).replace("\\", "/")).name
    stem = re.sub(r"\.(mp3|wav|flac|ogg|aif|aiff|m4a)$", "", stem, flags=re.IGNORECASE)
    kept: list[str] = []
    for raw in re.split(r"[_\-.\s]+", stem):
        t = norm_token(raw)
        if not t:
            continue
        if t in _VARIANT_TOKENS or _DUR_TOKEN.match(t):
            continue
        kept.append(t)
    return "_".join(kept)


def _intent_tokens(*texts: str) -> list[str]:
    """Split the given texts into normalized word tokens for intent matching."""
    out: list[str] = []
    for text in texts:
        for raw in re.split(r"[^A-Za-z0-9]+", str(text or "")):
            t = norm_token(raw)
            if t:
                out.append(t)
    return out


def _token_is_intent(tok: str) -> bool:
    """A token names a real narrative sound intent (handles simple plural: ticks->tick)."""
    if tok in ALLOWED_INTENTS:
        return True
    if tok.endswith("s") and tok[:-1] in ALLOWED_INTENTS:
        return True
    if tok.endswith("es") and tok[:-2] in ALLOWED_INTENTS:
        return True
    return False


def cue_intent(cue: dict[str, Any]) -> Optional[str]:
    """Return the matched narrative sound intent for a cue, or None.

    Hole #1 fix: meaning is NOT "any non-empty phrase". The phrase / trigger / explicit intent field
    must name a real intent from ALLOWED_INTENTS. phrase="x" / "a sound" / "" -> None (meaningless).
    """
    explicit = " ".join(
        str(cue.get(k) or "") for k in ("intent", "sound_intent", "meaning", "tag", "role")
    )
    phrase = str(cue.get("phrase") or "")
    trigger = str(cue.get("trigger") or "")
    for tok in _intent_tokens(explicit, phrase, trigger):
        if _token_is_intent(tok):
            return tok
    return None


def _has_meaning(cue: dict[str, Any]) -> bool:
    """True only when the cue carries a REAL narrative sound-intent tag (see cue_intent)."""
    return cue_intent(cue) is not None


def _is_filler(cue: dict[str, Any], declared_bed_files: set[str]) -> bool:
    """True if this cue is a filler / cadence-bed hit that must be excluded before counting."""
    if cue.get("filler") is True:
        return True
    if str(cue.get("source") or "").strip().lower() in FILLER_SOURCES:
        return True
    if str(cue.get("timing") or "").strip().lower() in FILLER_TIMINGS:
        return True
    fname = Path(str(cue.get("file") or "").replace("\\", "/")).name.lower()
    if fname and fname in declared_bed_files:
        return True
    return False


def _iter_strings(obj: Any) -> Iterator[str]:
    """Yield every string value nested anywhere inside a JSON-like structure."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _iter_strings(v)


def _attested_basenames(prov: dict[str, Any]) -> set[str]:
    """Basenames of audio files the provenance INDEPENDENTLY attests as real paths.

    Hole #2 fix: we deliberately EXCLUDE the `sfx_cues` list itself, so a cue cannot self-attest by
    merely naming a file. Attestation must come from a real path referenced elsewhere — e.g. the
    rendered ffmpeg `-i "H:\\...\\sfx_whoosh.mp3"` input list, `wrote_files`, or a *_path field.
    """
    clone = {k: v for k, v in prov.items() if k != "sfx_cues"}
    out: set[str] = set()
    for s in _iter_strings(clone):
        for m in _PATH_AUDIO.finditer(s):
            out.add(m.group(1).lower())
    return out


def _resolve_candidates(file_ref: str, ep_dir: Path, library_root: str) -> list[Path]:
    """On-disk locations where the referenced SFX file could physically live."""
    ref = str(file_ref).replace("\\", "/").lstrip("/")
    name = Path(ref).name
    cands: list[Path] = []
    if library_root:
        lr = Path(str(library_root).replace("\\", "/"))
        cands += [lr / ref, lr / name, lr / "sfx" / name]
    cands += [ep_dir / ref, ep_dir / "06_audio" / ref, ep_dir / "06_audio" / name, ep_dir / name]
    return cands


def _file_backed(file_ref: str, ep_dir: Path, library_root: str,
                 attested: set[str]) -> tuple[bool, str]:
    """Return (is_backed, how). A cue counts only if its file is real: exists on disk OR is attested
    by an independent real path/sha in the provenance."""
    if not str(file_ref or "").strip():
        return False, "no-file"
    for cand in _resolve_candidates(file_ref, ep_dir, library_root):
        try:
            if cand.is_file():
                return True, "on-disk"
        except OSError:
            continue
    name = Path(str(file_ref).replace("\\", "/")).name.lower()
    if name and name in attested:
        return True, "attested"
    return False, "missing"


def _latest_provenance(ep_dir: Path) -> Optional[Path]:
    provs = sorted((ep_dir / "06_audio").glob("audio_provenance.v*.json"))
    return provs[-1] if provs else None


def _ending_chapter(prov: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Return the ending/CTA chapter dict (by id/title, else the last chapter), or None."""
    chapters = prov.get("chapters") or []
    if not isinstance(chapters, list) or not chapters:
        return None
    for ch in chapters:
        if not isinstance(ch, dict):
            continue
        cid = str(ch.get("chapter_id") or "").strip().lower()
        title = str(ch.get("title") or "").strip().lower()
        if cid == "ending" or "ending" in cid or "ending" in title or "cta" in cid or "cta" in title:
            return ch
    last = chapters[-1]
    return last if isinstance(last, dict) else None


def _ending_bed_flagged(bed: str) -> tuple[str, list[str]]:
    """Return (ending_bed_base, [bad tags found]) for the ending ambience bed reference."""
    base = base_family(bed) if bed else ""
    toks = set(re.split(r"[_\-.\s]+", base)) if base else set()
    raw = Path(str(bed).replace("\\", "/")).name.lower()
    raw_toks = set(re.split(r"[^a-z0-9]+", raw))
    hits = sorted((toks | raw_toks) & ENDING_BED_BAD_TAGS)
    return base or raw, hits


def evaluate(ep_dir: Path) -> dict[str, Any]:
    """Measure SFX-manifest richness + meaning + reality + a clean ending bed. Never raises/exits.

    Returns a check_final_acceptance-compatible dict. Keys include:
      check, ok, hard, reason, skipped(optional), distinct_base, distinct_bases,
      untagged_count, untagged_examples, unbacked_count, unbacked_examples, unidentified_count,
      filler_excluded, total_cues, backed_cues, meaningful_cues, ending_bed, ending_bed_missing,
      ending_bed_bad_tags, min_distinct, prov, problems.
    """
    ep_dir = Path(ep_dir)
    prov_path = _latest_provenance(ep_dir)
    if prov_path is None:
        return {"check": "sfx_manifest", "ok": True, "hard": False, "skipped": True,
                "reason": f"no 06_audio/audio_provenance.v*.json under {ep_dir} "
                          "(mix likely on media SSD, not synced) -> skipped honestly"}
    try:
        prov = json.loads(prov_path.read_text("utf-8"))
    except Exception as exc:  # noqa: BLE001 - malformed provenance is a skip, never a crash
        return {"check": "sfx_manifest", "ok": True, "hard": False, "skipped": True,
                "reason": f"could not parse {prov_path.name}: {exc}"}
    if not isinstance(prov, dict):
        return {"check": "sfx_manifest", "ok": True, "hard": False, "skipped": True,
                "reason": f"{prov_path.name} is not a JSON object -> cannot measure the palette"}

    cues = prov.get("sfx_cues")
    if not isinstance(cues, list) or not cues:
        return {"check": "sfx_manifest", "ok": True, "hard": False, "skipped": True,
                "reason": f"{prov_path.name} has no sfx_cues[] list -> cannot measure the palette"}

    # files the provenance itself declares as filler beds (excluded by name too)
    sfx_layer = (prov.get("layers") or {}).get("sfx") or {}
    declared_bed_files: set[str] = set()
    val = sfx_layer.get("transient_bed")
    if isinstance(val, str) and val.strip():  # riser_fill is a legit musical riser, NOT filler
        declared_bed_files.add(Path(val.replace("\\", "/")).name.lower())

    library_root = str(prov.get("library_root") or "")
    attested = _attested_basenames(prov)

    total_cues = len(cues)
    filler_excluded = 0
    backed_cues = 0
    unbacked_count = 0
    unidentified_count = 0
    meaningful_by_base: dict[str, int] = {}
    untagged_bases: dict[str, int] = {}
    untagged_examples: list[str] = []
    unbacked_examples: list[str] = []
    unidentified_examples: list[str] = []
    meaningful_cues = 0

    for cue in cues:
        if not isinstance(cue, dict):
            continue
        if _is_filler(cue, declared_bed_files):
            filler_excluded += 1
            continue
        file_ref = cue.get("file") or ""
        backed, _how = _file_backed(file_ref, ep_dir, library_root, attested)
        cid = str(cue.get("cue_id") or file_ref or "?")
        if not backed:
            # Hole #2: a fabricated name with no real file counts for NOTHING.
            unbacked_count += 1
            if len(unbacked_examples) < 6:
                unbacked_examples.append(cid)
            continue
        backed_cues += 1
        base = base_family(file_ref)
        if not base:
            # Hole #4: an unidentifiable file (no semantic token) is junk, never a distinct family.
            unidentified_count += 1
            if len(unidentified_examples) < 6:
                unidentified_examples.append(cid)
            continue
        if _has_meaning(cue):
            meaningful_by_base[base] = meaningful_by_base.get(base, 0) + 1
            meaningful_cues += 1
        else:
            untagged_bases[base] = untagged_bases.get(base, 0) + 1
            if len(untagged_examples) < 6:
                untagged_examples.append(f"{cid} phrase={cue.get('phrase')!r}")

    distinct_bases = sorted(meaningful_by_base)  # never contains '(unidentified)'
    distinct_base = len(distinct_bases)
    untagged_count = sum(untagged_bases.values())

    ending_ch = _ending_chapter(prov)
    ending_bed_raw = str((ending_ch or {}).get("ambience_bed") or "").strip()
    ending_bed_missing = (ending_ch is None) or (not ending_bed_raw)
    ending_bed, ending_bad = _ending_bed_flagged(ending_bed_raw)

    problems: list[str] = []
    if distinct_base < MIN_DISTINCT_BASE:
        problems.append(
            f"only {distinct_base} distinct MEANINGFUL+REAL base SFX < {MIN_DISTINCT_BASE} "
            f"(variants collapsed; palette too thin / しょぼい). bases={distinct_bases}")
    if unbacked_count > 0:
        problems.append(
            f"{unbacked_count} SFX cue(s) point to a file with NO backing (not on disk, not attested "
            f"by a real path/sha -> fabricated / missing): e.g. {unbacked_examples}")
    if untagged_count > 0:
        problems.append(
            f"{untagged_count} decoration-only SFX cue(s) with NO real meaning tag "
            f"(phrase/trigger names no intent in ALLOWED_INTENTS -> meaningless pips): "
            f"e.g. {untagged_examples}")
    if unidentified_count > 0:
        problems.append(
            f"{unidentified_count} SFX cue(s) whose file reduces to NO semantic family "
            f"('(unidentified)' junk, excluded from the {MIN_DISTINCT_BASE}): "
            f"e.g. {unidentified_examples}")
    if ending_bed_missing:
        problems.append(
            "ending chapter declares NO ambience bed (missing/empty) -> a roar/broadband bed could "
            "be hidden by omission; the ending MUST declare an explicit quiet room tone")
    elif ending_bad:
        problems.append(
            f"ending chapter ambience {ending_bed_raw!r} carries roar/broadband tag(s) "
            f"{ending_bad} (must resolve to a quiet room tone, not a broadband wash)")

    ok = not problems
    dg = prov.get("density_gate") or {}
    return {
        "check": "sfx_manifest",
        "ok": ok,
        "hard": True,
        "reason": ("rich, meaningful, real palette; clean ending bed" if ok else "; ".join(problems)),
        "prov": str(prov_path),
        "min_distinct": MIN_DISTINCT_BASE,
        "distinct_base": distinct_base,
        "distinct_bases": distinct_bases,
        "total_cues": total_cues,
        "backed_cues": backed_cues,
        "meaningful_cues": meaningful_cues,
        "untagged_count": untagged_count,
        "untagged_examples": untagged_examples,
        "unbacked_count": unbacked_count,
        "unbacked_examples": unbacked_examples,
        "unidentified_count": unidentified_count,
        "unidentified_examples": unidentified_examples,
        "filler_excluded": filler_excluded,
        "attested_files": len(attested),
        "ending_bed": ending_bed_raw,
        "ending_bed_base": ending_bed,
        "ending_bed_missing": ending_bed_missing,
        "ending_bed_bad_tags": ending_bad,
        "declared_filler_beds": sorted(declared_bed_files),
        "density_gate_sfx_count": dg.get("sfx_count"),
        "problems": problems,
    }


# ---------------------------------------------------------------------------------------------
# reporting / CLI
# ---------------------------------------------------------------------------------------------

def _print_report(r: dict[str, Any]) -> None:
    if r.get("skipped"):
        print(f"\n[SKIP] {r.get('reason')}")
        return
    print("\n" + "=" * 78)
    print("SFX MANIFEST REPORT  (distinct MEANINGFUL + REAL base families, variants collapsed)")
    print("=" * 78)
    print(f"  provenance      : {r['prov']}")
    print(f"  total cues      : {r['total_cues']}   backed: {r['backed_cues']}   "
          f"meaningful: {r['meaningful_cues']}   filler excluded: {r['filler_excluded']}")
    print(f"  attested files  : {r['attested_files']}")
    print(f"  distinct base   : {r['distinct_base']} / min {r['min_distinct']}")
    print(f"  bases           : {', '.join(r['distinct_bases'])}")
    print(f"  unbacked cues   : {r['unbacked_count']}"
          + (f"  e.g. {r['unbacked_examples']}" if r['unbacked_count'] else ""))
    print(f"  untagged cues   : {r['untagged_count']}"
          + (f"  e.g. {r['untagged_examples']}" if r['untagged_count'] else ""))
    print(f"  unidentified    : {r['unidentified_count']}"
          + (f"  e.g. {r['unidentified_examples']}" if r['unidentified_count'] else ""))
    print(f"  ending bed      : {r['ending_bed']!r}  missing={r['ending_bed_missing']}  "
          f"bad-tags={r['ending_bed_bad_tags']}")
    print("-" * 78)
    if r["ok"]:
        print("  RESULT: PASS  — rich, meaningful, real SFX palette; ending resolves clean")
    else:
        print("  RESULT: FAIL")
        for p in r["problems"]:
            print(f"    - {p}")
    print("-" * 78)


def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    """Atomic JSON write: temp file in the same dir, then os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False, default=str)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


# ---------------------------------------------------------------------------------------------
# self-test: RED fixture (the exact gaming probe -> must FAIL) + a GREEN good case (must PASS)
# ---------------------------------------------------------------------------------------------

def _red_fixture() -> dict[str, Any]:
    """The EXACT reviewer gaming probe. 12 DISTINCT base families so the old distinct-base bar is
    satisfied, but every cue is junk:
      * phrase="x"           -> no real meaning tag (hole #1)
      * files DON'T EXIST    -> fabricated names, not on disk, not attested anywhere (hole #2)
      * ending chapter       -> declares NO ambience bed (roar-by-omission, hole #3)
      * one '(unidentified)' -> file reduces to no semantic family (hole #4)
    Under the OLD gate this returned ok=True. After the fix it MUST report ok=False.
    """
    families = [
        "sfx/nonexist_whoosh.mp3", "sfx/nonexist_boom.mp3", "sfx/nonexist_riser.mp3",
        "sfx/nonexist_stamp.mp3", "sfx/nonexist_gavel.mp3", "sfx/nonexist_lock.mp3",
        "sfx/nonexist_click.mp3", "sfx/nonexist_page.mp3", "sfx/nonexist_tear.mp3",
        "sfx/nonexist_knock.mp3", "sfx/nonexist_drop.mp3", "sfx/nonexist_tick.mp3",
    ]
    cues: list[dict[str, Any]] = []
    for i, f in enumerate(families):
        cues.append({"cue_id": f"R-{i:03d}", "file": f, "source": "script_sfx",
                     "phrase": "x", "trigger": "", "timing": "beat_offset"})
    # a file that reduces to no semantic base family at all (unidentified junk)
    cues.append({"cue_id": "R-900", "file": "sfx/12345.mp3", "source": "script_sfx",
                 "phrase": "x", "trigger": "", "timing": "beat_offset"})
    return {
        "library_root": "Z:/does/not/exist",
        "chapters": [
            {"chapter_id": "act1", "title": "ACT I", "ambience_bed": "amb_office_hum.mp3"},
            # ending chapter present but NO ambience_bed declared -> omission bypass
            {"chapter_id": "ending", "title": "Ending / CTA"},
        ],
        "layers": {"sfx": {"transient_bed": None, "distinct_files": 12}},
        "density_gate": {"sfx_count": 13},
        "sfx_cues": cues,
    }


def _roar_ending_fixture() -> dict[str, Any]:
    """A variant whose ending bed IS declared but is a broadband ROAR -> must also FAIL."""
    f = _red_fixture()
    f["chapters"][-1]["ambience_bed"] = "amb_crowd_roar.mp3"
    return f


def _unidentified_fixture(ep: Path) -> dict[str, Any]:
    """A manifest with a BACKED (real on-disk) file whose name reduces to NO semantic family
    ('12345.mp3'). It must be counted as unidentified junk and NEVER appear as a distinct base."""
    lib = ep / "lib"
    (lib / "sfx").mkdir(parents=True, exist_ok=True)
    (lib / "sfx" / "12345.mp3").write_bytes(b"\x00")
    return {
        "library_root": str(lib),
        "chapters": [{"chapter_id": "ending", "title": "Ending / CTA",
                      "ambience_bed": "amb_room_tone.mp3"}],
        "layers": {"sfx": {"transient_bed": None}},
        "sfx_cues": [
            {"cue_id": "U-000", "file": "sfx/12345.mp3", "source": "script_sfx",
             "phrase": "a whoosh", "trigger": "", "timing": "beat_offset"},
        ],
    }


def _green_fixture(ep: Path) -> dict[str, Any]:
    """A genuinely good manifest: 12 distinct REAL base families, each with a real intent phrase and
    a file that ACTUALLY EXISTS on disk, plus a clean, declared ending bed. Must PASS."""
    lib = ep / "lib"
    (lib / "sfx").mkdir(parents=True, exist_ok=True)
    fam = [
        ("whoosh", "sfx_whoosh_v2_long.mp3", "a fast whoosh past the mic"),
        ("boom", "sfx_low_boom.mp3", "a low boom on the title"),
        ("riser", "sfx_riser_2s.mp3", "a tight riser"),
        ("page_turn", "sfx_page_turn.mp3", "page turn"),
        ("stamp", "sfx_stamp_seal.mp3", "a soft stamp"),
        ("gavel", "sfx_gavel_knock.mp3", "a gavel knock"),
        ("binder_lock", "sfx_binder_lock.mp3", "a lock pop"),
        ("click", "sfx_ui_click.mp3", "a confirming click"),
        ("tick", "sfx_tick_hi.mp3", "a soft tick"),
        ("blip", "sfx_data_blip.mp3", "a rising data-blip"),
        ("impact", "sfx_soft_impact.mp3", "the hardest impact in the film"),
        ("rustle", "sfx_paper_rustle.mp3", "a paper rustle"),
    ]
    cues: list[dict[str, Any]] = []
    for i, (_base, name, phrase) in enumerate(fam):
        (lib / "sfx" / name).write_bytes(b"\x00")  # a real (empty) file on disk
        cues.append({"cue_id": f"G-{i:03d}", "file": f"sfx/{name}", "source": "script_sfx",
                     "phrase": phrase, "trigger": "", "timing": "beat_offset"})
    return {
        "library_root": str(lib),
        "chapters": [
            {"chapter_id": "act1", "title": "ACT I", "ambience_bed": "amb_office_hum.mp3"},
            {"chapter_id": "ending", "title": "Ending / CTA", "ambience_bed": "amb_room_tone.mp3"},
        ],
        "layers": {"sfx": {"transient_bed": None, "distinct_files": 12}},
        "density_gate": {"sfx_count": 12},
        "sfx_cues": cues,
    }


def _run_selftest() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    print("### verify_sfx_manifest --selftest ###")
    rc = 0

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        # (a) RED FIXTURE = the exact gaming probe -> must be reported ok=False
        ep_red = base / "PD-9999-999-redfixture"
        (ep_red / "06_audio").mkdir(parents=True)
        _atomic_write_json(ep_red / "06_audio" / "audio_provenance.v001.json", _red_fixture())
        r = evaluate(ep_red)
        print("\n-- RED FIXTURE (exact probe: phrase='x', 12 non-existent files, missing ending bed) --")
        _print_report(r)
        red_ok = (r.get("ok") is False and not r.get("skipped"))
        print(f"\nRED-FIXTURE: {'PASS' if red_ok else 'FAIL'}  "
              f"(gate {'correctly reported ok=False' if red_ok else 'FAILED to flag the bad input'})")
        if not red_ok:
            rc = 1

        # (a2) targeted sub-probes proving each hole is closed independently
        print("\n-- HOLE SUB-PROBES --")
        m_x = cue_intent({"phrase": "x", "trigger": ""})
        m_ok = cue_intent({"phrase": "a fast whoosh", "trigger": ""})
        print(f"   hole#1 meaning-vocab : phrase='x'->{m_x!r} (want None) ; "
              f"'a fast whoosh'->{m_ok!r} (want a tag)")
        if m_x is not None or m_ok is None:
            print("   hole#1 SUB-PROBE: FAIL"); rc = 1
        else:
            print("   hole#1 SUB-PROBE: PASS")
        unbacked = r.get("unbacked_count", 0)
        print(f"   hole#2 existence     : unbacked_count={unbacked} (want 12), "
              f"distinct_base={r.get('distinct_base')} (want 0)")
        if unbacked < 12 or r.get("distinct_base") != 0:
            print("   hole#2 SUB-PROBE: FAIL"); rc = 1
        else:
            print("   hole#2 SUB-PROBE: PASS")
        ep_roar = base / "PD-9999-998-roar"
        (ep_roar / "06_audio").mkdir(parents=True)
        _atomic_write_json(ep_roar / "06_audio" / "audio_provenance.v001.json", _roar_ending_fixture())
        rr = evaluate(ep_roar)
        print(f"   hole#3 ending bed    : missing-omission ok={r.get('ending_bed_missing')} ; "
              f"roar-bed bad_tags={rr.get('ending_bed_bad_tags')}")
        if not r.get("ending_bed_missing") or not rr.get("ending_bed_bad_tags") or rr.get("ok"):
            print("   hole#3 SUB-PROBE: FAIL"); rc = 1
        else:
            print("   hole#3 SUB-PROBE: PASS")
        ep_uid = base / "PD-9999-997-unidentified"
        (ep_uid / "06_audio").mkdir(parents=True)
        _atomic_write_json(ep_uid / "06_audio" / "audio_provenance.v001.json",
                           _unidentified_fixture(ep_uid))
        ru = evaluate(ep_uid)
        uid = ru.get("unidentified_count", 0)
        print(f"   hole#4 unidentified  : backed junk '12345.mp3' -> unidentified_count={uid} "
              f"(want >=1); '(unidentified)' not in bases="
              f"{'(unidentified)' not in ru.get('distinct_bases', [])}; ok={ru.get('ok')}")
        if uid < 1 or "(unidentified)" in ru.get("distinct_bases", []) or ru.get("ok"):
            print("   hole#4 SUB-PROBE: FAIL"); rc = 1
        else:
            print("   hole#4 SUB-PROBE: PASS")

        # (b) GREEN FIXTURE = a genuinely good manifest -> must PASS
        ep_green = base / "PD-9999-000-greenfixture"
        (ep_green / "06_audio").mkdir(parents=True)
        _atomic_write_json(ep_green / "06_audio" / "audio_provenance.v001.json", _green_fixture(ep_green))
        g = evaluate(ep_green)
        print("\n-- GREEN FIXTURE (12 distinct real families, real files on disk, clean ending) --")
        _print_report(g)
        green_ok = (g.get("ok") is True and not g.get("skipped"))
        print(f"\nGREEN-FIXTURE: {'PASS' if green_ok else 'FAIL'}")
        if not green_ok:
            rc = 1

    # (c) REAL EPISODES: the designated TEST_EP (skips if provenance is SSD-only), plus a real
    #     episode that DOES carry provenance in-repo, to print live PASS-path numbers.
    for ep_slug in (DEFAULT_EP, "PD-2026-032-carsearch"):
        ep_dir = ROOT / "episodes" / ep_slug
        print(f"\n-- REAL EPISODE: {ep_slug} --")
        if not ep_dir.exists():
            print(f"   (episode dir not found: {ep_dir})")
            continue
        _print_report(evaluate(ep_dir))

    print(f"\n### selftest overall: {'PASS' if rc == 0 else 'FAIL'} ###")
    return rc


def main(argv: Optional[list[str]] = None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(
        description="Independent SFX-manifest gate: FAIL if the SFX palette is thin, "
                    "decoration-only, fabricated (no real file), or the ending bed roars/omitted.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--ep", default=DEFAULT_EP, help="episode slug")
    ap.add_argument("--dry-run", action="store_true",
                    help="evaluate read-only and report; never writes; always exit 0")
    ap.add_argument("--json", default=None,
                    help="atomically write the result dict to this path")
    ap.add_argument("--selftest", action="store_true",
                    help="run the RED fixture + GREEN fixture + real-episode numbers, then exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return _run_selftest()

    ep_dir = ROOT / "episodes" / args.ep
    if not ep_dir.exists():
        print(f"[ERROR] episode dir not found: {ep_dir}")
        return 1

    r = evaluate(ep_dir)
    _print_report(r)
    if args.json:
        _atomic_write_json(Path(args.json), r)
        print(f"\nwrote {args.json}")

    if args.dry_run:
        return 0
    return 0 if r.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
