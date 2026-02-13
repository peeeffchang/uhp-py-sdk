import pytest
from pydantic import ValidationError
from uhp.models.capability import Capability
from typing import Dict, Any, List

def test_capability_creation_valid_data():
    """
    Test that a Capability model can be created with valid data.
    """
    capability_data = {
        "id": "job_application_submit",
        "description": "Submits a job application for a candidate.",
        "input_schema": {"type": "object", "properties": {"job_id": {"type": "string"}}},
        "output_schema": {"type": "object", "properties": {"application_id": {"type": "string"}}},
        "examples": [
            {"input": {"job_id": "job_123"}, "output": {"application_id": "app_456"}}
        ]
    }
    capability = Capability(**capability_data)
    assert capability.id == "job_application_submit"
    assert capability.description == "Submits a job application for a candidate."
    assert capability.input_schema == {"type": "object", "properties": {"job_id": {"type": "string"}}}
    assert capability.output_schema == {"type": "object", "properties": {"application_id": {"type": "string"}}}
    assert capability.examples == [
        {"input": {"job_id": "job_123"}, "output": {"application_id": "app_456"}}
    ]

def test_capability_creation_missing_required_field():
    """
    Test that Capability creation fails with missing required fields.
    """
    capability_data = {
        "description": "Submits a job application for a candidate.",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"}
    }
    with pytest.raises(ValidationError, match="Field required"):
        Capability(**capability_data)

def test_capability_creation_extra_field_forbidden():
    """
    Test that Capability creation fails with extra fields.
    """
    capability_data = {
        "id": "job_application_submit",
        "description": "Submits a job application for a candidate.",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"},
        "extra_field": "should not be here"
    }
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        Capability(**capability_data)

def test_capability_immutability():
    """
    Test that Capability model instances are immutable.
    """
    capability_data = {
        "id": "job_application_submit",
        "description": "Submits a job application for a candidate.",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"}
    }
    capability = Capability(**capability_data)
    with pytest.raises(ValidationError):
        capability.id = "new_id"

def test_capability_examples_default_empty_list():
    """
    Test that 'examples' defaults to an empty list if not provided.
    """
    capability_data = {
        "id": "test_cap",
        "description": "A test capability",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"}
    }
    capability = Capability(**capability_data)
    assert capability.examples == []

