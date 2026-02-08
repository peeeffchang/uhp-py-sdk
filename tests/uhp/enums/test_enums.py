# tests/uhp/enums/test_enums.py
import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# These imports are expected to fail initially (before implementation)
from uhp.enums.visibility import VisibilityLevel
from uhp.enums.application_state import ApplicationState
from uhp.enums.consent_state import ConsentState
from uhp.enums.intent import IntentType

def test_visibility_level_enum_members():
    assert VisibilityLevel.PUBLIC.value == "PUBLIC"
    assert VisibilityLevel.PRIVATE.value == "PRIVATE"

def test_application_state_enum_members():
    assert ApplicationState.DRAFT.value == "DRAFT"
    assert ApplicationState.SUBMITTED.value == "SUBMITTED"
    assert ApplicationState.ACCEPTED.value == "ACCEPTED"

def test_consent_state_enum_members():
    assert ConsentState.GRANTED.value == "GRANTED"
    assert ConsentState.DENIED.value == "DENIED"
    assert ConsentState.REVOKED.value == "REVOKED"

def test_intent_type_enum_members():
    assert IntentType.APPLY_FOR_JOB.value == "APPLY_FOR_JOB"
    assert IntentType.WITHDRAW_APPLICATION.value == "WITHDRAW_APPLICATION"
    assert IntentType.PROPOSE_CONSENT.value == "PROPOSE_CONSENT"
    assert IntentType.REVOKE_CONSENT.value == "REVOKE_CONSENT"