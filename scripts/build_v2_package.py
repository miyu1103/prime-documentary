#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/(ROOT.name+'.zip')
EXCLUDE={OUT.resolve()}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.resolve() not in EXCLUDE and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts:
            z.write(p,p.relative_to(ROOT.parent))
print(OUT)
print(hashlib.sha256(OUT.read_bytes()).hexdigest())
