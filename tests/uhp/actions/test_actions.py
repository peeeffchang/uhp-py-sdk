import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.application import Application
from uhp.models.job import Job
from uhp.enums.application_state import ApplicationState
from datetime import datetime

from uhp.actions.base import ActionRequest
from uhp.actions.apply import ApplyForJob
# from uhp.actions.withdraw import WithdrawApplication
# from uhp.actions.consent import ProposeConsent, RevokeConsent


def test_action_request_is_abstract():
    with pytest.raises(TypeError):
        ActionRequest(intent="test")

def test_apply_for_job_execution():
    job = Job(title="Dev", description="test", is_remote=True)
    candidate_id = "cand789"

    apply_action = ApplyForJob(job_id=job.title, candidate_id=candidate_id) # Using job title as job_id for simplicity in test
    result_application = apply_action.execute()

    assert isinstance(result_application, Application)
    assert result_application.job_id == job.title
    assert result_application.candidate_id == candidate_id
    assert result_application.status == ApplicationState.SUBMITTED