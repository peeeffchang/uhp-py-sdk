from pydantic import BaseModel
from typing import Optional

class DummyInputModel(BaseModel):
    name: str
    age: Optional[int] = None

class DummyOutputModel(BaseModel):
    status: str
    message: str
