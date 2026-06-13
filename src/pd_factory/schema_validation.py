from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker

class SchemaValidationError(ValueError):
    pass

def validate_data(instance: Any, schema_path: Path) -> None:
    """Validate an in-memory instance against a Draft 2020-12 schema file."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        rendered = []
        for error in errors:
            loc = ".".join(map(str, error.path)) or "<root>"
            rendered.append(f"{loc}: {error.message}")
        raise SchemaValidationError("\n".join(rendered))

def validate_json(instance_path: Path, schema_path: Path) -> None:
    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    validate_data(instance, schema_path)
