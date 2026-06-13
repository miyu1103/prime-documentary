#!/usr/bin/env python3
"""Run the real Miranda research adapter and write 01_research artifacts.

Usage (from repo root):
    py -3.11 scripts/run_research.py            # live fetch (needs COURTLISTENER_TOKEN)
    py -3.11 scripts/run_research.py --dry-run  # preflight only, no network, no writes

Token: put `COURTLISTENER_TOKEN=...` in a git-ignored `.env` at the repo root, or set
it in the environment. Oyez needs no token. Re-runs reuse the on-disk fetch cache
(idempotent: no duplicate network calls, no duplicate budget spend).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from pd_factory.budget import BudgetLedger, BudgetPolicy  # noqa: E402
from pd_factory.episode_repo import EpisodeRepo, next_revision  # noqa: E402
from pd_factory.idempotency import make_idempotency_key  # noqa: E402
from pd_factory.provenance import make_provenance, now_iso  # noqa: E402
from pd_factory.research import preflight  # noqa: E402
from pd_factory.research.build import (  # noqa: E402
    COURTLISTENER_CLUSTER_API,
    OYEZ_CASE_URL,
    acquire,
    build_claim_ledger,
    build_research_plan,
    build_sources,
)
from pd_factory.schema_validation import validate_data  # noqa: E402

SCHEMA_DIR = REPO_ROOT / "schemas"
CONFIG_REVISION = "0002"  # bump when adapter logic/grading changes (idempotency input)


def load_env_token() -> str | None:
    if os.environ.get("COURTLISTENER_TOKEN"):
        return os.environ["COURTLISTENER_TOKEN"]
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            if key.strip() == "COURTLISTENER_TOKEN":
                return value.strip().strip('"').strip("'") or None
    return None


def _write(repo: EpisodeRepo, *, stem: str, revision: str, data, episode_id: str, input_revs: dict[str, str]):
    key = make_idempotency_key(
        stage=stem,
        episode_id=episode_id,
        input_revisions=[f"{k}:{v}" for k, v in input_revs.items()],
        config_revision=CONFIG_REVISION,
        provider_profile="research:miranda-adapter",
    )
    prov = make_provenance(
        artifact_id=f"{episode_id}:{stem}:{revision}",
        artifact_type=stem,
        revision=revision,
        producer="research:miranda-adapter",
        input_revisions=input_revs,
        idempotency_key=key,
        checksum="pending",
        cost_amount=0.0,
        cost_currency="USD",
    )
    uri, checksum = repo.write_artifact(
        folder="01_research", stem=stem, revision=revision, data=data, provenance=prov
    )
    # Rewrite provenance with the authoritative checksum (mirror pipeline behavior).
    meta_path = repo.root / "01_research" / f"{stem}.{revision}.meta.json"
    meta_path.write_text(
        json.dumps({**prov, "checksum": checksum}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return uri, checksum


def main() -> int:
    ap = argparse.ArgumentParser(description="Miranda real-research adapter")
    ap.add_argument("--episode-dir", default=str(REPO_ROOT / "episodes" / "PD-2026-001-miranda"))
    ap.add_argument("--cache-dir", default=str(REPO_ROOT / "cache" / "research"))
    ap.add_argument("--dry-run", action="store_true", help="preflight only; no network, no writes")
    args = ap.parse_args()

    episode_dir = Path(args.episode_dir)
    cache_dir = Path(args.cache_dir)
    accessed_at = now_iso()

    if args.dry_run:
        print("DRY-RUN: would fetch (after preflight):")
        for url in (COURTLISTENER_CLUSTER_API, OYEZ_CASE_URL):
            host = preflight(url)  # raises if not allowlisted
            print(f"  [{host}] {url}")
        print("No network call and no artifacts written.")
        return 0

    token = load_env_token()
    if not token:
        print(
            "WARNING: no COURTLISTENER_TOKEN found (.env or env). CourtListener will be "
            "fetched unauthenticated and may be rate-limited; Oyez is unaffected.",
            file=sys.stderr,
        )

    repo = EpisodeRepo(episode_dir)
    manifest = repo.read_manifest()
    episode_id = manifest["episode_id"]
    revision = next_revision(repo.existing_revisions("01_research", "claims"))

    # Budget is in *requests* (these APIs are free but rate-limited).
    budget = BudgetLedger(BudgetPolicy(soft_limit=6.0, hard_limit=12.0))

    cl, oyez = acquire(
        accessed_at=accessed_at, token=token, cache_dir=cache_dir, budget=budget
    )

    sources = build_sources(cl, oyez)
    plan = build_research_plan(episode_id, revision)
    claims = build_claim_ledger(episode_id, revision, sources)

    # Validate before any write (rules/15).
    validate_data(plan, SCHEMA_DIR / "research-plan.schema.json")
    for src in sources:
        validate_data(src, SCHEMA_DIR / "source.schema.json")
    validate_data(claims, SCHEMA_DIR / "claim-ledger.schema.json")

    _write(repo, stem="research_plan", revision=revision, data=plan, episode_id=episode_id, input_revs={"topic": manifest["active_revisions"].get("topic", "v001")})
    _write(repo, stem="sources", revision=revision, data=sources, episode_id=episode_id, input_revs={"research_plan": revision})
    _write(repo, stem="claims", revision=revision, data=claims, episode_id=episode_id, input_revs={"sources": revision, "research_plan": revision})

    # Update manifest revisions + state (mechanical advance; approval gate unchanged).
    manifest["active_revisions"].update(
        {"research_plan": revision, "sources": revision, "claims": revision}
    )
    qc_status = claims["qc"]["status"]
    if qc_status == "pass":
        manifest["state"] = "research_ready"
    else:
        manifest["state"] = "researching"
        msg = f"Research QC status={qc_status}: {claims['qc']['findings']}"
        if msg not in manifest.get("warnings", []):
            manifest.setdefault("warnings", []).append(msg)
    repo.write_manifest(manifest)

    repo.append_event(
        {
            "episode_id": episode_id,
            "event": "research_acquired",
            "stage": "claims",
            "revision": revision,
            "cl_status": cl.status,
            "cl_from_cache": cl.from_cache,
            "oyez_status": oyez.status,
            "oyez_from_cache": oyez.from_cache,
            "qc_status": qc_status,
            "budget_committed_requests": budget.committed,
            "actor": "local-claude-code",
        }
    )

    # Report (rules/17: exact results, no secrets).
    print("=== Miranda research acquired ===")
    print(f"revision           : {revision}")
    print(f"CourtListener      : HTTP {cl.status}  cache={cl.from_cache}  hash={cl.content_hash}")
    print(f"Oyez               : HTTP {oyez.status}  cache={oyez.from_cache}  hash={oyez.content_hash}")
    print(f"sources            : {len(sources)}  -> {[s['source_id'] for s in sources]}")
    print(f"claims             : {len(claims['claims'])}  (critical_supported={claims['qc']['critical_supported']})")
    print(f"research QC status : {qc_status}")
    if claims["qc"]["findings"]:
        for f in claims["qc"]["findings"]:
            print(f"  - finding: {f}")
    print(f"budget (requests)  : committed={budget.committed} / hard={budget.policy.hard_limit}")
    print(f"manifest state     : {manifest['state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
