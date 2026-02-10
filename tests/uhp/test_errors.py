import pytest
import sys
import os
from datetime import datetime

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from uhp.errors import InvalidStateTransition, PrivacyViolation, ConsentExpired


def test_invalid_state_transition_error_instantiation():
    error = InvalidStateTransition("DRAFT", "SUBMITTED", "Invalid transition.")
    assert error.current_state == "DRAFT"
    assert error.new_state == "SUBMITTED"
    assert "Invalid transition. Cannot transition from DRAFT to SUBMITTED." in str(error)

def test_privacy_violation_error_instantiation():
    error = PrivacyViolation("email", "access_without_consent")
    assert error.field == "email"
    assert error.reason == "access_without_consent"
    assert "Privacy violation detected. Field 'email' accessed due to 'access_without_consent'." in str(error)

def test_consent_expired_error_instantiation():
    expiration_time = datetime(2026, 1, 1, 12, 0, 0)
    error = ConsentExpired("consent123", expiration_time)
    assert error.consent_id == "consent123"
    assert "Consent 'consent123' expired on 2026-01-01T12:00:00." in str(error)