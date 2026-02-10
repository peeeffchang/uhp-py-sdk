import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.application import Application
from uhp.enums.application_state import ApplicationState
from uhp.state_machines.application import ApplicationStateMachine


def test_application_initial_state_is_draft():
    # An application should start in DRAFT state if not specified, or if specified explicitly
    app = Application(
        application_id="app123",
        job_id="job456",
        candidate_id="cand789",
        status=ApplicationState.DRAFT,
        submission_date="2026-01-01T12:00:00Z"
    )
    assert app.status == ApplicationState.DRAFT

def test_application_can_transition_from_draft_to_submitted():
    app = Application(
        application_id="app123",
        job_id="job456",
        candidate_id="cand789",
        status=ApplicationState.DRAFT,
        submission_date="2026-01-01T12:00:00Z"
    )
    assert ApplicationStateMachine.can_transition(app.status, ApplicationState.SUBMITTED) is True

def test_application_cannot_transition_from_submitted_to_draft():
    app = Application(
        application_id="app123",
        job_id="job456",
        candidate_id="cand789",
        status=ApplicationState.SUBMITTED,
        submission_date="2026-01-01T12:00:00Z"
    )
    assert ApplicationStateMachine.can_transition(app.status, ApplicationState.DRAFT) is False

