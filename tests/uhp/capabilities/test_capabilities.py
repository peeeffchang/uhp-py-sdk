import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.capability import CapabilityDescriptor

from uhp.capabilities.registry import CapabilityRegistry

def test_capability_registry_register_and_get():
    descriptor = CapabilityDescriptor(capability_id="cap1", name="Test Cap", version="1.0")
    registry = CapabilityRegistry()
    registry.register(descriptor)
    retrieved_descriptor = registry.get("cap1")
    assert retrieved_descriptor == descriptor

def test_capability_registry_describe_all():
    descriptor1 = CapabilityDescriptor(capability_id="cap1", name="Test Cap 1", version="1.0")
    descriptor2 = CapabilityDescriptor(capability_id="cap2", name="Test Cap 2", version="1.0")
    registry = CapabilityRegistry()
    registry.register(descriptor1)
    registry.register(descriptor2)
    all_descriptors = registry.describe_all()
    assert len(all_descriptors) == 2
    assert descriptor1 in all_descriptors
    assert descriptor2 in all_descriptors