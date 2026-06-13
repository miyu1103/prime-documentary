from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class Approval:
    approval_id: str
    target_id: str
    target_revision: str
    target_sha256: str
    decision: str
    decided_by: str
    decided_at: datetime

    def is_valid_for(self, *, target_id: str, revision: str, sha256: str) -> bool:
        return (
            self.decision == "approved"
            and self.target_id == target_id
            and self.target_revision == revision
            and self.target_sha256 == sha256
        )

def approval_now(**kwargs: str) -> Approval:
    return Approval(decided_at=datetime.now(timezone.utc), **kwargs)
