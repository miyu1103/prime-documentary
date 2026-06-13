"""Read secrets from the repo-root `.env` (git-ignored) or the process environment.

Never writes secrets anywhere. `.env` real values must not be committed (rules/03).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


@dataclass
class EnvStore:
    """Lookup order: process env first, then `.env` file. Empty values count as missing."""

    root: Path = REPO_ROOT
    _file: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._file = _parse_env_file(self.root / ".env")

    def get(self, key: str) -> str | None:
        val = os.environ.get(key) or self._file.get(key)
        return val or None

    def require(self, key: str) -> str:
        val = self.get(key)
        if not val:
            raise KeyError(f"{key} is not set (.env or environment)")
        return val

    def present(self, *keys: str) -> bool:
        return all(self.get(k) for k in keys)


def load_env(root: Path = REPO_ROOT) -> EnvStore:
    return EnvStore(root=root)
