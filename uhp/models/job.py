from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any

class Job(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    title: str = Field(..., description="The title of the job.")
    description: str = Field(..., description="A detailed description of the job.")
    salary_range: Optional[Dict[str, float]] = Field(None, description="The salary range for the job, e.g., {'min': 80000, 'max': 120000}.")
    is_remote: bool = Field(False, description="Indicates if the job can be performed remotely.")
