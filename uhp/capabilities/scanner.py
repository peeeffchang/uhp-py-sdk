import inspect
from types import ModuleType
from typing import Any, Dict, List, get_origin, get_args
from pydantic import BaseModel # Import BaseModel

from uhp.models.capability import Capability

from uhp.capabilities.decorators import uhp_capability

def _extract_schema_from_callable(obj) -> Dict[str, Any]:
    """
    Extracts Pydantic-like JSON schema from a callable's signature.
    """
    schema = {"type": "object", "properties": {}, "required": []}
    sig = inspect.signature(obj)

    for name, param in sig.parameters.items():
        if (param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD or 
            param.kind == inspect.Parameter.KEYWORD_ONLY):
            
            # If the parameter is a Pydantic model, use its schema directly
            if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
                schema["properties"][name] = param.annotation.model_json_schema()
            elif param.annotation is not inspect.Parameter.empty:
                # Basic type mapping for non-Pydantic annotated types
                prop = {}
                if param.annotation is str:
                    prop["type"] = "string"
                elif param.annotation is int:
                    prop["type"] = "integer"
                elif param.annotation is bool:
                    prop["type"] = "boolean"
                elif param.annotation is float:
                    prop["type"] = "number"
                elif get_origin(param.annotation) is list:
                    prop["type"] = "array"
                elif get_origin(param.annotation) is dict:
                    prop["type"] = "object"
                else:
                    prop["type"] = "string"
                schema["properties"][name] = prop
            else:
                # Default to string if no annotation
                schema["properties"][name] = {"type": "string"}
            
            if param.default is inspect.Parameter.empty:
                schema["required"].append(name)
    return schema

def _extract_return_schema_from_callable(obj) -> Dict[str, Any]:
    """
    Extracts Pydantic-like JSON schema for a callable's return type.
    """
    sig = inspect.signature(obj)
    return_annotation = sig.return_annotation
    
    if return_annotation is inspect.Parameter.empty:
        return {"type": "null"} # Or {"type": "any"}
    
    # Handle Pydantic models
    if isinstance(return_annotation, type) and issubclass(return_annotation, BaseModel):
        return return_annotation.model_json_schema()
    # Basic type mapping for return
    elif return_annotation is str:
        return {"type": "string"}
    elif return_annotation is int:
        return {"type": "integer"}
    elif return_annotation is bool:
        return {"type": "boolean"}
    elif return_annotation is float:
        return {"type": "number"}
    elif get_origin(return_annotation) is list:
        return {"type": "array"}
    elif get_origin(return_annotation) is dict:
        return {"type": "object"}
    else:
        # For Pydantic models or other complex types, we might need a more sophisticated
        # mechanism, e.g., return_annotation.model_json_schema() if it's a Pydantic model
        return {"type": "object"} # Default to object for more complex types

def scan_for_capabilities(module: ModuleType) -> List[Capability]:
    """
    Scans a given module for UHP capabilities marked with the uhp_capability decorator.
    """
    capabilities: List[Capability] = []
    
    for name, obj in inspect.getmembers(module):
        if hasattr(obj, '_is_uhp_capability') and getattr(obj, '_is_uhp_capability'):
            cap_id = obj.__name__
            description = inspect.getdoc(obj) or f"Automatically discovered capability: {obj.__name__}"
            
            input_schema: Dict[str, Any] = {}
            output_schema: Dict[str, Any] = {}
            examples: List[Dict[str, Any]] = [] # Currently no way to extract from function/class directly

            if inspect.isfunction(obj):
                input_schema = _extract_schema_from_callable(obj)
                output_schema = _extract_return_schema_from_callable(obj)
            elif inspect.isclass(obj):
                # For classes, assume the __init__ method defines inputs,
                # and a special 'execute' method defines the primary action.
                # This is a simplification; a real scenario might be more complex.
                if hasattr(obj, '__init__'):
                    init_sig = inspect.signature(obj.__init__)
                    # Exclude 'self' from __init__ parameters if present
                    init_params = list(init_sig.parameters.values())
                    if init_params and init_params[0].name == 'self':
                        init_params = init_params[1:]
                    
                    class_input_schema = {"type": "object", "properties": {}, "required": []}
                    for param in init_params:
                        # If the parameter is a Pydantic model, use its schema directly
                        if isinstance(param.annotation, type) and issubclass(param.annotation, BaseModel):
                            class_input_schema["properties"][param.name] = param.annotation.model_json_schema()
                        elif param.annotation is not inspect.Parameter.empty:
                            prop = {}
                            if param.annotation is str: prop["type"] = "string"
                            elif param.annotation is int: prop["type"] = "integer"
                            else: prop["type"] = "string" # Default for other types
                            class_input_schema["properties"][param.name] = prop
                        else:
                            class_input_schema["properties"][param.name] = {"type": "string"} # Default if no annotation
                        
                        if param.default is inspect.Parameter.empty:
                            class_input_schema["required"].append(param.name)
                    input_schema = class_input_schema
                
                if hasattr(obj, 'execute') and inspect.isfunction(obj.execute):
                    output_schema = _extract_return_schema_from_callable(obj.execute)


            capabilities.append(
                Capability(
                    id=cap_id,
                    description=description,
                    input_schema=input_schema,
                    output_schema=output_schema,
                    examples=examples
                )
            )
            
    return capabilities
