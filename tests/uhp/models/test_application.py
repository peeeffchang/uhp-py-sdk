import pytest
from pydantic import ValidationError
from uhp.models.application import Application
from datetime import datetime

def test_application_creation_valid_data():
    """
    Test that an Application model can be created with valid data.
    """
    application_data = {
        "application_id": "app_123",
        "job_id": "job_abc",
        "candidate_id": "cand_xyz",
        "status": "SUBMITTED",
        "submission_date": datetime(2024, 1, 1, 12, 0, 0)
    }
    application = Application(**application_data)
    assert application.application_id == "app_123"
    assert application.job_id == "job_abc"
    assert application.candidate_id == "cand_xyz"
    assert application.status == "SUBMITTED"
    assert application.submission_date == datetime(2024, 1, 1, 12, 0, 0)

def test_application_creation_missing_required_field():
    """
    Test that Application creation fails with missing required fields.
    (This assumes 'application_id' and 'job_id' are required fields).
    """
    application_data = {
        "job_id": "job_abc",
        "candidate_id": "cand_xyz"
    }
    with pytest.raises(ValidationError):
        Application(**application_data)

def test_application_creation_extra_field_forbidden():
    """
    Test that Application creation fails with extra fields if extra='forbid' is set.
    """
    application_data = {
        "application_id": "app_123",
        "job_id": "job_abc",
        "candidate_id": "cand_xyz",
        "extra_field": "should not be here"
    }
    with pytest.raises(ValidationError):
        Application(**application_data)

def test_application_immutability():
    """
    Test that Application model instances are immutable.
    """
    application_data = {
        "application_id": "app_123",
        "job_id": "job_abc",
        "candidate_id": "cand_xyz",
        "status": "SUBMITTED",
        "submission_date": datetime(2024, 1, 1, 12, 0, 0)
    }
    application = Application(**application_data)
    with pytest.raises(ValidationError): # Expect ValidationError for Pydantic v2 frozen models
        application.status = "ACCEPTED"
