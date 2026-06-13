from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

class InvalidArtifactURI(ValueError):
    pass

@dataclass(frozen=True)
class ArtifactURI:
    logical_path: PurePosixPath

    @classmethod
    def parse(cls, value: str) -> "ArtifactURI":
        prefix = "artifact://"
        if not value.startswith(prefix):
            raise InvalidArtifactURI("Artifact URI must start with artifact://")
        path = PurePosixPath(value[len(prefix):])
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise InvalidArtifactURI("Artifact URI must be a safe relative logical path")
        return cls(path)

    def resolve(self, root: Path) -> Path:
        root = root.resolve()
        candidate = (root / Path(*self.logical_path.parts)).resolve()
        if root != candidate and root not in candidate.parents:
            raise InvalidArtifactURI("Resolved path escapes artifact root")
        return candidate

    def __str__(self) -> str:
        return "artifact://" + self.logical_path.as_posix()
