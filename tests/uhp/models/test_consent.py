import pytest
from pydantic import ValidationError
from datetime import datetime
from uhp.models.consent import Consent
# from uhp.enums.consent_state import ConsentState # Will be used in Phase 3

def test_consent_creation_valid_data():
    """
    Test that a Consent model can be created with valid data.
    """
    consent_data = {
        "consent_id": "con_456",
        "actor_id": "cand_xyz",
        "target_id": "job_abc",
        "state": "GRANTED",
        "granted_at": datetime(2024, 1, 1, 12, 0, 0)
    }
    consent = Consent(**consent_data)
    assert consent.consent_id == "con_456"
    assert consent.actor_id == "cand_xyz"
    assert consent.target_id == "job_abc"
    assert consent.state == "GRANTED"
    assert consent.granted_at == datetime(2024, 1, 1, 12, 0, 0)
    assert consent.revoked_at is None

def test_consent_creation_missing_required_field():
    """
    Test that Consent creation fails with missing required fields.
    (This assumes 'consent_id' and 'actor_id' are required fields).
    """
    consent_data = {
        "actor_id": "cand_xyz",
        "target_id": "job_abc"
    }
    with pytest.raises(ValidationError):
        Consent(**consent_data)

def test_consent_creation_extra_field_forbidden():
    """
    Test that Consent creation fails with extra fields if extra='forbid' is set.
    """
    consent_data = {
        "consent_id": "con_456",
        "actor_id": "cand_xyz",
        "target_id": "job_abc",
        "extra_field": "should not be here"
    }
    with pytest.raises(ValidationError):
        Consent(**consent_data)

def test_consent_immutability():
    """
    Test that Consent model instances are immutable.
    """
    consent_data = {
        "consent_id": "con_456",
        "actor_id": "cand_xyz",
        "target_id": "job_abc",
        "state": "GRANTED",
        "granted_at": datetime(2024, 1, 1, 12, 0, 0)
    }
    consent = Consent(**consent_data)
    with pytest.raises(ValidationError): # Expect ValidationError for Pydantic v2 frozen models
        consent.state = "REVOKED"

def test_consent_creation_with_purpose():
    """
    Test that a Consent model can be created with the new 'purpose' field.
    """
    consent_data = {
        "consent_id": "con_789",
        "actor_id": "cand_abc",
        "target_id": "job_def",
        "state": "GRANTED",
        "purpose": ["ANALYTICS", "CONTACT"],
        "granted_at": datetime(2024, 1, 1, 12, 0, 0)
    }
    consent = Consent(**consent_data)
    assert consent.purpose == ["ANALYTICS", "CONTACT"]
