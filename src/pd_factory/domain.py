from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

class EpisodeState(StrEnum):
    IDEA = "idea"
    SCREENING = "screening"
    APPROVED = "approved"
    PRE_RESEARCH = "pre_research"
    RESEARCHING = "researching"
    RESEARCH_READY = "research_ready"
    THESIS_READY = "thesis_ready"
    OUTLINE_READY = "outline_ready"
    SCRIPT_DRAFT = "script_draft"
    SCRIPT_REVIEW = "script_review"
    SCRIPT_VERIFIED = "script_verified"
    SCENE_PLANNED = "scene_planned"
    ASSET_PLAN_READY = "asset_plan_ready"
    ASSETS_GENERATING = "assets_generating"
    ASSETS_READY = "assets_ready"
    AUDIO_GENERATING = "audio_generating"
    AUDIO_READY = "audio_ready"
    EDIT_ASSEMBLY = "edit_assembly"
    EDIT_REVIEW = "edit_review"
    FINALIZING = "finalizing"
    PACKAGE_READY = "package_ready"
    PUBLISH_APPROVED = "publish_approved"
    UPLOADING = "uploading"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    ANALYTICS_ACTIVE = "analytics_active"
    ANALYTICS_REVIEWED = "analytics_reviewed"
    ARCHIVED = "archived"

class JobState(StrEnum):
    QUEUED = "queued"
    LEASED = "leased"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED_RETRYABLE = "failed_retryable"
    FAILED_TERMINAL = "failed_terminal"
    BLOCKED = "blocked"
    AWAITING_APPROVAL = "awaiting_approval"
    CANCELLED = "cancelled"
    SUPERSEDED = "superseded"
    DEAD_LETTER = "dead_letter"

class RiskClass(StrEnum):
    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"

class Severity(StrEnum):
    S0 = "S0"
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"

@dataclass(frozen=True)
class RevisionRef:
    entity_id: str
    revision: str
    sha256: str

@dataclass(frozen=True)
class StateEvent:
    episode_id: str
    from_state: EpisodeState
    to_state: EpisodeState
    reason: str
    actor: str
    input_revisions: tuple[RevisionRef, ...] = field(default_factory=tuple)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)
