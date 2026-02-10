import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.enums.visibility import VisibilityLevel
from uhp.enums.consent_state import ConsentState
from uhp.enums.application_state import ApplicationState # Added import
from uhp.models.application import Application
from uhp.models.candidate import CandidateProfile
from uhp.models.consent import Consent
from uhp.models.job import Job

from uhp.privacy.visibility import filter_visible_fields
from uhp.privacy.purpose import assert_purpose_allowed


def test_filter_visible_fields_public_job():
    job = Job(
        title="Software Engineer",
        description="Develop awesome software.",
        salary_range={"min": 80000, "max": 120000},
        is_remote=True
    )
    filtered_job = filter_visible_fields(job, VisibilityLevel.PUBLIC, None)
    assert filtered_job == job.model_dump()


def test_filter_visible_fields_public_candidate_profile():
    candidate = CandidateProfile(
        candidate_id="cand789",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        skills=["Python", "Go"],
        is_open_to_remote=True
    )
    filtered_candidate = filter_visible_fields(candidate, VisibilityLevel.PUBLIC, None)
    assert filtered_candidate == candidate.model_dump()


def test_filter_visible_fields_private_candidate_profile_no_consent():
    candidate = CandidateProfile(
        candidate_id="cand789",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        skills=["Python", "Go"],
        is_open_to_remote=True
    )
    filtered_candidate = filter_visible_fields(candidate, VisibilityLevel.PRIVATE, None)
    assert filtered_candidate == {}


def test_filter_visible_fields_public_application():
    app = Application(
        application_id="app123",
        job_id="job456",
        candidate_id="cand789",
        status=ApplicationState.SUBMITTED,
        submission_date="2026-01-01T12:00:00Z"
    )
    filtered_app = filter_visible_fields(app, VisibilityLevel.PUBLIC, None)
    assert filtered_app == app.model_dump()


def test_filter_visible_fields_private_application():
    app = Application(
        application_id="app123",
        job_id="job456",
        candidate_id="cand789",
        status=ApplicationState.SUBMITTED,
        submission_date="2026-01-01T12:00:00Z"
    )
    filtered_app = filter_visible_fields(app, VisibilityLevel.PRIVATE, None)
    assert filtered_app == {}


def test_filter_visible_fields_public_consent():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        granted_at="2026-01-01T12:00:00Z"
    )
    filtered_consent = filter_visible_fields(consent, VisibilityLevel.PUBLIC, None)
    assert filtered_consent == consent.model_dump()


def test_filter_visible_fields_private_consent():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        granted_at="2026-01-01T12:00:00Z"
    )
    filtered_consent = filter_visible_fields(consent, VisibilityLevel.PRIVATE, None)
    assert filtered_consent == {}


def test_filter_visible_fields_unsupported_type():
    data = {"unknown_field": "value"}
    filtered_data = filter_visible_fields(data, VisibilityLevel.PUBLIC, None)
    assert filtered_data == {}


def test_assert_purpose_allowed_granted_consent():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        granted_at="2026-01-01T12:00:00Z"
    )
    assert assert_purpose_allowed(consent, "process_application") is True


def test_assert_purpose_allowed_denied_consent():
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.DENIED,
        granted_at="2026-01-01T12:00:00Z"
    )
    assert assert_purpose_allowed(consent, "process_application") is False