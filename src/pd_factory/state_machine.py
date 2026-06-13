from __future__ import annotations
from dataclasses import dataclass
from .domain import EpisodeState, StateEvent

class InvalidTransition(ValueError):
    """Raised when an episode attempts a non-canonical transition."""

_ORDER = list(EpisodeState)
_ALLOWED: dict[EpisodeState, set[EpisodeState]] = {
    state: ({_ORDER[i + 1]} if i + 1 < len(_ORDER) else set())
    for i, state in enumerate(_ORDER)
}

# Explicit operational loops. They are narrow and must carry a reason.
_ALLOWED[EpisodeState.RESEARCH_READY].add(EpisodeState.RESEARCHING)
_ALLOWED[EpisodeState.THESIS_READY].add(EpisodeState.RESEARCHING)
_ALLOWED[EpisodeState.SCRIPT_REVIEW].add(EpisodeState.SCRIPT_DRAFT)
_ALLOWED[EpisodeState.SCRIPT_VERIFIED].add(EpisodeState.SCRIPT_REVIEW)
_ALLOWED[EpisodeState.ASSETS_GENERATING].add(EpisodeState.ASSET_PLAN_READY)
_ALLOWED[EpisodeState.EDIT_REVIEW].add(EpisodeState.EDIT_ASSEMBLY)
_ALLOWED[EpisodeState.FINALIZING].add(EpisodeState.EDIT_REVIEW)
_ALLOWED[EpisodeState.PACKAGE_READY].add(EpisodeState.FINALIZING)

@dataclass
class EpisodeStateMachine:
    episode_id: str
    state: EpisodeState

    def can_transition(self, target: EpisodeState) -> bool:
        return target in _ALLOWED[self.state]

    def transition(self, target: EpisodeState, *, reason: str, actor: str) -> StateEvent:
        if not reason.strip():
            raise InvalidTransition("Transition reason is required")
        if not self.can_transition(target):
            raise InvalidTransition(f"Invalid transition: {self.state} -> {target}")
        event = StateEvent(
            episode_id=self.episode_id,
            from_state=self.state,
            to_state=target,
            reason=reason,
            actor=actor,
        )
        self.state = target
        return event

    @staticmethod
    def allowed_targets(state: EpisodeState) -> tuple[EpisodeState, ...]:
        return tuple(sorted(_ALLOWED[state], key=lambda item: item.value))
