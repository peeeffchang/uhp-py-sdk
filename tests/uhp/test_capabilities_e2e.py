import pytest
import sys
import os
import importlib.util
from types import ModuleType
from uhp.models.capability import Capability
from uhp.capabilities.registry import capability_registry, process_and_register_capabilities_from_module
from uhp.capabilities.decorators import uhp_capability
from uhp.capabilities import discover_capabilities # The public API
import uhp # Import uhp to access its internal functions
from pydantic import BaseModel
from typing import Optional, Dict, Any


# Fixture to set up a dummy capability module for E2E tests
@pytest.fixture
def dummy_e2e_capability_module(tmp_path):
    module_content = """
from uhp.capabilities.decorators import uhp_capability
from pydantic import BaseModel
from typing import Optional, Dict, Any, List # Import List here

class E2EInputModel(BaseModel):
    query: str
    limit: Optional[int] = 10

class E2EOutputModel(BaseModel):
    results: List[str]
    count: int

@uhp_capability
def search_data(input_data: E2EInputModel) -> E2EOutputModel:
    '''Performs an end-to-end data search.'''
    return E2EOutputModel(results=["item1", "item2"], count=2)

@uhp_capability
def get_status() -> str:
    '''Retrieves the system status.'''
    return "System Operational"
"""
    module_path = tmp_path / "e2e_capabilities_module.py"
    module_path.write_text(module_content)

    # Add tmp_path to sys.path so our scanner can find it
    sys.path.insert(0, str(tmp_path))
    
    yield str(module_path) # Yield path to the dummy module
    
    # Clean up sys.path
    sys.path.remove(str(tmp_path))
    if "e2e_capabilities_module" in sys.modules:
        del sys.modules["e2e_capabilities_module"]


def test_e2e_discovery_api_flow(dummy_e2e_capability_module):
    """
    Tests the complete end-to-end flow of capability definition, SDK startup discovery,
    and retrieval via the public discovery API.
    This test is expected to pass if all previous components are correctly integrated.
    """
    # Clear sys.modules for uhp and related modules to force a clean re-import
    modules_to_delete = [
        m for m in sys.modules if m.startswith('uhp') or m.startswith('e2e_capabilities_module')
    ]
    for m in modules_to_delete:
        if m in sys.modules:
            del sys.modules[m]

    # Dynamically load the dummy module so its capabilities are in sys.modules
    # and can be picked up by the SDK's initialization logic
    spec = importlib.util.spec_from_file_location("e2e_capabilities_module", dummy_e2e_capability_module)
    e2e_dummy_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = e2e_dummy_module
    spec.loader.exec_module(e2e_dummy_module)

    # Force uhp to initialize with the dummy module
    # This will clear the registry and re-scan, including e2e_dummy_module
    uhp._initialize_capabilities(modules_to_scan=[e2e_dummy_module])

    # Call the public discovery API
    discovered_caps = discover_capabilities()

    # Assertions
    assert len(discovered_caps) == 2

    search_cap = next(cap for cap in discovered_caps if cap.id == "search_data")
    assert search_cap.description == "Performs an end-to-end data search."
    assert search_cap.input_schema["properties"]["input_data"]["title"] == "E2EInputModel"
    assert search_cap.output_schema["title"] == "E2EOutputModel"

    status_cap = next(cap for cap in discovered_caps if cap.id == "get_status")
    assert status_cap.description == "Retrieves the system status."
    assert status_cap.input_schema == {"type": "object", "properties": {}, "required": []}
    assert status_cap.output_schema == {"type": "string"}
