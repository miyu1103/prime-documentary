"""Prime Documentary reference domain core.

This is deliberately small. It demonstrates contracts and safety properties; it is not the
complete production application.
"""
from .domain import EpisodeState, JobState, RiskClass, Severity
from .state_machine import EpisodeStateMachine, InvalidTransition

__all__ = [
    "EpisodeState",
    "JobState",
    "RiskClass",
    "Severity",
    "EpisodeStateMachine",
    "InvalidTransition",
]
