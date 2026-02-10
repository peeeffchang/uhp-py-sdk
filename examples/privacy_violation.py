import sys
import os
from datetime import datetime

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uhp.models.candidate import CandidateProfile
from uhp.enums.visibility import VisibilityLevel
from uhp.enums.consent_state import ConsentState
from uhp.privacy.visibility import filter_visible_fields
from uhp.privacy.purpose import assert_purpose_allowed
from uhp.models.consent import Consent
from uhp.errors import PrivacyViolation

def demonstrate_privacy_violation():
    print("--- Privacy Violation Demonstration ---")

    candidate_full_profile = CandidateProfile(
        candidate_id="candidate123",
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com",
        skills=["Python", "AI", "Ethics"],
        is_open_to_remote=True
    )

    # Scenario 1: Attempt to access private data without consent (using filter_visible_fields)
    print("\n")
    print("--- Scenario 1: Accessing private data without consent ---")
    # Current filter_visible_fields returns empty dict for PRIVATE, effectively anonymizing
    anonymized_profile = filter_visible_fields(candidate_full_profile, VisibilityLevel.PRIVATE, None)
    print(f"Attempting to view private profile: {anonymized_profile}")
    if "email" not in anonymized_profile:
        print("Successfully prevented direct access to sensitive fields like email (anonymized).")
    else:
        print("Error: Sensitive fields were exposed.")

    # Scenario 2: Attempt to use data for an unapproved purpose (using assert_purpose_allowed)
    print("\n")
    print("--- Scenario 2: Using data for an unapproved purpose ---")
    denied_consent = Consent(
        consent_id="con456",
        actor_id=candidate_full_profile.candidate_id,
        target_id="employer789",
        state=ConsentState.DENIED,
        granted_at=datetime.now()
    )
    purpose = "share_with_third_party"
    try:
        if not assert_purpose_allowed(denied_consent, purpose):
            raise PrivacyViolation("candidate_data", f"purpose '{purpose}' not allowed with DENIED consent")
    except PrivacyViolation as e:
        print(f"Privacy Violation Caught: {e.message}")
        print("Successfully prevented data usage for unapproved purpose.")
    else:
        print("Error: Data usage for unapproved purpose was not prevented.")

    print("\n")
    print("Privacy Violation Demonstration complete.")

if __name__ == "__main__":
    demonstrate_privacy_violation()
