from enum import Enum

class VisibilityLevel(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    ANONYMIZED = "ANONYMIZED"
    RESTRICTED = "RESTRICTED"
