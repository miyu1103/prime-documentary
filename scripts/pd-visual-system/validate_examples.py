#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

PAIRS = [
    ('templates/pd-visual-system/scene-plan.example.json', 'schemas/scene-plan.schema.json'),
    ('templates/pd-visual-system/asset-record.example.json', 'schemas/asset-record.schema.json'),
    ('templates/pd-visual-system/generation-request.example.json', 'schemas/generation-request.schema.json'),
    ('templates/pd-visual-system/review-record.example.json', 'schemas/review-record.schema.json'),
    ('templates/pd-visual-system/benchmark-shot.example.json', 'schemas/benchmark-shot.schema.json'),
    ('docs/pd-visual-system/PHASE_STATE.json', 'schemas/phase-state.schema.json'),
]

root = Path(__file__).resolve().parents[2]
for instance_rel, schema_rel in PAIRS:
    instance = json.loads((root / instance_rel).read_text(encoding='utf-8'))
    schema = json.loads((root / schema_rel).read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator(schema).validate(instance)
    print(f'OK {instance_rel}')
