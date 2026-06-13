#!/usr/bin/env python3
"""Build a concise status report for all episode manifests."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("episodes"))
    args = parser.parse_args()
    manifests = sorted(args.root.glob("*/manifest.json")) if args.root.exists() else []
    states: Counter[str] = Counter()
    blockers: list[tuple[str, list[str]]] = []
    total_actual = 0.0
    total_estimated = 0.0
    rows: list[tuple[str, str, str, str]] = []

    for path in manifests:
        data = json.loads(path.read_text(encoding="utf-8"))
        state = data.get("state", "unknown")
        states[state] += 1
        episode_id = data.get("episode_id", path.parent.name)
        episode_blockers = data.get("blockers", [])
        if episode_blockers:
            blockers.append((episode_id, episode_blockers))
        costs = data.get("costs", {})
        total_actual += float(costs.get("actual", {}).get("amount", 0) or 0)
        total_estimated += float(costs.get("estimated", {}).get("amount", 0) or 0)
        rows.append((episode_id, state, str(len(episode_blockers)), data.get("updated_at", "")))

    print("# PD Production Status")
    print(f"\nEpisodes: {len(manifests)}")
    print(f"Estimated cost total: {total_estimated:.2f}")
    print(f"Actual cost total: {total_actual:.2f}")
    print("\n## States")
    for state, count in sorted(states.items()):
        print(f"- {state}: {count}")
    print("\n## Episodes")
    print("| Episode | State | Blockers | Updated |")
    print("|---|---:|---:|---|")
    for row in rows:
        print("| " + " | ".join(row) + " |")
    if blockers:
        print("\n## Blockers")
        for episode_id, items in blockers:
            print(f"- {episode_id}: {', '.join(map(str, items))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
