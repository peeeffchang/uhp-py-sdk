import pytest
import os
import sys
import importlib.util
import inspect
from uhp.models.capability import Capability
from typing import List, Dict, Any
from uhp.capabilities.decorators import uhp_capability

@pytest.fixture
def dummy_capability_module(tmp_path):
    module_content = """
from uhp.capabilities.decorators import uhp_capability # Import from the common location
import inspect
from typing import List, Dict, Any

@uhp_capability
def dummy_func_capability(param_str: str, param_int: int, param_bool: bool = False, param_float: float = 1.0) -> Dict[str, Any]:
    '''A dummy capability function.'''
    return {"result": f"{param_str}_{param_int}_{param_bool}_{param_float}"}

@uhp_capability
def func_no_annotations():
    '''Function with no annotations.'''
    pass

@uhp_capability
def func_list_return() -> List[str]:
    '''Function returning a list.'''
    return ["a", "b"]

class NotACapability:
    pass

@uhp_capability
class DummyClassCapability:
    '''A dummy class capability.'''
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value
    def execute(self, action: str) -> str:
        '''Execute method for class.'''
        return f"Hello {self.name}, executing {action} with value {self.value}"
"""
    # Create the dummy module
    module_path = tmp_path / "dummy_capabilities.py"
    module_path.write_text(module_content)

    # Add tmp_path to sys.path to allow imports
    sys.path.insert(0, str(tmp_path))
    
    # Load the dummy module
    spec = importlib.util.spec_from_file_location("dummy_capabilities", module_path)
    dummy_module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = dummy_module # Add to sys.modules
    spec.loader.exec_module(dummy_module)

    yield dummy_module # Yield the loaded module object
    
    # Clean up sys.path and sys.modules
    sys.path.remove(str(tmp_path))
    if "dummy_capabilities" in sys.modules:
        del sys.modules["dummy_capabilities"]


def test_scanner_finds_all_decorated_capabilities(dummy_capability_module):
    """
    Test that the scanner can find all functions and classes marked with @uhp_capability.
    """
    from uhp.capabilities.scanner import scan_for_capabilities 

    capabilities_found = scan_for_capabilities(dummy_capability_module)

    assert len(capabilities_found) == 4 # dummy_func_capability, func_no_annotations, func_list_return, DummyClassCapability

    # Assert specific capabilities are found by ID
    assert any(cap.id == "dummy_func_capability" for cap in capabilities_found)
    assert any(cap.id == "func_no_annotations" for cap in capabilities_found)
    assert any(cap.id == "func_list_return" for cap in capabilities_found)
    assert any(cap.id == "DummyClassCapability" for cap in capabilities_found)

    # Test details of dummy_func_capability
    func_cap = next(cap for cap in capabilities_found if cap.id == "dummy_func_capability")
    assert func_cap.description == "A dummy capability function."
    assert func_cap.input_schema == {
        'type': 'object',
        'properties': {
            'param_str': {'type': 'string'},
            'param_int': {'type': 'integer'},
            'param_bool': {'type': 'boolean'},
            'param_float': {'type': 'number'}
        },
        'required': ['param_str', 'param_int']
    }
    assert func_cap.output_schema == {'type': 'object'} # Dict[str, Any]

    # Test details of func_no_annotations
    no_anno_cap = next(cap for cap in capabilities_found if cap.id == "func_no_annotations")
    assert no_anno_cap.description == "Function with no annotations."
    assert no_anno_cap.input_schema == {'type': 'object', 'properties': {}, 'required': []}
    assert no_anno_cap.output_schema == {'type': 'null'}

    # Test details of func_list_return
    list_return_cap = next(cap for cap in capabilities_found if cap.id == "func_list_return")
    assert list_return_cap.output_schema == {'type': 'array'}

    # Test details of DummyClassCapability
    class_cap = next(cap for cap in capabilities_found if cap.id == "DummyClassCapability")
    assert class_cap.description == "A dummy class capability."
    # For classes, we expect __init__ params as input schema
    assert class_cap.input_schema == {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'value': {'type': 'integer'}
        },
        'required': ['name']
    }
    # For class, output schema is from its 'execute' method
    assert class_cap.output_schema == {'type': 'string'} # `execute` returns str
