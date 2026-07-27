# -*- coding: utf-8 -*-
"""Ledger-backed theme lookup for the Asset Factory shelf — the ONLY safe selection source.

WHY THIS EXISTS
---------------
`factory_themes.theme_of()` derives a theme from the FILENAME, and the filename is
the download QUERY, not the picture. FACTORY_LABEL_AUDIT.v001 measured it:

* 40.0% of the shelf's claim-bearing theme labels are contradicted by the file's own
  recovered Pexels/Pixabay title; 17.5% are confidently mislabeled.
* By eyeball (n=40), picking blind off the shelf label gets the wrong subject ~47%
  of the time (52.5% correct). The audited/corrected theme is 70% correct.
* Confirmed: `evidence_bag` = a leather wallet, `courtroom_interior` = a bus in
  Vietnam, `prison_corridor` = the Hamburg Elbe tunnel, `server_room_red_alert` = a cat.

The audit wrote ground truth into the factory ledger — per file: `theme_recovered`
(scored from the real provider title), `theme_local` (the old filename claim),
`label_verdict` + `label_verdict_kind`, and `label_scores`. This module reads that
and nothing else, so build-path selection stops parsing filenames.

SELECTION POLICY (tiers; lower is better)
-----------------------------------------
    0  match                     title supports the theme
    1  match:dual_subject        title supports this theme and another
    2  contradiction:cross_theme RE-HOMED INTO this theme (positive evidence for it;
                                 simultaneously EXCLUDED from its wrong local theme)
    3  weak                      title neither supports nor refutes (generic slug,
                                 filename-corroborated, or an unclaimed misc label)
    4  contradiction:off_label   nothing in the title supports the label -> LAST RESORT,
                                 only with allow_off_label=True / --allow-off-label
    5  no ledger row             unauditable -> same flag as tier 4

Tier 2 outranks tier 3 because a cross_theme move required score >= 30 with a >= 25
margin (positive evidence), where `weak` is an absence of evidence. Eyeball says the
moves were right 69% of the time.

The ledger is READ-ONLY here. It is written by the ingest/retrofit tools.

Env override: PD_FACTORY_LEDGER=<path to factory.jsonl>
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LEDGER = Path(r"H:\pd-media\assets\archive\_ledger\factory.jsonl")

# tier -> human label, in the order used for reporting
TIER_NAMES = {
    0: "match",
    1: "match:dual_subject",
    2: "cross_theme->here",
    3: "weak",
    4: "off_label",
    5: "no_ledger_row",
}
TIER_DEFAULT_MAX = 3          # tiers 4/5 need allow_off_label
TIER_LAST_RESORT = 4


@dataclass(frozen=True)
class LedgerRow:
    """One audited factory file (only the label-relevant fields)."""
    manifest_id: str
    theme: str                 # == theme_recovered (canonical since label_audit_v001)
    theme_local: str
    verdict: str               # match | weak | contradiction
    kind: str                  # '' | dual_subject | cross_theme | off_label | generic_title | ...
    title: str                 # recovered provider title
    source: str

    @property
    def tier(self) -> int:
        if self.verdict == "match":
            return 1 if self.kind == "dual_subject" else 0
        if self.verdict == "contradiction":
            return 2 if self.kind == "cross_theme" else TIER_LAST_RESORT
        return 3               # weak (generic_title / filename_only / unclaimed_label)

    @property
    def tier_name(self) -> str:
        return TIER_NAMES[self.tier]


class LedgerUnavailable(RuntimeError):
    """Raised when the audited ledger cannot be read and the caller demanded it."""


class ThemeIndex:
    """manifest_id -> LedgerRow, plus theme rollups. Built once, ~0.5 s for 88,740 rows."""

    def __init__(self, rows: dict[str, LedgerRow], path: Path):
        self.rows = rows
        self.path = path

    def __len__(self) -> int:
        return len(self.rows)

    def get(self, asset: dict) -> LedgerRow | None:
        return self.rows.get(str(asset.get("id") or ""))

    def theme_of_asset(self, asset: dict) -> str | None:
        row = self.get(asset)
        return row.theme if row else None

    def tier_of(self, asset: dict, theme: str) -> int | None:
        """Tier of `asset` AS A CANDIDATE FOR `theme`, or None if it does not belong there.

        A cross_theme item is invisible under its wrong local theme (it is only
        reachable under the theme the audit re-homed it to) — that is the whole point.
        """
        row = self.get(asset)
        if row is None:
            return 5 if theme else None
        return row.tier if row.theme == theme else None

    def counts(self) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = {}
        for row in self.rows.values():
            b = out.setdefault(row.theme, {})
            b[row.tier_name] = b.get(row.tier_name, 0) + 1
            b["total"] = b.get("total", 0) + 1
        return out


def ledger_path() -> Path:
    return Path(os.environ.get("PD_FACTORY_LEDGER") or DEFAULT_LEDGER)


def load_index(path: Path | None = None, *, required: bool = False,
               quiet: bool = False) -> ThemeIndex | None:
    """Load the audited factory ledger. Returns None (after a LOUD warning) if missing.

    `required=True` raises LedgerUnavailable instead, for callers that must not
    silently regress to filename-derived themes.
    """
    p = Path(path) if path else ledger_path()
    if not p.is_file():
        msg = (f"factory ledger NOT FOUND at {p} — theme selection would fall back to "
               f"filename parsing, which FACTORY_LABEL_AUDIT.v001 measured at 40% wrong. "
               f"Set PD_FACTORY_LEDGER or mount the media drive.")
        if required:
            raise LedgerUnavailable(msg)
        if not quiet:
            print("!" * 100, file=sys.stderr)
            print(f"!! WARNING: {msg}", file=sys.stderr)
            print("!! Any footage picked in this run is UNVERIFIED — eyeball every clip.", file=sys.stderr)
            print("!" * 100, file=sys.stderr)
        return None
    rows: dict[str, LedgerRow] = {}
    bad = 0
    with p.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                bad += 1
                continue
            mid = str(r.get("manifest_id") or "")
            if not mid:
                continue
            rows[mid] = LedgerRow(
                manifest_id=mid,
                theme=str(r.get("theme") or r.get("theme_recovered") or ""),
                theme_local=str(r.get("theme_local") or r.get("original_dir_theme") or ""),
                verdict=str(r.get("label_verdict") or ""),
                kind=str(r.get("label_verdict_kind") or ""),
                title=str(r.get("title") or ""),
                source=str(r.get("source") or ""),
            )
    if bad and not quiet:
        print(f"[factory-ledger] skipped {bad} malformed line(s) in {p.name}", file=sys.stderr)
    if rows and not any(r.verdict for r in rows.values()) and not quiet:
        print("!! WARNING: factory ledger has no label_verdict fields — it predates "
              "FACTORY_LABEL_AUDIT.v001. Re-run scripts/audit_factory_labels.py measure.",
              file=sys.stderr)
    return ThemeIndex(rows, p)


def select(assets: list[dict], theme: str, index: ThemeIndex | None, *,
           allow_off_label: bool = False) -> tuple[list[dict], dict[str, int]]:
    """Rank `assets` as candidates for `theme` using the audited ledger.

    Returns (ordered candidates, per-tier counts). Each returned asset dict is a SHALLOW
    COPY carrying `_tier`, `_tier_name`, `_verdict`, `_theme_local`, `_theme_recovered`
    and `_title` (`_theme_local` is the OLD filename claim — label sheets with
    `_theme_recovered`), so
    callers can label a contact sheet without re-reading the ledger. Original manifest
    dicts are never mutated. Stable within a tier (manifest order preserved).

    With `index is None` (ledger missing) this degrades to filename-derived themes and
    marks every item tier 5 / `no_ledger_row` so the caller can see the run is unverified.
    """
    max_tier = 5 if allow_off_label else TIER_DEFAULT_MAX
    tiers: dict[int, list[dict]] = {}
    counts: dict[str, int] = {}
    if index is None:
        from factory_themes import theme_of  # local import: fallback path only
        for a in assets:
            if theme_of(a.get("subtype"), a.get("type")) != theme:
                continue
            item = dict(a, _tier=5, _tier_name="no_ledger_row", _verdict="unaudited",
                        _theme_local=theme, _theme_recovered=theme, _title="")
            tiers.setdefault(5, []).append(item)
        # graceful degradation: still return the filename-derived pick (there is no better
        # source available), but every item is marked unaudited and the caller has already
        # printed the missing-ledger banner.
        counts["no_ledger_row"] = len(tiers.get(5, []))
        return tiers.get(5, []), counts

    for a in assets:
        row = index.get(a)
        if row is None:
            tier, name, verdict, local, title = 5, TIER_NAMES[5], "no_ledger_row", "", ""
            # an unauditable file is only a candidate for the theme its filename claims
            from factory_themes import theme_of
            if theme_of(a.get("subtype"), a.get("type")) != theme:
                continue
        else:
            if row.theme != theme:
                continue
            tier = row.tier
            name = row.tier_name
            verdict = f"{row.verdict}:{row.kind}" if row.kind else row.verdict
            local, title = row.theme_local, row.title
        counts[name] = counts.get(name, 0) + 1
        if tier > max_tier:
            continue
        tiers.setdefault(tier, []).append(
            dict(a, _tier=tier, _tier_name=name, _verdict=verdict,
                 _theme_local=local, _theme_recovered=theme, _title=title))
    ordered = [x for t in sorted(tiers) for x in tiers[t]]
    return ordered, counts


def format_counts(counts: dict[str, int]) -> str:
    order = [TIER_NAMES[i] for i in range(6)]
    parts = [f"{k}={counts[k]}" for k in order if counts.get(k)]
    return " ".join(parts) if parts else "none"


def main() -> int:
    """CLI: inspect the audited theme tree (`python scripts/factory_ledger_themes.py`)."""
    sys.stdout.reconfigure(encoding="utf-8")
    idx = load_index()
    if idx is None:
        return 2
    print(f"{len(idx)} audited factory rows from {idx.path}")
    counts = idx.counts()
    hdr = ["match", "match:dual_subject", "cross_theme->here", "weak", "off_label"]
    print(f"{'theme':<22}{'total':>8}" + "".join(f"{h:>20}" for h in hdr))
    for theme in sorted(counts, key=lambda t: -counts[t]["total"]):
        b = counts[theme]
        print(f"{theme:<22}{b['total']:>8}" + "".join(f"{b.get(h, 0):>20}" for h in hdr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
