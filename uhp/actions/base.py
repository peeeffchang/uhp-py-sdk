from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Any

class ActionRequest(BaseModel, ABC):
    """
    Base class for all intent-based action requests.
    """
    intent: str = Field(..., description="The type of intent this action represents.")

    @abstractmethod
    def execute(self) -> Any:
        """
        Executes the action.
        """
        pass
