#!/usr/bin/env python3
"""Turn every authored design into the lines file the narration generator consumes.

gen_newshort_narration.py --text-json expects [{id, delivery, text}, ...] at
episodes/<EP>/09_package/short<NN>_lines.v001.json. The designs already hold exactly that, plus
the provenance (`source_lines`) that the generator does not need but the audit trail does — so the
provenance is carried into the file rather than dropped.

Idempotent: an existing file with identical spoken text is left alone, so re-running after a
design tweak only rewrites what actually changed.

Usage: py -3.11 scripts/emit_short_lines_from_designs.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = ROOT / "episodes" / "_planning" / "short_designs"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    written = skipped = 0
    chars = 0
    for f in sorted(DESIGNS.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        ep = d["episode_id"]
        for s in d["shorts"]:
            if not s.get("angle"):
                continue
            nn = s["short_id"].replace("short", "")
            payload = [{
                "id": l["id"],
                "delivery": l["delivery"],
                "source": "rerecord",
                "text": l["text"].strip(),
                "provenance": l.get("source_lines", []),
            } for l in s["lines"]]
            chars += sum(len(x["text"]) for x in payload)
            out = ROOT / "episodes" / ep / "09_package" / f"short{nn}_lines.v001.json"
            new = json.dumps(payload, ensure_ascii=False, indent=2)
            if out.exists():
                old = json.loads(out.read_text(encoding="utf-8"))
                if [x.get("text") for x in old] == [x["text"] for x in payload]:
                    skipped += 1
                    continue
            if not args.dry_run:
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(new, encoding="utf-8")
            written += 1

    est = chars / 1000 * 0.30
    print(f"{written} lines files {'would be ' if args.dry_run else ''}written, {skipped} unchanged")
    print(f"total spoken characters {chars:,}  -> ElevenLabs estimate ${est:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
