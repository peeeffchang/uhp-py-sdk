from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

# Assuming ApplicationState enum is available
# from uhp.enums.application_state import ApplicationState 

class Application(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    application_id: str = Field(..., description="Unique identifier for the application.")
    job_id: str = Field(..., description="Identifier of the job this application is for.")
    candidate_id: str = Field(..., description="Identifier of the candidate who submitted the application.")
    status: str = Field(..., description="The current status of the application, e.g., 'SUBMITTED', 'ACCEPTED'. (Will use ApplicationState enum later)")
    submission_date: datetime = Field(..., description="The date and time the application was submitted.")
    notes: Optional[str] = Field(None, description="Any additional notes or comments on the application.")
