import pytest
from pydantic import ValidationError
from uhp.models.candidate import CandidateProfile

def test_candidate_profile_creation_valid_data():
    """
    Test that a CandidateProfile model can be created with valid data.
    """
    candidate_data = {
        "candidate_id": "cand_123",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "skills": ["Python", "Pydantic", "FastAPI"],
        "is_open_to_remote": True
    }
    candidate = CandidateProfile(**candidate_data)
    assert candidate.candidate_id == "cand_123"
    assert candidate.first_name == "John"
    assert candidate.last_name == "Doe"
    assert candidate.email == "john.doe@example.com"
    assert candidate.skills == ["Python", "Pydantic", "FastAPI"]
    assert candidate.is_open_to_remote is True

def test_candidate_profile_creation_missing_required_field():
    """
    Test that CandidateProfile creation fails with missing required fields.
    (This assumes 'candidate_id' and 'first_name' are required fields).
    """
    candidate_data = {
        "first_name": "John",
        "email": "john.doe@example.com"
    }
    with pytest.raises(ValidationError):
        CandidateProfile(**candidate_data)

def test_candidate_profile_creation_extra_field_forbidden():
    """
    Test that CandidateProfile creation fails with extra fields if extra='forbid' is set.
    """
    candidate_data = {
        "candidate_id": "cand_123",
        "first_name": "John",
        "last_name": "Doe",
        "extra_field": "should not be here"
    }
    with pytest.raises(ValidationError):
        CandidateProfile(**candidate_data)

def test_candidate_profile_immutability():
    """
    Test that CandidateProfile model instances are immutable.
    """
    candidate_data = {
        "candidate_id": "cand_123",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    candidate = CandidateProfile(**candidate_data)
    with pytest.raises(ValidationError): # Expect ValidationError for Pydantic v2 frozen models
        candidate.first_name = "Jane"
