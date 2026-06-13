from __future__ import annotations
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifact_uri import ArtifactURI
from .provenance import canonical_json, content_hash, now_iso

_REV_RE = re.compile(r"^v(\d{3})$")


class EpisodeRepoError(RuntimeError):
    pass


def next_revision(existing: list[str]) -> str:
    """Return the next vNNN revision given existing revision strings."""
    nums = [int(m.group(1)) for r in existing if (m := _REV_RE.match(r))]
    return f"v{(max(nums) + 1) if nums else 1:03d}"


@dataclass
class EpisodeRepo:
    """Immutable, revisioned artifact store for one episode directory.

    Enforces invariant 6 (never overwrite an existing revision) and invariant 7
    (every artifact carries provenance, hash and timestamps).
    """

    root: Path

    def __post_init__(self) -> None:
        self.root = Path(self.root).resolve()

    # -- manifest -------------------------------------------------------------
    @property
    def manifest_path(self) -> Path:
        return self.root / "manifest.json"

    def read_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.exists():
            raise EpisodeRepoError(f"manifest not found: {self.manifest_path}")
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, manifest: dict[str, Any]) -> None:
        manifest["updated_at"] = now_iso()
        self.manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    # -- artifacts ------------------------------------------------------------
    def existing_revisions(self, folder: str, stem: str) -> list[str]:
        directory = self.root / folder
        if not directory.exists():
            return []
        out = []
        for path in directory.glob(f"{stem}.v*.json"):
            rev = path.name[len(stem) + 1 : -len(".json")]
            if _REV_RE.match(rev):
                out.append(rev)
        return sorted(out)

    def read_artifact(self, folder: str, stem: str, revision: str) -> Any:
        return json.loads(
            (self.root / folder / f"{stem}.{revision}.json").read_text(encoding="utf-8")
        )

    def artifact_exists(self, folder: str, stem: str, revision: str) -> bool:
        return (self.root / folder / f"{stem}.{revision}.json").exists()

    def read_provenance(self, folder: str, stem: str, revision: str) -> dict | None:
        path = self.root / folder / f"{stem}.{revision}.meta.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def write_artifact(
        self, *, folder: str, stem: str, revision: str, data: Any, provenance: dict
    ) -> tuple[str, str]:
        """Write an immutable artifact + provenance sidecar.

        Returns (logical_uri, checksum). Refuses to overwrite an existing revision.
        """
        directory = self.root / folder
        directory.mkdir(parents=True, exist_ok=True)
        artifact_path = directory / f"{stem}.{revision}.json"
        if artifact_path.exists():
            raise EpisodeRepoError(
                f"refusing to overwrite immutable artifact: {artifact_path}"
            )
        # canonical_json guarantees the checksum matches the bytes we hash, while the
        # on-disk file stays human-readable (indented).
        checksum = content_hash(data)
        artifact_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (directory / f"{stem}.{revision}.meta.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        logical = ArtifactURI.parse(f"artifact://{folder}/{artifact_path.name}")
        return str(logical), checksum

    # -- event log ------------------------------------------------------------
    @property
    def events_path(self) -> Path:
        return self.root / "events.jsonl"

    def append_event(self, event: dict[str, Any]) -> None:
        event = {"ts": now_iso(), **event}
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(event) + "\n")
