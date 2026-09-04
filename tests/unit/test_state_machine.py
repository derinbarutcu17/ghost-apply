import pytest

from ghost_apply.state_machine import StateMachine


def test_happy_path_requires_confirmation_evidence():
    machine = StateMachine()
    for state in ("researched", "tailored", "PDF-QA-passed", "form-reviewed", "submitted-pending-confirmation"):
        machine.transition(state, {"source": "fixture"})
    with pytest.raises(ValueError, match="confirmation"):
        machine.transition("confirmed")
    machine.transition("confirmed", {"confirmation_text": "Application received"})
    assert machine.state == "confirmed"


def test_blocked_state_requires_explicit_resume():
    machine = StateMachine()
    machine.block("CAPTCHA requires user")
    with pytest.raises(ValueError, match="resumed"):
        machine.transition("researched")
    machine.resume("draft", {"resolved": True})
    assert machine.state == "draft"


def test_invalid_skip_is_rejected():
    with pytest.raises(ValueError, match="Invalid transition"):
        StateMachine().transition("tailored")
