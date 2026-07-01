#!/usr/bin/env python
"""Validate the Asset Factory shelf registry against schemas/asset-manifest.schema.json.

Usage:
    .venv/Scripts/python.exe scripts/validate_asset_manifest.py
    .venv/Scripts/python.exe scripts/validate_asset_manifest.py assets/asset_manifest.v001.json
    .venv/Scripts/python.exe scripts/validate_asset_manifest.py --check-files   # sample on-disk existence

Checks:
  1. Structural JSON Schema validity of every entry (Draft 2020-12).
  2. Duplicate id detection (ids must be unique within the shelf).
  3. id digit-width: warns if any AF-...-NNNN number > 9999 (brief's fixed {4} pattern
     would reject it; this schema uses {4,} so it still validates -- the warning is a
     heads-up that downstream consumers assuming 4 digits need {4,} too).
  4. Rights lint (commercial-use safety): classifies each license as allowed /
     restricted / unknown. Only "allowed" assets may reach a timeline (brief sec.32,
     CLAUDE.md invariant 11 / rights). Restricted or unknown licenses are reported as
     WARNINGS -- they do not fail structural validation, but flag review before use.

Exit code: 0 = schema-valid and no duplicate ids (warnings allowed). 1 = problems.
This is read-only. It never writes, downloads, or mutates the manifest.
"""
import sys, os, json, re, argparse, collections
from jsonschema import Draft202012Validator

sys.stdout.reconfigure(encoding="utf-8")  # cp932 console safety

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MANIFEST = os.path.join(ROOT, "assets", "asset_manifest.v001.json")
SCHEMA_PATH = os.path.join(ROOT, "schemas", "asset-manifest.schema.json")
MEDIA_ROOT = os.environ.get("PD_MEDIA_ROOT", r"H:\pd-media")

# license -> commercial-use class. Canonical vocabulary (docs sec.4.3) plus the
# real stock licenses the bulk builder records. Anything else => unknown (warn).
ALLOWED_LICENSES = {
    "cc0", "royalty_free", "generated_owned",
    "Pexels License", "Pixabay Content License",
}
RESTRICTED_LICENSES = {"licensed", "editorial_only"}


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def license_class(lic: str) -> str:
    if lic in ALLOWED_LICENSES:
        return "allowed"
    if lic in RESTRICTED_LICENSES:
        return "restricted"
    return "unknown"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", nargs="?", default=DEFAULT_MANIFEST)
    ap.add_argument("--schema", default=SCHEMA_PATH)
    ap.add_argument("--check-files", action="store_true",
                    help=f"sample-check that asset paths exist under {MEDIA_ROOT} (assets/)")
    args = ap.parse_args()

    try:
        schema = load(args.schema)
        doc = load(args.manifest)
    except json.JSONDecodeError as e:
        # The manifest may be mid-write by a concurrent bulk builder.
        raise SystemExit(f"Could not parse JSON ({e}). If a download is running, retry once it settles.")

    assets = doc.get("assets", []) if isinstance(doc, dict) else doc
    n = len(assets)
    validator = Draft202012Validator(schema)

    # 1. structural validation
    errors = [f"{list(e.path)}: {e.message}" for e in validator.iter_errors(doc)]

    # 2. duplicate ids
    ids = collections.Counter(a.get("id") for a in assets)
    dups = [i for i, c in ids.items() if c > 1]

    # 3. digit-width over 9999
    overflow = []
    for a in assets:
        m = re.match(r"^AF-[A-Z_]+-([0-9]+)$", a.get("id", ""))
        if m and int(m.group(1)) > 9999:
            overflow.append(a["id"])

    # 4. rights lint + stats
    by_type = collections.Counter(a.get("type") for a in assets)
    by_tool = collections.Counter(a.get("sourceTool") for a in assets)
    by_src = collections.Counter(a.get("source") for a in assets)
    by_lic = collections.Counter(a.get("license") for a in assets)
    by_rights = collections.Counter(license_class(a.get("license", "")) for a in assets)
    not_allowed = [a["id"] for a in assets if license_class(a.get("license", "")) != "allowed"]

    # optional on-disk sample existence check (deterministic stride, no randomness)
    missing = []
    if args.check_files and n:
        stride = max(1, n // 200)
        for a in assets[::stride]:
            rel = (a.get("path") or "").replace("/", os.sep)
            fp = os.path.join(MEDIA_ROOT, "assets", rel)
            if not os.path.exists(fp):
                missing.append(a.get("id"))

    # ---- report ----
    print(f"Manifest: {os.path.relpath(args.manifest, ROOT)}   entries={n}")
    print(f"schema: {doc.get('schema') if isinstance(doc, dict) else '(list)'}")
    print("by type:   " + ", ".join(f"{k}={v}" for k, v in by_type.most_common()))
    print("by tool:   " + ", ".join(f"{k}={v}" for k, v in by_tool.most_common()))
    print("by source: " + ", ".join(f"{k}={v}" for k, v in by_src.most_common()))
    print("by license:" + ", ".join(f" {k}={v}" for k, v in by_lic.most_common()))
    print(f"rights:    allowed={by_rights['allowed']} restricted={by_rights['restricted']} unknown={by_rights['unknown']}")
    print(f"Schema errors: {len(errors)} | duplicate ids: {len(dups)}")

    for e in errors[:20]:
        print("  ERROR:", e)
    if len(errors) > 20:
        print(f"  ... (+{len(errors) - 20} more schema errors)")
    for d in dups[:20]:
        print(f"  ERROR: duplicate id {d} (x{ids[d]})")

    if overflow:
        print(f"  WARN: {len(overflow)} ids exceed 9999 digits (e.g. {overflow[:3]}) -- consumers must accept >=4 digits")
    if not_allowed:
        print(f"  WARN: {len(not_allowed)} assets are NOT commercial-allowed (restricted/unknown license) -- review before timeline use (e.g. {not_allowed[:3]})")
    if args.check_files:
        print(f"  files: sampled {min(200, n)} paths under {MEDIA_ROOT}; missing={len(missing)}" +
              (f" (e.g. {missing[:3]})" if missing else ""))

    ok = not errors and not dups
    print("\nRESULT:", "PASS" if ok and not (overflow or not_allowed) else
          ("PASS (with warnings)" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
