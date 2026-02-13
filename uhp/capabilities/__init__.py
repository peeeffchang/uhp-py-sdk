from uhp.capabilities.registry import capability_registry
from typing import List
from uhp.models.capability import Capability
from uhp.capabilities.decorators import uhp_capability

def discover_capabilities() -> List[Capability]:
    """
    Returns a list of all discovered and registered UHP capabilities.
    """
    return capability_registry.describe_all()