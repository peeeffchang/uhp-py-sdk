import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.consent import Consent
from uhp.enums.consent_state import ConsentState
from uhp.state_machines.consent import ConsentStateMachine


def test_consent_initial_state_is_granted():
    # A consent should start in GRANTED state if not specified, or if specified explicitly
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        granted_at="2026-01-01T12:00:00Z"
    )
    assert consent.state == ConsentState.GRANTED

def test_consent_can_transition_from_granted_to_revoked():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        granted_at="2026-01-01T12:00:00Z"
    )
    assert ConsentStateMachine.can_transition(consent.state, ConsentState.REVOKED) is True

def test_consent_cannot_transition_from_revoked_to_granted():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.REVOKED,
        granted_at="2026-01-01T12:00:00Z",
        revoked_at="2026-01-02T12:00:00Z"
    )
    assert ConsentStateMachine.can_transition(consent.state, ConsentState.GRANTED) is False
