import pytest
import os
import sys
import importlib.util
from uhp.models.capability import Capability
from uhp.capabilities.registry import capability_registry
from types import ModuleType
from typing import List, Dict, Any
from uhp.capabilities.decorators import uhp_capability

# Re-define the fixture here or import if from test_scanner.py if possible
# For now, re-defining for self-containment of the test file.
@pytest.fixture
def dummy_capability_module(tmp_path):
    module_content = """
from uhp.capabilities.decorators import uhp_capability
import inspect
from typing import List, Dict, Any

@uhp_capability
def registerable_func_capability(param_a: str, param_b: int) -> Dict[str, Any]:
    '''A function to be registered.'''
    return {"status": "success"}

@uhp_capability
class RegisterableClassCapability:
    '''A class to be registered.'''
    def __init__(self, item_id: str):
        self.item_id = item_id
    def execute(self, action: str) -> bool:
        return True
"""
    module_path = tmp_path / "dummy_registerable_capabilities.py"
    module_path.write_text(module_content)

    sys.path.insert(0, str(tmp_path))
    
    spec = importlib.util.spec_from_file_location("dummy_registerable_capabilities", module_path)
    dummy_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = dummy_module
    spec.loader.exec_module(dummy_module)

    yield dummy_module
    
    sys.path.remove(str(tmp_path))
    if "dummy_registerable_capabilities" in sys.modules:
        del sys.modules["dummy_registerable_capabilities"]

@pytest.fixture
def pydantic_capability_module(tmp_path):
    module_content = """
from uhp.capabilities.decorators import uhp_capability
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Define a dummy Pydantic model for input
class InputModel(BaseModel):
    name: str
    age: Optional[int] = None

# Define a dummy Pydantic model for output
class OutputModel(BaseModel):
    status: str
    message: str

@uhp_capability
def pydantic_func_capability(input_data: InputModel) -> OutputModel:
    '''A capability using Pydantic models.'''
    return OutputModel(status="ok", message=f"Processed {input_data.name}")
"""
    module_path = tmp_path / "dummy_pydantic_capabilities.py"
    module_path.write_text(module_content)

    sys.path.insert(0, str(tmp_path))
    
    spec = importlib.util.spec_from_file_location("dummy_pydantic_capabilities", module_path)
    dummy_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = dummy_module
    spec.loader.exec_module(dummy_module)

    yield dummy_module
    
    sys.path.remove(str(tmp_path))
    if "dummy_pydantic_capabilities" in sys.modules:
        del sys.modules["dummy_pydantic_capabilities"]


def test_registration_process_converts_and_registers_capabilities(dummy_capability_module: ModuleType):
    """
    Test that the registration process can convert raw capabilities (functions/classes)
    into Capability Pydantic models and register them in the global capability_registry.
    """
    # Ensure the registry is clean before the test
    capability_registry._registry.clear()

    from uhp.capabilities.registry import process_and_register_capabilities_from_module

    # This function will scan the module, convert, and register
    process_and_register_capabilities_from_module(dummy_capability_module)

    # Assertions
    registered_capabilities = capability_registry.describe_all()
    assert len(registered_capabilities) == 2

    # Check the first registered capability (function)
    func_cap = next(cap for cap in registered_capabilities if cap.id == "registerable_func_capability")
    assert func_cap.id == "registerable_func_capability"
    assert func_cap.description == "A function to be registered."
    assert func_cap.input_schema == {
        "type": "object",
        "properties": {
            "param_a": {"type": "string"},
            "param_b": {"type": "integer"}
        },
        "required": ["param_a", "param_b"]
    }
    assert func_cap.output_schema == {"type": "object"} # Dict[str, Any]

    # Check the second registered capability (class)
    class_cap = next(cap for cap in registered_capabilities if cap.id == "RegisterableClassCapability")
    assert class_cap.id == "RegisterableClassCapability"
    assert class_cap.description == "A class to be registered."
    assert class_cap.input_schema == {
        "type": "object",
        "properties": {
            "item_id": {"type": "string"}
        },
        "required": ["item_id"]
    }
    assert class_cap.output_schema == {"type": "boolean"} # bool return for execute()

def test_pydantic_schema_generation_for_capabilities(pydantic_capability_module: ModuleType):
    """
    Test that the scanner correctly generates Pydantic JSON schemas for capabilities
    that use Pydantic models as input/output types.
    """
    capability_registry._registry.clear()
    from uhp.capabilities.registry import process_and_register_capabilities_from_module

    process_and_register_capabilities_from_module(pydantic_capability_module)

    registered_caps = capability_registry.describe_all()
    assert len(registered_caps) == 1
    pydantic_cap = registered_caps[0]

    assert pydantic_cap.id == "pydantic_func_capability"
    assert pydantic_cap.description == "A capability using Pydantic models."

    # Corrected expected input schema based on current scanner output
    expected_input_schema = {
        "type": "object",
        "properties": {
            "input_data": { # The parameter name is 'input_data'
                "title": "InputModel",
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "age": {
                        "anyOf": [{"type": "integer"}, {"type": "null"}],
                        "default": None,
                        "title": "Age",
                    },
                },
                "required": ["name"],
            }
        },
        "required": ["input_data"], # 'input_data' is a required parameter of the function
    }
    assert pydantic_cap.input_schema == expected_input_schema

    # Expected Pydantic JSON schema for OutputModel (direct return from _extract_return_schema_from_callable)
    expected_output_schema = {
        "title": "OutputModel",
        "type": "object",
        "properties": {
            "status": {"title": "Status", "type": "string"},
            "message": {"title": "Message", "type": "string"}
        },
        "required": ["status", "message"]
    }
    assert pydantic_cap.output_schema == expected_output_schema