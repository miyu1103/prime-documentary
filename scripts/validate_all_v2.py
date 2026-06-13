#!/usr/bin/env python3
from __future__ import annotations
import ast
import json
import pathlib
import subprocess
import sys
from jsonschema import Draft202012Validator
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

def check_json() -> None:
    for path in ROOT.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if path.name.endswith("schema.json"):
                Draft202012Validator.check_schema(data)
        except Exception as exc:
            ERRORS.append(f"JSON {path.relative_to(ROOT)}: {exc}")

def check_yaml() -> None:
    for pattern in ("*.yaml", "*.yml"):
        for path in ROOT.rglob(pattern):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:
                ERRORS.append(f"YAML {path.relative_to(ROOT)}: {exc}")

def check_python() -> None:
    for path in ROOT.rglob("*.py"):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except Exception as exc:
            ERRORS.append(f"PYTHON {path.relative_to(ROOT)}: {exc}")

def check_required() -> None:
    required = [
        "CLAUDE.md", "BOOTSTRAP_PROMPT.txt", "START_HERE.md",
        "PD_AUTONOMOUS_STUDIO_MASTER_SPEC_V2.md",
        "config/pd.v2.example.yaml", "schemas/pd-common-v2.schema.json",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            ERRORS.append(f"MISSING {rel}")

def run_pytest() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"], cwd=ROOT,
        text=True, capture_output=True, check=False,
        env={**__import__('os').environ, "PYTHONPATH": str(ROOT / "src")},
    )
    if result.returncode:
        ERRORS.append("PYTEST:\n" + result.stdout + result.stderr)

def main() -> int:
    check_json(); check_yaml(); check_python(); check_required(); run_pytest()
    if ERRORS:
        print("VALIDATION FAILED")
        print("\n\n".join(ERRORS))
        return 1
    print("VALIDATION PASSED")
    print(f"JSON files: {sum(1 for _ in ROOT.rglob('*.json'))}")
    print(f"YAML files: {sum(1 for _ in ROOT.rglob('*.yaml')) + sum(1 for _ in ROOT.rglob('*.yml'))}")
    print(f"Python files: {sum(1 for _ in ROOT.rglob('*.py'))}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
