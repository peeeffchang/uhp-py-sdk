import pytest
import sys
import os

# Add the project root to sys.path for local testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from uhp.models.capability import Capability
from uhp.capabilities.registry import capability_registry # Import the module-level singleton instance
from uhp.capabilities import uhp_capability # Import for decorator usage in tests

# Fixture to clear the registry for each test
@pytest.fixture(autouse=True)
def clear_capability_registry():
    capability_registry._registry.clear()
    yield

def test_capability_registry_register_and_get():
    descriptor = Capability(id="cap1", description="Test Cap", input_schema={}, output_schema={})
    capability_registry.register(descriptor)
    retrieved_descriptor = capability_registry.get("cap1")
    assert retrieved_descriptor == descriptor

def test_capability_registry_describe_all():
    descriptor1 = Capability(id="cap1", description="Test Cap 1", input_schema={}, output_schema={})
    descriptor2 = Capability(id="cap2", description="Test Cap 2", input_schema={}, output_schema={})
    capability_registry.register(descriptor1)
    capability_registry.register(descriptor2)
    all_descriptors = capability_registry.describe_all()
    assert len(all_descriptors) == 2
    assert descriptor1 in all_descriptors
    assert descriptor2 in all_descriptors

def test_capability_registry_is_singleton():
    """
    Test that the CapabilityRegistry behaves as a singleton (or a single source of truth).
    """
    # Register a capability
    descriptor = Capability(id="singleton_test_cap", description="Singleton Test Cap", input_schema={}, output_schema={})
    capability_registry.register(descriptor)

    # Re-import to simulate getting another "instance" (which should be the same module-level object)
    from uhp.capabilities.registry import capability_registry as another_registry_access

    # Check if the "another_registry_access" can retrieve it
    retrieved_descriptor = another_registry_access.get("singleton_test_cap")
    assert retrieved_descriptor == descriptor
    
    # Assert that the objects are indeed the same (optional, but good for true singleton check)
    assert capability_registry is another_registry_access

def test_public_discovery_api_function_returns_registered_capabilities():
    """
    Test that the public discovery API function returns all registered capabilities.
    This test is expected to fail initially because the public API function does not exist.
    """
    # Register some dummy capabilities
    cap1 = Capability(id="api_cap1", description="API Test Cap 1", input_schema={}, output_schema={})
    cap2 = Capability(id="api_cap2", description="API Test Cap 2", input_schema={}, output_schema={})
    capability_registry.register(cap1)
    capability_registry.register(cap2)

    # Placeholder for the public discovery API function
    # It could be in uhp/__init__.py or uhp/capabilities/__init__.py
    from uhp.capabilities import discover_capabilities 

    discovered = discover_capabilities()

    assert len(discovered) == 2
    assert cap1 in discovered
    assert cap2 in discovered
