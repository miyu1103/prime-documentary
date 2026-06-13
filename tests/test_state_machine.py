import pytest
from pd_factory.domain import EpisodeState
from pd_factory.state_machine import EpisodeStateMachine, InvalidTransition

def test_canonical_transition():
    sm = EpisodeStateMachine("PD-2026-001-example", EpisodeState.IDEA)
    event = sm.transition(EpisodeState.SCREENING, reason="candidate created", actor="test")
    assert sm.state is EpisodeState.SCREENING
    assert event.from_state is EpisodeState.IDEA

def test_invalid_skip_is_blocked():
    sm = EpisodeStateMachine("PD-2026-001-example", EpisodeState.IDEA)
    with pytest.raises(InvalidTransition):
        sm.transition(EpisodeState.PUBLISHED, reason="skip", actor="test")

def test_reason_is_required():
    sm = EpisodeStateMachine("PD-2026-001-example", EpisodeState.IDEA)
    with pytest.raises(InvalidTransition):
        sm.transition(EpisodeState.SCREENING, reason=" ", actor="test")
