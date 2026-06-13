#!/usr/bin/env python3
"""Basic repository secret scanner. This complements, not replaces, a dedicated scanner."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "tmp", "raw"}
PATTERNS = {
    "generic_api_key": re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
ALLOWED_SUFFIXES = {".py", ".md", ".json", ".yaml", ".yml", ".toml", ".txt", ".env", ".ini"}


def main() -> int:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in ALLOWED_SUFFIXES and path.name != ".env":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(ROOT)}:{line}: {name}")
    if findings:
        print("Potential secrets detected:")
        print("\n".join(f"- {item}" for item in findings))
        return 1
    print("No obvious secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
