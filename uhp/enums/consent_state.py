from enum import Enum

class ConsentState(str, Enum):
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    REVOKED = "REVOKED"
    PENDING = "PENDING"
