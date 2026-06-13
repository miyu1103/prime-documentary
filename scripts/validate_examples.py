#!/usr/bin/env python3
"""Validate Prime Documentary example artifacts against JSON Schemas."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"

CASES: list[tuple[Path, Path, bool]] = [
    (EXAMPLES / "episode/manifest.json", SCHEMAS / "episode-manifest.schema.json", False),
    (EXAMPLES / "episode/00_topic/topic.v001.json", SCHEMAS / "topic.schema.json", False),
    (EXAMPLES / "episode/01_research/sources.v001.json", SCHEMAS / "source.schema.json", True),
    (EXAMPLES / "episode/01_research/claims.v001.json", SCHEMAS / "claim-ledger.schema.json", False),
    (EXAMPLES / "episode/03_script/script.annotated.v001.json", SCHEMAS / "script-annotated.schema.json", False),
    (EXAMPLES / "episode/04_scenes/scene_plan.v001.json", SCHEMAS / "scene-plan.schema.json", False),
    (EXAMPLES / "episode/approvals/APR-0001.json", SCHEMAS / "approval.schema.json", False),
    (EXAMPLES / "job.json", SCHEMAS / "job.schema.json", False),
    (EXAMPLES / "analytics-snapshot.json", SCHEMAS / "analytics-snapshot.schema.json", False),
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_one(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    return [f"{label}: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]


def main() -> int:
    failures: list[str] = []
    for example_path, schema_path, is_list in CASES:
        instance = load_json(example_path)
        schema = load_json(schema_path)
        if is_list:
            if not isinstance(instance, list):
                failures.append(f"{example_path}: expected a JSON array")
                continue
            for index, item in enumerate(instance):
                failures.extend(validate_one(item, schema, f"{example_path}[{index}]"))
        else:
            failures.extend(validate_one(instance, schema, str(example_path)))

    if failures:
        print("Validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(CASES)} example groups successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
