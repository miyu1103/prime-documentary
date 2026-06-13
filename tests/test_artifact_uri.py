from pathlib import Path
import pytest
from pd_factory.artifact_uri import ArtifactURI, InvalidArtifactURI

def test_safe_artifact_uri(tmp_path: Path):
    uri = ArtifactURI.parse("artifact://episodes/PD-2026-001/file.json")
    assert uri.resolve(tmp_path) == tmp_path / "episodes" / "PD-2026-001" / "file.json"

def test_escape_is_rejected():
    with pytest.raises(InvalidArtifactURI):
        ArtifactURI.parse("artifact://../secret")
