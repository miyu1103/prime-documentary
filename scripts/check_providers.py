#!/usr/bin/env python3
"""Free/minimal provider auth checks — NO paid calls, NO uploads, NO generation.

Runs each provider's auth_check() only for keys present in .env / environment.
Owner runs this AFTER putting real keys in .env:
    py -3.11 scripts/check_providers.py
    py -3.11 scripts/check_providers.py courtlistener elevenlabs   # subset

What each check does (all read-only / free):
- courtlistener : GET one court (token check)
- elevenlabs    : GET /v1/voices (no characters spent)
- runway        : GET /v1/organization (credit balance read)
- youtube       : refresh-token -> access-token -> channels.list(mine) (read only)
"""
from __future__ import annotations

import sys
from pathlib import Path

# Be robust on Windows' cp932 console.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pd_factory.providers import load_env  # noqa: E402
from pd_factory.providers import courtlistener, elevenlabs, runway, youtube  # noqa: E402

CHECKS = {
    "courtlistener": courtlistener.auth_check,
    "elevenlabs": elevenlabs.auth_check,
    "runway": runway.auth_check,
    "youtube": youtube.auth_check,
}


def main(argv: list[str]) -> int:
    selected = [a for a in argv if a in CHECKS] or list(CHECKS)
    env = load_env()
    print("Provider auth checks (free/minimal — no paid calls):\n")
    any_fail = False
    for name in selected:
        try:
            r = CHECKS[name](env)
        except Exception as exc:  # network or parse error — report, don't crash
            r = {"provider": name, "ok": False, "status": None, "detail": f"error: {exc}"}
        mark = "OK  " if r["ok"] else "MISS"
        if not r["ok"]:
            any_fail = True
        print(f"  [{mark}] {r['provider']:<14} status={r['status']}  {r['detail']}")
    print("\nNote: MISS may simply mean the key isn't set yet. No paid operation was performed.")
    return 1 if any_fail else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
