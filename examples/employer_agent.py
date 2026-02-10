import sys
import os
from datetime import datetime

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from uhp.models.candidate import CandidateProfile
from uhp.enums.visibility import VisibilityLevel
from uhp.privacy.visibility import filter_visible_fields

def demonstrate_employer_agent():
    print("--- Employer Agent Demonstration ---")

    # Scenario: Reviewing Anonymized Candidate Profiles
    candidate_original = CandidateProfile(
        candidate_id="candidate123",
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        skills=["Python", "Go", "Cloud"],
        is_open_to_remote=True
    )

    print("\n")
    print(f"Original Candidate Profile: {candidate_original.model_dump_json(indent=2)}")

    # Anonymize profile for employer review (e.g., PRIVATE visibility)
    # The filter_visible_fields function currently returns an empty dict for PRIVATE visibility
    # In a more advanced implementation, it would selectively hide fields.
    anonymized_profile = filter_visible_fields(candidate_original, VisibilityLevel.PRIVATE, None)

    print("\n")
    print(f"Anonymized Profile for Employer Review (PRIVATE visibility): {anonymized_profile}")
    assert "email" not in anonymized_profile # Assuming email is always private

    # Simulate public visibility (all fields visible)
    public_profile = filter_visible_fields(candidate_original, VisibilityLevel.PUBLIC, None)
    print("\n")
    print(f"Public Profile (PUBLIC visibility): {public_profile}")
    assert "email" in public_profile

    print("\n")
    print("Employer Agent Demonstration complete.")

if __name__ == "__main__":
    demonstrate_employer_agent()
