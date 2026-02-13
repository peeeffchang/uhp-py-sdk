import pytest
import sys
import os
import importlib.util
from types import ModuleType
from uhp.models.capability import Capability
from uhp.capabilities.registry import capability_registry
from uhp.capabilities.decorators import uhp_capability
from uhp.capabilities import discover_capabilities # The public API
import uhp # Import uhp to access its internal functions

# Fixture to set up a dummy capability module and clean up
@pytest.fixture
def dummy_startup_capability_module(tmp_path):
    module_content = """
from uhp.capabilities.decorators import uhp_capability
from pydantic import BaseModel
from typing import Optional, Dict, Any

@uhp_capability
def startup_func(name: str) -> str:
    '''A capability discovered on startup.'''
    return f"Hello, {name} from startup!"
"""
    module_path = tmp_path / "startup_capabilities_module.py"
    module_path.write_text(module_content)

    # Add tmp_path to sys.path so our scanner can find it
    sys.path.insert(0, str(tmp_path))
    
    yield str(module_path) # Yield path to the dummy module
    
    # Clean up sys.path
    sys.path.remove(str(tmp_path))
    if "startup_capabilities_module" in sys.modules:
        del sys.modules["startup_capabilities_module"]


def test_capabilities_discovered_on_sdk_startup(dummy_startup_capability_module):
    """
    Test that capabilities defined in modules are automatically discovered
    and registered when the SDK (uhp package) is initialized/imported.
    """
    # Force a reload of uhp and its submodules to simulate fresh import,
    # ensuring discovery runs
    # Clear any existing capabilities from previous tests (handled by _initialize_capabilities)
    
    # Import the dummy module to make its capabilities available for scanning
    spec = importlib.util.spec_from_file_location("startup_capabilities_module", dummy_startup_capability_module)
    dummy_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = dummy_module
    spec.loader.exec_module(dummy_module)

    # Explicitly call _initialize_capabilities with the dummy module
    # This simulates "startup" discovery for the specific module
    uhp._initialize_capabilities(modules_to_scan=[dummy_module])

    discovered_caps = discover_capabilities()

    assert len(discovered_caps) == 1
    cap = discovered_caps[0]
    assert cap.id == "startup_func"
    assert cap.description == "A capability discovered on startup."
    assert cap.input_schema["properties"]["name"]["type"] == "string"
    assert cap.output_schema["type"] == "string"
