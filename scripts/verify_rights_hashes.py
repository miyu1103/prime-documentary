#!/usr/bin/env python3
"""Verify rights_manifest content hashes against real files, and report missing/mismatch.

Read-only. Resolves remotion/public/* (repo-relative) and artifact://episodes/<id>/* (media SSD
from config/storage.local.json). Prints, per asset: OK / MISMATCH / MISSING / NO-HASH (+ computed).
Usage: py -3.11 scripts/verify_rights_hashes.py episodes/PD-2026-002-gideon/09_package/rights_manifest.v001.json
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def media_root() -> Path:
    cfg = json.loads((REPO / "config" / "storage.local.json").read_text(encoding="utf-8"))
    return Path(cfg["roots"]["media"]["path"])


def resolve(uri: str) -> Path | None:
    if uri.startswith("artifact://"):
        rest = uri[len("artifact://"):]
        return media_root() / rest  # artifact://episodes/<id>/... -> <media>/episodes/<id>/...
    # repo-relative (e.g. remotion/public/mj/x.png)
    return REPO / uri


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    mani = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    ok = mismatch = missing = nohash = 0
    for a in mani["assets"]:
        aid, uri = a["asset_id"], a["file"]
        declared = (a.get("content_hash") or "").replace("sha256:", "")
        p = resolve(uri)
        if p is not None and p.is_dir():
            # directory pointer (narration draft folder) -> hash the master instead
            m = media_root() / "episodes" / mani["episode_id"] / "06_voice" / "master" / "vc_master_v001.mp3"
            if m.exists():
                print(f"{aid}: NARRATION (dir {uri}) -> master vc_master_v001.mp3 sha256:{sha256(m)}")
                nohash += 1
                continue
        if p is None or not p.exists():
            print(f"{aid}: MISSING  {uri}")
            missing += 1
            continue
        actual = sha256(p)
        if not declared:
            print(f"{aid}: NO-HASH  computed sha256:{actual}  ({uri})")
            nohash += 1
        elif declared == actual:
            print(f"{aid}: OK       {uri}")
            ok += 1
        else:
            print(f"{aid}: MISMATCH declared {declared[:16]}.. actual {actual[:16]}..  ({uri})")
            mismatch += 1
    print(f"\nsummary: OK={ok} MISMATCH={mismatch} MISSING={missing} NO-HASH={nohash}  total={len(mani['assets'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
