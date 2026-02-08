from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CapabilityDescriptor(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    capability_id: str = Field(..., description="Unique identifier for the capability.")
    name: str = Field(..., description="A human-readable name for the capability.")
    description: Optional[str] = Field(None, description="A detailed description of what the capability entails.")
    version: str = Field(..., description="The version of the capability descriptor.")
