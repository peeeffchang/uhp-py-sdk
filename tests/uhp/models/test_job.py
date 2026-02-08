import pytest
from pydantic import ValidationError
from uhp.models.job import Job 

def test_job_creation_valid_data():
    """
    Test that a Job model can be created with valid data.
    """
    job_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software.",
        "salary_range": {"min": 80000.0, "max": 120000.0},
        "is_remote": True
    }
    job = Job(**job_data)
    assert job.title == "Software Engineer"
    assert job.description == "Develop and maintain software."
    assert job.salary_range == {"min": 80000.0, "max": 120000.0}
    assert job.is_remote is True

def test_job_creation_missing_required_field():
    """
    Test that Job creation fails with missing required fields.
    (This assumes 'title' is a required field).
    """
    job_data = {
        "description": "Develop and maintain software.",
        "salary_range": {"min": 80000, "max": 120000},
        "is_remote": True
    }
    # When Job is a Pydantic model, this should raise ValidationError
    with pytest.raises(ValidationError):
        Job(**job_data)

def test_job_creation_extra_field_forbidden():
    """
    Test that Job creation fails with extra fields if extra='forbid' is set.
    """
    job_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software.",
        "extra_field": "should not be here"
    }
    # When Job is a Pydantic model with extra='forbid', this should raise ValidationError
    with pytest.raises(ValidationError):
        Job(**job_data)

def test_job_immutability():
    """
    Test that Job model instances are immutable.
    """
    job_data = {
        "title": "Software Engineer",
        "description": "Develop and maintain software."
    }
    job = Job(**job_data)
    # When Job is a Pydantic frozen model, attempting to set an attribute should raise TypeError
    with pytest.raises(ValidationError):
        job.title = "Senior Software Engineer"
