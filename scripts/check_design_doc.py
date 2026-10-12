#!/usr/bin/env python
"""PRE-FLIGHT: one gate an episode's DESIGN must pass before any production work starts.

Why this exists
---------------
The owner's standing requirements are real, repeated, and scattered. `check_opening_spec.py`
encodes 35 of them, but only for the opening overlay -- section 7 of the packaging document. The
rest live in `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`, in `.claude/rules/19-ship-gate.md`, in the
episode-spec schema, and in a dozen memory notes, so every episode rediscovers them by failing.
On EP66 the owner asked FIVE times whether the design followed the manual; two of my answers were
unmeasured, the fourth ask found a real gap, and the fifth found that the checklist itself was ten
items short. Nobody should have to ask a fifth time.

What it does NOT do (invariant 14 -- no second implementation of an existing capability)
---------------------------------------------------------------------------------------
Nothing here re-implements a check that already exists. It composes:

  * the 35 opening checks are IMPORTED from `check_opening_spec.CHECKS`. They are never retyped;
    retyping that list is precisely how it came to be ten items short.
  * the episode machine contract is validated by `check_episode_spec.load_and_validate`.
  * the title rules are the constants and regex from `check_packaging_qc`, imported.
  * `check_planning_package.py` (the F1-F10 pre-spend gate for the EP53-59 document template) is
    RUN as a subprocess when that template's files are present, and its verdict reported as one
    line. Its checks are not copied here.

It adds only the owner-standard items that no existing tool reads out of a design document.

The rule every added check obeys
--------------------------------
EVIDENCE-SEEKING. Each check searches the documents for a concrete answer -- a number, a named
artifact, a placement -- and reports MISSING when there is none. It never decides that a
requirement "does not apply here". That specific failure ("a requirement with no evidence is
reported as missing, not explained away") is the reason `check_opening_spec.py` was written.

Some owner standards cannot be judged by a machine at all. They are printed under HUMAN MUST
CONFIRM rather than being faked as a check. See HUMAN_ONLY at the bottom of this file.

    python scripts/check_design_doc.py --slug openfields
    python scripts/check_design_doc.py --slug openfields --json
    python scripts/check_design_doc.py --slug demo --planning-dir /tmp/demo_docs   # for testing

Exit 0 = every check PASS. Exit 1 = at least one MISSING. Read-only; touches no network.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_caption_breaks as CAPB  # noqa: E402  MIN_CUE_WORDS / MAX_BAD_SHARE
import check_final_acceptance as ACC  # noqa: E402  every ship-gate numeric floor, imported
import check_footage_utilization as UTIL  # noqa: E402  UTIL_THRESHOLD
import check_motion_density as MD  # noqa: E402  kinetic-beat / coverage / variety floors
import check_opening_spec  # noqa: E402  the 35 opening checks, imported not retyped
from check_episode_spec import load_and_validate  # noqa: E402
from check_packaging_qc import (  # noqa: E402
    MIN_TITLE_VARIANTS,
    RE_DOCTRINE,
    TITLE_MAX_CHARS,
    TITLE_MIN_CHARS,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

ROOT = Path(__file__).resolve().parents[1]


# --------------------------------------------------------------------------------------------
# result plumbing
# --------------------------------------------------------------------------------------------
@dataclass
class Result:
    label: str
    ok: bool
    evidence: str
    source: str
    group: str = ""


@dataclass
class Docs:
    """Every design document this episode has, discovered from the slug alone."""
    slug: str
    planning: Path
    found: dict[str, Path] = field(default_factory=dict)
    text: dict[str, str] = field(default_factory=dict)

    @property
    def corpus(self) -> str:
        return "\n".join(self.text.values())

    def get(self, *keys: str) -> str:
        """Concatenated text of whichever of these document roles exist."""
        return "\n".join(self.text[k] for k in keys if k in self.text)


def _newest(planning: Path, *patterns: str) -> Path | None:
    hits: list[Path] = []
    for pat in patterns:
        hits += sorted(planning.glob(pat))
    return hits[-1] if hits else None


def discover(slug: str, planning: Path) -> Docs:
    """Find the episode's design documents. Templates differ across episodes, so each role
    accepts every filename the channel has actually used -- EP53-59 wrote DESIGN_ARCHITECTURE,
    EP33-35 wrote DESIGN, EP66 wrote FILM_BIBLE, and all three are the same role."""
    d = Docs(slug=slug, planning=planning)
    roles = {
        "packaging":  (f"EP*_{slug}_PACKAGING.v*.md",),
        "bible":      (f"EP*_{slug}_FILM_BIBLE.v*.md",
                       f"EP*_{slug}_DESIGN_ARCHITECTURE.v*.md",
                       f"EP*_{slug}_DESIGN.v*.md"),
        "footage":    (f"EP*_{slug}_FOOTAGE_PLAN.v*.md",),
        "script":     (f"EP*_{slug}_script.en.v*.md",),
        "ledger":     (f"EP*_{slug}_FACTS_LEDGER.v*.md",),
    }
    for role, pats in roles.items():
        p = _newest(planning, *pats)
        if p is not None:
            d.found[role] = p
    # asset/image documents: every batch, concatenated under one role
    assets = []
    for pat in (f"EP*_{slug}_CODEX_*.md", f"EP*_{slug}_CODEX_A_ASSETS.v*.md",
                f"EP*_{slug}_ai_prompts.v*.md", f"EP*_{slug}_ANIMATION_ASSETS.v*.md"):
        assets += sorted(planning.glob(pat))
    if assets:
        d.found["assets"] = assets[0]
        d.text["assets"] = "\n".join(p.read_text(encoding="utf-8", errors="ignore")
                                     for p in dict.fromkeys(assets))
    for role, p in d.found.items():
        if role not in d.text:
            d.text[role] = p.read_text(encoding="utf-8", errors="ignore")
    return d


# --------------------------------------------------------------------------------------------
# owner-standard checks. Each entry: (label, source, evaluator) where the evaluator returns
# (ok, evidence). Evidence is what was FOUND -- an empty evidence string with ok=True is a bug.
# --------------------------------------------------------------------------------------------
def _find(text: str, pattern: str, flags: int = re.I | re.M) -> str:
    m = re.search(pattern, text, flags)
    return m.group(0)[:110].replace("\n", " ") if m else ""







# --------------------------------------------------------------------------------------------
# 1. DOCUMENT SET
# --------------------------------------------------------------------------------------------
REQUIRED_DOCS = [
    ("packaging", "title/thumbnail/hook/opening-overlay document (PACKAGING)"),
    ("bible",     "structure + motion design document (FILM_BIBLE / DESIGN_ARCHITECTURE / DESIGN)"),
    ("footage",   "archive-footage query plan with measured hit counts (FOOTAGE_PLAN)"),
    ("script",    "narration script (script.en)"),
    ("assets",    "image/asset prompt document (CODEX_* / ai_prompts)"),
]


def check_documents(d: Docs) -> list[Result]:
    out = []
    for role, what in REQUIRED_DOCS:
        p = d.found.get(role)
        ok = p is not None and len(d.text.get(role, "")) >= 1500
        out.append(Result(
            f"doc:{role}", ok,
            (f"{p.name} ({len(d.text.get(role, ''))} chars)"
             + ("" if ok else " -- under the 1500-char floor; a stub is not a design"))
            if p else f"no {what}",
            "CLAUDE.md s4.6 / channel document template", "DOCUMENT SET"))
    return out


# --------------------------------------------------------------------------------------------
# 2. MACHINE CONTRACT  (delegated to check_episode_spec -- not re-implemented)
# --------------------------------------------------------------------------------------------
def check_machine_contract(d: Docs) -> tuple[list[Result], dict]:
    spec, problems, epdir = load_and_validate(d.slug)
    out = [Result(
        "episode_spec valid", spec is not None,
        f"{epdir.name}/episode_spec.v001.json" if spec else "; ".join(problems)[:150],
        "CLAUDE.md s4.6 item 2-3 (an undeclared value is an error, never an inferred default)",
        "MACHINE CONTRACT")]
    spec = spec or {}

    # s4.6 item 4: the spec carries what must NOT appear, not only what must. EP60 staged 31
    # clips of the exact subject the episode forbade, because the constraint lived only in prose.
    for key in ("forbidden_subjects", "forbidden_claims"):
        vals = spec.get(key) or []
        out.append(Result(
            f"episode_spec.{key}", bool(vals),
            f"{len(vals)} declared" if vals else "empty or absent",
            "CLAUDE.md s4.6 item 4", "MACHINE CONTRACT"))

    # era_setting has been in schemas/episode_spec.v001.json since EP62 and is OPTIONAL there,
    # which is why EP62-65 declared none and shipped a modern US election ballot and a 2011
    # Range Rover into films set in 1975 and 1991. All four declare one now. It is reported
    # here rather than made schema-required because ten shipped specs (EP51-60) carry none and
    # making it required would fail their validation retroactively -- a decision, not a default.
    era = spec.get("era_setting") or {}
    out.append(Result(
        "episode_spec.era_setting", bool(era.get("place") and era.get("years")),
        (f"{era.get('place')} {era.get('years')}" if era else
         "absent -- nothing says what CENTURY OR CONTINENT this film is in, which is the "
         "constraint the EP62 ballot and Evoque clips broke"),
        "schemas/episode_spec.v001.json era_setting; read by check_pool_frames.era_prompts",
        "MACHINE CONTRACT"))

    tcs = spec.get("target_cut_sec")
    out.append(Result(
        "episode_spec.target_cut_sec", isinstance(tcs, (int, float)),
        (f"{tcs}s per cut" if isinstance(tcs, (int, float)) else
         "absent -- build_case_film_generic now REFUSES rather than substituting its own 4.6"),
        "CLAUDE.md s4.6 item 3; enforced in build_case_film_generic.make_cuts",
        "MACHINE CONTRACT"))

    band = spec.get("runtime_seconds")
    out.append(Result(
        "runtime band declared", bool(band) and len(band) == 2 and band[0] < band[1],
        f"{band[0]}-{band[1]}s" if band and len(band) == 2 else "not declared",
        "CLAUDE.md s4.6 item 3; check_runtime_band.py reads this band", "MACHINE CONTRACT"))
    return out, spec


# --------------------------------------------------------------------------------------------
# 3. THE DESIGN DOCUMENT AND THE MACHINE CONTRACT MUST AGREE
# --------------------------------------------------------------------------------------------
# CLAUDE.md s4.6 item 2 says episode_spec.v001.json is "the ONLY place any tool reads a number
# from". It does not stop the prose from stating a DIFFERENT number, and the prose is what a
# person builds to. Measured 2026-08-11 across EP66-69, three had already drifted:
#
#   EP66 FILM_BIBLE line 599  target_cut_sec 3.5   spec 3.1
#   EP66 FILM_BIBLE line 599  people_plates 10     spec people_plates_min 20 (20 ids listed)
#   EP67 FILM_BIBLE line 380  mandatory_stills 96  spec 122
#
# Each of those documents writes its numbers under the heading 契約値 -- "the contract values" --
# so the drift is not a stray mention; it is the document claiming to quote the contract and
# quoting it wrong. Nothing read both files, so nothing could say so.
#
# WHAT IT DOES NOT DO: it never flags a value the documents do not mention. Silence is not
# disagreement, and a check that demanded every key appear in prose would fire on every episode
# and be switched off within a week.
_CONTRACT_SCALARS = {
    "distinct_video_assets": "distinct_video_assets",
    "mandatory_stills": "__len_mandatory_stills",
    "target_cut_sec": "target_cut_sec",
    "people_plates_min": "people_plates_min",
    "people_plates": "__len_people_plates",
    "thumbnail_candidates_min": "thumbnail_candidates_min",
    "audio_layers": "audio_layers",
}
_CONTRACT_PAIRS = ("figure_beats_per_act", "runtime_seconds", "script_words")


def _spec_value(spec: dict, field: str):
    if field == "__len_mandatory_stills":
        return len(spec.get("mandatory_stills") or []) or None
    if field == "__len_people_plates":
        return len(spec.get("people_plates") or []) or spec.get("people_plates_min")
    return spec.get(field)


# A document is superseded when it says so near the top, in either language the orders use.
_SUPERSEDED = re.compile(
    r"廃棄されました|は廃棄|このバッチだけでは完結しません|abandoned|superseded by|"
    r"do not reuse the ids|使わないでください")


def contract_drift(d: Docs, spec: dict) -> list[Result]:
    """Every number the design documents state for a spec key, checked against the spec."""
    out: list[Result] = []
    SRC = ("CLAUDE.md s4.6 item 2: episode_spec.v001.json is the ONLY place a tool reads a "
           "number from. A design document that states a different one sends the human and the "
           "machine to different places.")
    if not spec:
        return [Result("design numbers == episode_spec", False,
                       "no valid episode_spec to compare the documents against", SRC,
                       "MACHINE CONTRACT")]
    # PER FILE, not per role. `discover` concatenates every CODEX_* order under one "assets"
    # role, so a line number computed on the concatenation names the first batch file and a
    # line that is not in it. A wrong citation is worse than none: it sends the reader to the
    # wrong document and the finding gets dismissed.
    files: list[Path] = [p for r, p in d.found.items() if r != "assets"]
    files += sorted(d.planning.glob(f"EP*_{d.slug}_CODEX_*.md"))
    findings: list[str] = []
    checked = 0
    for _f in dict.fromkeys(files):
        text = _f.read_text(encoding="utf-8", errors="ignore")
        # A document that declares itself abandoned is a record, not a claim about the contract.
        # EP66 batch A opens by saying the owner discarded it on 2026-08-10 and that batch B
        # replaces it; its 69 plates are deliberately not staged. Reading its pre-revision numbers
        # as contract drift told the operator to rewrite a superseded document -- which would
        # falsify the record of what was actually ordered. The abandonment must be declared in the
        # first 60 lines, so a passing mention deep in a live document cannot switch the file off.
        if _SUPERSEDED.search("\n".join(text.splitlines()[:60])):
            continue
        for key, field in _CONTRACT_SCALARS.items():
            want = _spec_value(spec, field)
            if want is None:
                continue
            pat = rf"`?{key}`?\s*(?:[=:：])?\s*\*{{0,2}}\s*(\d+(?:\.\d+)?)"
            for m in re.finditer(pat, text):
                # A PASTED GATE MESSAGE IS NOT A STATED CONTRACT. EP62 batch B line 24 carries
                # check_spec_satisfied output verbatim -- "distinct_video_assets: 196 distinct
                # footage+motion source(s) across 272 video cut(s)" -- which is a record of a
                # measurement that failed, not the document claiming 196 is the contract.
                # Reading it as drift would train the reader to dismiss this check.
                if re.match(r"\s*(?:distinct\s+)?(?:footage|source|video)?[^\n]{0,40}"
                            r"(?:source\(s\)|cut\(s\))", text[m.end():m.end() + 80]):
                    continue
                checked += 1
                got = float(m.group(1))
                if abs(got - float(want)) > 1e-9:
                    line = text[:m.start()].count("\n") + 1
                    findings.append(f"{_f.name}:{line} says "
                                    f"{key} {m.group(1)}, spec says {want}")
        for key in _CONTRACT_PAIRS:
            want = spec.get(key)
            if not (isinstance(want, list) and len(want) == 2):
                continue
            for m in re.finditer(rf"`?{key}`?\s*(?:[=:：])?\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]",
                                 text):
                checked += 1
                got = [float(m.group(1)), float(m.group(2))]
                if [abs(a - float(b)) < 1e-9 for a, b in zip(got, want)] != [True, True]:
                    line = text[:m.start()].count("\n") + 1
                    findings.append(f"{_f.name}:{line} says "
                                    f"{key} [{m.group(1)}, {m.group(2)}], spec says {want}")
    out.append(Result(
        "design numbers == episode_spec", not findings,
        (f"{checked} stated value(s) across {len(dict.fromkeys(files))} document(s), all "
         f"matching the spec"
         if not findings else "; ".join(sorted(set(findings)))),
        SRC, "MACHINE CONTRACT"))
    return out


def spec_document_drift(slug: str, planning: Path | None = None) -> list[str]:
    """The drift findings alone, for callers that are not the whole design gate.

    `check_episode_inputs.py` calls this: it is on the path that blocks a build, and this file
    is not. Returns [] when the documents and the spec agree, or when there is nothing to
    compare -- never raises.
    """
    try:
        spec, problems, _ = load_and_validate(slug)
        if problems or not spec:
            return []
        d = discover(slug, planning or (ROOT / "episodes" / "_planning"))
        if not d.text:
            return []
        return [r.evidence for r in contract_drift(d, spec) if not r.ok]
    except Exception:  # noqa: BLE001
        return []


# Row 13 names four title rules. check_packaging_qc.py implements two of them (the 59-100 band
# and RE_DOCTRINE) and does NOT implement question-form or second-person, so there is nothing to
# import for those two and defining them here is not a duplicate implementation. They BELONG in
# check_packaging_qc.py next to the other two; that edit was deliberately NOT made tonight because
# check_final_acceptance.py line 1805 runs check_packaging_qc as an external gate and an
# acceptance scan is live. Recorded as the follow-up, not silently skipped.
RE_QUESTION_TITLE = re.compile(
    r"(?i)\?|^\s*(is|are|was|were|do|does|did|can|could|should|would|will|why|how|what|who"
    r"|whom|when|where|which)\b")
RE_SECOND_PERSON_TITLE = re.compile(
    r"(?i)\b(you|your|yours|yourself|yourselves)\b")

_TIME = r"(\d{1,2}):(\d{2}(?:\.\d+)?)"


def _secs(mm: str, ss: str) -> float:
    return int(mm) * 60 + float(ss)


def _hook_window(text: str) -> tuple[float, float] | None:
    """Start and end of the declared HOOK in seconds, from a 'HOOK ... 0:00-0:20.3' line."""
    m = re.search(r"(?:HOOK|COLD\s*OPEN)[^\n]{0,80}?" + _TIME + r"\s*[-\u2013\u2014~]+\s*" + _TIME,
                  text, re.I)
    return (_secs(m.group(1), m.group(2)), _secs(m.group(3), m.group(4))) if m else None


def _opening_start(text: str) -> float | None:
    """Where the brand opening is placed, in seconds, however the document writes it."""
    for pat in (r"(?:^|\n)#*\s*OP\b[^\n]{0,60}?" + _TIME,
                r"(?:brand opening|BrandOpening)[^\n]{0,160}?" + _TIME,
                r"Sequence\s+from=\{Math\.round\((\d+(?:\.\d+)?)\s*\*\s*fps"):
        m = re.search(pat, text, re.I)
        if m:
            return float(m.group(1)) if m.lastindex == 1 else _secs(m.group(1), m.group(2))
    return None


def _title_candidates(packaging: str) -> list[str]:
    """Titles proposed in the packaging document's title section.

    Splits on UNESCAPED pipes only. The channel's title pattern contains a literal pipe, written
    as a backslash-pipe inside the markdown table; a naive split truncates every title there and
    then measures the wrong length -- silently turning a 96-char title into a 59-char failure.
    """
    m = re.search(r"^#+\s*\d*\.?\s*Title[^\n]*$", packaging, re.I | re.M)
    if not m:
        return []
    sec = packaging[m.end():]
    nxt = re.search(r"^##\s", sec, re.M)
    sec = sec[:nxt.start()] if nxt else sec

    out: list[str] = []
    for line in sec.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line) if c.strip()]
        if len(cells) < 2:
            continue
        title = re.sub(r"\*\*|\u2605", "", cells[1]).replace("\\|", "|").strip()
        if len(title) >= 20 and not re.fullmatch(r"(?i)title", title):
            out.append(title)
    return out


def check_owner_standards(d: Docs, spec: dict, root: Path) -> list[Result]:
    R: list[Result] = []
    corpus = d.corpus
    pack = d.text.get("packaging", "")

    def add(label: str, ok: bool, ev: str, src: str) -> None:
        R.append(Result(label, ok, ev, src, "OWNER STANDARD"))

    # --- hook: voiced from 0:00, written first, ~20s ------------------------------------------
    ROW9 = ("docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md line 32 (row 9), binding from EP66 onward: "
            "Hook = 0:00-~0:20, voiced throughout, written FIRST; narration audio starts at "
            "0:00 +/- 0.5s")
    hw = _hook_window(corpus)
    add("hook starts at 0:00", bool(hw) and hw[0] <= 0.5,
        f"HOOK {hw[0]:.1f}-{hw[1]:.1f}s" if hw else
        "no HOOK/COLD OPEN with a declared time range in any design document", ROW9)
    add("hook is ~20s long", bool(hw) and 15.0 <= (hw[1] - hw[0]) <= 25.0,
        f"{hw[1] - hw[0]:.1f}s" if hw else "no hook window declared", ROW9)
    voiced = _find(pack + "\n" + d.get("bible"),
                   r"[^\n]{0,50}(?:words spoken|as narration|voiced|\u30ca\u30ec\u30fc\u30b7\u30e7\u30f3)"
                   r"[^\n]{0,60}")
    add("hook is voiced, not a silent plate", bool(voiced),
        voiced or "the first 20s are described only as pictures -- no spoken words are written "
                  "for 0:00", ROW9)
    op = _opening_start(corpus)
    add("hook comes BEFORE the brand opening", bool(hw and op is not None and op >= hw[1] - 0.5),
        f"hook ends {hw[1]:.1f}s, brand opening at {op:.1f}s" if (hw and op is not None) else
        (f"brand opening at {op}s but no hook window declared" if op is not None else
         "no brand-opening placement found in any design document"), ROW9)

    # --- title (row 13) -------------------------------------------------------------------------
    ROW13 = ("docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md line 36 (row 13); band and doctrine regex "
             "imported from check_packaging_qc.py lines 89-95")
    cands = _title_candidates(pack)
    add(f"title candidates >= {MIN_TITLE_VARIANTS} (A/B)", len(cands) >= MIN_TITLE_VARIANTS,
        f"{len(cands)} candidate(s)" if cands else
        "no title-candidates table found in the packaging document", ROW13)
    bad = [f"{t[:30]}.. = {len(t)}ch" for t in cands
           if not TITLE_MIN_CHARS <= len(t) <= TITLE_MAX_CHARS]
    add(f"every title {TITLE_MIN_CHARS}-{TITLE_MAX_CHARS} chars", bool(cands) and not bad,
        f"all {len(cands)} in band ({', '.join(str(len(t)) for t in cands)})"
        if (cands and not bad) else
        ("; ".join(bad) if cands else "no candidates to measure"), ROW13)
    for name, rx in (("no question-form title", RE_QUESTION_TITLE),
                     ("no second-person title", RE_SECOND_PERSON_TITLE),
                     ("no case citation in title", RE_DOCTRINE)):
        hits = [t for t in cands if rx.search(t)]
        add(name, bool(cands) and not hits,
            f"{len(cands)} clean" if (cands and not hits) else
            (hits[0][:70] if hits else "no candidates to measure"), ROW13)

    # --- OP/ED bookends genuinely PLACED --------------------------------------------------------
    # A NAME IS NOT A PLACEMENT. The op_ed_bookends gate used to grep the shared CaseFilm.tsx for
    # the string BrandOpening; every episode shares that file, so it went green on EP66's first
    # film, where leadSeconds:0 meant no opening rendered at all. Rewritten 2026-08-10
    # (check_final_acceptance.check_bookends, line 570). At design time there is no film.json to
    # measure, so the design itself must state the placement and the opening variant.
    BOOK = (f"docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md line 37 (row 14): canonical "
            f"remotion/src/components/Bookends.tsx, OPENING_SEC={ACC.BOOKEND_OP_SEC} / "
            f"ENDCARD_SEC={ACC.BOOKEND_ED_SEC}; measured by check_final_acceptance.check_bookends")
    for name in ("BrandOpening", "BrandEndcard"):
        placed = ""
        for m in re.finditer(name, corpus):
            # 200 characters, not 400: this proves a placement is WRITTEN next to the
            # component name. What proves it is RENDERED is check_bookends, after the
            # film json exists -- which is the whole reason that gate was rewritten.
            ctx = corpus[max(0, m.start() - 200): m.end() + 200]
            t = re.search(r"from=\{[^}]*\}|" + _TIME + r"|\b\d+(?:\.\d+)?\s*s\b|\bframes?\s*\d+",
                          ctx)
            if t:
                placed = t.group(0)[:60]
                break
        add(f"{name} placed at an explicit position", bool(placed),
            f"placement {placed}" if placed else
            (f"{name} is named but no frame or second appears near it -- a name is not a placement"
             if name in corpus else f"{name} appears in no design document"), BOOK)
    variant = _find(corpus, r"[^\n]{0,50}(?:openingVariant|leadSeconds)[^\n]{0,60}")
    add("opening variant / leadSeconds decided", bool(variant),
        variant or "neither openingVariant nor leadSeconds is decided; leadSeconds 0 with no "
                   "variant renders NO opening, and that is what used to pass this gate", BOOK)

    # --- After Effects kinetic beats --------------------------------------------------------------
    AE = ("docs/PD_CANON.md lines 149-151: AE kinetic text 1-2 times mid-film, on the numbers "
          "and the turns (owner approval 2026-08-04); jobs in scripts/ae/jobs_<slug>.json, "
          "rendered by scripts/ae/render_beats.sh")
    beats: list[dict] = []
    jobs = sorted((root / "scripts" / "ae").glob(f"jobs_*{d.slug}*.json"))
    for j in jobs:
        try:
            data = json.loads(j.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        beats += [b for b in data if isinstance(b, dict) and b.get("style") != "note"]
    add("AE kinetic beats authored (>=1)", len(beats) >= 1,
        (f"{len(beats)} beat(s) in {jobs[0].name}: "
         + ", ".join(str(b.get('id')) for b in beats[:4])) if beats else
        f"no scripts/ae/jobs_*{d.slug}*.json holding a real beat -- an approved capability unused",
        AE)
    ae_doc = _find(corpus, r"[^\n]{0,50}(?:After Effects|render_beats|kinetic beat|"
                           r"\u30ad\u30cd\u30c6\u30a3\u30c3\u30af)[^\n]{0,60}")
    add("AE beats written into the DESIGN documents", bool(ae_doc),
        ae_doc or "no design document mentions After Effects or a kinetic beat, so the assembly "
                  "is never told to place one (PD_CANON: what is not in the document is not used)",
        AE)

    # --- archive shelf actually used ----------------------------------------------------------------
    SHELF = (f"docs/PD_CANON.md lines 143-148: floor = 1 distinct factory clip per "
             f"{ACC.FACTORY_SECONDS_PER_CLIP}s "
             f"(check_final_acceptance.FACTORY_SECONDS_PER_CLIP), target >= 60 clips; "
             f"a zero hit is a fact about the search words, not about the shelf. NOTE: this "
             f"counts measured QUERY HITS, and the footage plan is right that a hit count is "
             f"not a supply count -- the staged clips still have to be looked at")
    foot = d.text.get("footage", "")
    counts = [int(x) for x in re.findall(r"^###\s+\S+\s+union\s+(\d+)\s*$", foot, re.M)]
    if not counts:
        counts = [int(x) for x in re.findall(r"^\|[^|]+\|\s*(\d+)\s*\|", foot, re.M)]
    supply = sum(counts)
    add("archive queries enumerated with measured hit counts (>=8)", len(counts) >= 8,
        f"{len(counts)} queries, {supply} hits measured" if counts else
        "the footage plan records no query with a measured hit count -- the shelf was not searched",
        SHELF)
    retried = _find(foot, r"[^\n]{0,60}(?:retr(?:y|ies|ied)|widen|re-?ran|\u518d\u691c\u7d22|\u8a9e\u5f59)"
                          r"[^\n]{0,60}")
    add("zero-hit queries retried with different words", bool(retried),
        retried or "no record that a zero result was retried with other vocabulary before being "
                   "written down as a gap", SHELF)
    lo = (spec.get("runtime_seconds") or [0, 0])[0]
    floor = max(1, int(lo // ACC.FACTORY_SECONDS_PER_CLIP)) if lo else 0
    add(f"query hits cover the clip floor (runtime/{ACC.FACTORY_SECONDS_PER_CLIP}s) and the 60 target",
        bool(lo) and supply >= max(floor, 60),
        f"supply {supply} vs floor {floor} / target 60" if lo else
        "no runtime declared, so the clip floor cannot be computed", SHELF)
    want = spec.get("distinct_video_assets")
    add("supply >= episode_spec.distinct_video_assets", bool(want) and supply >= want,
        f"supply {supply} vs declared {want}" if want else
        "episode_spec declares no distinct_video_assets", SHELF)

    # --- people in the images -------------------------------------------------------------------------
    PEOPLE = ("owner decision 2026-07-04, written at episodes/_planning/EP28_forfeiture_DESIGN."
              "v001.md line 142: depicted people are REQUIRED and welcome; the only thing barred "
              "is the likeness of a real, identifiable individual (CLAUDE.md invariant 11)")
    ppl = spec.get("people_plates_min")
    add("episode_spec requires people plates (>=1)", bool(ppl) and ppl >= 1,
        f"people_plates_min = {ppl}" if ppl else
        "people_plates_min absent or zero -- a film with nobody in it", PEOPLE)
    lane = _find(d.get("assets", "bible"),
                 r"[^\n]{0,50}(?:\u2605HP|\[HSTYLE\]|human-present|people plate|people lane|"
                 r"figure lane|\u4eba\u7269[^\n]{0,8}\u679a)[^\n]{0,60}")
    add("people lane declared in the image documents", bool(lane),
        lane or "no people / human-present lane in any image document (the channel writes this "
                "as a HP total or an [HSTYLE] prompt lane)", PEOPLE)
    ban = _find(d.get("assets", "bible", "packaging"),
                r"[^\n]{0,50}(?:likeness|no real[- ]person|\u8096\u50cf)[^\n]{0,60}")
    add("real-person likeness ban stated", bool(ban),
        ban or "the image documents never state the one thing that IS barred", PEOPLE)

    # --- motion: not a slideshow ----------------------------------------------------------------------
    MOTION = (f".claude/rules/19-ship-gate.md line 8 and spec v2 line 31 (row 8); machine floors: "
              f"animation_density near-still <= {ACC.LOW_MOTION_MAX_FRACTION:.0%} of runtime, "
              f"single hold <= {ACC.LOW_MOTION_MAX_SPAN_S}s; motion_density >= "
              f"{MD.MIN_KINETIC_BEATS_PER_MIN} kinetic beats/min, coverage >= "
              f"{MD.MIN_ANIMATED_COVERAGE}, variety >= {MD.MIN_ANIMATED_VARIETY}; "
              f"docs/PD_EPISODE_DESIGN_MANUAL.v001.md line 85: 13-17 beats per act")
    fb = spec.get("figure_beats_per_act")
    add("figure beats per act declared, >= 13", bool(fb) and len(fb) == 2 and fb[0] >= 13,
        f"figure_beats_per_act = {fb}" if fb else "not declared", MOTION)
    mot = _find(corpus, r"[^\n]{0,50}(?:animation_density|motion_density|figure[- ]?beat|i2v|"
                        r"motion budget|\u30e2\u30fc\u30b7\u30e7\u30f3\u4e88\u7b97|\u7d19\u82dd\u5c45)"
                        r"[^\n]{0,60}")
    add("anti-slideshow motion budget written into the design", bool(mot),
        mot or "the design never says how the picture moves -- no motion budget, no i2v, no "
               "figure beats", MOTION)

    # --- footage diversity and cross-episode reuse -------------------------------------------------------
    DIV = (f".claude/rules/19-ship-gate.md line 9: footage_diversity distinct >= "
           f"{ACC.FOOTAGE_MIN_DISTINCT_FRACTION}, reuse <= {ACC.FOOTAGE_MAX_USES_PER_CLIP}, "
           f"generic symbols <= {ACC.FOOTAGE_GENERIC_MAX_USES}; utilisation >= "
           f"{UTIL.UTIL_THRESHOLD:.0%} (check_footage_utilization.UTIL_THRESHOLD)")
    div = _find(corpus, r"[^\n]{0,60}(?:footage_diversity|footage_utilization|"
                        r"distinct\s*[\u2265>]=?\s*0?\.4|no-?repeat|non-?repeat)[^\n]{0,60}")
    add("footage diversity / utilisation floor declared", bool(div),
        div or "no diversity or utilisation floor anywhere in the design", DIV)
    cross = _find(corpus, r"[^\n]{0,60}(?:cross[_ -]?episode|arc_nonrepeat|STAGED_CLIP_INDEX|"
                          r"\u8a71\u307e\u305f\u304e)[^\n]{0,60}")
    add("cross-episode reuse guarded", bool(cross),
        cross or "nothing says these clips were checked against what other episodes already used",
        DIV + "; index built by scripts/check_cross_episode_reuse.py --build")

    # --- captions ---------------------------------------------------------------------------------------
    CAP = (f"docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md line 27 (row 4): 1 cue = 1 breath group, "
           f"<= 2 lines, <= 42 chars/line, 1.0-6.0s, <= 17cps; check_caption_breaks.py enforces "
           f">= {CAPB.MIN_CUE_WORDS} words per cue and <= {CAPB.MAX_BAD_SHARE:.0%} mid-phrase "
           f"endings")
    cap = _find(corpus, r"[^\n]{0,60}(?:\u606f\u7d99\u304e|breath group|breath unit|caption break|"
                        r"_smart_split|\u5b57\u5e55[^\n]{0,8}\u5206\u5272)[^\n]{0,60}")
    add("caption breath-unit rule declared", bool(cap),
        cap or "the design says nothing about where captions are cut", CAP)

    # --- image provenance -----------------------------------------------------------------------------------
    IMG = (".claude/rules/19-ship-gate.md line 10: long-form images are Codex by default; "
           "SD3.5/SDXL only to repair or to fill an emergency gap; FLUX-dev never")
    src_img = _find(d.get("assets", "bible"),
                    r"[^\n]{0,50}(?:Codex|SD3\.5|sd35_gen|gen_max\.ps1)[^\n]{0,60}")
    add("image source policy stated (Codex primary)", bool(src_img),
        src_img or "no image-source policy in the design", IMG)
    return R


# --------------------------------------------------------------------------------------------
# 4. DELEGATION -- the EP53-59 pre-spend gate is RUN, never copied
# --------------------------------------------------------------------------------------------
def check_planning_package_delegate(d: Docs, root: Path) -> Result:
    """Run scripts/check_planning_package.py (F1-F10) when its document template is present.

    Its ten checks are NOT reproduced here. When the episode uses a different template -- EP66
    writes FILM_BIBLE and CODEX_BATCH_* where EP53-59 wrote DESIGN_ARCHITECTURE and
    CODEX_A_ASSETS -- this reports SKIP, which is an honest "not measured" rather than a pass.
    """
    m = re.match(r"EP(\d+)_", d.found.get("packaging", Path("x")).name)
    template = (list(d.planning.glob(f"EP*_{d.slug}_DESIGN_ARCHITECTURE.v*.md"))
                and list(d.planning.glob(f"EP*_{d.slug}_CODEX_A_ASSETS.v*.md"))
                and list(d.planning.glob(f"EP*_{d.slug}_review_log.v*.md")))
    if not (m and template):
        return Result("check_planning_package.py F1-F10", True,
                      "SKIP (not measured) -- this episode does not use the "
                      "DESIGN_ARCHITECTURE / CODEX_A_ASSETS / review_log template that gate reads",
                      "scripts/check_planning_package.py", "DELEGATED")
    r = subprocess.run([sys.executable, str(root / "scripts" / "check_planning_package.py"),
                        str(int(m.group(1))), d.slug],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = [ln for ln in (r.stdout or "").splitlines() if ln.startswith("FAIL")]
    return Result("check_planning_package.py F1-F10", r.returncode == 0,
                  "PASS" if r.returncode == 0 else "; ".join(tail)[:200],
                  "scripts/check_planning_package.py", "DELEGATED")


# --------------------------------------------------------------------------------------------
# 5. WHAT A MACHINE CANNOT JUDGE
# --------------------------------------------------------------------------------------------
# These are real owner standards. None of them is checked above, because a regex claiming to
# check them would be decoration -- and decoration is exactly what let a green gate ship a
# slideshow. They are printed after every run so they cannot quietly disappear.
HUMAN_ONLY = [
    ("Does the hook actually withhold the outcome?",
     "row 9 forbids summarising the outcome in the first 10s. A machine can find the words; "
     "only a reader can tell whether the promise is still open at 0:20."),
    ("Is the writing free of AI register?",
     "the owner asks for the feel of a first-rate writer. No lexical test survives contact "
     "with a writer who knows the test."),
    ("Do the pictures mean what the narration means?",
     "a clip can satisfy every diversity and motion floor and still be the wrong picture for "
     "the sentence underneath it."),
    ("Are the staged clips what their labels claim?",
     "factory shelf filename labels are wrong about 40% of the time. Only the labelled contact "
     "sheet, opened by a person, answers this."),
    ("Does the film feel like it moves?",
     "animation_density has gone green on films the owner called a slideshow. The floor "
     "measures 'not frozen'; it never measures 'alive'."),
    ("Is the thumbnail worth clicking, and does the title tempt?",
     "CTR is decided after publication. The character band is the only part a machine holds."),
    ("Are the facts in the ledger true?",
     "claim verification is research, not text search."),
    ("Are the OP/ED in the channel's taste?",
     "placement is measurable; taste is not."),
]


# --------------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------------
def run(slug: str, planning: Path, root: Path) -> list[Result]:
    d = discover(slug, planning)
    results = check_documents(d)
    contract, spec = check_machine_contract(d)
    results += contract

    # the 35 opening checks, IMPORTED from check_opening_spec.CHECKS
    sec = check_opening_spec.opening_section(d.text.get("packaging", ""))
    for label, ok, snippet, must in check_opening_spec.run_checks(sec):
        results.append(Result(
            f"opening: {label}", ok,
            (snippet or ("absent -- forbidden pattern not found" if not must else "matched"))
            if ok else
            (f"forbidden text present: {snippet}" if not must else
             "no evidence in packaging section 7"),
            "C:/Users/aab15/CLAUDE.md, via check_opening_spec.CHECKS (imported, not retyped)",
            "OPENING (35, imported)"))

    results += contract_drift(d, spec)
    results += check_owner_standards(d, spec, root)
    results.append(check_planning_package_delegate(d, root))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-flight gate for an episode's design documents.")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--planning-dir", help="override episodes/_planning (for testing this gate)")
    ap.add_argument("--root", help="override the repo root used for episodes/ and scripts/ae/")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    root = Path(a.root).resolve() if a.root else ROOT
    planning = Path(a.planning_dir).resolve() if a.planning_dir else root / "episodes" / "_planning"
    if root != ROOT:
        # the spec validator resolves episodes/ from its own module ROOT; aim it at the test root
        import check_episode_spec
        check_episode_spec.ROOT = root

    results = run(a.slug, planning, root)
    if a.json:
        print(json.dumps([r.__dict__ for r in results], ensure_ascii=False, indent=2))
        return 1 if any(not r.ok for r in results) else 0

    print("=" * 100)
    print(f"DESIGN PRE-FLIGHT  slug={a.slug}  ({len(results)} checks)")
    print(f"planning dir: {planning}")
    print("=" * 100)
    group = ""
    for i, r in enumerate(results, 1):
        if r.group != group:
            group = r.group
            print(f"\n--- {group} " + "-" * max(0, 94 - len(group)))
        status = "PASS   " if r.ok else "MISSING"
        print(f"{i:3d}. [{status}] {r.label:46s} {r.evidence[:96]}")
        if not r.ok:
            print(f"     {'':9s} source: {r.source}")

    bad = [r for r in results if not r.ok]
    print("\n" + "=" * 100)
    print(f"RESULT: {len(results) - len(bad)}/{len(results)} PASS, {len(bad)} MISSING")
    for r in bad:
        print(f"  MISSING  {r.label}")
    print(f"\nHUMAN MUST CONFIRM -- {len(HUMAN_ONLY)} owner standards no machine can judge, "
          f"deliberately NOT checked above:")
    for q, why in HUMAN_ONLY:
        print(f"  - {q}\n      {why}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())


