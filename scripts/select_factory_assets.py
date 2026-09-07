# -*- coding: utf-8 -*-
"""
Select candidate Asset Factory assets from assets/asset_manifest.v001.json.
Operationalizes the asset-first workflow: given a sceneType / mood / category / keyword,
return matching AF-* ids + paths so a Scene Plan / Shot Recipe can pick from the shelf
BEFORE generating anything new.

THEME SELECTION IS LEDGER-BACKED (2026-07-28, FACTORY_LABEL_AUDIT.v001)
-----------------------------------------------------------------------
`--theme` used to derive the theme from the FILENAME via `factory_themes.theme_of()`.
The filename is the download QUERY, not the picture: 40.0% of the shelf's claim-bearing
labels are contradicted by the file's own recovered provider title, and by eyeball a
builder picking blind off that label got the wrong subject ~47% of the time
(`evidence_bag` = a leather wallet, `courtroom_interior` = a bus in Vietnam,
`prison_corridor` = the Hamburg Elbe tunnel, `server_room_red_alert` = a cat).

`--theme` now reads the audited ledger (`factory_ledger_themes.py`): items are ranked
match > match:dual_subject > cross_theme-re-homed-here > weak, `cross_theme` items are
INVISIBLE under the wrong theme they used to sit in, and `off_label` items are excluded
unless you pass `--allow-off-label`. Every result — including `--query` / `--subtype`
picks — is annotated with its recovered theme, verdict and REAL provider title.

EVERY SELECTION WRITES A LABELED CONTACT SHEET. The corrected labels are 70% right,
not 100%, so the eyeball step is not optional: a selection run emits
`runs/qc/factory_selection/<stamp>__<label>/` containing `selection.v001.json` plus
`*_footage_contact_NN.png`, and exits non-zero if the sheet could not be produced.
`--no-sheet` is for scripted/plumbing use only and prints an UNREVIEWED banner.

Usage:
  python scripts/select_factory_assets.py --scene-type explanation --limit 20
  python scripts/select_factory_assets.py --category light_assets
  python scripts/select_factory_assets.py --query "smoke" --kind video
  python scripts/select_factory_assets.py --theme legal_court --kind video   # theme b-roll
  python scripts/select_factory_assets.py --theme legal_court --allow-off-label
  python scripts/select_factory_assets.py --subtype courtroom_interior
  python scripts/select_factory_assets.py --themes                           # list themes + counts
"""
from __future__ import annotations
import sys, os, json, argparse, datetime as _dt, re, subprocess

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factory_themes import theme_of  # legacy filename-derived theme (40% wrong; fallback only)
import factory_ledger_themes as flt   # audited ledger -> the real theme source

US_PLACES = (
    "united states", "u s a", "usa", "american", "america", "washington dc",
    "washington d c", "capitol hill", "white house", "supreme court of united",
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho", "illinois",
    "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine", "maryland",
    "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana",
    "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york",
    "north carolina", "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania",
    "rhode island", "south carolina", "south dakota", "tennessee", "texas", "utah",
    "vermont", "virginia", "wisconsin", "wyoming", "chicago", "los angeles",
    "san francisco", "boston", "philadelphia", "houston", "phoenix", "dallas",
    "seattle", "denver", "atlanta", "miami", "detroit", "brooklyn", "manhattan",
)

