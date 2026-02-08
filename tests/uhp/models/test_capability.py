import pytest
from pydantic import ValidationError
from uhp.models.capability import CapabilityDescriptor

def test_capability_descriptor_creation_valid_data():
    """
    Test that a CapabilityDescriptor model can be created with valid data.
    """
    capability_data = {
        "capability_id": "cap_1",
        "name": "ViewJob",
        "description": "Allows viewing of job details.",
        "version": "1.0.0"
    }
    capability = CapabilityDescriptor(**capability_data)
    assert capability.capability_id == "cap_1"
    assert capability.name == "ViewJob"
    assert capability.description == "Allows viewing of job details."
    assert capability.version == "1.0.0"

def test_capability_descriptor_creation_missing_required_field():
    """
    Test that CapabilityDescriptor creation fails with missing required fields.
    (This assumes 'capability_id' and 'name' are required fields).
    """
    capability_data = {
        "name": "ViewJob",
        "version": "1.0.0"
    }
    with pytest.raises(ValidationError):
        CapabilityDescriptor(**capability_data)

def test_capability_descriptor_creation_extra_field_forbidden():
    """
    Test that CapabilityDescriptor creation fails with extra fields if extra='forbid' is set.
    """
    capability_data = {
        "capability_id": "cap_1",
        "name": "ViewJob",
        "extra_field": "should not be here"
    }
    with pytest.raises(ValidationError):
        CapabilityDescriptor(**capability_data)

def test_capability_descriptor_immutability():
    """
    Test that CapabilityDescriptor model instances are immutable.
    """
    capability_data = {
        "capability_id": "cap_1",
        "name": "ViewJob",
        "version": "1.0.0"
    }
    capability = CapabilityDescriptor(**capability_data)
    with pytest.raises(ValidationError): # Expect ValidationError for Pydantic v2 frozen models
        capability.name = "EditJob"
