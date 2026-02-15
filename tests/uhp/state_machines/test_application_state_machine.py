import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.enums.application_state import ApplicationState
from uhp.state_machines.application import ApplicationStateMachine
from uhp.errors import InvalidStateTransitionError
from uhp.enums.intent import IntentType


def test_application_state_machine_initial_state():
    sm = ApplicationStateMachine()
    assert sm.current_state == ApplicationState.DRAFT

def test_application_state_machine_apply_for_job():
    sm = ApplicationStateMachine()
    sm.apply_for_job()
    assert sm.current_state == ApplicationState.SUBMITTED

def test_application_state_machine_withdraw_application_from_submitted():
    sm = ApplicationStateMachine()
    sm.apply_for_job() # Transition to SUBMITTED
    sm.withdraw_application()
    assert sm.current_state == ApplicationState.WITHDRAWN

def test_application_state_machine_cannot_apply_for_job_from_submitted():
    sm = ApplicationStateMachine()
    sm.apply_for_job() # Transition to SUBMITTED
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.apply_for_job() # Attempt to apply again
    assert excinfo.value.current_state == ApplicationState.SUBMITTED
    assert excinfo.value.intended_action == IntentType.APPLY_FOR_JOB

def test_application_state_machine_cannot_withdraw_application_from_withdrawn():
    sm = ApplicationStateMachine()
    sm.apply_for_job() # Transition to SUBMITTED
    sm.withdraw_application() # Transition to WITHDRAWN
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.withdraw_application() # Attempt to withdraw again
    assert excinfo.value.current_state == ApplicationState.WITHDRAWN
    assert excinfo.value.intended_action == IntentType.WITHDRAW_APPLICATION

def test_application_state_machine_cannot_withdraw_application_from_rejected():
    # Simulate a rejected state - need a way to set initial state for testing
    sm = ApplicationStateMachine(current_state=ApplicationState.REJECTED)
    with pytest.raises(InvalidStateTransitionError) as excinfo:
        sm.withdraw_application()
    assert excinfo.value.current_state == ApplicationState.REJECTED
    assert excinfo.value.intended_action == IntentType.WITHDRAW_APPLICATION