# Place names that mark an item as foreign to the cases this channel covers. Measured
# on the shelf: 226 of 3,092 legal_court titles name one of these (7.3%), and they were
# clustering at the head of the ledger, so a Wroclaw courtroom was being offered before
# the Supreme Court of the United States. Titles naming no place at all are the majority
# (82%) and are never demoted by this list.
NON_US_PLACES = (
    "poland", "polish", "wroclaw", "warsaw", "krakow", "london", "liverpool",
    "england", "britain", "british", "france", "french", "paris", "rennes",
    "germany", "german", "berlin", "munich", "italy", "italian", "rome", "milan",
    "spain", "spanish", "madrid", "barcelona", "india", "indian", "delhi", "mumbai",
    "china", "chinese", "beijing", "shanghai", "japan", "tokyo", "russia", "moscow",
    "turkey", "istanbul", "brazil", "mexico", "netherlands", "dutch", "amsterdam",
    "sweden", "norway", "denmark", "finland", "czech", "prague", "hungary",
    "budapest", "austria", "vienna", "ukraine", "kyiv", "greece", "athens",
    "portugal", "lisbon", "belgium", "brussels", "ireland", "dublin", "scotland",
    "edinburgh", "australia", "sydney", "melbourne", "canada", "toronto",
    "bulgaria", "sofia", "romania", "bucharest", "serbia", "croatia", "baghdad",
    "iraq", "iran", "tehran", "egypt", "cairo", "korea", "seoul", "thailand",
    "bangkok", "vietnam", "indonesia", "jakarta", "philippines", "manila",
    "malaysia", "singapore", "pakistan", "bangladesh", "nigeria", "kenya",
    "south africa", "argentina", "chile", "colombia", "peru", "switzerland",
    "zurich", "geneva", "israel", "jerusalem", "tel aviv",
    # Added after a Kazakh government building reached the top ten on the first run:
    # this list demotes the place names it knows and nothing else, so an unlisted
    # country still surfaces. It narrows the problem; it does not close it.
    "kazakhstan", "uzbekistan", "mongolia", "nepal", "sri lanka", "taiwan",
    "hong kong", "new zealand", "ecuador", "venezuela", "bolivia", "uruguay",
    "morocco", "tunisia", "algeria", "saudi", "dubai", "abu dhabi", "qatar",
    "lithuania", "latvia", "estonia", "slovakia", "slovenia", "belarus",
    "armenia", "azerbaijan", "iceland", "luxembourg", "malta", "cyprus",
    "kuwait", "oman", "jordan", "lebanon", "syria", "ethiopia", "ghana",
    "tanzania", "uganda", "zimbabwe", "botswana", "namibia",
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(REPO, "assets", "asset_manifest.v001.json")
SHELF = os.path.join("H:", os.sep, "pd-media", "assets")   # manifest paths are relative to here
QC_ROOT = os.path.join(REPO, "runs", "qc", "factory_selection")
SHEET_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_footage_contact_sheet.py")


def used_basenames(exempt_ep: str = "") -> set[str]:
    """Cross-episode footage fingerprint universe: the lowercased basenames of every clip already
    CUT INTO or STAGED FOR any other episode. Reuses check_arc_nonrepeat.build_universe (the same
    source of truth the arc_nonrepeat ship gate uses), so `--exclude-used` can never disagree with
    the gate. ``exempt_ep`` (slug or PD-id) is removed from the universe so an episode does not
    exclude its own already-staged clips. Returns an empty set if the arc module is unavailable
    (fail-open: staging still works, it just can't pre-filter)."""
    try:
        import check_arc_nonrepeat as arc  # local module, same scripts/ dir
    except Exception:  # noqa: BLE001 - keep the selector usable even if the gate module moves
        return set()
    from pathlib import Path
    data_dir = Path(REPO) / "remotion" / "src" / "data"
    public_dir = Path(REPO) / "remotion" / "public"
    labels: set[str] = set()
    if exempt_ep:
        resolved = arc.resolve_target_film(data_dir, exempt_ep)
        labels = resolved[2] if resolved else {exempt_ep, exempt_ep.lower(),
                                               exempt_ep.split("-")[-1].lower()}
    fp_to_eps, _ = arc.build_universe(data_dir, public_dir, labels)
    return set(fp_to_eps.keys())

# coarse category -> sceneType affinity (used until per-asset compatibleSceneTypes is enriched)
CAT_SCENE = {
    "backgrounds": ["explanation", "place_intro", "company_profile", "character_profile",
                    "problem_statement", "summary", "abstract_emotion", "chapter_title",
                    "opening_hook", "ending", "transition_bridge", "evidence_board", "quote"],
    "light_assets": ["opening_hook", "turning_point", "ending", "emotional_pause", "chapter_title",
                     "abstract_emotion", "quote"],
    "particle_assets": ["opening_hook", "emotional_pause", "abstract_emotion", "ending",
                        "silent_hold", "chapter_title"],
    "vfx_overlays": ["turning_point", "abstract_emotion", "transition_bridge", "opening_hook",
                     "emotional_pause"],
    "texture_assets": ["chapter_title", "quote", "evidence_board", "explanation", "summary"],
    "loops": ["explanation", "abstract_emotion", "transition_bridge", "data_reveal", "summary"],
}


def abs_path(asset: dict) -> str:
    return os.path.join(SHELF, str(asset.get("path", "")).replace("/", os.sep))


def annotate(hits: list[dict], index: "flt.ThemeIndex | None") -> list[dict]:
    """Attach ledger truth (`_tier*`, `_verdict`, `_theme_recovered`, `_title`) to non-theme hits."""
    out = []
    for x in hits:
        if "_tier" in x:            # already came from flt.select()
            out.append(x)
            continue
        row = index.get(x) if index else None
        if row is None:
            out.append(dict(x, _tier=5, _tier_name="no_ledger_row", _verdict="unaudited",
                            _theme_recovered=theme_of(x.get("subtype"), x.get("type")),
                            _theme_local=theme_of(x.get("subtype"), x.get("type")), _title=""))
        else:
            out.append(dict(x, _tier=row.tier, _tier_name=row.tier_name,
                            _verdict=f"{row.verdict}:{row.kind}" if row.kind else row.verdict,
                            _theme_recovered=row.theme, _theme_local=row.theme_local,
                            _title=row.title))
    return out


def sheet_label(x: dict) -> str:
    """The line burned under each contact-sheet tile: the ONLY honest description available."""
    theme = x.get("_theme_recovered") or x.get("_theme_local") or "?"
    title = (x.get("_title") or "(no recovered title)")[:44]
    return f"{x.get('_tier_name', '?')} | {theme} | {title}"


def write_selection(hits: list[dict], label: str, args, counts: dict[str, int]) -> str:
    """Write runs/qc/factory_selection/<stamp>__<label>/selection.v001.json. Returns its path."""
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "-", label).strip("-") or "selection"
    out_dir = os.path.join(QC_ROOT, f"{stamp}__{safe}")
    os.makedirs(out_dir, exist_ok=True)
    doc = {
        "schema": "pd.factory_selection.v001",
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "title": safe,
        "query": {"theme": args.theme, "subtype": args.subtype, "query": args.query,
                  "category": args.category, "kind": args.kind, "scene_type": args.scene_type,
                  "limit": args.limit, "allow_off_label": args.allow_off_label,
                  "exclude_used": args.exclude_used, "ep": args.ep},
        "label_source": "factory.jsonl (label_audit_v001)" if not args.no_ledger else "filename (UNVERIFIED)",
        "tier_counts": counts,
        "review": {"contact_sheets": [], "reviewed_by": None, "reviewed_at": None,
                   "rejected_ids": []},
        "items": [{"id": x["id"], "path": x["path"], "abs_path": abs_path(x),
                   "kind": x.get("kind"), "subtype": x.get("subtype"),
                   "tier": x.get("_tier"), "tier_name": x.get("_tier_name"),
                   "verdict": x.get("_verdict"), "theme_local": x.get("_theme_local"),
                   "theme_recovered": x.get("_theme_recovered", args.theme or ""),
                   "recovered_title": x.get("_title"), "license": x.get("license"),
                   "label": sheet_label(x)} for x in hits],
    }
    path = os.path.join(out_dir, "selection.v001.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return path


def make_sheets(selection_json: str) -> list[str]:
    """Render labeled contact sheets next to the selection JSON. Raises on failure."""
    out_dir = os.path.dirname(selection_json)
    proc = subprocess.run([sys.executable, SHEET_TOOL, "--from-json", selection_json,
                           "--out-dir", out_dir],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "").strip()[:2000])
    print(proc.stdout.rstrip())
    sheets = sorted(f for f in os.listdir(out_dir) if f.endswith(".png"))
    doc = json.load(open(selection_json, encoding="utf-8"))
    doc["review"]["contact_sheets"] = [os.path.join(out_dir, s) for s in sheets]
    with open(selection_json, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    return doc["review"]["contact_sheets"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene-type", default="")
    ap.add_argument("--category", default="")
    ap.add_argument("--theme", default="", help="AUDITED theme e.g. legal_court, crime_police, finance_money")
    ap.add_argument("--subtype", default="", help="exact subtype e.g. courtroom_interior")
    ap.add_argument("--query", default="")
    ap.add_argument("--kind", default="", help="image|video")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--in-order", action="store_true",
                    help="return ledger order instead of spreading across subtypes "
                         "(reproduces a pre-2026-08-10 selection)")
    ap.add_argument("--themes", action="store_true", help="list all themes with counts and exit")
    ap.add_argument("--allow-off-label", action="store_true",
                    help="LAST RESORT: also admit contradiction:off_label items (nothing in the "
                         "file's real title supports the theme) and files with no ledger row. "
                         "Only with a human eyeballing the contact sheet.")
    ap.add_argument("--no-ledger", action="store_true",
                    help="ignore the audited ledger and derive themes from filenames (40%% wrong). "
                         "Debug/forensics only.")
    ap.add_argument("--no-sheet", action="store_true",
                    help="skip contact-sheet generation (scripted plumbing only — the result is "
                         "UNREVIEWED and must not be shipped)")
    ap.add_argument("--exclude-used", action="store_true",
                    help="drop any clip whose basename is already used/staged by another episode "
                         "(cross-episode fingerprint universe) so a NEW episode stages FRESH-ONLY "
                         "footage and never trips the arc_nonrepeat ship gate. Prefer FRESH staging.")
    ap.add_argument("--ep", default="",
                    help="target episode slug/id exempted from --exclude-used (its own staged "
                         "clips are not treated as 'used'), e.g. PD-2026-034-rolin")
    a = ap.parse_args()

    if not os.path.exists(MAN):
        print("manifest not found:", MAN); return 2
    assets = json.load(open(MAN, encoding="utf-8")).get("assets", [])

    index = None if a.no_ledger else flt.load_index()
    if a.no_ledger:
        print("!! --no-ledger: themes derived from FILENAMES, measured 40% wrong. Not for shipping.",
              file=sys.stderr)

    used: set[str] = used_basenames(a.ep) if a.exclude_used else set()
    if a.exclude_used:
        before = len(assets)
        assets = [x for x in assets
                  if os.path.basename(x.get("path", "")).lower() not in used]
        print(f"[--exclude-used] {len(used)} cross-episode fingerprints; "
              f"dropped {before - len(assets)} already-used asset(s), {len(assets)} fresh remain.")

    if a.themes:
        import collections
        if index is not None:
            counts = index.counts()
            print(f"{len(index)} audited assets across {len(counts)} themes "
                  f"(source: {index.path}); 'usable' = match+dual+cross_theme+weak:")
            for th in sorted(counts, key=lambda t: -counts[t]["total"]):
                b = counts[th]
                usable = b["total"] - b.get("off_label", 0)
                print(f"  {b['total']:6}  {th:<22} usable={usable:<6} "
                      f"match={b.get('match', 0)} dual={b.get('match:dual_subject', 0)} "
                      f"rehomed={b.get('cross_theme->here', 0)} weak={b.get('weak', 0)} "
                      f"off_label={b.get('off_label', 0)}")
        else:
            by = collections.Counter(f"{x.get('type')}/{theme_of(x.get('subtype'), x.get('type'))}"
                                     for x in assets)
            print(f"{len(assets)} assets across {len(by)} category/theme groups "
                  f"(FILENAME-derived, UNVERIFIED):")
            for k, n in sorted(by.items()):
                print(f"  {n:6}  {k}")
        return 0

    def ok(x):
        if a.category and x.get("type") != a.category:
            return False
        if a.subtype and x.get("subtype") != a.subtype:
            return False
        if a.kind and x.get("kind") != a.kind:
            return False
        if a.query and a.query.lower() not in (x.get("subtype", "") + " " + " ".join(x.get("tags", []))).lower():
            return False
        if a.scene_type:
            st = x.get("compatibleSceneTypes") or CAT_SCENE.get(x.get("type"), [])
            if a.scene_type not in st:
                return False
        return True

    pool = [x for x in assets if ok(x)]
    counts: dict[str, int] = {}
    if a.theme:
        hits, counts = flt.select(pool, a.theme, index, allow_off_label=a.allow_off_label)
        print(f"[theme={a.theme}] ledger tiers: {flt.format_counts(counts)}"
              + ("" if a.allow_off_label else "   (off_label/no_ledger_row excluded; "
                                              "--allow-off-label to admit them)"))
    else:
        hits = annotate(pool, index)
        if index is not None and not a.allow_off_label:
            dropped = [x for x in hits if x.get("_tier", 5) >= flt.TIER_LAST_RESORT]
            hits = [x for x in hits if x.get("_tier", 5) < flt.TIER_LAST_RESORT]
            if dropped:
                print(f"[label-audit] dropped {len(dropped)} item(s) whose real provider title "
                      f"contradicts or cannot corroborate the shelf label "
                      f"(--allow-off-label to admit them)")
        for x in hits:
            counts[x["_tier_name"]] = counts.get(x["_tier_name"], 0) + 1
    if not a.in_order:
        # Ledger order is contributor order. The first fifteen legal_court "match"
        # items are AF-BG-0463..0477 and five of them are one photographer's Wroclaw
        # courtroom, so taking the head of the list is how a Polish courtroom ends up
        # standing in for an American one five times in a cut. Round-robin across
        # subtype WITHIN each tier: rank still decides who is eligible, spread decides
        # who gets picked. Same idea as stratified_sample in qc_archive_contact_sheets,
        # which round-robins across sources for the same reason.
        by_tier: dict = {}
        for x in hits:
            by_tier.setdefault(x.get("_tier", 5), []).append(x)
        spread = []
        for tier in sorted(by_tier):
            groups: dict = {}
            for x in by_tier[tier]:
                key = str(x.get("subtype") or os.path.basename(str(x.get("path", "")))
                          .split("__")[-1].rsplit(".", 1)[0])
                groups.setdefault(key, []).append(x)
            # Inside a subtype, an item whose real title names a place outside the
            # United States goes last. Not excluded -- a Bulgarian courtroom is still a
            # courtroom and a thin subtype may need it -- but this channel tells US
            # cases, so it should be reached only after the domestic and unlabelled
            # ones are used. Only explicit place names count; most titles name none.
            def _place_rank(x) -> int:
                """0 = names a US place, 1 = names none, 2 = names a foreign one.

                Promoting the domestic ones is what makes this robust; demoting the
                foreign ones alone was whack-a-mole. A country list caught Bulgaria
                and Iraq, then Kazakhstan surfaced, then Montevideo -- a city whose
                country was already on the list. Unknown foreign places now land in
                the middle, and the Supreme Court of the United States still leads.
                """
                t = str(x.get("_title") or x.get("title") or "").lower()
                if any(w in t for w in US_PLACES):
                    return 0
                return 2 if any(w in t for w in NON_US_PLACES) else 1
            for k in groups:
                groups[k].sort(key=_place_rank)
            keys = sorted(groups)
            i = 0
            while any(groups[k] for k in keys):
                k = keys[i % len(keys)]
                if groups[k]:
                    spread.append(groups[k].pop(0))
                i += 1
        hits = spread
    hits = hits[: a.limit]

    if a.json:
        print(json.dumps([{"id": x["id"], "path": x["path"], "kind": x.get("kind"),
                           "license": x.get("license"), "tier": x.get("_tier_name"),
                           "verdict": x.get("_verdict"),
                           "theme_recovered": x.get("_theme_recovered", a.theme),
                           "recovered_title": x.get("_title")}
                          for x in hits], ensure_ascii=False, indent=1))
    else:
        print(f"{len(hits)} match (of {len(pool)} after filters, {len(assets)} in shelf)")
        for x in hits:
            print(f"  {x['id']:<16} {x.get('kind','?'):<6} {x.get('_tier_name','?'):<18} "
                  f"{x.get('_theme_recovered', a.theme) or '?':<18} {x['path']}")
            print(f"  {'':<16} real title: {x.get('_title') or '(none)'}")

    if not hits:
        print("no candidates — widen the query or check the theme name (`--themes`).")
        return 0

    # ---- the eyeball step is not optional: the corrected labels are 70% right, not 100% ----
    if a.no_sheet:
        print("!" * 100, file=sys.stderr)
        print("!! --no-sheet: this selection is UNREVIEWED. The audited labels are 70% correct, "
              "not 100%.\n!! Do not stage or ship these clips without a labeled contact sheet.",
              file=sys.stderr)
        print("!" * 100, file=sys.stderr)
        return 0
    label = a.theme or a.subtype or a.query or a.category or a.scene_type or "shelf"
    sel = write_selection(hits, f"{label}-{a.kind or 'any'}", a, counts)
    try:
        sheets = make_sheets(sel)
    except Exception as exc:  # noqa: BLE001 - a missing sheet must FAIL the selection
        print(f"ERROR: contact sheet generation failed ({exc}). The selection at {sel} is "
              f"UNREVIEWED — do not stage it. Fix the sheet tool (needs Pillow + ffmpeg and the "
              f"media drive mounted) or re-run with --no-sheet and accept the risk.",
              file=sys.stderr)
        return 3
    print(f"\n[selection] {sel}")
    for s in sheets:
        print(f"[contact-sheet] {s}")
    print("目視QC必須: 各タイルの絵が theme と narration の意味に合っているか確認し、"
          "外す ID を selection.v001.json の review.rejected_ids に記録してから staging へ。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
