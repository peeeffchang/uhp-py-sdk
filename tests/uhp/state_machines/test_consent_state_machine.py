import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.enums.consent_state import ConsentState
from uhp.state_machines.consent import ConsentStateMachine
from uhp.errors import InvalidStateTransitionError
from uhp.enums.intent import IntentType


def test_consent_state_machine_initial_state():
    sm = ConsentStateMachine()
    assert sm.current_state == ConsentState.PENDING

def test_consent_state_machine_propose_consent_granted():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=True)
    assert sm.current_state == ConsentState.GRANTED

def test_consent_state_machine_propose_consent_denied():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=False)
    assert sm.current_state == ConsentState.DENIED

def test_consent_state_machine_revoke_consent_from_granted():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=True) # Go to GRANTED
    sm.revoke_consent()
    assert sm.current_state == ConsentState.REVOKED

def test_consent_state_machine_revoke_consent_from_denied():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=False) # Go to DENIED
    sm.revoke_consent()
    assert sm.current_state == ConsentState.REVOKED

def test_consent_state_machine_cannot_propose_consent_from_granted():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=True) # Go to GRANTED
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.propose_consent(grant=True) # Attempt to propose again
    assert excinfo.value.current_state == ConsentState.GRANTED
    assert excinfo.value.intended_action == IntentType.PROPOSE_CONSENT

def test_consent_state_machine_cannot_revoke_consent_from_revoked():
    sm = ConsentStateMachine()
    sm.propose_consent(grant=True) # Go to GRANTED
    sm.revoke_consent() # Go to REVOKED
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.revoke_consent() # Attempt to revoke again
    assert excinfo.value.current_state == ConsentState.REVOKED
    assert excinfo.value.intended_action == IntentType.REVOKE_CONSENT

def test_consent_state_machine_cannot_propose_consent_from_revoked():
    sm = ConsentStateMachine(current_state=ConsentState.REVOKED)
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.propose_consent(grant=True)
    assert excinfo.value.current_state == ConsentState.REVOKED
    assert excinfo.value.intended_action == IntentType.PROPOSE_CONSENT
