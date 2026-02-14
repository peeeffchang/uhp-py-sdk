from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uhp.enums.consent_state import ConsentState

# Assuming ConsentState enum is available
# from uhp.enums.consent_state import ConsentState

class Consent(BaseModel):
    model_config = ConfigDict(frozen=True, extra='forbid')

    consent_id: str = Field(..., description="Unique identifier for the consent record.")
    actor_id: str = Field(..., description="Identifier of the actor granting/revoking consent (e.g., candidate_id).")
    target_id: str = Field(..., description="Identifier of the entity consent is granted for (e.g., job_id, another candidate_id).")
    state: ConsentState = Field(..., description="The current state of the consent.")
    purpose: Optional[List[str]] = Field(None, description="A list of specific purposes for which consent is granted.")
    granted_at: datetime = Field(..., description="The date and time the consent was granted.")
    revoked_at: Optional[datetime] = Field(None, description="The date and time the consent was revoked, if applicable.")
