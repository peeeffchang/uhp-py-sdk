from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional

class CandidateProfile(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    candidate_id: str = Field(..., description="Unique identifier for the candidate.")
    first_name: str = Field(..., description="The first name of the candidate.")
    last_name: str = Field(..., description="The last name of the candidate.")
    email: EmailStr = Field(..., description="The email address of the candidate.")
    skills: List[str] = Field(default_factory=list, description="A list of skills the candidate possesses.")
    is_open_to_remote: bool = Field(False, description="Indicates if the candidate is open to remote work.")
