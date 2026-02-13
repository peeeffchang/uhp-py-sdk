from pydantic import BaseModel, Field
from typing import Any, Dict, List

class Capability(BaseModel):
    """
    Represents a UHP capability that can be discovered by agents.
    """
    id: str = Field(..., description="A unique identifier for the capability.")
    description: str = Field(..., description="A human-readable description of the capability's purpose and functionality.")
    input_schema: Dict[str, Any] = Field(..., description="JSON schema for the input parameters of the capability's operations.")
    output_schema: Dict[str, Any] = Field(..., description="JSON schema for the expected output of the capability's operations.")
    examples: List[Dict[str, Any]] = Field(default_factory=list, description="Practical examples demonstrating how an agent can invoke and interact with the capability.")

    model_config = {
        "frozen": True,  # Make instances immutable
        "extra": "forbid" # Forbid extra fields to enforce strict schema
    }
