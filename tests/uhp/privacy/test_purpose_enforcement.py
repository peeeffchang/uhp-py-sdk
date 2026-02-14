import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.job import Job
from uhp.privacy.purpose import assert_purpose_allowed
from uhp.errors import PrivacyViolation
from uhp.models.consent import Consent
from uhp.enums.consent_state import ConsentState
from datetime import datetime

# Tests for purpose-bound access enforcement will be added here.

def test_mismatched_purpose_raises_privacy_violation():
    """
    Tests that assert_purpose_allowed raises a PrivacyViolation if the
    purpose is not included in the granted consent.
    """
    consent = Consent(
        consent_id="con123",
        actor_id="cand789",
        target_id="job456",
        state=ConsentState.GRANTED,
        purpose=["ANALYTICS", "CONTACT"], # A list of granted purposes
        granted_at=datetime(2024, 1, 1, 12, 0, 0)
    )
    with pytest.raises(PrivacyViolation, match="Purpose 'SALARY_NEGOTIATION' not granted in consent con123"):
        assert_purpose_allowed(consent, "SALARY_NEGOTIATION")

def test_matched_purpose_allows_access():
    """
    Tests that assert_purpose_allowed returns True if the
    purpose is included in the granted consent.
    """
    consent = Consent(
        consent_id="con456",
        actor_id="cand456",
        target_id="job789",
        state=ConsentState.GRANTED,
        purpose=["ANALYTICS", "SALARY_NEGOTIATION"], # A list of granted purposes
        granted_at=datetime(2024, 1, 1, 12, 0, 0)
    )
    assert assert_purpose_allowed(consent, "SALARY_NEGOTIATION") is True
